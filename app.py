import nltk
nltk.download('punkt_tab')

from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from flask_cors import CORS
import mysql.connector
import uuid
import os
import re

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "supersecret"
CORS(app)


db_config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "aria_db",
    "auth_plugin": "caching_sha2_password"
}


GEMINI_KEY = "AIzaSyCTxfLflpqC7onzId5IfdyicrF0FdATuJQ"   # replace with your key
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def is_response_useful(text):
    if not text:
        return False
    txt = text.strip()
    if len(re.sub(r'\s+', '', txt)) < 20:  # short check
        return False
    low = txt.lower()
    bad = ["i don't know", "not sure", "sorry", "cannot", "can't help"]
    return not any(b in low for b in bad)

def detect_emotion(user_input):
    """Use Gemini instead of text2emotion for more accurate results"""
    try:
        prompt = f"""
        Analyze the following user text and respond with only the dominant emotion 
        from this list: [Happy, Sad, Angry, Fear, Surprise, Neutral].
        User text: "{user_input}"
        """
        resp = model.generate_content(prompt)
        emotion = resp.text.strip().capitalize()
        if emotion not in ["Happy", "Sad", "Angry", "Fear", "Surprise", "Neutral"]:
            return "Neutral"
        return emotion
    except Exception as e:
        print("Emotion detection error:", e)
        return "Neutral"

# ---------- routes ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/new_session", methods=["POST"])
def new_session():
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    return jsonify({"session_id": session_id})

@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json or {}
    user_input = payload.get("message", "")
    session_id = session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id

    
    dominant_emotion = detect_emotion(user_input)

    
    prompt = f"""
    You are ARIA, an empathetic and professional AI assistant.
    The user said: "{user_input}".
    Detected emotion: {dominant_emotion}.

    Respond in a warm, natural, and human-like way.
    - Keep it 2–4 sentences.
    - Do not repeat the same phrase often.
    - If the user is sad, comfort them sincerely.
    - If the user is happy, share in their joy.
    - If the user is angry, acknowledge calmly.
    - If the user is fearful, reassure gently.
    - If neutral, be helpful and friendly.
    Vary your expressions each time so it feels human.
    """

    aria_reply = ""
    try:
        if not user_input.strip():
            aria_reply = "Please type something — I’m here to listen."
        else:
            resp = model.generate_content(prompt)
            aria_reply = getattr(resp, "text", "") or ""
    except Exception as e:
        print("Gemini error:", e)
        aria_reply = "I had trouble responding just now. Can you try again?"

    
    if not aria_reply.strip():
        aria_reply = "I'm here with you. Can you share a little more about what’s on your mind?"

    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_message, aria_reply, emotion, session_id) VALUES (%s, %s, %s, %s)",
            (user_input, aria_reply, dominant_emotion, session_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB insert error:", e)

    return jsonify({
        "user": user_input,
        "aria": aria_reply,
        "emotion": dominant_emotion,
        "session_id": session_id
    })


@app.route("/history/<session_id>", methods=["GET"])
def history(session_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_message, aria_reply, emotion, timestamp FROM chat_history WHERE session_id=%s ORDER BY timestamp ASC",
            (session_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB history error:", e)
        rows = []
    return jsonify(rows)

@app.route("/sessions", methods=["GET"])
def sessions():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT session_id, MIN(user_message) AS title, MIN(timestamp) AS created_at
            FROM chat_history
            GROUP BY session_id
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB sessions error:", e)
        rows = []
    for r in rows:
        if not r.get("title"):
            r["title"] = "New Chat"
    return jsonify(rows)

@app.route("/clear_history/<session_id>", methods=["POST"])
def clear_history(session_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE session_id=%s", (session_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB clear error:", e)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
