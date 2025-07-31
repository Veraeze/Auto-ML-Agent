import os
import pandas as pd
import subprocess
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, confusion_matrix,
    r2_score, mean_absolute_error, mean_squared_error
)
from sklearn.model_selection import train_test_split

# Locate latest dataset folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(BASE_DIR, "..", "datasets")
folders = sorted(os.listdir(datasets_dir), reverse=True)
latest_folder = os.path.join(datasets_dir, folders[0])

# Load processed data and model
data_path = os.path.join(latest_folder, "processed_data.csv")
model_path = os.path.join(latest_folder, "trained_model.pkl")
summary_path = os.path.join(latest_folder, "model_selection_summary.txt")

df = pd.read_csv(data_path)
model = joblib.load(model_path)

with open(summary_path) as f:
    lines = f.readlines()
    problem_type = [line for line in lines if "Problem type" in line][0].split(":")[1].strip()

# Split X and y
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate and log results
eval_log = os.path.join(latest_folder, "model_evaluation_summary.txt")
with open(eval_log, "w") as f:
    if problem_type == "classification":
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        cm = confusion_matrix(y_test, y_pred)

        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall: {rec:.4f}\n")

        # Save confusion matrix plot
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.tight_layout()
        plt.savefig(os.path.join(latest_folder, "confusion_matrix.png"))
        plt.close()

    else:
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        f.write(f"R² Score: {r2:.4f}\n")
        f.write(f"MAE: {mae:.4f}\n")
        f.write(f"RMSE: {rmse:.4f}\n")

print("Model evaluation complete and saved.")

# Git add, commit, push
commit_msg = f" Evaluation results for {folders[0]}"
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", commit_msg])
subprocess.run(["git", "push"])