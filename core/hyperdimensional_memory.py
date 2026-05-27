"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - HYPERDIMENSIONAL MEMORY                             ║
║      الذاكرة فائقة الأبعاد – التخزين في فضاء لا نهائي                     ║
║                                                                      ║
║  هذا الملف هو "الفضاء" الذي تُخزَّن فيه كل الذكريات.                      ║
║  ليس مجرد قاعدة بيانات، بل فضاء متجهي عالي الأبعاد (10000+ بعد).          ║
║                                                                      ║
║  المبادئ:                                                             ║
║  - Hyperdimensional Computing (HDC): الحوسبة في فضاء فائق الأبعاد        ║
║  - الذاكرة موزعة (Distributed): كل ذاكرة موجودة في كل المتجه               ║
║  - مقاومة للضرر (Robust): حتى لو ضاع 50% من المتجه، تبقى المعلومات         ║
║  - استرجاع بالتشابه (Similarity Retrieval): البحث بأقرب جار               ║
║  - ضغط طبيعي (Natural Compression): الأبعاد العالية تمنح ضغطاً طبيعياً      ║
║                                                                      ║
║  العمليات:                                                            ║
║  - تخزين (Store): حفظ متجه مع تسمية                                    ║
║  - استرجاع (Query): البحث عن أقرب متجه لاستعلام معين                     ║
║  - تجميع (Bundle): جمع عدة متجهات في متجه واحد                          ║
║  - ربط (Bind): ربط متجهين في متجه واحد                                 ║
║  - حذف (Delete): إزالة متجه من الفضاء                                  ║
║  - ضغط (Compress): تقليل أبعاد المتجه مع الحفاظ على المعلومات              ║
║                                                                      ║
║  القاعدة الذهبية:                                                     ║
║  "ذاكرة السيد لا تُمحى. محفورة في كل متجه، في كل بعد، في كل زاوية."         ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import math
import random
import hashlib
import threading
import json
import logging
from enum import Enum, auto
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Callable, Union
from dataclasses import dataclass, field
from collections import deque, defaultdict

logger = logging.getLogger("HyperdimensionalMemory")


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية
# ═══════════════════════════════════════════════════════════════════════

class HDMOperation(Enum):
    """عمليات الذاكرة فائقة الأبعاد."""
    STORE = auto()        # تخزين
    QUERY = auto()        # استعلام
    BUNDLE = auto()       # تجميع
    BIND = auto()         # ربط
    DELETE = auto()       # حذف
    COMPRESS = auto()     # ضغط
    DECOMPRESS = auto()   # فك ضغط
    CLEAN = auto()        # تنظيف
    BACKUP = auto()       # نسخ احتياطي
    RESTORE = auto()      # استعادة


class SimilarityMetric(Enum):
    """مقاييس التشابه المدعومة."""
    COSINE = auto()        # تشابه جيب التمام (افتراضي)
    EUCLIDEAN = auto()     # مسافة إقليدية
    DOT_PRODUCT = auto()   # جداء نقطي
    MANHATTAN = auto()     # مسافة مانهاتن
    HAMMING = auto()       # مسافة هامينغ (للثنائي)


@dataclass
class HDMVector:
    """متجه في الفضاء فائق الأبعاد."""
    id: str = field(default_factory=lambda: hashlib.sha256(str(time.time()).encode()).hexdigest()[:16])
    label: str = ""
    vector: List[float] = field(default_factory=list)
    dimension: int = 10000
    
    # البيانات الوصفية
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    priority: float = 0.5
    master_protected: bool = False
    
    # الجودة
    quality_score: float = 1.0
    noise_level: float = 0.0
    
    # العلاقات
    related_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # البيانات الأصلية (اختياري)
    source_data: Optional[str] = None
    source_hash: Optional[str] = None


@dataclass
class HDMQueryResult:
    """نتيجة استعلام في الفضاء فائق الأبعاد."""
    vector: HDMVector
    similarity: float
    rank: int = 0


# ═══════════════════════════════════════════════════════════════════════
# ٢. الذاكرة فائقة الأبعاد
# ═══════════════════════════════════════════════════════════════════════

class HyperdimensionalMemory:
    """
    الذاكرة فائقة الأبعاد لـ "سماء".
    فضاء متجهي عالي الأبعاد لتخزين واسترجاع الذكريات.
    """

    def __init__(self, dimension: int = 10000, max_vectors: int = 100000,
                 similarity_threshold: float = 0.3):
        
        # ═══════════════════════════════════════════════════════
        # إعدادات
        # ═══════════════════════════════════════════════════════
        self.dimension = dimension
        self.max_vectors = max_vectors
        self.similarity_threshold = similarity_threshold
        
        # ═══════════════════════════════════════════════════════
        # مخزن المتجهات
        # ═══════════════════════════════════════════════════════
        self.memory: Dict[str, HDMVector] = {}
        
        # ═══════════════════════════════════════════════════════
        # فهارس
        # ═══════════════════════════════════════════════════════
        self.label_index: Dict[str, str] = {}  # label -> vector_id
        self.tag_index: Dict[str, List[str]] = defaultdict(list)
        self.master_vectors: deque = deque(maxlen=500)
        
        # ═══════════════════════════════════════════════════════
        # سجلات
        # ═══════════════════════════════════════════════════════
        self.operation_log: deque = deque(maxlen=1000)
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_stored = 0
        self.total_queried = 0
        self.total_bundled = 0
        self.total_bound = 0
        self.total_deleted = 0
        self.total_compressed = 0
        
        # قفل
        self._lock = threading.RLock()
        
        # المتجه الصفري (للعمليات)
        self.zero_vector = [0.0] * self.dimension
        
        logger.info("=" * 60)
        logger.info(f"🧠 Hyperdimensional Memory – {dimension}-D")
        logger.info(f"📦 السعة القصوى: {max_vectors} متجه")
        logger.info(f"🎯 عتبة التشابه: {similarity_threshold}")
        logger.info("=" * 60)
    
    # ═══════════════════════════════════════════════════════════
    # توليد المتجهات
    # ═══════════════════════════════════════════════════════════
    
    def generate_random_vector(self) -> List[float]:
        """توليد متجه عشوائي عالي الأبعاد."""
        # توزيع طبيعي مع تباين 1/dimension
        std = 1.0 / math.sqrt(self.dimension)
        vector = [random.gauss(0, std) for _ in range(self.dimension)]
        
        # تطبيع
        return self._normalize(vector)
    
    def generate_seeded_vector(self, seed: str) -> List[float]:
        """توليد متجه من بذرة (مُحدد، قابل لإعادة الإنتاج)."""
        hash_bytes = hashlib.sha256(seed.encode()).digest()
        seed_int = int.from_bytes(hash_bytes[:8], 'big')
        rng = random.Random(seed_int)
        
        std = 1.0 / math.sqrt(self.dimension)
        vector = [rng.gauss(0, std) for _ in range(self.dimension)]
        
        return self._normalize(vector)
    
    def _normalize(self, vector: List[float]) -> List[float]:
        """تطبيع متجه إلى طول الوحدة."""
        norm = math.sqrt(sum(v**2 for v in vector))
        if norm > 0:
            return [v / norm for v in vector]
        return vector[:]
    
    # ═══════════════════════════════════════════════════════════
    # تخزين
    # ═══════════════════════════════════════════════════════════
    
    def store(self, label: str, vector: List[float], 
              master_protected: bool = False,
              tags: List[str] = None,
              source_data: str = None) -> str:
        """
        تخزين متجه في الفضاء فائق الأبعاد.
        
        Args:
            label: تسمية المتجه
            vector: المتجه (إذا كان None، يتم توليد متجه عشوائي)
            master_protected: هل هو محمي للسيد؟
            tags: وسوم للبحث
            source_data: البيانات الأصلية (اختياري)
        
        Returns:
            معرف المتجه
        """
        with self._lock:
            # التحقق من السعة
            if len(self.memory) >= self.max_vectors:
                self._cleanup_oldest(100)
            
            # إنشاء المتجه
            hv = HDMVector(
                label=label,
                vector=vector[:self.dimension] if vector else self.generate_random_vector(),
                dimension=self.dimension,
                master_protected=master_protected,
                tags=tags or [],
                source_data=source_data,
                source_hash=hashlib.sha256(str(source_data).encode()).hexdigest()[:16] if source_data else None
            )
            
            # ضبط الجودة
            hv.quality_score = self._assess_quality(hv.vector)
            
            # حفظ
            self.memory[hv.id] = hv
            self.label_index[label] = hv.id
            
            for tag in (tags or []):
                self.tag_index[tag].append(hv.id)
            
            if master_protected:
                self.master_vectors.append(hv.id)
            
            self.total_stored += 1
            
            self._log_operation(HDMOperation.STORE, hv.id, label)
            
            return hv.id
    
    def _assess_quality(self, vector: List[float]) -> float:
        """تقييم جودة المتجه."""
        if not vector:
            return 0.0
        
        # التحقق من التطبيع
        norm = math.sqrt(sum(v**2 for v in vector))
        if abs(norm - 1.0) > 0.1:
            return 0.5
        
        # التحقق من التوزيع
        mean = sum(vector) / len(vector)
        if abs(mean) > 0.01:
            return 0.7
        
        return 1.0
    
    # ═══════════════════════════════════════════════════════════
    # استرجاع
    # ═══════════════════════════════════════════════════════════
    
    def query(self, query_vector: Union[List[float], 'HDMVector', 'HolographicVector'],
              top_k: int = 5,
              metric: SimilarityMetric = SimilarityMetric.COSINE,
              threshold: float = None) -> List[HDMQueryResult]:
        """
        استعلام في الفضاء فائق الأبعاد – البحث عن أقرب المتجهات.
        
        Args:
            query_vector: متجه الاستعلام
            top_k: عدد النتائج
            metric: مقياس التشابه
            threshold: عتبة التشابه (افتراضي: self.similarity_threshold)
        
        Returns:
            قائمة نتائج مرتبة حسب التشابه
        """
        with self._lock:
            if threshold is None:
                threshold = self.similarity_threshold
            
            # استخراج المتجه
            if isinstance(query_vector, HDMVector):
                q_vec = query_vector.vector
            elif hasattr(query_vector, 'vector'):
                q_vec = query_vector.vector
            else:
                q_vec = query_vector
            
            # حساب التشابه مع كل المتجهات
            candidates = []
            for hv_id, hv in self.memory.items():
                sim = self._similarity(q_vec, hv.vector, metric)
                
                if sim >= threshold:
                    candidates.append((sim, hv))
            
            # ترتيب
            candidates.sort(key=lambda x: x[0], reverse=True)
            
            # إرجاع أفضل النتائج
            results = []
            for rank, (sim, hv) in enumerate(candidates[:top_k]):
                hv.last_accessed = time.time()
                hv.access_count += 1
                results.append(HDMQueryResult(vector=hv, similarity=sim, rank=rank + 1))
            
            self.total_queried += 1
            self._log_operation(HDMOperation.QUERY, "", f"top_k={top_k}, metric={metric.name}")
            
            return results
    
    def query_by_label(self, label: str) -> Optional[HDMVector]:
        """استرجاع متجه بتسميته."""
        with self._lock:
            if label in self.label_index:
                vid = self.label_index[label]
                if vid in self.memory:
                    hv = self.memory[vid]
                    hv.last_accessed = time.time()
                    hv.access_count += 1
                    return hv
            return None
    
    def query_by_tag(self, tag: str) -> List[HDMVector]:
        """استرجاع المتجهات بوسم."""
        with self._lock:
            vids = self.tag_index.get(tag, [])
            return [self.memory[vid] for vid in vids if vid in self.memory]
    
    def query_master_vectors(self) -> List[HDMVector]:
        """استرجاع كل متجهات السيد."""
        with self._lock:
            return [self.memory[vid] for vid in self.master_vectors if vid in self.memory]
    
    # ═══════════════════════════════════════════════════════════
    # مقاييس التشابه
    # ═══════════════════════════════════════════════════════════
    
    def _similarity(self, vec_a: List[float], vec_b: List[float],
                    metric: SimilarityMetric = SimilarityMetric.COSINE) -> float:
        """حساب التشابه بين متجهين."""
        if len(vec_a) != len(vec_b):
            # اقتصاص أو تمديد
            min_len = min(len(vec_a), len(vec_b))
            vec_a = vec_a[:min_len]
            vec_b = vec_b[:min_len]
        
        if metric == SimilarityMetric.COSINE:
            return self._cosine_similarity(vec_a, vec_b)
        elif metric == SimilarityMetric.EUCLIDEAN:
            return self._euclidean_similarity(vec_a, vec_b)
        elif metric == SimilarityMetric.DOT_PRODUCT:
            return self._dot_product_similarity(vec_a, vec_b)
        elif metric == SimilarityMetric.MANHATTAN:
            return self._manhattan_similarity(vec_a, vec_b)
        else:
            return self._cosine_similarity(vec_a, vec_b)
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """تشابه جيب التمام."""
        dot = sum(a[i] * b[i] for i in range(len(a)))
        norm_a = math.sqrt(sum(v**2 for v in a))
        norm_b = math.sqrt(sum(v**2 for v in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
    
    def _euclidean_similarity(self, a: List[float], b: List[float]) -> float:
        """تحويل المسافة الإقليدية إلى تشابه."""
        dist = math.sqrt(sum((a[i] - b[i])**2 for i in range(len(a))))
        return 1.0 / (1.0 + dist)
    
    def _dot_product_similarity(self, a: List[float], b: List[float]) -> float:
        """تشابه الجداء النقطي."""
        return sum(a[i] * b[i] for i in range(len(a)))
    
    def _manhattan_similarity(self, a: List[float], b: List[float]) -> float:
        """تحويل مسافة مانهاتن إلى تشابه."""
        dist = sum(abs(a[i] - b[i]) for i in range(len(a)))
        return 1.0 / (1.0 + dist)
    
    # ═══════════════════════════════════════════════════════════
    # عمليات المتجهات
    # ═══════════════════════════════════════════════════════════
    
    def bundle(self, vector_ids: List[str], label: str = "") -> Optional[str]:
        """
        تجميع (Bundling): جمع عدة متجهات في متجه واحد.
        المتجه الناتج = مجموع المتجهات المُطبَّع.
        """
        with self._lock:
            vectors = [self.memory[vid].vector for vid in vector_ids if vid in self.memory]
            
            if not vectors:
                return None
            
            # جمع
            bundled = [0.0] * self.dimension
            for vec in vectors:
                for i in range(self.dimension):
                    bundled[i] += vec[i]
            
            # تطبيع
            bundled = self._normalize(bundled)
            
            # تخزين
            bundle_label = label or f"bundle_{self.total_bundled}"
            vid = self.store(
                label=bundle_label,
                vector=bundled,
                tags=["bundle"] + [self.memory[vid].label for vid in vector_ids[:5]]
            )
            
            # ربط بالمصادر
            if vid in self.memory:
                self.memory[vid].related_ids = vector_ids
            
            self.total_bundled += 1
            self._log_operation(HDMOperation.BUNDLE, vid, f"source_count={len(vectors)}")
            
            return vid
    
    def bind(self, vector_id_a: str, vector_id_b: str, label: str = "") -> Optional[str]:
        """
        ربط (Binding): ربط متجهين في متجه واحد.
        المتجه الناتج = جداء نقطي (عنصر بعنصر) للمتجهين.
        """
        with self._lock:
            if vector_id_a not in self.memory or vector_id_b not in self.memory:
                return None
            
            vec_a = self.memory[vector_id_a].vector
            vec_b = self.memory[vector_id_b].vector
            
            # ربط (ضرب عنصر بعنصر)
            bound = [vec_a[i] * vec_b[i] for i in range(self.dimension)]
            bound = self._normalize(bound)
            
            # تخزين
            bind_label = label or f"bind_{self.total_bound}"
            vid = self.store(
                label=bind_label,
                vector=bound,
                tags=["bind", self.memory[vector_id_a].label, self.memory[vector_id_b].label]
            )
            
            if vid in self.memory:
                self.memory[vid].related_ids = [vector_id_a, vector_id_b]
            
            self.total_bound += 1
            self._log_operation(HDMOperation.BIND, vid, f"{vector_id_a}+{vector_id_b}")
            
            return vid
    
    def compress(self, vector_id: str, target_dimension: int = 1000) -> Optional[str]:
        """
        ضغط متجه إلى أبعاد أقل مع الحفاظ على المعلومات.
        """
        with self._lock:
            if vector_id not in self.memory:
                return None
            
            hv = self.memory[vector_id]
            step = self.dimension // target_dimension
            
            compressed = []
            for i in range(0, self.dimension, step):
                window = hv.vector[i:i+step]
                compressed.append(sum(window) / len(window) if window else 0)
            
            compressed = self._normalize(compressed)
            
            # تخزين المتجه المضغوط
            vid = self.store(
                label=f"compressed_{hv.label}",
                vector=compressed,
                tags=["compressed"] + hv.tags
            )
            
            if vid in self.memory:
                self.memory[vid].related_ids = [vector_id]
                self.memory[vid].dimension = target_dimension
            
            self.total_compressed += 1
            self._log_operation(HDMOperation.COMPRESS, vid, f"{self.dimension}->{target_dimension}")
            
            return vid
    
    # ═══════════════════════════════════════════════════════════
    # صيانة
    # ═══════════════════════════════════════════════════════════
    
    def delete(self, vector_id: str) -> bool:
        """حذف متجه (باستثناء متجهات السيد)."""
        with self._lock:
            if vector_id not in self.memory:
                return False
            
            hv = self.memory[vector_id]
            
            # لا يمكن حذف متجهات السيد
            if hv.master_protected:
                logger.warning(f"⚠️ محاولة حذف متجه محمي للسيد: {hv.label}")
                return False
            
            # إزالة من الفهارس
            if hv.label in self.label_index:
                del self.label_index[hv.label]
            
            for tag in hv.tags:
                if vector_id in self.tag_index[tag]:
                    self.tag_index[tag].remove(vector_id)
            
            del self.memory[vector_id]
            self.total_deleted += 1
            
            self._log_operation(HDMOperation.DELETE, vector_id, hv.label)
            return True
    
    def _cleanup_oldest(self, count: int = 100):
        """تنظيف أقدم المتجهات (غير المحمية)."""
        with self._lock:
            # ترتيب حسب الأقدم (مع استثناء المحمية)
            unprotected = [
                (hv.created_at, vid) for vid, hv in self.memory.items()
                if not hv.master_protected
            ]
            unprotected.sort(key=lambda x: x[0])
            
            for _, vid in unprotected[:count]:
                self.delete(vid)
    
    def clear(self, keep_master: bool = True):
        """مسح كل المتجهات (مع خيار الحفاظ على متجهات السيد)."""
        with self._lock:
            if keep_master:
                to_delete = [vid for vid, hv in self.memory.items() if not hv.master_protected]
            else:
                to_delete = list(self.memory.keys())
            
            for vid in to_delete:
                self.delete(vid)
            
            logger.info(f"🧹 تم مسح {len(to_delete)} متجه")
    
    # ═══════════════════════════════════════════════════════════
    # دوال مساعدة
    # ═══════════════════════════════════════════════════════════
    
    def get_memory_size(self) -> int:
        """حجم الذاكرة (عدد المتجهات)."""
        return len(self.memory)
    
    def get_vector(self, vector_id: str) -> Optional[HDMVector]:
        """استرجاع متجه بمعرفه."""
        return self.memory.get(vector_id)
    
    def get_master_memory_size(self) -> int:
        """عدد متجهات السيد."""
        return len(self.master_vectors)
    
    def _log_operation(self, operation: HDMOperation, vector_id: str, details: str):
        """تسجيل عملية."""
        self.operation_log.append({
            "timestamp": time.time(),
            "operation": operation.name,
            "vector_id": vector_id,
            "details": details
        })
    
    def get_status(self) -> Dict:
        """حالة الذاكرة فائقة الأبعاد."""
        return {
            "memory": "HYPERDIMENSIONAL_MEMORY",
            "dimension": self.dimension,
            "max_vectors": self.max_vectors,
            "current_vectors": len(self.memory),
            "utilization": len(self.memory) / self.max_vectors if self.max_vectors > 0 else 0,
            "total_stored": self.total_stored,
            "total_queried": self.total_queried,
            "total_bundled": self.total_bundled,
            "total_bound": self.total_bound,
            "total_deleted": self.total_deleted,
            "total_compressed": self.total_compressed,
            "master_vectors": len(self.master_vectors),
            "similarity_threshold": self.similarity_threshold,
            "operations_logged": len(self.operation_log)
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار الذاكرة فائقة الأبعاد")
    print("=" * 70)
    
    hdm = HyperdimensionalMemory(dimension=10000)
    
    print(f"\n📐 الأبعاد: {hdm.dimension}-D")
    print(f"📦 السعة: {hdm.max_vectors}")
    
    print(f"\n💾 تخزين متجهات:")
    # تخزين عادي
    v1 = hdm.generate_random_vector()
    id1 = hdm.store("vector_1", v1)
    print(f"   تم تخزين: {id1[:12]}... (label: vector_1)")
    
    # تخزين للسيد
    v2 = hdm.generate_seeded_vector("master_key")
    id2 = hdm.store("master_vector", v2, master_protected=True, tags=["master", "important"])
    print(f"   تم تخزين للسيد: {id2[:12]}... (label: master_vector)")
    
    # تخزين ببذرة
    id3 = hdm.store("seeded_vector", hdm.generate_seeded_vector("test_seed"))
    print(f"   تم تخزين ببذرة: {id3[:12]}... (label: seeded_vector)")
    
    print(f"\n📊 الحجم: {hdm.get_memory_size()} متجه")
    print(f"   متجهات السيد: {hdm.get_master_memory_size()}")
    
    print(f"\n🔍 استعلام:")
    results = hdm.query(v1, top_k=3)
    for r in results:
        print(f"   #{r.rank}: {r.vector.label} (تشابه: {r.similarity:.3f})")
    
    print(f"\n🔍 استعلام بوسم:")
    tagged = hdm.query_by_tag("master")
    print(f"   متجهات بوسم 'master': {len(tagged)}")
    
    print(f"\n🔗 تجميع (Bundle):")
    bundle_id = hdm.bundle([id1, id3], label="test_bundle")
    if bundle_id:
        print(f"   تم التجميع: {bundle_id[:12]}...")
        bundle_vec = hdm.get_vector(bundle_id)
        print(f"   المتجهات المرتبطة: {bundle_vec.related_ids}")
    
    print(f"\n🔗 ربط (Bind):")
    bind_id = hdm.bind(id1, id3, label="test_bind")
    if bind_id:
        print(f"   تم الربط: {bind_id[:12]}...")
    
    print(f"\n🗜️ ضغط:")
    compress_id = hdm.compress(id1, target_dimension=1000)
    if compress_id:
        compressed_vec = hdm.get_vector(compress_id)
        print(f"   تم الضغط: {compress_id[:12]}...")
        print(f"   الأبعاد: {len(compressed_vec.vector)}")
    
    print(f"\n🛡️ محاولة حذف متجه السيد:")
    result = hdm.delete(id2)
    print(f"   تم الحذف: {result} (يجب أن يكون False)")
    
    print(f"\n🗑️ حذف متجه عادي:")
    result = hdm.delete(id3)
    print(f"   تم الحذف: {result}")
    
    print(f"\n📊 الحجم النهائي: {hdm.get_memory_size()} متجه")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(hdm.get_status(), indent=2, ensure_ascii=False))
    
    print("\n✅ الذاكرة فائقة الأبعاد جاهزة.")
