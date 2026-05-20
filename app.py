# SkyOS Backend — HyperOS v7.1 (Production + Render Ready)
# By Driving & Copilot — 2026

"""
المميزات الأساسية في v7.1:
- دمج كامل v6.1 (روابط خلفية + Caching + Safe Core + Video + Scraping)
- إصلاح full_text → text فقط
- إنشاء __init__.py تلقائيًا داخل core
- إضافة render_ready في /status
- تحسين إدارة الأخطاء (Fail-Safe لكل المسارات)
- تحسين الأداء لـ Render (تقليل البلوك + استخدام Threads للمهام الثقيلة)
- طبقة Caching ذكية للروابط والردود
- تحليل الروابط: متزامن إذا كان سريع، وخلفية إذا كان ثقيل
- دعم: نص + ملفات + صور + فيديو + صوت + صفحات كاملة
- دعم تعدد المزودين (Groq / Gemini / OpenAI) مع Fallback
- ذاكرة متقدمة + شخصية ديناميكية + RLHF
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

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# ============================
# إضافة مجلد core إلى مسار Python (مع حماية)
# ============================
CORE_PATH = os.path.join(os.path.dirname(__file__), "core")
if os.path.exists(CORE_PATH):
    sys.path.insert(0, CORE_PATH)
else:
    logging.warning("⚠️ مجلد core غير موجود! سيتم إنشاؤه تلقائياً.")
    os.makedirs(CORE_PATH, exist_ok=True)
    sys.path.insert(0, CORE_PATH)

# إنشاء __init__.py تلقائيًا
init_file = os.path.join(CORE_PATH, "__init__.py")
if not os.path.exists(init_file):
    Path(init_file).touch()
    logging.info("✅ تم إنشاء __init__.py في مجلد core")

# ============================
# حماية استيراد core modules
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

UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=4)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("SkyOS")

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
# دوال آمنة للـ Core
# ============================

def safe_get_system_prompt(user_message="", session_id="", extra_context=""):
    if sky_core and hasattr(sky_core, "get_enhanced_system_prompt"):
        try:
            return sky_core.get_enhanced_system_prompt(
                user_message, session_id, extra_context
            )
        except Exception as e:
            logger.error(f"خطأ في system prompt: {e}")
    return f"أنت مساعد ذكي ومفيد. المستخدم قال: {user_message[:200]}"

def safe_add_to_history(role, content, session_id):
    if sky_core and hasattr(sky_core, "add_to_history"):
        try:
            return sky_core.add_to_history(role, content, session_id)
        except Exception as e:
            logger.warning(f"خطأ في حفظ التاريخ: {e}")

def safe_init_db():
    if memory and hasattr(memory, "init_db"):
        try:
            return memory.init_db()
        except Exception as e:
            logger.warning(f"خطأ في تهيئة DB: {e}")

def safe_get_conversation_context(session_id, limit=45):
    if memory and hasattr(memory, "get_full_conversation_context"):
        try:
            return memory.get_full_conversation_context(session_id, limit)
        except Exception as e:
            logger.warning(f"خطأ في جلب السياق: {e}")
    return []

def safe_analyze_url(url):
    if sky_analyzer and hasattr(sky_analyzer, "analyze_url"):
        try:
            return sky_analyzer.analyze_url(url)
        except Exception as e:
            logger.warning(f"خطأ في تحليل الرابط: {e}")
    return {"success": False, "error": "Analyzer غير متاح"}

def safe_analyze_file(file_path, filename):
    if sky_analyzer and hasattr(sky_analyzer, "analyze_file"):
        try:
            return sky_analyzer.analyze_file(file_path, filename)
        except Exception as e:
            logger.warning(f"خطأ في تحليل الملف: {e}")
    return {"success": False, "error": "Analyzer غير متاح"}

def safe_analyze_image(image_path, api_key):
    if sky_analyzer and hasattr(sky_analyzer, "analyze_image_with_gemini"):
        try:
            return sky_analyzer.analyze_image_with_gemini(image_path, api_key)
        except Exception as e:
            logger.warning(f"خطأ في تحليل الصورة: {e}")
    return {"success": False, "error": "Analyzer غير متاح"}

safe_init_db()
logger.info("✅ SkyOS v7.1 جاهز")

# ============================
# 1) AI Providers
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
                    "model": os.environ.get(
                        "GROQ_MODEL", "llama-3.3-70b-versatile"
                    ),
                    "messages": messages,
                    "temperature": 0.25,
                    "max_tokens": 2400,
                },
                timeout=55,
            )
            return r.json()["choices"][0]["message"]["content"].strip()

"][0]["message"]["content"].strip()

        if provider == "gemini":
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                return None
            url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                "gemini-1.5-flash:generateContent?key=" + key
            )
            prompt = "\n\n".join(
                [f"{m['role']}: {m['content']}" for m in messages]
            )
            r = requests.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=55,
            )
            return (
                r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            )

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
                timeout=55,
            )
            return r.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.warning(f"[Provider:{provider}] failed: {e}")
        return None

# ============================
# 2) تحليل الروابط في الخلفية
# ============================

def _background_url_analysis(url, session_id=None):
    try:
        result = safe_analyze_url(url)
        if not result.get("success"):
            return

        title = result.get("title", url)
        full_text = result.get("text", "")

        if memory and hasattr(memory, "save_url_analysis"):
            try:
                memory.save_url_analysis(url, title, full_text)
            except:
                pass

        if memory and hasattr(memory, "save_knowledge"):
            try:
                memory.save_knowledge(
                    f"رابط: {title}", full_text[:1800], source=url
                )
            except:
                pass

        if session_id:
            safe_add_to_history(
                "assistant",
                f"[معلومة مضافة من تحليل رابط سابق]: {title}",
                session_id,
            )

    except Exception as e:
        logger.error(f"[BG-URL] خطأ: {e}")

def _quick_url_context(user_message, session_id=None):
    urls = re.findall(r"https?://[^\s]+", user_message)
    if not urls:
        return "", []

    extra_context = ""
    background_urls = []

    if len(urls) == 1 and len(user_message) < 400:
        url = urls[0]
        cached_result = cache.get(f"url:{url}")
        if cached_result:
            extra_context += cached_result
        else:
            try:
                result = safe_analyze_url(url)
                if result.get("success"):
                    title = result.get("title", url)
                    full_text = result.get("text", "")
                    ctx = f"\n🔗 {title}\n{full_text[:2000]}\n---\n"
                    extra_context += ctx
                    cache.set(f"url:{url}", ctx)
                else:
                    background_urls.append(url)
            except:
                background_urls.append(url)
    else:
        background_urls = urls

    for url in background_urls[:3]:
        thread = threading.Thread(
            target=_background_url_analysis, args=(url, session_id)
        )
        thread.daemon = True
        thread.start()

    if background_urls:
        extra_context += (
            "\n[ملاحظة]: يتم الآن تحليل بعض الروابط في الخلفية.\n"
        )

    return extra_context, urls

# ============================
# 3) AI Router
# ============================

@cached(ttl=1800)
def generate_ai_response(session_id, user_message, ai_type="groq"):
    extra_context, urls = _quick_url_context(user_message, session_id)

    system_prompt = safe_get_system_prompt(
        user_message=user_message,
        session_id=session_id,
        extra_context=extra_context,
    )

    if isinstance(system_prompt, str) and system_prompt.startswith("REFUSE:"):
        return system_prompt.replace("REFUSE:", "").strip(), "safety"

    messages = [{"role": "system", "content": system_prompt}]

    history = safe_get_conversation_context(session_id, 45)
    for h in history[-38:]:
        messages.append(
            {
                "role": "user" if h.get("role") == "user" else "assistant",
                "content": h.get("content", ""),
            }
        )

    messages.append({"role": "user", "content": user_message})

    providers = []
    for p in [ai_type, "groq", "gemini", "openai"]:
        if p not in providers:
            providers.append(p)

    for prov in providers:
        reply = call_provider(messages, prov)
        if reply:
            return reply, prov

    return "⚠️ جميع مزودي الذكاء غير متاحين حالياً.", "offline"

# ============================
# 4) Scraping
# ============================

@app.route("/scrape", methods=["POST"])
def scrape_website():
    try:
        data = request.get_json(force=True) or {}
        url = data.get("url", "").strip()
        session_id = data.get("session_id") or str(uuid.uuid4())

        if not url:
            return jsonify({"reply": "الرجاء إرسال رابط صحيح"})

        import requests
        from bs4 import BeautifulSoup

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        title = soup.find("title")
        title_text = title.get_text().strip() if title else "بدون عنوان"

        main_content = (
            soup.find("main") or soup.find("article") or soup.find("body")
        )
        text = (
            main_content.get_text(separator="\n", strip=True)
            if main_content
            else ""
        )
        text = re.sub(r"\n+", "\n", text)[:8000]

        if memory and hasattr(memory, "save_knowledge"):
            try:
                memory.save_knowledge(
                    f"تحليل صفحة: {title_text}", text[:1800], source=url
                )
            except:
                pass

        safe_add_to_history("user", f"[تحليل صفحة: {url}]", session_id)

        reply = f"📄 **{title_text}**\n\n{text[:3000]}"
        if len(text) > 3000:
            reply += "\n\n... (تم اختصار المحتوى)"

        safe_add_to_history("assistant", reply[:2000], session_id)

        return jsonify(
            {"reply": reply, "title": title_text, "session_id": session_id}
        )

    except Exception as e:
        logger.error(f"خطأ في /scrape: {e}")
        return jsonify({"reply": f"فشل تحليل الصفحة: {str(e)}"}), 500

# ============================
# 5) Video
# ============================

@app.route("/upload-video", methods=["POST"])
def upload_video():
    try:
        if "video" not in request.files:
            return jsonify({"reply": "لم يتم إرسال أي فيديو"})

        video = request.files["video"]
        session_id = request.form.get("session_id") or str(uuid.uuid4())

        if not video.filename:
            return jsonify({"reply": "الملف غير صالح"})

        filename = secure_filename(video.filename)
        video_path = UPLOAD_FOLDER / filename
        video.save(video_path)

        reply_parts = []

        try:
            import cv2

            cap = cv2.VideoCapture(str(video_path))
            ret, frame = cap.read()
            if ret:
                thumb_path = UPLOAD_FOLDER / f"thumb_{uuid.uuid4()}.jpg"
                cv2.imwrite(str(thumb_path), frame)
                cap.release()

                vision_result = safe_analyze_image(
                    str(thumb_path), os.environ.get("GEMINI_API_KEY")
                )
                if vision_result and vision_result.get("success"):
                    reply_parts.append(
                        f"🖼️ **وصف الصورة الأولى**:\n{vision_result['description'][:500]}"
                    )

                thumb_path.unlink(missing_ok=True)
            else:
                cap.release()
        except Exception as e:
            logger.warning(f"تحليل الفيديو فشل: {e}")
            reply_parts.append("⚠️ لم أتمكن من تحليل لقطات الفيديو")

        file_size_mb = video_path.stat().st_size / (1024 * 1024)
        reply_parts.append(f"📹 **ملف الفيديو**: {filename}")
        reply_parts.append(f"📦 **الحجم**: {file_size_mb:.2f} MB")

        if memory and hasattr(memory, "save_uploaded_file"):
            try:
                memory.save_uploaded_file(
                    str(uuid.uuid4()),
                    filename,
                    "video",
                    video_path.stat().st_size,
                    "\n".join(reply_parts),
                )
            except:
                pass

        safe_add_to_history("user", f"[رفع فيديو: {filename}]", session_id)

        final_reply = "\n\n".join(reply_parts)
        safe_add_to_history("assistant", final_reply[:2000], session_id)

        video_path.unlink(missing_ok=True)

        return jsonify({"reply": final_reply, "session_id": session_id})

    except RequestEntityTooLarge:
        return jsonify({"reply": "الفيديو كبير جداً (الحد الأقصى 200 ميجا)"})
    except Exception as e:
        logger.error(f"خطأ في /upload-video: {e}")
        return jsonify({"reply": f"حدث خطأ: {str(e)}"}), 500

# ============================
# 6) المسارات الأساسية
# ============================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = None
    try:
        data = request.get_json(force=True) or {}
        message = (data.get("message") or "").strip()
        ai_type = (data.get("ai_type") or "groq").lower()
        session_id = data.get("session_id") or str(uuid.uuid4())

        if not message:
            return jsonify(
                {"reply": "أسمعك يا سيدي.", "
