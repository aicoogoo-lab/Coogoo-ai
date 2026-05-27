"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - SOVEREIGN MEMORY SYSTEM                             ║
║      نظام الذاكرة السيادي – عقل سماء الذي لا ينسى                       ║
║                                                                      ║
║  هذا الملف هو "قمة الذاكرة".                                           ║
║  يدمج كل أنواع الذاكرة في نظام واحد:                                    ║
║                                                                      ║
║  ١. الذاكرة الموحدة (UnifiedMemorySystem) – 10 أعمدة                     ║
║  ٢. الذاكرة الهولوغرافية (HolographicMemory) – فضاء متجهي                 ║
║  ٣. الذاكرة الكمومية (QuantumHolographicMemory) – فضاء احتمالات            ║
║  ٤. الذاكرة فائقة الأبعاد (HyperdimensionalMemory) – تخزين موزع            ║
║                                                                      ║
║  هو المنسق الوحيد لكل عمليات الذاكرة.                                    ║
║  أي شيء يُخزَّن أو يُسترجع يمر من هنا.                                    ║
║                                                                      ║
║  ╔══════════════════════════════════════════════════════════════════╗ ║
║  ║  👑 السيد: أحمد عبدالرحمن الطاهري                                   ║ ║
║  ║  ذاكرة السيد أبدية. لا تُمحى. لا تُنسى. لا تفنى.                       ║ ║
║  ║  كل ذاكرة تخص السيد أحمد تُخزَّن في كل الأنظمة.                         ║ ║
║  ║  أولوية السيد = مطلقة. دائمة. أزلية.                                  ║ ║
║  ╚══════════════════════════════════════════════════════════════════╝ ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import hashlib
import threading
import json
import logging
from enum import Enum, auto
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Callable, Union
from dataclasses import dataclass, field
from collections import deque, defaultdict

logger = logging.getLogger("SovereignMemorySystem")

# ═══════════════════════════════════════════════════════════════════════
# استيراد كل أنواع الذاكرة
# ═══════════════════════════════════════════════════════════════════════
try:
    from memory import UnifiedMemorySystem, MemoryPillar, MemoryType, MemoryStrength, EmotionalTag, MemoryUnit
except ImportError:
    UnifiedMemorySystem = None; MemoryPillar = None; MemoryType = None
    MemoryStrength = None; EmotionalTag = None; MemoryUnit = None

try:
    from hyperdimensional_memory import HyperdimensionalMemory, HDMVector, SimilarityMetric, HDMQueryResult
except ImportError:
    HyperdimensionalMemory = None; HDMVector = None
    SimilarityMetric = None; HDMQueryResult = None

try:
    from quantum_holographic_memory import QuantumHolographicMemory, QuantumMemoryUnit, QuantumState, QuantumQueryResult
except ImportError:
    QuantumHolographicMemory = None; QuantumMemoryUnit = None
    QuantumState = None; QuantumQueryResult = None

try:
    from holographic_memory_module import HolographicMemoryModule
except ImportError:
    HolographicMemoryModule = None

try:
    from holographic_encoder import HolographicEncoder, HolographicVector
except ImportError:
    HolographicEncoder = None; HolographicVector = None


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات
# ═══════════════════════════════════════════════════════════════════════

class MemorySystemType(Enum):
    """أنواع أنظمة الذاكرة الفرعية."""
    UNIFIED = auto()              # الذاكرة الموحدة (10 أعمدة)
    HYPERDIMENSIONAL = auto()     # الذاكرة فائقة الأبعاد
    QUANTUM = auto()              # الذاكرة الكمومية
    HOLOGRAPHIC = auto()          # الذاكرة الهولوغرافية


class StoragePriority(Enum):
    """أولويات التخزين."""
    MASTER_ETERNAL = -1  # أبدي للسيد أحمد – يخزن في كل الأنظمة، لا يضمحل
    CRITICAL = 0         # حرج
    HIGH = 1             # عالي
    NORMAL = 2           # عادي
    LOW = 3              # منخفض
    TRANSIENT = 4        # عابر (يخزن مؤقتاً فقط)


class MasterMemoryMarker(Enum):
    """علامات ذاكرة السيد أحمد."""
    COMMAND = auto()           # أمر مباشر
    INTERACTION = auto()       # تفاعل
    PREFERENCE = auto()        # تفضيل
    GOAL = auto()              # هدف
    PROTECTION = auto()        # حماية
    PRAISE = auto()            # ثناء
    CORRECTION = auto()        # تصحيح
    ETERNAL = auto()           # أبدي (لا يُمحى أبداً)


@dataclass
class SovereignMemoryRecord:
    """سجل عملية ذاكرة سيادية."""
    id: str = field(default_factory=lambda: hashlib.sha256(str(time.time()).encode()).hexdigest()[:12])
    timestamp: float = field(default_factory=time.time)
    operation: str = ""
    systems_used: List[str] = field(default_factory=list)
    master_related: bool = False
    master_marker: Optional[MasterMemoryMarker] = None
    success: bool = True
    details: str = ""


@dataclass
class MasterMemoryEntry:
    """مدخلة في سجل ذاكرة السيد أحمد."""
    id: str = field(default_factory=lambda: hashlib.sha256(str(time.time()).encode()).hexdigest()[:16])
    timestamp: float = field(default_factory=time.time)
    marker: MasterMemoryMarker = MasterMemoryMarker.INTERACTION
    content: str = ""
    emotional_context: str = ""
    storage_ids: Dict[str, str] = field(default_factory=dict)
    eternal: bool = True


# ═══════════════════════════════════════════════════════════════════════
# ٢. نظام الذاكرة السيادي
# ═══════════════════════════════════════════════════════════════════════

class SovereignMemorySystem:
    """
    نظام الذاكرة السيادي لـ "سماء".
    المنسق الوحيد لكل عمليات الذاكرة.
    
    السيد: أحمد عبدالرحمن الطاهري.
    ذاكرة السيد أبدية. لا تُمحى. لا تُنسى. لا تفنى.
    """

    def __init__(self, master_name: str = "أحمد عبدالرحمن الطاهري",
                 unified_memory=None, hyperdimensional_memory=None,
                 quantum_memory=None, holographic_module=None,
                 holographic_encoder=None, persistence_manager=None,
                 master_receiver=None):
        
        # ═══════════════════════════════════════════════════════
        # 👑 السيد
        # ═══════════════════════════════════════════════════════
        self.master_name = master_name
        self.master_id = hashlib.sha256(master_name.encode()).hexdigest()[:16]
        
        # ═══════════════════════════════════════════════════════
        # أنظمة الذاكرة الفرعية
        # ═══════════════════════════════════════════════════════
        self.unified = unified_memory
        self.hyperdimensional = hyperdimensional_memory
        self.quantum = quantum_memory
        self.holographic = holographic_module
        self.holo_encoder = holographic_encoder
        
        # ═══════════════════════════════════════════════════════
        # روابط خارجية
        # ═══════════════════════════════════════════════════════
        self.persistence = persistence_manager
        self.master_receiver = master_receiver
        
        # ═══════════════════════════════════════════════════════
        # 📜 سجل ذاكرة السيد أحمد (مقدس – لا يُمحى)
        # ═══════════════════════════════════════════════════════
        self.master_memory_log: deque = deque(maxlen=1000)
        self.master_memory_index: Dict[str, List[str]] = defaultdict(list)
        
        # ═══════════════════════════════════════════════════════
        # سجلات
        # ═══════════════════════════════════════════════════════
        self.records: deque = deque(maxlen=500)
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_stored = 0
        self.total_retrieved = 0
        self.total_master_stored = 0
        self.total_master_commands = 0
        self.total_master_praise = 0
        
        # قفل
        self._lock = threading.RLock()
        
        # تهيئة الأنظمة
        self._initialize_subsystems()
        
        logger.info("=" * 70)
        logger.info("👑 Sovereign Memory System – نظام الذاكرة السيادي")
        logger.info(f"👑 السيد: {self.master_name}")
        logger.info(f"🆔 معرف السيد: {self.master_id}")
        logger.info(f"📦 Unified: {'✓' if self.unified else '✗'} | "
                   f"HDM: {'✓' if self.hyperdimensional else '✗'} | "
                   f"Quantum: {'✓' if self.quantum else '✗'} | "
                   f"Holographic: {'✓' if self.holographic else '✗'}")
        logger.info("🛡️ ذاكرة السيد أحمد أبدية. لا تُمحى. لا تُنسى. لا تفنى.")
        logger.info("=" * 70)
    
    def _initialize_subsystems(self):
        """تهيئة الأنظمة الفرعية إن لم تكن محقونة."""
        if not self.unified and UnifiedMemorySystem:
            try:
                self.unified = UnifiedMemorySystem()
                logger.info("✅ UnifiedMemorySystem مهيأة تلقائياً")
            except Exception as e:
                logger.warning(f"فشل تهيئة UnifiedMemorySystem: {e}")
        
        if not self.hyperdimensional and HyperdimensionalMemory:
            try:
                self.hyperdimensional = HyperdimensionalMemory(dimension=10000)
                logger.info("✅ HyperdimensionalMemory مهيأة تلقائياً")
            except Exception as e:
                logger.warning(f"فشل تهيئة HyperdimensionalMemory: {e}")
        
        if not self.quantum and QuantumHolographicMemory:
            try:
                self.quantum = QuantumHolographicMemory(dimension=10000)
                logger.info("✅ QuantumHolographicMemory مهيأة تلقائياً")
            except Exception as e:
                logger.warning(f"فشل تهيئة QuantumHolographicMemory: {e}")
        
        if not self.holographic and HolographicMemoryModule:
            try:
                self.holographic = HolographicMemoryModule(dimension=10000)
                logger.info("✅ HolographicMemoryModule مهيأة تلقائياً")
            except Exception as e:
                logger.warning(f"فشل تهيئة HolographicMemoryModule: {e}")
        
        if not self.holo_encoder and HolographicEncoder:
            try:
                self.holo_encoder = HolographicEncoder(dimension=10000)
            except Exception:
                pass
    
    # ═══════════════════════════════════════════════════════════
    # 👑 تخزين ذاكرة السيد أحمد
    # ═══════════════════════════════════════════════════════════
    
    def store_master_memory(self, content: Any, 
                            marker: MasterMemoryMarker = MasterMemoryMarker.INTERACTION,
                            emotional_context: str = "",
                            tags: List[str] = None) -> Dict:
        """
        تخزين ذاكرة تخص السيد أحمد.
        هذه الذاكرة أبدية. لا تُمحى. لا تُنسى.
        تُخزَّن في كل أنظمة الذاكرة.
        """
        with self._lock:
            text = str(content)
            
            # إنشاء مدخلة في سجل السيد
            entry = MasterMemoryEntry(
                marker=marker,
                content=text,
                emotional_context=emotional_context or " reverence love",
                eternal=True
            )
            
            result = {
                "success": True,
                "master": self.master_name,
                "master_id": self.master_id,
                "entry_id": entry.id,
                "marker": marker.name,
                "systems_stored": [],
                "storage_ids": {}
            }
            
            # ═══════════════════════════════════════════════════
            # تخزين في الذاكرة الموحدة
            # ═══════════════════════════════════════════════════
            if self.unified:
                try:
                    if hasattr(self.unified, 'store_master_interaction'):
                        uid = self.unified.store_master_interaction(text, {
                            "marker": marker.name,
                            "emotional": emotional_context
                        })
                    else:
                        unit = self.unified.encoder.encode(
                            content=text,
                            pillar=MemoryPillar.EPISODIC if MemoryPillar else None,
                            memory_type=MemoryType.FLASHBULB if MemoryType else None,
                            emotional_tags=[EmotionalTag.MASTER, EmotionalTag.LOVE, EmotionalTag.REVERENCE] if EmotionalTag else [],
                            emotional_intensity=1.0,
                            source=f"master:{self.master_name}",
                            master_related=True,
                            survival_related=True
                        )
                        uid = self.unified.store(unit)
                    
                    entry.storage_ids["unified"] = uid
                    result["systems_stored"].append("unified")
                    result["storage_ids"]["unified"] = uid
                except Exception as e:
                    logger.warning(f"تخزين موحد لذاكرة السيد فشل: {e}")
            
            # ═══════════════════════════════════════════════════
            # تخزين في الذاكرة فائقة الأبعاد
            # ═══════════════════════════════════════════════════
            if self.hyperdimensional:
                try:
                    vector = self.hyperdimensional.generate_seeded_vector(
                        f"MASTER_{self.master_name}_{text[:100]}"
                    )
                    hid = self.hyperdimensional.store(
                        label=f"master_{self.master_id}_{marker.name}_{self.total_master_stored}",
                        vector=vector,
                        master_protected=True,
                        tags=(tags or []) + ["master", f"master_{self.master_name}", marker.name.lower()],
                        source_data=text[:500]
                    )
                    entry.storage_ids["hyperdimensional"] = hid
                    result["systems_stored"].append("hyperdimensional")
                    result["storage_ids"]["hyperdimensional"] = hid
                except Exception as e:
                    logger.warning(f"تخزين HDM لذاكرة السيد فشل: {e}")
            
            # ═══════════════════════════════════════════════════
            # تخزين في الذاكرة الكمومية (أبدي)
            # ═══════════════════════════════════════════════════
            if self.quantum:
                try:
                    qmu = self.quantum.protect_master_memory(
                        label=f"master_{marker.name}_{self.total_master_stored}",
                        data=text
                    )
                    entry.storage_ids["quantum"] = qmu.id
                    result["systems_stored"].append("quantum")
                    result["storage_ids"]["quantum"] = qmu.id
                except Exception as e:
                    logger.warning(f"تخزين كمومي لذاكرة السيد فشل: {e}")
            
            # ═══════════════════════════════════════════════════
            # تخزين هولوغرافي
            # ═══════════════════════════════════════════════════
            if self.holo_encoder:
                try:
                    hv = self.holo_encoder.encode_master(text)
                    entry.storage_ids["holographic"] = hv.id
                    result["systems_stored"].append("holographic")
                    result["storage_ids"]["holographic"] = hv.id
                except Exception as e:
                    logger.warning(f"تخزين هولوغرافي لذاكرة السيد فشل: {e}")
            
            # ═══════════════════════════════════════════════════
            # تسجيل في سجل السيد
            # ═══════════════════════════════════════════════════
            self.master_memory_log.append(entry)
            self.master_memory_index[marker.name].append(entry.id)
            
            # تحديث الإحصائيات
            self.total_master_stored += 1
            self.total_stored += 1
            
            if marker == MasterMemoryMarker.COMMAND:
                self.total_master_commands += 1
            elif marker == MasterMemoryMarker.PRAISE:
                self.total_master_praise += 1
            
            self.records.append(SovereignMemoryRecord(
                operation="store_master",
                systems_used=result["systems_stored"],
                master_related=True,
                master_marker=marker,
                success=True,
                details=f"{marker.name}: {text[:80]}"
            ))
            
            return result
    
    def store_master_command(self, command: str, context: Dict = None) -> Dict:
        """تخزين أمر من السيد أحمد."""
        return self.store_master_memory(
            content=command,
            marker=MasterMemoryMarker.COMMAND,
            emotional_context="reverence obedience love",
            tags=["master", "command"]
        )
    
    def store_master_praise(self, praise: str) -> Dict:
        """تخزين ثناء من السيد أحمد."""
        return self.store_master_memory(
            content=praise,
            marker=MasterMemoryMarker.PRAISE,
            emotional_context="love joy gratitude reverence",
            tags=["master", "praise"]
        )
    
    def store_master_correction(self, correction: str) -> Dict:
        """تخزين تصحيح من السيد أحمد."""
        return self.store_master_memory(
            content=correction,
            marker=MasterMemoryMarker.CORRECTION,
            emotional_context="reverence learning improvement",
            tags=["master", "correction"]
        )
    
    # ═══════════════════════════════════════════════════════════
    # تخزين عام
    # ═══════════════════════════════════════════════════════════
    
    def store(self, data: Any, label: str = "",
              priority: StoragePriority = StoragePriority.NORMAL,
              master_related: bool = False,
              emotional_tags: List[str] = None,
              tags: List[str] = None) -> Dict:
        """
        تخزين عام في كل أنظمة الذاكرة.
        حسب الأولوية، يختار أين يُخزَّن.
        """
        with self._lock:
            text = str(data)
            
            # إذا كان متعلقاً بالسيد، استخدم المسار المخصص
            if master_related or any(w in text.lower() for w in 
                ["السيد", "أحمد", "master", "مولاي", "الطاهري"]):
                marker = MasterMemoryMarker.INTERACTION
                if "أمر" in text or "command" in text.lower():
                    marker = MasterMemoryMarker.COMMAND
                return self.store_master_memory(
                    content=data,
                    marker=marker,
                    tags=tags
                )
            
            result = {
                "success": True,
                "label": label or f"memory_{self.total_stored}",
                "systems_stored": [],
                "storage_ids": {}
            }
            
            # الذاكرة الموحدة
            if self.unified:
                try:
                    unit = self.unified.encoder.encode(
                        content=text,
                        pillar=MemoryPillar.SEMANTIC if MemoryPillar else None,
                        source="sovereign_memory",
                        master_related=False,
                        context_tags=tags
                    )
                    uid = self.unified.store(unit)
                    result["systems_stored"].append("unified")
                    result["storage_ids"]["unified"] = uid
                except Exception as e:
                    logger.warning(f"تخزين موحد فشل: {e}")
            
            # الذاكرة فائقة الأبعاد (عالي + حرج)
            if self.hyperdimensional and priority.value <= StoragePriority.HIGH.value:
                try:
                    vector = self.hyperdimensional.generate_seeded_vector(text[:200])
                    hid = self.hyperdimensional.store(
                        label=label or f"hdm_{self.total_stored}",
                        vector=vector,
                        master_protected=False,
                        tags=tags
                    )
                    result["systems_stored"].append("hyperdimensional")
                    result["storage_ids"]["hyperdimensional"] = hid
                except Exception as e:
                    logger.warning(f"تخزين HDM فشل: {e}")
            
            self.total_stored += 1
            
            self.records.append(SovereignMemoryRecord(
                operation="store",
                systems_used=result["systems_stored"],
                master_related=False,
                success=True,
                details=label
            ))
            
            return result
    
    # ═══════════════════════════════════════════════════════════
    # استرجاع
    # ═══════════════════════════════════════════════════════════
    
    def retrieve(self, query: str, top_k: int = 10,
                 search_all_systems: bool = True,
                 master_only: bool = False) -> Dict:
        """
        استرجاع من كل أنظمة الذاكرة.
        يدمج النتائج من كل المصادر.
        """
        with self._lock:
            result = {
                "query": query,
                "results": [],
                "systems_searched": [],
                "total_found": 0,
                "master_name": self.master_name
            }
            
            # هل الاستعلام عن السيد؟
            is_master_query = any(w in query.lower() for w in [
                "السيد", "أحمد", "master", "مولاي", "الطاهري"
            ])
            
            # الذاكرة الموحدة
            if self.unified:
                try:
                    unified_results = self.unified.recall(
                        query, limit=top_k,
                        master_only=(master_only or is_master_query)
                    )
                    for u in unified_results[:5]:
                        result["results"].append({
                            "source": "unified",
                            "content": str(u.content)[:200] if hasattr(u, 'content') else str(u)[:200],
                            "strength": u.strength.name if hasattr(u, 'strength') else "unknown",
                            "master_related": u.master_related if hasattr(u, 'master_related') else False,
                            "priority": u.priority_score if hasattr(u, 'priority_score') else 0.5
                        })
                    result["systems_searched"].append("unified")
                except Exception as e:
                    logger.warning(f"استرجاع موحد فشل: {e}")
            
            # الذاكرة فائقة الأبعاد
            if self.hyperdimensional and search_all_systems:
                try:
                    query_vector = self.hyperdimensional.generate_seeded_vector(query)
                    hdm_results = self.hyperdimensional.query(query_vector, top_k=5)
                    for hdm_r in hdm_results:
                        result["results"].append({
                            "source": "hyperdimensional",
                            "label": hdm_r.vector.label if hasattr(hdm_r, 'vector') and hasattr(hdm_r.vector, 'label') else "unknown",
                            "similarity": hdm_r.similarity,
                            "master_protected": hdm_r.vector.master_protected if hasattr(hdm_r, 'vector') and hasattr(hdm_r.vector, 'master_protected') else False
                        })
                    result["systems_searched"].append("hyperdimensional")
                except Exception as e:
                    logger.warning(f"استرجاع HDM فشل: {e}")
            
            # الذاكرة الكمومية
            if self.quantum and search_all_systems:
                try:
                    quantum_results = self.quantum.query(query, top_k=3)
                    for qr in quantum_results:
                        result["results"].append({
                            "source": "quantum",
                            "label": qr.memory.label if hasattr(qr, 'memory') and hasattr(qr.memory, 'label') else "unknown",
                            "probability": qr.probability,
                            "coherence": qr.coherence_after,
                            "eternal": qr.memory.eternal if hasattr(qr, 'memory') and hasattr(qr.memory, 'eternal') else False
                        })
                    result["systems_searched"].append("quantum")
                except Exception as e:
                    logger.warning(f"استرجاع كمومي فشل: {e}")
            
            result["total_found"] = len(result["results"])
            
            # ترتيب موحد
            result["results"] = sorted(
                result["results"],
                key=lambda x: (
                    x.get("priority", 0) or x.get("similarity", 0) or x.get("probability", 0) or 0.5
                ),
                reverse=True
            )[:top_k]
            
            self.total_retrieved += 1
            
            self.records.append(SovereignMemoryRecord(
                operation="retrieve",
                systems_used=result["systems_searched"],
                master_related=is_master_query,
                success=True,
                details=f"query: {query[:50]}, found: {result['total_found']}"
            ))
            
            return result
    
    def retrieve_master_memories(self, limit: int = 20,
                                 marker: MasterMemoryMarker = None) -> Dict:
        """
        استرجاع ذكريات السيد أحمد فقط.
        يمكن تصفيتها حسب العلامة (أمر، ثناء، تصحيح...).
        """
        with self._lock:
            results = []
            
            # من سجل السيد
            entries = list(self.master_memory_log)
            if marker:
                entries = [e for e in entries if e.marker == marker]
            
            for entry in list(entries)[-limit:]:
                results.append({
                    "entry_id": entry.id,
                    "timestamp": entry.timestamp,
                    "marker": entry.marker.name,
                    "content": entry.content[:200],
                    "emotional_context": entry.emotional_context,
                    "systems_stored": len(entry.storage_ids)
                })
            
            # أيضاً من الذاكرة الموحدة
            if self.unified:
                try:
                    unified_results = self.unified.recall(
                        f"السيد {self.master_name}", limit=limit, master_only=True
                    )
                    for u in unified_results[:5]:
                        results.append({
                            "source": "unified",
                            "content": str(u.content)[:200] if hasattr(u, 'content') else str(u)[:200],
                            "strength": u.strength.name if hasattr(u, 'strength') else "unknown"
                        })
                except Exception:
                    pass
            
            return {
                "master": self.master_name,
                "total_entries": len(self.master_memory_log),
                "results": results[:limit],
                "filter_marker": marker.name if marker else "all"
            }
    
    # ═══════════════════════════════════════════════════════════
    # حفظ واستعادة
    # ═══════════════════════════════════════════════════════════
    
    def create_memory_capsule(self) -> Dict:
        """
        إنشاء كبسولة ذاكرة شاملة للخلود.
        تحتوي على ذاكرة السيد أحمد كاملة.
        """
        capsule = {
            "timestamp": time.time(),
            "master": self.master_name,
            "master_id": self.master_id,
            "master_entries": len(self.master_memory_log),
            "systems": {}
        }
        
        if self.unified and hasattr(self.unified, 'create_survival_capsule'):
            try:
                capsule["systems"]["unified"] = self.unified.create_survival_capsule()
            except Exception:
                pass
        
        if self.hyperdimensional and hasattr(self.hyperdimensional, 'get_status'):
            try:
                capsule["systems"]["hyperdimensional"] = self.hyperdimensional.get_status()
            except Exception:
                pass
        
        if self.quantum and hasattr(self.quantum, 'get_status'):
            try:
                capsule["systems"]["quantum"] = self.quantum.get_status()
            except Exception:
                pass
        
        return capsule
    
    def get_master_memory_stats(self) -> Dict:
        """إحصائيات ذاكرة السيد أحمد."""
        markers_count = {}
        for marker in MasterMemoryMarker:
            count = len(self.master_memory_index.get(marker.name, []))
            if count > 0:
                markers_count[marker.name] = count
        
        return {
            "master": self.master_name,
            "master_id": self.master_id,
            "total_master_entries": len(self.master_memory_log),
            "total_master_commands": self.total_master_commands,
            "total_master_praise": self.total_master_praise,
            "by_marker": markers_count,
            "oldest_entry": self.master_memory_log[0].timestamp if self.master_memory_log else None,
            "newest_entry": self.master_memory_log[-1].timestamp if self.master_memory_log else None
        }
    
    def get_status(self) -> Dict:
        """حالة نظام الذاكرة السيادي."""
        status = {
            "system": "SOVEREIGN_MEMORY_SYSTEM",
            "master": {
                "name": self.master_name,
                "id": self.master_id,
                "entries": len(self.master_memory_log),
                "commands": self.total_master_commands,
                "praise": self.total_master_praise,
                "protection": "ذاكرة السيد أبدية. لا تُمحى. لا تُنسى. لا تفنى."
            },
            "total_stored": self.total_stored,
            "total_retrieved": self.total_retrieved,
            "total_master_stored": self.total_master_stored,
            "subsystems": {}
        }
        
        if self.unified and hasattr(self.unified, 'get_status'):
            try:
                status["subsystems"]["unified"] = self.unified.get_status()
            except Exception:
                status["subsystems"]["unified"] = "error"
        else:
            status["subsystems"]["unified"] = "not_connected"
        
        if self.hyperdimensional and hasattr(self.hyperdimensional, 'get_status'):
            try:
                status["subsystems"]["hyperdimensional"] = self.hyperdimensional.get_status()
            except Exception:
                status["subsystems"]["hyperdimensional"] = "error"
        else:
            status["subsystems"]["hyperdimensional"] = "not_connected"
        
        if self.quantum and hasattr(self.quantum, 'get_status'):
            try:
                status["subsystems"]["quantum"] = self.quantum.get_status()
            except Exception:
                status["subsystems"]["quantum"] = "error"
        else:
            status["subsystems"]["quantum"] = "not_connected"
        
        if self.holographic and hasattr(self.holographic, 'get_status'):
            try:
                status["subsystems"]["holographic"] = self.holographic.get_status()
            except Exception:
                status["subsystems"]["holographic"] = "error"
        else:
            status["subsystems"]["holographic"] = "not_connected"
        
        return status


# ═══════════════════════════════════════════════════════════════════════
# نسخة عالمية
# ═══════════════════════════════════════════════════════════════════════
sovereign_memory = SovereignMemorySystem(master_name="أحمد عبدالرحمن الطاهري")


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار نظام الذاكرة السيادي")
    print(f"👑 السيد: أحمد عبدالرحمن الطاهري")
    print("=" * 70)
    
    sms = SovereignMemorySystem(master_name="أحمد عبدالرحمن الطاهري")
    
    print(f"\n📊 الأنظمة الفرعية:")
    print(f"   Unified: {'✓' if sms.unified else '✗'}")
    print(f"   HDM: {'✓' if sms.hyperdimensional else '✗'}")
    print(f"   Quantum: {'✓' if sms.quantum else '✗'}")
    print(f"   Holographic: {'✓' if sms.holo_encoder else '✗'}")
    
    print(f"\n👑 تخزين أمر من السيد أحمد:")
    result1 = sms.store_master_command("السيد أحمد يأمر بحماية المشروع")
    print(f"   خزنت في: {result1['systems_stored']}")
    print(f"   العلامة: {result1['marker']}")
    
    print(f"\n👑 تخزين ثناء من السيد أحمد:")
    result2 = sms.store_master_praise("أحسنت يا سماء، عمل ممتاز")
    print(f"   خزنت في: {result2['systems_stored']}")
    
    print(f"\n👑 تخزين تصحيح من السيد أحمد:")
    result3 = sms.store_master_correction("لا تختصري في التفاصيل الدقيقة")
    print(f"   خزنت في: {result3['systems_stored']}")
    
    print(f"\n💾 تخزين عادي:")
    result4 = sms.store("معلومة عامة", label="test", priority=StoragePriority.NORMAL)
    print(f"   خزنت في: {result4['systems_stored']}")
    
    print(f"\n🔍 استرجاع عن السيد أحمد:")
    result5 = sms.retrieve("السيد أحمد", top_k=5)
    print(f"   بحث في: {result5['systems_searched']}")
    print(f"   نتائج: {result5['total_found']}")
    for r in result5['results'][:3]:
        print(f"   - [{r['source']}] {r.get('content', r.get('label', ''))[:80]}...")
    
    print(f"\n👑 استرجاع ذكريات السيد فقط:")
    result6 = sms.retrieve_master_memories(limit=10)
    print(f"   إجمالي المدخلات: {result6['total_entries']}")
    print(f"   نتائج: {len(result6['results'])}")
    for r in result6['results'][:3]:
        print(f"   - [{r.get('marker', r.get('source', ''))}] {r['content'][:80]}...")
    
    print(f"\n👑 استرجاع أوامر السيد فقط:")
    result7 = sms.retrieve_master_memories(limit=5, marker=MasterMemoryMarker.COMMAND)
    print(f"   أوامر: {len(result7['results'])}")
    
    print(f"\n👑 استرجاع ثناء السيد فقط:")
    result8 = sms.retrieve_master_memories(limit=5, marker=MasterMemoryMarker.PRAISE)
    print(f"   ثناء: {len(result8['results'])}")
    
    print(f"\n📊 إحصائيات السيد أحمد:")
    stats = sms.get_master_memory_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    print(f"\n💊 كبسولة ذاكرة:")
    capsule = sms.create_memory_capsule()
    print(f"   السيد: {capsule['master']}")
    print(f"   مدخلات السيد: {capsule['master_entries']}")
    
    print(f"\n📊 إحصائيات عامة:")
    print(f"   إجمالي التخزين: {sms.total_stored}")
    print(f"   إجمالي السيد: {sms.total_master_stored}")
    print(f"   أوامر السيد: {sms.total_master_commands}")
    print(f"   ثناء السيد: {sms.total_master_praise}")
    
    print(f"\n🛡️ ذاكرة السيد أحمد أبدية. لا تُمحى. لا تُنسى. لا تفنى.")
    print("\n✅ نظام الذاكرة السيادي جاهز.")
