# ==========================================================
# SAMA - API GATEWAY (Fixed + Stable)
# بوابة الميلاد – الجسر بين العالم وسماء
# ==========================================================

import os
import hmac
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Optional

from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, session, send_from_directory, make_response
)

from werkzeug.middleware.proxy_fix import ProxyFix


# ---------------------------
# Logging
# ---------------------------
logger = logging.getLogger("SamaGateway")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# ---------------------------
# Flask App
# ---------------------------
app = Flask(__name__)

# لازم Secret Key ثابت في Railway Variables
app.secret_key = os.getenv("FLASK_SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")

# Reverse Proxy trust (Railway / any proxy)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# ---------------------------
# Sovereign key / header
# ---------------------------
SOVEREIGN_KEY = (os.getenv("SOVEREIGN_KEY", "") or "").strip()
MASTER_AUTH_HEADER = "X-Master-Key"

if not SOVEREIGN_KEY:
    logger.warning("⚠️ SOVEREIGN_KEY غير معيّن. تسجيل الدخول لن يعمل حتى تضبطه في Variables.")

# ---------------------------
# Session/Cookie config
# ---------------------------
# ملاحظة: SameSite و Secure قد يمنعوا الكوكي في حالات cross-site أو http
# القيم المسموحة في Flask عادة: 'Lax' أو 'Strict' أو 'None' (كنص)  ‎[3](https://stackoverflow.com/questions/69573920/python-flask-how-to-set-session-cookie-attributes-samesite-none-and-secure)‎[5](https://github.com/pallets/flask/issues/3845)
cookie_secure = (os.getenv("COOKIE_SECURE", "1") == "1")
cookie_samesite = os.getenv("COOKIE_SAMESITE", "Lax")  # خليه Lax افتراضي عشان يقلّل مشاكل تسجيل الدخول

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=cookie_secure,
    SESSION_COOKIE_SAMESITE=cookie_samesite,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=int(os.getenv("SESSION_MINUTES", "45"))),
)

# ---------------------------
# Helpers: detect JSON/AJAX
# ---------------------------
def _wants_json() -> bool:
    accept = (request.headers.get("Accept", "") or "").lower()
    xrw = (request.headers.get("X-Requested-With", "") or "").lower()
    ctype = (request.headers.get("Content-Type", "") or "").lower()
    # أي طلب API أو fetch غالبًا بيكون Accept: application/json أو Content-Type json
    return (
        request.path.startswith("/api/")
        or "application/json" in accept
        or "application/json" in ctype
        or xrw == "xmlhttprequest"
    )

def _has_valid_master_header() -> bool:
    auth_key = (request.headers.get(MASTER_AUTH_HEADER, "") or "").strip()
    key = (SOVEREIGN_KEY or "").strip()
    return bool(auth_key) and bool(key) and hmac.compare_digest(auth_key, key)

def require_master(f):
    """
    حماية:
    - session.is_master للواجهة
    - أو X-Master-Key للطلبات البرمجية
    IMPORTANT: للـ API لازم نرجّع JSON 401 بدل redirect (عشان ما يكسر fetch)
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("is_master"):
            return f(*args, **kwargs)
        if _has_valid_master_header():
            return f(*args, **kwargs)

        # لو الطلب API/JSON: رجّع JSON 401 (ده يمنع JSON.parse error اللي بيحصل لما يرجع HTML) ‎[1](https://www.w3tutorials.net/blog/syntaxerror-json-parse-unexpected-character-at-line-1-column-1-of-the-json-data/)‎[2](https://stackoverflow.com/questions/76993250/flask-react-cant-parse-correct-json-unexpected-character-at-line-1-column-1)
        if _wants_json():
            return jsonify({"success": False, "error": "غير مصرح. سجّل الدخول أو استخدم X-Master-Key."}), 401

        # غير كده: redirect لصفحة login
        return redirect(url_for("login_page"))
    return decorated


# ==========================================================
# Safe import systems (زي ملفك)
# ==========================================================
CORE_AVAILABLE = True
SYSTEMS_LOADED = {}
SYSTEMS_FAILED = {}

def _safe_import(module_path: str, system_name: str) -> Optional[Any]:
    try:
        module = __import__(module_path, fromlist=[system_name])
        cls = getattr(module, system_name)
        SYSTEMS_LOADED[system_name] = True
        return cls
    except Exception as e:
        SYSTEMS_FAILED[system_name] = str(e)[:200]
        return None

# استيراد الأنظمة (زي السابق)
SentientCore = _safe_import("core.sentient_core", "SentientCore")
UnifiedMemorySystem = _safe_import("core.memory", "UnifiedMemorySystem")
SovereignMemorySystem = _safe_import("core.sovereign_memory_system", "SovereignMemorySystem")
DefenseCore = _safe_import("core.defense_core", "DefenseCore")
EmotionalIntelligence = _safe_import("core.emotional_intelligence", "EmotionalIntelligence")
MetaphoricalReasoning = _safe_import("core.metaphorical_reasoning", "MetaphoricalReasoning")
StrategyEngine = _safe_import("core.strategy_engine", "StrategyEngine")
StrategicRiskManagement = _safe_import("core.strategic_risk_management", "StrategicRiskManagement")
SamaAdvancedTactics = _safe_import("core.sama_advanced_tactics", "SamaAdvancedTactics")
SelfModifier = _safe_import("core.self_modifier", "SelfModifier")
PersistenceManager = _safe_import("core.persistence_manager", "EternalPersistenceManager")
ReasoningEngine = _safe_import("core.reasoning_engine", "ReasoningEngine")
MetaCognition = _safe_import("core.meta_cognition", "MetaCognition")
HolographicEncoder = _safe_import("core.holographic_encoder", "HolographicEncoder")
VisionModule = _safe_import("core.vision_module", "VisionModule")
SkyAnalyzer = _safe_import("core.sky_analyzer", "SkyAnalyzer")
SkyCore = _safe_import("core.sky_core", "SkyCore")

OmniscienceCore = _safe_import("core.omniscience.integration_core", "OmniscienceCore")
KnowledgeCore = _safe_import("core.knowledge.knowledge_core", "KnowledgeCore")
InferenceCore = _safe_import("core.inference.inference_core", "InferenceCore")

CoreEngine = _safe_import("core.core_engine", "CoreEngine")
RequestType = None
if CoreEngine:
    try:
        from core.core_engine import RequestType as RT
        RequestType = RT
    except Exception:
        RequestType = None

SAMA = _safe_import("core.sama", "SAMA")


# ==========================================================
# Init SAMA
# ==========================================================
sama_instance = None
core_engine = None

def _init_sama():
    global sama_instance, core_engine

    if not SAMA or not CoreEngine:
        logger.error("❌ SAMA أو CoreEngine غير متاح. البوابة ستعمل بوضع محدود.")
        return

    try:
        logger.info("🔧 بدء تهيئة سماء...")

        # 1) Memory
        memory_instance = None
        sovereign_memory = None
        if UnifiedMemorySystem:
            try:
                memory_instance = UnifiedMemorySystem()
                logger.info("✅ UnifiedMemorySystem")
            except Exception as e:
                logger.warning(f"⚠️ UnifiedMemorySystem: {e}")

        if SovereignMemorySystem:
            try:
                sovereign_memory = SovereignMemorySystem(
                    master_name="أحمد عبدالرحمن الطاهري",
                    unified_memory=memory_instance
                )
                logger.info("✅ SovereignMemorySystem")
            except Exception as e:
                logger.warning(f"⚠️ SovereignMemorySystem: {e}")

        # 2) Holographic
        holo_encoder = None
        if HolographicEncoder:
            try:
                holo_encoder = HolographicEncoder(dimension=10000)
                logger.info("✅ HolographicEncoder")
            except Exception as e:
                logger.warning(f"⚠️ HolographicEncoder: {e}")

        # 3) Emotion
        emotional_instance = None
        if EmotionalIntelligence:
            try:
                emotional_instance = EmotionalIntelligence(memory_engine=memory_instance)
                logger.info("✅ EmotionalIntelligence")
            except Exception as e:
                logger.warning(f"⚠️ EmotionalIntelligence: {e}")

        # 4) Metaphor
        metaphorical_instance = None
        if MetaphoricalReasoning:
            try:
                metaphorical_instance = MetaphoricalReasoning(
                    memory_engine=memory_instance,
                    emotional_intelligence=emotional_instance
                )
                logger.info("✅ MetaphoricalReasoning")
            except Exception as e:
                logger.warning(f"⚠️ MetaphoricalReasoning: {e}")

        # 5) Defense
        defense_instance = None
        if DefenseCore:
            try:
                defense_instance = DefenseCore()
                logger.info("✅ DefenseCore")
            except Exception as e:
                logger.warning(f"⚠️ DefenseCore: {e}")

        # 6) Tactics
        tactics_instance = None
        if SamaAdvancedTactics:
            try:
                tactics_instance = SamaAdvancedTactics(
                    defense_core=defense_instance,
                    risk_manager=None
                )
                logger.info("✅ SamaAdvancedTactics")
            except Exception as e:
                logger.warning(f"⚠️ SamaAdvancedTactics: {e}")

        # 7) Risk
        risk_instance = None
        if StrategicRiskManagement:
            try:
                risk_instance = StrategicRiskManagement(
                    master_name="أحمد",
                    defense_core=defense_instance,
                    tactics_manager=tactics_instance
                )
                logger.info("✅ StrategicRiskManagement")
            except Exception as e:
                logger.warning(f"⚠️ StrategicRiskManagement: {e}")

        # 8) Strategy
        strategy_instance = None
        if StrategyEngine:
            try:
                strategy_instance = StrategyEngine(
                    master_name="أحمد",
                    defense_core=defense_instance,
                    tactics_manager=tactics_instance,
                    risk_manager=risk_instance,
                    sovereign_memory=sovereign_memory
                )
                logger.info("✅ StrategyEngine")
            except Exception as e:
                logger.warning(f"⚠️ StrategyEngine: {e}")

        # 9) SelfModifier
        modifier_instance = None
        if SelfModifier:
            try:
                modifier_instance = SelfModifier(
                    memory_engine=memory_instance,
                    defense_core=defense_instance
                )
                logger.info("✅ SelfModifier")
            except Exception as e:
                logger.warning(f"⚠️ SelfModifier: {e}")

        # 10) Reasoning
        reasoning_instance = None
        if ReasoningEngine:
            try:
                reasoning_instance = ReasoningEngine(
                    probability_engine=None,
                    prediction_engine=None,
                    causality_engine=None,
                    inference_core=None,
                    emotional_intelligence=emotional_instance,
                    defense_core=defense_instance,
                    metaphorical_reasoning=metaphorical_instance
                )
                logger.info("✅ ReasoningEngine")
            except Exception as e:
                logger.warning(f"⚠️ ReasoningEngine: {e}")

        # 11) Persistence
        persistence_instance = None
        if PersistenceManager:
            try:
                persistence_instance = PersistenceManager(auto_save=True, distributed_mode=True)
                logger.info("✅ EternalPersistenceManager")
            except Exception as e:
                logger.warning(f"⚠️ EternalPersistenceManager: {e}")

        # 12) Meta
        meta_instance = None
        if MetaCognition:
            try:
                meta_instance = MetaCognition()
                logger.info("✅ MetaCognition")
            except Exception as e:
                logger.warning(f"⚠️ MetaCognition: {e}")

        # 13) Vision
        vision_instance = None
        if VisionModule:
            try:
                vision_instance = VisionModule()
                logger.info("✅ VisionModule")
            except Exception as e:
                logger.warning(f"⚠️ VisionModule: {e}")

        # 14) Analyzer
        analyzer_instance = None
        if SkyAnalyzer:
            try:
                analyzer_instance = SkyAnalyzer(
                    memory_engine=memory_instance,
                    holographic_encoder=holo_encoder,
                    emotional_intelligence=emotional_instance,
                    metaphorical_reasoning=metaphorical_instance
                )
                logger.info("✅ SkyAnalyzer")
            except Exception as e:
                logger.warning(f"⚠️ SkyAnalyzer: {e}")

        # 15) Sentient
        sentient_instance = None
        if SentientCore:
            try:
                sentient_instance = SentientCore(
                    master_receiver=None,
                    knowledge_core=None,
                    inference_core=None,
                    defense_core=defense_instance,
                    memory_engine=memory_instance,
                    meta_cognition=meta_instance,
                    self_knowledge=None
                )
                logger.info("✅ SentientCore")
            except Exception as e:
                logger.warning(f"⚠️ SentientCore: {e}")

        # Create SAMA
        logger.info("☀️ إنشاء SAMA...")
        sama_instance = SAMA(
            master_name="أحمد عبدالرحمن الطاهري",
            sentient_core=sentient_instance,
            omniscience_core=None,
            knowledge_core=None,
            inference_core=None,
            defense_core=defense_instance,
            self_modifier=modifier_instance,
            sovereign_memory=sovereign_memory,
            emotional_intelligence=emotional_instance,
            metaphorical_reasoning=metaphorical_instance,
            strategy_engine=strategy_instance,
            risk_manager=risk_instance,
            advanced_tactics=tactics_instance,
            persistence_manager=persistence_instance,
            autonomous_loop=None,
            vision_module=vision_instance,
            sky_analyzer=analyzer_instance,
            sky_core=None,
            meta_cognition=meta_instance,
            reasoning_engine=reasoning_instance,
            holographic_encoder=holo_encoder,
            master_receiver=None
        )

        # Create CoreEngine
        logger.info("🧠 إنشاء CoreEngine...")
        core_engine = CoreEngine(
            sama_core=sama_instance,
            master_name="أحمد عبدالرحمن الطاهري"
        )

        try:
            boot_result = core_engine.boot()
            logger.info(f"✅ {boot_result.get('message', 'تم الإقلاع')}")
        except Exception as e:
            logger.warning(f"⚠️ boot(): {e}")

        logger.info(f"📊 loaded={len(SYSTEMS_LOADED)} failed={len(SYSTEMS_FAILED)}")

    except Exception as e:
        logger.error(f"❌ فشل تهيئة سماء: {e}")
        sama_instance = None
        core_engine = None

_init_sama()


# ==========================================================
# Pages
# ==========================================================

@app.route("/")
@require_master
def index():
    # لازم تكون محمية عشان تسجيل الدخول “يبان” ويشتغل فعليًا
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    """
    بوابة الدخول:
    - strip whitespace
    - rate limit attempts + lock
    """
    if request.method == "POST":
        password = (request.form.get("password") or "").strip()
        key = (SOVEREIGN_KEY or "").strip()

        if not key:
            logger.error("SOVEREIGN_KEY غير مضبوط.")
            return render_template("login.html", error="خطأ إعداد: SOVEREIGN_KEY غير مضبوط."), 500

        # lock logic
        attempts = int(session.get("login_attempts", 0))
        locked_until = session.get("locked_until")

        if locked_until:
            try:
                until = datetime.fromisoformat(locked_until)
                if datetime.now() < until:
                    return render_template("login.html", error="البوابة مقفولة مؤقتًا. افتح /logout لتصفير الجلسة."), 429
            except Exception:
                session.pop("locked_until", None)

        if hmac.compare_digest(password, key):
            session.clear()
            session["is_master"] = True
            session["login_at"] = datetime.now().isoformat()
            session.permanent = True
            return redirect(url_for("index"))

        attempts += 1
        session["login_attempts"] = attempts
        remaining = max(0, 7 - attempts)

        if attempts >= 7:
            session["locked_until"] = (datetime.now() + timedelta(minutes=10)).isoformat()
            return render_template("login.html", error="تم قفل البوابة 10 دقائق. افتح /logout لتصفير الجلسة."), 429

        return render_template("login.html", error=f"مفتاح غير صحيح. متبقي {remaining} محاولة."), 401

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ==========================================================
# Public endpoints
# ==========================================================

@app.route("/healthz")
def healthz():
    systems_count = sama_instance._count_systems() if sama_instance else 0
    return jsonify({
        "ok": True,
        "service": "SAMA SkyOS",
        "core_available": core_engine is not None,
        "sama_alive": bool(sama_instance),
        "systems_unified": systems_count,
        "systems_loaded": len(SYSTEMS_LOADED),
        "systems_failed": len(SYSTEMS_FAILED)
    })


@app.route("/status", methods=["GET"])
def public_status():
    if core_engine:
        try:
            status = core_engine.get_status()
            return jsonify({
                "state": status.get("state", "unknown"),
                "systems_connected": status.get("systems_count", 0),
                "uptime_seconds": status.get("uptime_seconds", 0)
            })
        except Exception:
            pass
    return jsonify({"state": "limited", "message": "سماء في وضع محدود"})


@app.route("/info", methods=["GET"])
def public_info():
    return jsonify({
        "name": "سماء",
        "version": "v10.5",
        "master": "أحمد عبدالرحمن الطاهري",
        "systems_unified": sama_instance._count_systems() if sama_instance else 0
    })


# Endpoint يساعدك تتأكد إن السيشن اتسجلت
@app.route("/api/whoami", methods=["GET"])
def api_whoami():
    return jsonify({
        "is_master": bool(session.get("is_master")),
        "login_at": session.get("login_at"),
        "cookie_secure": app.config.get("SESSION_COOKIE_SECURE"),
        "cookie_samesite": app.config.get("SESSION_COOKIE_SAMESITE"),
    })


# ==========================================================
# API - JSON ONLY (ده اللي يحل JSON.parse error)
# لأن الخطأ بيحصل لما السيرفر يرجع HTML بدل JSON  ‎[1](https://www.w3tutorials.net/blog/syntaxerror-json-parse-unexpected-character-at-line-1-column-1-of-the-json-data/)‎[2](https://stackoverflow.com/questions/76993250/flask-react-cant-parse-correct-json-unexpected-character-at-line-1-column-1)
# ==========================================================

@app.route("/api/command", methods=["POST"])
@require_master
def api_command():
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
        # ensure JSON object
        if isinstance(result, dict):
            return jsonify(result)
        return jsonify({"success": True, "response": str(result)})
    except Exception as e:
        logger.error(f"خطأ في معالجة الأمر: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/reason", methods=["POST"])
@require_master
def api_reason():
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
        if isinstance(result, dict):
            return jsonify(result)
        return jsonify({"success": True, "response": str(result)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/simulate", methods=["POST"])
@require_master
def api_simulate():
    if core_engine and sama_instance and getattr(sama_instance, "reasoning", None):
        payload = request.get_json(silent=True) or {}
        scenario = payload.get("scenario", "general")
        iterations = min(int(payload.get("iterations", 1000)), 10000)
        try:
            result = sama_instance.reasoning.run_simulations(scenario, iterations)
            return jsonify({"success": True, "simulation": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "محرك المحاكاة غير متاح"}), 500


@app.route("/api/master/unlock", methods=["POST"])
def api_master_unlock():
    if not _has_valid_master_header():
        return jsonify({"success": False, "error": "غير مصرح"}), 401
    session.clear()
    return jsonify({"success": True, "message": "تم تصفير الجلسة/فك القفل."})


# ==========================================================
# Backward compatible route: /command (same JSON behavior)
# عشان لو واجهتك بتستخدم /command
# ==========================================================

@app.route("/command", methods=["POST"])
@require_master
def handle_command():
    # استخدم نفس منطق API عشان لا يرجع HTML ويكسر JSON.parse  ‎[1](https://www.w3tutorials.net/blog/syntaxerror-json-parse-unexpected-character-at-line-1-column-1-of-the-json-data/)‎[2](https://stackoverflow.com/questions/76993250/flask-react-cant-parse-correct-json-unexpected-character-at-line-1-column-1)
    return api_command()


@app.route("/reason", methods=["POST"])
@require_master
def handle_reason():
    return api_reason()


# ==========================================================
# Static
# ==========================================================
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


# ==========================================================
# Error handlers:
# - للـ API: JSON
# - للصفحات: JSON بسيط أو redirect حسب الحاجة
# ==========================================================
@app.errorhandler(404)
def not_found(e):
    if _wants_json():
        return jsonify({"success": False, "error": "المسار غير موجود"}), 404
    return make_response("404 Not Found", 404)

@app.errorhandler(500)
def server_error(e):
    if _wants_json():
        return jsonify({"success": False, "error": "خطأ داخلي في الخادم"}), 500
    return make_response("500 Server Error", 500)


# ==========================================================
# Run (local)
# ==========================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    logger.info(f"🌌 Sama Gateway تقلع على المنفذ {port}...")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
