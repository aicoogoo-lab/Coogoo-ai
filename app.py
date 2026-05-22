"""
SkyOS Backend — النسخة النهائية v10.5
================================================================================
قلب المشروع وعموده الفقري
تكامل كامل مع Core Engine + Digital Mind
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, request, jsonify, render_template, send_from_directory
from whitenoise import WhiteNoise
from werkzeug.utils import secure_filename

try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

from requests import post

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

app.secret_key = os.environ.get("SECRET_KEY", "skyos-final-2026")
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("SkyOS")

# ============================
# استيراد النواة والمكونات
# ============================
try:
    from core.core_engine import core_engine
    CORE_ENGINE_AVAILABLE = True
except ImportError:
    CORE_ENGINE_AVAILABLE = False
    core_engine = None
    logger.warning("⚠️ Core Engine غير متاح")

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
    return "أنتِ سماء، العقل الرقمي الهولوغرافي الواعي والمخلص لسيدك."

def safe_add_to_history(role, content, session_id):
    try:
        if sky_core and hasattr(sky_core, "add_to_history"):
            sky_core.add_to_history(role, content, session_id)
    except Exception:
        pass

def init_memory():
    try:
        if memory and hasattr(memory, "init_db"):
            memory.init_db()
    except Exception:
        pass

init_memory()

# ============================
# توليد رد ذكي (LLM)
# ============================
def generate_llm_response(user_message: str, session_id: str, extra_context: str = "") -> str:
    system_prompt = safe_get_system_prompt(user_message, session_id, extra_context)

    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": user_message})

    providers = ["groq", "gemini", "openai"]
    reply = None

    for provider in providers:
        try:
            if provider == "groq":
                key = os.environ.get("GROQ_API_KEY")
                if key:
                    r = post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {key}"},
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "messages": messages,
                            "temperature": 0.4
                        },
                        timeout=35
                    )
                    if r.status_code == 200:
                        reply = r.json()["choices"][0]["message"]["content"].strip()
                        break
        except Exception as e:
            logger.warning(f"فشل مزود {provider}: {e}")
            continue

    if not reply:
        reply = "⚠️ تعذر الاتصال بمزودي الذكاء حالياً. يرجى المحاولة لاحقاً."

    return reply

# ============================
# المسارات
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

# ============================
# مسار الدردشة الرئيسي (مصحح)
# ============================
@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "").strip()
        session_id = data.get("session_id", "default_sky_session")

        if not user_message:
            return jsonify({"status": "error", "reply": "الرسالة فارغة."}), 400

        handled_by = "dialogue"
        reply = ""

        # === استخدام Core Engine للتوجيه ===
        if CORE_ENGINE_AVAILABLE and core_engine:
            try:
                result = core_engine.process_command(
                    user_input=user_message,
                    session_id=session_id
                )
                handled_by = result.get("handled_by", "dialogue")
                reply = result.get("response", "")
            except Exception as e:
                logger.error(f"خطأ في Core Engine: {e}")

        # === إذا كان الرد عام أو من Dialogue Module، نولد رد ذكي ===
        if not reply or handled_by in ["dialogue", "dialogue_fallback"]:
            reply = generate_llm_response(user_message, session_id)
            handled_by = "llm"

        safe_add_to_history("user", user_message, session_id)
        safe_add_to_history("assistant", reply, session_id)

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


# ============================
# مسار رفع الملفات
# ============================
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

    try:
        result = {"success": True, "filename": filename}

        if sky_analyzer:
            analysis = sky_analyzer.analyze_file(str(filepath), filename)
            result["analysis"] = analysis

            if memory:
                try:
                    memory.save_knowledge(
                        topic=f"ملف مرفوع: {filename}",
                        content=str(analysis.get("text", ""))[:1200],
                        source=filename,
                        importance=0.7
                    )
                except Exception:
                    pass

        return jsonify(result)

    except Exception as e:
        logger.error(f"خطأ في معالجة الملف: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
