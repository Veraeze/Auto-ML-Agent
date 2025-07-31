import os
import pandas as pd
import subprocess

# Locate latest dataset folder
datasets_dir = "datasets"
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])

# Load processed dataset
processed_file = os.path.join(latest_folder, "processed_data.csv")
if not os.path.exists(processed_file):
    raise FileNotFoundError("processed_data.csv not found!")

df = pd.read_csv(processed_file)

# Assume the target column is the last column
target_col = df.columns[-1]

# Determine problem type
unique_values = df[target_col].nunique()

if df[target_col].dtype == 'object':
    problem_type = "classification"
elif df[target_col].dtype in ['int', 'int64'] and unique_values <= 10:
    problem_type = "classification"
else:
    problem_type = "regression"

# Save result
summary_path = os.path.join(latest_folder, "model_selection_summary.txt")
with open(summary_path, "w") as f:
    f.write(f"Target column: {target_col}\n")
    f.write(f"Unique values: {unique_values}\n")
    f.write(f"Problem type: {problem_type}\n")

print(f"Detected problem type: {problem_type}")
print(f"Summary saved to {summary_path}")

# Git commit and push
commit_msg = f"Model type selected for {folders[0]} ({problem_type})"
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push"])