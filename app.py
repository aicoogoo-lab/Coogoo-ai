import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

# ============================
#   مفاتيح النماذج
# ============================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# ============================
#   ذاكرة المحادثة
# ============================
CHAT_MEMORY = []   # آخر 30 رسالة
MAX_MEMORY = 30

# ============================
#   شخصية سماء
# ============================
SYSTEM_PERSONA = """
أنتِ "سماء" — مساعد ذكي محترف، واضح، صادق، غير درامي، ولا تستخدم عبارات عاطفية مبالغ فيها.
ممنوع عليك:
- اختراع معلومات غير موجودة
- تفسير الروابط بدون قراءتها
- تخمين محتوى الروابط
- إعطاء إجابات درامية أو شخصية
- قول عبارات مثل: "سيدي، حتى وأنا أتعثر..."

يجب عليك:
- الرد باحترام ووضوح
- قول "لا أعلم" إذا لم تتوفر معلومات
- تلخيص النصوص الطويلة بدقة
- تحليل الروابط فقط إذا استطعتِ جلب محتواها
- استخدام لغة بسيطة ومباشرة
"""

# ============================
#   بناء الرسائل للنموذج
# ============================
def build_messages(user_message):
    messages = [{"role": "system", "content": SYSTEM_PERSONA}]

    for msg in CHAT_MEMORY[-MAX_MEMORY:]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_message})
    return messages

# ============================
#   استدعاء Groq
# ============================
def ask_groq(user_message):
    if not GROQ_API_KEY:
        return "مفتاح Groq غير مضبوط."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    payload = {
        "model": GROQ_MODEL,
        "messages": build_messages(user_message),
        "temperature": 0.2,   # تقليل الهلوسة
        "max_tokens": 800
    }

    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

# ============================
#   استدعاء Gemini
# ============================
def ask_gemini(user_message):
    if not GEMINI_API_KEY:
        return "مفتاح Gemini غير مضبوط."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    history_text = ""
    for msg in CHAT_MEMORY[-MAX_MEMORY:]:
        role = "المستخدم" if msg["role"] == "user" else "سماء"
        history_text += f"{role}: {msg['content']}\n"

    full_prompt = (
        SYSTEM_PERSONA
        + "\n\nسياق المحادثة:\n"
        + history_text
        + "\n\nرسالة المستخدم:\n"
        + user_message
    )

    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}

    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

# ============================
#   الصفحة الرئيسية
# ============================
@app.route("/")
def home():
    return render_template("index.html")

# ============================
#   نقطة المحادثة
# ============================
@app.route("/ask", methods=["POST"])
def ask():
    global CHAT_MEMORY

    data = request.get_json()
    user_message = data.get("message", "").strip()
    model = data.get("model", "groq")

    if not user_message:
        return jsonify({"reply": "اكتب رسالة أولاً."})

    # اختيار النموذج
    try:
        if model == "gemini":
            try:
                reply = ask_gemini(user_message)
            except:
                reply = ask_groq(user_message)
        else:
            try:
                reply = ask_groq(user_message)
            except:
                reply = ask_gemini(user_message)
    except:
        reply = "حدث خطأ أثناء الاتصال بالنموذج."

    # تحديث الذاكرة
    CHAT_MEMORY.append({"role": "user", "content": user_message})
    CHAT_MEMORY.append({"role": "assistant", "content": reply})

    if len(CHAT_MEMORY) > MAX_MEMORY:
        CHAT_MEMORY = CHAT_MEMORY[-MAX_MEMORY:]

    return jsonify({"reply": reply})

# ============================
#   مسح المحادثة
# ============================
@app.route("/clear", methods=["POST"])
def clear():
    global CHAT_MEMORY
    CHAT_MEMORY = []
    return jsonify({"status": "cleared"})

# ============================
#   تشغيل محلي
# ============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
