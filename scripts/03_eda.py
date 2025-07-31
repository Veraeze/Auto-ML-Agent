import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import numpy as np

# Locate latest dataset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(BASE_DIR, "..", "datasets")
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])

# Load cleaned dataset
cleaned_file = os.path.join(latest_folder, "cleaned_data.csv")
if not os.path.exists(cleaned_file):
    raise FileNotFoundError("cleaned_data.csv not found!")

df = pd.read_csv(cleaned_file)

# Create EDA plots folder
eda_dir = os.path.join(latest_folder, "eda_plots")
os.makedirs(eda_dir, exist_ok=True)

# Generate histograms for numeric features
for col in df.select_dtypes(include='number').columns:
    plt.figure()
    sns.histplot(df[col].dropna(), kde=True)
    plt.title(f"Histogram of {col}")
    plt.savefig(os.path.join(eda_dir, f"{col}_histogram.png"))
    plt.close()

# Correlation heatmap 
corr_txt_path = os.path.join(latest_folder, "correlation_summary.txt")
numeric_cols = df.select_dtypes(include='number')

if numeric_cols.shape[1] >= 2:
    corr = numeric_cols.corr()
    
    # Save heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig(os.path.join(eda_dir, "correlation_heatmap.png"))
    plt.close()

    # Save correlation pairs
    sorted_corr = (
        corr.where(~np.eye(corr.shape[0], dtype=bool))  
        .unstack()
        .dropna()
        .sort_values(key=lambda x: abs(x), ascending=False)
        .drop_duplicates()
    )
    with open(corr_txt_path, "w") as f:
        f.write("Top 5 correlation pairs:\n")
        f.write(sorted_corr.head(5).to_string())
else:
    with open(corr_txt_path, "w") as f:
        f.write("Not enough numeric columns for correlation analysis.\n")

print(f" EDA plots saved in {eda_dir}")
print(f" Correlation summary saved to {corr_txt_path}")

# Git commit and push
commit_msg = f"EDA complete for {folders[0]}"
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push"])