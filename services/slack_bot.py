# slack_adk_bot_sessions.py
from flask import Flask, request, make_response
import os
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
ADK_BASE_URL = "http://127.0.0.1:8000"
ADK_AGENT_NAME = "agents"

# store user sessions in memory
user_sessions = {}

# fetch bot user id
SLACK_BOT_USER_ID = None
def get_bot_user_id():
    global SLACK_BOT_USER_ID
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    resp = requests.get("https://slack.com/api/auth.test", headers=headers)
    data = resp.json()
    if data.get("ok"):
        SLACK_BOT_USER_ID = data["user_id"]
    print("Bot user ID:", SLACK_BOT_USER_ID)

get_bot_user_id()

def get_or_create_session(user_id):
    # Generate a consistent session ID (or use a mapping to store per-user)
    session_id = str(uuid.uuid4())

    url = f"{ADK_BASE_URL}/apps/{ADK_AGENT_NAME}/users/{user_id}/sessions/{session_id}"
    
    # Create session with the ID
    resp = requests.post(url, json={})
    
    if resp.status_code == 200 or resp.status_code == 201:
        print(f"Created session for {user_id}: {session_id}")
        return session_id
    else:
        print(f"Failed to create session: {resp.status_code} {resp.text}")
        return None

def run_adk_agent(user_id, user_text):
    session_id = get_or_create_session(user_id)
    if not session_id:
        return "Error creating session"

    payload = {
        "appName": ADK_AGENT_NAME,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "parts": [{"text": user_text}],
            "role": "user"
        },
        "streaming": False,
        "stateDelta": {}
    }

    resp = requests.post(f"{ADK_BASE_URL}/run", json=payload)
    if resp.status_code != 200:
        return f"Error from ADK agent: {resp.status_code} {resp.text}"

    adk_resp = resp.json()
    
    # Extract text from ADK response
    message_text = ""
    for event in adk_resp:
        for part in event.get("content", {}).get("parts", []):
            if "text" in part:
                message_text = part["text"]

    return message_text or "No response from ADK agent"



# 3️⃣ Slack event endpoint
@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    if data.get("type") == "url_verification":
        return make_response(data.get("challenge"), 200, {"content_type": "text/plain"})

    if data.get("type") == "event_callback":
        event = data.get("event", {})
        user_id = event.get("user")
        channel_id = event.get("channel")

        if event.get("subtype") == "bot_message" or user_id is None or user_id == SLACK_BOT_USER_ID:
            return make_response("", 200)

        user_text = event.get("text")
        print(f"Message from {user_id}: {user_text}")

        # Call ADK agent
        response_text = run_adk_agent(user_id, user_text)
        print(f"ADK response: {response_text}")

        # Send back to Slack
        # Send back to Slack (fixed)
        headers = {
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "channel": channel_id,
            "text": response_text
        }
        resp = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
        print("Slack API response:", resp.status_code, resp.text)


        return make_response("", 200)

    return make_response("", 200)

if __name__ == "__main__":
    app.run(port=3000)
