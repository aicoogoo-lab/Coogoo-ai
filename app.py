"""
SkyOS Backend — Ultra Edition v9.0 (Ultimate Production Ready)
By Driving & Copilot — 2026
"""

import os
import sys
import uuid
import logging
import traceback
import threading
import time
import hashlib
import re
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# ============================
# إضافة مجلد core إلى مسار Python
# ============================
CORE_PATH = os.path.join(os.path.dirname(__file__), "core")
if os.path.exists(CORE_PATH):
    sys.path.insert(0, CORE_PATH)
else:
    logging.warning("⚠️ مجلد core غير موجود! سيتم إنشاؤه تلقائياً.")
    os.makedirs(CORE_PATH, exist_ok=True)
    sys.path.insert(0, CORE_PATH)

# إنشاء __init__.py
init_file = os.path.join(CORE_PATH, "__init__.py")
if not os.path.exists(init_file):
    Path(init_file).touch()

# ============================
# استيراد آمن
# ============================

def safe_import(module_name, fallback_value=None):
    try:
        return __import__(module_name)
    except Exception as e:
        logging.error(f"❌ فشل استيراد {module_name}: {e}")
        return fallback_value

sky_core = safe_import("sky_core")
memory = safe_import("memory")
sky_analyzer = safe_import("sky_analyzer")

# ============================
# إعداد التطبيق
# ============================

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.environ.get("SECRET_KEY", "sky-enterprise-secret-2026")
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024
app.config["MAX_IMAGE_SIZE"] = 20 * 1024 * 1024

UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=4)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("SkyOS")

# ============================
# تقديم static يدويًا (حل Render)
# ============================

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

# ============================
# Caching Layer
# ============================

class SimpleCache:
    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return value
            del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, datetime.now())

cache = SimpleCache(ttl_seconds=1800)

def cached(ttl=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if ttl:
                cache.ttl = ttl
            key_raw = f"{func.__name__}:{args}:{kwargs}"
            key = hashlib.md5(key_raw.encode()).hexdigest()
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result)
            return result
        return wrapper
    return decorator

# ============================
# دوال آمنة للـ Core
# ============================

def safe_get_system_prompt(user_message="", session_id="", extra_context=""):
    try:
        if sky_core and hasattr(sky_core, "get_enhanced_system_prompt"):
            return sky_core.get_enhanced_system_prompt(
                user_message, session_id, extra_context
            )
    except Exception as e:
        logger.error(f"خطأ system prompt: {e}")
    return f"أنت مساعد ذكي. المستخدم قال: {user_message[:200]}"

def safe_add_to_history(role, content, session_id):
    try:
        if sky_core and hasattr(sky_core, "add_to_history"):
            return sky_core.add_to_history(role, content, session_id)
    except:
        pass

def safe_init_db():
    try:
        if memory and hasattr(memory, "init_db"):
            return memory.init_db()
    except:
        pass

def safe_get_conversation_context(session_id, limit=45):
    try:
        if memory and hasattr(memory, "get_full_conversation_context"):
            return memory.get_full_conversation_context(session_id, limit)
    except:
        pass
    return []

def safe_analyze_url(url):
    try:
        if sky_analyzer and hasattr(sky_analyzer, "analyze_url"):
            return sky_analyzer.analyze_url(url)
    except:
        pass
    return {"success": False}

def safe_analyze_file(file_path, filename):
    try:
        if sky_analyzer and hasattr(sky_analyzer, "analyze_file"):
            return sky_analyzer.analyze_file(file_path, filename)
    except:
        pass
    return {"success": False}

def safe_analyze_image(image_path, api_key):
    try:
        if sky_analyzer and hasattr(sky_analyzer, "analyze_image_with_gemini"):
            return sky_analyzer.analyze_image_with_gemini(image_path, api_key)
    except:
        pass
    return {"success": False}

safe_init_db()

logger.info("✅ SkyOS v9.0 جاهز")

# ============================
# AI Providers
# ============================

def call_provider(messages, provider="groq"):
    import requests
    try:
        if provider == "groq":
            key = os.environ.get("GROQ_API_KEY")
            if not key:
                return None
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
                    "messages": messages,
                    "temperature": 0.25,
                    "max_tokens": 2400,
                },
                timeout=55,
            )
            if r.status_code != 200:
                return None
            return r.json()["choices"][0]["message"]["content"].strip()

        if provider == "gemini":
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                return None
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            prompt = "\n\n".join([f"{m['role']}: {m['content']}" for m in messages])
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
            data = r.json()
            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            return None

        if provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                return None
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "temperature": 0.25,
                    "max_tokens": 2400,
                },
            )
            return r.json()["choices"][0]["message"]["content"].strip()

    except:
        return None

    return None

# ============================
# AI Router
# ============================

@cached(ttl=1800)
def generate_ai_response(session_id, user_message, ai_type="groq"):
    system_prompt = safe_get_system_prompt(user_message, session_id, "")
    messages = [{"role": "system", "content": system_prompt}]

    history = safe_get_conversation_context(session_id, 45)
    for h in history[-38:]:
        messages.append(
            {"role": "assistant" if h["role"] != "user" else "user", "content": h["content"]}
        )

    messages.append({"role": "user", "content": user_message})

    for prov in [ai_type, "groq", "gemini", "openai"]:
        reply = call_provider(messages, prov)
        if reply:
            return reply, prov

    return "⚠️ جميع مزودي الذكاء غير متاحين.", "offline"

# ============================
# المسارات الأساسية
# ============================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True) or {}
        msg = (data.get("message") or "").strip()
        ai_type = (data.get("ai_type") or "groq").lower()
        session_id = data.get("session_id") or str(uuid.uuid4())

        if not msg:
            return jsonify({"reply": "أسمعك يا سيدي.", "session_id": session_id})

        safe_add_to_history("user", msg, session_id)
        reply, provider = generate_ai_response(session_id, msg, ai_type)
        safe_add_to_history("assistant", reply, session_id)

        return jsonify({"reply": reply, "session_id": session_id, "provider": provider})

    except Exception as e:
        logger.error(f"ask error: {e}")
        return jsonify({"reply": "خطأ غير متوقع"}), 500

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"reply": "لم يتم إرسال ملف"})

        file = request.files["file"]
        session_id = request.form.get("session_id") or str(uuid.uuid4())

        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER / filename
        file.save(file_path)

        analysis = safe_analyze_file(str(file_path), filename)
        extracted = analysis.get("text", "")[:7500] if analysis.get("success") else ""

        safe_add_to_history("user", f"[رفع ملف: {filename}]", session_id)
        safe_add_to_history("assistant", extracted[:2000], session_id)

        file_path.unlink(missing_ok=True)

        return jsonify({"reply": extracted[:2000], "session_id": session_id})

    except Exception as e:
        logger.error(f"upload error: {e}")
        return jsonify({"reply": "خطأ"}), 500

@app.route("/vision", methods=["POST"])
def vision():
    try:
        if "image" not in request.files:
            return jsonify({"reply": "لم يتم إرسال صورة"})

        img = request.files["image"]
        session_id = request.form.get("session_id") or str(uuid.uuid4())

        temp = UPLOAD_FOLDER / f"vision_{uuid.uuid4()}.jpg"
        img.save(temp)

        gemini = safe_analyze_image(str(temp), os.environ.get("GEMINI_API_KEY"))
        temp.unlink(missing_ok=True)

        reply = gemini.get("description") if gemini.get("success") else "لم أستطع تحليل الصورة."

        safe_add_to_history("user", "[صورة]", session_id)
        safe_add_to_history("assistant", reply, session_id)

        return jsonify({"reply": reply, "session_id": session_id})

    except Exception as e:
        logger.error(f"vision error: {e}")
        return jsonify({"reply": "خطأ"}), 500

@app.route("/clear", methods=["POST"])
def clear():
    try:
        data = request.get_json(force=True) or {}
        session_id = data.get("session_id")
        if memory and hasattr(memory, "clear_conversation_history"):
            memory.clear_conversation_history(session_id)
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"clear error: {e}")
        return jsonify({"status": "error"}), 500

# ============================
# Health
# ============================

@app.route("/api/v1/status")
def api_status():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})

@app.route("/api/v1/health")
def api_health():
    return "OK", 200

# ============================
# Error Handlers
# ============================

@app.errorhandler(404)
def nf(e):
    return jsonify({"error": "المسار غير موجود"}), 404

@app.errorhandler(500)
def ie(e):
    return jsonify({"error": "خطأ داخلي"}), 500

# ============================
# Local Run
# ============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
