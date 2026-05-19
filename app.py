# app.py
"""
سماء - الكيان الجبار
النسخة النهائية v2.5 Ultimate (Unified)
"""

import os
import sys
import uuid
import logging
import traceback
import re
from pathlib import Path
from datetime import datetime, timedelta

import requests
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ====================== إعداد مسارات المشروع ======================
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR / "core"))

from sky_core import get_system_prompt, ENTITY_NAME
from memory import (
    init_db, save_conversation, get_full_conversation_context,
    get_all_knowledge_text, get_master_profile_text,
    save_knowledge, save_master_info, save_uploaded_file,
    save_url_analysis, clear_conversation_history
)
from sky_analyzer import analyze_url, analyze_file, analyze_image_with_gemini

# ====================== تهيئة Flask ======================
app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.environ.get("SECRET_KEY", "sky-ultimate-secret-2026-v2")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", app.secret_key)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

# ====================== Rate Limiting ======================
redis_url = os.environ.get("REDIS_URL", "memory://")
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["60 per minute"],
    storage_uri=redis_url,
    strategy="fixed-window"
)

# ====================== إعدادات التطبيق ======================
class Config:
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    UPLOAD_FOLDER = Path("/tmp/sky_uploads")
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'md', 'jpg', 'jpeg', 'png', 'gif', 'webp', 'docx', 'csv', 'json'}

config = Config()
app.config.from_object(config)
config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# ====================== Logging ======================
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

init_db()


# ====================== مدير الذاكرة ======================
class SkyMemory:
    @staticmethod
    def get_session_id():
        return (request.get_json(silent=True) or {}).get('session_id') or str(uuid.uuid4())

    @staticmethod
    def save(session_id: str, role: str, content: str):
        try:
            save_conversation(role, content, session_id)
        except Exception as e:
            logger.error(f"فشل حفظ الرسالة: {e}")

    @staticmethod
    def get_context(session_id: str, limit: int = 50):
        try:
            return get_full_conversation_context(session_id, limit)
        except Exception:
            return []

    @staticmethod
    def clear(session_id: str):
        try:
            clear_conversation_history(session_id)
        except Exception:
            pass

memory = SkyMemory()


# ====================== دوال مساعدة ======================
def extract_urls(text: str):
    return re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s<>"\']*', text)

def analyze_urls_automatically(message: str):
    urls = extract_urls(message)
    extra_context = ""
    for url in urls[:3]:
        try:
            result = analyze_url(url)
            if result.get("success"):
                title = result.get("title", "رابط")
                text = result.get("text", "")[:2800]
                extra_context += f"\n🔗 {title}\n{text}\n---\n"
                save_url_analysis(url, title, text)
                save_knowledge(topic=f"رابط: {title}", content=text[:2000], source=url)
        except Exception as e:
            logger.warning(f"فشل تحليل الرابط {url}: {e}")
    return extra_context


# ====================== استدعاء مزودي الذكاء ======================
def call_ai_provider(messages: list, provider: str):
    try:
        if provider == "groq":
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key: return None
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
                    "messages": messages, "temperature": 0.35, "max_tokens": 2048
                },
                timeout=60
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()

        elif provider == "gemini":
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key: return None
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')}:generateContent?key={api_key}"
            prompt = ""
            for m in messages:
                role = "سيدي" if m['role'] == 'user' else ("سماء" if m['role'] == 'assistant' else "تعليمات")
                prompt += f"[{role}]: {m['content']}\n\n"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

        elif provider == "gateway":
            gw = os.environ.get("GATEWAY_URL")
            if not gw: return None
            resp = requests.post(
                f"{gw.rstrip('/')}/v1/chat/completions",
                json={"model": "groq/llama-3.3-70b-versatile", "messages": messages, "temperature": 0.35, "max_tokens": 2048},
                timeout=8
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("content") or data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        logger.warning(f"مزود {provider} فشل: {str(e)[:100]}")
        return None


# ====================== بناء الرد الذكي ======================
def get_ai_response(session_id: str, user_message: str, ai_type: str = "groq"):
    extra_context = analyze_urls_automatically(user_message)

    messages = [{"role": "system", "content": get_system_prompt("سيدي")}]

    if knowledge := get_all_knowledge_text():
        messages.append({"role": "system", "content": f"📚 معرفتي:\n{knowledge}"})
    if master := get_master_profile_text():
        messages.append({"role": "system", "content": f"👤 سيدي:\n{master}"})

    history = memory.get_context(session_id, 55)
    if history:
        for m in history[-45:]:
            role = "user" if m['role'] == 'user' else "assistant"
            messages.append({"role": role, "content": m['content']})

    if extra_context:
        messages.append({"role": "system", "content": f"🔗 معلومات من الروابط:\n{extra_context}"})

    messages.append({"role": "user", "content": user_message})

    for prov in [ai_type, "gateway", "gemini" if ai_type == "groq" else "groq"]:
        if response := call_ai_provider(messages, prov):
            return response.strip(), prov
    return "⚠️ جميع خدمات الذكاء معطلة حالياً.", "offline"


# ====================== معالجة أخطاء JWT ======================
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"success": False, "error": "انتهت صلاحية التوكن", "code": "TOKEN_EXPIRED"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"success": False, "error": "توكن غير صالح", "code": "INVALID_TOKEN"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"success": False, "error": "مطلوب توكن للوصول", "code": "MISSING_TOKEN"}), 401


# ====================== Routes API v1 ======================
@app.route("/api/v1/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "sidi")
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify({"success": True, "access_token": access_token, "refresh_token": refresh_token, "entity": ENTITY_NAME})

@app.route("/api/v1/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"success": True, "access_token": access_token})

@app.route("/api/v1/ask", methods=["POST"])
@jwt_required()
@limiter.limit("40 per minute")
def api_ask():
    try:
        data = request.get_json(force=True) or {}
        user_message = data.get("message", "").strip()
        ai_type = data.get("ai_type", "groq")
        session_id = data.get("session_id") or memory.get_session_id()

        if not user_message:
            return jsonify({"success": False, "error": "الرسالة فارغة"}), 400

        memory.save(session_id, "user", user_message)
        ai_reply, provider = get_ai_response(session_id, user_message, ai_type)
        memory.save(session_id, "assistant", ai_reply)
        save_master_info("آخر_نشاط", datetime.utcnow().isoformat())

        return jsonify({"success": True, "reply": ai_reply, "session_id": session_id, "provider": provider})
    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"success": False, "error": "خطأ داخلي"}), 500

@app.route("/api/v1/upload", methods=["POST"])
@jwt_required()
@limiter.limit("12 per minute")
def api_upload():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "لم يتم إرسال أي ملف"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "اسم الملف فارغ"}), 400

        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in config.ALLOWED_EXTENSIONS:
            return jsonify({"success": False, "error": f"نوع الملف .{file_ext} غير مدعوم", "allowed": sorted(list(config.ALLOWED_EXTENSIONS))}), 400

        session_id = memory.get_session_id()
        original_filename = file.filename
        secure_name = secure_filename(original_filename)
        file_path = config.UPLOAD_FOLDER / secure_name
        file.save(file_path)

        analysis = analyze_file(str(file_path), original_filename)
        if not analysis.get("success"):
            file_path.unlink(missing_ok=True)
            return jsonify({"success": False, "error": analysis.get("error", "فشل التحليل")}), 422

        extracted_text = analysis.get("text", "")[:9500]
        file_type = analysis.get("type", file_ext)

        image_description = ""
        if file_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            try:
                img_result = analyze_image_with_gemini(str(file_path), os.environ.get("GEMINI_API_KEY"))
                if img_result and img_result.get("success"):
                    image_description = img_result["description"]
                    extracted_text += f"\n\n[تحليل الصورة]:\n{image_description}"
            except Exception as img_e:
                logger.warning(f"فشل تحليل الصورة: {img_e}")

        save_uploaded_file(secure_name, original_filename, file_type, file_path.stat().st_size, extracted_text, image_description)
        memory.save(session_id, "user", f"[رفع ملف: {original_filename}]")
        memory.save(session_id, "assistant", f"تم تحليل {original_filename}")

        reply = f"✅ **تم تحليل الملف بنجاح**\n\n📁 {original_filename}\n📏 {file_path.stat().st_size / 1024:.1f} KB\n📋 {file_type.upper()}\n\n{extracted_text[:1900]}"
        if len(extracted_text) > 1900:
            reply += "\n\n*(النص الكامل محفوظ في ذاكرتي)*"

        file_path.unlink(missing_ok=True)
        return jsonify({"success": True, "reply": reply, "session_id": session_id, "filename": original_filename})

    except RequestEntityTooLarge:
        return jsonify({"success": False, "error": "الملف كبير جداً (50MB حد أقصى)"}), 413
    except Exception as e:
        logger.error(traceback.format_exc())
        try:
            if 'file_path' in locals(): file_path.unlink(missing_ok=True)
        except: pass
        return jsonify({"success": False, "error": "حدث خطأ أثناء رفع الملف"}), 500


# ====================== Backward Compatibility (الواجهة الحالية) ======================
@app.route("/")
def home():
    return render_template("index.html", entity_name=ENTITY_NAME)

@app.route("/ask", methods=["POST"])
def ask():
    """مسار متوافق مع الواجهة القديمة (بدون JWT إجباري)"""
    try:
        data = request.get_json(force=True) or {}
        user_message = data.get("message", "").strip()
        ai_type = data.get("ai_type", "groq")
        session_id = data.get("session_id") or memory.get_session_id()

        if not user_message:
            return jsonify({"reply": "أسمعك يا سيدي، تفضل.", "session_id": session_id})

        memory.save(session_id, "user", user_message)
        ai_reply, provider = get_ai_response(session_id, user_message, ai_type)
        memory.save(session_id, "assistant", ai_reply)
        save_master_info("آخر_نشاط", datetime.utcnow().isoformat())

        return jsonify({"reply": ai_reply, "session_id": session_id, "provider": provider})
    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"reply": "⚠️ حدث خطأ داخلي. حاول مرة أخرى.", "session_id": None})

@app.route("/upload", methods=["POST"])
def upload():
    """مسار رفع الملفات للواجهة القديمة"""
    try:
        if 'file' not in request.files:
            return jsonify({"reply": "لم يتم إرسال أي ملف."})

        file = request.files['file']
        if file.filename == '':
            return jsonify({"reply": "الملف فارغ."})

        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in config.ALLOWED_EXTENSIONS:
            return jsonify({"reply": f"نوع الملف .{file_ext} غير مدعوم."})

        session_id = request.form.get('session_id') or memory.get_session_id()
        secure_name = secure_filename(file.filename)
        file_path = config.UPLOAD_FOLDER / secure_name
        file.save(file_path)

        analysis = analyze_file(str(file_path), file.filename)
        if not analysis.get("success"):
            file_path.unlink(missing_ok=True)
            return jsonify({"reply": f"فشل التحليل: {analysis.get('error')}"})

        extracted_text = analysis.get("text", "")[:9500]
        file_type = analysis.get("type", file_ext)

        if file_ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
            try:
                img_result = analyze_image_with_gemini(str(file_path), os.environ.get("GEMINI_API_KEY"))
                if img_result and img_result.get("success"):
                    extracted_text += f"\n\n[تحليل الصورة]:\n{img_result['description']}"
            except: pass

        save_uploaded_file(secure_name, file.filename, file_type, file_path.stat().st_size, extracted_text)
        memory.save(session_id, "user", f"[رفع ملف: {file.filename}]")
        memory.save(session_id, "assistant", f"تم تحليل {file.filename}")

        reply = f"✅ تم تحليل الملف.\n📁 {file.filename}\n📝 {file_type}\n\n{extracted_text[:1800]}"
        if len(extracted_text) > 1800:
            reply += "\n\n(النص الكامل محفوظ في ذاكرتي)"

        file_path.unlink(missing_ok=True)
        return jsonify({"reply": reply, "session_id": session_id})
    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({"reply": "حدث خطأ أثناء رفع الملف."})

@app.route("/clear", methods=["POST"])
def clear():
    data = request.get_json(force=True) or {}
    sid = data.get("session_id")
    if sid:
        memory.clear(sid)
    return jsonify({"status": "success"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "name": ENTITY_NAME,
        "groq": bool(os.environ.get("GROQ_API_KEY")),
        "gemini": bool(os.environ.get("GEMINI_API_KEY")),
        "gateway": bool(os.environ.get("GATEWAY_URL")),
        "jwt": True,
        "limiter": True
    })


# ====================== تشغيل التطبيق ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
