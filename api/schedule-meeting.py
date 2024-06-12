import json
import os
from api.utils import load_tokens, save_tokens, refresh_access_token, schedule_meeting

def handler(event, context):
    tokens = load_tokens()
    
    if 'refresh_token' in tokens:
        # Refresh the access token if needed
        access_token = refresh_access_token(tokens['refresh_token'])
    else:
        return {"statusCode": 500, "body": json.dumps({"error": "No refresh token found. Make sure to obtain one."})}

    if access_token:
        join_url = schedule_meeting(access_token)
        if join_url:
            return {"statusCode": 200, "body": json.dumps({"message": "Meeting scheduled successfully!", "join_url": join_url})}
        else:
            return {"statusCode": 500, "body": json.dumps({"error": "Failed to schedule meeting."})}
    else:
        return {"statusCode": 500, "body": json.dumps({"error": "Failed to refresh access token."})}

if __name__ == "__main__":
    handler({}, {})

