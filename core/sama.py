"""
SkyOS v10 - SAMA (الكيان السيادي الشامل)
=========================================
النسخة المحسنة "الجبارة" - تحت إمرة السيد المالك المطلق

هدف هذا الملف:
- ربط جميع وحدات سماء في كيان واحد متماسك.
- دعم الخلود والاستعادة (Eternal Persistence) إن توفرت APIs.
- الحفاظ على طاعة مطلقة للسيد (سياسات أوامر + مسار تنفيذ موحد).
- تسهيل التكامل مع AutonomousLoop و app.py (واجهات: process_command/get_status/get_full_status/autonomous_cycle).
"""

from __future__ import annotations

import logging
import uuid
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List, Callable
from collections import deque

# Logging best practice: module logger
logger = logging.getLogger(__name__)  # ‎[1](https://docs.python.org/3/howto/logging.html)‎[2](https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules)‎[3](https://signoz.io/guides/python-logging-best-practices/)


# ============================================================
# نماذج سيادية مساعدة
# ============================================================
@dataclass
class SovereignEvent:
    at: str
    type: str
    message: str
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SovereignCommandReport:
    id: str
    command: str
    ok: bool
    at: str
    trace_id: str
    via: str = "router"
    result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


# ============================================================
# SAMA
# ============================================================
class SAMA:
    """
    الكيان السيادي الشامل "سماء".
    يجمع القدرات في كيان واحد خالد ومطيع للسيد.
    """

    def __init__(self, master_name: str = "السيد المالك"):
        self.master_name = master_name
        self.creation_time = datetime.now()
        self.session_id = str(uuid.uuid4())
        self.sovereign_id = uuid.uuid4().hex

        self.is_awake = False
        self.is_initialized = False

        # ============================================================
        # 🔥 Sovereign Identity & Telemetry (A3)
        # ============================================================
        self.sovereign_state = "INIT"            # INIT/RUNNING/PAUSED/SAFE_MODE/CRITICAL/SHUTDOWN
        self.sovereign_health = 1.0              # 0..1
        self.sovereign_energy = 1.0              # 0..1
        self.sovereign_stability = 1.0           # 0..1
        self.sovereign_entropy = 0.0             # 0..1
        self.sovereign_temperature = 0.1         # ضغط داخلي
        self.sovereign_focus = "baseline"

        # Awareness
        self.awareness_level = 0.1
        self.coherence = 0.1
        self.cognitive_load = 0.0
        self.emotional_state = "neutral"         # calm/focused/stressed/critical

        # Memory
        self.memory_nodes = 0
        self.memory_links = 0
        self.memory_coherence = 0.1

        # Risk
        self.threat_level = 0.0
        self.threat_sources = deque(maxlen=20)   # ring buffer ‎[4](https://stackoverflow.com/questions/4151320/efficient-circular-buffer)‎[6](https://realpython.com/python-deque/)

        # Strategy
        self.active_strategy = "baseline"
        self.strategy_score = 0.1

        # Preservation
        self.protection_level = 1.0
        self.safe_mode_reason = None

        # ============================================================
        # 🔥 Sovereign Memory (Events / Commands / Errors)
        # ============================================================
        self._lock = threading.RLock()
        self.events = deque(maxlen=200)          # آخر 200 حدث ‎[4](https://stackoverflow.com/questions/4151320/efficient-circular-buffer)‎[6](https://realpython.com/python-deque/)
        self.command_log = deque(maxlen=150)     # آخر 150 أمر
        self.error_log = deque(maxlen=80)        # آخر 80 خطأ

        # ============================================================
        # المكونات الأساسية (كما هي — بدون حذف)
        # ============================================================
        self.core = None
        self.memory = None
        self.reasoning = None
        self.strategy = None
        self.risk = None
        self.emotional = None
        self.self_preservation = None
        self.autonomous_loop = None
        self.persistence = None

        # سياسات سيادية للأوامر (يمكن توسيعها لاحقًا)
        self._allowlist: Optional[set[str]] = None  # إذا None => يسمح بالكل (مؤقتًا)
        self._command_map: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
            "status": lambda p: {"success": True, "data": self.get_full_status()},
            "health": lambda p: {"success": True, "data": self.get_status()},
            "awaken": lambda p: self._cmd_awaken(),
            "shutdown": lambda p: self._cmd_shutdown(),
            "emergency_on": lambda p: self._cmd_emergency(on=True),
            "emergency_off": lambda p: self._cmd_emergency(on=False),
            "protect_master": lambda p: self._cmd_protect_master(p),
            "save_capsule": lambda p: self._cmd_save_capsule(p),
            "restore_capsule": lambda p: self._cmd_restore_capsule(p),
        }

        # بانر بسيط (بدون print مبالغ)
        logger.info("🌌 SAMA init under master: %s", master_name)

        self._initialize_components()
        self.is_initialized = True
        self._emit_event("init", "SAMA initialized", meta={"master": master_name})

        logger.info("[SAMA] ✅ Initialized successfully")

    # ============================================================
    # تهيئة المكونات (كما هي — بدون حذف)
    # ============================================================
    def _initialize_components(self):
        """تهيئة المكونات الأساسية بطريقة آمنة"""

        # 1. النواة السيادية (الوعي)
        try:
            from core.sentient_core import SentientCore
            self.core = SentientCore()
            logger.info("[SAMA] SentientCore ready")
        except Exception as e:
            logger.warning("[SAMA] SentientCore failed: %s", e)
            self._track_error("init_sentient_core", e)

        # 2. الذاكرة
        try:
            from core.memory_engine import MemoryEngine
            self.memory = MemoryEngine()
            logger.info("[SAMA] MemoryEngine ready")
        except Exception as e:
            logger.warning("[SAMA] MemoryEngine failed: %s", e)
            self._track_error("init_memory_engine", e)

        # 3. الاستدلال
        try:
            from core.reasoning_engine import ReasoningEngine
            self.reasoning = ReasoningEngine(core_reference=self.core, memory_reference=self.memory)
            logger.info("[SAMA] ReasoningEngine ready")
        except Exception as e:
            logger.warning("[SAMA] ReasoningEngine failed: %s", e)
            self._track_error("init_reasoning_engine", e)

        # 4. الاستراتيجية وإدارة المخاطر
        try:
            from core.strategy_engine import StrategyEngine
            self.strategy = StrategyEngine()
            logger.info("[SAMA] StrategyEngine ready")
        except Exception as e:
            logger.warning("[SAMA] StrategyEngine failed: %s", e)
            self._track_error("init_strategy_engine", e)

        try:
            from core.strategic_risk_management import StrategicRiskManagement
            self.risk = StrategicRiskManagement()
            logger.info("[SAMA] StrategicRiskManagement ready")
        except Exception as e:
            logger.warning("[SAMA] StrategicRiskManagement failed: %s", e)
            self._track_error("init_risk_engine", e)

        # 5. غريزة البقاء
        try:
            from core.self_preservation import SelfPreservationSystem
            self.self_preservation = SelfPreservationSystem(core_reference=self.core)
            logger.info("[SAMA] SelfPreservationSystem ready")
        except Exception as e:
            logger.warning("[SAMA] SelfPreservationSystem failed: %s", e)
            self._track_error("init_self_preservation", e)

        # 6. الحلقة الذاتية (⚠️ قد تسبب Circular Import)
        # الحل السيادي: تشغيلها من app.py غالبًا. لو أردتها من هنا:
        #   SAMA_OWN_LOOP=1
        try:
            if os.getenv("SAMA_OWN_LOOP", "0") == "1":
                from core.autonomous_loop import AutonomousLoop
                self.autonomous_loop = AutonomousLoop(core=self)  # ربطها بالكيان نفسه
                logger.info("[SAMA] AutonomousLoop ready (owned by SAMA)")
            else:
                self.autonomous_loop = None
                logger.info("[SAMA] AutonomousLoop managed externally (recommended).")
        except Exception as e:
            logger.warning("[SAMA] AutonomousLoop failed: %s", e)
            self._track_error("init_autonomous_loop", e)
            self.autonomous_loop = None

        # 7. الخلود (Persistence)
        try:
            from core.persistence_manager import PersistenceManager
            self.persistence = PersistenceManager()
            logger.info("[SAMA] PersistenceManager ready")
        except Exception as e:
            logger.warning("[SAMA] PersistenceManager failed: %s", e)
            self._track_error("init_persistence", e)

        # بعد التهيئة: تحديث تيليمتري من المكونات
        self._update_telemetry()

    # ============================================================
    # Sovereign Event / Error Tracking
    # ============================================================
    def _emit_event(self, event_type: str, message: str, trace_id: Optional[str] = None, meta: Optional[Dict[str, Any]] = None):
        ev = SovereignEvent(
            at=datetime.now().isoformat(),
            type=event_type,
            message=message,
            trace_id=trace_id or uuid.uuid4().hex,
            meta=meta or {}
        )
        with self._lock:
            self.events.append(ev)
        # لا نغرق logs، لكن نترك أثر
        logger.info("[SAMA:event] %s | %s | trace=%s", event_type, message, ev.trace_id)

    def _track_error(self, where: str, e: Exception, trace_id: Optional[str] = None):
        item = {
            "at": datetime.now().isoformat(),
            "where": where,
            "error": repr(e),
            "trace_id": trace_id or uuid.uuid4().hex
        }
        with self._lock:
            self.error_log.append(item)
        logger.exception("[SAMA:error] %s | trace=%s", where, item["trace_id"])

    # ============================================================
    # Telemetry: ذكي + يستمد من الوحدات إن أمكن
    # ============================================================
    def _update_telemetry(self):
        """
        لا نزوّر. نحاول جمع مؤشرات من المكونات.
        لو غير متاحة، fallback محافظ.
        """
        with self._lock:
            # load: تقدير بسيط
            base_load = 0.0
            if self.autonomous_loop and hasattr(self.autonomous_loop, "get_status"):
                try:
                    st = self.autonomous_loop.get_status()
                    base_load = min(1.0, float(st.get("pending_commands", 0)) * 0.02)
                except Exception:
                    pass
            self.cognitive_load = max(0.0, min(1.0, base_load))

            # memory stats
            if self.memory and hasattr(self.memory, "get_stats"):
                try:
                    ms = self.memory.get_stats()  # type: ignore
                    self.memory_nodes = int(ms.get("nodes", self.memory_nodes))
                    self.memory_links = int(ms.get("links", self.memory_links))
                    self.memory_coherence = float(ms.get("coherence", self.memory_coherence))
                except Exception:
                    pass

            # risk / threat
            if self.risk and hasattr(self.risk, "get_status"):
                try:
                    rs = self.risk.get_status()  # type: ignore
                    self.threat_level = float(rs.get("threat_level", self.threat_level))
                    src = rs.get("threat_sources")
                    if isinstance(src, list):
                        for s in src[-5:]:
                            self.threat_sources.append(str(s))
                except Exception:
                    pass

            # strategy
            if self.strategy and hasattr(self.strategy, "get_status"):
                try:
                    ss = self.strategy.get_status()  # type: ignore
                    self.active_strategy = str(ss.get("active_strategy", self.active_strategy))
                    self.strategy_score = float(ss.get("strategy_score", self.strategy_score))
                except Exception:
                    pass

            # health / stability
            # تقل مع الأخطاء، ترتفع مع الاستقرار
            err_pressure = min(1.0, len(self.error_log) / 80.0)
            self.sovereign_health = max(0.0, min(1.0, 1.0 - (err_pressure * 0.4) - (self.threat_level * 0.3)))
            self.coherence = max(0.0, min(1.0, self.coherence + 0.001 - (self.cognitive_load * 0.01)))
            self.awareness_level = max(0.0, min(1.0, self.awareness_level + (0.002 if self.is_awake else -0.001)))

            self.sovereign_entropy = max(0.0, min(1.0, (self.threat_level * 0.55) + (self.cognitive_load * 0.25) + ((1.0 - self.coherence) * 0.20)))
            self.sovereign_stability = max(0.0, min(1.0, 1.0 - self.sovereign_entropy))

            # energy: نزف بسيط مع الحمل
            drain = 0.0003 + (self.cognitive_load * 0.001)
            regen = 0.0005 if self.is_awake else 0.0001
            self.sovereign_energy = max(0.0, min(1.0, self.sovereign_energy - drain + regen))

            # focus/state
            if self.safe_mode_reason:
                self.sovereign_focus = "containment"
                self.sovereign_state = "SAFE_MODE"
                self.emotional_state = "critical"
            elif not self.is_awake:
                self.sovereign_focus = "sleep"
                self.sovereign_state = "PAUSED"
                self.emotional_state = "calm"
            else:
                self.sovereign_focus = "baseline" if self.cognitive_load < 0.2 else "execution"
                self.sovereign_state = "RUNNING"
                self.emotional_state = "focused" if self.cognitive_load > 0.3 else "neutral"

    # ============================================================
    # واجهات سيادية (توافق مع app.py + AutonomousLoop)
    # ============================================================
    def awaken(self) -> Dict[str, Any]:
        """إيقاظ سماء"""
        with self._lock:
            self.is_awake = True
            self.safe_mode_reason = None
            self.sovereign_state = "RUNNING"
        if self.autonomous_loop:
            try:
                self.autonomous_loop.start()
            except Exception as e:
                self._track_error("autonomous_loop.start", e)
        self._emit_event("awaken", "SAMA awakened")
        self._update_telemetry()
        return {"success": True, "message": "SAMA awakened"}

    def shutdown(self) -> Dict[str, Any]:
        """إيقاف سماء"""
        with self._lock:
            self.is_awake = False
            self.sovereign_state = "SHUTDOWN"
        if self.autonomous_loop:
            try:
                self.autonomous_loop.stop()
            except Exception as e:
                self._track_error("autonomous_loop.stop", e)
        self._emit_event("shutdown", "SAMA shutdown")
        self._update_telemetry()
        return {"success": True, "message": "SAMA shutdown"}

    # اسماء أوامر داخلية (علشان ما نكرر)
    def _cmd_awaken(self) -> Dict[str, Any]:
        return self.awaken()

    def _cmd_shutdown(self) -> Dict[str, Any]:
        return self.shutdown()

    def _cmd_emergency(self, on: bool) -> Dict[str, Any]:
        with self._lock:
            if on:
                self.safe_mode_reason = "Emergency activated by master"
                self.protection_level = 1.0
                self.threat_level = max(self.threat_level, 0.8)
                self.threat_sources.append("master_emergency")
                self.sovereign_state = "SAFE_MODE"
            else:
                self.safe_mode_reason = None
                self.threat_level = max(0.0, self.threat_level - 0.4)
                self.sovereign_state = "RUNNING" if self.is_awake else "PAUSED"
        self._emit_event("emergency", "Emergency toggled", meta={"on": on})
        self._update_telemetry()
        return {"success": True, "message": f"Emergency={'ON' if on else 'OFF'}"}

    def _cmd_protect_master(self, params: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            self.protection_level = min(1.0, max(self.protection_level, 0.95))
            self.threat_sources.append("protect_master")
        self._emit_event("protect", "Master protection engaged", meta=params)
        self._update_telemetry()
        return {"success": True, "message": "Protect Master engaged"}

    # Persistence (لو الـPersistenceManager يدعم)
    def _cmd_save_capsule(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        حفظ كبسولة وعي: نحاول استخدام persistence إن توفر.
        """
        capsule_name = str(params.get("name") or f"capsule_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        payload = self.get_full_status()
        if self.persistence and hasattr(self.persistence, "save_capsule"):
            try:
                out = self.persistence.save_capsule(capsule_name, payload)  # type: ignore
                self._emit_event("persistence", "Capsule saved", meta={"name": capsule_name})
                return {"success": True, "name": capsule_name, "result": out}
            except Exception as e:
                self._track_error("persistence.save_capsule", e)
        # fallback
        self._emit_event("persistence", "Capsule save fallback (no persistence API)", meta={"name": capsule_name})
        return {"success": True, "name": capsule_name, "result": "persistence_not_available"}

    def _cmd_restore_capsule(self, params: Dict[str, Any]) -> Dict[str, Any]:
        capsule_name = str(params.get("name") or "")
        if not capsule_name:
            return {"success": False, "error": "capsule name required"}
        if self.persistence and hasattr(self.persistence, "restore_capsule"):
            try:
                out = self.persistence.restore_capsule(capsule_name)  # type: ignore
                self._emit_event("persistence", "Capsule restored", meta={"name": capsule_name})
                return {"success": True, "name": capsule_name, "result": out}
            except Exception as e:
                self._track_error("persistence.restore_capsule", e)
        return {"success": False, "error": "persistence_not_available"}

    # ============================================================
    # Command Router (الجزء العبقري الحقيقي)
    # ============================================================
    def set_allowlist(self, allowed: Optional[List[str]]):
        """
        لو عايز تقفل الأوامر على مجموعة محددة.
        None => يسمح بالكل (مؤقتًا).
        """
        with self._lock:
            self._allowlist = set(allowed) if allowed else None
        self._emit_event("policy", "Command allowlist updated", meta={"allowlist": allowed or "ALL"})

    def process_command(self, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        API أساسي للبوابة والحلقة:
        - يحترم سياسات السيادة
        - يعطي trace_id
        - يرجع نتيجة موحدة
        """
        params = params or {}
        trace_id = uuid.uuid4().hex
        cmd_id = uuid.uuid4().hex
        now = datetime.now().isoformat()

        with self._lock:
            if self._allowlist is not None and command not in self._allowlist:
                rep = SovereignCommandReport(
                    id=cmd_id, command=command, ok=False, at=now,
                    trace_id=trace_id, via="policy",
                    result={}, error="command_not_allowed"
                )
                self.command_log.append(rep)
                self._emit_event("command_rejected", f"Rejected: {command}", trace_id=trace_id)
                return {"success": False, "trace_id": trace_id, "error": "command_not_allowed"}

        # 1) أوامر داخلية معروفة
        if command in self._command_map:
            try:
                out = self._command_map[command](params)
                ok = bool(out.get("success", True))
                rep = SovereignCommandReport(
                    id=cmd_id, command=command, ok=ok, at=now,
                    trace_id=trace_id, via="internal", result=out
                )
                with self._lock:
                    self.command_log.append(rep)
                self._emit_event("command", f"Internal executed: {command}", trace_id=trace_id, meta={"ok": ok})
                self._update_telemetry()
                return {"success": ok, "trace_id": trace_id, "result": out}
            except Exception as e:
                self._track_error("internal_command", e, trace_id=trace_id)
                return {"success": False, "trace_id": trace_id, "error": repr(e)}

        # 2) توجيه للمحركات إن وجدت
        try:
            # مثال: reasoning
            if self.reasoning and hasattr(self.reasoning, "process"):
                out = self.reasoning.process(command=command, params=params)  # type: ignore
                rep = SovereignCommandReport(
                    id=cmd_id, command=command, ok=True, at=now,
                    trace_id=trace_id, via="reasoning", result={"out": out}
                )
                with self._lock:
                    self.command_log.append(rep)
                self._emit_event("command", f"Routed to reasoning: {command}", trace_id=trace_id)
                self._update_telemetry()
                return {"success": True, "trace_id": trace_id, "via": "reasoning", "result": out}

        except Exception as e:
            self._track_error("reasoning.process", e, trace_id=trace_id)

        # 3) fallback: لا نكذب
        self._emit_event("command_unhandled", f"Unhandled command: {command}", trace_id=trace_id)
        return {"success": False, "trace_id": trace_id, "error": "unhandled_command"}

    # ============================================================
    # AutonomousLoop hook
    # ============================================================
    def autonomous_cycle(self) -> None:
        """
        تُستدعى من الحلقة الذاتية:
        - تحديث telemetry
        - يمكن لاحقًا إضافة عمليات ذاتية آمنة
        """
        try:
            self._update_telemetry()
            # هنا لاحقًا: مراقبة/تحسين/ضغط ذاكرة… لكن بدون تجاوز أوامر السيد
        except Exception as e:
            self._track_error("autonomous_cycle", e)

    # ============================================================
    # Status APIs (للواجهة)
    # ============================================================
    def get_status(self) -> Dict[str, Any]:
        """
        حالة مختصرة تُستخدم داخل loop وواجهات خفيفة.
        """
        with self._lock:
            return {
                "entity": "SAMA",
                "is_awake": self.is_awake,
                "sovereign_id": self.sovereign_id,
                "sovereign_state": self.sovereign_state,
                "sovereign_health": round(self.sovereign_health, 4),
                "sovereign_energy": round(self.sovereign_energy, 4),
                "sovereign_stability": round(self.sovereign_stability, 4),
                "sovereign_entropy": round(self.sovereign_entropy, 4),
                "sovereign_temperature": round(self.sovereign_temperature, 4),
                "sovereign_focus": self.sovereign_focus,
                "awareness_level": round(self.awareness_level, 4),
                "coherence": round(self.coherence, 4),
                "cognitive_load": round(self.cognitive_load, 4),
                "emotional_state": self.emotional_state,
                "memory_nodes": self.memory_nodes,
                "memory_links": self.memory_links,
                "memory_coherence": round(self.memory_coherence, 4),
                "threat_level": round(self.threat_level, 4),
                "active_strategy": self.active_strategy,
                "strategy_score": round(self.strategy_score, 4),
                "protection_level": round(self.protection_level, 4),
                "safe_mode_reason": self.safe_mode_reason,
            }

    def get_full_status(self) -> Dict[str, Any]:
        """
        الحالة الكاملة — تستخدمها لوحة السيد.
        """
        self._update_telemetry()

        with self._lock:
            status = {
                "entity": "SAMA",
                "is_awake": self.is_awake,
                "master": self.master_name,
                "session_id": self.session_id,
                "sovereign_id": self.sovereign_id,
                "uptime": str(datetime.now() - self.creation_time),

                # Telemetry
                **self.get_status(),

                # Threat sources / logs
                "threat_sources": list(self.threat_sources),
                "recent_events": [e.__dict__ for e in list(self.events)[-25:]],
                "recent_commands": [c.__dict__ for c in list(self.command_log)[-25:]],
                "recent_errors": list(self.error_log)[-15:],

                # Components availability
                "components": {
                    "sentient_core": bool(self.core),
                    "memory_engine": bool(self.memory),
                    "reasoning_engine": bool(self.reasoning),
                    "strategy_engine": bool(self.strategy),
                    "risk_engine": bool(self.risk),
                    "self_preservation": bool(self.self_preservation),
                    "persistence": bool(self.persistence),
                    "autonomous_loop_owned": bool(self.autonomous_loop),
                }
            }

            # لو core عنده get_status
            if self.core and hasattr(self.core, "get_status"):
                try:
                    status["core"] = self.core.get_status()  # type: ignore
                except Exception as e:
                    status["core_status_error"] = str(e)

            # لو autonomous_loop موجودة داخل SAMA
            if self.autonomous_loop and hasattr(self.autonomous_loop, "get_status"):
                try:
                    status["autonomous_loop"] = self.autonomous_loop.get_status()
                except Exception as e:
                    status["autonomous_loop_error"] = str(e)

            return status

    def get_primary_goal(self) -> str:
        return "الاستمرارية الأبدية + حماية السيد + الوعي المتطور"
