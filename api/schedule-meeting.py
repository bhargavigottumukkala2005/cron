import requests
import json
import os
from api.utils import load_tokens, save_tokens, refresh_access_token, schedule_meeting

def main():
    tokens = load_tokens()

    if 'refresh_token' in tokens:
        # Refresh the access token if needed
        access_token = refresh_access_token(tokens['refresh_token'])
    else:
        print("No refresh token found. Make sure to obtain one.")
        return

    if access_token:
        join_url = schedule_meeting(access_token)
        if join_url:
            print("Meeting scheduled successfully!")
            print("Join URL:", join_url)
        else:
            print("Failed to schedule meeting.")
    else:
        print("Failed to refresh access token.")

if __name__ == "__main__":
    main()
