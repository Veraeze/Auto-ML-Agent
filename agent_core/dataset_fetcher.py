import os
import datetime
import random
import subprocess

from kaggle.api.kaggle_api_extended import KaggleApi

# Define datasets to choose from 
DATASET_CHOICES = [
    "uciml/iris",                         
    "uciml/pima-indians-diabetes-database",
    "ronitf/heart-disease-uci"
]

def fetch_and_save_dataset():
    # Pick one at random
    dataset_name = random.choice(DATASET_CHOICES)
    dataset_id = dataset_name.split("/")[-1]
    
    # Create today's folder
    today = datetime.date.today().strftime("%Y-%m-%d")
    save_path = f"datasets/{today}_{dataset_id}"
    os.makedirs(save_path, exist_ok=True)

    # Download using Kaggle API
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset_name, path=save_path, unzip=True)

    print(f" Downloaded {dataset_name} to {save_path}")
    return save_path, dataset_id

def commit_dataset_step(path, dataset_id):
    commit_message = f" Step 1: Downloaded dataset {dataset_id}"
    
    subprocess.run(["git", "add", path])
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    path, dataset_id = fetch_and_save_dataset()
    commit_dataset_step(path, dataset_id)