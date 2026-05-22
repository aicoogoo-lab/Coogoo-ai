"""
SkyOS v10.2 — Holographic Encoder
=================================
نظام تحويل النصوص والمعلومات إلى متجهات هولوغرافية (Encoding).

هدف هذا الملف:
- تحويل نص عادي إلى متجه هولوغرافي ذي معنى.
- دعم عمليات الربط (Binding) والتجميع (Bundling).
- أن يكون أساسًا قويًا للذاكرة الهولوغرافية الذكية.
"""

import numpy as np
import re
import hashlib
from typing import List, Optional, Dict
import logging

logger = logging.getLogger("HolographicEncoder")


class HolographicEncoder:
    """
    محول نصوص إلى متجهات هولوغرافية.
    يستخدم تقنية Random Projection + Bundling لإنشاء تمثيلات دلالية.
    """

    def __init__(self, dimension: int = 10000, seed: Optional[int] = 42):
        self.dimension = dimension
        self.rng = np.random.default_rng(seed)
        self.token_vectors: Dict[str, np.ndarray] = {}  # تخزين متجهات الكلمات
        logger.info(f"Holographic Encoder initialized with {dimension} dimensions")

    def _get_token_vector(self, token: str) -> np.ndarray:
        """إنشاء أو استرجاع متجه لكلمة معينة"""
        if token not in self.token_vectors:
            # نستخدم hash لجعل المتجهات ثابتة لنفس الكلمة
            seed = int(hashlib.md5(token.encode()).hexdigest(), 16) % (2**32)
            rng = np.random.default_rng(seed)
            vector = rng.choice([-1., 1.], size=self.dimension)
            self.token_vectors[token] = vector.astype(np.float32)
        return self.token_vectors[token]

    def clean_and_tokenize(self, text: str) -> List[str]:
        """تنظيف النص وتقسيمه إلى كلمات"""
        if not text:
            return []
        text = text.lower()
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)  # دعم العربية
        tokens = text.split()
        # إزالة الكلمات القصيرة جدًا
        tokens = [t for t in tokens if len(t) > 1]
        return tokens

    def encode_text(self, text: str) -> np.ndarray:
        """
        تحويل نص إلى متجه هولوغرافي باستخدام Bundling.
        هذه هي الدالة الأساسية.
        """
        tokens = self.clean_and_tokenize(text)
        if not tokens:
            # إرجاع متجه صفري إذا كان النص فارغًا
            return np.zeros(self.dimension, dtype=np.float32)

        vectors = []
        for token in tokens:
            vec = self._get_token_vector(token)
            vectors.append(vec)

        # Bundling (جمع المتجهات + تطبيع)
        bundled = np.sum(vectors, axis=0)
        norm = np.linalg.norm(bundled)
        if norm > 0:
            bundled = bundled / norm

        return bundled.astype(np.float32)

    def encode_and_bind(self, text1: str, text2: str) -> np.ndarray:
        """ربط تمثيل نصين معًا (Binding)"""
        v1 = self.encode_text(text1)
        v2 = self.encode_text(text2)
        return (v1 * v2).astype(np.float32)

    def batch_encode(self, texts: List[str]) -> List[np.ndarray]:
        """تحويل قائمة نصوص إلى قائمة متجهات"""
        return [self.encode_text(text) for text in texts]

    def get_token_count(self) -> int:
        """عدد الكلمات التي تم ترميزها حتى الآن"""
        return len(self.token_vectors)

    def clear(self):
        """مسح ذاكرة المتجهات"""
        self.token_vectors.clear()
        logger.info("Holographic Encoder cleared")


# إنشاء نسخة عامة جاهزة للاستخدام
holographic_encoder = HolographicEncoder(dimension=10000)

logger.info("✅ Holographic Encoder جاهز للاستخدام")
