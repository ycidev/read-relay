#!/usr/bin/env python3
import os
import time
import subprocess
import sys

################################################ CONFIGURATION ################################################
MOUNT_POINT = "/mnt/my_reader" 
DEVICE_PATH = "/dev/sda1" # Check with "lsblk" command and adjust if needed
REMOTE_DIR = "" # Name from "rclone config" (e.g. "remote:folder")
TARGET_DIR = "/mnt/my_reader/documents/ReadRelay" # Directory on the reader to copy files to
LOG_FILE = "ReadRelay.log"
############################################## END CONFIGURATION ##############################################

def log(message):
    """Log a message to the log file with a timestamp. Also print it to the console."""
    # Open the log file in append mode and write the message with a timestamp
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    # Also print the message to the console
    print(message)

def main():
    log("=== ReadRelay Started ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("=== ReadRelay Stopped by User ===")