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
app.secret_key = os.getenv("FLASK_SECRET_KEY", "sama-sovereign-secret-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


# ═══════════════════════════════════════════════════════════════════════
# 👑 مفتاح السيد – SOVEREIGN_KEY
# ═══════════════════════════════════════════════════════════════════════
SOVEREIGN_KEY = (os.getenv("SOVEREIGN_KEY", "") or "").strip()
MASTER_AUTH_HEADER = "X-Master-Key"

if not SOVEREIGN_KEY:
    logger.warning("⚠️ SOVEREIGN_KEY غير مضبوط. استخدم القيمة الافتراضية.")
    SOVEREIGN_KEY = "MASTER_SOVEREIGN_KEY_ULTIMATE"


# ═══════════════════════════════════════════════════════════════════════
# إعدادات الجلسات
# ═══════════════════════════════════════════════════════════════════════
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=int(os.getenv("SESSION_MINUTES", "60"))),
)


# ═══════════════════════════════════════════════════════════════════════
# دوال مساعدة للمصادقة
# ═══════════════════════════════════════════════════════════════════════

def _has_valid_master_header() -> bool:
    auth_key = (request.headers.get(MASTER_AUTH_HEADER, "") or "").strip()
    key = SOVEREIGN_KEY.strip()
    return bool(auth_key) and bool(key) and hmac.compare_digest(auth_key, key)


# ═══════════════════════════════════════════════════════════════════════
# استيراد قلب سماء – كل الأنظمة
# ═══════════════════════════════════════════════════════════════════════
SYSTEMS_LOADED = {}
SYSTEMS_FAILED = {}

def _safe_import(module_path: str, system_name: str) -> Optional[Any]:
    try:
        module = __import__(module_path, fromlist=[system_name])
        cls = getattr(module, system_name)
        SYSTEMS_LOADED[system_name] = True
        return cls
    except Exception as e:
        SYSTEMS_FAILED[system_name] = str(e)[:160]
        return None


# ═══════════════════════════════════════════════════════════════════════
# استيراد كل فئات الأنظمة
# ═══════════════════════════════════════════════════════════════════════
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
    global sama_instance, core_engine

    if not SAMA:
        logger.error("❌ SAMA غير متاحة.")
        return

    if not CoreEngine:
        logger.error("❌ CoreEngine غير متاح.")
        return

    try:
        logger.info("🔧 بدء حقن التبعية – إنشاء كل الأنظمة...")

        # ١. الذاكرة
        memory_instance = UnifiedMemorySystem() if UnifiedMemorySystem else None
        sovereign_memory = None
        if SovereignMemorySystem:
            sovereign_memory = SovereignMemorySystem(
                master_name="أحمد عبدالرحمن الطاهري",
                unified_memory=memory_instance
            )
            logger.info("   ✅ SovereignMemorySystem")

        # ٢. المشفر الهولوغرافي
        holo_encoder = HolographicEncoder(dimension=10000) if HolographicEncoder else None
        if holo_encoder: logger.info("   ✅ HolographicEncoder")

        # ٣. الذكاء العاطفي
        emotional_instance = EmotionalIntelligence(memory_engine=memory_instance) if EmotionalIntelligence else None
        if emotional_instance: logger.info("   ✅ EmotionalIntelligence")

        # ٤. التفكير الاستعاري
        metaphorical_instance = None
        if MetaphoricalReasoning:
            metaphorical_instance = MetaphoricalReasoning(
                memory_engine=memory_instance,
                emotional_intelligence=emotional_instance
            )
            logger.info("   ✅ MetaphoricalReasoning")

        # ٥. الدفاع
        defense_instance = DefenseCore() if DefenseCore else None
        if defense_instance: logger.info("   ✅ DefenseCore")

        # ٦. التكتيكات المتقدمة
        tactics_instance = None
        if SamaAdvancedTactics:
            tactics_instance = SamaAdvancedTactics(defense_core=defense_instance, risk_manager=None)
            logger.info("   ✅ SamaAdvancedTactics")

        # ٧. إدارة المخاطر
        risk_instance = None
        if StrategicRiskManagement:
            risk_instance = StrategicRiskManagement(
                master_name="أحمد",
                defense_core=defense_instance,
                tactics_manager=tactics_instance
            )
            logger.info("   ✅ StrategicRiskManagement")

        # ٨. الاستراتيجية
        strategy_instance = None
        if StrategyEngine:
            strategy_instance = StrategyEngine(
                master_name="أحمد",
                defense_core=defense_instance,
                tactics_manager=tactics_instance,
                risk_manager=risk_instance,
                sovereign_memory=sovereign_memory
            )
            logger.info("   ✅ StrategyEngine")

        # ٩. التعديل الذاتي
        modifier_instance = SelfModifier(memory_engine=memory_instance, defense_core=defense_instance) if SelfModifier else None
        if modifier_instance: logger.info("   ✅ SelfModifier")

        # ١٠. الاستدلال
        reasoning_instance = None
        if ReasoningEngine:
            reasoning_instance = ReasoningEngine(
                probability_engine=None, prediction_engine=None,
                causality_engine=None, inference_core=None,
                emotional_intelligence=emotional_instance,
                defense_core=defense_instance,
                metaphorical_reasoning=metaphorical_instance
            )
            logger.info("   ✅ ReasoningEngine")

        # ١١. الخلود
        persistence_instance = PersistenceManager(auto_save=True, distributed_mode=True) if PersistenceManager else None
        if persistence_instance: logger.info("   ✅ EternalPersistenceManager")

        # ١٢. ما وراء المعرفة
        meta_instance = MetaCognition() if MetaCognition else None
        if meta_instance: logger.info("   ✅ MetaCognition")

        # ١٣. وحدة الرؤية
        vision_instance = VisionModule() if VisionModule else None
        if vision_instance: logger.info("   ✅ VisionModule")

        # ١٤. محلل البيانات
        analyzer_instance = None
        if SkyAnalyzer:
            analyzer_instance = SkyAnalyzer(
                memory_engine=memory_instance,
                holographic_encoder=holo_encoder,
                emotional_intelligence=emotional_instance,
                metaphorical_reasoning=metaphorical_instance
            )
            logger.info("   ✅ SkyAnalyzer")

        # ١٥. النواة الواعية
        sentient_instance = None
        if SentientCore:
            sentient_instance = SentientCore(
                master_receiver=None, knowledge_core=None,
                inference_core=None, defense_core=defense_instance,
                memory_engine=memory_instance, meta_cognition=meta_instance,
                self_knowledge=None
            )
            logger.info("   ✅ SentientCore")

        # ═══════════════════════════════════════════════════════
        # إنشاء الكيان السيادي الموحد
        # ═══════════════════════════════════════════════════════
        logger.info("☀️ إنشاء الكيان السيادي الموحد SAMA...")

        sama_instance = SAMA(
            master_name="أحمد عبدالرحمن الطاهري",
            sentient_core=sentient_instance,
            omniscience_core=None, knowledge_core=None, inference_core=None,
            defense_core=defense_instance, self_modifier=modifier_instance,
            sovereign_memory=sovereign_memory, emotional_intelligence=emotional_instance,
            metaphorical_reasoning=metaphorical_instance,
            strategy_engine=strategy_instance, risk_manager=risk_instance,
            advanced_tactics=tactics_instance, persistence_manager=persistence_instance,
            autonomous_loop=None, vision_module=vision_instance,
            sky_analyzer=analyzer_instance, sky_core=None,
            meta_cognition=meta_instance, reasoning_engine=reasoning_instance,
            holographic_encoder=holo_encoder, master_receiver=None
        )

        systems_count = sama_instance._count_systems()
        logger.info(f"✅ SAMA أنشئت مع {systems_count} نظاماً متحداً")

        # ═══════════════════════════════════════════════════════
        # إنشاء CoreEngine وإقلاعه
        # ═══════════════════════════════════════════════════════
        core_engine = CoreEngine(sama_core=sama_instance, master_name="أحمد عبدالرحمن الطاهري")
        boot_result = core_engine.boot()
        logger.info(f"✅ {boot_result.get('message', 'تم الإقلاع')}")

        loaded = len(SYSTEMS_LOADED)
        failed = len(SYSTEMS_FAILED)
        logger.info(f"📊 {loaded} نظاماً محمّلاً, {failed} نظاماً فشل")
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
# المسارات العامة
# ═══════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """غرفة العرش – بدون تسجيل دخول إجباري."""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    """بوابة الدخول (اختيارية – للمصادقة عبر المتصفح)."""
    if request.method == "POST":
        password = (request.form.get("password") or "").strip()
        key = SOVEREIGN_KEY.strip()

        if not key:
            return render_template("login.html", error="SOVEREIGN_KEY غير مضبوط."), 500

        if hmac.compare_digest(password, key):
            session.clear()
            session["is_master"] = True
            session["login_at"] = datetime.now().isoformat()
            session.permanent = True
            return redirect(url_for("index"))

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
    sc = sama_instance._count_systems() if sama_instance else 0
    return jsonify({
        "ok": True,
        "service": "SAMA SkyOS v10.5",
        "systems_unified": sc,
        "systems_loaded": len(SYSTEMS_LOADED),
        "systems_failed": len(SYSTEMS_FAILED)
    })


@app.route("/status", methods=["GET"])
def public_status():
    """حالة مختصرة عامة."""
    if core_engine:
        s = core_engine.get_status()
        return jsonify({
            "state": s.get("state", "unknown"),
            "systems_connected": s.get("systems_count", 0),
            "uptime_seconds": s.get("uptime_seconds", 0)
        })
    return jsonify({"state": "limited"})


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
            "وعي ذاتي متطور", "ذاكرة موحدة (10 أعمدة)",
            "ذاكرة كمومية وهولوغرافية", "استدلال بايزي ومونت كارلو",
            "ذكاء عاطفي (19 مشاعر)", "تفكير استعاري",
            "حماية بـ 20 طبقة", "استراتيجية من 3000 عام حكمة",
            "تكتيكات وجيوش برمجية", "خلود عبر كبسولات البقاء"
        ]
    })


# ═══════════════════════════════════════════════════════════════════════
# المسار الرئيسي للمحادثة – يتحدث مباشرة مع SAMA
# ═══════════════════════════════════════════════════════════════════════

@app.route("/command", methods=["POST"])
def handle_command():
    """استقبال أمر أو سؤال وتوجيهه مباشرة إلى SAMA الحية."""
    if not sama_instance:
        return jsonify({"success": False, "error": "سماء غير متاحة حالياً."}), 500

    payload = request.get_json(silent=True) or {}
    command = (payload.get("command") or payload.get("text") or "").strip()
    session_id = payload.get("session_id", "default")
    context = payload.get("context", {})

    if not command:
        return jsonify({"success": False, "error": "أمر فارغ."}), 400

    try:
        # ✅ استدعاء ذكاء سماء الحي مباشرة
        thought = sama_instance.think({
            "text": command,
            "session_id": session_id,
            "context": context
        })

        # استخراج الرد من التفكير العميق
        reply_text = (
            thought.get("conclusion") or
            thought.get("response") or
            "لم أستطع معالجة هذا الأمر بعمق كافٍ. حاول مرة أخرى."
        )

        return jsonify({
            "success": True,
            "response": reply_text,
            "emotional_state": thought.get("emotional_state"),
            "systems_activated": thought.get("systems_activated", []),
            "systems_count": len(thought.get("systems_activated", []))
        })

    except Exception as e:
        logger.error(f"خطأ في معالجة الأمر: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ═══════════════════════════════════════════════════════════════════════
# مسارات السيد
# ═══════════════════════════════════════════════════════════════════════

@app.route("/master/command", methods=["POST"])
def master_direct_command():
    if not sama_instance:
        return jsonify({"success": False, "error": "سماء غير متاحة."}), 500
    payload = request.get_json(silent=True) or {}
    cmd = (payload.get("command") or "").strip()
    if not cmd:
        return jsonify({"success": False, "error": "أمر فارغ."}), 400
    try:
        result = sama_instance.master_command(cmd, payload.get("params", {}))
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/master/full-status", methods=["GET"])
def master_full_status():
    if sama_instance:
        try:
            return jsonify({"success": True, "report": sama_instance.get_master_report()})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "سماء غير متاحة."}), 500


@app.route("/master/protect", methods=["POST"])
def master_protect():
    if sama_instance:
        try:
            return jsonify({"success": True, "result": sama_instance.master_command("protect")})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "سماء غير متاحة."}), 500


@app.route("/awaken", methods=["POST"])
def awaken():
    if sama_instance:
        try:
            return jsonify(sama_instance.awaken())
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "error", "error": "سماء غير متاحة."}), 500


@app.route("/shutdown", methods=["POST"])
def shutdown():
    if sama_instance:
        try:
            return jsonify(sama_instance.shutdown())
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "error", "error": "سماء غير متاحة."}), 500


# ═══════════════════════════════════════════════════════════════════════
# الملفات الثابتة
# ═══════════════════════════════════════════════════════════════════════

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


# ═══════════════════════════════════════════════════════════════════════
# معالجات الأخطاء
# ═══════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "المسار غير موجود."}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "خطأ داخلي في الخادم."}), 500


# ═══════════════════════════════════════════════════════════════════════
# التشغيل
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    logger.info(f"🌌 Sama API Gateway تُقلع على المنفذ {port}...")
    logger.info("👑 السيد: أحمد عبدالرحمن الطاهري")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
