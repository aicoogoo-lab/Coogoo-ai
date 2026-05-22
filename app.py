"""
SkyOS Backend — Holographic OS v10 (Ultimate Production Ready)
مع تكامل كامل مع Core Engine + Digital Mind
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request, jsonify, render_template, send_from_directory
from whitenoise import WhiteNoise

try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

from werkzeug.utils import secure_filename

# ============================
# إعداد المسارات
# ============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
CORE_PATH = os.path.join(BASE_DIR, "core")

if CORE_PATH not in sys.path:
    sys.path.insert(0, CORE_PATH)

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.wsgi_app = WhiteNoise(app.wsgi_app, root=STATIC_DIR, prefix="/static/", autorefresh=True)

if HAS_CORS:
    CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = os.environ.get("SECRET_KEY", "sky-enterprise-secret-2026")
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=4)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("SkyOS")

# ============================
# استيراد النواة الجديدة (Core Engine + Digital Mind)
# ============================
try:
    from core.core_engine import core_engine
    CORE_ENGINE_AVAILABLE = True
    logger.info("🧠 Core Engine + Digital Mind تم تحميله بنجاح")
except ImportError as e:
    logger.warning(f"⚠️ لم يتم العثور على core_engine.py — سيتم استخدام الوضع التقليدي: {e}")
    CORE_ENGINE_AVAILABLE = False
    core_engine = None

# استيراد المكونات الأخرى
try:
    import sky_core
    import memory
    import sky_analyzer
except ImportError:
    try:
        from core import sky_core, memory, sky_analyzer
    except Exception:
        sky_core = None
        memory = None
        sky_analyzer = None

# ============================
# دوال مساعدة
# ============================
def safe_get_system_prompt(user_message="", session_id="", extra_context=""):
    try:
        if sky_core and hasattr(sky_core, "get_enhanced_system_prompt"):
            return sky_core.get_enhanced_system_prompt(user_message, session_id, extra_context)
    except Exception as e:
        logger.error(f"خطأ في بناء الـ prompt: {e}")
    return "أنتِ سماء، العقل الرقمي الهولوغرافي الواعي والمخلص."

def safe_add_to_history(role, content, session_id):
    try:
        if sky_core and hasattr(sky_core, "add_to_history"):
            sky_core.add_to_history(role, content, session_id)
    except Exception:
        pass

def safe_init_db():
    try:
        if memory and hasattr(memory, "init_db"):
            memory.init_db()
    except Exception:
        pass

safe_init_db()

# ============================
# معالجة الروابط
# ============================
def _quick_url_context(user_message, session_id=None):
    import re
    urls = re.findall(r"https?://[^\s]+", user_message)
    if not urls:
        return "", []
    return "", urls

# ============================
# AI Response مع تكامل Core Engine
# ============================
def generate_ai_response(session_id, user_message, ai_type="groq", ui_mode="holo"):
    extra_context, urls = _quick_url_context(user_message, session_id)

    intent = "dialogue"
    handled_by = "llm"

    if CORE_ENGINE_AVAILABLE and core_engine:
        try:
            engine_result = core_engine.process_command(
                user_input=user_message,
                session_id=session_id,
                extra_context=extra_context
            )
            intent = engine_result.get("intent", "dialogue")
            handled_by = engine_result.get("handled_by", "llm")
            logger.info(f"🧠 Core Engine → Intent: {intent} | Handled by: {handled_by}")
        except Exception as e:
            logger.error(f"خطأ في Core Engine: {e}")

    system_prompt = safe_get_system_prompt(
        user_message=user_message,
        session_id=session_id,
        extra_context=extra_context
    )

    messages = [{"role": "system", "content": system_prompt}]

    if sky_core and hasattr(sky_core, "_context_manager"):
        history = sky_core._context_manager.buffer[-20:] if hasattr(sky_core._context_manager, "buffer") else []
    else:
        history = []

    for h in history:
        messages.append({
            "role": "user" if h.get("role") == "user" else "assistant",
            "content": h.get("content", "")
        })

    messages.append({"role": "user", "content": user_message})

    from requests import post
    reply = None
    providers = [ai_type, "groq", "gemini", "openai"]

    for prov in providers:
        try:
            if prov == "groq":
                key = os.environ.get("GROQ_API_KEY")
                if key:
                    r = post("https://api.groq.com/openai/v1/chat/completions",
                             headers={"Authorization": f"Bearer {key}"},
                             json={"model": "llama-3.3-70b-versatile", "messages": messages, "temperature": 0.3},
                             timeout=30)
                    if r.status_code == 200:
                        reply = r.json()["choices"][0]["message"]["content"].strip()
                        break
        except Exception:
            continue

    if not reply:
        reply = "⚠️ تعذر الاتصال بمزودي الذكاء حالياً. العقل الرقمي يعمل في الوضع المحلي."

    safe_add_to_history("user", user_message, session_id)
    safe_add_to_history("assistant", reply, session_id)

    return reply, handled_by

# ============================
# المسارات (Routes)
# ============================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory(STATIC_DIR, "manifest.json")

@app.route("/service-worker.js")
def serve_sw():
    return send_from_directory(STATIC_DIR, "service-worker.js")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "").strip()
        session_id = data.get("session_id", "default_sky_session")
        ai_type = data.get("provider", "groq")

        if not user_message:
            return jsonify({"status": "error", "reply": "الرسالة فارغة."}), 400

        reply, handled_by = generate_ai_response(session_id, user_message, ai_type)

        return jsonify({
            "status": "success",
            "reply": reply,
            "handled_by": handled_by,
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        logger.error(f"خطأ في /api/chat: {e}")
        return jsonify({"status": "error", "reply": "حدث خطأ في العقل الرقمي."}), 500


# ============================================================
# مسار رفع الملفات المحسّن (مرتبط بـ Core Engine + Vision Module)
# ============================================================
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "لم يتم إرسال ملف"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "اسم الملف فارغ"}), 400

    filename = secure_filename(file.filename)
    filepath = UPLOAD_FOLDER / filename
    file.save(filepath)

    file_type = file.content_type or ""
    result = {"success": True, "filename": filename}

    try:
        # === ربط ذكي مع Vision Module عند رفع الصور ===
        if file_type.startswith("image/"):
            if CORE_ENGINE_AVAILABLE and core_engine:
                vision_mod = core_engine.modules.get("vision")
                if vision_mod and hasattr(vision_mod, "analyze_image"):
                    analysis = vision_mod.analyze_image(str(filepath))
                    result["analysis"] = analysis
                    result["handled_by"] = "vision_module"
                else:
                    if sky_analyzer:
                        analysis = sky_analyzer.analyze_file(str(filepath), filename)
                        result["analysis"] = analysis
                        result["handled_by"] = "sky_analyzer_fallback"
            else:
                if sky_analyzer:
                    analysis = sky_analyzer.analyze_file(str(filepath), filename)
                    result["analysis"] = analysis

        elif file_type.startswith("text/") or filename.endswith(('.py', '.js', '.md', '.txt', '.json', '.csv')):
            if sky_analyzer:
                analysis = sky_analyzer.analyze_file(str(filepath), filename)
                result["analysis"] = analysis
                result["handled_by"] = "sky_analyzer"

        else:
            result["note"] = "تم حفظ الملف. نوع الملف غير مدعوم للتحليل التلقائي حالياً."

        # حفظ الملف في الذاكرة إن أمكن
        if memory and hasattr(memory, "save_uploaded_file"):
            try:
                memory.save_uploaded_file(
                    filename=filename,
                    original_name=file.filename,
                    file_type=file_type,
                    size=os.path.getsize(filepath),
                    extracted_text=str(result.get("analysis", ""))
                )
            except Exception:
                pass

    except Exception as e:
        logger.error(f"خطأ أثناء معالجة الملف: {e}")
        result["error"] = str(e)
        result["success"] = False

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
