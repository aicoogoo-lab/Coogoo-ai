"""
SkyOS v10.1 — Hyperdimensional Memory Module
=============================================
وحدة أولية للحوسبة فائقة الأبعاد (Hyperdimensional Computing)

تدعم:
- إنشاء متجهات عالية الأبعاد
- عملية الربط (Binding)
- عملية التجميع (Bundling)
- عملية التبديل (Permutation)
- تخزين واسترجاع ترابطي (Associative Memory)
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger("HyperdimensionalMemory")


class HyperdimensionalMemory:
    """
    ذاكرة هولوغرافية تعتمد على الحوسبة فائقة الأبعاد.
    """

    def __init__(self, dimension: int = 10000, seed: Optional[int] = None):
        """
        :param dimension: عدد أبعاد المتجهات (يفضل أن يكون كبيراً)
        :param seed: بذرة عشوائية لإعادة الإنتاجية
        """
        self.dimension = dimension
        self.rng = np.random.default_rng(seed)
        self.memory: Dict[str, np.ndarray] = {}           # key -> vector
        self.labels: Dict[int, str] = {}                  # index -> label

        logger.info(f"Hyperdimensional Memory initialized with {dimension} dimensions")

    # ============================================================
    # إنشاء متجه عشوائي
    # ============================================================
    def create_vector(self, label: Optional[str] = None) -> np.ndarray:
        """إنشاء متجه ثنائي عشوائي (-1 أو +1)"""
        vector = self.rng.choice([-1, 1], size=self.dimension).astype(np.float32)
        
        if label:
            self.memory[label] = vector
            logger.debug(f"Created vector for label: {label}")
        return vector

    # ============================================================
    # عملية الربط (Binding)
    # ============================================================
    def bind(self, vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        """ربط متجهين (Element-wise multiplication)"""
        if vec1.shape != vec2.shape:
            raise ValueError("Vectors must have the same shape")
        return (vec1 * vec2).astype(np.float32)

    # ============================================================
    # عملية التجميع (Bundling)
    # ============================================================
    def bundle(self, vectors: List[np.ndarray]) -> np.ndarray:
        """تجميع عدة متجهات معاً"""
        if not vectors:
            raise ValueError("No vectors provided for bundling")
        
        stacked = np.stack(vectors)
        bundled = np.sum(stacked, axis=0)
        
        # تطبيع المتجه
        norm = np.linalg.norm(bundled)
        if norm > 0:
            bundled = bundled / norm
        return bundled.astype(np.float32)

    # ============================================================
    # عملية التبديل (Permutation)
    # ============================================================
    def permute(self, vector: np.ndarray, shift: int = 1) -> np.ndarray:
        """تبديل المتجه (يُستخدم لتمثيل الترتيب أو السياق)"""
        return np.roll(vector, shift=shift).astype(np.float32)

    # ============================================================
    # تخزين متجه في الذاكرة
    # ============================================================
    def store(self, label: str, vector: Optional[np.ndarray] = None) -> np.ndarray:
        """تخزين متجه في الذاكرة الترابطية"""
        if vector is None:
            vector = self.create_vector()
        
        self.memory[label] = vector
        logger.debug(f"Stored vector: {label}")
        return vector

    # ============================================================
    # الاسترجاع الترابطي (Query)
    # ============================================================
    def query(self, vector: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        البحث عن أقرب المتجهات المخزنة باستخدام التشابه (Dot Product)
        """
        if not self.memory:
            return []

        results = []
        for label, stored_vec in self.memory.items():
            similarity = np.dot(vector, stored_vec) / (np.linalg.norm(vector) * np.linalg.norm(stored_vec) + 1e-8)
            results.append((label, float(similarity)))

        # ترتيب تنازلي حسب التشابه
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    # ============================================================
    # فك الربط (Unbinding) - تقريبي
    # ============================================================
    def unbind(self, bound_vector: np.ndarray, known_vector: np.ndarray) -> np.ndarray:
        """محاولة فك الربط (تقريبي)"""
        return self.bind(bound_vector, known_vector)  # في HDC البسيط، الربط عكسه نفسه

    # ============================================================
    # معلومات عامة
    # ============================================================
    def get_memory_size(self) -> int:
        return len(self.memory)

    def clear(self):
        self.memory.clear()
        logger.info("Hyperdimensional Memory cleared")


# ============================================================
# مثال سريع للاستخدام
# ============================================================
if __name__ == "__main__":
    hdm = HyperdimensionalMemory(dimension=5000)

    # إنشاء متجهات للمفاهيم
    project = hdm.create_vector("مشروع")
    coogoo = hdm.create_vector("Coogoo-ai")
    sentient = hdm.create_vector("SENTIENT CORE")

    # ربط المفاهيم
    project_coogoo = hdm.bind(project, coogoo)
    hdm.store("مشروع Coogoo-ai", project_coogoo)

    # تجميع عدة مفاهيم
    bundled = hdm.bundle([project, coogoo, sentient])
    hdm.store("مشروع Coogoo + Sentient", bundled)

    # استرجاع
    results = hdm.query(project_coogoo, top_k=3)
    print("نتائج الاسترجاع:")
    for label, score in results:
        print(f"  {label}: {score:.4f}")
