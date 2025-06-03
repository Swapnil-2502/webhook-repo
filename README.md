# 📡 GitHub Webhook Receiver (Flask Backend)

This repository contains the backend service that receives and logs GitHub Webhook events such as `PUSH`, `PULL REQUEST`, and `MERGE`. It stores these events in a MongoDB database and provides an API to retrieve them, enabling real-time activity display in the connected frontend UI.

---

## 📦 Project Structure

This is part of a larger 3-repo system:

1. **[Action-repo](https://github.com/Swapnil-2502/action-repo)** – Where actual GitHub activity (push, pull requests, merge) takes place.
2. **Webhook-repo (this repo)** – A Flask backend exposed via public URL to receive and log webhook events.
3. **[Webhook-Frontend](https://github.com/Swapnil-2502/Webhook-Frontend)** – A React frontend that polls and displays GitHub event activity to users.

---

## 🧠 Features

- ✅ Handles GitHub `push` and `pull_request` webhook events.
- ✅ Detects and avoids duplicate commits (via unique `request_id`).
- ✅ Differentiates between PR creation (`PULL REQUEST`) and PR merge (`MERGE`).
- ✅ Stores all activity in MongoDB.
- ✅ Exposes a `/api/events_data` endpoint for frontend polling.
- ✅ CORS enabled for frontend-backend interaction.

---

## 🚀 Getting Started

### 🛠 Prerequisites

- Python 3.8+
- pip
- MongoDB Atlas or local MongoDB instance
- `.env` file with the following:
		 MONGODB_URL=mongodb+srv://<your-mongo-uri>

### 📥 Installation

```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo
pip install -r requirements.txt
```

🏃 Running the Server
Local (for testing):
```bash
python -m flask run --port=5002
```

### 🔄 GitHub Webhook Setup

1.  Go to your `action-repo` on GitHub.
    
2.  Settings → Webhooks → Add Webhook
    
3.  Payload URL: `http://<your-public-ip>:5002/webhook` Or you can use Ngrok to expose your local server to the internet.
    
4.  Content type: `application/json`
    
5.  Events to send:
    
    -   ✅ Just the `push` and `pull_request` events
        
6.  Click **Add Webhook**

## 🧪 API Endpoints

### `POST /webhook`

Receives GitHub webhook payload. Internally handles and stores events.

### `GET /api/events_data`

Returns all logged events in JSON format:

## 👨‍💻 Author

**Swapnil Hajare**