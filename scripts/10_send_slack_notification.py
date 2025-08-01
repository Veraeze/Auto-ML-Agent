import requests
import os

# Load webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Read latest model folder
datasets_dir = os.path.join(os.path.dirname(__file__), "..", "datasets")
latest_run = sorted(os.listdir(datasets_dir), reverse=True)[0]

message = {
    "text": f" AutoML Agent has completed a new model run for *{latest_run}*. Check the latest results on GitHub!"
}

response = requests.post(SLACK_WEBHOOK_URL, json=message)

if response.status_code != 200:
    raise Exception(f"Slack notification failed: {response.status_code}, {response.text}")
else:
    print("Slack notification sent.")