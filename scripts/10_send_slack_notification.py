import os
import requests

# Get OAuth token and channel ID from environment variables
slack_token = os.getenv("SLACK_BOT_TOKEN")
channel_id = os.getenv("SLACK_CHANNEL_ID")

if not slack_token or not channel_id:
    raise Exception("Missing SLACK_BOT_TOKEN or SLACK_CHANNEL_ID environment variable.")

message = "AutoML Agent completed today's job!"

url = "https://slack.com/api/chat.postMessage"
headers = {
    "Authorization": f"Bearer {slack_token}",
    "Content-Type": "application/json"
}
data = {
    "channel": channel_id,
    "text": message
}

response = requests.post(url, headers=headers, json=data)
if not response.ok or not response.json().get("ok"):
    raise Exception(f"Slack notification failed: {response.status_code}, {response.text}")
else:
    print("Slack notification sent.")