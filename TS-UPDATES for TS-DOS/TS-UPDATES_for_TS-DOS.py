import datetime
import requests # type: ignore
import tkinter as tk
from tkinter import messagebox
import os
import subprocess

# Constants
GITHUB_USER = "Coolis1362"
REPO_NAME = "TS-DOS"
UPDATE_PREFIX = "TS-DOS UPDATE "

def check_updates():
    """Checks for updates in the GitHub repo."""
    try:
        response = requests.get(f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/releases")
        response.raise_for_status()
        releases = response.json()
        
        today = datetime.date.today()
        for release in releases:
            name = release.get("name", "")
            if name.startswith(UPDATE_PREFIX):
                update_date_str = name.replace(UPDATE_PREFIX, "").strip()
                update_date = datetime.datetime.strptime(update_date_str, "%m/%d/%Y").date()
                if update_date == today:
                    return release["zipball_url"], update_date_str
        return None, None
    except Exception as e:
        print(f"Error checking updates: {e}")
        return None, None

def download_and_install_update(url):
    """Downloads and installs the update."""
    try:
        # Download the update
        response = requests.get(url)
        response.raise_for_status()
        update_file = "update.zip"
        with open(update_file, "wb") as file:
            file.write(response.content)
        
        # Uninstall previous version
        print("Uninstalling previous version...")
        # Here, you'd add code to remove the previous version (if applicable).
        
        # Install the new version
        print("Installing the latest version...")
        # Extract the zip and install
        subprocess.run(["unzip", "-o", update_file], check=True)
        os.remove(update_file)
        print("Installation completed.")
    except Exception as e:
        print(f"Error during update: {e}")

def prompt_update(update_url, update_date):
    """Prompts the user for update installation."""
    def on_yes():
        root.destroy()
        download_and_install_update(update_url)

    def on_no():
        root.destroy()

    root = tk.Tk()
    root.withdraw()
    answer = messagebox.askquestion(
        "Update Available",
        f"Would you like to install the update dated {update_date}?",
        icon="question"
    )
    if answer == "yes":
        on_yes()
    else:
        on_no()

# Main Logic
update_url, update_date = check_updates()
if update_url and update_date:
    prompt_update(update_url, update_date)
else:
    print("No updates available today.")
