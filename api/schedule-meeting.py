import os
import json
from api.utils import load_tokens, save_tokens, refresh_access_token, schedule_meeting

# Load environment variables
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET')

if not ZOOM_CLIENT_ID or not ZOOM_CLIENT_SECRET:
    raise ValueError("Zoom client ID or secret not set in environment variables.")

# Load Zoom tokens from file
tokens = load_tokens('api/zoom_tokens.json')

# Refresh access token if necessary
if 'access_token' not in tokens or 'refresh_token' not in tokens:
    print("Missing access or refresh token.")
    exit(1)

access_token = tokens['access_token']
refresh_token = tokens['refresh_token']

# Refresh tokens if necessary
new_tokens = refresh_access_token(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, refresh_token)
if new_tokens:
    access_token = new_tokens['access_token']
    refresh_token = new_tokens['refresh_token']
    save_tokens('api/zoom_tokens.json', new_tokens)

# Define meeting details
meeting_details = {
    "topic": "Test Meeting",
    "type": 2,
    "start_time": "2024-06-15T15:00:00Z",
    "duration": 30,
    "timezone": "UTC",
    "agenda": "This is a test meeting",
    "settings": {
        "host_video": True,
        "participant_video": True,
        "mute_upon_entry": False,
        "watermark": True,
        "use_pmi": False,
        "approval_type": 0,
        "registration_type": 1,
        "audio": "both",
        "auto_recording": "none"
    }
}

# Schedule the meeting
join_url = schedule_meeting(access_token, meeting_details)
if join_url:
    print(f"Meeting scheduled successfully!\nJoin URL: {join_url}")
else:
    print("Failed to schedule meeting.")

