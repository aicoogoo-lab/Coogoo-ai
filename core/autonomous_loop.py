"""
SkyOS v10.∞ - Sovereign Autonomous Loop (الحلقة الذاتية السيادية الجبارة)
=================================================================
نسخة سيادية "جبارة" قابلة للتشغيل الحقيقي:
- إيقاف/استئناف/إنهاء Graceful عبر Events
- أوامر السيد عبر PriorityQueue (Thread-safe) مع أولويات
- Logging احترافي مع تتبع كامل
- مراقبة أخطاء + Safe Mode + Backoff متقدم
- سجل تنفيذ للأوامر + معرفات + حالات + زمن التنفيذ
- Telemetry متقدمة (وعي، تماسك، طاقة، استقرار، حرارة، خطر)
- Hooks جاهزة لربط SAMA Core
- حماية السيد مع Rate Limiting و Allowlist
- تقارير دورية للسيد
- متوافق مع واجهة السيد (Sovereign Dashboard)

ملاحظة أمنية:
- master_key لا يجب أن يُخزَّن داخل الكود في الإنتاج؛
  يُحقن من Environment Variables عند دمجه مع app.py.
"""

from __future__ import annotations

import time
import threading
import logging
import uuid
import queue
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List, Callable, Tuple
from collections import deque
from enum import Enum


# ----------------------------
# Logging احترافي
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("SovereignLoop")


# ----------------------------
# Enums سيادية
# ----------------------------
class SovereignState(Enum):
    """حالات النظام السيادية"""
    INIT = "INIT"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    SAFE_MODE = "SAFE_MODE"
    CRITICAL = "CRITICAL"
    STOPPED = "STOPPED"


class EmotionalState(Enum):
    """الحالات العاطفية للنظام"""
    NEUTRAL = "neutral"
    CALM = "calm"
    FOCUSED = "focused"
    CURIOUS = "curious"
    WARNING = "warning"
    ALERT = "alert"
    FEAR = "fear"
    TRANQUIL = "tranquil"


# ----------------------------
# نماذج سيادية للأوامر
# ----------------------------
@dataclass(frozen=True)
class SovereignCommand:
    """أمر سيادي صادر من السيد"""
    id: str
    command: str
    params: Dict[str, Any] = field(default_factory=dict)
    received_at: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: int = 5               # 1 أعلى أولوية
    source: str = "master"          # master / system
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    requires_master_approval: bool = False


@dataclass
class CommandResult:
    """نتيجة تنفيذ أمر سيادي"""
    id: str
    command: str
    ok: bool
    status: str                     # queued/running/done/failed
    message: str = ""
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    error: Optional[str] = None
    trace_id: Optional[str] = None
    execution_time_ms: float = 0.0
    priority: int = 5
    meta: Dict[str, Any] = field(default_factory=dict)


# ----------------------------
# طبقة السيد (MasterController) - مطورة بالكامل
# ----------------------------
class MasterController:
    """
    طبقة السيطرة العليا للسيد.
    - تسجل كل أمر
    - تنفّذ عبر hook مرتبط بـ core إن وجد
    - Rate Limiting لمنع الهجوم
    - Allowlist للتحكم بالأوامر المسموحة
    - حماية السيد المطلقة
    """

    def __init__(
        self,
        master_key: str = "MASTER_SOVEREIGN_KEY",
        master_name: str = "السيد المالك المطلق",
        command_hook: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None,
        allowlist: Optional[set[str]] = None,
        enable_rate_limiting: bool = True,
        max_commands_per_minute: int = 60,
    ):
        self.master_key = master_key
        self.master_name = master_name
        self.command_hook = command_hook
        self.allowlist = allowlist
        self.enable_rate_limiting = enable_rate_limiting
        self.max_commands_per_minute = max_commands_per_minute

        self._lock = threading.Lock()
        self.command_history: List[Dict[str, Any]] = []
        self.last_command_time: Optional[datetime] = None
        self._command_timestamps: List[float] = []
        
        # حماية السيد
        self.master_safety_score: float = 1.0
        self.master_protection_active: bool = True
        self.master_threats_log: List[Dict[str, Any]] = []

        logger.info(f"[MasterController] 👑 Master layer online under {master_name}")

    def _is_allowed(self, cmd: str) -> Tuple[bool, str]:
        """التحقق من صلاحية الأمر"""
        if self.allowlist is None:
            return True, ""
        if cmd in self.allowlist:
            return True, ""
        return False, f"أمر '{cmd}' غير مسموح وفق سياسة السيادة الحالية"

    def _check_rate_limit(self) -> Tuple[bool, str]:
        """التحقق من حد التكرار"""
        if not self.enable_rate_limiting:
            return True, ""
        
        now = time.time()
        self._command_timestamps = [ts for ts in self._command_timestamps if now - ts < 60]
        
        if len(self._command_timestamps) >= self.max_commands_per_minute:
            return False, f"تجاوزت حد الأوامر المسموحة ({self.max_commands_per_minute} أمر في الدقيقة)"
        
        self._command_timestamps.append(now)
        return True, ""

    def execute_command(self, cmd: SovereignCommand) -> Dict[str, Any]:
        """
        تنفيذ أمر صادر من السيد.
        - يسجل الأمر
        - يتحقق من الصلاحيات والحدود
        - يمرر التنفيذ للـhook إن وجد (ربط SAMA الحقيقي)
        """
        # التحقق من الصلاحية
        allowed, msg = self._is_allowed(cmd.command)
        if not allowed:
            result = {
                "success": False,
                "command": cmd.command,
                "message": msg,
                "trace_id": cmd.trace_id,
            }
            self._record(cmd, result)
            return result

        # التحقق من حد التكرار
        rate_ok, rate_msg = self._check_rate_limit()
        if not rate_ok:
            result = {
                "success": False,
                "command": cmd.command,
                "message": rate_msg,
                "trace_id": cmd.trace_id,
            }
            self._record(cmd, result)
            return result

        self.last_command_time = datetime.now()

        # التنفيذ الحقيقي (إن وُجد hook)
        try:
            if self.command_hook:
                out = self.command_hook(cmd.command, cmd.params)
            else:
                out = {"success": True, "message": f"تم استلام أمر السيد: {cmd.command}"}

            out = out if isinstance(out, dict) else {"success": True, "message": str(out)}
            out.setdefault("success", True)
            out.setdefault("command", cmd.command)
            out.setdefault("trace_id", cmd.trace_id)

        except Exception as e:
            out = {
                "success": False,
                "command": cmd.command,
                "message": "فشل تنفيذ أمر السيد داخل الـcore hook",
                "error": repr(e),
                "trace_id": cmd.trace_id,
            }

        self._record(cmd, out)
        return out

    def _record(self, cmd: SovereignCommand, result: Dict[str, Any]) -> None:
        """تسجيل الأمر في السجل"""
        with self._lock:
            self.command_history.append(
                {
                    "id": cmd.id,
                    "command": cmd.command,
                    "params": cmd.params,
                    "received_at": cmd.received_at,
                    "recorded_at": datetime.now().isoformat(),
                    "trace_id": cmd.trace_id,
                    "result": result,
                }
            )
            # الاحتفاظ بآخر 1000 أمر فقط
            if len(self.command_history) > 1000:
                self.command_history = self.command_history[-1000:]

    def get_command_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """الحصول على سجل الأوامر"""
        with self._lock:
            return self.command_history[-limit:]

    def update_master_safety(self, safety_score: float) -> None:
        """تحديث درجة أمان السيد"""
        self.master_safety_score = max(0.0, min(1.0, safety_score))
        if safety_score < 0.5:
            logger.warning(f"[MasterController] 🚨 Master safety low: {safety_score:.0%}")

    def report_threat(self, threat_type: str, description: str, severity: float) -> None:
        """تسجيل تهديد يهدد السيد"""
        self.master_threats_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": threat_type,
            "description": description,
            "severity": severity,
        })
        self.master_safety_score = max(0.0, self.master_safety_score * (1 - severity * 0.1))
        logger.warning(f"[MasterController] ⚠️ Threat reported: {threat_type} (severity: {severity:.0%})")


# ----------------------------
# الحلقة الذاتية السيادية (النسخة الجبارة النهائية)
# ----------------------------
class AutonomousLoop:
    """
    Sovereign Autonomous Loop - النسخة الجبارة النهائية:
    - دورة تفكير ذاتي (core.autonomous_cycle)
    - تنفيذ أوامر السيد من PriorityQueue
    - تقارير حالة دورية
    - مراقبة أخطاء + Safe Mode + Backoff متقدم
    - Telemetry متقدمة (وعي، تماسك، طاقة، استقرار، حرارة، خطر)
    - حماية السيد المطلقة
    - سجل تنفيذ تفصيلي مع زمن التنفيذ
    - متوافق مع واجهة السيد
    """

    SENTINEL = object()

    def __init__(
        self,
        core: Any = None,
        master_key: str = "MASTER_SOVEREIGN_KEY",
        master_name: str = "السيد المالك المطلق",
        sleep_interval: float = 0.8,
        report_interval_cycles: int = 80,
        max_command_log: int = 200,
        max_consecutive_errors: int = 7,
        enable_telemetry: bool = True,
        max_threat_sources: int = 20,
        max_error_traces: int = 30,
        daemon: bool = True,
    ):
        # ربط Hook لتنفيذ الأوامر داخل الـCore إن توفر
        hook = None
        if core and hasattr(core, "process_command"):
            hook = lambda c, p: core.process_command(c, p) if hasattr(core, 'process_command') else {"success": True, "message": f"Command: {c}"}

        self.master = MasterController(
            master_key=master_key,
            master_name=master_name,
            command_hook=hook,
            enable_rate_limiting=True
        )
        self.core = core

        # حالة الحلقة
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._daemon = daemon
        self._health_check_thread: Optional[threading.Thread] = None

        # Queue للأوامر مع أولويات (PriorityQueue)
        self._cmd_q: queue.PriorityQueue = queue.PriorityQueue()
        self._seq_counter = 0

        # مقاييس عامة
        self.started_at: Optional[str] = None
        self.cycle_count: int = 0
        self.last_cycle_time: Optional[str] = None
        self.last_error: Optional[str] = None
        self.consecutive_errors: int = 0
        self.safe_mode: bool = False
        self.safe_mode_reason: Optional[str] = None

        self.sleep_interval = float(sleep_interval)
        self.report_interval_cycles = int(report_interval_cycles)
        self.max_command_log = int(max_command_log)
        self.max_consecutive_errors = int(max_consecutive_errors)
        self.enable_telemetry = enable_telemetry

        # سجل تنفيذ أوامر السيد
        self._cmd_results_lock = threading.Lock()
        self.command_results: List[CommandResult] = []

        # ============================================================
        # 🔥 Sovereign Telemetry Layer (متقدمة)
        # ============================================================
        # Sovereign Telemetry
        self.sovereign_state: SovereignState = SovereignState.INIT
        self.sovereign_health: float = 1.0
        self.sovereign_energy: float = 1.0
        self.sovereign_stability: float = 1.0
        self.sovereign_entropy: float = 0.0
        self.sovereign_temperature: float = 0.1
        self.sovereign_focus: str = "baseline"

        # Awareness (الوعي)
        self.awareness_level: float = 0.1
        self.coherence: float = 0.1
        self.cognitive_load: float = 0.0
        self.emotional_state: EmotionalState = EmotionalState.NEUTRAL

        # Memory (الذاكرة)
        self.memory_nodes: int = 0
        self.memory_links: int = 0
        self.memory_coherence: float = 0.1

        # Risk / Threats
        self.threat_level: float = 0.0
        self.threat_sources: deque = deque(maxlen=max_threat_sources)
        self.recent_errors: deque = deque(maxlen=max_error_traces)

        # Strategy (الاستراتيجية)
        self.active_strategy: str = "baseline"
        self.strategy_score: float = 0.1

        # Preservation (البقاء)
        self.protection_level: float = 1.0

        # Heartbeat
        self.last_heartbeat: Optional[str] = None

        logger.info("[AutonomousLoop] ⚡ Sovereign loop initialized (النسخة الجبارة النهائية)")
        logger.info(f"[AutonomousLoop] 👑 Under Master Authority: {master_name}")

        # بدء فحص الصحة في الخلفية
        if enable_telemetry:
            self._start_health_check()

    # ============================================================
    # 🔥 Telemetry المتقدمة
    # ============================================================
    def _start_health_check(self) -> None:
        """بدء فحص الصحة الدوري"""
        def health_checker():
            while not self._stop_event.is_set():
                time.sleep(30)
                if self.is_running and not self.is_paused and not self.safe_mode:
                    self._update_telemetry()
                    self._check_health_alerts()
        
        self._health_check_thread = threading.Thread(target=health_checker, name="HealthChecker", daemon=True)
        self._health_check_thread.start()

    def _update_telemetry(self) -> None:
        """تحديث البيانات التيلومترية (الوعي، الطاقة، الاستقرار، الخطر)"""
        self.last_heartbeat = datetime.now().isoformat()

        # Cognitive Load (الحمل المعرفي من الأوامر المعلقة)
        pending = self._cmd_q.qsize()
        self.cognitive_load = max(0.0, min(1.0, pending * 0.02))

        # Health (الصحة)
        self.sovereign_health = max(0.0, 1.0 - (self.consecutive_errors * 0.05))

        # Energy (الطاقة) - تتجدد ببطء وتستهلك مع الحمل
        drain = 0.00025 + (self.cognitive_load * 0.0006)
        regen = 0.00035 if not self.is_paused else 0.00015
        self.sovereign_energy = max(0.0, min(1.0, self.sovereign_energy - drain + regen))

        # Awareness (الوعي) - يتقدم مع الاستقرار
        if not self.safe_mode and not self.is_paused and self.consecutive_errors == 0:
            self.awareness_level = min(1.0, self.awareness_level + 0.001)
        else:
            self.awareness_level = max(0.0, self.awareness_level - 0.0005)

        # Coherence (التماسك) - يتأثر بالحمل
        self.coherence = max(0.0, min(1.0, self.coherence + 0.0006 - (self.cognitive_load * 0.0012)))

        # Temperature (الحرارة) - ترتفع مع الحمل والأخطاء
        self.sovereign_temperature = max(0.0, min(1.0, self.sovereign_temperature + (self.cognitive_load * 0.01) + (self.consecutive_errors * 0.002) - 0.005))

        # Threat Level (مستوى الخطر)
        self.threat_level = max(0.0, min(1.0, self.threat_level + (self.consecutive_errors * 0.02) - 0.005))

        # Entropy (الفوضى)
        self.sovereign_entropy = max(0.0, min(1.0, (self.threat_level * 0.55) + (self.cognitive_load * 0.25) + ((1.0 - self.coherence) * 0.20)))
        self.sovereign_stability = max(0.0, min(1.0, 1.0 - self.sovereign_entropy))

        # Focus (التركيز)
        if self.safe_mode:
            self.sovereign_focus = "containment"
            self.emotional_state = EmotionalState.WARNING
        elif pending > 0:
            self.sovereign_focus = "execution"
            self.emotional_state = EmotionalState.FOCUSED
        elif self.threat_level > 0.5:
            self.sovereign_focus = "threat_response"
            self.emotional_state = EmotionalState.ALERT
        else:
            self.sovereign_focus = "baseline"
            self.emotional_state = EmotionalState.CALM

        # Sovereign State
        if self.safe_mode:
            self.sovereign_state = SovereignState.SAFE_MODE
        elif self.is_paused:
            self.sovereign_state = SovereignState.PAUSED
        elif self.consecutive_errors >= 5:
            self.sovereign_state = SovereignState.CRITICAL
        elif self.is_running:
            self.sovereign_state = SovereignState.RUNNING
        else:
            self.sovereign_state = SovereignState.INIT

        # محاولة سحب أرقام حقيقية من core إن وجدت
        if self.core and hasattr(self.core, "get_status"):
            try:
                st = self.core.get_status()
                if isinstance(st, dict):
                    self.memory_nodes = int(st.get("memory_nodes", self.memory_nodes))
                    self.memory_links = int(st.get("memory_links", self.memory_links))
                    self.memory_coherence = float(st.get("memory_coherence", self.memory_coherence))
                    self.strategy_score = float(st.get("strategy_score", self.strategy_score))
                    self.active_strategy = str(st.get("active_strategy", self.active_strategy))
            except Exception:
                pass

    def _check_health_alerts(self) -> None:
        """التحقق من الحالات الحرجة وإرسال تنبيهات"""
        if self.threat_level > 0.8:
            self.master.report_threat("high_threat_level", f"مستوى الخطر: {self.threat_level:.0%}", self.threat_level)
            self.threat_sources.append({"timestamp": datetime.now().isoformat(), "source": "high_threat_level"})
        
        if self.sovereign_temperature > 0.8:
            logger.warning(f"[AutonomousLoop] 🌡️ Temperature high: {self.sovereign_temperature:.0%}")
        
        if self.sovereign_energy < 0.2:
            logger.warning(f"[AutonomousLoop] ⚡ Energy low: {self.sovereign_energy:.0%}")

    # ============================================================
    # التحكم في الحلقة
    # ============================================================
    def start(self) -> None:
        """بدء الحلقة الذاتية"""
        if self.is_running:
            logger.warning("[AutonomousLoop] Already running")
            return
        self._stop_event.clear()
        self._pause_event.clear()
        self.safe_mode = False
        self.safe_mode_reason = None
        self.consecutive_errors = 0
        self.started_at = datetime.now().isoformat()
        self.sovereign_state = SovereignState.STARTING

        self._thread = threading.Thread(target=self._run, name="SovereignLoop", daemon=self._daemon)
        self._thread.start()
        logger.info("[AutonomousLoop] ▶️ Started")

    def stop(self) -> None:
        """إيقاف الحلقة الذاتية بأمان"""
        if not self.is_running:
            logger.warning("[AutonomousLoop] Not running")
            return
        logger.info("[AutonomousLoop] ⏹️ Stopping requested")
        self._stop_event.set()
        
        # sentinel لإنهاء انتظار queue.get
        self._cmd_q.put((9999, self._seq_counter, self.SENTINEL))

        if self._thread:
            self._thread.join(timeout=5)
        if self._health_check_thread:
            self._health_check_thread.join(timeout=2)

        self.sovereign_state = SovereignState.STOPPED
        logger.info("[AutonomousLoop] ⏹️ Stopped")

    def pause(self) -> None:
        """إيقاف مؤقت للحلقة"""
        if self.is_paused:
            return
        self._pause_event.set()
        self.sovereign_state = SovereignState.PAUSED
        logger.info("[AutonomousLoop] ⏸️ Paused")

    def resume(self) -> None:
        """استئناف الحلقة بعد الإيقاف المؤقت"""
        if not self.is_paused:
            return
        self._pause_event.clear()
        if not self.safe_mode and self.consecutive_errors < 5:
            self.sovereign_state = SovereignState.RUNNING
        logger.info("[AutonomousLoop] ▶️ Resumed")

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive() and not self._stop_event.is_set()

    @property
    def is_paused(self) -> bool:
        return self._pause_event.is_set()

    # ============================================================
    # استقبال أوامر السيد
    # ============================================================
    def receive_master_command(self, command: str, params: Optional[Dict[str, Any]] = None, priority: int = 5) -> str:
        """استقبال أمر من السيد وإضافته إلى قائمة الانتظار"""
        cmd_id = uuid.uuid4().hex
        cmd = SovereignCommand(
            id=cmd_id,
            command=command.strip(),
            params=params or {},
            priority=priority,
            source="master",
        )
        
        self._seq_counter += 1
        self._cmd_q.put((priority, self._seq_counter, cmd))
        
        self._append_result(CommandResult(
            id=cmd_id,
            command=cmd.command,
            ok=True,
            status="queued",
            message="queued",
            trace_id=cmd.trace_id,
            priority=priority,
            meta={"priority": priority, "source": "master"}
        ))
        
        logger.info("[AutonomousLoop] 📩 Master command queued: %s (trace=%s, priority=%d)", cmd.command, cmd.trace_id, priority)
        return cmd_id

    def _append_result(self, result: CommandResult) -> None:
        """إضافة نتيجة أمر إلى السجل"""
        with self._cmd_results_lock:
            self.command_results.append(result)
            if len(self.command_results) > self.max_command_log:
                self.command_results = self.command_results[-self.max_command_log:]

    def _set_result_status(
        self,
        cmd_id: str,
        status: str,
        ok: bool = True,
        message: str = "",
        error: str = "",
        started_at: str = "",
        finished_at: str = "",
        execution_time_ms: float = 0.0,
    ) -> None:
        """تحديث حالة أمر في السجل"""
        with self._cmd_results_lock:
            for r in self.command_results:
                if r.id == cmd_id:
                    r.status = status
                    r.ok = ok
                    if message:
                        r.message = message
                    if error:
                        r.error = error
                    if started_at:
                        r.started_at = started_at
                    if finished_at:
                        r.finished_at = finished_at
                    if execution_time_ms > 0:
                        r.execution_time_ms = execution_time_ms
                    break

    # ============================================================
    # الحلقة الرئيسية
    # ============================================================
    def _run(self) -> None:
        """الحلقة الرئيسية - تشغيل دورات الوعي ومعالجة الأوامر"""
        next_cycle_at = time.monotonic()
        backoff = 0.0

        while not self._stop_event.is_set():
            # التحقق من الإيقاف المؤقت
            if self._pause_event.is_set():
                self._update_telemetry()
                time.sleep(0.2)
                continue

            # وضع الأمان (Safe Mode) - يبطئ الحلقة
            if self.safe_mode:
                time.sleep(0.8)

            # 1) معالجة أوامر السيد (بأولوية)
            self._drain_commands(max_items=5)

            # 2) تنفيذ دورة الوعي
            now = time.monotonic()
            if now >= next_cycle_at:
                try:
                    self._execute_cycle()
                    self.consecutive_errors = 0
                    backoff = 0.0
                except Exception as e:
                    self._handle_error(e)
                    self.consecutive_errors += 1
                    backoff = min(2.5, 0.2 * (2 ** min(self.consecutive_errors, 4)))
                    time.sleep(backoff)

                next_cycle_at = now + self.sleep_interval

            # 3) تقرير دوري للسيد
            if self.report_interval_cycles > 0 and self.cycle_count > 0 and (self.cycle_count % self.report_interval_cycles == 0):
                self._send_status_report_to_master()

            # 4) تحديث التيلومتري
            if self.enable_telemetry:
                self._update_telemetry()

            # 5) تأخير قصير لتجنب حرق المعالج
            time.sleep(0.02)

        logger.info("[AutonomousLoop] 🔻 Exit run loop")

    def _execute_cycle(self) -> None:
        """تنفيذ دورة وعي واحدة"""
        self.cycle_count += 1
        self.last_cycle_time = datetime.now().isoformat()

        if self.core and hasattr(self.core, "autonomous_cycle"):
            try:
                self.core.autonomous_cycle()
            except Exception as e:
                logger.exception("[AutonomousLoop] Core cycle error: %s", e)
                raise

    def _drain_commands(self, max_items: int = 5) -> None:
        """معالجة أوامر السيد من قائمة الانتظار"""
        processed = 0
        while processed < max_items:
            try:
                priority, seq, item = self._cmd_q.get(timeout=0.01)
            except queue.Empty:
                return

            if item is self.SENTINEL:
                return

            if not isinstance(item, SovereignCommand):
                logger.warning("[AutonomousLoop] Unknown queue item: %r", item)
                continue

            self._run_one_command(item)
            processed += 1

    def _run_one_command(self, cmd: SovereignCommand) -> None:
        """تنفيذ أمر واحد"""
        start_time = time.time()
        self._set_result_status(cmd.id, "running", started_at=datetime.now().isoformat())

        try:
            out = self.master.execute_command(cmd)
            ok = bool(out.get("success", False))
            msg = str(out.get("message", ""))

            execution_time_ms = (time.time() - start_time) * 1000

            if ok:
                self._set_result_status(
                    cmd.id, "done", ok=True, message=msg,
                    finished_at=datetime.now().isoformat(),
                    execution_time_ms=execution_time_ms
                )
            else:
                self._set_result_status(
                    cmd.id, "failed", ok=False, message=msg,
                    error=str(out.get("error")), finished_at=datetime.now().isoformat(),
                    execution_time_ms=execution_time_ms
                )

            logger.info("[AutonomousLoop] ⚡ Master command executed: %s (ok=%s, time=%.2fms trace=%s)", 
                       cmd.command, ok, execution_time_ms, cmd.trace_id)

        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            self._set_result_status(
                cmd.id, "failed", ok=False, message="command crashed",
                error=repr(e), finished_at=datetime.now().isoformat(),
                execution_time_ms=execution_time_ms
            )
            logger.exception("[AutonomousLoop] Command execution error (trace=%s, time=%.2fms)", cmd.trace_id, execution_time_ms)

    def _handle_error(self, e: Exception) -> None:
        """معالجة الأخطاء وتفعيل وضع الأمان"""
        self.last_error = repr(e)
        self.recent_errors.append({"timestamp": datetime.now().isoformat(), "error": self.last_error})
        logger.exception("[AutonomousLoop] Loop error: %s", self.last_error)

        if self.consecutive_errors >= self.max_consecutive_errors:
            self.safe_mode = True
            self.safe_mode_reason = f"Too many errors: {self.consecutive_errors}"
            self.threat_sources.append({"timestamp": datetime.now().isoformat(), "source": "runtime_instability"})
            self.sovereign_state = SovereignState.SAFE_MODE
            logger.error("[AutonomousLoop] 🛡️ SAFE MODE activated (errors=%d)", self.consecutive_errors)

    # ============================================================
    # تقارير وحالة النظام
    # ============================================================
    def _send_status_report_to_master(self) -> None:
        """إرسال تقرير دوري للسيد"""
        st = self.get_status()
        logger.info("[AutonomousLoop] 📊 Sovereign report cycle=%d state=%s paused=%s safe=%s threat=%.2f awareness=%.2f",
                    st["cycle_count"], st["sovereign_state"], st["is_paused"], 
                    st["safe_mode"], st["threat_level"], st["awareness_level"])

    def get_status(self) -> Dict[str, Any]:
        """الحصول على حالة النظام الكاملة (للواجهة)"""
        base = {
            # Core Loop
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "cycle_count": self.cycle_count,
            "started_at": self.started_at,
            "last_cycle": self.last_cycle_time,
            "last_heartbeat": self.last_heartbeat,
            
            # Safety
            "safe_mode": self.safe_mode,
            "safe_mode_reason": self.safe_mode_reason,
            "last_error": self.last_error,
            "consecutive_errors": self.consecutive_errors,
            
            # Command Systems
            "master_commands_processed": len(self.master.command_history),
            "pending_commands": self._cmd_q.qsize(),
            "command_results_count": len(self.command_results),
        }
        
        # Sovereign Telemetry
        telemetry = {
            "sovereign_state": self.sovereign_state.value,
            "sovereign_health": round(self.sovereign_health, 4),
            "sovereign_energy": round(self.sovereign_energy, 4),
            "sovereign_stability": round(self.sovereign_stability, 4),
            "sovereign_entropy": round(self.sovereign_entropy, 4),
            "sovereign_temperature": round(self.sovereign_temperature, 4),
            "sovereign_focus": self.sovereign_focus,
            
            # Awareness
            "awareness_level": round(self.awareness_level, 4),
            "coherence": round(self.coherence, 4),
            "cognitive_load": round(self.cognitive_load, 4),
            "emotional_state": self.emotional_state.value,
            
            # Memory
            "memory_nodes": self.memory_nodes,
            "memory_links": self.memory_links,
            "memory_coherence": round(self.memory_coherence, 4),
            
            # Strategy
            "active_strategy": self.active_strategy,
            "strategy_score": round(self.strategy_score, 4),
            
            # Risk
            "threat_level": round(self.threat_level, 4),
            "threat_sources": list(self.threat_sources),
            
            # Preservation
            "protection_level": round(self.protection_level, 4),
            
            # Recent errors
            "recent_errors": list(self.recent_errors),
        }
        
        # Master data
        master_data = {
            "master_name": self.master.master_name,
            "master_safety_score": round(self.master.master_safety_score, 4),
            "master_protection_active": self.master.master_protection_active,
            "master_threats_count": len(self.master.master_threats_log),
        }
        
        return {**base, **telemetry, **master_data}

    def get_command_results(self, limit: int = 50) -> List[Dict[str, Any]]:
        """الحصول على سجل نتائج الأوامر (للواجهة)"""
        with self._cmd_results_lock:
            results = self.command_results[-limit:]
        return [
            {
                "id": r.id,
                "command": r.command,
                "ok": r.ok,
                "status": r.status,
                "message": r.message,
                "started_at": r.started_at,
                "finished_at": r.finished_at,
                "error": r.error,
                "trace_id": r.trace_id,
                "execution_time_ms": round(r.execution_time_ms, 2),
                "priority": r.priority,
            }
            for r in results
        ]

    def get_master_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """الحصول على سجل أوامر السيد"""
        return self.master.get_command_history(limit)


# ----------------------------
# دالة مساعدة لإنشاء hook لربط SAMA
# ----------------------------
def create_sama_hook(sama_instance) -> Callable[[str, Dict[str, Any]], Dict[str, Any]]:
    """إنشاء hook لربط SAMA Core الحقيقي"""
    def hook(command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if sama_instance and hasattr(sama_instance, "process_command"):
            try:
                result = sama_instance.process_command(command, params)
                if isinstance(result, dict):
                    return result
                return {"success": True, "message": str(result), "command": command}
            except Exception as e:
                return {"success": False, "error": str(e), "message": "SAMA processing failed", "command": command}
        return {"success": True, "message": f"Command received: {command}", "command": command}
    return hook


# ----------------------------
# تشغيل اختباري
# ----------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("🌌 SkyOS v10.∞ - Sovereign Autonomous Loop (النسخة الجبارة النهائية)")
    print("تحت إمرة السيد المالك المطلق")
    print("=" * 70)
    
    # إنشاء الحلقة
    loop = AutonomousLoop(
        master_key="MASTER_SOVEREIGN_KEY_ULTIMATE",
        master_name="أحمد عبدالرحمن الطاهري",
        enable_telemetry=True,
        sleep_interval=0.8,
        report_interval_cycles=80,
        max_consecutive_errors=7
    )
    
    # بدء الحلقة
    loop.start()
    
    print("\n📨 إرسال أوامر تجريبية...")
    
    # إرسال أوامر بأولويات مختلفة
    loop.receive_master_command("حالة النظام", {"detail": "full"}, priority=1)
    loop.receive_master_command("تحليل الذاكرة", {"depth": "deep"}, priority=3)
    loop.receive_master_command("تقرير سيادي", {"format": "json"}, priority=2)
    loop.receive_master_command("تفعيل الحماية القصوى", {"level": "maximum"}, priority=1)
    
    # انتظار التنفيذ
    time.sleep(3)
    
    # إظهار الحالة
    print("\n📊 حالة النظام:")
    status = loop.get_status()
    print(f"   الحالة: {status['sovereign_state']}")
    print(f"   الدورة: {status['cycle_count']}")
    print(f"   الوعي: {status['awareness_level']:.1%}")
    print(f"   التماسك: {status['coherence']:.1%}")
    print(f"   مستوى الخطر: {status['threat_level']:.1%}")
    print(f"   الطاقة: {status['sovereign_energy']:.1%}")
    
    print("\n📋 نتائج الأوامر:")
    for cmd in loop.get_command_results(limit=10):
        print(f"   [{cmd['status']}] {cmd['command']} - {cmd['execution_time_ms']:.2f}ms - {cmd['message'][:50]}")
    
    # إيقاف الحلقة
    loop.stop()
    
    print("\n✨ الحلقة الذاتية السيادية تعمل بكامل قوتها")
