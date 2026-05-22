"""
SkyOS v10.0 — Vision Module (وحدة الرؤية والتحليل البصري)
================================================================================
هذه أول وحدة متقدمة في نظام الوحدات.

وظيفتها:
- استقبال طلبات تحليل الصور
- استخدام Gemini Vision + OCR كـ fallback
- إرجاع نتيجة منظمة يفهمها الـ Core Engine
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("VisionModule")

try:
    from sky_analyzer import analyze_image_with_gemini, analyzer
except ImportError:
    try:
        from core.sky_analyzer import analyze_image_with_gemini, analyzer
    except ImportError:
        analyze_image_with_gemini = None
        analyzer = None


class VisionModule:
    """وحدة معالجة الصور والرؤية"""

    name = "vision"
    description = "وحدة الرؤية والتحليل البصري باستخدام Gemini Vision + OCR"

    def can_handle(self, intent: str, user_input: str = "") -> bool:
        return intent == "vision"

    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        تنفيذ تحليل الصورة.
        ملاحظة: حالياً الوحدة جاهزة للربط مع رفع الملفات.
        في النسخ القادمة سنربطها مباشرة مع الـ file upload.
        """
        session_id = context.get("session_id", "unknown")

        logger.info(f"👁️ VisionModule تم استدعاؤها | Session: {session_id}")

        # في هذه المرحلة نعيد رسالة توضيحية + نجهز البنية
        # (لاحقاً سنربطها بملف مرفوع فعلياً)
        return {
            "success": True,
            "handled_by": "vision",
            "response": (
                "تم استدعاء وحدة الرؤية بنجاح.\n\n"
                "أرسل صورة الآن وسأقوم بتحليلها باستخدام Gemini Vision "
                "مع دعم التعرف على النصوص العربية والإنجليزية."
            ),
            "intent": "vision",
            "requires_file": True
        }

    def analyze_image(self, image_path: str, api_key: str = None) -> Dict[str, Any]:
        """
        دالة مساعدة لتحليل صورة مباشرة.
        يمكن استدعاؤها من أماكن أخرى في المستقبل.
        """
        if not analyze_image_with_gemini:
            return {"success": False, "error": "محرك الرؤية غير متاح"}

        try:
            result = analyze_image_with_gemini(image_path, api_key)
            return {
                "success": True,
                "description": result.get("description", ""),
                "method": result.get("method", "unknown")
            }
        except Exception as e:
            logger.error(f"خطأ في VisionModule.analyze_image: {e}")
            return {"success": False, "error": str(e)}


# إنشاء نسخة جاهزة للتسجيل
vision_module = VisionModule()

logger.info("👁️ Vision Module جاهزة للتسجيل في Core Engine")
