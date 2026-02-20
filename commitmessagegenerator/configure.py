import os
from pathlib import Path
from dotenv import load_dotenv


GLOBAL_ENV_PATH = Path.home() / ".commitgen" / ".env"
CONFIG_SCOPES = {"auto", "local", "global"}


def _iter_local_env_candidates():
    """Yield .env paths from cwd up to filesystem root."""
    current = Path.cwd().resolve()
    for directory in (current, *current.parents):
        yield directory / ".env"


def resolve_local_env_path():
    """Resolve an existing local .env from cwd up to filesystem root."""
    for candidate in _iter_local_env_candidates():
        if candidate.exists():
            return candidate
    return None


def resolve_env_path():
    """Resolve the best available config file path."""
    local_path = resolve_local_env_path()
    if local_path is not None:
        return local_path
    if GLOBAL_ENV_PATH.exists():
        return GLOBAL_ENV_PATH
    return None


def resolve_writable_env_path(scope="auto"):
    """
    Resolve where settings should be written.

    scope:
    - auto: existing local .env, then existing global .env, else new global .env
    - local: .env in current working directory
    - global: ~/.commitgen/.env
    """
    if scope not in CONFIG_SCOPES:
        raise ValueError(f"Invalid config scope: {scope}")

    if scope == "local":
        return Path.cwd().resolve() / ".env"

    if scope == "global":
        return GLOBAL_ENV_PATH

    existing_path = resolve_env_path()
    if existing_path is not None:
        return existing_path
    return GLOBAL_ENV_PATH


def load_config_env():
    """
    Load configuration from the resolved .env path (if found).
    Returns the loaded path or None.
    """
    env_path = resolve_env_path()
    if env_path is not None:
        load_dotenv(dotenv_path=env_path, override=False)
        return env_path
    load_dotenv(override=False)
    return None

def update_setting(setting_name, value, scope="auto"):
    """Update a single setting in the .env file"""
    env_path = resolve_writable_env_path(scope=scope)
    env_path.parent.mkdir(parents=True, exist_ok=True)

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        found = False
        new_lines = []
        for line in lines:
            key_name = line.split("=")[0] if "=" in line else None
            if key_name == setting_name:
                new_lines.append(f"{setting_name}={value}\n")
                found = True
            else:
                new_lines.append(line)
        
        if not found:
            new_lines.append(f"{setting_name}={value}\n")
        
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    else:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"{setting_name}={value}\n")
    
    _ensure_gitignore(env_path)

def _ensure_gitignore(env_path):
    """Ensure .env is in .gitignore for local (non-global) config files."""
    if env_path == GLOBAL_ENV_PATH:
        return

    gitignore_path = env_path.parent / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r+", encoding="utf-8") as outfile:
            lines = outfile.readlines()
            env_in_gitignore = next((line for line in lines if line.strip() == ".env"), None)
            if not env_in_gitignore:
                outfile.write("\n.env")

def api_key(key, model="gemini-2.0-flash", auto_add_all=True, scope="auto"):
    """Set all configuration at once (legacy function)"""
    config = {
        "GEMINI_API_KEY": key,
        "AI_MODEL": model,
        "AUTO_ADD_ALL": str(auto_add_all).lower()
    }

    env_path = resolve_writable_env_path(scope=scope)
    env_path.parent.mkdir(parents=True, exist_ok=True)

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        existing_keys = set()
        new_lines = []
        for line in lines:
            key_name = line.split("=")[0] if "=" in line else None
            if key_name in config:
                new_lines.append(f"{key_name}={config[key_name]}\n")
                existing_keys.add(key_name)
            else:
                new_lines.append(line)
        
        for key_name, value in config.items():
            if key_name not in existing_keys:
                new_lines.append(f"{key_name}={value}\n")
        
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    else:
        with open(env_path, "w", encoding="utf-8") as f:
            for key_name, value in config.items():
                f.write(f"{key_name}={value}\n")

    _ensure_gitignore(env_path)

def get_api_key_status():
    """Check if API key is set"""
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return True

    env_path = resolve_env_path()
    if env_path is not None:
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            api_line = next((line for line in lines if line.startswith("GEMINI_API_KEY=")), None)
            if api_line:
                value = api_line.split("=", 1)[1].strip()
                return bool(value)
    return False

def get_configured_model():
    """Get the currently configured AI model from .env file"""
    env_model = os.getenv("AI_MODEL")
    if env_model:
        return env_model

    env_path = resolve_env_path()
    if env_path is not None:
        with open(env_path, "r", encoding="utf-8") as outfile:
            lines = outfile.readlines()
            model_line = next((line for line in lines if line.startswith("AI_MODEL=")), None)
            if model_line:
                return model_line.split("=", 1)[1].strip()
    return "gemini-2.0-flash"  # Default fallback

def get_auto_add_setting():
    """Get the auto-add all files setting from .env file"""
    env_auto_add = os.getenv("AUTO_ADD_ALL")
    if env_auto_add is not None:
        return env_auto_add.strip().lower() == "true"

    env_path = resolve_env_path()
    if env_path is not None:
        with open(env_path, "r", encoding="utf-8") as outfile:
            lines = outfile.readlines()
            auto_add_line = next((line for line in lines if line.startswith("AUTO_ADD_ALL=")), None)
            if auto_add_line:
                return auto_add_line.split("=", 1)[1].strip().lower() == "true"
    return True  # Default: auto-add all files (current behavior)
