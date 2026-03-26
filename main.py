#!/usr/bin/env python3
import os
import time
import subprocess
import sys
import json
import socket
from INA219 import INA219


def shutdown():
    """Shut down the Raspberry Pi safely."""
    log("Shutting down Raspberry Pi...")

    # Wait a moment to ensure all logs are flushed before shutting down
    time.sleep(1) 
    subprocess.run(["sudo", "poweroff"])

    # In case the shutdown command fails, exit the script
    sys.exit(1)


def cleanup(exit_code):
    """Perform any necessary cleanup before exiting the script."""
    unmount_device()

    if exit_code == 0:
        log("=== ReadRelay Finished without Errors ===")
    else:
        log(f"=== ReadRelay Exited with Errors ===")

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
    global MOUNT_POINT, DEVICE_PATH, REMOTE_DIR, TARGET_DIR, SYNC_DIRECTION, LOG_FILE, AUTO_SHUTDOWN, BATTERY_ENABLED, BATTERY_THRESHOLD

    config = load_config()

    # Device config
    MOUNT_POINT = config["device"]["mount_point"]
    DEVICE_PATH = config["device"]["device_path"]
    TARGET_DIR = config["device"]["target_dir"]

    # System config
    LOG_FILE = config["system"]["log_file"]
    AUTO_SHUTDOWN = config["system"]["auto_shutdown"]
    BATTERY_ENABLED = config["system"]["battery"]["enabled"]
    BATTERY_THRESHOLD = config["system"]["battery"]["threshold"]

    # Sync config
    REMOTE_DIR = config["sync"]["remote_dir"]
    SYNC_DIRECTION = config["sync"]["sync_direction"]

    log("Config loaded successfully.")


def check_battery():
    """Check the battery level using the INA219 sensor. If the battery level is below the threshold, log a warning and shut down."""
    ina219 = INA219(addr=0x43)
    battery_percent = ina219.getPercent()
    log(f"Battery level: {battery_percent:.2f}%")

    if battery_percent < BATTERY_THRESHOLD:
        log(f"Warning: Battery level is below {BATTERY_THRESHOLD}%. Initiating shutdown to prevent damage.")
        shutdown()


def wait_for_device():
    pass


def mount_device():
    pass


def unmount_device():
    pass


def wait_for_wifi():
    """Check for Wi-Fi connectivity by attempting to connect to a well-known server. If the connection fails, log an error and exit."""
    timeout = 3
    host = "8.8.8.8"
    port = 53
    try:
        socket.setdefaulttimeout(timeout)
        socket,socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        log("Wi-Fi connection established.")
    except socket.error as ex:
        log(f"Error: No Wi-Fi connection. {ex}")
        log("Please connect to Wi-Fi and restart the script.")
        cleanup(1)


def sync_files():
    pass


def main():
    """Main function to orchestrate the steps of the script."""
    log("=========== ReadRelay Started ===========")
    setup()
    if BATTERY_ENABLED: check_battery()
    wait_for_device()
    mount_device()
    wait_for_wifi()
    sync_files()
    cleanup(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("=== ReadRelay Stopped by User ===")
        cleanup(130)  # 130 is the standard exit code for script termination by Ctrl+C