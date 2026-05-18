import os
import sys
import requests
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# ---------- إعدادات المسار ----------
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from sky_core import get_system_prompt, ENTITY_NAME
from memory import (
    init_db, save_conversation, get_recent_conversations,
    get_all_knowledge_text, get_master_profile_text,
    save_knowledge, save_master_info, save_uploaded_file, save_url_analysis
)
from sky_analyzer import analyze_url, analyze_file, analyze_image_with_gemini

app = Flask(__name__, template_folder="templates", static_folder="static")
init_db()

# مجلد رفع الملفات
UPLOAD_FOLDER = '/tmp/sky_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# المفاتيح
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

SYSTEM_PERSONA = get_system_prompt("سيدي")

# ======================== بناء الرسائل (يدمج الذاكرة الدائمة) ========================
def build_messages(user_message):
    messages = [{"role": "system", "content": SYSTEM_PERSONA}]

    # إضافة معرفة السماء وملف السيد
    knowledge_text = get_all_knowledge_text()
    master_text = get_master_profile_text()
    if knowledge_text or master_text:
        ctx = "ذاكرتي الدائمة:\n" + knowledge_text + "\n" + master_text
        messages.append({"role": "system", "content": ctx})

    # آخر 20 رسالة من الذاكرة الدائمة
    recent = get_recent_conversations(20)
    for msg in recent:
        messages.append(msg)

    messages.append({"role": "user", "content": user_message})
    return messages

# ======================== استدعاء النماذج ========================
def call_groq(user_message):
    if not GROQ_API_KEY: return "مفتاح Groq غير مضبوط."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": GROQ_MODEL, "messages": build_messages(user_message), "temperature": 0.2, "max_tokens": 800}
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def call_gemini(user_message):
    if not GEMINI_API_KEY: return "مفتاح Gemini غير مضبوط."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    messages_for_context = build_messages(user_message)
    context_parts = []
    for msg in messages_for_context[1:-1]:
        role = "المستخدم" if msg["role"] == "user" else "سماء"
        context_parts.append(f"{role}: {msg['content']}")
    full_prompt = SYSTEM_PERSONA + "\n\n" + "السياق:\n" + "\n".join(context_parts) + "\n\nرسالة سيدي:\n" + user_message
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

def get_ai_reply(user_message, model):
    try:
        if model == "gemini":
            try: return call_gemini(user_message)
            except: return call_groq(user_message)
        else:
            try: return call_groq(user_message)
            except: return call_gemini(user_message)
    except: return "خطأ في الاتصال. حاول مرة أخرى."

# ======================== المسارات ========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    model = data.get("model", "groq")

    if not user_message:
        return jsonify({"reply": "أنا جاهز. تفضل."})

    reply = get_ai_reply(user_message, model)
    save_conversation("user", user_message)
    save_conversation("assistant", reply)
    save_master_info("آخر_موضوع_نوقش", user_message[:100])

    return jsonify({"reply": reply})

@app.route("/analyze_url", methods=["POST"])
def handle_url():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url: return jsonify({"reply": "أين الرابط؟"})

    result = analyze_url(url)
    if result["success"]:
        title = result.get("title", "")
        text = result.get("text", "")
        save_url_analysis(url, title, text)
        save_knowledge(topic=f"رابط: {title}", content=text[:3000], source=url)

        # نجعل النموذج يرد بناءً على المحتوى الحقيقي
        prompt = f"حلل هذا النص من رابط <{url}> بدقة. العنوان: {title}. النص: {text[:2000]}... أجب سيدي مباشرة."
        reply = get_ai_reply(prompt, "groq")
    else:
        reply = f"فشل فتح الرابط: {result.get('error')}"
    return jsonify({"reply": reply})

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files: return jsonify({"reply": "لم أجد ملفًا."})
    file = request.files['file']
    if file.filename == '': return jsonify({"reply": "الملف فارغ."})

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    result = analyze_file(filepath, file.filename)
    if result["success"]:
        text = result.get("text", "")
        ftype = result.get("type", "")
        save_uploaded_file(filename, file.filename, ftype, os.path.getsize(filepath), text)

        if ftype.lower() in ['jpg','jpeg','png']:
            img = analyze_image_with_gemini(filepath, GEMINI_API_KEY)
            if img["success"]: text += "\n[صورة]: " + img["description"]

        save_knowledge(topic=f"ملف: {file.filename}", content=text[:3000], source="ملف مرفوع")
        prompt = f"حلل هذا الملف المرفوع من سيدي. اسمه {file.filename}، محتواه: {text[:2000]}... أجب سيدي مباشرة."
        reply = get_ai_reply(prompt, "groq")
    else:
        reply = f"فشل تحليل الملف: {result.get('error')}"

    os.remove(filepath)
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    from memory import get_connection
    conn = get_connection()
    conn.cursor().execute("DELETE FROM conversations")
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
