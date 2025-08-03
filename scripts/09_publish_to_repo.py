import os
import shutil
import subprocess

# CONFIG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(BASE_DIR, "..", "datasets")
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = folders[0]
source_path = os.path.join(datasets_dir, latest_folder)
dest_path = os.path.join(os.path.expanduser("~/ml_daily_models/ml_daily_models"), latest_folder)

# Copy folder 
if os.path.exists(dest_path):
    print(f"Folder {latest_folder} already exists in destination. Overwriting...")
    shutil.rmtree(dest_path)

shutil.copytree(source_path, dest_path)
print(f"Copied {latest_folder} to ML-daily-models repo.")

# Force-add trained_model.pkl
model_path = os.path.join(dest_path, "trained_model.pkl")
if os.path.exists(model_path):
    subprocess.run(["git", "add", model_path])
    
# Git add, commit, push ===
os.chdir(os.path.expanduser("~/ml_daily_models/ml_daily_models"))
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f" Daily model update: {latest_folder}"])
subprocess.run(["git", "push"])