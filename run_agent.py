import os
import subprocess

# Define scripts in order
steps = [
    "01_data_loading.py",
    "02_data_cleaning.py",
    "03_eda.py",
    "04_feature_engineering.py",
    "05_model_selection.py",
    "06_model_training.py",
    "07_model_evaluation.py",
    "08_generate_readme.py",
    "09_publish_to_repo.py"
]

for step in steps:
    print(f"\n Running {step} ...\n")
    subprocess.run(["python3", f"scripts/{step}"])