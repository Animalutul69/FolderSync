"""
Syncronizong from source folder with replica folder (Create, Copy, Delete)
"""

import os
import shutil
import time
import argparse
from datetime import datetime

def sync_folders(source_folder, replica_folder, log_file, interval):
    # Create the replica folder if it doesn't exist
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    while True:
        # Sync the folders
        for root, dirs, files in os.walk(source_folder):
            # Get the path of the corresponding directory in the replica folder
            replica_dir = root.replace(source_folder, replica_folder, 1)

            # Sync the directories
            for dir in dirs:
                source_path = os.path.join(root, dir)
                replica_path = os.path.join(replica_dir, dir)

                if not os.path.exists(replica_path):
                    os.makedirs(replica_path)

            # Sync the files
            for file in files:
                source_path = os.path.join(root, file)
                replica_path = os.path.join(replica_dir, file)

                if not os.path.exists(replica_path) or (os.path.exists(replica_path) and os.path.getmtime(replica_path) < os.path.getmtime(source_path)):
                    shutil.copy2(source_path, replica_path)
                    log(f"Copied {source_path} to {replica_path}", log_file)

        # Delete files in the replica folder that no longer exist in the source folder
        for root, dirs, files in os.walk(replica_folder):
            for file in files:
                source_path = os.path.join(root.replace(replica_folder, source_folder, 1), file)
                replica_path = os.path.join(root, file)

                if not os.path.exists(source_path):
                    os.remove(replica_path)
                    log(f"Deleted {replica_path}", log_file)

        # Sleep for the specified interval
        time.sleep(interval)

def log(message, log_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(log_file, "a") as f:
        f.write(log_message + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync two folders")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    args = parser.parse_args()

    sync_folders(args.source_folder, args.replica_folder, args.log_file, args.interval)


