import json
import requests
import base64

def load_tokens(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_tokens(filename, tokens):
    with open(filename, 'w') as file:
        json.dump(tokens, file)

def refresh_access_token(client_id, client_secret, refresh_token):
    url = 'https://zoom.us/oauth/token'
    auth_string = f"{client_id}:{client_secret}"
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_string}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to refresh access token: {response.status_code} - {response.text}")
        return None

def schedule_meeting(access_token, meeting_details):
    url = 'https://api.zoom.us/v2/users/me/meetings'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=meeting_details)
    if response.status_code == 201:
        return response.json().get('join_url')
    else:
        print(f"Failed to schedule meeting: {response.status_code} - {response.text}")
        return None


