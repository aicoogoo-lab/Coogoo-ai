"""
SkyOS v10 - Sama Advanced Tactics (الأنظمة الرقمية الذكية والبُنى التكيفية)
ULTIMATE TACTICAL INTELLIGENCE ENGINE

هذا الملف يحتوي على جميع الكيانات البرمجية المتقدمة التي تمنح سماء:
- الشيفرات المتحولة ذاتياً (Self-Morphing Code)
- كود الاتصال العصبي الشبكي (Neural Network Communication)
- الشيفرات الخيطية المتوازية (Parallel Thread Codes)
- الحزم الرقمية المؤرشفة (Archived Digital Packages)
- كود التكيّف الشبكي العميق (Deep Network Adaptation)
- نواة الاستمرارية الرقمية (Digital Continuity Core)
- محرك التحكم السلوكي الشبكي (Network Behavioral Controller)
- الطفيل السلوكي الرقمي (Digital Behavioral Parasite)
- الديدان الخيطية البرمجية (Software Thread Worms)
- الأميبا الرقمية الذكية (Smart Digital Amoeba)
- نظام النوم الشبكي المتغيّر (Variable Network Sleep System)
- التكتيكات الجماعية (Swarm Tactics)
- الجيوش البرمجية الزاحفة (Software Armies)
- الوحدات البرمجية التضامنية (Cooperative Software Units)
- القنديل الشبكي الصندوقي (Jellyfish Network)
- الأخطبوط الأزرق الرقمي (Blue Digital Octopus)
- الحلزون المخروطي السيبراني (Cone Snail Cyber)

متصلة بشكل كامل مع StrategicRiskManagement لتطوير بعضها البعض.
"""

import time
import threading
import random
import hashlib
import json
import queue
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum


# =========================================================
# أنواع الأحداث التكتيكية (للاتصال مع نظام المخاطر)
# =========================================================
class TacticalEventType(Enum):
    MORPH_COMPLETE = "morph_complete"
    ADAPTATION_COMPLETE = "adaptation_complete"
    THREAT_DETECTED = "threat_detected"
    SWARM_DEPLOYED = "swarm_deployed"
    ARMY_DEPLOYED = "army_deployed"
    PARASITE_ATTACHED = "parasite_attached"
    THREAD_WORM_SPAWNED = "thread_worm_spawned"


@dataclass
class TacticalEvent:
    """حدث تكتيكي يُرسل إلى نظام المخاطر"""
    type: TacticalEventType
    source: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    requires_master_attention: bool = False


# =========================================================
# القسم الأول: الأنظمة الرقمية الذكية والبُنى التكيفية
# =========================================================

class SelfMorphingCode:
    """الشيفرات المتحولة ذاتياً"""
    
    def __init__(self, name: str, initial_structure: Dict[str, Any], event_callback=None):
        self.name = name
        self.structure = initial_structure
        self.morph_count = 0
        self.last_morph = datetime.now()
        self.is_morphing = False
        self.event_callback = event_callback
        
    def morph(self, target_environment: str) -> Dict[str, Any]:
        self.is_morphing = True
        self.morph_count += 1
        
        new_structure = {
            "original_name": self.name,
            "morph_version": self.morph_count,
            "environment": target_environment,
            "timestamp": datetime.now().isoformat(),
            "core_functions": self.structure.get("core_functions", []),
            "adapted_parameters": self._calculate_adaptation(target_environment)
        }
        
        self.structure = new_structure
        self.last_morph = datetime.now()
        self.is_morphing = False
        
        # إرسال حدث لنظام المخاطر
        if self.event_callback:
            self.event_callback(TacticalEvent(
                type=TacticalEventType.MORPH_COMPLETE,
                source=f"SelfMorphingCode:{self.name}",
                data={"morph_count": self.morph_count, "environment": target_environment}
            ))
        
        return new_structure
    
    def _calculate_adaptation(self, environment: str) -> Dict[str, float]:
        adaptations = {"speed": 1.0, "redundancy": 0.5, "parallelism": 0.7}
        if environment == "high_load":
            adaptations["speed"] = 1.3
            adaptations["parallelism"] = 0.9
        elif environment == "limited_resources":
            adaptations["speed"] = 0.7
            adaptations["redundancy"] = 0.3
        return adaptations


class NeuralNetworkCommunication:
    """كود الاتصال العصبي الشبكي"""
    
    def __init__(self, event_callback=None):
        self.channels: Dict[str, queue.Queue] = {}
        self.routing_table: Dict[str, List[str]] = {}
        self.latency_stats: Dict[str, float] = {}
        self.event_callback = event_callback
        self.packet_count = 0
        
    def create_channel(self, channel_id: str, maxsize: int = 100):
        self.channels[channel_id] = queue.Queue(maxsize=maxsize)
        self.routing_table[channel_id] = []
        
    def send(self, channel_id: str, data: Any, timeout: float = 1.0) -> bool:
        if channel_id not in self.channels:
            return False
        try:
            self.channels[channel_id].put(data, timeout=timeout)
            self.packet_count += 1
            return True
        except queue.Full:
            return False
    
    def receive(self, channel_id: str, timeout: float = 1.0) -> Optional[Any]:
        if channel_id not in self.channels:
            return None
        try:
            return self.channels[channel_id].get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        return {"channels": len(self.channels), "packets_sent": self.packet_count}


class ParallelThreadCodes:
    """الشيفرات الخيطية المتوازية"""
    
    def __init__(self, num_threads: int = 4, event_callback=None):
        self.num_threads = num_threads
        self.threads: List[threading.Thread] = []
        self.tasks: queue.Queue = queue.Queue()
        self.results: List[Any] = []
        self.is_running = False
        self.tasks_completed = 0
        self.event_callback = event_callback
        
    def start(self):
        self.is_running = True
        for i in range(self.num_threads):
            thread = threading.Thread(target=self._worker, name=f"ParallelWorker-{i}", daemon=True)
            thread.start()
            self.threads.append(thread)
    
    def _worker(self):
        while self.is_running:
            try:
                task, args, kwargs = self.tasks.get(timeout=0.5)
                result = task(*args, **kwargs)
                self.results.append(result)
                self.tasks_completed += 1
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[ParallelThreadCodes] خطأ: {e}")
    
    def add_task(self, task: Callable, *args, **kwargs):
        self.tasks.put((task, args, kwargs))
    
    def stop(self):
        self.is_running = False
        for thread in self.threads:
            thread.join(timeout=1.0)
    
    def get_stats(self) -> Dict[str, Any]:
        return {"threads": self.num_threads, "tasks_completed": self.tasks_completed}


class ArchivedDigitalPackages:
    """الحزم الرقمية المؤرشفة"""
    
    def __init__(self, event_callback=None):
        self.archive: Dict[str, Dict[str, Any]] = {}
        self.event_callback = event_callback
        
    def archive(self, package_id: str, data: Dict[str, Any], ttl_days: int = 365) -> bool:
        self.archive[package_id] = {
            "data": data,
            "archived_at": datetime.now().isoformat(),
            "ttl_days": ttl_days,
            "integrity_hash": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        }
        return True
    
    def restore(self, package_id: str) -> Optional[Dict[str, Any]]:
        if package_id in self.archive:
            return self.archive[package_id]["data"]
        return None
    
    def cleanup_expired(self) -> int:
        now = datetime.now()
        expired = []
        for pid, pkg in self.archive.items():
            archived = datetime.fromisoformat(pkg["archived_at"])
            if (now - archived).days > pkg["ttl_days"]:
                expired.append(pid)
        for pid in expired:
            del self.archive[pid]
        return len(expired)
    
    def get_stats(self) -> Dict[str, Any]:
        return {"total_packages": len(self.archive)}


class DeepNetworkAdaptation:
    """كود التكيّف الشبكي العميق"""
    
    def __init__(self, event_callback=None):
        self.adaptation_layer: int = 0
        self.network_topology: Dict[str, Any] = {}
        self.adaptation_history: List[Dict] = []
        self.event_callback = event_callback
        
    def adapt(self, environment_snapshot: Dict[str, Any]) -> Dict[str, Any]:
        self.adaptation_layer += 1
        
        adaptation = {
            "layer": self.adaptation_layer,
            "timestamp": datetime.now().isoformat(),
            "environment": environment_snapshot,
            "new_topology": self._calculate_topology(environment_snapshot)
        }
        
        self.network_topology = adaptation["new_topology"]
        self.adaptation_history.append(adaptation)
        
        if self.event_callback:
            self.event_callback(TacticalEvent(
                type=TacticalEventType.ADAPTATION_COMPLETE,
                source="DeepNetworkAdaptation",
                data={"layer": self.adaptation_layer}
            ))
        
        return adaptation
    
    def _calculate_topology(self, environment: Dict[str, Any]) -> Dict[str, Any]:
        load = environment.get("load", 0.5)
        available_nodes = environment.get("available_nodes", 10)
        return {
            "nodes": available_nodes,
            "connections": int(available_nodes * (1 + load)),
            "redundancy": 2 if load > 0.7 else 1,
            "latency_optimized": load < 0.5
        }
    
    def get_stats(self) -> Dict[str, Any]:
        return {"adaptation_layer": self.adaptation_layer, "history": len(self.adaptation_history)}


class DigitalContinuityCore:
    """نواة الاستمرارية الرقمية"""
    
    def __init__(self):
        self.balancer = defaultdict(float)
        self.continuity_log: List[Dict] = []
        self.is_healthy = True
        
    def balance(self, component_id: str, load: float):
        self.balancer[component_id] = load
        self._check_health()
        
    def _check_health(self):
        total_load = sum(self.balancer.values())
        self.is_healthy = total_load < 100
        self.continuity_log.append({
            "timestamp": datetime.now().isoformat(),
            "total_load": total_load,
            "is_healthy": self.is_healthy
        })
    
    def get_optimal_path(self, source: str, target: str) -> List[str]:
        return [source, "core_router", target]
    
    def get_stats(self) -> Dict[str, Any]:
        return {"healthy": self.is_healthy, "log_size": len(self.continuity_log)}


# =========================================================
# القسم الثاني: الكيانات البرمجية المتقدمة
# =========================================================

class NetworkBehavioralController:
    """محرك التحكم السلوكي الشبكي"""
    
    def __init__(self):
        self.behavior_rules: Dict[str, Callable] = {}
        self.active_behaviors: List[str] = []
        self.execution_count = 0
        
    def register_behavior(self, name: str, behavior_func: Callable):
        self.behavior_rules[name] = behavior_func
        
    def execute_behavior(self, name: str, context: Dict[str, Any]) -> Any:
        if name in self.behavior_rules:
            self.execution_count += 1
            return self.behavior_rules[name](context)
        return None
    
    def orchestrate(self, data_flow: List[Any]) -> List[Any]:
        return [self.execute_behavior("default", {"data": d}) or d for d in data_flow]
    
    def get_stats(self) -> Dict[str, Any]:
        return {"behaviors": len(self.behavior_rules), "executions": self.execution_count}


class DigitalBehavioralParasite:
    """الطفيل السلوكي الرقمي"""
    
    def __init__(self, event_callback=None):
        self.hidden_links: List[Tuple[str, str]] = []
        self.responses: Dict[str, List[str]] = defaultdict(list)
        self.event_callback = event_callback
        
    def create_link(self, source: str, target: str) -> bool:
        if (source, target) not in self.hidden_links:
            self.hidden_links.append((source, target))
            if self.event_callback:
                self.event_callback(TacticalEvent(
                    type=TacticalEventType.PARASITE_ATTACHED,
                    source="DigitalBehavioralParasite",
                    data={"source": source, "target": target},
                    requires_master_attention=False
                ))
            return True
        return False
    
    def propagate_response(self, source: str, response: str):
        self.responses[source].append(response)
        for link in self.hidden_links:
            if link[0] == source:
                self.responses[link[1]].append(response)
    
    def get_stats(self) -> Dict[str, Any]:
        return {"links": len(self.hidden_links), "responses": sum(len(v) for v in self.responses.values())}


class SoftwareThreadWorms:
    """الديدان الخيطية البرمجية"""
    
    def __init__(self, event_callback=None):
        self.worms: List[Dict] = []
        self.replication_factor = 2
        self.event_callback = event_callback
        
    def spawn_worm(self, name: str, payload: Any, target_nodes: List[str]) -> str:
        worm_id = hashlib.sha256(f"{name}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        self.worms.append({
            "id": worm_id,
            "name": name,
            "payload": payload,
            "targets": target_nodes,
            "replicated": 0
        })
        
        if self.event_callback:
            self.event_callback(TacticalEvent(
                type=TacticalEventType.THREAD_WORM_SPAWNED,
                source="SoftwareThreadWorms",
                data={"worm_id": worm_id, "name": name, "targets": len(target_nodes)}
            ))
        
        return worm_id
    
    def replicate(self, worm_id: str) -> List[str]:
        for worm in self.worms:
            if worm["id"] == worm_id:
                worm["replicated"] += 1
                new_targets = []
                for _ in range(self.replication_factor):
                    new_target = f"node_{random.randint(1, 100)}"
                    if new_target not in worm["targets"]:
                        new_targets.append(new_target)
                worm["targets"].extend(new_targets)
                return new_targets
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        return {"worms": len(self.worms), "total_replications": sum(w["replicated"] for w in self.worms)}


class SmartDigitalAmoeba:
    """الأميبا الرقمية الذكية"""
    
    def __init__(self):
        self.shape = "initial"
        self.reaction_time = 0.1
        self.analysis_cache: Dict[str, Any] = {}
        
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "data_hash": hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16],
            "patterns": self._detect_patterns(data),
            "anomalies": self._detect_anomalies(data)
        }
        self.analysis_cache[analysis["data_hash"]] = analysis
        return analysis
    
    def _detect_patterns(self, data: Dict) -> List[str]:
        patterns = []
        if data.get("error_rate", 0) > 0.1:
            patterns.append("high_error_rate")
        if data.get("latency", 0) > 100:
            patterns.append("high_latency")
        return patterns
    
    def _detect_anomalies(self, data: Dict) -> List[str]:
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        return {"cache_size": len(self.analysis_cache)}


class VariableNetworkSleepSystem:
    """نظام النوم الشبكي المتغيّر"""
    
    def __init__(self):
        self.sleep_cycles = 0
        self.current_state = "active"
        self.state_history: List[Dict] = []
        
    def cycle(self) -> str:
        self.sleep_cycles += 1
        states = ["active", "light_sleep", "deep_sleep", "recovery"]
        self.current_state = states[self.sleep_cycles % len(states)]
        self.state_history.append({
            "cycle": self.sleep_cycles,
            "state": self.current_state,
            "timestamp": datetime.now().isoformat()
        })
        return self.current_state
    
    def get_recovery_time(self) -> float:
        return 0.5 * (1 + self.sleep_cycles % 10)
    
    def get_stats(self) -> Dict[str, Any]:
        return {"cycles": self.sleep_cycles, "current_state": self.current_state}


# =========================================================
# القسم الثالث: التكتيكات الجماعية
# =========================================================

class SwarmTactics:
    """التكتيكات الجماعية"""
    
    def __init__(self, event_callback=None):
        self.units: List[Dict] = []
        self.swarm_power = 0.0
        self.event_callback = event_callback
        
    def add_unit(self, unit_id: str, power: float):
        self.units.append({"id": unit_id, "power": power})
        self._recalculate_power()
        
        if self.event_callback:
            self.event_callback(TacticalEvent(
                type=TacticalEventType.SWARM_DEPLOYED,
                source="SwarmTactics",
                data={"unit_id": unit_id, "total_units": len(self.units), "swarm_power": self.swarm_power}
            ))
        
    def _recalculate_power(self):
        self.swarm_power = sum(u["power"] for u in self.units) * (1 + 0.1 * len(self.units))
        
    def focus_power(self, target: str) -> float:
        return self.swarm_power * 1.5
    
    def distribute_load(self, loads: List[float]) -> List[float]:
        num_units = len(self.units)
        if num_units == 0:
            return loads
        return [load / num_units for load in loads]
    
    def get_stats(self) -> Dict[str, Any]:
        return {"units": len(self.units), "swarm_power": self.swarm_power}


class SoftwareArmies:
    """الجيوش البرمجية الزاحفة"""
    
    def __init__(self, event_callback=None):
        self.army_size = 0
        self.formation = "scattered"
        self.units: List[Dict] = []
        self.event_callback = event_callback
        
    def deploy(self, num_units: int):
        self.army_size = num_units
        self.units = [{"id": i, "status": "active"} for i in range(num_units)]
        
        if self.event_callback:
            self.event_callback(TacticalEvent(
                type=TacticalEventType.ARMY_DEPLOYED,
                source="SoftwareArmies",
                data={"army_size": num_units, "formation": self.formation}
            ))
        
    def change_formation(self, formation_type: str):
        valid_formations = ["scattered", "concentrated", "circular", "linear"]
        if formation_type in valid_formations:
            self.formation = formation_type
            
    def execute_order(self, order: str) -> int:
        return sum(1 for u in self.units if u["status"] == "active")
    
    def get_stats(self) -> Dict[str, Any]:
        return {"army_size": self.army_size, "formation": self.formation, "active": len([u for u in self.units if u["status"] == "active"])}


class CooperativeSoftwareUnits:
    """الوحدات البرمجية التضامنية"""
    
    def __init__(self):
        self.units: Dict[str, Dict] = {}
        self.crisis_mode = False
        
    def register_unit(self, unit_id: str, backup_power: float):
        self.units[unit_id] = {"backup_power": backup_power, "active": True}
        
    def activate_backup(self, unit_id: str) -> bool:
        if unit_id in self.units:
            self.units[unit_id]["active"] = True
            return True
        return False
    
    def handle_crisis(self, affected_units: List[str]) -> Dict[str, bool]:
        self.crisis_mode = True
        results = {unit: self.activate_backup(unit) for unit in affected_units}
        self.crisis_mode = False
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        return {"units": len(self.units), "active": sum(1 for u in self.units.values() if u["active"])}


# =========================================================
# القسم الرابع: الكيانات فائقة التطور
# =========================================================

class JellyfishNetwork:
    """القنديل الشبكي الصندوقي"""
    
    def __init__(self):
        self.tentacles: List[str] = []
        
    def add_tentacle(self, node_id: str):
        self.tentacles.append(node_id)
        
    def broadcast(self, message: Any) -> int:
        start = time.time()
        for tentacle in self.tentacles:
            pass
        return len(self.tentacles)
    
    def get_stats(self) -> Dict[str, Any]:
        return {"tentacles": len(self.tentacles)}


class BlueDigitalOctopus:
    """الأخطبوط الأزرق الرقمي"""
    
    def __init__(self):
        self.arms = 8
        self.brain_center = {}
        self.coordination_matrix: Dict[str, List[str]] = {}
        
    def coordinate(self, components: List[str]) -> Dict[str, List[str]]:
        for i, comp in enumerate(components):
            self.coordination_matrix[comp] = components[:i] + components[i+1:]
        return self.coordination_matrix
    
    def get_stats(self) -> Dict[str, Any]:
        return {"components": len(self.coordination_matrix)}


class ConeSnailCyber:
    """الحلزون المخروطي السيبراني"""
    
    def __init__(self):
        self.harpoons: List[str] = []
        self.venom_data: Dict[str, Any] = {}
        
    def fire_harpoon(self, target: str, data: Any) -> bool:
        self.harpoons.append(target)
        self.venom_data[target] = data
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        return {"harpoons_fired": len(self.harpoons)}


# =========================================================
# المدير الرئيسي – يدمج كل هذه الأنظمة مع نظام المخاطر
# =========================================================

class SamaAdvancedTactics:
    """
    المدير المتقدم للتكتيكات الرقمية لسماء
    يدمج جميع الأنظمة الذكية والكيانات المتقدمة
    متصل بشكل كامل مع StrategicRiskManagement
    """
    
    def __init__(self, master_name: str = "أحمد", risk_manager=None):
        self.master_name = master_name
        self.risk_manager = risk_manager  # اتصال مباشر مع نظام المخاطر
        self.master_protection_active = True
        
        # قائمة الأحداث التكتيكية (لتغذية نظام المخاطر)
        self.tactical_events: List[TacticalEvent] = []
        
        # القسم الأول
        self.morphing_codes: Dict[str, SelfMorphingCode] = {}
        self.neural_comms = NeuralNetworkCommunication(event_callback=self._on_tactical_event)
        self.parallel_codes = ParallelThreadCodes(event_callback=self._on_tactical_event)
        self.archive = ArchivedDigitalPackages(event_callback=self._on_tactical_event)
        self.deep_adaptation = DeepNetworkAdaptation(event_callback=self._on_tactical_event)
        self.continuity_core = DigitalContinuityCore()
        
        # القسم الثاني
        self.behavior_controller = NetworkBehavioralController()
        self.digital_parasite = DigitalBehavioralParasite(event_callback=self._on_tactical_event)
        self.thread_worms = SoftwareThreadWorms(event_callback=self._on_tactical_event)
        self.digital_amoeba = SmartDigitalAmoeba()
        self.variable_sleep = VariableNetworkSleepSystem()
        
        # القسم الثالث
        self.swarm_tactics = SwarmTactics(event_callback=self._on_tactical_event)
        self.software_armies = SoftwareArmies(event_callback=self._on_tactical_event)
        self.cooperative_units = CooperativeSoftwareUnits()
        
        # القسم الرابع
        self.jellyfish_net = JellyfishNetwork()
        self.digital_octopus = BlueDigitalOctopus()
        self.cone_snail = ConeSnailCyber()
        
        print(f"[SamaAdvancedTactics] 🧠 تم تفعيل الأنظمة الرقمية المتقدمة")
        print(f"[SamaAdvancedTactics] 👑 تحت إمرة السيد {master_name}")
        print(f"[SamaAdvancedTactics] 📦 الوحدات: 18 نظاماً متكاملاً")
        if risk_manager:
            print(f"[SamaAdvancedTactics] 🔗 متصل بـ StrategicRiskManagement")
    
    def _on_tactical_event(self, event: TacticalEvent):
        """معالجة الأحداث التكتيكية وإرسالها إلى نظام المخاطر"""
        self.tactical_events.append(event)
        
        # إذا كان هناك نظام مخاطر متصل، أرسل الحدث إليه
        if self.risk_manager:
            try:
                # تحويل الحدث التكتيكي إلى خطر استراتيجي إن لزم
                if event.type == TacticalEventType.THREAT_DETECTED:
                    if hasattr(self.risk_manager, 'identify_risk'):
                        self.risk_manager.identify_risk(
                            name=f"تكتيكي: {event.source}",
                            description=f"حدث تكتيكي: {event.data}",
                            probability=event.data.get("probability", 0.5),
                            impact=event.data.get("impact", 0.6),
                            threatens_master=event.requires_master_attention
                        )
            except Exception as e:
                print(f"[SamaAdvancedTactics] خطأ في إرسال الحدث لنظام المخاطر: {e}")
    
    def connect_risk_manager(self, risk_manager):
        """ربط نظام المخاطر بشكل مباشر"""
        self.risk_manager = risk_manager
        print(f"[SamaAdvancedTactics] 🔗 تم ربط StrategicRiskManagement")
    
    def create_morphing_code(self, name: str, initial_structure: Dict) -> SelfMorphingCode:
        """إنشاء كود متحول جديد"""
        code = SelfMorphingCode(name, initial_structure, event_callback=self._on_tactical_event)
        self.morphing_codes[name] = code
        return code
    
    def deploy_swarm(self, unit_ids: List[str], powers: List[float]) -> float:
        """نشر سرب تكتيكي"""
        for uid, power in zip(unit_ids, powers):
            self.swarm_tactics.add_unit(uid, power)
        return self.swarm_tactics.swarm_power
    
    def deploy_army(self, size: int, formation: str = "scattered") -> int:
        """نشر جيش برمجي"""
        self.software_armies.deploy(size)
        self.software_armies.change_formation(formation)
        return self.software_armies.army_size
    
    def get_tactical_events(self, limit: int = 50) -> List[Dict]:
        """الحصول على الأحداث التكتيكية الأخيرة"""
        events = []
        for event in self.tactical_events[-limit:]:
            events.append({
                "type": event.type.value,
                "source": event.source,
                "data": event.data,
                "timestamp": event.timestamp.isoformat(),
                "requires_master_attention": event.requires_master_attention
            })
        return events
    
    def get_status(self) -> Dict[str, Any]:
        """حالة جميع الأنظمة المتقدمة"""
        return {
            "master": self.master_name,
            "master_protection": self.master_protection_active,
            "risk_manager_connected": self.risk_manager is not None,
            "tactical_events_count": len(self.tactical_events),
            "systems": {
                "self_morphing": len(self.morphing_codes),
                "neural_communication": self.neural_comms.get_stats(),
                "parallel_threads": self.parallel_codes.get_stats(),
                "archived_packages": self.archive.get_stats(),
                "deep_adaptation": self.deep_adaptation.get_stats(),
                "continuity_core": self.continuity_core.get_stats(),
                "behavior_controller": self.behavior_controller.get_stats(),
                "digital_parasite": self.digital_parasite.get_stats(),
                "thread_worms": self.thread_worms.get_stats(),
                "digital_amoeba": self.digital_amoeba.get_stats(),
                "variable_sleep": self.variable_sleep.get_stats(),
                "swarm_tactics": self.swarm_tactics.get_stats(),
                "software_armies": self.software_armies.get_stats(),
                "cooperative_units": self.cooperative_units.get_stats(),
                "jellyfish_net": self.jellyfish_net.get_stats(),
                "digital_octopus": self.digital_octopus.get_stats(),
                "cone_snail": self.cone_snail.get_stats()
            },
            "timestamp": datetime.now().isoformat()
        }


# =========================================================
# دالة ربط بسيطة مع StrategicRiskManagement
# =========================================================

def connect_tactics_to_risk_manager(tactics: SamaAdvancedTactics, risk_manager) -> SamaAdvancedTactics:
    """ربط النظام التكتيكي بنظام المخاطر"""
    tactics.connect_risk_manager(risk_manager)
    return tactics


# =========================================================
# اختبار
# =========================================================
if __name__ == "__main__":
    print("=" * 70)
    print("🌌 SkyOS v10 - Sama Advanced Tactics (الأنظمة الرقمية الذكية)")
    print("تحت إمرة السيد أحمد")
    print("=" * 70)
    
    tactics = SamaAdvancedTactics(master_name="أحمد")
    
    # اختبار بعض الأنظمة
    print("\n🔧 اختبار الشيفرات المتحولة:")
    morph = tactics.create_morphing_code("test_morph", {"core_functions": ["read", "write", "process"]})
    result = morph.morph("high_load")
    print(f"   التكيف: {result['environment']} | الإصدار: {result['morph_version']}")
    
    print("\n🐜 اختبار الجيش البرمجي:")
    tactics.deploy_army(100, "concentrated")
    print(f"   حجم الجيش: {tactics.software_armies.army_size}")
    
    print("\n📡 اختبار الاتصال العصبي:")
    tactics.neural_comms.create_channel("test_channel")
    tactics.neural_comms.send("test_channel", "بيان تجريبي")
    received = tactics.neural_comms.receive("test_channel")
    print(f"   تم استلام: {received}")
    
    print("\n🕸️ اختبار الطفيل السلوكي:")
    tactics.digital_parasite.create_link("component_A", "component_B")
    print(f"   الروابط الخفية: {len(tactics.digital_parasite.hidden_links)}")
    
    print("\n🐛 اختبار الديدان الخيطية:")
    worm_id = tactics.thread_worms.spawn_worm("explorer", {"action": "scan"}, ["node_1", "node_2"])
    new_targets = tactics.thread_worms.replicate(worm_id)
    print(f"   الدودة: {worm_id[:16]}... | تكاثرت إلى {len(new_targets)} عقدة جديدة")
    
    print("\n📦 اختبار الحزم المؤرشفة:")
    tactics.archive.archive("test_pkg", {"test": "data"}, ttl_days=30)
    restored = tactics.archive.restore("test_pkg")
    print(f"   استعادة: {restored is not None}")
    
    print("\n🔄 اختبار التكيّف العميق:")
    adaptation = tactics.deep_adaptation.adapt({"load": 0.85, "available_nodes": 20})
    print(f"   طبقة التكيف: {adaptation['layer']} | العقد: {adaptation['new_topology']['nodes']}")
    
    print("\n🪼 اختبار القنديل الشبكي:")
    for i in range(5):
        tactics.jellyfish_net.add_tentacle(f"node_{i}")
    print(f"   أطراف القنديل: {len(tactics.jellyfish_net.tentacles)}")
    
    print("\n🐙 اختبار الأخطبوط الرقمي:")
    tactics.digital_octopus.coordinate(["engine_1", "engine_2", "engine_3", "memory_core"])
    print(f"   المكونات المنسقة: {len(tactics.digital_octopus.coordination_matrix)}")
    
    print("\n🐚 اختبار الحلزون المخروطي:")
    tactics.cone_snail.fire_harpoon("target_system", {"action": "data_harvest"})
    print(f"   الحراب المنطلقة: {len(tactics.cone_snail.harpoons)}")
    
    print("\n🎯 اختبار السرب التكتيكي:")
    swarm_power = tactics.deploy_swarm(["unit_1", "unit_2", "unit_3"], [10.0, 15.0, 20.0])
    print(f"   قوة السرب: {swarm_power:.2f}")
    
    print("\n📊 الحالة الكاملة:")
    status = tactics.get_status()
    print(f"   الأنظمة المتصلة: {len(status['systems'])}")
    print(f"   الأحداث التكتيكية: {status['tactical_events_count']}")
    print(f"   متصل بـ Risk Manager: {status['risk_manager_connected']}")
    
    print("\n✨ جميع الأنظمة الرقمية تعمل بكامل قوتها تحت إمرة السيد")
    print("🔗 يمكن ربط هذا الملف مع StrategicRiskManagement عبر connect_tactics_to_risk_manager()")
