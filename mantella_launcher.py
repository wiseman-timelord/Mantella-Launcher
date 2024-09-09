# Script: .\mantella_launcher.py

# Imports
import os, sys, time, shutil, traceback, subprocess  # Common Imports
import configparser, json  # Config/Json Related

# Global variables
OUTPUT_FILE = '.\\data\\temporary_batch.txt'
game = "Skyrim"
optimization = "Default"
game_folders = {}
mod_folders = {}
xvasynth_folder = ""
model_id = ""
custom_token_count = 8192    # Default value
lmstudio_api_url = "http://localhost:1234/v1/models"
microphone_enabled = False
FILE_NAME = ''
DOCUMENTS_FOLDER = ''

# Initialization
def verbose_print(message):
    print(message, file=sys.stderr)
    sys.stderr.flush()
def delay(seconds=1):
    time.sleep(seconds)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def get_documents_folder():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
    return os.path.expandvars(winreg.QueryValueEx(key, "Personal")[0])

# Optimization presets
optimization_presets = {
    "Default": {"max_tokens": 250, "max_response_sentences": 999, "temperature": 1.0},
    "Faster": {"max_tokens": 100, "max_response_sentences": 1, "temperature": 0.4},
    "Regular": {"max_tokens": 150, "max_response_sentences": 2, "temperature": 0.5},
    "Quality": {"max_tokens": 200, "max_response_sentences": 3, "temperature": 0.6}
}

def get_or_set_models_drive():
    json_file_path = os.path.join("data", "temporary_launcher.json")
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    
    try:
        # Try to read the existing JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            models_drive_letter = data.get('models_drive_letter')
        
        if models_drive_letter:
            verbose_print(f"Using saved models drive: {models_drive_letter}")
            return models_drive_letter
    except FileNotFoundError:
        verbose_print("No saved models drive found.")
    except json.JSONDecodeError:
        verbose_print("Error reading JSON file. Will create a new one.")
    
    # If we couldn't get the drive letter from the file, ask the user
    models_drive_letter = input("Enter the drive letter where your models are stored (e.g., C, D, E): ").upper()
    
    # Save the drive letter to the JSON file
    with open(json_file_path, 'w') as f:
        json.dump({'models_drive_letter': models_drive_letter}, f)
    
    verbose_print(f"Saved models drive: {models_drive_letter}")
    return models_drive_letter

def get_config_from_file():
    txt_file_path = os.path.join("data", "config_paths.txt")  # Path to your text file
    try:
        with open(txt_file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                config_ini_path = lines[0].strip()  # First line: path to config.ini
                xvasynth_folder = lines[1].strip()  # Second line: xVASynth folder
                return config_ini_path, xvasynth_folder
            else:
                verbose_print("Config paths file doesn't contain enough lines.")
                return None, None
    except FileNotFoundError:
        verbose_print(f"Config paths file not found: {txt_file_path}")
        return None, None

def read_config():
    verbose_print(f"Reading config file from: {FILE_NAME}")
    global game, optimization, custom_token_count, game_folders, mod_folders, microphone_enabled
    config = configparser.ConfigParser()

    try:
        config.read(FILE_NAME)
    except configparser.Error as e:
        verbose_print(f"Error reading config.ini file: {str(e)}")
        delay(3)
        return

    # Get the game name
    game = config.get("Game", "game", fallback="Skyrim")

    # Fetch paths based on sections and keys
    game_folders = {
        "skyrim": config.get("Paths", "skyrim_folder", fallback="Not set"),
        "skyrimvr": config.get("Paths", "skyrimvr_folder", fallback="Not set"),
        "fallout4": config.get("Paths", "fallout4_folder", fallback="Not set"),
        "fallout4vr": config.get("Paths", "fallout4vr_folder", fallback="Not set"),
    }

    mod_folders = {
        "skyrim": config.get("Paths", "skyrim_mod_folder", fallback="Not set"),
        "skyrimvr": config.get("Paths", "skyrim_mod_folder", fallback="Not set"),
        "fallout4": config.get("Paths", "fallout4_mod_folder", fallback="Not set"),
        "fallout4vr": config.get("Paths", "fallout4vr_mod_folder", fallback="Not set"),
    }

    # Set xVASynth folder
    xvasynth_folder = config.get("Paths", "xvasynth_folder", fallback="Not set")

    # Fetch Language Model settings
    custom_token_count = int(config.get("LanguageModel.Advanced", "custom_token_count", fallback="2048"))

    # Check for optimization preset
    max_tokens = int(config.get("LanguageModel.Advanced", "max_tokens", fallback="250"))
    max_response_sentences = int(config.get("LanguageModel", "max_response_sentences", fallback="999"))
    temperature = float(config.get("LanguageModel.Advanced", "temperature", fallback="1.0"))

    for preset, values in optimization_presets.items():
        if (
            max_tokens == values["max_tokens"]
            and max_response_sentences == values["max_response_sentences"]
            and abs(temperature - values["temperature"]) < 0.01
        ):
            optimization = preset
            break
    else:
        optimization = "Default"

    # Read microphone setting
    microphone_enabled = config.getboolean("Microphone", "microphone_enabled", fallback=False)

    verbose_print(f"Read Keys: config.ini.")
    delay(2)

def write_config():
    verbose_print("Writing config file...")
    global microphone_enabled
    config = configparser.ConfigParser()
    
    try:
        config.read(FILE_NAME)
    except configparser.Error as e:
        verbose_print(f"Error reading existing config for writing: {str(e)}")
        delay(3)
        return
    
    if "Game" not in config:
        config["Game"] = {}
    config["Game"]["game"] = game
    
    if "LanguageModel.Advanced" not in config:
        config["LanguageModel.Advanced"] = {}
    config["LanguageModel.Advanced"]["custom_token_count"] = str(custom_token_count)
    
    preset = optimization_presets[optimization]
    config["LanguageModel.Advanced"]["max_tokens"] = str(preset["max_tokens"])
    config["LanguageModel.Advanced"]["temperature"] = str(preset["temperature"])
    
    if "LanguageModel" not in config:
        config["LanguageModel"] = {}
    config["LanguageModel"]["max_response_sentences"] = str(preset["max_response_sentences"])
    config["LanguageModel"]["model"] = model_id
    
    if "Microphone" not in config:
        config["Microphone"] = {}
    config["Microphone"]["microphone_enabled"] = str(int(microphone_enabled))
    
    # Add the Speech section and tts_service key
    if "Speech" not in config:
        config["Speech"] = {}
    config["Speech"]["tts_service"] = "xVASynth"

    # Add the LM Studio API key
    if "LanguageModel.Advanced" not in config:
        config["LanguageModel.Advanced"] = {}
    config["LanguageModel.Advanced"]["llm_api"] = "http://localhost:1234/v1"
    
    try:
        os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)
        with open(FILE_NAME, 'w') as configfile:
            config.write(configfile)
        verbose_print("Config file updated successfully.")
    except Exception as e:
        verbose_print(f"Error writing config: {str(e)}")
        delay(3)
    delay(2)

def write_output_file(exit_code):
    verbose_print(f"Writing output file")
    try:
        game_key = game.lower().replace(" ", "")
        game_folder = game_folders.get(game_key, "Not set")
        with open(OUTPUT_FILE, 'w') as f:
            f.write(f"exit_code={exit_code}\n")
            f.write(f"xvasynth_folder={xvasynth_folder}\n")  # Updated from the text file
            f.write(f"game={game}\n")
            f.write(f"game_folder={game_folder}")
        verbose_print(f"Output file written successfully: {OUTPUT_FILE}")
    except Exception as e:
        verbose_print(f"Error writing output file: {str(e)}")

def fetch_model_details_ollama():
    global model_id
    config = configparser.ConfigParser()

    try:
        config.read(FILE_NAME)

        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().split('\n')
        filtered_output = '\n'.join([line for line in output_lines if not line.startswith("failed to get console mode")])
        lines = [line for line in filtered_output.splitlines() if not line.startswith("failed to get console mode")]

        if len(lines) < 2:
            verbose_print("No models currently loaded in Ollama.")
            model_id = "No model loaded"
            return

        model_line = lines[1]
        verbose_print(f"Model line: {model_line}")

        model_parts = model_line.split()
        if len(model_parts) < 1:
            verbose_print(f"Unexpected format in 'ollama ps' output: {model_line}")
            model_id = "Unexpected model format"
            return

        model_name = model_parts[0].split(':')[0]
        verbose_print(f"Detected model name: {model_name}")

        model_folder_name = model_name.replace("IQ3_M-imat", "GGUF-IQ-Imatrix")

        models_drive_letter = get_or_set_models_drive()

        found = False
        for root, dirs, files in os.walk(f"{models_drive_letter}:\\"):
            verbose_print(f"Searching in directory: {root}")
            if model_folder_name in dirs:
                full_path = os.path.join(root, model_folder_name)
                verbose_print(f"Found model folder: {full_path}")

                path_parts = full_path.split(os.path.sep)
                if len(path_parts) >= 2:
                    author_folder = path_parts[-2]
                    model_folder = path_parts[-1]
                    model_id = f"{author_folder}\\{model_folder}"
                    verbose_print(f"Extracted model ID: {model_id}")

                    if "LanguageModel" not in config:
                        config["LanguageModel"] = {}
                    config["LanguageModel"]["model"] = model_id

                    with open(FILE_NAME, 'w') as configfile:
                        config.write(configfile)

                    verbose_print(f"Model Read: Ollama - {model_id}")
                    found = True
                    break
        
        if not found:
            verbose_print(f"Model folder not found for {model_folder_name}")
            model_id = "Model folder not found"

    except subprocess.CalledProcessError as e:
        verbose_print(f"Error running 'ollama ps' command: {e}")
        verbose_print(f"Command output: {e.stderr}")
        model_id = "Error running Ollama command"
    except Exception as e:
        verbose_print(f"Error fetching model details from Ollama: {str(e)}")
        traceback.print_exc()
        model_id = "Error occurred"

    delay(1)

def fetch_model_details_lmstudio():
    global model_id
    config = configparser.ConfigParser()

    try:
        config.read(FILE_NAME)
        try:
            result = subprocess.run(['curl', lmstudio_api_url], capture_output=True, text=True, check=True)
            model_data = json.loads(result.stdout)
            
            if 'data' in model_data and len(model_data['data']) > 0:
                full_id = model_data['data'][0]['id']
                model_id = full_id.rsplit('/', 1)[0]

                if "LanguageModel" not in config:
                    config["LanguageModel"] = {}
                config["LanguageModel"]["model"] = model_id

                with open(FILE_NAME, 'w') as configfile:
                    config.write(configfile)

                verbose_print(f"Model Read: LM Studio - {model_id}")
            else:
                verbose_print("No models currently loaded in LM Studio.")
                model_id = "No model loaded"
        except subprocess.CalledProcessError as e:
            verbose_print(f"Error running curl command: {e}")
            verbose_print(f"Curl output: {e.stderr}")
            model_id = "Error fetching model"
        except json.JSONDecodeError:
            verbose_print("Error parsing JSON from curl output")
            model_id = "Error parsing model data"
    except Exception as e:
        verbose_print(f"Error fetching model details: {str(e)}")
        traceback.print_exc()
        model_id = "Error occurred"

    delay(1)

def check_and_update_prompts():
    verbose_print("Checking Prompts")
    config = configparser.ConfigParser()
    config.read(FILE_NAME)

    prompt_keys = [
        "skyrim_prompt", "skyrim_multi_npc_prompt", "fallout4_prompt", 
        "fallout4_multi_npc_prompt", "radiant_start_prompt", "radiant_end_prompt", 
        "memory_prompt", "resummarize_prompt"
    ]

    updated_prompts = {
        "skyrim_prompt": "Shortened for editing.",
        
        "skyrim_multi_npc_prompt": "Shortened for editing.",
        
        "fallout4_prompt": "Shortened for editing.",
        
        "fallout4_multi_npc_prompt": "Shortened for editing.",
        
        "radiant_start_prompt": "Shortened for editing.",
        
        "radiant_end_prompt": "In, {language} and a maximum of 100 text characters, wrap up the current topic naturally. No need for formal goodbyes as no one is leaving. Keep the summary concise, and remember narration ONLY, do not use, symbols such as asterisks or describe actions, in your output.", 
        
        "memory_prompt": "Shortened for editing.", 
        
        "resummarize_prompt": "Shortened for editing."
    }

    needs_update = False
    if 'Prompt' not in config:
        verbose_print("'Prompt' section not found in config. Creating it.")
        config['Prompt'] = {}
        needs_update = True
    else:
        for key in prompt_keys:
            if key not in config['Prompt']:
                verbose_print(f"Prompt key '{key}' not found in config. Will update.")
                needs_update = True
                break
            elif len(config['Prompt'][key].strip()) != len(updated_prompts[key].strip()):
                verbose_print(f"Prompt '{key}' needs updating.")
                verbose_print(f"Current: {config['Prompt'][key]}")
                verbose_print(f"Updated: {updated_prompts[key]}")
                needs_update = True
                break

    if needs_update:
        verbose_print("Optimizing Prompts..")
        for key, value in updated_prompts.items():
            config['Prompt'][key] = value
        
        try:
            with open(FILE_NAME, 'w') as configfile:
                config.write(configfile)
            verbose_print("..Prompts Optimized.")
        except Exception as e:
            verbose_print(f"Error writing updated prompts to config file: {str(e)}")
            delay(3)
    else:
        verbose_print("Prompts Already Optimized.")
        delay(1)


def display_title():
    clear_screen()
    print("=" * 119)
    print("    MaNTella-Launcher")
    print("-" * 119)
    print("")

def display_menu_and_handle_input():
    global game, optimization, custom_token_count, microphone_enabled, model_id
    while True:
        display_title()
        print(f"\n")
        print(f"    1. Game Used: {game}\n")
        print(f"    2. Microphone On: {'True' if microphone_enabled else 'False'}\n")
        print(f"    3. Optimization: {optimization}\n")
        print(f"    4. Token Count: {custom_token_count}\n")
        print(f"")
        print("-" * 119)
        game_key = game.lower().replace(" ", "")
        print(f"\n")
        print(f"    model:")
        print(f"        {model_id}\n")
        print(f"    {game}_folder = {game_folders.get(game_key, 'Not set')}\n")
        print(f"    xvasynth_folder:")
        print(f"        {xvasynth_folder}")
        print(f"\n\n")
        print("=" * 119)

        choice = input("Selection, Program Options = 1-4, Refresh Display = R, Begin Mantella/xVASynth/Fallout4 = B, Exit and Save = X: ").strip().upper()
        
        if choice == '1':
            games = ["Skyrim", "SkyrimVR", "Fallout4", "Fallout4VR"]
            game = games[(games.index(game) + 1) % len(games)]
        elif choice == '2':
            microphone_enabled = not microphone_enabled
        elif choice == '3':
            optimizations = list(optimization_presets.keys())
            optimization = optimizations[(optimizations.index(optimization) + 1) % len(optimizations)]
        elif choice == '4':
            context_lengths = [2048, 4096, 8192]
            custom_token_count = context_lengths[(context_lengths.index(custom_token_count) + 1) % len(context_lengths)]
        elif choice == 'R':
            server_choice = read_temp_file()
            if server_choice == "lmstudio":
                fetch_model_details_lmstudio()
            elif server_choice == "ollama":
                fetch_model_details_ollama()
            continue
        elif choice == 'B':
            display_title()
            write_config()
            verbose_print("Saved File: config.ini")
            write_output_file(0)
            verbose_print("Saved File: .\data\temporary_batch.txt")
            verbose_print("Exiting, then Running Mantella/xVASynth...")
            return 0, xvasynth_folder
        elif choice == 'X':
            display_title()
            write_config()
            verbose_print("Saved File: config.ini")
            write_output_file(1)
            verbose_print("Saved File: .\data\temporary_batch.txt")
            verbose_print("Exiting Launcher/Optimizer...") 
            return 1, xvasynth_folder
        else:
            verbose_print("Invalid selection. Please try again.")
        
        delay()

# Main Function
def main():
    verbose_print("Entering main function")
    try:
        read_config()

        server_choice = read_temp_file()
        if server_choice == "lmstudio":
            fetch_model_details_lmstudio()
        elif server_choice == "ollama":
            fetch_model_details_ollama()
        else:
            verbose_print("No valid model server choice found.")
            model_id = "No valid server choice"

        return display_menu_and_handle_input()
    except Exception as e:
        verbose_print(f"An unexpected error occurred: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())
        write_output_file(1)
        return 1, ""

# Entry Point
if __name__ == "__main__":
    verbose_print("Script execution started")
    try:
        exit_code, xvasynth_path = main()
        print(f"{exit_code},{xvasynth_path}", file=sys.stdout)
        sys.stdout.flush()
        verbose_print(f"Final output: exit_code={exit_code}, xvasynth_path={xvasynth_path}")
    except Exception as e:
        verbose_print(f"An unexpected error occurred in the main execution: {str(e)}")
        verbose_print("Traceback:")
        verbose_print(traceback.format_exc())
        print("1,", file=sys.stdout)
        sys.stdout.flush()
    verbose_print("Script execution ended")
    sys.exit(0)   # Always exit with code 0