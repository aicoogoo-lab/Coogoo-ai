"""
SkyOS v10.2 — Hyperdimensional Memory (النسخة المحسّنة)
=======================================================
ذاكرة هولوغرافية تعتمد على الحوسبة فائقة الأبعاد (Hyperdimensional Computing).

التحسينات:
- دقة استرجاع محسنة
- معالجة أفضل للتشابه
- كود أنظف وأكثر استقرارًا
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger("HyperdimensionalMemory")


class HyperdimensionalMemory:
    """
    ذاكرة هولوغرافية متقدمة تدعم:
    - إنشاء متجهات عالية الأبعاد
    - عمليات الربط (Binding) والتجميع (Bundling)
    - الاسترجاع الترابطي بدقة محسنة
    """

    def __init__(self, dimension: int = 10000, seed: Optional[int] = 42):
        self.dimension = dimension
        self.rng = np.random.default_rng(seed)
        self.memory: Dict[str, np.ndarray] = {}

        logger.info(f"Hyperdimensional Memory initialized with {dimension} dimensions")

    # ============================================================
    # إنشاء متجه
    # ============================================================
    def create_vector(self, label: Optional[str] = None) -> np.ndarray:
        """إنشاء متجه ثنائي عشوائي (-1 أو +1)"""
        vector = self.rng.choice([-1., 1.], size=self.dimension).astype(np.float32)
        if label:
            self.memory[label] = vector
        return vector

    # ============================================================
    # عمليات HDC الأساسية
    # ============================================================
    def bind(self, vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        """ربط متجهين (Element-wise multiplication)"""
        if vec1.shape != vec2.shape:
            raise ValueError("Vectors must have the same shape")
        return (vec1 * vec2).astype(np.float32)

    def bundle(self, vectors: List[np.ndarray]) -> np.ndarray:
        """تجميع عدة متجهات مع التطبيع"""
        if not vectors:
            raise ValueError("No vectors provided for bundling")

        stacked = np.stack(vectors)
        bundled = np.sum(stacked, axis=0)

        norm = np.linalg.norm(bundled)
        if norm > 0:
            bundled = bundled / norm
        return bundled.astype(np.float32)

    def permute(self, vector: np.ndarray, shift: int = 1) -> np.ndarray:
        """تبديل المتجه (لتمثيل الترتيب والسياق)"""
        return np.roll(vector, shift=shift).astype(np.float32)

    # ============================================================
    # التخزين
    # ============================================================
    def store(self, label: str, vector: Optional[np.ndarray] = None) -> np.ndarray:
        """تخزين متجه في الذاكرة"""
        if vector is None:
            vector = self.create_vector()
        self.memory[label] = vector
        return vector

    # ============================================================
    # الاسترجاع (محسّن الدقة)
    # ============================================================
    def query(self, vector: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        البحث عن أقرب المتجهات باستخدام Cosine Similarity.
        هذه النسخة أكثر دقة واستقرارًا.
        """
        if not self.memory:
            return []

        results = []
        vec_norm = np.linalg.norm(vector) + 1e-8

        for label, stored_vec in self.memory.items():
            stored_norm = np.linalg.norm(stored_vec) + 1e-8
            similarity = np.dot(vector, stored_vec) / (vec_norm * stored_norm)
            results.append((label, float(similarity)))

        # ترتيب تنازلي حسب التشابه
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def get_top_similar(self, vector: np.ndarray, top_k: int = 5, threshold: float = 0.0) -> List[Tuple[str, float]]:
        """
        استرجاع النتائج التي تتجاوز عتبة تشابه معينة.
        مفيدة لتحسين دقة الاسترجاع.
        """
        results = self.query(vector, top_k=top_k * 2)
        filtered = [(label, score) for label, score in results if score >= threshold]
        return filtered[:top_k]

    # ============================================================
    # فك الربط (تقريبي)
    # ============================================================
    def unbind(self, bound_vector: np.ndarray, known_vector: np.ndarray) -> np.ndarray:
        return self.bind(bound_vector, known_vector)

    # ============================================================
    # أدوات مساعدة
    # ============================================================
    def get_memory_size(self) -> int:
        return len(self.memory)

    def clear(self):
        self.memory.clear()
        logger.info("Hyperdimensional Memory cleared")


# ============================================================
# اختبار سريع
# ============================================================
if __name__ == "__main__":
    hdm = HyperdimensionalMemory(dimension=5000)

    # مثال بسيط
    vec1 = hdm.create_vector("مفهوم_1")
    vec2 = hdm.create_vector("مفهوم_2")

    hdm.store("مفهوم_مرتبط", hdm.bind(vec1, vec2))

    results = hdm.query(vec1, top_k=3)
    print("نتائج الاسترجاع:")
    for label, score in results:
        print(f"  {label}: {score:.4f}")
