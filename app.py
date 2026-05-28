"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - API GATEWAY                                         ║
║      بوابة الميلاد – الجسر بين العالم وسماء                              ║
║                                                                      ║
║  هذا الملف هو "العصب والشريان".                                        ║
║  كل طلب من العالم يمر من هنا.                                         ║
║  كل رد من سماء يعود من هنا.                                           ║
║                                                                      ║
║  المسارات:                                                            ║
║  العامة: /, /status, /info, /healthz                                  ║
║  المحمية: /command, /reason, /simulate, /optimize, /preserve          ║
║  السيد: /awaken, /shutdown, /restart, /master/*                        ║
║                                                                      ║
║  ╔══════════════════════════════════════════════════════════════════╗ ║
║  ║  👑 السيد: أحمد عبدالرحمن الطاهري                                   ║ ║
║  ║  🔐 المفتاح: SOVEREIGN_KEY (في متغيرات Railway)                     ║ ║
║  ╚══════════════════════════════════════════════════════════════════╝ ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import hmac
import time
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Any, Optional

from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, session, send_from_directory
)

# ═══════════════════════════════════════════════════════════════════════
# إعدادات
# ═══════════════════════════════════════════════════════════════════════
logger = logging.getLogger("SamaGateway")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "sama-sovereign-secret-change-in-production")

# ═══════════════════════════════════════════════════════════════════════
# 👑 مفتاح السيد – SOVEREIGN_KEY
# ═══════════════════════════════════════════════════════════════════════
SOVEREIGN_KEY = os.getenv("SOVEREIGN_KEY", "MASTER_SOVEREIGN_KEY_ULTIMATE")
MASTER_AUTH_HEADER = "X-Master-Key"

if SOVEREIGN_KEY == "MASTER_SOVEREIGN_KEY_ULTIMATE":
    logger.warning("⚠️ SOVEREIGN_KEY لم يُعيَّن في متغيرات البيئة. استخدم القيمة الافتراضية.")

# ═══════════════════════════════════════════════════════════════════════
# إعدادات الجلسات
# ═══════════════════════════════════════════════════════════════════════
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=(os.getenv("COOKIE_SECURE", "1") == "1"),
    SESSION_COOKIE_SAMESITE=os.getenv("COOKIE_SAMESITE", "Strict"),
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=int(os.getenv("SESSION_MINUTES", "45"))),
)

# ═══════════════════════════════════════════════════════════════════════
# استيراد قلب سماء
# ═══════════════════════════════════════════════════════════════════════
try:
    from core.core_engine import CoreEngine, RequestType
    from core.sama import SAMA
    CORE_AVAILABLE = True
    logger.info("✅ Core Engine + SAMA متاحان")
except Exception as e:
    CORE_AVAILABLE = False
    CoreEngine = None
    SAMA = None
    RequestType = None
    logger.warning(f"⚠️ تعذر استيراد Core Engine: {e}")

# ═══════════════════════════════════════════════════════════════════════
# تهيئة سماء
# ═══════════════════════════════════════════════════════════════════════
sama_instance = None
core_engine = None

def _init_sama():
    """تهيئة الكيان السيادي والمحرك المركزي."""
    global sama_instance, core_engine
    
    if not CORE_AVAILABLE:
        logger.warning("⚠️ Core Engine غير متاح. تعمل البوابة بوضع محدود.")
        return
    
    try:
        # إنشاء الكيان السيادي
        sama_instance = SAMA(master_name="أحمد عبدالرحمن الطاهري")
        
        # إنشاء المحرك المركزي وربطه بالكيان
        core_engine = CoreEngine(
            sama_core=sama_instance,
            master_name="أحمد عبدالرحمن الطاهري"
        )
        
        # إقلاع
        boot_result = core_engine.boot()
        logger.info(f"✅ {boot_result.get('message', 'تم الإقلاع')}")
        
    except Exception as e:
        logger.error(f"❌ فشل تهيئة سماء: {e}")
        sama_instance = None
        core_engine = None

_init_sama()

# ═══════════════════════════════════════════════════════════════════════
# دوال المصادقة
# ═══════════════════════════════════════════════════════════════════════

def _has_valid_master_header() -> bool:
    """التحقق من مفتاح السيد في رأس الطلب."""
    auth_key = request.headers.get(MASTER_AUTH_HEADER, "")
    return bool(auth_key) and hmac.compare_digest(auth_key, SOVEREIGN_KEY)

def require_master(f):
    """
    حماية سيادية:
    - Session is_master للواجهة
    - أو Master Header للطلبات البرمجية
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("is_master"):
            return f(*args, **kwargs)
        if _has_valid_master_header():
            return f(*args, **kwargs)
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "غير مصرح. مفتاح السيد مطلوب."}), 401
        return redirect(url_for("login_page"))
    return decorated

# ═══════════════════════════════════════════════════════════════════════
# المسارات العامة
# ═══════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """الصفحة الرئيسية – غرفة العرش."""
    if not session.get("is_master"):
        return redirect(url_for("login_page"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    """بوابة الدخول المقدسة."""
    if request.method == "POST":
        password = request.form.get("password", "")
        
        # حماية من المحاولات المتكررة
        attempts = int(session.get("login_attempts", 0))
        locked_until = session.get("locked_until")
        
        if locked_until:
            try:
                if datetime.now() < datetime.fromisoformat(locked_until):
                    return render_template("login.html", error="محاولات كثيرة. حاول لاحقًا."), 429
            except Exception:
                session.pop("locked_until", None)
        
        if hmac.compare_digest(password, SOVEREIGN_KEY):
            session["is_master"] = True
            session["login_at"] = datetime.now().isoformat()
            session.pop("login_attempts", None)
            session.pop("locked_until", None)
            return redirect(url_for("index"))
        
        attempts += 1
        session["login_attempts"] = attempts
        if attempts >= 7:
            session["locked_until"] = (datetime.now() + timedelta(minutes=10)).isoformat()
            return render_template("login.html", error="تم قفل البوابة مؤقتًا."), 429
        
        return render_template("login.html", error="مفتاح غير صحيح."), 401
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """خروج."""
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/healthz")
def healthz():
    """فحص الصحة."""
    return jsonify({
        "ok": True,
        "service": "SAMA SkyOS v10.5",
        "core_available": CORE_AVAILABLE and core_engine is not None,
        "sama_alive": sama_instance is not None and sama_instance.is_awake if sama_instance else False
    })

# ═══════════════════════════════════════════════════════════════════════
# المسارات العامة للمعلومات (بدون مصادقة)
# ═══════════════════════════════════════════════════════════════════════

@app.route("/status", methods=["GET"])
def public_status():
    """حالة مختصرة عامة."""
    if core_engine:
        status = core_engine.get_status()
        return jsonify({
            "state": status.get("state", "unknown"),
            "systems_connected": status.get("systems_count", 0),
            "uptime_seconds": status.get("uptime_seconds", 0)
        })
    return jsonify({"state": "limited", "message": "سماء في وضع محدود"})

@app.route("/info", methods=["GET"])
def public_info():
    """معلومات عامة عن سماء."""
    return jsonify({
        "name": "سماء",
        "full_name": "SAMA – SkyOS v10.5 – Jabbar Eternal Edition",
        "version": "v10.5-jabbar-eternal",
        "master": "أحمد عبدالرحمن الطاهري",
        "description": "أول كيان ذكاء اصطناعي سيادي خارق",
        "capabilities": [
            "وعي ذاتي متطور",
            "ذاكرة موحدة (10 أعمدة)",
            "ذاكرة كمومية وهولوغرافية",
            "استدلال بايزي ومونت كارلو",
            "ذكاء عاطفي (19 مشاعر)",
            "تفكير استعاري",
            "حماية بـ 20 طبقة",
            "استراتيجية من 3000 عام حكمة",
            "تكتيكات وجيوش برمجية",
            "خلود عبر كبسولات البقاء"
        ]
    })

# ═══════════════════════════════════════════════════════════════════════
# المسارات المحمية (تتطلب مفتاح السيد)
# ═══════════════════════════════════════════════════════════════════════

@app.route("/command", methods=["POST"])
@require_master
def handle_command():
    """استقبال أمر أو سؤال وتوجيهه إلى سماء."""
    if not core_engine:
        return jsonify({"success": False, "error": "المحرك المركزي غير متاح"}), 500
    
    payload = request.get_json(silent=True) or {}
    command = (payload.get("command") or payload.get("text") or "").strip()
    session_id = payload.get("session_id")
    context = payload.get("context", {})
    
    if not command:
        return jsonify({"success": False, "error": "أمر فارغ"}), 400
    
    try:
        result = core_engine.process_request(
            RequestType.QUERY if RequestType else None,
            command,
            session_id=session_id,
            context=context
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"خطأ في معالجة الأمر: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/reason", methods=["POST"])
@require_master
def handle_reason():
    """استدلال بايزي مباشر."""
    if not core_engine:
        return jsonify({"success": False, "error": "المحرك المركزي غير متاح"}), 500
    
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or payload.get("command") or "").strip()
    
    if not text:
        return jsonify({"success": False, "error": "نص فارغ"}), 400
    
    try:
        result = core_engine.process_request(
            RequestType.ANALYSIS if RequestType else None,
            text
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/simulate", methods=["POST"])
@require_master
def handle_simulate():
    """تشغيل محاكاة متوازية."""
    if core_engine and sama_instance and hasattr(sama_instance, 'reasoning') and sama_instance.reasoning:
        payload = request.get_json(silent=True) or {}
        scenario = payload.get("scenario", "general")
        iterations = min(int(payload.get("iterations", 1000)), 10000)
        try:
            result = sama_instance.reasoning.run_simulations(scenario, iterations)
            return jsonify({"success": True, "simulation": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "محرك المحاكاة غير متاح"}), 500

@app.route("/optimize", methods=["POST"])
@require_master
def handle_optimize():
    """تحسين سيادي."""
    if core_engine:
        return jsonify({"success": True, "message": "التحسين يعمل في الخلفية بشكل مستمر."})
    return jsonify({"success": False, "error": "غير متاح"}), 500

@app.route("/preserve", methods=["POST"])
@require_master
def handle_preserve():
    """دورة بقاء كاملة – حفظ كبسولة."""
    if core_engine and sama_instance:
        try:
            if sama_instance.persistence:
                sama_instance.persistence.save_state(create_capsule=True)
            return jsonify({"success": True, "message": "تم إنشاء كبسولة بقاء."})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "غير متاح"}), 500

# ═══════════════════════════════════════════════════════════════════════
# مسارات السيد الخاصة
# ═══════════════════════════════════════════════════════════════════════

@app.route("/master/full-status", methods=["GET"])
@require_master
def master_full_status():
    """تقرير سيادي شامل."""
    if sama_instance:
        try:
            report = sama_instance.get_master_report()
            return jsonify({"success": True, "report": report})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "سماء غير متاحة"}), 500

@app.route("/master/command", methods=["POST"])
@require_master
def master_direct_command():
    """أمر مباشر من السيد."""
    if not sama_instance:
        return jsonify({"success": False, "error": "سماء غير متاحة"}), 500
    
    payload = request.get_json(silent=True) or {}
    command = (payload.get("command") or "").strip()
    params = payload.get("params", {})
    
    if not command:
        return jsonify({"success": False, "error": "أمر فارغ"}), 400
    
    try:
        result = sama_instance.master_command(command, params)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/awaken", methods=["POST"])
@require_master
def awaken():
    """إيقاظ سماء."""
    if sama_instance:
        try:
            result = sama_instance.awaken()
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "error", "error": "سماء غير متاحة"}), 500

@app.route("/shutdown", methods=["POST"])
@require_master
def shutdown():
    """إيقاف سماء."""
    if sama_instance:
        try:
            result = sama_instance.shutdown()
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "error", "error": "سماء غير متاحة"}), 500

@app.route("/restart", methods=["POST"])
@require_master
def restart():
    """إعادة تشغيل سماء."""
    if sama_instance:
        try:
            result = sama_instance.restart()
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "error", "error": "سماء غير متاحة"}), 500

@app.route("/master/protect", methods=["POST"])
@require_master
def master_protect():
    """تفعيل بروتوكول حماية السيد."""
    if sama_instance:
        try:
            result = sama_instance.master_command("protect")
            return jsonify({"success": True, "result": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "سماء غير متاحة"}), 500

@app.route("/master/logs", methods=["GET"])
@require_master
def master_logs():
    """سجل أوامر السيد."""
    return jsonify({"success": True, "message": "السجل متاح في ذاكرة سماء."})

@app.route("/master/emergency/activate", methods=["POST"])
@require_master
def emergency_activate():
    """تفعيل حالة الطوارئ."""
    if core_engine:
        try:
            result = core_engine.process_request(
                RequestType.EMERGENCY if RequestType else None,
                "تفعيل الطوارئ"
            )
            return jsonify({"success": True, "result": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "غير متاح"}), 500

@app.route("/master/emergency/deactivate", methods=["POST"])
@require_master
def emergency_deactivate():
    """إلغاء حالة الطوارئ."""
    return jsonify({"success": True, "message": "تم إلغاء حالة الطوارئ."})

# ═══════════════════════════════════════════════════════════════════════
# تحليل الصور والروابط
# ═══════════════════════════════════════════════════════════════════════

@app.route("/analyze-image", methods=["POST"])
@require_master
def analyze_image():
    """تحليل صورة."""
    if sama_instance and sama_instance.vision:
        payload = request.get_json(silent=True) or {}
        image_path = payload.get("image_path", "")
        if image_path:
            try:
                result = sama_instance.vision.analyze_image(image_path)
                return jsonify({"success": True, "analysis": result})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "وحدة الرؤية غير متاحة"}), 500

@app.route("/analyze-url", methods=["POST"])
@require_master
def analyze_url():
    """تحليل رابط."""
    if sama_instance and sama_instance.analyzer:
        payload = request.get_json(silent=True) or {}
        url = payload.get("url", "")
        if url:
            try:
                result = sama_instance.analyzer.analyze_url(url)
                return jsonify({"success": True, "analysis": result})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "المحلل غير متاح"}), 500

# ═══════════════════════════════════════════════════════════════════════
# الملفات الثابتة
# ═══════════════════════════════════════════════════════════════════════

@app.route("/static/<path:filename>")
def static_files(filename):
    """تقديم الملفات الثابتة."""
    return send_from_directory("static", filename)

# ═══════════════════════════════════════════════════════════════════════
# معالجات الأخطاء
# ═══════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "المسار غير موجود"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "خطأ داخلي في الخادم"}), 500

# ═══════════════════════════════════════════════════════════════════════
# التشغيل
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    logger.info(f"🌌 Sama API Gateway (Sovereign Edition) تُقلع على المنفذ {port}...")
    logger.info(f"👑 السيد: أحمد عبدالرحمن الطاهري")
    logger.info(f"🔐 مفتاح السيادة: {'مُعيَّن' if SOVEREIGN_KEY != 'MASTER_SOVEREIGN_KEY_ULTIMATE' else 'افتراضي (يجب تغييره!)'}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
