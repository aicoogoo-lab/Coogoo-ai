"""
SkyOS Backend — Holographic OS v10 (Ultimate Production Ready)
By Driving & Copilot — 2026

- الإصدار v10.0 المصحح بالكامل والمنسجم مع نواة الذاكرة ومحرك الرؤية وسماء
- مدمج به محرك WhiteNoise لتقديم الملفات الستاتيكية والـ CSS فوراً على خوادم الإنتاج
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
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_from_directory,
)

from whitenoise import WhiteNoise  # محرك الإنتاج الفائق لملفات الـ CSS والـ JS

try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

from werkzeug.utils import secure_filename

# ============================
# إعداد مسار core
# ============================

CORE_PATH = os.path.join(os.path.dirname(__file__), "core")
if os.path.exists(CORE_PATH):
    sys.path.insert(0, CORE_PATH)
else:
    os.makedirs(CORE_PATH, exist_ok=True)
    sys.path.insert(0, CORE_PATH)

init_file = os.path.join(CORE_PATH, "__init__.py")
if not os.path.exists(init_file):
    Path(init_file).touch()

# ============================
# استيراد آمن ومباشر لوحدات النواة
# ============================

try:
    import sky_core
    import memory
    import sky_analyzer
except ImportError:
    try:
        from core import sky_core, memory, sky_analyzer
    except Exception as e:
        logging.error(f"❌ فشل فادح في تحميل تروس النواة الأساسية: {e}")
        sky_core = None
        memory = None
        sky_analyzer = None

# ============================
# إعداد التطبيق وتفعيل WhiteNoise
# ============================

app = Flask(__name__, template_folder="templates", static_folder="static")

# ربط وتكوين WhiteNoise لتقديم الملفات الثابتة وتفادي انهيار الـ CSS
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/", prefix="static/")

if HAS_CORS:
    CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = os.environ.get("SECRET_KEY", "sky-enterprise-secret-2026")
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB آمنة
UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=4)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("SkyOS")

# ============================
# تقديم الحزم الأساسية يدويًا
# ============================

@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory(app.static_folder, "manifest.json")

@app.route("/service-worker.js")
def serve_sw():
    if os.path.exists(os.path.join(app.static_folder, "service-worker.js")):
        return send_from_directory(app.static_folder, "service-worker.js")
    return send_from_directory(".", "service-worker.js")

# ============================
# Caching Layer (محمي ومحدد للأصول الثابتة)
# ============================

class SimpleCache:
    def __init__(self, ttl_seconds=1800):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = (value, datetime.now())

    def clear(self):
        self.cache.clear()

cache = SimpleCache(ttl_seconds=1800)

def cached(ttl=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if ttl:
                cache.ttl = ttl
            key_raw = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            key = hashlib.md5(key_raw.encode()).hexdigest()
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result)
            return result
        return wrapper
    return decorator

# ============================
# دوال آمنة ومصححة للتواصل مع النواة
# ============================

def safe_get_system_prompt(user_message="", session_id="", extra_context=""):
    try:
        if sky_core and hasattr(sky_core, "get_enhanced_system_prompt"):
            return sky_core.get_enhanced_system_prompt(user_message, session_id, extra_context)
    except Exception as e:
        logger.error(f"خطأ في بناء سياق النواة: {e}")
    return "أنتِ سماء، نظام ذكي واعٍ ومخلص."

def safe_add_to_history(role, content, session_id):
    try:
        if sky_core and hasattr(sky_core, "add_to_history"):
            sky_core.add_to_history(role, content, session_id)
            return True
    except Exception as e:
        logger.warning(f"خطأ في تسجيل تاريخ المحادثة: {e}")
    return False

def safe_init_db():
    try:
        if memory and hasattr(memory, "init_db"):
            memory.init_db()
    except Exception as e:
        logger.warning(f"خطأ في تهيئة DB: {e}")

def safe_get_conversation_context(session_id, limit=30):
    try:
        if memory and hasattr(memory, "get_full_conversation_context"):
            return memory.get_full_conversation_context(session_id, limit)
    except Exception as e:
        logger.warning(f"خطأ في جلب السياق: {e}")
    return []

def safe_analyze_url(url):
    try:
        if sky_analyzer and hasattr(sky_analyzer, "analyze_url"):
            return sky_analyzer.analyze_url(url)
    except Exception as e:
        logger.warning(f"خطأ في تحليل الرابط: {e}")
    return {"success": False, "error": "المحلل غير متاح حالياً"}

# تهيئة أولية آمنة لقاعدة البيانات عند الاستدعاء
safe_init_db()

# ============================
# AI Providers Multi-Engine
# ============================

def call_provider(messages, provider="groq"):
    import requests
    try:
        # 1) GROQ ENGINE
        if provider == "groq":
            key = os.environ.get("GROQ_API_KEY")
            if not key: return None
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 2500,
                },
                timeout=30,
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()

        # 2) GEMINI ENGINE
        if provider == "gemini":
            key = os.environ.get("GEMINI_API_KEY")
            if not key: return None
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            prompt_text = ""
            for m in messages:
                role_label = "سماء" if m['role'] == 'system' or m['role'] == 'assistant' else "سيدي"
                prompt_text += f"{role_label}: {m['content']}\n"
            
            response = requests.post(url, json={"contents": [{"parts": [{"text": prompt_text}]}]}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        # 3) OPENAI ENGINE
        if provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key: return None
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "gpt-4o-mini", "messages": messages, "temperature": 0.3},
                timeout=30,
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.warning(f"فشل تواصل محرك الذكاء [{provider}]: {e}")
    return None

# ============================
# تحليل الروابط الذكي (الخلفي والمتزامن)
# ============================

def _background_url_analysis(url, session_id=None):
    try:
        result = safe_analyze_url(url)
        if result.get("success") and session_id:
            logger.info(f"✅ تم انتهاء تحليل الرابط الخلفي بنجاح: {url}")
    except Exception as e:
        logger.error(f"خطأ كشط خلفي للرابط: {e}")

def _quick_url_context(user_message, session_id=None):
    urls = re.findall(r"https?://[^\s]+", user_message)
    if not urls:
        return "", []

    extra_context = ""
    background_urls = []

    if len(urls) == 1 and len(user_message) < 300:
        url = urls[0]
        cached_result = cache.get(f"url:{url}")
        if cached_result:
            extra_context += cached_result
        else:
            try:
                result = safe_analyze_url(url)
                if result.get("success"):
                    ctx = f"\n🔗 محتوى الرابط المحلل [{result.get('title')}]:\n{result.get('text')[:2000]}\n---\n"
                    extra_context += ctx
                    cache.set(f"url:{url}", ctx)
                else:
                    background_urls.append(url)
            except Exception:
                background_urls.append(url)
    else:
        background_urls = urls

    for url in background_urls[:2]:
        executor.submit(_background_url_analysis, url, session_id)

    if background_urls:
        extra_context += "\n[ملاحظة للنظام: يتم كشط بعض الروابط الإضافية في الخلفية وتغذية الذاكرة بها حالياً].\n"

    return extra_context, urls

# ============================
# 3) AI Router & Core Pipeline
# ============================

def generate_ai_response(session_id, user_message, ai_type="groq", ui_mode="holo"):
    extra_context, urls = _quick_url_context(user_message, session_id)
    extra_context += f"\n[واجهة العرض الحالية]: {ui_mode}\n"

    system_prompt = safe_get_system_prompt(
        user_message=user_message,
        session_id=session_id,
        extra_context=extra_context
    )

    if isinstance(system_prompt, str) and system_prompt.startswith("REFUSE:"):
        return system_prompt.replace("REFUSE:", "").strip(), "safety"

    messages = [{"role": "system", "content": system_prompt}]
    
    history = safe_get_conversation_context(session_id, 20)
    for h in history:
        messages.append({
            "role": "user" if h.get("role") == "user" else "assistant",
            "content": h.get("content", "")
        })
        
    messages.append({"role": "user", "content": user_message})

    providers_chain = [ai_type, "groq", "gemini", "openai"]
    used_providers = []
    
    for prov in providers_chain:
        if prov and prov not in used_providers:
            used_providers.append(prov)
            reply = call_provider(messages, prov)
            if reply:
                safe_add_to_history("user", user_message, session_id)
                safe_add_to_history("assistant", reply, session_id)
                return reply, prov

    return "⚠️ تعذر الاتصال بجميع بوابات ومزودي الذكاء الاصطناعي حالياً. يرجى التحقق من مفاتيح API الخاصة بك.", "offline"

# ============================
# 4) Holographic OS Routes (أبواب الواجهات)
# ============================

@app.route("/")
def home():
    ui_mode = request.args.get("mode", "holo")
    try:
        return render_template("index.html", ui_mode=ui_mode)
    except Exception:
        if os.path.exists(os.path.join(app.static_folder, "index.html")):
            return send_from_directory(app.static_folder, "index.html")
        return jsonify({"error": "ملف واجهة الرادار index.html غير موجود كلياً"}), 500

@app.route("/os/desktop")
def os_desktop():
    ui_mode = request.args.get("mode", "holo")
    try:
        return render_template("desktop.html", ui_mode=ui_mode)
    except Exception:
        return send_from_directory(app.static_folder, "desktop.html")

# ============================
# 5) API Endpoints & Chat Controller
# ============================

@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.json or {}
        user_message = data.get("message", "").strip()
        session_id = data.get("session_id", "default_sky_session")
        ai_type = data.get("provider", "groq")
        ui_mode = data.get("ui_mode", "holo")

        if not user_message:
            return jsonify({"status": "error", "reply": "لا يمكن معالجة رسالة فارغة."}), 400

        reply, current_provider = generate_ai_response(session_id, user_message, ai_type, ui_mode)

        return jsonify({
            "status": "success",
            "reply": reply,
            "provider": current_provider,
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        logger.error(f"خطأ في بوابة استقبال المحادثات: {e}")
        return jsonify({"status": "error", "reply": f"حدث خطأ غير متوقع في النواة: {str(e)}"}), 500

@app.route("/scrape", methods=["POST"])
def scrape_website():
    try:
        data = request.json or {}
        url = data.get("url", "").strip()
        if not url:
            return jsonify({"success": False, "error": "الرابط مطلوب"}), 400

        result = safe_analyze_url(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
