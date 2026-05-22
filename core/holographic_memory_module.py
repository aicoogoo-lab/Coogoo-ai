"""
SkyOS v10.2 — Holographic Memory Module (نسخة محسنة ومربوطة)
=============================================================
وحدة تربط HyperdimensionalMemory مع Core Engine باستخدام Encoding حقيقي.
"""

from typing import Dict, Any
from hyperdimensional_memory import HyperdimensionalMemory
from holographic_encoder import holographic_encoder
import logging

logger = logging.getLogger("HolographicMemoryModule")


class HolographicMemoryModule:
    """وحدة الذاكرة الهولوغرافية المحسّنة"""

    name = "holographic_memory"
    description = "وحدة الذاكرة فائقة الأبعاد مع دعم Encoding حقيقي"

    def __init__(self, dimension: int = 10000):
        self.hdm = HyperdimensionalMemory(dimension=dimension)
        logger.info("Holographic Memory Module (النسخة المحسنة) تم تهيئتها")

    def can_handle(self, intent: str, user_input: str = "") -> bool:
        keywords = ["ذاكرة", "تذكر", "استرجع", "memory", "holographic", "hdm"]
        return intent == "memory_query" or any(kw in user_input.lower() for kw in keywords)

    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        session_id = context.get("session_id", "default")

        # === حالة التخزين ===
        if any(word in user_input for word in ["احفظ", "خزن", "store", "حفظ"]):
            # ترميز النص الحقيقي بدلاً من إنشاء متجه عشوائي
            vector = holographic_encoder.encode_text(user_input)
            label = f"session_{session_id}_{len(self.hdm.memory)}"

            self.hdm.store(label, vector)

            return {
                "success": True,
                "handled_by": "holographic_memory",
                "response": "تم تخزين المعلومة في الذاكرة الهولوغرافية بنجاح.",
                "stored_label": label
            }

        # === حالة الاسترجاع ===
        elif any(word in user_input for word in ["تذكر", "استرجع", "recall", "memory"]):
            if self.hdm.get_memory_size() == 0:
                return {
                    "success": True,
                    "handled_by": "holographic_memory",
                    "response": "الذاكرة الهولوغرافية فارغة حالياً."
                }

            # إنشاء متجه استعلام من كلام المستخدم
            query_vector = holographic_encoder.encode_text(user_input)
            results = self.hdm.query(query_vector, top_k=5)

            if results:
                response_text = f"تم العثور على {len(results)} نتائج مرتبطة في الذاكرة الهولوغرافية."
            else:
                response_text = "لم أجد معلومات مرتبطة في الذاكرة الهولوغرافية."

            return {
                "success": True,
                "handled_by": "holographic_memory",
                "response": response_text,
                "results": results
            }

        # === الحالة الافتراضية ===
        else:
            vector = holographic_encoder.encode_text(user_input)
            label = f"session_{session_id}_{len(self.hdm.memory)}"
            self.hdm.store(label, vector)

            return {
                "success": True,
                "handled_by": "holographic_memory",
                "response": "تم معالجة الطلب وتخزينه في الذاكرة الهولوغرافية.",
                "stored_label": label
            }
