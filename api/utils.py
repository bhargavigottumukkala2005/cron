import requests
import json
import base64
import os

def load_tokens():
    token_file = 'zoom_tokens.json'
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return json.load(f)
    return {}

def save_tokens(tokens):
    token_file = 'zoom_tokens.json'
    with open(token_file, 'w') as f:
        json.dump(tokens, f)

def refresh_access_token(refresh_token):
    client_id = os.getenv('ZOOM_CLIENT_ID')
    client_secret = os.getenv('ZOOM_CLIENT_SECRET')
    
    token_url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode((client_id + ':' + client_secret).encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response_data = response.json()
    
    if 'access_token' in response_data:
        save_tokens(response_data)
        return response_data['access_token']
    else:
        print("Failed to refresh access token.")
        return None

def schedule_meeting(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    meeting_details = {
        "topic": "Automated Meeting",
        "type": 2,  # Scheduled meeting
        "start_time": "2024-06-04T07:20:00Z",
        "duration": 60,
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
            "audio": "both",
            "auto_recording": "cloud"
        }
    }
    
    user_id = 'me'  # Schedule meeting for the authenticated user
    response = requests.post(f'https://api.zoom.us/v2/users/{user_id}/meetings', headers=headers, json=meeting_details)
    
    if response.status_code == 201:
        meeting = response.json()
        join_url = meeting.get('join_url')
        return join_url
    else:
        print(f"Failed to schedule meeting: {response.text}")
        return None
