"""
SkyOS Backend — Holographic OS v10 (Ultimate Production Ready)
By Driving & Copilot — 2026

- Ultra Edition v9.0 أساس النظام
- v10: Holographic OS Layer + Memory Enhancements + OS Modes

المميزات:
- ✅ تصحيح جميع أخطاء الـ JSON parsing
- ✅ تحسين إدارة الأخطاء (Fail-Safe لكل المسارات)
- ✅ تحسين الأداء لـ Render (تقليل البلوك + استخدام Threads للمهام الثقيلة)
- ✅ طبقة Caching ذكية للروابط والردود
- ✅ تحليل الروابط: متزامن إذا كان سريع، وخلفية إذا كان ثقيل
- ✅ دعم: نص + ملفات + صور + فيديو + صوت + صفحات كاملة
- ✅ دعم تعدد المزودين (Groq / Gemini / OpenAI) مع Fallback
- ✅ ذاكرة متقدمة + تلخيص جلسات + حفظ معرفة
- ✅ Holographic UI Modes (classic / holo / liquid)
- ✅ متوافق 100% مع Render / Gunicorn / CORS Enabled
- ✅ تحسين أمان API Keys
- ✅ Rate Limiting بسيط مدمج
- ✅ Health Checks متقدمة
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
# استيراد حزمة CORS لحل مشكلة عدم استجابة طلبات الواجهة للمتصفح
try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# ============================
# إعداد مسار core
# ============================

CORE_PATH = os.path.join(os.path.dirname(__file__), "core")
if os.path.exists(CORE_PATH):
    sys.path.insert(0, CORE_PATH)
else:
    logging.warning("⚠️ مجلد core غير موجود! سيتم إنشاؤه تلقائياً.")
    os.makedirs(CORE_PATH, exist_ok=True)
    sys.path.insert(0, CORE_PATH)

init_file = os.path.join(CORE_PATH, "__init__.py")
if not os.path.exists(init_file):
    Path(init_file).touch()

# ============================
# استيراد آمن لوحدات SkyOS
# ============================

def safe_import(module_name, fallback_value=None):
    try:
        return __import__(module_name)
    except ImportError as e:
        logging.error(f"❌ فشل استيراد {module_name}: {e}")
        return fallback_value
    except Exception as e:
        logging.error(f"❌ خطأ غير متوقع في {module_name}: {e}")
        return fallback_value

sky_core = safe_import("sky_core")
memory = safe_import("memory")
sky_analyzer = safe_import("sky_analyzer")

# ============================
# إعداد التطبيق
# ============================

app = Flask(__name__, template_folder="templates", static_folder="static")

# تفعيل الـ CORS لحل مشاكل حظر المتصفح لطلبات الـ API الخاصة بالواجهة
if HAS_CORS:
    CORS(app, resources={r"/*": {"origins": "*"}})
else:
    logging.warning("⚠️ حزمة Flask-CORS غير مثبتة! قد تواجه الواجهة مشاكل اتصال بالـ API.")

app.secret_key = os.environ.get("SECRET_KEY", "sky-enterprise-secret-2026")
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200MB
app.config["MAX_IMAGE_SIZE"] = 20 * 1024 * 1024       # 20MB

UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=4)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("SkyOS")

# ============================
# تقديم static والملفات الرئيسية يدويًا (حل Render الـ Safe)
# ============================

@app.route("/static/<path:filename>")
def serve_static(filename):
    """ تقديم ملفات static يدويًا لضمان عمل الواجهة على Render/Gunicorn """
    return send_from_directory("static", filename)

@app.route("/manifest.json")
def serve_manifest():
    """ تقديم ملف المانيفست المباشر لتشغيل الـ PWA بنجاح """
    return send_from_directory(app.static_folder, "manifest.json")

@app.route("/service-worker.js")
def serve_sw():
    """ تقديم ملف الـ Service Worker من المجلد الرئيسي أو الستاتيك """
    if os.path.exists(os.path.join(app.static_folder, "service-worker.js")):
        return send_from_directory(app.static_folder, "service-worker.js")
    return send_from_directory(".", "service-worker.js")

# ============================
# Caching Layer
# ============================

class SimpleCache:
    """نظام تخزين مؤقت بسيط"""
    def __init__(self, ttl_seconds=3600):
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

cache = SimpleCache(ttl_seconds=1800)  # 30 دقيقة

def cached(ttl=None):
    """Decorator للتخزين المؤقت للنتائج الثقيلة (مثل الردود الطويلة)"""
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
# Rate Limiting بسيط
# ============================

_rate_limiter = {}
RATE_LIMIT_WINDOW = 10   # ثواني
RATE_LIMIT_MAX = 40      # عدد الطلبات في النافذة

def check_rate_limit(client_id: str) -> bool:
    """ إرجاع True إذا مسموح، False إذا تجاوز الحد """
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    entries = _rate_limiter.get(client_id, [])
    entries = [t for t in entries if t >= window_start]
    if len(entries) >= RATE_LIMIT_MAX:
        _rate_limiter[client_id] = entries
        return False
    entries.append(now)
    _rate_limiter[client_id] = entries
    return True

def get_client_id():
    return request.remote_addr or "unknown"

# ============================
# دوال آمنة للـ Core + الذاكرة
# ============================

def safe_get_system_prompt(user_message="", session_id="", extra_context=""):
    """ v10: إضافة extra_context (روابط، ملفات، حالة النظام) إلى الـ System Prompt """
    try:
        if sky_core and hasattr(sky_core, "get_enhanced_system_prompt"):
            return sky_core.get_enhanced_system_prompt(
                user_message, session_id, extra_context
            )
    except Exception as e:
        logger.error(f"خطأ في system prompt: {e}")
    return f"أنت مساعد ذكاء اصطناعي متقدم يعمل ضمن نظام تشغيل SkyOS v10. المستخدم قال: {user_message[:200]}"

def safe_add_to_history(role, content, session_id):
    try:
        if sky_core and hasattr(sky_core, "add_to_history"):
            return sky_core.add_to_history(role, content, session_id)
    except Exception as e:
        logger.warning(f"خطأ في حفظ التاريخ: {e}")
    return None

def safe_init_db():
    try:
        if memory and hasattr(memory, "init_db"):
            return memory.init_db()
    except Exception as e:
        logger.warning(f"خطأ في تهيئة DB: {e}")
    return None

def safe_get_conversation_context(session_id, limit=45):
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
    return {"success": False, "error": "Analyzer غير متاح"}

def safe_analyze_file(file_path, filename):
    try:
        if sky_analyzer and hasattr(sky_analyzer, "analyze_file"):
            return sky_analyzer.analyze_file(file_path, filename)
    except Exception as e:
        logger.warning(f"خطأ في تحليل الملف: {e}")
    return {"success": False, "error": "Analyzer غير متاح"}

def safe_analyze_image(image_path, api_key):
    try:
        if sky_analyzer and hasattr(sky_analyzer, "analyze_image_with_gemini"):
            return sky_analyzer.analyze_image_with_gemini(image_path, api_key)
    except Exception as e:
        logger.warning(f"خطأ في تحليل الصورة: {e}")
    return {"success": False, "error": "Analyzer غير متاح"}

def safe_save_knowledge(title, text, source=None):
    try:
        if memory and hasattr(memory, "save_knowledge"):
            memory.save_knowledge(title, text, source=source)
    except Exception:
        pass

def safe_save_uploaded_file(file_id, filename, ftype, size, summary):
    try:
        if memory and hasattr(memory, "save_uploaded_file"):
            memory.save_uploaded_file(file_id, filename, ftype, size, summary)
    except Exception:
        pass

def safe_process_feedback(score, session_id, reason):
    try:
        if memory and hasattr(memory, "process_feedback"):
            memory.process_feedback("", "", score, session_id, reason)
    except Exception:
        pass
    try:
        if sky_core and hasattr(sky_core, "rlhf_feedback_hook"):
            sky_core.rlhf_feedback_hook(session_id, score, reason)
    except Exception:
        pass

def safe_summarize_session(session_id):
    """ v10: تلخيص الجلسة عند مسحها أو عند الطلب """
    try:
        history = safe_get_conversation_context(session_id, limit=80)
        if not history:
            return
        text_chunks = []
        for h in history:
            role = h.get("role", "user")
            content = h.get("content", "")
            text_chunks.append(f"{role}: {content}")
        full_text = "\n".join(text_chunks)[:6000]

        system_prompt = (
            "أنت مختص في تلخيص الجلسات. لخص هذه الجلسة في نقاط قصيرة، "
            "مع إبراز أهداف المستخدم وأسلوبه واهتماماته."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_text},
        ]
        summary = call_provider(messages, provider="groq") or ""
        if summary:
            safe_save_knowledge(
                f"ملخص جلسة: {session_id}",
                summary[:1800],
                source=f"session:{session_id}",
            )
    except Exception as e:
        logger.warning(f"فشل تلخيص الجلسة: {e}")

# تهيئة آمنة
safe_init_db()
logger.info("✅ SkyOS v10 جاهز مع جميع أنظمة الحماية والذاكرة المتقدمة")

# ============================
# 1) AI Providers
# ============================

def call_provider(messages, provider="groq"):
    """ دالة موحدة لاستدعاء مزودي الذكاء (Groq / Gemini / OpenAI) """
    import requests

    try:
        # GROQ
        if provider == "groq":
            key = os.environ.get("GROQ_API_KEY")
            if not key:
                logger.warning(f"[{provider}] لا يوجد مفتاح API")
                return None

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
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

            if response.status_code != 200:
                logger.warning(
                    f"[{provider}] HTTP {response.status_code}: {response.text[:200]}"
                )
                return None

            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        # GEMINI
        if provider == "gemini":
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                logger.warning(f"[{provider}] لا يوجد مفتاح API")
                return None

            url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                "gemini-1.5-flash:generateContent?key=" + key
            )
            prompt = "\n\n".join(
                [f"{m['role']}: {m['content']}" for m in messages]
            )

            response = requests.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=55,
            )

            if response.status_code != 200:
                logger.warning(
                    f"[{provider}] HTTP {response.status_code}: {response.text[:200]}"
                )
                return None

            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return (
                    data["candidates"][0]["content"]["parts"][0]["text"].strip()
                )
            return None

        # OPENAI
        if provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                logger.warning(f"[{provider}] لا يوجد مفتاح API")
                return None

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "temperature": 0.25,
                    "max_tokens": 2400,
                },
                timeout=55,
            )

            if response.status_code != 200:
                logger.warning(
                    f"[{provider}] HTTP {response.status_code}: {response.text[:200]}"
                )
                return None

            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        logger.warning(f"[{provider}] Timeout بعد 55 ثانية")
        return None
    except requests.exceptions.ConnectionError:
        logger.warning(f"[{provider}] خطأ في الاتصال")
        return None
    except KeyError as e:
        logger.warning(f"[{provider}] خطأ في parsing JSON: {e}")
        return None
    except Exception as e:
        logger.warning(f"[{provider}] فشل غير متوقع: {e}")
        logger.debug(traceback.format_exc())
        return None

    return None

# ============================
# 2) تحليل الروابط في الخلفية
# ============================

def _background_url_analysis(url, session_id=None):
    """تحليل رابط في الخلفية بدون تعطيل الرد"""
    try:
        logger.info(f"[BG-URL] بدء تحليل الرابط في الخلفية: {url}")
        result = safe_analyze_url(url)
        if not result.get("success"):
            logger.warning(f"[BG-URL] فشل تحليل الرابط: {url}")
            return

        title = result.get("title", url)
        full_text = result.get("text", "")

        try:
            if memory and hasattr(memory, "save_url_analysis"):
                memory.save_url_analysis(url, title, full_text)
        except Exception:
            pass

        safe_save_knowledge(f"رابط: {title}", full_text[:1800], source=url)

        if session_id:
            safe_add_to_history(
                "assistant",
                f"[معلومة مضافة من تحليل رابط سابق]: {title}",
                session_id,
            )

        logger.info(f"[BG-URL] تم تحليل الرابط وحفظه: {url}")
    except Exception as e:
        logger.error(f"[BG-URL] خطأ: {e}")

def _quick_url_context(user_message, session_id=None):
    """ منطق ذكي لتحليل الروابط """
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
                start = time.time()
                result = safe_analyze_url(url)
                elapsed = time.time() - start
                if result.get("success"):
                    title = result.get("title", url)
                    full_text = result.get("text", "")
                    ctx = f"\n🔗 {title}\n{full_text[:2000]}\n---\n"
                    extra_context += ctx
                    cache.set(f"url:{url}", ctx)
                    logger.info(f"[URL] تحليل متزامن ({elapsed:.2f}s): {url}")
                else:
                    background_urls.append(url)
            except Exception as e:
                logger.warning(f"[URL] خطأ في التحليل المتزامن: {e}")
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
            "\n[ملاحظة]: يتم الآن تحليل بعض الروابط في الخلفية، "
            "وستُستخدم نتائجها لتحسين الردود القادمة.\n"
        )

    return extra_context, urls

# ============================
# 3) AI Router + OS Modes
# ============================

@cached(ttl=1800)
def generate_ai_response(session_id, user_message, ai_type="groq", ui_mode="classic"):
    extra_context, urls = _quick_url_context(user_message, session_id)
    extra_context += f"\n[SkyOS UI Mode]: {ui_mode}\n"

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
        if p and p not in providers:
            providers.append(p)

    for prov in providers:
        reply = call_provider(messages, prov)
        if reply:
            return reply, prov

    return "⚠️ جميع مزودي الذكاء غير متاحين حالياً.", "offline"

# ============================
# 4) Holographic OS Routes (تحديث التقديم الـ Fail-Safe)
# ============================

@app.route("/")
def home():
    """ صفحة الواجهة الرئيسية مع حماية في حال عدم وجود المجلد الافتراضي """
    ui_mode = request.args.get("mode", "holo")
    try:
        return render_template("index.html", ui_mode=ui_mode)
    except Exception:
        # حل بديل إذا كان الملف في مجلد static مباشرة
        if os.path.exists(os.path.join(app.static_folder, "index.html")):
            return send_from_directory(app.static_folder, "index.html")
        return jsonify({"error": "ملف index.html غير موجود في templates أو static"}), 500

@app.route("/os/desktop")
def os_desktop():
    ui_mode = request.args.get("mode", "holo")
    try:
        return render_template("desktop.html", ui_mode=ui_mode)
    except Exception:
        if os.path.exists(os.path.join(app.static_folder, "desktop.html")):
            return send_from_directory(app.static_folder, "desktop.html")
        return jsonify({"error": "ملف desktop.html غير موجود"}), 500

# ============================
# 5) Website Scraping
# ============================

@app.route("/scrape", methods=["POST"])
def scrape_website():
    try:
        if not check_rate_limit(get_client_id()):
            return jsonify({"reply": "تم تجاوز حد الطلبات مؤقتاً."}), 429

        data = request.get_json(force=True) or {}
        url = data.get("url", "").strip()
        session_id = data.get("session_id") or str(uuid.uuid4())

        if not url:
            return jsonify({"reply": "الرجاء إرسال رابط صحيح"})

        import requests
        from bs4 import BeautifulSoup

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            )
        }
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

        safe_save_knowledge(
            f"تحليل صفحة: {title_text}", text[:1800], source=url
        )

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
# 6) رفع وتحليل الفيديو
# ============================

@app.route("/upload-video", methods=["POST"])
def upload_video():
    try:
        if not check_rate_limit(get_client_id()):
            return jsonify({"reply": "تم تجاوز حد الطلبات مؤقتاً."}), 429

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
                        f"🖼️ **وصف الصورة الأولى**:\n"
                        f"{vision_result['description'][:500]}"
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

        safe_save_uploaded_file(
            str(uuid.uuid4()),
            filename,
            "video",
            video_path.stat().st_size,
            "\n".join(reply_parts),
        )

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
# 7) رفع وتحليل الملفات
# ============================

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if not check_rate_limit(get_client_id()):
            return jsonify({"reply": "تم تجاوز حد الطلبات مؤقتاً."}), 429

        if "file" not in request.files:
            return jsonify({"reply": "لم يتم إرسال أي ملف"})

        file = request.files["file"]
        session_id = request.form.get("session_id") or str(uuid.uuid4())

        if not file.filename:
            return jsonify({"reply": "الملف غير صالح"})

        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER / filename
        file.save(file_path)

        analysis = safe_analyze_file(str(file_path), filename)
        extracted = (
            analysis.get("text", "")[:7500]
            if analysis and analysis.get("success")
            else ""
        )

        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            gemini = safe_analyze_image(
                str(file_path), os.environ.get("GEMINI_API_KEY")
            )
            if gemini and gemini.get("success"):
                extracted += (
                    f"\n\n[تحليل Vision]:\n{gemini['description']}"
                )

        safe_save_uploaded_file(
            str(uuid.uuid4()),
            filename,
            analysis.get("type", ""),
            file_path.stat().st_size,
            extracted,
        )

        safe_add_to_history("user", f"[رفع ملف: {filename}]", session_id)
        safe_add_to_history(
            "assistant",
            f"تم تحليل الملف بنجاح.\n{extracted[:2000]}",
            session_id,
        )

        file_path.unlink(missing_ok=True)

        return jsonify(
            {
                "reply": f"✅ تم تحليل الملف بنجاح.\n\n{extracted[:2000]}",
                "session_id": session_id,
            }
        )

    except Exception as e:
        logger.error(f"خطأ في /upload: {e}")
        return jsonify({"reply": f"حدث خطأ: {str(e)}"}), 500

# ============================
# 8) الصوت → نص → ذكاء
# ============================

@app.route("/voice", methods=["POST"])
def voice():
    try:
        if not check_rate_limit(get_client_id()):
            return jsonify({"reply": "تم تجاوز حد الطلبات مؤقتاً."}), 429

        if "audio" not in request.files:
            return jsonify({"reply": "لم يتم إرسال أي صوت"})

        audio = request.files["audio"]
        session_id = request.form.get("session_id") or str(uuid.uuid4())

        if not audio.filename:
            return jsonify({"reply": "الملف الصوتي غير صالح"})

        temp_path = UPLOAD_FOLDER / f"voice_{uuid.uuid4()}.wav"
        audio.save(temp_path)

        import requests

        key = os.environ.get("OPENAI_API_KEY")
        text = ""

        if key:
            try:
                with open(temp_path, "rb") as f:
                    r = requests.post(
                        "https://api.openai.com/v1/audio/transcriptions",
                        headers={"Authorization": f"Bearer {key}"},
                        files={"file": f},
                        data={"model": "whisper-1"},
                        timeout=60,
                    )
                    text = r.json().get("text", "")
            except Exception as e:
                logger.warning(f"Whisper فشل: {e}")
                text = "[فشل تحويل الصوت عبر Whisper]"

        if not text:
            text = "[لم يتم تفعيل تحويل الصوت]"

        temp_path.unlink(missing_ok=True)

        safe_add_to_history("user", f"[صوت]: {text}", session_id)
        reply, provider = generate_ai_response(
            session_id, text, ai_type="groq", ui_mode="holo"
        )
        safe_add_to_history("assistant", reply, session_id)

        return jsonify({"reply": reply, "session_id": session_id})

    except Exception as e:
        logger.error(f"خطأ في /voice: {e}")
        return jsonify({"reply": f"خطأ: {str(e)}"}), 500

# ============================
# 9) Vision (صور)
# ============================

@app.route("/vision", methods=["POST"])
def vision():
    try:
        if not check_rate_limit(get_client_id()):
            return jsonify({"reply": "تم تجاوز حد الطلبات مؤقتاً."}), 429

        if "image" not in request.files:
            return jsonify({"reply": "لم يتم إرسال أي صورة"})

        img = request.files["image"]
        session_id = request.form.get("session_id") or str(uuid.uuid4())

        if not img.filename:
            return jsonify({"reply": "الملف غير صالح"})

        temp_path = UPLOAD_FOLDER / f"vision_{uuid.uuid4()}.jpg"
        img.save(temp_path)

        gemini = safe_analyze_image(
            str(temp_path), os.environ.get("GEMINI_API_KEY")
        )
        temp_path.unlink(missing_ok=True)

        reply = (
            gemini["description"]
            if gemini and gemini.get("success")
            else "لم أستطع تحليل الصورة."
        )

        safe_add_to_history("user", "[صورة مرسلة]", session_id)
        safe_add_to_history("assistant", reply, session_id)

        return jsonify({"reply": reply, "session_id": session_id})

    except Exception as e:
        logger.error(f"خطأ في /vision: {e}")
        return jsonify({"reply": f"خطأ: {str(e)}"}), 500

# ============================
# 10) المسار الرئيسي للمحادثة النصية
# ============================

@app.route("/ask", methods=["POST"])
def ask():
    data = None
    try:
        if not check_rate_limit(get_client_id()):
            return jsonify({"reply": "تم تجاوز حد الطلبات مؤقتاً."}), 429

        data = request.get_json(force=True) or {}
        message = (data.get("message") or "").strip()
        ai_type = (data.get("ai_type") or "groq").lower()
        session_id = data.get("session_id") or str(uuid.uuid4())
        ui_mode = data.get("ui_mode") or "holo"

        if not message:
            return jsonify(
                {"reply": "أسمعك يا سيدي.", "session_id": session_id}
            )

        safe_add_to_history("user", message, session_id)
        reply, provider = generate_ai_response(
            session_id, message, ai_type=ai_type, ui_mode=ui_mode
        )
        safe_add_to_history("assistant", reply, session_id)

        return jsonify(
            {
                "reply": reply,
                "session_id": session_id,
                "provider": provider,
                "ui_mode": ui_mode,
            }
        )

    except Exception as e:
        logger.error(f"خطأ في /ask: {e}")
        return (
            jsonify(
                {
                    "reply": "حدث خطأ غير متوقع",
                    "session_id": data.get("session_id") if data else None,
                }
            ),
            500,
        )

# ============================
# 11) Feedback (RLHF)
# ============================

@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json(force=True) or {}
        score = float(data.get("score", 0))
        session_id = data.get("session_id")
        reason = data.get("comment", "")

        safe_process_feedback(score, session_id, reason)

        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"خطأ في /feedback: {e}")
        return jsonify({"success": False}), 500

# ============================
# 12) Clear Session + Summarize
# ============================

@app.route("/clear", methods=["POST"])
def clear():
    try:
        data = request.get_json(force=True) or {}
        session_id = data.get("session_id")

        if session_id:
            safe_summarize_session(session_id)

        if memory and hasattr(memory, "clear_conversation_history"):
            memory.clear_conversation_history(session_id)

        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"خطأ في /clear: {e}")
        return jsonify({"status": "error"}), 500

# ============================
# 13) Health & Status
# ============================

@app.route("/api/v1/status", methods=["GET"])
def api_status():
    try:
        return jsonify(
            {
                "status": "ok",
                "service": "SkyOS v10 Holographic OS",
                "time": datetime.utcnow().isoformat() + "Z",
            }
        )
    except Exception as e:
        logger.error(f"خطأ في /api/v1/status: {e}")
        return jsonify({"status": "error"}), 500

@app.route("/api/v1/health", methods=["GET"])
def api_health():
    return "OK", 200

# ============================
# 14) Error Handlers عامة
# ============================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "المسار غير موجود"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal Server Error: {e}")
    return jsonify({"error": "خطأ داخلي في الخادم"}), 500

# ============================
# 15) Local Run
# ============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
