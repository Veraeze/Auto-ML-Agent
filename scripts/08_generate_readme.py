import os
import subprocess

# Locate latest dataset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(BASE_DIR, "..", "datasets")folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])
readme_path = os.path.join(latest_folder, "README.md")

# Read summary files
def read_if_exists(filename):
    path = os.path.join(latest_folder, filename)
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return "No information available."

data_cleaning = read_if_exists("data_cleaning_summary.txt")
model_selection = read_if_exists("model_selection_summary.txt")
feature_summary = read_if_exists("feature_engineering_summary.txt")
model_eval = read_if_exists("model_evaluation_summary.txt")

# Generate markdown content
content = f"""# Daily AutoML Model — {folders[0]}

This model was automatically trained by the AutoML Agent.

---

## Problem Type
{model_selection}

---

## Data Cleaning Summary
{data_cleaning}

---

## Feature Engineering
{feature_summary}

---

## Model Evaluation
{model_eval}

---

## Model File
- `trained_model.pkl`  
- Plots: `confusion_matrix.png` (if classification)

---

_This model was automatically trained and pushed using the AutoML Agent._
"""

# Save README
with open(readme_path, "w") as f:
    f.write(content)

print(f"README.md generated at {readme_path}")

#  Git add, commit, push
commit_msg = f"README generated for {folders[0]}"
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push"])