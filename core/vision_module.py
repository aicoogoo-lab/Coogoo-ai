"""
SkyOS v10.1 — Vision Module (وحدة الرؤية والتحليل البصري - نسخة مقوّاة)
================================================================================
وحدة متقدمة لمعالجة وتحليل الصور باستخدام Gemini Vision + OCR.

التحسينات في هذه النسخة:
- بنية أقوى وأكثر تنظيمًا
- دعم أفضل للتكامل مع Core Engine
- معالجة أخطاء محسنة
- جاهزة للربط المباشر مع نظام رفع الملفات
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("VisionModule")

# استيراد محرك التحليل
try:
    from sky_analyzer import analyze_image_with_gemini, analyzer
except ImportError:
    try:
        from core.sky_analyzer import analyze_image_with_gemini, analyzer
    except ImportError:
        analyze_image_with_gemini = None
        analyzer = None
        logger.warning("⚠️ لم يتم العثور على sky_analyzer. بعض الوظائف ستكون محدودة.")


class VisionModule:
    """وحدة الرؤية والتحليل البصري المقوّاة"""

    name = "vision"
    description = "وحدة الرؤية والتحليل البصري باستخدام Gemini Vision + OCR كـ Fallback"

    def __init__(self):
        self.last_analysis: Optional[Dict[str, Any]] = None

    def can_handle(self, intent: str, user_input: str = "") -> bool:
        """تحديد ما إذا كانت الوحدة قادرة على معالجة الطلب"""
        vision_keywords = ["صورة", "صور", "image", "vision", "analyze image", "وصف الصورة"]
        return intent == "vision" or any(kw in user_input.lower() for kw in vision_keywords)

    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        تنفيذ أمر الرؤية.
        حاليًا تُرجع توجيهًا للمستخدم. 
        سيتم تطويرها لاحقًا لتستقبل نتائج التحليل مباشرة.
        """
        session_id = context.get("session_id", "unknown")

        logger.info(f"👁️ VisionModule تم استدعاؤها | Session: {session_id}")

        return {
            "success": True,
            "handled_by": "vision",
            "response": (
                "تم استدعاء وحدة الرؤية.\n\n"
                "أرسل صورة الآن وسأقوم بتحليلها باستخدام Gemini Vision "
                "مع دعم التعرف على النصوص بالعربية والإنجليزية."
            ),
            "intent": "vision",
            "requires_file": True,
            "session_id": session_id
        }

    def analyze_image(self, image_path: str, api_key: str = None) -> Dict[str, Any]:
        """
        تحليل صورة مباشرة باستخدام Gemini Vision أو OCR.
        هذه الدالة جاهزة للاستخدام من أماكن أخرى في النظام.
        """
        if not analyze_image_with_gemini:
            return {
                "success": False,
                "error": "محرك تحليل الصور (Gemini Vision) غير متاح حاليًا."
            }

        try:
            result = analyze_image_with_gemini(image_path, api_key)

            # حفظ آخر تحليل
            self.last_analysis = result

            return {
                "success": True,
                "description": result.get("description", ""),
                "method": result.get("method", "unknown"),
                "handled_by": "vision_module"
            }

        except Exception as e:
            logger.error(f"خطأ في VisionModule.analyze_image: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_last_analysis(self) -> Optional[Dict[str, Any]]:
        """استرجاع آخر تحليل تم إجراؤه"""
        return self.last_analysis

    def clear_last_analysis(self):
        """مسح آخر تحليل"""
        self.last_analysis = None


# إنشاء نسخة جاهزة للتسجيل في Core Engine
vision_module = VisionModule()

logger.info("👁️ Vision Module (النسخة المقوّاة) جاهزة للتسجيل في Core Engine")
