# File: bots/ai_responder.py

import requests
import json
from config import load_config

def generate_reply(user_message):
    config = load_config()
    groq_key = config.get("groq_api_key")
    if not groq_key:
        return "AI is not configured."

    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "model": "mixtral-8x7b-32768"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Sorry, I couldn’t understand that."
