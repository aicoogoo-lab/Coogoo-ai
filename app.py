import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# قراءة مفاتيح الـ API من متغيرات البيئة بأمان
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# النماذج المستخدمة (استخدمنا هنا نموذج لاما 70 بي الخارق!)
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"


def call_groq_llm(user_message: str) -> str:
    """استدعاء نموذج Llama القوي عبر Groq"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful, smart assistant."},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def call_gemini_llm(user_message: str) -> str:
    """استدعاء نموذج Gemini الذكي عبر قوقل"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": user_message}]}]}
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    body = request.get_json(force=True) or {}
    user_message = body.get("message", "").strip()
    selected_ai = body.get("ai_type", "gemini")  # يقرأ الاختيار القادم من أزرار الواجهة

    if not user_message:
        return jsonify({"reply": "الرجاء كتابة رسالة أولاً."})

    # التحقق من وجود المفاتيح
    if selected_ai == "gemini" and not GEMINI_API_KEY:
        return jsonify({"reply": "مفتاح Gemini غير مضبوط في السيرفر."})
    if selected_ai == "groq" and not GROQ_API_KEY:
        return jsonify({"reply": "مفتاح Groq غير مضبوط في السيرفر."})

    # منطق التشغيل الذكي مع ميزة التحويل الاحتياطي التلقائي عند سقوط أي سيرفر
    try:
        if selected_ai == "gemini":
            try:
                reply = call_gemini_llm(user_message)
            except Exception:
                reply = "[تحويل تلقائي احتياطي] " + call_groq_llm(user_message)
        else:
            try:
                reply = call_groq_llm(user_message)
            except Exception:
                reply = "[تحويل تلقائي احتياطي] " + call_gemini_llm(user_message)
    except Exception as e:
        reply = "عذراً يا صديقي، يبدو أن كلا السيرفرين واجها مشكلة في نفس الوقت. حاول مجدداً."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
