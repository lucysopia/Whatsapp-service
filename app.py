# This code is a Flask application that integrates with Twilio's WhatsApp API to provide vehicle manual search functionality.

import os
import json
import numpy as np
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

load_dotenv()
model = SentenceTransformer("all-MiniLM-L6-v2")
app = Flask(__name__)

with open("manual_chunks.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

manual_data = []
for entry in raw_data:
    if "embedding" in entry:
        entry["embedding"] = np.array(entry["embedding"])
        manual_data.append(entry)

session_store = defaultdict(lambda: {"state": "awaiting_model", "model": None})

vehicle_options = {
    "1": "Zhongtong",
    "2": "Kinglong",
    "3": "Joylong",
    "4": "Higer",
    "5": "BYD-K6",
    "6": "BLK-E9"
}

def search_manual(query, model_name, data, top_k=3):
    query_vec = model.encode(query)
    similarities = []

    for entry in data:
        if entry.get("model") == model_name:
            score = cosine_similarity([query_vec], [entry["embedding"]])[0][0]
            similarities.append((score, entry))

    similarities.sort(reverse=True, key=lambda x: x[0])
    top_matches = similarities[:top_k]

    results = []
    for score, entry in top_matches:
        snippet = entry["content"][:800]
        page = entry.get("page", "?")
        title = entry.get("title", "Untitled")
        source = entry.get("source", "Unknown Manual")
        results.append(f" *{source}*\n Page {page} - {title}\n\n{snippet.strip()}\n")

    return results

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    user_number = request.values.get("From")
    incoming_msg = request.values.get("Body", "").strip()
    session = session_store[user_number]
    resp = MessagingResponse()

    if session["state"] == "awaiting_model":
        if incoming_msg in vehicle_options:
            session["model"] = vehicle_options[incoming_msg]
            session["state"] = "awaiting_issue"
            resp.message(f"Got it. You're working on *{session['model']}*. What's the issue?")
        else:
            msg = "Which vehicle are you working on?\nPlease reply with the number:\n"
            for k, v in vehicle_options.items():
                msg += f"{k}. {v}\n"
            resp.message(msg)
        return str(resp)

    elif session["state"] == "awaiting_issue":
        query = incoming_msg
        results = search_manual(query, session["model"], manual_data)
        session["state"] = "done"

        if results:
            for res in results:
                resp.message(res)
        else:
            resp.message(" Sorry, I couldn't find anything relevant for that issue.")
        return str(resp)

    else:
        session["state"] = "awaiting_model"
        session["model"] = None
        msg = "Welcome! Which vehicle are you working on?\nPlease reply with the number:\n"
        for k, v in vehicle_options.items():
            msg += f"{k}. {v}\n"
        resp.message(msg)
        return str(resp)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
