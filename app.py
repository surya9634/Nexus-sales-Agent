# Folder: automated_bot_app/
# File: app.py

from flask import Flask, request, render_template, jsonify
import requests
import json
from bots.ai_responder import generate_reply

app = Flask(__name__)

VERIFY_TOKEN = "surya_verify"
WHATSAPP_TOKEN = "YOUR_WHATSAPP_TOKEN"
INSTAGRAM_TOKEN = "YOUR_INSTAGRAM_TOKEN"

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# WhatsApp webhook verification
@app.route('/webhook/whatsapp', methods=['GET'])
def verify_whatsapp():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed"

# Instagram webhook verification
@app.route('/webhook/instagram', methods=['GET'])
def verify_instagram():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed"

# WhatsApp incoming message
@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    data = request.get_json()
    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry["changes"]:
                value = change["value"]
                if "messages" in value:
                    for msg in value["messages"]:
                        phone = msg["from"]
                        text = msg["text"]["body"]
                        reply = generate_reply(text)
                        send_whatsapp_reply(phone, reply)
    return "OK", 200

# Instagram incoming message
@app.route('/webhook/instagram', methods=['POST'])
def instagram_webhook():
    data = request.get_json()
    if data.get("entry"):
        for entry in data["entry"]:
            messaging = entry.get("messaging", [])
            for msg in messaging:
                sender = msg["sender"]["id"]
                text = msg["message"]["text"]
                reply = generate_reply(text)
                send_instagram_reply(sender, reply)
    return "OK", 200

def send_whatsapp_reply(phone, message):
    url = f"https://graph.facebook.com/v19.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)

def send_instagram_reply(sender_id, message):
    url = f"https://graph.facebook.com/v19.0/me/messages"
    headers = {
        "Authorization": f"Bearer {INSTAGRAM_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": message}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
