# app.py
# الموقع المعدّل: الآن تسكنه "سماء" بدلاً من المساعد العام.

import os
import requests
from flask import Flask, render_template, request, jsonify
import sys

# --- إضافة: استيراد روح سماء ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from sky_core import get_system_prompt, ENTITY_NAME
# --------------------------------

app = Flask(__name__, template_folder="templates", static_folder="static")

# مفاتيح الـ API من متغيرات البيئة
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# النماذج
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# ذاكرة محادثة داخل السيرفر
CHAT_HISTORY = []  # [{"role": "user"/"assistant", "content": "..." }]

# --- تعديل: شخصية المساعد أصبحت تستدعى من روح سماء ---
# كان اسم المتغير: ASSISTANT_PERSONA
# الآن نستدعيها من ملف السماء لتصبح ديناميكية
ASSISTANT_PERSONA = get_system_prompt("سيدي")
# -----------------------------------------------------


def build_messages(user_message: str):
    """يبني الرسائل المرسلة للنموذج (شخصية + تاريخ + رسالة حالية)"""
    messages = [{"role": "system", "content": ASSISTANT_PERSONA}]

    for msg in CHAT_HISTORY[-10:]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_message})
    return messages


def call_groq_llm(user_message: str) -> str:
    """استدعاء نموذج Llama عبر Groq"""
    if not GROQ_API_KEY:
        return "مفتاح Groq غير مضبوط في السيرفر."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": build_messages(user_message),
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def call_gemini_llm(user_message: str) -> str:
    """استدعاء نموذج Gemini عبر REST API"""
    if not GEMINI_API_KEY:
        return "مفتاح Gemini غير مضبوط في السيرفر."

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    history_text = ""
    for msg in CHAT_HISTORY[-10:]:
        role = "المستخدم" if msg["role"] == "user" else "المساعد"
        history_text += f"{role}: {msg['content']}\n"

    full_prompt = (
        ASSISTANT_PERSONA
        + "\n\n"
        + "سياق المحادثة السابقة:\n"
        + history_text
        + "\nالرسالة الحالية من المستخدم:\n"
        + user_message
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ]
    }

    resp = requests.post(url, json=payload, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


@app.route("/")
def home():
    # --- تعديل: إرسال اسم الكيان للواجهة ---
    return render_template("index.html", entity_name=ENTITY_NAME)
    # -----------------------------------------

@app.route("/ask", methods=["POST"])
def ask():
    global CHAT_HISTORY

    body = request.get_json(force=True) or {}
    user_message = body.get("message", "").strip()
    selected_ai = body.get("ai_type", "groq")  # "groq" أو "gemini"

    if not user_message:
        return jsonify({"reply": "الرجاء كتابة رسالة أولاً."})

    # اختيار الذكاء + تحويل احتياطي
    try:
        if selected_ai == "gemini":
            try:
                reply = call_gemini_llm(user_message)
            except Exception:
                reply = "[تم التحويل تلقائياً إلى Groq] " + call_groq_llm(
                    user_message
                )
        else:
            try:
                reply = call_groq_llm(user_message)
            except Exception:
                reply = "[تم التحويل تلقائياً إلى Gemini] " + call_gemini_llm(
                    user_message
                )
    except Exception:
        reply = "حدثت مشكلة في الاتصال بالنماذج حالياً. حاول مرة أخرى لاحقاً."

    # تحديث الذاكرة
    CHAT_HISTORY.append({"role": "user", "content": user_message})
    CHAT_HISTORY.append({"role": "assistant", "content": reply})

    if len(CHAT_HISTORY) > 100:
        CHAT_HISTORY = CHAT_HISTORY[-100:]

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
