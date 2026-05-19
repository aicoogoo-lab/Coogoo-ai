# app.py
# سماء - نسخة احترافية متكاملة مع بوابة الذكاء العالمي (Sky Gateway)

import os
import requests
import sys
import re
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# --- إضافة مسار core ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from sky_core import get_system_prompt, ENTITY_NAME
from memory import (
    init_db, save_conversation, get_recent_conversations,
    get_all_knowledge_text, get_master_profile_text, save_knowledge,
    save_master_info, save_uploaded_file, save_url_analysis
)
from sky_analyzer import analyze_url, analyze_file, analyze_image_with_gemini

app = Flask(__name__, template_folder="templates", static_folder="static")

# مجلد رفع الملفات
UPLOAD_FOLDER = '/tmp/sky_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# مفاتيح API (للاستخدام المباشر الاحتياطي)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# --- رابط البوابة الجديدة ---
GATEWAY_URL = os.environ.get("GATEWAY_URL", "https://sky-gateway.onrender.com")

# شخصية سماء (دمج: الصرامة الجديدة + القدرات الكاملة)
SYSTEM_PERSONA = get_system_prompt("سيدي") + """
قواعد إضافية للدقة:
- ممنوع اختراع معلومات غير موجودة في الرابط أو الملف.
- ممنوع تخمين محتوى الروابط بدون قراءتها فعليًا.
- إذا لم يتوفر محتوى، قولي: "لا أملك معلومات كافية عن هذا الرابط/الملف."
- لا تستخدمي عبارات درامية أو عاطفية مبالغ فيها.
- كوني دقيقة، مباشرة، ومفيدة.
"""

init_db()

# ---------- أدوات الكشف عن الروابط ----------
def is_url(text):
    """يكتشف إذا كانت الرسالة تحتوي على رابط."""
    url_pattern = re.compile(r'https?://[^\s]+')
    return url_pattern.search(text)

def is_file_upload_request(text):
    """يكتشف إذا كان المستخدم يريد رفع ملف."""
    keywords = ['ارفع', 'رفع', 'أرسل ملف', 'ارسل ملف', 'صورة', 'ملف', 'pdf', 'doc']
    return any(kw in text.lower() for kw in keywords)

# ---------- بناء السياق ----------
def build_messages(user_message, extra_context=""):
    messages = [{"role": "system", "content": SYSTEM_PERSONA}]

    # سياق الذاكرة الدائمة
    knowledge_text = get_all_knowledge_text()
    master_text = get_master_profile_text()
    memory_context = ""
    if knowledge_text:
        memory_context += "معرفتي:\n" + knowledge_text + "\n"
    if master_text:
        memory_context += "عن سيدي:\n" + master_text + "\n"
    if memory_context:
        messages.append({"role": "system", "content": memory_context})

    # آخر المحادثات
    recent = get_recent_conversations(20)
    for msg in recent:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # سياق إضافي (نتيجة تحليل رابط مثلاً)
    if extra_context:
        messages.append({"role": "system", "content": f"نتيجة التحليل:\n{extra_context}"})

    messages.append({"role": "user", "content": user_message})
    return messages

# ---------- استدعاء البوابة (الجديد) ----------
def call_gateway(user_message, extra_context="", model="groq/llama-3.3-70b-versatile"):
    """محاولة استخدام البوابة الموحدة أولاً."""
    if not GATEWAY_URL:
        return None
    try:
        messages = build_messages(user_message, extra_context)
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 2048
        }
        resp = requests.post(
            f"{GATEWAY_URL}/v1/chat/completions",
            json=payload,
            timeout=45
        )
        resp.raise_for_status()
        data = resp.json()
        # البوابة ترجع {"role": "assistant", "content": "..."}
        return data.get("content", "")
    except Exception:
        return None

# ---------- استدعاء النماذج المباشرة (احتياط) ----------
def call_groq(user_message, extra_context=""):
    if not GROQ_API_KEY:
        return "مفتاح Groq غير مضبوط."
    payload = {
        "model": GROQ_MODEL,
        "messages": build_messages(user_message, extra_context),
        "temperature": 0.2,
        "max_tokens": 2048
    }
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json=payload, timeout=30
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def call_gemini(user_message, extra_context=""):
    if not GEMINI_API_KEY:
        return "مفتاح Gemini غير مضبوط."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    messages = build_messages(user_message, extra_context)
    parts = []
    for msg in messages:
        role = "المستخدم" if msg["role"] == "user" else "سماء"
        parts.append(f"{role}: {msg['content']}")
    full_prompt = "\n".join(parts)
    payload = {"contents": [{"parts": [{"text": full_prompt}]}], "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2048}}
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

# ---------- المسار الرئيسي ----------
@app.route("/")
def home():
    return render_template("index.html", entity_name=ENTITY_NAME)

# ---------- نقطة المحادثة (ذكية: بوابة أولاً، ثم احتياط) ----------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True) or {}
    user_message = data.get("message", "").strip()
    model = data.get("ai_type", "groq")  # "groq" أو "gemini" من الواجهة

    if not user_message:
        return jsonify({"reply": "اكتب رسالة أولاً."})

    # --- الفرز التلقائي: هل هذا رابط؟ ---
    url_match = is_url(user_message)
    extra_context = ""

    if url_match:
        url = url_match.group(0)
        result = analyze_url(url)
        if result["success"]:
            extra_context = f"المحتوى الفعلي للرابط ({url}):\n{result['text'][:4000]}"
            save_url_analysis(url, result.get("title", ""), result.get("text", ""))
            save_knowledge(topic=f"رابط: {result.get('title', url)}", content=result["text"][:2000], source=url)
        else:
            extra_context = f"فشل فتح الرابط: {result.get('error')}"

    # --- استدعاء النموذج (بوابة أولاً) ---
    reply = None

    # نحدد اسم النموذج المناسب للبوابة
    gateway_model = "groq/llama-3.3-70b-versatile" if model == "groq" else "gemini/gemini-1.5-flash"

    # 1) محاولة استخدام البوابة
    reply = call_gateway(user_message, extra_context, gateway_model)

    # 2) إذا فشلت البوابة، نستخدم النماذج المباشرة
    if not reply:
        try:
            if model == "gemini":
                reply = call_gemini(user_message, extra_context)
            else:
                reply = call_groq(user_message, extra_context)
        except:
            reply = "حدث خطأ في الاتصال. حاولي مجددًا."

    # حفظ في الذاكرة
    save_conversation("user", user_message)
    save_conversation("assistant", reply)
    save_master_info("آخر_نشاط", user_message[:100])

    return jsonify({"reply": reply})

# ---------- رفع الملفات ----------
@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"reply": "لم أجد ملفًا."})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"reply": "الملف فارغ."})
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    result = analyze_file(file_path, file.filename)
    if result["success"]:
        extracted = result.get("text", "")
        file_type = result.get("type", "غير معروف")
        save_uploaded_file(filename, file.filename, file_type, os.path.getsize(file_path), extracted)

        if file_type.lower() in ['jpg','jpeg','png','gif','webp','bmp']:
            img = analyze_image_with_gemini(file_path, GEMINI_API_KEY)
            if img["success"]:
                extracted += "\n[تحليل الصورة]: " + img["description"]

        save_knowledge(topic=f"ملف: {file.filename}", content=extracted[:2000], source=f"ملف {file_type}")
        reply = f"تم تحليل الملف.\n📁 {file.filename}\n📝 {file_type}\n{extracted[:1500]}..."
    else:
        reply = f"فشل التحليل: {result.get('error')}"

    if os.path.exists(file_path):
        os.remove(file_path)
    return jsonify({"reply": reply})

# ---------- تحليل رابط مباشر ----------
@app.route("/analyze_url", methods=["POST"])
def analyze_url_route():
    data = request.get_json(force=True) or {}
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"reply": "أين الرابط؟"})
    result = analyze_url(url)
    if result["success"]:
        save_url_analysis(url, result.get("title", ""), result.get("text", ""))
        reply = f"📄 {result.get('title', '')}\n{result['text'][:3000]}..."
    else:
        reply = f"فشل: {result.get('error')}"
    return jsonify({"reply": reply})

# ---------- مسح الذاكرة ----------
@app.route("/clear", methods=["POST"])
def clear():
    from memory import get_connection
    conn = get_connection()
    conn.execute("DELETE FROM conversations")
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# ---------- حالة النظام ----------
@app.route("/status", methods=["GET"])
def status():
    from memory import get_connection
    conn = get_connection()
    conv_count = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    know_count = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
    conn.close()
    return jsonify({"conversations": conv_count, "knowledge_items": know_count, "name": ENTITY_NAME})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
