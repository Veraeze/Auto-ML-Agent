import os
import datetime
import random
import subprocess

from kaggle.api.kaggle_api_extended import KaggleApi

# Define datasets to choose from 
DATASET_CHOICES = [
    "uciml/iris",                         
    "uciml/pima-indians-diabetes-database",
    "ronitf/heart-disease-uci",
    "alexteboul/diabetes-health-indicators-dataset",
    "dev0980/loan-prediction-dataset",
    "jsphyg/weather-dataset-rattle-package",
    "mathchi/churn-for-bank-customers",
    "yasserh/song-popularity-dataset",
    "thedevastator/air-pollution-pm25-dataset",
    "sujaykapadnis/student-performance-in-exams",
    "yasserh/breast-cancer-dataset",
    "shilongzhuang/credit-card-approval-prediction",
    "rohanrao/nifty50-stock-market-data",
    "abcsds/pokemon",
    "sagnik1511/loan-default-dataset",
    "mathchi/churn-for-bank-customers",
    "olistbr/brazilian-ecommerce"
]

def fetch_and_save_dataset():
    # Use today's date as a seed to ensure variation each day
    # random.seed(datetime.date.today().toordinal())
    random.seed(datetime.datetime.now().timestamp())
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