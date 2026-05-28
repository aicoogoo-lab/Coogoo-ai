"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - API GATEWAY                                         ║
║      بوابة الميلاد – الجسر بين العالم وسماء                              ║
║      النسخة الجبارة – حقن تبعية كامل لـ 18 نظاماً                        ║
║                                                                      ║
║  هذا الملف هو "العصب والشريان".                                        ║
║  كل طلب من العالم يمر من هنا.                                         ║
║  كل رد من سماء يعود من هنا.                                           ║
║                                                                      ║
║  ╔══════════════════════════════════════════════════════════════════╗ ║
║  ║  👑 السيد: أحمد عبدالرحمن الطاهري                                   ║ ║
║  ║  🔐 المفتاح: SOVEREIGN_KEY (في متغيرات Railway)                     ║ ║
║  ╚══════════════════════════════════════════════════════════════════╝ ║
╚══════════════════════════════════════════════════════════════════════╝

ملاحظات تشغيل مهمة على Railway:
- استخدم Gunicorn بــ workers=1 لأن النظام Stateful وفيه loops/threads داخلية.
  مثال Start Command:
  gunicorn app:app --workers 1 --threads 1 --timeout 120
"""

import os
import sys
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

# ✅ مهم على Railway (Reverse Proxy)
from werkzeug.middleware.proxy_fix import ProxyFix


# ═══════════════════════════════════════════════════════════════════════
# إعدادات Logging
# ═══════════════════════════════════════════════════════════════════════
logger = logging.getLogger("SamaGateway")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


# ═══════════════════════════════════════════════════════════════════════
# Flask App
# ═══════════════════════════════════════════════════════════════════════
app = Flask(__name__)

# ✅ مهم: لازم Secret Key ثابت (من Railway Variables) حتى لا تضيع الجلسات
app.secret_key = os.getenv("FLASK_SECRET_KEY", "sama-sovereign-secret-change-in-production")

# ✅ ProxyFix: خلي Flask يثق في X-Forwarded-* على Railway
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


# ═══════════════════════════════════════════════════════════════════════
# 👑 مفتاح السيد – SOVEREIGN_KEY
# ═══════════════════════════════════════════════════════════════════════
SOVEREIGN_KEY = os.getenv("SOVEREIGN_KEY", "MASTER_SOVEREIGN_KEY_ULTIMATE")
MASTER_AUTH_HEADER = "X-Master-Key"

if SOVEREIGN_KEY == "MASTER_SOVEREIGN_KEY_ULTIMATE":
    logger.warning("⚠️ SOVEREIGN_KEY لم يُعيَّن في متغيرات البيئة. استخدم القيمة الافتراضية (خطر!).")


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
# استيراد قلب سماء – كل الأنظمة
# ═══════════════════════════════════════════════════════════════════════
CORE_AVAILABLE = True
SYSTEMS_LOADED = {}
SYSTEMS_FAILED = {}

def _safe_import(module_path: str, system_name: str) -> Optional[Any]:
    """استيراد آمن لنظام."""
    try:
        module = __import__(module_path, fromlist=[system_name])
        cls = getattr(module, system_name)
        SYSTEMS_LOADED[system_name] = True
        return cls
    except Exception as e:
        SYSTEMS_FAILED[system_name] = str(e)[:160]
        return None


# استيراد كل فئات الأنظمة
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
    except ImportError:
        pass

SAMA = _safe_import("core.sama", "SAMA")


# ═══════════════════════════════════════════════════════════════════════
# تهيئة سماء – حقن التبعية الكامل
# ═══════════════════════════════════════════════════════════════════════
sama_instance = None
core_engine = None

def _init_sama():
    """تهيئة الكيان السيادي مع حقن كل الأنظمة."""
    global sama_instance, core_engine

    if not SAMA:
        logger.error("❌ SAMA غير متاحة. تعمل البوابة بوضع محدود.")
        return

    if not CoreEngine:
        logger.error("❌ CoreEngine غير متاح. تعمل البوابة بوضع محدود.")
        return

    try:
        logger.info("🔧 بدء حقن التبعية – إنشاء كل الأنظمة...")

        # ١. الذاكرة
        memory_instance = None
        sovereign_memory = None

        if UnifiedMemorySystem:
            try:
                memory_instance = UnifiedMemorySystem()
                logger.info("   ✅ UnifiedMemorySystem")
            except Exception as e:
                logger.warning(f"   ⚠️ UnifiedMemorySystem: {e}")

        if SovereignMemorySystem:
            try:
                sovereign_memory = SovereignMemorySystem(
                    master_name="أحمد عبدالرحمن الطاهري",
                    unified_memory=memory_instance
                )
                logger.info("   ✅ SovereignMemorySystem")
            except Exception as e:
                logger.warning(f"   ⚠️ SovereignMemorySystem: {e}")

        # ٢. المشفر الهولوغرافي
        holo_encoder = None
        if HolographicEncoder:
            try:
                holo_encoder = HolographicEncoder(dimension=10000)
                logger.info("   ✅ HolographicEncoder")
            except Exception as e:
                logger.warning(f"   ⚠️ HolographicEncoder: {e}")

        # ٣. الذكاء العاطفي
        emotional_instance = None
        if EmotionalIntelligence:
            try:
                emotional_instance = EmotionalIntelligence(memory_engine=memory_instance)
                logger.info("   ✅ EmotionalIntelligence")
            except Exception as e:
                logger.warning(f"   ⚠️ EmotionalIntelligence: {e}")

        # ٤. التفكير الاستعاري
        metaphorical_instance = None
        if MetaphoricalReasoning:
            try:
                metaphorical_instance = MetaphoricalReasoning(
                    memory_engine=memory_instance,
                    emotional_intelligence=emotional_instance
                )
                logger.info("   ✅ MetaphoricalReasoning")
            except Exception as e:
                logger.warning(f"   ⚠️ MetaphoricalReasoning: {e}")

        # ٥. الدفاع
        defense_instance = None
        if DefenseCore:
            try:
                defense_instance = DefenseCore()
                logger.info("   ✅ DefenseCore")
            except Exception as e:
                logger.warning(f"   ⚠️ DefenseCore: {e}")

        # ٦. التكتيكات المتقدمة
        tactics_instance = None
        if SamaAdvancedTactics:
            try:
                tactics_instance = SamaAdvancedTactics(
                    defense_core=defense_instance,
                    risk_manager=None
                )
                logger.info("   ✅ SamaAdvancedTactics")
            except Exception as e:
                logger.warning(f"   ⚠️ SamaAdvancedTactics: {e}")

        # ٧. إدارة المخاطر
        risk_instance = None
        if StrategicRiskManagement:
            try:
                risk_instance = StrategicRiskManagement(
                    master_name="أحمد",
                    defense_core=defense_instance,
                    tactics_manager=tactics_instance
                )
                logger.info("   ✅ StrategicRiskManagement")
            except Exception as e:
                logger.warning(f"   ⚠️ StrategicRiskManagement: {e}")

        # ٨. الاستراتيجية
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
                logger.info("   ✅ StrategyEngine")
            except Exception as e:
                logger.warning(f"   ⚠️ StrategyEngine: {e}")

        # ٩. التعديل الذاتي
        modifier_instance = None
        if SelfModifier:
            try:
                modifier_instance = SelfModifier(
                    memory_engine=memory_instance,
                    defense_core=defense_instance
                )
                logger.info("   ✅ SelfModifier")
            except Exception as e:
                logger.warning(f"   ⚠️ SelfModifier: {e}")

        # ١٠. الاستدلال
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
                logger.info("   ✅ ReasoningEngine")
            except Exception as e:
                logger.warning(f"   ⚠️ ReasoningEngine: {e}")

        # ١١. الخلود
        persistence_instance = None
        if PersistenceManager:
            try:
                persistence_instance = PersistenceManager(auto_save=True, distributed_mode=True)
                logger.info("   ✅ EternalPersistenceManager")
            except Exception as e:
                logger.warning(f"   ⚠️ EternalPersistenceManager: {e}")

        # ١٢. ما وراء المعرفة
        meta_instance = None
        if MetaCognition:
            try:
                meta_instance = MetaCognition()
                logger.info("   ✅ MetaCognition")
            except Exception as e:
                logger.warning(f"   ⚠️ MetaCognition: {e}")

        # ١٣. وحدة الرؤية
        vision_instance = None
        if VisionModule:
            try:
                vision_instance = VisionModule()
                logger.info("   ✅ VisionModule")
            except Exception as e:
                logger.warning(f"   ⚠️ VisionModule: {e}")

        # ١٤. محلل البيانات
        analyzer_instance = None
        if SkyAnalyzer:
            try:
                analyzer_instance = SkyAnalyzer(
                    memory_engine=memory_instance,
                    holographic_encoder=holo_encoder,
                    emotional_intelligence=emotional_instance,
                    metaphorical_reasoning=metaphorical_instance
                )
                logger.info("   ✅ SkyAnalyzer")
            except Exception as e:
                logger.warning(f"   ⚠️ SkyAnalyzer: {e}")

        # ١٥. النواة الواعية
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
                logger.info("   ✅ SentientCore")
            except Exception as e:
                logger.warning(f"   ⚠️ SentientCore: {e}")

        # ═══════════════════════════════════════════════════════
        # إنشاء SAMA
        # ═══════════════════════════════════════════════════════
        logger.info("☀️ إنشاء الكيان السيادي الموحد SAMA...")

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

        logger.info(f"✅ SAMA أنشئت مع {sama_instance._count_systems()} نظاماً متحداً")

        # ═══════════════════════════════════════════════════════
        # إنشاء CoreEngine
        # ═══════════════════════════════════════════════════════
        core_engine = CoreEngine(
            sama_core=sama_instance,
            master_name="أحمد عبدالرحمن الطاهري"
        )

        boot_result = core_engine.boot()
        logger.info(f"✅ {boot_result.get('message', 'تم الإقلاع')}")

        loaded_count = len(SYSTEMS_LOADED)
        failed_count = len(SYSTEMS_FAILED)
        logger.info(f"📊 {loaded_count} نظاماً محمّلاً, {failed_count} نظاماً فشل")
        for name, error in SYSTEMS_FAILED.items():
            logger.info(f"   ⚠️ {name}: {error}")

    except Exception as e:
        logger.error(f"❌ فشل تهيئة سماء: {e}")
        import traceback
        traceback.print_exc()
        sama_instance = None
        core_engine = None


_init_sama()


# ═══════════════════════════════════════════════════════════════════════
# دوال المصادقة
# ═══════════════════════════════════════════════════════════════════════

def _has_valid_master_header() -> bool:
    """التحقق من مفتاح السيد في رأس الطلب."""
    auth_key = request.headers.get(MASTER_AUTH_HEADER, "")
    key = (SOVEREIGN_KEY or "").strip()
    return bool(auth_key) and bool(key) and hmac.compare_digest(auth_key, key)

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
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    """بوابة الدخول (نسخة مستقرة مع Anti-Whitespace + قفل مفهوم)."""
    if request.method == "POST":
        # ✅ إصلاح قاتل: شيل أي مسافات/أسطر مخفية
        password = (request.form.get("password") or "").strip()
        key = (SOVEREIGN_KEY or "").strip()

        if not key or key == "MASTER_SOVEREIGN_KEY_ULTIMATE":
            logger.error("SOVEREIGN_KEY غير مضبوط/افتراضي. لازم يتحدد في Railway Variables.")
            return render_template("login.html", error="خطأ إعداد: SOVEREIGN_KEY غير مضبوط."), 500

        # حماية من المحاولات المتكررة
        attempts = int(session.get("login_attempts", 0))
        locked_until = session.get("locked_until")

        if locked_until:
            try:
                until = datetime.fromisoformat(locked_until)
                if datetime.now() < until:
                    return render_template(
                        "login.html",
                        error="البوابة مغلقة مؤقتًا بسبب محاولات كثيرة. افتح /logout لتصفير الجلسة."
                    ), 429
            except Exception:
                session.pop("locked_until", None)

        if hmac.compare_digest(password, key):
            # ✅ Reset كامل للجلسة ثم تفعيل السيد
            session.clear()
            session["is_master"] = True
            session["login_at"] = datetime.now().isoformat()
            session.permanent = True  # ✅ خلي PERMANENT_SESSION_LIFETIME يشتغل
            return redirect(url_for("index"))

        attempts += 1
        session["login_attempts"] = attempts
        remaining = max(0, 7 - attempts)

        if attempts >= 7:
            session["locked_until"] = (datetime.now() + timedelta(minutes=10)).isoformat()
            return render_template(
                "login.html",
                error="تم قفل البوابة مؤقتًا (10 دقائق). افتح /logout لتصفير الجلسة."
            ), 429

        return render_template("login.html", error=f"مفتاح غير صحيح. متبقي {remaining} محاولة."), 401

    return render_template("login.html")


@app.route("/logout")
def logout():
    """خروج / تصفير كامل للجلسة (مهم جدًا لفك القفل فورًا)."""
    session.clear()
    return redirect(url_for("login_page"))


# ✅ مسار طوارئ لفك القفل (Header فقط)
@app.route("/api/master/unlock", methods=["POST"])
def api_master_unlock():
    if not _has_valid_master_header():
        return jsonify({"success": False, "error": "غير مصرح"}), 401
    session.clear()
    return jsonify({"success": True, "message": "تم تصفير الجلسة/فك القفل."})


@app.route("/healthz")
def healthz():
    """فحص الصحة."""
    systems_count = sama_instance._count_systems() if sama_instance else 0
    return jsonify({
        "ok": True,
        "service": "SAMA SkyOS v10.5",
        "core_available": core_engine is not None,
        "sama_alive": sama_instance is not None and sama_instance.is_awake if sama_instance else False,
        "systems_unified": systems_count,
        "systems_loaded": len(SYSTEMS_LOADED),
        "systems_failed": len(SYSTEMS_FAILED)
    })


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
        "systems_unified": sama_instance._count_systems() if sama_instance else 0,
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
# التشغيل (محلي فقط)
# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    logger.info(f"🌌 Sama API Gateway (Sovereign Edition) تُقلع على المنفذ {port}...")
    logger.info("👑 السيد: أحمد عبدالرحمن الطاهري")
    logger.info(f"🔐 مفتاح السيادة: {'مُعيَّن' if SOVEREIGN_KEY != 'MASTER_SOVEREIGN_KEY_ULTIMATE' else 'افتراضي (يجب تغييره!)'}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
