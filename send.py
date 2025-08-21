import os
import time
import pyautogui
import pyperclip
import yaml
from git import Repo

# Load YAML config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

repo_cfg = config["repo"]
request_file = repo_cfg["request"]
response_file = repo_cfg["response"]
actions = config["constant_loop"]

# Clone repo if not exists
if not os.path.exists(repo_cfg["local_path"]):
    print(f"[INFO] Cloning repo '{repo_cfg['name']}' from {repo_cfg['url']}...")
    Repo.clone_from(repo_cfg["url"], repo_cfg["local_path"])
    print(f"[INFO] Repo cloned successfully at {repo_cfg['local_path']}")

repo = Repo(repo_cfg["local_path"])
last_commit = repo.head.commit.hexsha

def git_pull():
    global last_commit
    print("[INFO] Pulling latest changes from repo...")
    repo.remotes.origin.pull()
    new_commit = repo.head.commit.hexsha
    if new_commit != last_commit:
        print(f"[INFO] New commit detected: {new_commit}")
        last_commit = new_commit

def git_push():
    print("[INFO] Starting git push...")
    repo.remotes.origin.push()
    print("[INFO] Git push completed successfully")

def press_keys(keys):
    if isinstance(keys, str) and keys.lower() == "enter":
        print("[INFO] Pressing Enter key")
        pyautogui.press("enter")
    elif isinstance(keys, list):
        print(f"[INFO] Pressing keys: {keys}")
        pyautogui.hotkey(*keys)

def wait(seconds):
    print(f"[INFO] Waiting {seconds} seconds")
    time.sleep(seconds)

def mouse_click(coord):
    print(f"[INFO] Moving mouse to {coord} and clicking")
    pyautogui.moveTo(*coord)
    pyautogui.click()

def mouse_move_click(coord):
    print(f"[INFO] Moving mouse to {coord} and clicking")
    pyautogui.moveTo(*coord)
    pyautogui.click()

def write_clipboard_to_file(filename):
    file_path = os.path.join(repo_cfg["local_path"], filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(pyperclip.paste())
    print(f"[INFO] Written clipboard content to '{filename}'")
    repo.index.add([filename])
    repo.index.commit(f"Update {filename} from clipboard")
    print(f"[INFO] Committed '{filename}' to local repo")
    git_push()

def write_file_to_clipboard(filename):
    """Read a file from repo and copy its content to the clipboard"""
    file_path = os.path.join(repo_cfg["local_path"], filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            pyperclip.copy(f.read())
        print(f"[INFO] Copied content of '{filename}' to clipboard")
    else:
        print(f"[WARNING] File '{filename}' not found")

# Main loop
while True:
    for step in actions:
        key, value = next(iter(step.items()))
        if key == "git_pull" and value:
            git_pull()
        elif key == "git_push" and value:
            git_push()
        elif key == "press":
            press_keys(value)
        elif key == "wait_sec":
            wait(value)
        elif key == "mouse_click":
            mouse_click(value)
        elif key == "mouse_move_click":
            mouse_move_click(value)
        elif key == "write_clipboard_to_file":
            write_clipboard_to_file(value)
        elif key == "write_file_to_clipboard":
            write_file_to_clipboard(value)
