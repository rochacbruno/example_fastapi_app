#!/usr/bin/env python3
import os
import sys
import httpx

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#alerts")
REPO_NAME = os.getenv("GITHUB_REPOSITORY", "unknown repo")
PR_NUMBER = os.getenv("PR_NUMBER", "N/A")
GITHUB_ACTOR = os.getenv("GITHUB_ACTOR", "someone")

def send_slack_alert(message: str):
    if not SLACK_WEBHOOK_URL:
        print("❌ SLACK_WEBHOOK_URL is not set.")
        sys.exit(1)

    payload = {
        "channel": SLACK_CHANNEL,
        "username": "Commit Validator Bot",
        "text": f":warning: *Commit validation failed*\n\n*Repo:* {REPO_NAME}\n*PR:* #{PR_NUMBER}\n*By:* @{GITHUB_ACTOR}\n\n*Details:* {message}",
        "icon_emoji": ":rotating_light:"
    }

    response = httpx.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        print(f"❌ Slack notification failed: {response.status_code} - {response.text}")
        sys.exit(1)
    else:
        print("✅ Slack alert sent successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python alert_on_slack.py '<error_message>'")
        sys.exit(1)

    error_msg = sys.argv[1]
    send_slack_alert(error_msg)
