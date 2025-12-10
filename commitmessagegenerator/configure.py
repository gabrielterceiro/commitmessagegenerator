import os

def update_setting(setting_name, value):
    """Update a single setting in the .env file"""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
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
        
        with open(".env", "w") as f:
            f.writelines(new_lines)
    else:
        with open(".env", "w") as f:
            f.write(f"{setting_name}={value}\n")
    
    _ensure_gitignore()

def _ensure_gitignore():
    """Ensure .env is in .gitignore"""
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r+") as outfile:
            lines = outfile.readlines()
            env_in_gitignore = next((line for line in lines if line.strip() == ".env"), None)
            if not env_in_gitignore:
                outfile.write("\n.env")

def api_key(key, model="gemini-2.0-flash", auto_add_all=True):
    """Set all configuration at once (legacy function)"""
    config = {
        "GEMINI_API_KEY": key,
        "AI_MODEL": model,
        "AUTO_ADD_ALL": str(auto_add_all).lower()
    }
    
    if os.path.exists(".env"):
        with open(".env", "r") as f:
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
        
        with open(".env", "w") as f:
            f.writelines(new_lines)
    else:
        with open(".env", "w") as f:
            for key_name, value in config.items():
                f.write(f"{key_name}={value}\n")

    _ensure_gitignore()

def get_api_key_status():
    """Check if API key is set"""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()
            api_line = next((line for line in lines if line.startswith("GEMINI_API_KEY=")), None)
            if api_line:
                value = api_line.split("=", 1)[1].strip()
                return bool(value)
    return False

def get_configured_model():
    """Get the currently configured AI model from .env file"""
    if os.path.exists(".env"):
        with open(".env", "r") as outfile:
            lines = outfile.readlines()
            model_line = next((line for line in lines if line.startswith("AI_MODEL=")), None)
            if model_line:
                return model_line.split("=", 1)[1].strip()
    return "gemini-2.0-flash"  # Default fallback

def get_auto_add_setting():
    """Get the auto-add all files setting from .env file"""
    if os.path.exists(".env"):
        with open(".env", "r") as outfile:
            lines = outfile.readlines()
            auto_add_line = next((line for line in lines if line.startswith("AUTO_ADD_ALL=")), None)
            if auto_add_line:
                return auto_add_line.split("=", 1)[1].strip().lower() == "true"
    return True  # Default: auto-add all files (current behavior)
