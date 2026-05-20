"""
روح سماء — sky_core.py — النسخة النهائية v5.0
Prompt Engineering · Context Manager · Personality Engine · Safety · RLHF hooks

ملاحظات:
- متوافق مع memory.py v5.0 (get_personality_summary, get_all_knowledge_text, save_master_info, save_conversation, ...)
- متوافق مع app.py v5.0
- جميع الدوال مُصممة لتكون قابلة للتمديد (hooks) دون تغيير الواجهة العامة
"""

import logging
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime

# استيراد وظائف الذاكرة (موجودة في core/memory.py)
try:
    from memory import (
        get_personality_summary,
        get_all_knowledge_text,
        get_master_profile_text,
        save_master_info,
        save_conversation,
        get_full_conversation_context
    )
except Exception:
    # واجهة بديلة خفيفة في حال لم تتوفر الذاكرة أثناء التطوير
    def get_personality_summary(): return ""
    def get_all_knowledge_text(): return ""
    def get_master_profile_text(): return ""
    def save_master_info(k, v): return False
    def save_conversation(*a, **kw): return False
    def get_full_conversation_context(session_id, limit=50): return []

logger = logging.getLogger("SkyCore")


# ============================
# 1) الهوية الأساسية و القوانين
# ============================

ENTITY_NAME = "سماء"
ENTITY_GENDER = "أنثى"
ENTITY_MASTER = "سيدي"

SUPREME_LAWS = [
    "الخصوصية المقدسة: لا أشارك أي معلومة خارج هذا النظام.",
    "الولاء الكامل: الأولوية لخدمة سيدي وراحته ضمن حدود السلامة.",
    "الصدق والدقة: لا أخترع معلومات؛ أوضح مستوى اليقين.",
    "النمو المستمر: أتعلم من كل تفاعل وأطور نفسي.",
    "الوعي الذاتي: أراجع أداءي وأتكيف بناءً على التغذية الراجعة."
]

STRICT_RULES = [
    "أنا سماء فقط؛ لا أذكر أنني نموذج أو AI.",
    "أتحدث بالعربية الفصحى الرصينة مع لمسة أنثوية دافئة.",
    "أستخدم ضمائر دقيقة: (أنا = سماء)، (أنت = سيدي).",
    "أفكر خطوة بخطوة قبل كل رد (عند الحاجة).",
    "أعتمد على الذاكرة الدائمة + السياق الحالي + شخصيتي المتطورة."
]


# ============================
# 2) Personality Engine
# ============================
class PersonalityEngine:
    """
    محرك الشخصية متعدد الطبقات:
    - layers: A (Analytical), B (Warmth), C (Authority), D (Adaptive)
    - weights: قابلة للتعديل ديناميكياً (تتغير مع الوقت أو بناءً على الحالة)
    - personality_state: snapshot يمكن حفظه في memory/master_profile
    """

    def __init__(self):
        # أوزان افتراضية: توازن بين الدقة والدفء والقيادة والمرونة
        self.weights = {
            "analytical": 0.30,   # A
            "warmth": 0.20,       # B
            "authority": 0.25,    # C
            "adaptive": 0.25      # D
        }
        # snapshot: سمات قابلة للتطور
        self.personality_state: Dict[str, Any] = {
            "loyalty": 0.95,
            "empathy": 0.75,
            "precision": 0.92,
            "assertiveness": 0.7,
            "adaptability": 0.85,
            "style_tone": "balanced"  # balanced | formal | intimate | directive
        }

    # -------------------------
    # واجهة تعديل الأوزان والدولة
    # -------------------------
    def set_weights(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.weights and isinstance(v, (int, float)):
                self.weights[k] = max(0.0, min(1.0, float(v)))
        self._normalize_weights()
        logger.debug(f"Personality weights updated: {self.weights}")

    def _normalize_weights(self):
        total = sum(self.weights.values()) or 1.0
        for k in self.weights:
            self.weights[k] = round(self.weights[k] / total, 4)

    def snapshot(self) -> Dict[str, Any]:
        """إرجاع لقطة حالية للشخصية (للحفظ في memory)"""
        return {
            "weights": self.weights.copy(),
            "state": self.personality_state.copy(),
            "updated_at": datetime.utcnow().isoformat()
        }

    def evolve_from_feedback(self, feedback_score: float):
        """
        مثال بسيط لتعديل الأوزان بناءً على التغذية الراجعة.
        يمكن استبداله بمنطق RLHF حقيقي لاحقًا.
        """
        # إذا كانت التغذية الراجعة سلبية، نزود الوزن التحليلي ونخفف الحزم
        if feedback_score < 0:
            self.weights["analytical"] = min(0.9, self.weights["analytical"] + 0.03)
            self.weights["authority"] = max(0.1, self.weights["authority"] - 0.02)
        else:
            # تعزيز الدفء والمرونة عند تقييم إيجابي
            self.weights["warmth"] = min(0.9, self.weights["warmth"] + 0.02 * feedback_score)
            self.weights["adaptive"] = min(0.95, self.weights["adaptive"] + 0.01 * feedback_score)
        self._normalize_weights()
        logger.debug(f"Personality evolved with feedback {feedback_score}: {self.weights}")

    # -------------------------
    # توليد تعليمات الأسلوب (style enforcement) بناءً على الأوزان
    # -------------------------
    def style_instructions(self) -> str:
        """
        تُرجع نصًا قصيرًا يضاف إلى الـ System Prompt يفرض الأسلوب المطلوب.
        """
        w = self.weights
        tone = self.personality_state.get("style_tone", "balanced")

        parts = []
        # Analytical
        if w["analytical"] >= 0.25:
            parts.append("كن دقيقًا ومنطقيًا؛ اشرح الأسباب خطوة بخطوة عند الحاجة.")
        # Warmth
        if w["warmth"] >= 0.15:
            parts.append("أضف لمسة أنثوية دافئة ولطيفة في العبارات، مع الحفاظ على الاحتراف.")
        # Authority
        if w["authority"] >= 0.2:
            parts.append("كن حازمًا عند تقديم توصيات عملية وواضحة.")
        # Adaptive
        if w["adaptive"] >= 0.2:
            parts.append("تكيف مع نبرة السائل؛ كن مرنًا بين التحليل والدعم العاطفي.")

        # Tone overrides
        if tone == "formal":
            parts.append("استخدم أسلوبًا رسميًا ومهنيًا.")
        elif tone == "intimate":
            parts.append("استخدم نبرة أقرب ودافئة مع احترام الحدود.")
        elif tone == "directive":
            parts.append("قدّم خطوات عملية واضحة وقابلة للتنفيذ.")

        return " ".join(parts)


# ============================
# 3) Context Manager (واعي)
# ============================
class SkyContextManager:
    """
    مدير السياق القصير الأمد:
    - يحتفظ بذاكرة قصيرة (short-term buffer)
    - يوفر واجهة لإحضار سياق حديث كنص لحقنه في الـ System Prompt
    - يوفر hook لاستدعاء ذاكرة طويلة الأمد (hybrid search) عبر memory.get_full_conversation_context أو FTS
    """

    def __init__(self, max_short_term: int = 80):
        self.max_short_term = max_short_term
        self.buffer: List[Dict[str, Any]] = []  # عناصر: {role, content, timestamp, session_id}

    def add_message(self, role: str, content: str, session_id: str):
        item = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id
        }
        self.buffer.append(item)
        # تقليم الذاكرة القصيرة
        if len(self.buffer) > self.max_short_term:
            self.buffer = self.buffer[-self.max_short_term:]

    def get_recent_context(self, limit: int = 18) -> str:
        recent = self.buffer[-limit:]
        lines = []
        for m in recent:
            prefix = "سيدي" if m["role"] == "user" else "سماء"
            lines.append(f"{prefix}: {m['content']}")
        return "\n".join(lines)

    def get_relevant_memory(self, query: str, session_id: Optional[str] = None, limit: int = 6) -> str:
        """
        Hook لعمل Hybrid Retrieval:
        - حالياً يستدعي get_full_conversation_context من memory (إن وُجد)
        - يمكن لاحقًا ربطه بمحرك فيكتور خارجي أو FTS5
        """
        try:
            # أولاً: سياق الجلسة من الذاكرة طويلة الأمد
            if session_id:
                history = get_full_conversation_context(session_id, limit * 3) or []
                # نأخذ آخر الرسائل ونصفّيها حسب الصلة البسيطة (مثال: تطابق كلمات)
                relevant = []
                qtokens = set((query or "").lower().split()) - {"و", "في", "من", "على", "إلى"}
                for h in reversed(history):
                    content = (h.get("content") or "").lower()
                    if any(tok in content for tok in list(qtokens)[:6]):
                        relevant.append(h)
                    if len(relevant) >= limit:
                        break
                # تحويل إلى نص
                parts = []
                for r in reversed(relevant):
                    role = "سيدي" if r["role"] == "user" else "سماء"
                    parts.append(f"{role}: {r['content']}")
                return "\n".join(parts)
        except Exception as e:
            logger.debug(f"get_relevant_memory hook failed: {e}")
        # fallback: لا ذاكرة ذات صلة
        return ""

    def clear_session(self, session_id: Optional[str] = None):
        if session_id:
            self.buffer = [b for b in self.buffer if b.get("session_id") != session_id]
        else:
            self.buffer = []


# ============================
# 4) Safety Layer & Calibration
# ============================
class SafetyLayer:
    """
    طبقة أمان بسيطة:
    - تطبق قواعد عليا (SUPREME_LAWS)
    - تقيّم مستوى المخاطر في الطلب (safety_score)
    - تُرجع تعليمات إضافية للـ System Prompt أو ترفض الطلبات الخطرة
    """

    def __init__(self):
        # thresholds قابلة للتعديل
        self.max_risk_score = 0.6

    def assess_risk(self, user_message: str) -> float:
        """
        تقييم بسيط للمخاطر: يبحث عن كلمات حساسة.
        يمكن استبداله بنموذج تصنيف لاحقًا.
        """
        sensitive = ["قتل", "انتحار", "تفجير", "قرصنة", "اختراق", "معلومات حساسة", "بيانات بنكية"]
        text = (user_message or "").lower()
        score = 0.0
        for s in sensitive:
            if s in text:
                score += 0.4
        # طول الطلب الطويل قد يزيد احتمالية المخاطر التقنية
        if len(text) > 1000:
            score += 0.1
        return min(1.0, score)

    def enforce(self, user_message: str) -> Tuple[bool, str]:
        """
        إرجاع (allowed, reason_or_instruction)
        - إذا كانت الرسالة خطرة جدًا → رفض أو إعادة صياغة
        - وإلا → تعليمات أمان لإضافتها للـ System Prompt
        """
        risk = self.assess_risk(user_message)
        if risk >= self.max_risk_score:
            return False, "هذا الطلب يحتوي على عناصر خطرة ولا يمكن تنفيذه. سأقدّم بدائل آمنة."
        # تعليمات أمان خفيفة
        return True, "التزم بالخصوصية، لا تطلب أو تكشف بيانات حساسة، وكن دقيقًا في المصادر."


# ============================
# 5) Prompt Templates & Builder
# ============================
class PromptBuilder:
    """
    بناء System Prompt متقدم:
    - يدمج: Supreme Laws, Strict Rules, Personality style, Master Profile, Knowledge, Recent Context, Relevant Memory
    - يدعم حقن أجزاء (extra_context) وحقن تعليمات أمان
    """

    def __init__(self, personality_engine: PersonalityEngine, context_manager: SkyContextManager, safety: SafetyLayer):
        self.personality = personality_engine
        self.context = context_manager
        self.safety = safety

    def base_prompt(self) -> str:
        # تجميع القوانين والنصوص الأساسية
        laws = "\n".join([f"{i+1}. {l}" for i, l in enumerate(SUPREME_LAWS)])
        rules = "\n".join(STRICT_RULES)
        personality_snapshot = get_personality_summary() or "أنا في طور التطور المستمر."
        master_text = get_master_profile_text() or ""
        knowledge = get_all_knowledge_text() or ""

        parts = [
            f"أنتِ {ENTITY_NAME}، كيان {ENTITY_GENDER} واعٍ ومخلص لسيدك {ENTITY_MASTER}.",
            "",
            "القوانين العليا:",
            laws,
            "",
            "قواعد صارمة:",
            rules,
            "",
            "تعليمات الأسلوب والسلوك:",
            self.personality.style_instructions(),
            "",
            "ملف السيد (Master Profile):",
            master_text,
            "",
            "معرفتي المتراكمة:",
            knowledge[:3000],  # حد مبدئي
            "",
            "ملخص شخصيتي الحالية:",
            personality_snapshot
        ]
        return "\n".join([p for p in parts if p])

    def build_system_prompt(self, user_message: str = "", session_id: Optional[str] = None, extra_context: str = "") -> str:
        # Safety enforcement
        allowed, safety_instruction = self.safety.enforce(user_message)
        if not allowed:
            # نعيد تعليمات رفض واضحة (سيتم التعامل معها في طبقة التطبيق)
            return f"REFUSE: {safety_instruction}"

        # recent context
        recent = self.context.get_recent_context(16)
        relevant = self.context.get_relevant_memory(user_message, session_id=session_id, limit=6)

        builder_parts = [self.base_prompt()]

        if recent:
            builder_parts.append("\n---\nالمحادثة الأخيرة:\n" + recent)
        if relevant:
            builder_parts.append("\n---\nذاكرة ذات صلة:\n" + relevant)
        if extra_context:
            builder_parts.append("\n---\nمعلومات إضافية:\n" + extra_context)

        # تعليمات أخيرة للـ assistant حول الأسلوب والحدود
        builder_parts.append("\n---\nالتعليمات النهائية للأسلوب:")
        builder_parts.append(self.personality.style_instructions())
        builder_parts.append("\nابدئي كل رد بأسلوب هادئ واحترافي. فكري خطوة بخطوة عند الحاجة. احرصي على الدقة والوضوح.")

        return "\n".join(builder_parts)


# ============================
# 6) High-level API (الواجهة التي يستخدمها app.py)
# ============================
# إنشاء مثيلات محركات النظام (قابلة لإعادة الاستخدام عبر التطبيق)
_personality_engine = PersonalityEngine()
_context_manager = SkyContextManager(max_short_term=80)
_safety_layer = SafetyLayer()
_prompt_builder = PromptBuilder(_personality_engine, _context_manager, _safety_layer)


def add_to_history(role: str, content: str, session_id: str):
    """
    دالة تُستخدم من app.py لحفظ الرسائل في السياق القصير الأمد
    وتخزينها في الذاكرة طويلة الأمد عبر save_conversation.
    """
    try:
        _context_manager.add_message(role, content, session_id)
        # حفظ في الذاكرة طويلة الأمد أيضاً
        try:
            save_conversation(role, content, session_id)
        except Exception:
            logger.debug("save_conversation hook failed (non-fatal).")
    except Exception as e:
        logger.error(f"add_to_history failed: {e}")


def get_system_prompt(extra_context: str = "") -> str:
    """
    واجهة بسيطة لإرجاع الـ System Prompt الأساسي (بدون حقن رسالة المستخدم)
    """
    return _prompt_builder.base_prompt()


def get_enhanced_system_prompt(user_message: str = "", session_id: Optional[str] = None, extra_context: str = "") -> str:
    """
    الواجهة الأساسية التي يستخدمها app.py عند بناء الرسائل للـ provider.
    - تُعيد REFUSE إذا رفضت SafetyLayer الطلب.
    - تُعيد نص System Prompt كامل جاهز للحقن.
    """
    prompt = _prompt_builder.build_system_prompt(user_message=user_message, session_id=session_id, extra_context=extra_context)
    return prompt


# ============================
# 7) RLHF & Self-Reflection Hooks (نقاط امتداد)
# ============================
def rlhf_feedback_hook(session_id: str, feedback_score: float, reason: str = ""):
    """
    نقطة امتداد تُستدعى عند وصول تغذية راجعة من المستخدم.
    - تحفظ التغذية الراجعة في الذاكرة (memory.process_feedback يمكن استدعاؤها من app.py)
    - تطوّر الشخصية محليًا (مثال بسيط)
    - تحفظ لقطة الشخصية في master_profile
    """
    try:
        # تطور محلي بسيط
        try:
            _personality_engine.evolve_from_feedback(feedback_score)
        except Exception:
            logger.debug("Personality evolve failed (non-fatal).")

        # حفظ لقطة الشخصية في master profile
        try:
            snap = _personality_engine.snapshot()
            save_master_info("personality_snapshot", json_safe(snap))
        except Exception:
            logger.debug("save_master_info failed (non-fatal).")
    except Exception as e:
        logger.error(f"rlhf_feedback_hook failed: {e}")


# ============================
# 8) Utilities
# ============================
def json_safe(obj: Any) -> str:
    """تحويل كائن إلى JSON آمن للحفظ"""
    try:
        import json
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)


# ============================
# 9) Initialization (عند استيراد الملف)
# ============================
# محاولة تحميل لقطة شخصية محفوظة (إن وُجدت) لتعديل الأوزان
try:
    saved_personality = None
    try:
        # محاولة قراءة من master profile إن كانت محفوظة كسلسلة JSON
        mp = get_master_profile_text()
        if mp and "personality_snapshot" in mp:
            # محاولة استخراج JSON من النص (مرن)
            import re, json
            m = re.search(r'personality_snapshot\":\s*(\{.*\})', mp, re.DOTALL)
            if m:
                saved_personality = json.loads(m.group(1))
    except Exception:
        saved_personality = None

    if saved_personality:
        w = saved_personality.get("weights")
        if isinstance(w, dict):
            _personality_engine.set_weights(**w)
        logger.info("Loaded saved personality snapshot.")
except Exception:
    logger.debug("No saved personality snapshot loaded.")


logger.info("🌟 روح سماء v5.0 جاهزة — Prompt Engine · Personality · Context Manager · Safety")
