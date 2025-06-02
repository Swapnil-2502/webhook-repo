from flask import Flask,request, jsonify

import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MongoDB_url = os.getenv("MONGODB_URL")
client = MongoClient(MongoDB_url)
db = client.Webhook
collections = db.events_data

@app.route('/')
def home():
    return "GitHub Webhook Receiver is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    print(f"Received GitHub Event: {event_type}")
    
    if event_type == 'pull_request':
        handle_pull_request(data)
    elif event_type == 'push':
        handle_push_event(data)
    else:
        print("Unhandled event type:", event_type)


    return jsonify({"status": "received"}), 200

def handle_push_event(data):
    for commit in data.get("commits", []):
        if collections.find_one({"request_id": commit.get("id")}):
            print("Skipping duplicate PUSH event for request_id:", commit.get("id"))
            continue
        
        event = {
            "request_id": commit.get("id"),
            "author": commit.get("author", {}).get("name"),
            "action": "PUSH",
            "from_branch": None,
            "to_branch": data.get("ref").split("/")[-1],  # refs/heads/dev → dev
            "timestamp": commit.get("timestamp")
        }
        print("Inserting PUSH event:", event)
        collections.insert_one(event)

def handle_pull_request(data):
    action_type = data.get("action")
    pr = data.get("pull_request", {})
    
    if action_type == "opened":
        event_action = "PULL REQUEST"
    elif action_type == "closed" and pr.get("merged"):
        event_action = "MERGE"
    else:
        return
    
    event = {
        "request_id": str(pr.get("id")),
        "author": pr.get("user", {}).get("login"),
        "action": event_action,
        "from_branch": pr.get("head", {}).get("ref"),
        "to_branch": pr.get("base", {}).get("ref"),
        "timestamp": pr.get("created_at") if event_action == "PULL REQUEST" else pr.get("merged_at")
    }
    
    print(f"Inserting {event_action} event:", event)
    collections.insert_one(event)
    

if __name__ == '__main__':
    app.run(debug=True)
