import os
import requests
import subprocess
import sys

# GitHub repository information
REPO_OWNER = "AgenTEzClamps"
REPO_NAME = "ping"
UPDATE_SCRIPT_NAME = "ping.py"

def check_for_updates():
    try:
        # Get the latest commit hash from the GitHub repository
        response = requests.get(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/master")
        response.raise_for_status()
        latest_commit = response.json()["sha"]

        # Compare the latest commit hash with the local commit hash
        with open(sys.argv[0], "rb") as file:
            local_commit = subprocess.run(["git", "hash-object", "-t", "blob", "-w", "--stdin"], input=file.read(), stdout=subprocess.PIPE, check=True, universal_newlines=True).stdout.strip()

        return latest_commit != local_commit
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False

def download_update():
    try:
        # Download the latest version of the update script
        response = requests.get(f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/master/{UPDATE_SCRIPT_NAME}")
        response.raise_for_status()

        # Save the downloaded script as a temporary file
        with open(UPDATE_SCRIPT_NAME, "wb") as file:
            file.write(response.content)
    except Exception as e:
        print(f"Error downloading update: {e}")

def apply_update():
    try:
        # Replace the existing script with the updated script
        os.replace(UPDATE_SCRIPT_NAME, sys.argv[0])
    except Exception as e:
        print(f"Error applying update: {e}")

if __name__ == "__main__":
    if check_for_updates():
        print("Updates available. Downloading...")
        download_update()
        print("Updates downloaded. Applying...")
        apply_update()
        print("Updates applied successfully. Restarting program...")
        # Restart the program
        python_executable = sys.executable
        os.execl(python_executable, python_executable, *sys.argv)
    else:
        print("No updates available. Exiting update script.")
