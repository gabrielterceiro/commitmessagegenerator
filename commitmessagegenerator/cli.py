import argparse
import subprocess
from .generator import gerar_mensagem_commit
from .configure import api_key, get_configured_model, get_auto_add_setting, update_setting, get_api_key_status
import sys
import getpass

MODEL_MAP = {
    "1": "gemini-2.0-flash",
    "2": "gemini-1.5-flash", 
    "3": "gemini-1.5-pro",
    "4": "gemini-2.0-flash-exp",
    "5": "gemini-2.5-flash",
    "6": "gemini-2.5-pro"
}

def configure_menu():
    """Interactive configuration menu"""
    while True:
        # Get current settings
        api_set = get_api_key_status()
        current_model = get_configured_model()
        auto_add = get_auto_add_setting()
        
        print("\n" + "="*40)
        print("       CONFIGURATION MENU")
        print("="*40)
        print(f"\n1. API Key        [{('✓ Set' if api_set else '✗ Not set')}]")
        print(f"2. Model          [{current_model}]")
        print(f"3. File staging   [{('Auto-add all' if auto_add else 'Staged only')}]")
        print("\n0. Exit")
        print("="*40)
        
        choice = input("\nSelect option (0-3): ").strip()
        
        if choice == "0" or choice == "":
            print("\nExiting configuration.\n")
            break
        elif choice == "1":
            configure_api_key()
        elif choice == "2":
            configure_model()
        elif choice == "3":
            configure_staging()
        else:
            print("\nInvalid option. Please try again.")

def configure_api_key():
    """Configure the API key"""
    print("\n" + "-"*40)
    print("API KEY CONFIGURATION")
    print("-"*40)
    print("Enter your Gemini API key below.")
    print("Press Enter without typing to cancel.\n")
    
    key = getpass.getpass("API Key: ")
    
    if not key.strip():
        print("\nNo changes made.")
        return
    
    update_setting("GEMINI_API_KEY", key)
    print("\n✓ API Key saved successfully!")

def configure_model():
    """Configure the AI model"""
    current_model = get_configured_model()
    
    print("\n" + "-"*40)
    print("MODEL CONFIGURATION")
    print("-"*40)
    print(f"Current model: {current_model}\n")
    print("Available models:")
    print("1. gemini-2.0-flash (fast and efficient)")
    print("2. gemini-1.5-flash (good balance)")
    print("3. gemini-1.5-pro (highest quality, slower)")
    print("4. gemini-2.0-flash-exp (experimental)")
    print("5. gemini-2.5-flash (latest, fast)")
    print("6. gemini-2.5-pro (latest, highest quality)")
    print("\n0. Cancel")
    
    choice = input("\nSelect model (0-6): ").strip()
    
    if choice == "0" or choice == "":
        print("\nNo changes made.")
        return
    
    if choice in MODEL_MAP:
        selected_model = MODEL_MAP[choice]
        update_setting("AI_MODEL", selected_model)
        print(f"\n✓ Model changed to: {selected_model}")
    else:
        print("\nInvalid option. No changes made.")

def configure_staging():
    """Configure file staging behavior"""
    auto_add = get_auto_add_setting()
    
    print("\n" + "-"*40)
    print("FILE STAGING CONFIGURATION")
    print("-"*40)
    print(f"Current setting: {'Auto-add all files' if auto_add else 'Staged only'}\n")
    print("1. Auto-add all files - Automatically stages all changes")
    print("2. Staged only - Only use already staged files")
    print("\n0. Cancel")
    
    choice = input("\nSelect behavior (0-2): ").strip()
    
    if choice == "0" or choice == "":
        print("\nNo changes made.")
        return
    
    if choice == "1":
        update_setting("AUTO_ADD_ALL", "true")
        print("\n✓ Set to: Auto-add all files")
    elif choice == "2":
        update_setting("AUTO_ADD_ALL", "false")
        print("\n✓ Set to: Staged only")
    else:
        print("\nInvalid option. No changes made.")

def main():
    parser = argparse.ArgumentParser(description="Gerador de mensagens de commit com IA")
    parser.add_argument("-c", "--commit", action="store_true", help="Commits with the generated message")
    parser.add_argument("-cp", "--commitpush",  action="store_true", help="Commits and pushes with the generated message")
    parser.add_argument("-cf", "--configure", action="store_true", help="Configures the GEMINI_API_KEY environment variable")
    parser.add_argument("-s", "--status", action="store_true", help="Shows current configuration status")
    args = parser.parse_args()

    if args.status:
        from .configure import get_configured_model, get_auto_add_setting
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        key = os.getenv("GEMINI_API_KEY")
        model = get_configured_model()
        auto_add = get_auto_add_setting()
        
        print("\nCurrent Configuration:")
        print(f"API Key: {'✓ Set' if key else '✗ Not set'}")
        print(f"Model: {model}")
        print(f"Auto-add all files: {'✓ Yes' if auto_add else '✗ No (staged only)'}")
        return

    if not args.configure:
        mensagem = gerar_mensagem_commit()

        if "No changes detected" in mensagem:
            print(mensagem)
            return

        print("\nGenerated commit message:\n" + mensagem)

    if args.commit or args.commitpush:
        print("\nCommitting changes...")
        subprocess.run(["git", "commit", "-m", mensagem])

    if args.commitpush:
        print("\nPushing changes...")
        subprocess.run(["git", "push"])
    
    if args.configure:
        configure_menu()
    
    if len(sys.argv) == 1:
        print("\nRemoving staged changes (git reset)...")
        subprocess.run(["git", "reset"])
