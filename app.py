"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - API GATEWAY                                         ║
║      بوابة الميلاد – النسخة النهائية العاملة                             ║
║                                                                      ║
║  ╔══════════════════════════════════════════════════════════════════╗ ║
║  ║  👑 السيد: أحمد عبدالرحمن الطاهري                                   ║ ║
║  ║  🔐 المفتاح: SOVEREIGN_KEY (في متغيرات Railway)                     ║ ║
║  ╚══════════════════════════════════════════════════════════════════╝ ║
╚══════════════════════════════════════════════════════════════════════╝
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

logger = logging.getLogger("SamaGateway")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "sama-sovereign-secret-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

SOVEREIGN_KEY = (os.getenv("SOVEREIGN_KEY", "") or "").strip()
MASTER_AUTH_HEADER = "X-Master-Key"
if not SOVEREIGN_KEY:
    SOVEREIGN_KEY = "MASTER_SOVEREIGN_KEY_ULTIMATE"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=60),
)

SYSTEMS_LOADED = {}
SYSTEMS_FAILED = {}

def _safe_import(module_path, system_name):
    try:
        module = __import__(module_path, fromlist=[system_name])
        cls = getattr(module, system_name)
        SYSTEMS_LOADED[system_name] = True
        return cls
    except Exception as e:
        SYSTEMS_FAILED[system_name] = str(e)[:160]
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
CoreEngine = _safe_import("core.core_engine", "CoreEngine")
RequestType = None
if CoreEngine:
    try:
        from core.core_engine import RequestType as RT
        RequestType = RT
    except: pass
SAMA = _safe_import("core.sama", "SAMA")

sama_instance = None
core_engine = None

def _init_sama():
    global sama_instance, core_engine
    if not SAMA or not CoreEngine: return
    try:
        logger.info("🔧 بدء حقن التبعية...")
        mem = UnifiedMemorySystem() if UnifiedMemorySystem else None
        sov = SovereignMemorySystem(master_name="أحمد عبدالرحمن الطاهري", unified_memory=mem) if SovereignMemorySystem else None
        holo = HolographicEncoder(10000) if HolographicEncoder else None
        emo = EmotionalIntelligence(memory_engine=mem) if EmotionalIntelligence else None
        met = MetaphoricalReasoning(memory_engine=mem, emotional_intelligence=emo) if MetaphoricalReasoning else None
        defense = DefenseCore() if DefenseCore else None
        tactics = SamaAdvancedTactics(defense_core=defense, risk_manager=None) if SamaAdvancedTactics else None
        risk = StrategicRiskManagement(master_name="أحمد", defense_core=defense, tactics_manager=tactics) if StrategicRiskManagement else None
        strategy = StrategyEngine(master_name="أحمد", defense_core=defense, tactics_manager=tactics, risk_manager=risk, sovereign_memory=sov) if StrategyEngine else None
        modifier = SelfModifier(memory_engine=mem, defense_core=defense) if SelfModifier else None
        reasoning = ReasoningEngine(probability_engine=None, prediction_engine=None, causality_engine=None, inference_core=None, emotional_intelligence=emo, defense_core=defense, metaphorical_reasoning=met) if ReasoningEngine else None
        persistence = PersistenceManager(auto_save=True, distributed_mode=True) if PersistenceManager else None
        meta = MetaCognition() if MetaCognition else None
        vision = VisionModule() if VisionModule else None
        analyzer = SkyAnalyzer(memory_engine=mem, holographic_encoder=holo, emotional_intelligence=emo, metaphorical_reasoning=met) if SkyAnalyzer else None
        sentient = SentientCore(master_receiver=None, knowledge_core=None, inference_core=None, defense_core=defense, memory_engine=mem, meta_cognition=meta, self_knowledge=None) if SentientCore else None

        sama_instance = SAMA(
            master_name="أحمد عبدالرحمن الطاهري",
            sentient_core=sentient, omniscience_core=None, knowledge_core=None, inference_core=None,
            defense_core=defense, self_modifier=modifier, sovereign_memory=sov,
            emotional_intelligence=emo, metaphorical_reasoning=met,
            strategy_engine=strategy, risk_manager=risk, advanced_tactics=tactics,
            persistence_manager=persistence, autonomous_loop=None,
            vision_module=vision, sky_analyzer=analyzer, sky_core=None,
            meta_cognition=meta, reasoning_engine=reasoning, holographic_encoder=holo, master_receiver=None
        )
        logger.info(f"✅ SAMA بـ {sama_instance._count_systems()} نظام")

        core_engine = CoreEngine(sama_core=sama_instance, master_name="أحمد عبدالرحمن الطاهري")
        core_engine.boot()
        logger.info("✅ تم الإقلاع")
        logger.info(f"📊 {len(SYSTEMS_LOADED)} محمّل, {len(SYSTEMS_FAILED)} فشل")
        for n, e in SYSTEMS_FAILED.items(): logger.info(f"   ⚠️ {n}: {e}")
    except Exception as e:
        logger.error(f"❌ فشل تهيئة سماء: {e}")
        sama_instance = None; core_engine = None

_init_sama()

def _has_valid_master_header():
    auth_key = (request.headers.get(MASTER_AUTH_HEADER, "") or "").strip()
    return bool(auth_key) and hmac.compare_digest(auth_key, SOVEREIGN_KEY.strip())

# ================ الصفحات ================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        password = (request.form.get("password") or "").strip()
        key = SOVEREIGN_KEY.strip()
        if not key: return render_template("login.html", error="SOVEREIGN_KEY غير مضبوط"), 500
        if hmac.compare_digest(password, key):
            session.clear(); session["is_master"] = True; session["login_at"] = datetime.now().isoformat()
            session.permanent = True
            return redirect(url_for("index"))
        return render_template("login.html", error="مفتاح غير صحيح"), 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/healthz")
def healthz():
    sc = sama_instance._count_systems() if sama_instance else 0
    return jsonify({"ok": True, "service": "SAMA SkyOS v10.5", "systems_unified": sc})

@app.route("/status")
def public_status():
    if core_engine:
        s = core_engine.get_status()
        return jsonify({"state": s.get("state","unknown"), "systems_connected": s.get("systems_count",0), "uptime_seconds": s.get("uptime_seconds",0)})
    return jsonify({"state": "limited"})

@app.route("/info")
def public_info():
    return jsonify({"name": "سماء", "version": "v10.5-jabbar-eternal", "master": "أحمد عبدالرحمن الطاهري"})

# ================ API محمي ================
@app.route("/command", methods=["POST"])
def handle_command():
    if not core_engine: return jsonify({"success": False, "error": "CoreEngine غير متاح"}), 500
    payload = request.get_json(silent=True) or {}
    command = (payload.get("command") or payload.get("text") or "").strip()
    if not command: return jsonify({"success": False, "error": "أمر فارغ"}), 400
    try:
        result = core_engine.process_request(RequestType.QUERY if RequestType else None, command, session_id=payload.get("session_id"), context=payload.get("context", {}))
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/awaken", methods=["POST"])
def awaken():
    if sama_instance:
        try: return jsonify(sama_instance.awaken())
        except Exception as e: return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "error", "error": "سماء غير متاحة"}), 500

@app.route("/master/full-status")
def master_full_status():
    if sama_instance:
        try: return jsonify({"success": True, "report": sama_instance.get_master_report()})
        except Exception as e: return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "سماء غير متاحة"}), 500

@app.route("/master/command", methods=["POST"])
def master_direct_command():
    if not sama_instance: return jsonify({"success": False, "error": "سماء غير متاحة"}), 500
    payload = request.get_json(silent=True) or {}
    command = (payload.get("command") or "").strip()
    if not command: return jsonify({"success": False, "error": "أمر فارغ"}), 400
    try: return jsonify({"success": True, "result": sama_instance.master_command(command, payload.get("params", {}))})
    except Exception as e: return jsonify({"success": False, "error": str(e)}), 500

@app.route("/master/protect", methods=["POST"])
def master_protect():
    if sama_instance:
        try: return jsonify({"success": True, "result": sama_instance.master_command("protect")})
        except Exception as e: return jsonify({"success": False, "error": str(e)}), 500
    return jsonify({"success": False, "error": "سماء غير متاحة"}), 500

# ================ Static ================
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    logger.info(f"🌌 تُقلع على المنفذ {port}...")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
