"""
سماء - التطبيق الرئيسي المتكامل
النسخة الاحترافية المتقدمة v4.5
متوافقة مع memory.py v3.9 | واعية + RLHF + شخصية متطورة
"""

import os
import uuid
import logging
import traceback
from pathlib import Path
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import sys
sys.path.append(str(Path(__file__).parent / "core"))

from memory import (
    init_db,
    save_conversation,
    get_full_conversation_context,
    get_all_knowledge_text,
    save_knowledge,
    save_uploaded_file,
    save_url_analysis,
    clear_conversation_history,
    process_feedback,
    get_personality_summary,
    save_master_info
)
from sky_core import get_enhanced_system_prompt, add_to_history, ENTITY_NAME
from sky_analyzer import analyze_url, analyze_file, analyze_image_with_gemini

# ====================== إعداد التطبيق ======================
app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.environ.get("SECRET_KEY", "sky-professional-secret-2026")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", app.secret_key)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=90)

jwt = JWTManager(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["80 per minute"],
    storage_uri="memory://"
)

UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

init_db()


# ====================== دوال مساعدة ======================
def extract_urls(text: str):
    import re
    return re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s<>"\']*', text)


def analyze_urls_automatically(message: str):
    urls = extract_urls(message)
    extra = ""
    for url in urls[:3]:
        try:
            result = analyze_url(url)
            if result.get("success"):
                title = result.get("title", url)
                text = result.get("text", "")[:2600]
                extra += f"\n🔗 {title}\n{text}\n---\n"
                save_url_analysis(url, title, text)
                save_knowledge(topic=f"رابط: {title}", content=text[:1800], source=url)
        except Exception as e:
            logger.warning(f"فشل تحليل رابط: {e}")
    return extra


def call_provider(messages: list, provider: str):
    import requests
    try:
        if provider == "groq":
            key = os.environ.get("GROQ_API_KEY")
            if not key: return None
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
                    "messages": messages,
                    "temperature": 0.32,
                    "max_tokens": 2200
                },
                timeout=55
            )
            return r.json()["choices"][0]["message"]["content"].strip()

        elif provider == "gemini":
            key = os.environ.get("GEMINI_API_KEY")
            if not key: return None
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            prompt = "\n\n".join([f"{m['role']}: {m['content']}" for m in messages])
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=55)
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        logger.warning(f"فشل استدعاء {provider}: {e}")
        return None
    return None


def generate_ai_response(session_id: str, user_message: str, ai_type: str = "groq"):
    extra_context = analyze_urls_automatically(user_message)

    messages = [{"role": "system", "content": get_enhanced_system_prompt(user_message, session_id)}]

    if knowledge := get_all_knowledge_text():
        messages.append({"role": "system", "content": f"معرفتي الدائمة:\n{knowledge}"})

    history = get_full_conversation_context(session_id, 45)
    for h in history[-38:]:
        messages.append({"role": "user" if h["role"] == "user" else "assistant", "content": h["content"]})

    if extra_context:
        messages.append({"role": "system", "content": f"معلومات من الروابط:\n{extra_context}"})

    messages.append({"role": "user", "content": user_message})

    for prov in [ai_type, "groq", "gemini"]:
        if reply := call_provider(messages, prov):
            return reply, prov

    return "⚠️ جميع مزودي الذكاء الاصطناعي غير متاحين حالياً.", "offline"


# ====================== المسارات ======================

@app.route("/")
def home():
    return render_template("index.html", entity_name=ENTITY_NAME)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True) or {}
    message = data.get("message", "").strip()
    ai_type = data.get("ai_type", "groq")
    session_id = data.get("session_id") or str(uuid.uuid4())

    if not message:
        return jsonify({"reply": "أسمعك يا سيدي.", "session_id": session_id})

    save_conversation("user", message, session_id)
    add_to_history("user", message, session_id)
    save_master_info("last_activity", datetime.utcnow().isoformat())

    reply, provider = generate_ai_response(session_id, message, ai_type)

    save_conversation("assistant", reply, session_id)
    add_to_history("assistant", reply, session_id)

    return jsonify({"reply": reply, "session_id": session_id, "provider": provider})


@app.route("/upload", methods=["POST"])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"reply": "لم يتم إرسال أي ملف."})

        file = request.files['file']
        session_id = request.form.get('session_id') or str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER / filename
        file.save(file_path)

        analysis = analyze_file(str(file_path), filename)
        extracted = analysis.get("text", "")[:7500] if analysis.get("success") else ""

        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            gemini = analyze_image_with_gemini(str(file_path), os.environ.get("GEMINI_API_KEY"))
            if gemini.get("success"):
                extracted += f"\n\n[تحليل Gemini Vision]:\n{gemini['description']}"

        save_uploaded_file(filename, file.filename, analysis.get("type", ""), file_path.stat().st_size, extracted)
        save_conversation("user", f"[رفع ملف: {filename}]", session_id)
        save_conversation("assistant", f"تم تحليل الملف بنجاح.\n{extracted[:2200]}", session_id)

        file_path.unlink(missing_ok=True)
        return jsonify({"reply": f"✅ تم تحليل الملف بنجاح.\n\n{extracted[:2000]}", "session_id": session_id})

    except RequestEntityTooLarge:
        return jsonify({"reply": "الملف كبير جداً (الحد الأقصى 50 ميجا)."})
    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"reply": "حدث خطأ أثناء معالجة الملف."})


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json(force=True) or {}
    process_feedback("", "", float(data.get("score", 0)), data.get("session_id"), data.get("comment", ""))
    return jsonify({"success": True})


@app.route("/clear", methods=["POST"])
def clear():
    clear_conversation_history(request.get_json(force=True).get("session_id"))
    return jsonify({"status": "success"})


@app.route("/api/v1/status", methods=["GET"])
def api_status():
    return jsonify({
        "name": ENTITY_NAME,
        "version": "4.5",
        "groq": bool(os.environ.get("GROQ_API_KEY")),
        "gemini": bool(os.environ.get("GEMINI_API_KEY")),
        "rlhf": "PPO-Inspired + Personality Evolution",
        "personality": get_personality_summary()
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
