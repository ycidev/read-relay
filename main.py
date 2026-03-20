#!/usr/bin/env python3
import os
import time
import subprocess
import sys
import json


def shutdown():
    log("Shutting down Raspberry Pi...")

    # Wait a moment to ensure all logs are flushed before shutting down
    time.sleep(1) 
    subprocess.run(["sudo", "poweroff"])

    # In case the shutdown command fails, exit the script
    sys.exit(1)


def cleanup(exit_code):
    unmount_device()

    if AUTO_SHUTDOWN:
        shutdown()
    else:
        sys.exit(exit_code)


def log(message):
    """Log a message to the log file with a timestamp. Also print it to the console."""
    entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"
    # Open the log file in append mode and write the message with a timestamp
    # with open(LOG_FILE, "a") as f:
    #     f.write(entry)

    # Also print the message to the console
    print(entry, end="")


def load_config():
    """Load the configuration from config.json. If the file does not exist, print an error message and exit."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    # Check if the config file exists
    if not os.path.exists(config_path):
        log("Error: Config file not found.")
        log("Please copy config.json.example to config.json and fill in the required fields.")
        cleanup(1)

    # Load the config file
    with open(config_path, "r") as f:
        return json.load(f)
    

def setup():
    """Set up global variables from the config file."""
    global MOUNT_POINT, DEVICE_PATH, REMOTE_DIR, TARGET_DIR, SYNC_DIRECTION, LOG_FILE, AUTO_SHUTDOWN

    config = load_config()

    # Device config
    MOUNT_POINT = config["device"]["mount_point"]
    DEVICE_PATH = config["device"]["device_path"]
    TARGET_DIR = config["device"]["target_dir"]

    # System config
    LOG_FILE = config["system"]["log_file"]
    AUTO_SHUTDOWN = config["system"]["auto_shutdown"]

    # Sync config
    REMOTE_DIR = config["sync"]["remote_dir"]
    SYNC_DIRECTION = config["sync"]["sync_direction"]

    log("Config loaded successfully.")


def wait_for_device():
    pass


def mount_device():
    pass


def unmount_device():
    pass


def wait_for_wifi():
    pass


def sync_files():
    pass


def main():
    log("=========== ReadRelay Started ===========")
    setup()
    wait_for_device()
    mount_device()
    wait_for_wifi()
    sync_files()
    log("=== ReadRelay Finished without Errors ===")
    cleanup(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("=== ReadRelay Stopped by User ===")
        cleanup(130)  # 130 is the standard exit code for script termination by Ctrl+C