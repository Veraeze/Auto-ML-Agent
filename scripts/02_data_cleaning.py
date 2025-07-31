import os
import pandas as pd
import subprocess

# Locate the latest dataset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(BASE_DIR, "..", "datasets")
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])

# Load the first dataset
data_file = None
for file in os.listdir(latest_folder):
    if file.endswith(".csv") and "cleaned" not in file:
        data_file = os.path.join(latest_folder, file)
        break
    elif file.endswith(".xlsx"):
        data_file = os.path.join(latest_folder, file)
        break

if not data_file:
    raise FileNotFoundError("No data file found.")

# Load dataset
df = pd.read_csv(data_file) if data_file.endswith(".csv") else pd.read_excel(data_file)

# Basic cleaning
initial_shape = df.shape
df.drop_duplicates(inplace=True)
df.fillna(df.mean(numeric_only=True), inplace=True)
final_shape = df.shape

# Save cleaned data
cleaned_path = os.path.join(latest_folder, "cleaned_data.csv")
df.to_csv(cleaned_path, index=False)

# Save cleaning log
log_path = os.path.join(latest_folder, "data_cleaning_summary.txt")
with open(log_path, "w") as f:
    f.write(f"Original shape: {initial_shape}\n")
    f.write(f"Final shape after cleaning: {final_shape}\n")
    f.write("Missing values handled and duplicates removed.\n")

print(f"Cleaned data saved to {cleaned_path}")
print(f"Cleaning log saved to {log_path}")

# Git add, commit, push
commit_msg = f"Cleaned dataset for {folders[0]}"
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push"])