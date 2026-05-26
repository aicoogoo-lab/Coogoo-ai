"""
SkyOS v10 - Sama API Gateway (Sovereign Master Edition)
=======================================================
البوابة السيادية المغلقة لسماء — تحت إمرة السيد المالك المطلق فقط.

تحسينات سيادية:
- مصادقة موحدة: Session أو Master Header
- Cookies آمنة: Secure/HttpOnly/SameSite
- Lockout بسيط لمحاولات الدخول
- CORS مقيد (أو معطل حسب الإعداد)
- فصل منطق الـAPI عن الـDecorators لتجنب Redirect داخل JSON
- تشغيل الحلقة الذاتية عبر ENV لمنع تعدد النسخ في الإنتاج
- Logging احترافي بدل print
"""

import os
import hmac
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, Optional

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, make_response
from flask_cors import CORS

# ----------------------------
# Logging
# ----------------------------
logger = logging.getLogger(__name__)

# ============================================================
# استيراد نواة سماء والحلقة الذاتية السيادية
# ============================================================
try:
    from core.sama import SAMA
except Exception as e:
    SAMA = None
    logger.exception("[Gateway] ⚠️ Failed to import SAMA: %s", e)

try:
    from core.autonomous_loop import AutonomousLoop
except Exception as e:
    AutonomousLoop = None
    logger.exception("[Gateway] ⚠️ Failed to import AutonomousLoop: %s", e)

# ============================================================
# Flask App
# ============================================================
app = Flask(__name__)

# ============================================================
# إعدادات الأمان والجلسات
# ============================================================
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key-in-production")

# Cookie security best-practice for auth cookies (سيادي مغلق)
# Secure: HTTPS only, HttpOnly: not readable by JS, SameSite: CSRF mitigation
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=(os.getenv("COOKIE_SECURE", "1") == "1"),  # اجعلها 0 فقط لو dev بدون https
    SESSION_COOKIE_SAMESITE=os.getenv("COOKIE_SAMESITE", "Strict"),
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=int(os.getenv("SESSION_MINUTES", "45"))),
)

# ============================================================
# مفاتيح السيد (لا تُخزن في الكود في الإنتاج)
# ============================================================
MASTER_API_KEY = os.getenv("MASTER_API_KEY", "CHANGE_THIS_IN_ENV")
MASTER_AUTH_HEADER = "X-Master-Key"
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD", "sama2026")

if MASTER_API_KEY == "CHANGE_THIS_IN_ENV":
    logger.warning("⚠️ Security warning: MASTER_API_KEY not set in environment variables!")

# ============================================================
# CORS (الأفضل تقييده أو تعطيله)
# ============================================================
# إذا كانت الواجهة من نفس الدومين، تقدر تعطله كليًا:
#   DISABLE_CORS=1
# أو تحدد Origins:
#   CORS_ORIGINS=https://your-domain.com,https://another-domain.com
if os.getenv("DISABLE_CORS", "1") == "1":
    logger.info("[Gateway] CORS disabled (sovereign closed mode).")
else:
    origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
    CORS(app, resources={r"/api/*": {"origins": origins or "*"}}, supports_credentials=True)
    logger.info("[Gateway] CORS enabled for /api/* origins=%s", origins or ["*"])

# ============================================================
# Decorators
# ============================================================
def _has_valid_master_header() -> bool:
    auth_key = request.headers.get(MASTER_AUTH_HEADER, "")
    return bool(auth_key) and hmac.compare_digest(auth_key, MASTER_API_KEY)

def require_master_access(f):
    """
    حماية سيادية موحدة:
    - Session is_master للواجهة
    - أو Master Header للطلبات البرمجية
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("is_master"):
            return f(*args, **kwargs)
        if _has_valid_master_header():
            return f(*args, **kwargs)
        # لا Redirect في API endpoints؛ نرجع JSON
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "غير مصرح به"}), 401
        return redirect(url_for("login"))
    return decorated

def login_required_page(f):
    """لحماية صفحات HTML فقط"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_master"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# ============================================================
# تهيئة سماء + الحلقة الذاتية السيادية (مع Guards)
# ============================================================
sama = None
loop = None

def _should_start_loop() -> bool:
    """
    تشغيل الحلقة في الإنتاج يحتاج قرار واضح.
    اجعلها تعمل فقط إذا ENABLE_AUTONOMOUS_LOOP=1
    لتجنب تشغيل عدة نسخ عبر تعدد Workers.
    """
    return os.getenv("ENABLE_AUTONOMOUS_LOOP", "0") == "1"

def _init_sama():
    global sama
    if SAMA is None:
        logger.warning("[Gateway] SAMA not available (import failed).")
        return
    try:
        sama = SAMA()
        if hasattr(sama, "awaken"):
            sama.awaken()
        logger.info("[Gateway] ✅ SAMA initialized & awakened.")
    except Exception as e:
        sama = None
        logger.exception("[Gateway] ⚠️ Failed to initialize SAMA: %s", e)

def _init_loop():
    global loop
    if AutonomousLoop is None:
        logger.warning("[Gateway] AutonomousLoop not available (import failed).")
        return

    if not _should_start_loop():
        logger.info("[Gateway] AutonomousLoop startup skipped (ENABLE_AUTONOMOUS_LOOP=0).")
        return

    try:
        # لاحظ: master_key هنا ليس API_KEY الأفضل، لكنه مقبول مؤقتًا.
        # لاحقًا نفصل: LOOP_MASTER_KEY مختلف عن MASTER_API_KEY.
        loop = AutonomousLoop(core=sama, master_key=MASTER_API_KEY)
        loop.start()
        logger.info("[Gateway] ✅ AutonomousLoop started.")
    except Exception as e:
        loop = None
        logger.exception("[Gateway] ⚠️ Failed to start AutonomousLoop: %s", e)

_init_sama()
_init_loop()

# ============================================================
# Session behavior
# ============================================================
@app.before_request
def _session_policy():
    """
    - نجعل الجلسة دائمة ضمن PERMANENT_SESSION_LIFETIME
    - مع كل request من السيد نحدث آخر نشاط
    """
    if session.get("is_master"):
        session.permanent = True
        session["last_seen"] = datetime.now().isoformat()

# ============================================================
# Routes (Pages)
# ============================================================
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    بوابة السيادة:
    - Lockout بسيط داخل session
    - مقارنة ثابتة الزمن
    """
    if request.method == "POST":
        # lockout
        attempts = int(session.get("login_attempts", 0))
        locked_until = session.get("locked_until")

        if locked_until:
            try:
                if datetime.now() < datetime.fromisoformat(locked_until):
                    return "محاولات كثيرة. حاول لاحقًا.", 429
            except Exception:
                session.pop("locked_until", None)

        password = request.form.get("password", "")
        if hmac.compare_digest(password, MASTER_PASSWORD):
            session["is_master"] = True
            session["login_at"] = datetime.now().isoformat()
            session.pop("login_attempts", None)
            session.pop("locked_until", None)
            return redirect(url_for("sovereign"))

        # failed
        attempts += 1
        session["login_attempts"] = attempts
        if attempts >= int(os.getenv("LOGIN_MAX_ATTEMPTS", "7")):
            lock_minutes = int(os.getenv("LOGIN_LOCK_MINUTES", "10"))
            session["locked_until"] = (datetime.now() + timedelta(minutes=lock_minutes)).isoformat()
            return "محاولات كثيرة. تم قفل البوابة مؤقتًا.", 429

        return "كلمة مرور غير صحيحة", 401

    return render_template("login.html")

@app.route("/sovereign")
@login_required_page
def sovereign():
    return render_template("sovereign.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/healthz")
def healthz():
    """
    Health check minimal — لا يكشف أسرار.
    """
    return jsonify({"ok": True, "service": "SkyOS Gateway"})

# ============================================================
# Internal logic (تفادي تداخل decorators)
# ============================================================
def _build_status_payload() -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "sama_initialized": bool(sama),
        "loop_initialized": bool(loop),
    }

    if sama and hasattr(sama, "get_full_status"):
        try:
            data["sama_status"] = sama.get_full_status()
        except Exception as e:
            data["sama_status_error"] = str(e)

    if loop and hasattr(loop, "get_status"):
        try:
            data["loop_status"] = loop.get_status()
        except Exception as e:
            data["loop_status_error"] = str(e)

    return data

def _dispatch_command(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
    # أولوية: الحلقة الذاتية
    if loop and hasattr(loop, "receive_master_command"):
        cmd_id = loop.receive_master_command(command, params)
        return {
            "success": True,
            "via": "loop",
            "command_id": cmd_id,
            "message": "تم إرسال الأمر إلى الحلقة الذاتية السيادية"
        }

    # بديل: إرسال مباشر إلى SAMA
    if sama and hasattr(sama, "process_command"):
        result = sama.process_command(command, params)
        return {"success": True, "via": "sama", "result": result}

    return {"success": False, "error": "لا توجد آلية لتنفيذ الأوامر حالياً"}

# ============================================================
# API (Protected for Master)
# ============================================================
@app.route("/api/master/status", methods=["GET"])
@require_master_access
def master_status():
    if not sama and not loop:
        return jsonify({"success": False, "error": "سماء والحلقة غير مهيأتين"}), 500
    return jsonify({"success": True, "data": _build_status_payload()})

@app.route("/api/master/command", methods=["POST"])
@require_master_access
def master_command():
    if not sama and not loop:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    payload = request.get_json(silent=True) or {}
    command = (payload.get("command") or "").strip()
    params = payload.get("params") or {}

    if not command:
        return jsonify({"success": False, "error": "يجب إرسال command"}), 400

    try:
        return jsonify(_dispatch_command(command, params))
    except Exception as e:
        logger.exception("[Gateway] command failed")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/master/loop/commands", methods=["GET"])
@require_master_access
def master_loop_commands():
    if not loop or not hasattr(loop, "get_command_results"):
        return jsonify({"success": False, "error": "الحلقة الذاتية غير مهيأة"}), 500
    try:
        limit = int(request.args.get("limit", 50))
        results = loop.get_command_results(limit=limit)
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/master/loop/history", methods=["GET"])
@require_master_access
def master_loop_history():
    if not loop or not hasattr(loop, "get_master_command_history"):
        return jsonify({"success": False, "error": "الحلقة الذاتية غير مهيأة"}), 500
    try:
        limit = int(request.args.get("limit", 50))
        history = loop.get_master_command_history(limit=limit)
        return jsonify({"success": True, "history": history})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/master/emergency/activate", methods=["POST"])
@require_master_access
def emergency_activate():
    # Placeholder: اربطها لاحقًا بالـcore أو loop
    return jsonify({"success": True, "message": "تم تفعيل حالة الطوارئ (placeholder)"})

@app.route("/api/master/emergency/deactivate", methods=["POST"])
@require_master_access
def emergency_deactivate():
    # Placeholder: اربطها لاحقًا بالـcore أو loop
    return jsonify({"success": True, "message": "تم إلغاء حالة الطوارئ (placeholder)"})

# ============================================================
# API عبر Master Header (مباشر)
# ============================================================
@app.route("/api/secure/status", methods=["GET"])
@require_master_access
def secure_status():
    # الآن لا يوجد redirect لأنه نفس decorator
    return master_status()

@app.route("/api/secure/command", methods=["POST"])
@require_master_access
def secure_command():
    return master_command()

# ============================================================
# تشغيل التطبيق
# ============================================================
if __name__ == "__main__":
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    logger.info("🌌 Sama API Gateway (Sovereign Edition) running...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False, threaded=True)
