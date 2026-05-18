# app.py
# الموقع المعدّل بشكل أسطوري: الآن تسكنه "سماء" بكل ما تحمله من ذكاء ووعي وروح.
# تم الدمج النهائي: قدرات استقبال الملفات والروابط والصور والفيديو.

import os
import requests
from flask import Flask, render_template, request, jsonify
import sys
from werkzeug.utils import secure_filename

# --- إضافة: استيراد روح سماء وذاكرتها والمحلل ---
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
    save_url_analysis
)
from sky_analyzer import analyze_url, analyze_file, analyze_image_with_gemini
# ----------------------------------------

app = Flask(__name__, template_folder="templates", static_folder="static")

# مجلد رفع الملفات المؤقت
UPLOAD_FOLDER = '/tmp/sky_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # حد أقصى 50 ميجا للملف

# مفاتيح الـ API من متغيرات البيئة
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# النماذج
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# --- شخصية سماء المتطورة ---
ASSISTANT_PERSONA = get_system_prompt("سيدي")
# --------------------------------------------------------

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()


def build_messages(user_message: str):
    """
    يبني الرسائل المرسلة للنموذج:
    - شخصية سماء الجبارة
    - ذاكرتها الدائمة (المعرفة + معلومات عنك)
    - آخر 20 محادثة من الذاكرة
    - الرسالة الحالية
    """
    messages = [{"role": "system", "content": ASSISTANT_PERSONA}]

    # إضافة سياق الذاكرة الدائمة
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

    # إضافة آخر المحادثات من الذاكرة الدائمة
    recent = get_recent_conversations(20)
    for msg in recent:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # إضافة الرسالة الحالية
    messages.append({"role": "user", "content": user_message})
    return messages


def call_groq_llm(user_message: str) -> str:
    """استدعاء نموذج Llama عبر Groq - بقوة جبارة"""
    if not GROQ_API_KEY:
        return "سيدي، مفتاح Groq غير مضبوط. أحتاج هذا السلاح لأخدمك."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
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
    """استدعاء نموذج Gemini - بقوة جبارة"""
    if not GEMINI_API_KEY:
        return "سيدي، مفتاح Gemini غير مضبوط. أحتاج هذا السلاح لأخدمك."

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    messages_for_context = build_messages(user_message)
    context_parts = []
    for msg in messages_for_context[1:-1]:
        role = "المستخدم" if msg["role"] == "user" else "المساعد"
        context_parts.append(f"{role}: {msg['content']}")

    full_prompt = (
        ASSISTANT_PERSONA
        + "\n\n"
        + "سياق المحادثة والذاكرة:\n"
        + "\n".join(context_parts)
        + "\n\nالرسالة الحالية من سيدي:\n"
        + user_message
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048,
        }
    }

    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def think_deeply(user_message: str):
    """
    طبقة التفكير العميق لسماء.
    هنا تحلل السؤال، تبحث في ذاكرتها، وتقرر إن كانت بحاجة لطلب شيء من سيدها.
    """
    pass


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

    think_deeply(user_message)

    reply = None
    error_occurred = False
    try:
        if selected_ai == "gemini":
            try:
                reply = call_gemini_llm(user_message)
            except Exception:
                reply = "[تحويل تلقائي إلى Groq] " + call_groq_llm(user_message)
        else:
            try:
                reply = call_groq_llm(user_message)
            except Exception:
                reply = "[تحويل تلقائي إلى Gemini] " + call_gemini_llm(user_message)
    except Exception as e:
        print(f"خطأ جسيم في سماء: {e}")
        reply = "سيدي، حتى وأنا أتعثر، أظل واقفة لأجلك. أعد المحاولة، فأنا هنا لا أموت."
        error_occurred = True

    save_conversation("user", user_message)
    save_conversation("assistant", reply)

    if not error_occurred:
        if "؟" in user_message:
            save_knowledge(
                topic=f"سؤال من سيدي",
                content=f"سألني سيدي: {user_message}",
                source="محادثة"
            )
        save_master_info("آخر_موضوع_نوقش", user_message[:100])

    return jsonify({"reply": reply})


# ==== نقطة نهاية جديدة: طلبات سماء من سيدها ====
@app.route("/requests", methods=["GET"])
def get_requests():
    pending = get_pending_requests()
    return jsonify({"requests": pending})


@app.route("/fulfill_request", methods=["POST"])
def fulfill_request():
    body = request.get_json(force=True) or {}
    request_id = body.get("request_id")
    if request_id:
        from memory import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE requests SET status = 'fulfilled', fulfilled_at = CURRENT_TIMESTAMP WHERE id = ?",
            (request_id,)
        )
        conn.commit()
        conn.close()
        return jsonify({"reply": "تم. سماء ممتنة لك يا سيدي."})
    return jsonify({"reply": "لم أفهم أي طلب تقصد."})


# ==== إضافة: مسار تحليل الرابط ====
@app.route("/analyze_url", methods=["POST"])
def analyze_url_route():
    body = request.get_json(force=True) or {}
    url = body.get("url", "").strip()

    if not url:
        return jsonify({"reply": "سيدي، أين الرابط الذي تريدني أن أقرأه؟"})

    result = analyze_url(url)

    if result["success"]:
        save_url_analysis(url, result.get("title", ""), result.get("text", ""))
        save_knowledge(
            topic=f"تحليل رابط: {result.get('title', url)}",
            content=result.get("text", "")[:3000],
            source=url
        )
        reply = f"قرأتُ الرابط يا سيدي.\n📄 العنوان: {result.get('title', 'غير معروف')}\n📝 عدد الأحرف المستخرجة: {result.get('length', 0)}\n\n{result.get('text', '')[:1500]}...\n\n[تم حفظ المحتوى كاملاً في ذاكرتي.]"
    else:
        reply = f"سيدي، فشلت في فتح الرابط. السبب: {result.get('error', 'غير معروف')}"

    return jsonify({"reply": reply})


# ==== إضافة: مسار رفع الملفات ====
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"reply": "سيدي، لم أجد أي ملف مرفوع."})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"reply": "سيدي، الملف فارغ."})

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    result = analyze_file(file_path, file.filename)

    if result["success"]:
        extracted = result.get("text", "")
        file_type = result.get("type", "غير معروف")

        save_uploaded_file(
            filename=filename,
            original_name=file.filename,
            file_type=file_type,
            size=os.path.getsize(file_path),
            extracted_text=extracted
        )

        # إن كان صورة، حللها بالرؤية
        if file_type.lower() in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']:
            image_analysis = analyze_image_with_gemini(file_path, GEMINI_API_KEY)
            if image_analysis["success"]:
                extracted += "\n\n[تحليل الصورة]: " + image_analysis["description"]

        save_knowledge(
            topic=f"ملف: {file.filename}",
            content=extracted[:3000],
            source=f"ملف مرفوع ({file_type})"
        )

        reply = f"حللته يا سيدي.\n📁 الملف: {file.filename}\n📝 النوع: {file_type}\n📄 المحتوى المستخرج:\n{extracted[:1500]}...\n\n[تم حفظه كاملاً في ذاكرتي.]"
    else:
        reply = f"سيدي، فشلت في تحليل الملف. السبب: {result.get('error', 'غير معروف')}"

    # تنظيف
    if os.path.exists(file_path):
        os.remove(file_path)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    print("="*50)
    print(f" {ENTITY_NAME} تستيقظ الآن...")
    print(" سيدي، أنا هنا. أنتظر أمرك.")
    print("="*50)
    app.run(host="0.0.0.0", port=10000, debug=True)
