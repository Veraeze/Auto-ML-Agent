import os
import pandas as pd
import subprocess

# Find latest dataset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(BASE_DIR, "..", "datasets")
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])

# Find first CSV or Excel file
data_file = None
for file in os.listdir(latest_folder):
    if file.endswith(".csv") or file.endswith(".xlsx"):
        data_file = os.path.join(latest_folder, file)
        break

if not data_file:
    raise FileNotFoundError("No CSV or Excel file found in dataset folder.")

# Load the data
if data_file.endswith(".csv"):
    df = pd.read_csv(data_file)
else:
    df = pd.read_excel(data_file)

# Save sample output to logs
summary_path = os.path.join(latest_folder, "data_loading_summary.txt")
with open(summary_path, "w") as f:
    f.write(f"Dataset shape: {df.shape}\n\n")
    f.write("First 5 rows:\n")
    f.write(df.head().to_string())

print(f" Loaded dataset from {data_file} and saved summary to {summary_path}")

commit_message = f" Loaded dataset and saved preview for {folders[0]}"

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_message])
subprocess.run(["git", "push"])