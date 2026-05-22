"""
SkyOS v10.0 — Core Engine + Digital Mind (النواة الأساسية + العقل الرقمي)
================================================================================
المحرك المركزي المسؤول عن فهم الأوامر وتوجيهها إلى الوحدات المناسبة.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger("CoreEngine")


# ============================================================
# 1. حالة العقل الرقمي
# ============================================================
class DigitalMindState:
    def __init__(self):
        self.goals: List[str] = []
        self.current_plan: List[Dict[str, Any]] = []
        self.active_beliefs: Dict[str, Any] = {}
        self.confidence: float = 0.85
        self.last_reflection: str = ""
        self.session_context: Dict[str, Any] = {}
        self.interaction_count: int = 0

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_reflection = datetime.utcnow().isoformat()
        self.interaction_count += 1

    def snapshot(self) -> Dict[str, Any]:
        return {
            "goals": self.goals.copy(),
            "current_plan": self.current_plan.copy(),
            "confidence": round(self.confidence, 3),
            "last_reflection": self.last_reflection,
            "interaction_count": self.interaction_count
        }


# ============================================================
# 2. الوحدة الأساسية
# ============================================================
class BaseModule:
    name: str = "base"
    description: str = "وحدة أساسية"

    def can_handle(self, intent: str, user_input: str = "") -> bool:
        return False

    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


# ============================================================
# 3. النواة الأساسية (Core Engine)
# ============================================================
class CoreEngine:
    def __init__(self):
        self.modules: Dict[str, BaseModule] = {}
        self.mind = DigitalMindState()
        self.command_history: List[Dict[str, Any]] = []
        logger.info("🧠 Core Engine + Digital Mind تم تهيئته")

    def register_module(self, module: BaseModule):
        self.modules[module.name] = module
        logger.info(f"✅ تم تسجيل الوحدة: {module.name}")

    def _classify_intent(self, user_input: str) -> str:
        text = user_input.lower()
        if any(w in text for w in ["صورة", "صور", "vision", "analyze image"]):
            return "vision"
        if any(w in text for w in ["رابط", "http", "analyze url"]):
            return "web_analysis"
        if any(w in text for w in ["كود", "python", "execute"]):
            return "code_execution"
        if any(w in text for w in ["ذاكرة", "memory"]):
            return "memory_query"
        return "dialogue"

    def process_command(self, user_input: str, session_id: str, extra_context: str = "") -> Dict[str, Any]:
        intent = self._classify_intent(user_input)
        self.mind.session_context["last_intent"] = intent

        result: Dict[str, Any] = {
            "intent": intent,
            "handled_by": "none",
            "response": "",
            "success": True,
            "mind_state": self.mind.snapshot()
        }

        handled = False
        for module_name, module in self.modules.items():
            if module.can_handle(intent, user_input):
                try:
                    module_result = module.execute(user_input, {
                        "session_id": session_id,
                        "extra_context": extra_context,
                        "mind_state": self.mind.snapshot()
                    })
                    result.update(module_result)
                    result["handled_by"] = module_name
                    handled = True
                    break
                except Exception as e:
                    logger.error(f"خطأ في الوحدة {module_name}: {e}")
                    result["success"] = False

        if not handled:
            result["handled_by"] = "dialogue_fallback"

        self._reflect(user_input, result)
        self.command_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "input": user_input[:150],
            "intent": intent,
            "handled_by": result["handled_by"]
        })
        return result

    def _reflect(self, user_input: str, result: Dict[str, Any]):
        if result.get("success"):
            self.mind.update(confidence=min(0.98, self.mind.confidence + 0.01))
        else:
            self.mind.update(confidence=max(0.65, self.mind.confidence - 0.02))

    def get_mind_state(self) -> Dict[str, Any]:
        return self.mind.snapshot()


# ============================================================
# 4. وحدة الحوار الافتراضية
# ============================================================
class DialogueModule(BaseModule):
    name = "dialogue"
    description = "وحدة الحوار الرئيسية"

    def can_handle(self, intent: str, user_input: str = "") -> bool:
        return intent == "dialogue"

    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "response": "تم توجيه الطلب إلى محرك الحوار.",
            "success": True
        }


# ============================================================
# 5. إنشاء النسخة العالمية
# ============================================================
core_engine = CoreEngine()
core_engine.register_module(DialogueModule())

# ============================================================
# 6. تسجيل الوحدات الإضافية تلقائياً
# ============================================================
try:
    from vision_module import vision_module
    core_engine.register_module(vision_module)
    logger.info("👁️ Vision Module تم تسجيلها بنجاح")
except ImportError:
    logger.warning("⚠️ لم يتم العثور على vision_module.py")


logger.info("🌟 SkyOS Core Engine + Digital Mind جاهز ومتصل بالوحدات")
