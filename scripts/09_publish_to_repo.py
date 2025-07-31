import os
import shutil
import subprocess

# CONFIG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DATASETS_DIR = os.path.join(BASE_DIR, "..", "datasets")DEST_REPO_PATH = os.path.expanduser("~/ml_daily_models/ml_daily_models")  

# Locate latest folder
folders = sorted(os.listdir(SOURCE_DATASETS_DIR), reverse=True)
latest_folder = folders[0]
source_path = os.path.join(SOURCE_DATASETS_DIR, latest_folder)
dest_path = os.path.join(DEST_REPO_PATH, latest_folder)

# Copy folder 
if os.path.exists(dest_path):
    print(f"📂 Folder {latest_folder} already exists in destination. Overwriting...")
    shutil.rmtree(dest_path)

shutil.copytree(source_path, dest_path)
print(f"Copied {latest_folder} to ML-daily-models repo.")

# Git add, commit, push ===
os.chdir(DEST_REPO_PATH)
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f" Daily model update: {latest_folder}"])
subprocess.run(["git", "push"])