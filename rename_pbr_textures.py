"""
rename_pbr_textures.py
======================

Author: Sebastian
Date: 2025-03-11

This script recursively scans a directory for PNG files and renames them 
according to a specified pattern defined in a CSV configuration file.

Attributes:
    CONFIG_PATH (str): Path to the JSON configuration file.
    SOURCE_DIRECTORY (str): Path to the directory containing the files to be renamed.
    CONFIG_FILE (str): Path to the CSV file defining the renaming rules.
    LOG_FILE (str): Path to the log file containing details of the renaming process.

Configuration Files:
    The script uses two configuration files:
        - JSON file:
            - Stores the source directory, CSV file path, and log file path.
            - Example:
                {
                    "source_directory": "E:\\path\\to\\source",
                    "config_file": "E:\\path\\to\\csv_file.csv",
                    "log_directory": "E:\\path\\to\\log"
                }

        - CSV file:
            - Contains rename patterns in two columns separated by a semicolon (`;`).
            - Example:
                _BaseColor.png;_COL.png
                _Metallic.png;_METAL.png

Functionality:
    - Scans all PNG files in the specified directory (including subdirectories).
    - Applies renaming rules based on the CSV file.
    - Logs all operations to a log file.
    - Outputs progress and status (renamed or skipped) to the console.
    - Provides a final summary of renamed and skipped files.
    - Logs the list of processed directories and file locations.

Output:
    ✅ = Successfully renamed
    ⏭️ = Skipped (if no pattern match)
    ❌ = Error during renaming

Example Output:
    Processing file: 10-1009-110_BaseColor.png          ✅ renamed to → 10-1009-110_COL.png
    Processing file: 10-1009-110_Roughness.png          ⏭️ skipped

Notes:
    - The script uses `str.ljust()` to align the console output properly.
    - If a renaming operation fails, the error message is logged.
    - JSON file path, CSV file path, and log file path are output at the end.
    - The script follows PEP8 and PEP257 coding standards.
"""



import os
import json
from datetime import datetime

# Load configuration from JSON file
CONFIG_PATH = r"E:\local_Sebastian\z\PBR_Materials_0010_25\software\python\rename_path_config.json"

def load_config():
    """Load configuration from JSON file."""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config

# Load config into global variables
config = load_config()

# Use raw strings to avoid escape issues
SOURCE_DIRECTORY = r"{}".format(config["source_directory"])
CONFIG_FILE = r"{}".format(config["config_file"])
LOG_FILE = r"{}\{}_rename.log".format(
    config["log_directory"],
    datetime.now().strftime('%Y_%m_%d_%H_%M')
)

def load_rename_patterns():
    """Load rename patterns from the CSV file."""
    patterns = {}
    try:
        with open(CONFIG_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if len(row) == 2:
                    old_name = row[0].strip()
                    new_name = row[1].strip()
                    patterns[old_name] = new_name
    except Exception as e:
        print(f"Error reading config file: {e}")
    return patterns

def rename_files():
    """Rename files based on patterns from the CSV file."""
    rename_count = 0
    skipped_count = 0
    processed_paths = []
    patterns = load_rename_patterns()

    with open(LOG_FILE, 'w', encoding='utf-8') as log:
        log.write(f"=== Rename process started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

        for root, _, files in os.walk(SOURCE_DIRECTORY):
            for file in files:
                if file.endswith('.png'):
                    old_path = os.path.join(root, file)
                    new_file_name = file

                    # Apply rename patterns
                    for old_pattern, new_pattern in patterns.items():
                        if old_pattern in new_file_name:
                            new_file_name = new_file_name.replace(old_pattern, new_pattern)

                    new_path = os.path.join(root, new_file_name)
                    processed_paths.append(root)

                    # Create aligned output using str.ljust()
                    output = f"Processing file: {file.ljust(45)}"

                    if old_path != new_path:
                        try:
                            os.rename(old_path, new_path)
                            rename_count += 1
                            status_message = f"✅ renamed to → {new_file_name}"
                        except Exception as e:
                            status_message = f"❌ Failed: {e}"
                    else:
                        skipped_count += 1
                        status_message = f"⏭️ skipped"

                    # Print and write to log in one line
                    print(f"{output}{status_message}")
                    log.write(f"{output}{status_message}\n")

        # Write summary to log file
        log.write("\n=== Rename process finished ===\n")
        log.write(f"Total files renamed: {rename_count}\n")
        log.write(f"Total files skipped: {skipped_count}\n")
        log.write("\nProcessed directories:\n")

        for path in sorted(set(processed_paths)):
            log.write(f"{path}\n")

        # Write file locations (including JSON config)
        log.write("\n=== File locations ===\n")
        log.write(f"JSON config file: {CONFIG_PATH}\n")
        log.write(f"CSV config file: {CONFIG_FILE}\n")
        log.write(f"Log file: {LOG_FILE}\n")

        # Print summary to console
        print("\n=== Rename process finished ===")
        print(f"Total files renamed: {rename_count}")
        print(f"Total files skipped: {skipped_count}\n")

        print("Processed directories:")
        for path in sorted(set(processed_paths)):
            print(f" - {path}")

        # Print file locations to console
        print("\n=== File locations ===")
        print(f"JSON config file: {CONFIG_PATH}")
        print(f"CSV config file: {CONFIG_FILE}")
        print(f"Log file: {LOG_FILE}")

if __name__ == "__main__":
    rename_files()
