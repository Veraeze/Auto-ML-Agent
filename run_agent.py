import os
import subprocess
from datetime import datetime

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cron_log.txt")

scripts = [
    "01_data_loading.py",
    "02_data_cleaning.py",
    "03_eda.py",
    "04_feature_engineering.py",
    "05_model_selection.py",
    "06_model_training.py",
    "07_model_evaluation.py",
    "08_generate_readme.py",
    "09_publish_to_repo.py",
]

with open(log_path, "a") as log_file:
    for script in scripts:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", script)
        log_file.write(f"\n{datetime.now()} - Running {script} ...\n\n")
        subprocess.run(["/Library/Frameworks/Python.framework/Versions/3.11/bin/python3", script_path], check=True)

    slack_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "10_send_slack_notification.py")
    log_file.write(f"\n{datetime.now()} - Running 10_send_slack_notification.py ...\n\n")
    subprocess.run(["/Library/Frameworks/Python.framework/Versions/3.11/bin/python3", slack_script], check=True)