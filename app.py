# ==========================================================
# SAMA - API GATEWAY (SkyOS v10)
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
    redirect, url_for, session
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

# Secret Key
app.secret_key = os.getenv("FLASK_SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")

# Reverse Proxy trust
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
cookie_secure = (os.getenv("COOKIE_SECURE", "1") == "1")
cookie_samesite = os.getenv("COOKIE_SAMESITE", "Lax")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=cookie_secure,
    SESSION_COOKIE_SAMESITE=cookie_samesite,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=int(os.getenv("SESSION_MINUTES", "45"))),
)

# ---------------------------
# Helpers
# ---------------------------
def _wants_json() -> bool:
    accept = (request.headers.get("Accept", "") or "").lower()
    xrw = (request.headers.get("X-Requested-With", "") or "").lower()
    ctype = (request.headers.get("Content-Type", "") or "").lower()
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
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("is_master"):
            return f(*args, **kwargs)
        if _has_valid_master_header():
            return f(*args, **kwargs)

        if _wants_json():
            return jsonify({"success": False, "error": "غير مصرح. سجّل الدخول أو استخدم X-Master-Key."}), 401

        return redirect(url_for("login_page"))
    return decorated


# ==========================================================
# Safe import systems
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
        logger.warning(f"⚠️ فشل استيراد {system_name}: {e}")
        return None


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

        holo_encoder = None
        if HolographicEncoder:
            try:
                holo_encoder = HolographicEncoder(dimension=10000)
                logger.info("✅ HolographicEncoder")
            except Exception as e:
                logger.warning(f"⚠️ HolographicEncoder: {e}")

        emotional_instance = None
        if EmotionalIntelligence:
            try:
                emotional_instance = EmotionalIntelligence(memory_engine=memory_instance)
                logger.info("✅ EmotionalIntelligence")
            except Exception as e:
                logger.warning(f"⚠️ EmotionalIntelligence: {e}")

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

        defense_instance = None
        if DefenseCore:
            try:
                defense_instance = DefenseCore()
                logger.info("✅ DefenseCore")
            except Exception as e:
                logger.warning(f"⚠️ DefenseCore: {e}")

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

        persistence_instance = None
        if PersistenceManager:
            try:
                persistence_instance = PersistenceManager(auto_save=True, distributed_mode=True)
                logger.info("✅ EternalPersistenceManager")
            except Exception as e:
                logger.warning(f"⚠️ EternalPersistenceManager: {e}")

        meta_instance = None
        if MetaCognition:
            try:
                meta_instance = MetaCognition()
                logger.info("✅ MetaCognition")
            except Exception as e:
                logger.warning(f"⚠️ MetaCognition: {e}")

        vision_instance = None
        if VisionModule:
            try:
                vision_instance = VisionModule()
                logger.info("✅ VisionModule")
            except Exception as e:
                logger.warning(f"⚠️ VisionModule: {e}")

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

        logger.info("☀️ إنشاء SAMA...")
        sama = SAMA(
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

        logger.info("🧠 إنشاء CoreEngine...")
        engine = CoreEngine(
            sama_core=sama,
            master_name="أحمد عبدالرحمن الطاهري"
        )

        try:
            boot_result = engine.boot()
            logger.info(f"✅ {boot_result.get('message', 'تم الإقلاع')}")
        except Exception as e:
            logger.warning(f"⚠️ boot(): {e}")

        logger.info(f"📊 loaded={len(SYSTEMS_LOADED)} failed={len(SYSTEMS_FAILED)}")

        sama_instance = sama
        core_engine = engine

    except Exception as e:
        logger.error(f"❌ فشل تهيئة سماء: {e}")


_init_sama()

# ==========================================================
# Pages
# ==========================================================

@app.route("/")
@require_master
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        password = (request.form.get("password") or "").strip()
        key = (SOVEREIGN_KEY or "").strip()

        if not key:
            logger.error("SOVEREIGN_KEY غير مضبوط.")
            return render_template("login.html", error="خطأ إعداد: SOVEREIGN_KEY غير مضبوط."), 500

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


# واجهة السيّد (الجوال الخفيفة)
@app.route("/sovereign")
@require_master
def sovereign_mobile():
    return render_template("sovereign_mobile.html")


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


@app.route("/api/whoami", methods=["GET"])
def api_whoami():
    return jsonify({
        "is_master": bool(session.get("is_master")),
        "login_at": session.get("login_at"),
        "cookie_secure": app.config.get("SESSION_COOKIE_SECURE"),
        "cookie_samesite": app.config.get("SESSION_COOKIE_SAMESITE"),
    })


# ==========================================================
# API for SamaAPI (JSON ONLY)
# ==========================================================

def _core_command(kind: str, payload: dict) -> dict:
    if not core_engine:
        return {"success": False, "error": "المحرك المركزي غير متاح"}
    try:
        if RequestType and hasattr(core_engine, "handle_request"):
            rt = getattr(RequestType, kind.upper(), None)
            if rt is not None:
                return core_engine.handle_request(rt, payload)
        # fallback عام
        if hasattr(core_engine, "handle_command"):
            return core_engine.handle_command(kind, payload)
        return {"success": False, "error": "لا يوجد معالج أوامر مناسب في CoreEngine"}
    except Exception as e:
        logger.error(f"❌ خطأ في _core_command({kind}): {e}")
        return {"success": False, "error": f"خطأ داخلي: {e}"}


@app.route("/command", methods=["POST"])
@require_master
def command():
    payload = request.get_json(silent=True) or {}
    command_text = (payload.get("command") or payload.get("text") or "").strip()
    session_id = payload.get("session_id")
    context = payload.get("context", {})

    if not command_text:
        return jsonify({"success": False, "error": "لا يوجد أمر"}), 400

    result = _core_command("command", {
        "command": command_text,
        "session_id": session_id,
        "context": context
    })
    return jsonify(result)


# توافق مع النسخة القديمة /api/command
@app.route("/api/command", methods=["POST"])
@require_master
def api_command():
    return command()


@app.route("/master/command", methods=["POST"])
@require_master
def master_command():
    payload = request.get_json(silent=True) or {}
    cmd = (payload.get("command") or "").strip()
    params = {k: v for k, v in payload.items() if k != "command"}

    if not cmd:
        return jsonify({"success": False, "error": "لا يوجد أمر سيادي"}), 400

    result = _core_command("master", {
        "command": cmd,
        "params": params
    })
    return jsonify(result)


@app.route("/master/full-status", methods=["GET"])
@require_master
def master_full_status():
    result = _core_command("full_status", {})
    return jsonify(result)


@app.route("/awaken", methods=["POST"])
@require_master
def awaken():
    result = _core_command("awaken", {})
    return jsonify(result)


@app.route("/shutdown", methods=["POST"])
@require_master
def shutdown():
    result = _core_command("shutdown", {})
    return jsonify(result)


@app.route("/master/protect", methods=["POST"])
@require_master
def master_protect():
    result = _core_command("protect_master", {})
    return jsonify(result)


@app.route("/reason", methods=["POST"])
@require_master
def reason():
    payload = request.get_json(silent=True) or {}
    result = _core_command("reason", {"evidence": payload})
    return jsonify(result)


@app.route("/analyze-image", methods=["POST"])
@require_master
def analyze_image():
    payload = request.get_json(silent=True) or {}
    image_path = payload.get("image_path")
    result = _core_command("analyze_image", {"image_path": image_path})
    return jsonify(result)


@app.route("/analyze-url", methods=["POST"])
@require_master
def analyze_url():
    payload = request.get_json(silent=True) or {}
    url = payload.get("url")
    result = _core_command("analyze_url", {"url": url})
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
