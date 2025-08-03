import os
import pandas as pd
import subprocess
import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

# Locate latest dataset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(BASE_DIR, "..", "datasets")
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])

# Load processed data
data_file = os.path.join(latest_folder, "processed_data.csv")
if not os.path.exists(data_file):
    raise FileNotFoundError("processed_data.csv not found!")
df = pd.read_csv(data_file)

# Read problem type from summary
summary_path = os.path.join(latest_folder, "model_selection_summary.txt")
if not os.path.exists(summary_path):
    raise FileNotFoundError("model_selection_summary.txt not found!")
with open(summary_path) as f:
    lines = f.readlines()
    problem_type = [line for line in lines if "Problem type" in line][0].split(":")[1].strip()

# Split features and target
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
if problem_type == "classification":
    model = RandomForestClassifier()
else:
    model = RandomForestRegressor()

model.fit(X_train, y_train)

# Save model
model_path = os.path.join(latest_folder, "trained_model.pkl")
joblib.dump(model, model_path)

# Save model name
with open(os.path.join(latest_folder, "model_name.txt"), "w") as f:
    f.write(model.__class__.__name__)    
    
print(f" Trained model saved to {model_path}")
print("Target preview:", y.unique()[:5])
print("Target dtype:", y.dtype)
print("Problem type (from summary):", problem_type)

# Git add, commit, push
commit_msg = f" Trained {problem_type} model for {folders[0]}"
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push"])