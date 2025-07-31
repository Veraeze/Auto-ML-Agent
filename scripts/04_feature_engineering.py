import os
import pandas as pd
import numpy as np
import subprocess
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Locate latest dataset folder
datasets_dir = "datasets"
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])

# Load cleaned dataset
cleaned_file = os.path.join(latest_folder, "cleaned_data.csv")
if not os.path.exists(cleaned_file):
    raise FileNotFoundError("cleaned_data.csv not found!")

df = pd.read_csv(cleaned_file)

# Feature Engineering
summary_lines = []

# Encode categorical variables
cat_cols = df.select_dtypes(include='object').columns
le = LabelEncoder()

for col in cat_cols:
    try:
        df[col] = le.fit_transform(df[col])
        summary_lines.append(f"Label encoded: {col}")
    except Exception as e:
        summary_lines.append(f"Skipped {col} (couldn't encode): {e}")

# Scale numeric features
num_cols = df.select_dtypes(include='number').columns
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])
summary_lines.append(f"Standardized numeric columns: {list(num_cols)}")

# Save processed data
processed_path = os.path.join(latest_folder, "processed_data.csv")
df.to_csv(processed_path, index=False)

# Save feature engineering summary
summary_path = os.path.join(latest_folder, "feature_engineering_summary.txt")
with open(summary_path, "w") as f:
    for line in summary_lines:
        f.write(line + "\n")

print(f" Processed data saved to {processed_path}")
print(f" Feature engineering summary saved to {summary_path}")

# Git commit and push
commit_msg = f" Feature engineering complete for {folders[0]}"
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push"])