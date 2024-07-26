import requests
import json
import base64
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Zoom OAuth credentials (replace with your actual credentials)
CLIENT_ID = os.getenv('CLIENT_ID', '_6KMf8b7RJuB10ydU_bKGA')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', 'HbQRz9vf3hAFeqQXD1uat2biYCTYS4gh')
TOKEN_FILE = 'zoom_tokens.json'

# Helper function to load tokens from a file
def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return {}

# Helper function to save tokens to a file
def save_tokens(tokens):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

# Function to refresh the access token
def refresh_access_token(refresh_token):
    token_url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()
        if 'access_token' in response_data:
            logging.info("Access token refreshed successfully.")
            save_tokens(response_data)
            return response_data.get("access_token")
        else:
            logging.error("Failed to refresh access token. Response data: %s", response_data)
            return None
    except requests.RequestException as e:
        logging.error("Error refreshing access token: %s", e)
        if e.response:
            logging.error("Response content: %s", e.response.text)
        return None

# Function to schedule a meeting
def schedule_meeting(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    meeting_details = {
        "topic": "Automated Meeting",
        "type": 2,  # Scheduled meeting
        "start_time": "2024-06-08T11:20:00Z",  # Meeting start time in ISO 8601 format
        "duration": 60,  # Duration in minutes
        "timezone": "UTC",
        "agenda": "This is an automated meeting",
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "watermark": True,
            "use_pmi": False,
            "approval_type": 0,  # Automatically approve
            "registration_type": 1,  # Attendees register once and can attend any of the occurrences
            "audio": "both",  # Both telephony and VoIP
            "auto_recording": "cloud"
        }
    }
    
    user_id = 'me'  # Use 'me' for the authenticated user, or replace with a specific user ID
    try:
        response = requests.post(f'https://api.zoom.us/v2/users/{user_id}/meetings', headers=headers, json=meeting_details)
        response.raise_for_status()  # Raise an exception for HTTP errors
        meeting = response.json()
        join_url = meeting.get('join_url')
        return join_url
    except requests.RequestException as e:
        logging.error("Failed to schedule meeting: %s", e)
        if e.response:
            logging.error("Response content: %s", e.response.text)
        return None

# Main function to execute the script
def main():
    tokens = load_tokens()
    if 'refresh_token' in tokens:
        access_token = refresh_access_token(tokens['refresh_token'])
        if access_token:
            join_url = schedule_meeting(access_token)
            if join_url:
                print(f"Meeting scheduled successfully! Join URL: {join_url}")
            else:
                print("Failed to schedule meeting.")
        else:
            print("Failed to refresh access token.")
    else:
        print("No refresh token found. Please obtain an authorization code and save the tokens.")

if __name__ == "__main__":
    main()


