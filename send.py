#!/usr/bin/env python3

import sys
import yaml
import requests

CONFIG_FILE = "config.yaml"

def read_config():
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            config_data = yaml.safe_load(config_file)
            return config_data
    except FileNotFoundError:
        print("Error: config.yaml not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error while reading config.yaml: {e}")
        sys.exit(1)

def send_telegram_message(user_id, token, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': user_id,
        'text': message
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def main():
    # Read content from stdin
    content = sys.stdin.read()

    if not content:
        print("Pass content via stdin to send.")
        sys.exit(1)

    # Read Telegram config from config.yaml
    config = read_config()

    # Check if 'userid' and 'token' keys are present
    if 'telegram_bot' not in config or 'telegram' not in config:
        print("Error: 'telegram_bot' and 'telegram' keys are required in config.yaml.")
        sys.exit(1)

    # Extract user_id and token
    user_id = config['telegram']
    token = config['telegram_bot']

    # Send message using Telegram API
    send_telegram_message(user_id, token, content)

if __name__ == "__main__":
    main()

