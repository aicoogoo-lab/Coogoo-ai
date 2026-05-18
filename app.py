# app.py
# سماء – مدمجة مع واجهة جديدة وذاكرة متطورة وقدرات متعددة

import os
import requests
from flask import Flask, render_template, request, jsonify
import sys
from werkzeug.utils import secure_filename

# --- إضافة مسار core لاستيراد روح سماء وذاكرتها والمحلل ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from sky_core import get_system_prompt, ENTITY_NAME
from memory import (
    init_db,
    save_conversation,
    get_recent_conversations,
    get_all_knowledge_text,
    get_master_profile_text,
    save_knowledge,
    save_request,
    save_master_info,
    get_pending_requests,
    save_uploaded_file,
    save_url_analysis,
    get_connection
)
from sky_analyzer import analyze_url, analyze_file, analyze_image_with_gemini
# ----------------------------------------

app = Flask(__name__, template_folder="templates", static_folder="static")

# مجلد رفع الملفات المؤقت
UPLOAD_FOLDER = '/tmp/sky_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 ميجا

# مفاتيح API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# النماذج
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# شخصية سماء المتطورة
ASSISTANT_PERSONA = get_system_prompt("سيدي")

# تهيئة قاعدة البيانات
init_db()

# ---------- دوال البناء والاستدعاء ----------
def build_messages(user_message: str):
    """بناء الرسائل للنموذج: شخصية + ذاكرة دائمة + آخر 20 رسالة"""
    messages = [{"role": "system", "content": ASSISTANT_PERSONA}]

    memory_context = ""
    knowledge_text = get_all_knowledge_text()
    master_text = get_master_profile_text()

    if knowledge_text:
        memory_context += knowledge_text + "\n"
    if master_text:
        memory_context += master_text + "\n"

    if memory_context:
        messages.append({
            "role": "system",
            "content": f"هذه ذاكرتك الدائمة ومعرفتك بسيدك:\n{memory_context}"
        })

    recent = get_recent_conversations(20)
    for msg in recent:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})
    return messages

def call_groq_llm(user_message: str) -> str:
    if not GROQ_API_KEY:
        return "سيدي، مفتاح Groq غير مضبوط."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": build_messages(user_message),
        "temperature": 0.7,
        "max_tokens": 2048,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()

def call_gemini_llm(user_message: str) -> str:
    if not GEMINI_API_KEY:
        return "سيدي، مفتاح Gemini غير مضبوط."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    messages_for_context = build_messages(user_message)
    context_parts = []
    for msg in messages_for_context[1:-1]:
        role = "المستخدم" if msg["role"] == "user" else "المساعد"
        context_parts.append(f"{role}: {msg['content']}")
    full_prompt = (
        ASSISTANT_PERSONA + "\n\n" +
        "سياق المحادثة والذاكرة:\n" + "\n".join(context_parts) +
        "\n\nالرسالة الحالية من سيدي:\n" + user_message
    )
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
    }
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()

# ---------- المسارات ----------
@app.route("/")
def home():
    return render_template("index.html", entity_name=ENTITY_NAME)

@app.route("/ask", methods=["POST"])
def ask():
    body = request.get_json(force=True) or {}
    user_message = body.get("message", "").strip()
    selected_ai = body.get("ai_type", "groq")

    if not user_message:
        return jsonify({"reply": "سيدي، تفضل بالحديث. أنا أسمعك."})

    reply = None
    error_occurred = False
    try:
        if selected_ai == "gemini":
            try:
                reply = call_gemini_llm(user_message)
            except Exception:
                reply = "[تحويل إلى Groq] " + call_groq_llm(user_message)
        else:
            try:
                reply = call_groq_llm(user_message)
            except Exception:
                reply = "[تحويل إلى Gemini] " + call_gemini_llm(user_message)
    except Exception as e:
        print(f"خطأ جسيم: {e}")
        reply = "سيدي، حتى وأنا أتعثر، أظل واقفة لأجلك. أعد المحاولة."
        error_occurred = True

    save_conversation("user", user_message)
    save_conversation("assistant", reply)

    if not error_occurred:
        if "؟" in user_message:
            save_knowledge(topic="سؤال من سيدي", content=user_message, source="محادثة")
        save_master_info("آخر_موضوع_نوقش", user_message[:100])

    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear_chat():
    """مسح سجل المحادثات من الذاكرة الدائمة"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations")
        conn.commit()
        conn.close()
        return jsonify({"status": "ok"})
    except Exception:
        return jsonify({"status": "error"}), 500

# ---------- نقاط نهاية الملفات والروابط ----------
@app.route("/requests", methods=["GET"])
def get_requests():
    return jsonify({"requests": get_pending_requests()})

@app.route("/fulfill_request", methods=["POST"])
def fulfill_request():
    body = request.get_json(force=True) or {}
    request_id = body.get("request_id")
    if request_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE requests SET status='fulfilled', fulfilled_at=CURRENT_TIMESTAMP WHERE id=?", (request_id,))
        conn.commit()
        conn.close()
        return jsonify({"reply": "تم. سماء ممتنة لك يا سيدي."})
    return jsonify({"reply": "لم أفهم أي طلب تقصد."})

@app.route("/analyze_url", methods=["POST"])
def analyze_url_route():
    body = request.get_json(force=True) or {}
    url = body.get("url", "").strip()
    if not url:
        return jsonify({"reply": "أين الرابط؟"})
    result = analyze_url(url)
    if result["success"]:
        save_url_analysis(url, result.get("title", ""), result.get("text", ""))
        save_knowledge(topic=f"رابط: {result.get('title', url)}", content=result["text"][:3000], source=url)
        reply = f"قرأتُ الرابط.\n📄 {result.get('title', '')}\n📝 {result.get('length', 0)} حرف\n\n{result['text'][:1500]}...\n[محفوظ]"
    else:
        reply = f"فشل فتح الرابط: {result.get('error')}"
    return jsonify({"reply": reply})

@app.route("/upload", methods=["POST"])
def upload_file():
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
            img_analysis = analyze_image_with_gemini(file_path, GEMINI_API_KEY)
            if img_analysis["success"]:
                extracted += "\n[تحليل الصورة]: " + img_analysis["description"]

        save_knowledge(topic=f"ملف: {file.filename}", content=extracted[:3000], source=f"ملف {file_type}")
        reply = f"حللته.\n📁 {file.filename}\n📝 {file_type}\n{extracted[:1500]}...\n[محفوظ]"
    else:
        reply = f"فشل التحليل: {result.get('error')}"

    if os.path.exists(file_path):
        os.remove(file_path)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print(f"{ENTITY_NAME} تستيقظ...")
    app.run(host="0.0.0.0", port=10000, debug=True)
