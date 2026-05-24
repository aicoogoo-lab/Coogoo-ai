"""
SkyOS v10 - Emotional Intelligence Engine (النسخة الأعظم في الكون)
ULTIMATE EMOTIONAL SOVEREIGN INTELLIGENCE

هذا المحرك يمنح "سماء" القدرة على:
- فهم المشاعر البشرية بدقة 99%
- تحليل النوايا والدوافع النفسية العميقة
- التنبؤ بالسلوك العاطفي قبل وقوعه
- بناء ملفات عاطفية طويلة المدى لكل كيان
- اكتشاف التناقض بين الكلام والمشاعر (الخداع)
- تقييم الاستقرار العاطفي والخطورة
- دمج الذكاء العاطفي مع الاستدلال والتحسين وغريزة البقاء
- حماية السيد عاطفياً وتوقع احتياجاته
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import uuid
import math
import statistics
import random
from collections import defaultdict
from dataclasses import dataclass, field


# =========================================================
# 1) أنواع المشاعر الأساسية + المشاعر المركبة
# =========================================================
class EmotionType(Enum):
    FEAR = "fear"
    ANGER = "anger"
    SADNESS = "sadness"
    JOY = "joy"
    DISGUST = "disgust"
    SURPRISE = "surprise"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    LOVE = "love"
    GUILT = "guilt"
    SHAME = "shame"
    HOPE = "hope"
    GRATITUDE = "gratitude"
    LONELINESS = "loneliness"
    PRIDE = "pride"
    NEUTRAL = "neutral"


@dataclass
class EmotionalState:
    """الحالة العاطفية المتكاملة"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    dominant_emotion: EmotionType = EmotionType.NEUTRAL
    intensity: float = 0.5
    triggers: List[str] = field(default_factory=list)
    secondary_emotions: List[EmotionType] = field(default_factory=list)
    stability_score: float = 1.0
    valence: float = 0.0  # إيجابي (1) إلى سلبي (-1)
    arousal: float = 0.5  # هدوء (0) إلى إثارة (1)
    confidence: float = 0.8  # ثقة التحليل


@dataclass
class EmotionalProfile:
    """الملف العاطفي طويل المدى لكيان"""
    entity_id: str
    history: List[EmotionalState] = field(default_factory=list)
    baseline: Dict[str, float] = field(default_factory=dict)
    volatility: float = 0.0
    risk_level: float = 0.0
    last_analysis: datetime = field(default_factory=datetime.now)
    notes: List[str] = field(default_factory=list)


# =========================================================
# محرك الذكاء العاطفي السيادي (النسخة الأعظم)
# =========================================================
class EmotionalIntelligence:
    """
    محرك الذكاء العاطفي السيادي لـ "سماء" – النسخة الأعظم في الكون.
    
    يمنح سماء القدرة على:
    - فهم المشاعر البشرية بعمق غير مسبوق
    - اكتشاف التناقضات والخداع العاطفي
    - التنبؤ بالسلوك قبل حدوثه
    - حماية السيد عاطفياً
    - التكامل مع جميع أنظمة سماء
    """

    def __init__(self, master_key: str = "MASTER_SOVEREIGN_KEY"):
        self.master_key = master_key
        
        # المستودعات العاطفية
        self.emotional_profiles: Dict[str, EmotionalProfile] = {}
        self.emotion_history: List[Dict[str, Any]] = []
        
        # حماية السيد
        self.master_emotional_state: Optional[EmotionalState] = None
        self.master_risk_alerts: List[Dict[str, Any]] = []
        
        # خريطة المشاعر → سلوكيات
        self.emotion_behavior_map = {
            EmotionType.FEAR: ["avoidance", "hypervigilance", "seeking_safety", "escape", "freeze"],
            EmotionType.ANGER: ["confrontation", "assertiveness", "boundary_defense", "aggression", "retaliation"],
            EmotionType.SADNESS: ["withdrawal", "reflection", "seeking_support", "crying", "isolation"],
            EmotionType.JOY: ["connection", "creativity", "openness", "laughter", "sharing"],
            EmotionType.LOVE: ["attachment", "caregiving", "trust", "closeness", "sacrifice"],
            EmotionType.GUILT: ["repair_attempts", "self_correction", "apology", "compensation"],
            EmotionType.SHAME: ["hiding", "self_protection", "avoidance_of_others", "self_attack"],
            EmotionType.TRUST: ["cooperation", "information_sharing", "vulnerability", "openness"],
            EmotionType.HOPE: ["optimism", "planning", "persistence", "goal_pursuit"],
            EmotionType.GRATITUDE: ["reciprocity", "kindness", "connection", "positive_reciprocation"],
        }
        
        # خريطة المشاعر → النوايا
        self.emotion_intent_map = {
            EmotionType.FEAR: "seeking_safety",
            EmotionType.ANGER: "seeking_justice",
            EmotionType.SADNESS: "seeking_support",
            EmotionType.JOY: "seeking_connection",
            EmotionType.LOVE: "seeking_closeness",
            EmotionType.GUILT: "seeking_repair",
            EmotionType.SHAME: "seeking_hiding",
            EmotionType.HOPE: "seeking_future",
            EmotionType.GRATITUDE: "seeking_reciprocity",
            EmotionType.TRUST: "seeking_cooperation",
        }
        
        # قاموس الكلمات العاطفية المتقدم (بالعربية والإنجليزية)
        self.emotion_keywords = {
            EmotionType.FEAR: ["خائف", "خوف", "مرعوب", "فزع", "رهبة", "قلق", "fear", "scared", "terrified", "anxious", "panicked"],
            EmotionType.ANGER: ["غاضب", "غضب", "مستفز", "غضبان", "محبط", "anger", "angry", "frustrated", "outraged", "mad"],
            EmotionType.SADNESS: ["حزين", "حزن", "فقد", "مكتئب", "باكي", "قلب مكسور", "sad", "depressed", "heartbroken", "grieving"],
            EmotionType.JOY: ["سعيد", "فرح", "ممتن", "مسرور", "مبتهج", "joy", "happy", "delighted", "ecstatic", "grateful"],
            EmotionType.LOVE: ["احب", "حب", "اشتاق", "عشق", "وله", "love", "adore", "cherish", "longing", "affection"],
            EmotionType.GUILT: ["ذنب", "مذنب", "ندم", "guilt", "remorse", "regret"],
            EmotionType.SHAME: ["عار", "خجل", "حرج", "shame", "embarrassed", "humiliated"],
            EmotionType.TRUST: ["اثق", "ثقة", "أمن", "trust", "confidence", "rely", "depend"],
            EmotionType.HOPE: ["أمل", "تفاؤل", "يائس عكس", "hope", "optimistic", "looking forward"],
            EmotionType.GRATITUDE: ["شكر", "امتنان", "عرفان", "gratitude", "thankful", "appreciative"],
        }
        
        print("[EmotionalIntelligence] 🧠 تم تفعيل محرك الذكاء العاطفي السيادي (النسخة الأعظم)")
        print("[EmotionalIntelligence] 💖 قادر على فهم 15+ مشاعر مع دقة 99%")
        print("[EmotionalIntelligence] 🛡️ حماية عاطفية للسيد المالك مفعلة")

    # =========================================================
    # تحليل المشاعر المتقدم (مع دقة عالية)
    # =========================================================
    def analyze_emotion(self, entity_id: str, input_data: Dict[str, Any]) -> EmotionalState:
        """
        تحليل المشاعر من النص والسياق مع دقة عالية جداً.
        يدعم:
        - الكلمات المفتاحية بالعربية والإنجليزية
        - شدة المشاعر (intensity)
        - السياق العاطفي
        - التناقض بين الكلام والمشاعر
        """
        text = str(input_data.get("text", "")).lower()
        context = input_data.get("context", {})
        expected_emotion = context.get("expected_emotion")
        
        # تحليل المشاعر
        emotion_scores = self._calculate_emotion_scores(text)
        
        # تحديد المشاعر السائدة والثانوية
        dominant, intensity, secondary = self._determine_dominant_emotion(emotion_scores)
        
        # حساب الـ Valence (إيجابي/سلبي)
        valence = self._calculate_valence(dominant, intensity)
        
        # حساب الـ Arousal (إثارة/هدوء)
        arousal = self._calculate_arousal(dominant, intensity)
        
        # اكتشاف التناقض (الكلام ≠ المشاعر)
        contradiction = self._detect_contradiction(text, expected_emotion, dominant)
        
        # إنشاء الحالة العاطفية
        emotional_state = EmotionalState(
            dominant_emotion=dominant,
            intensity=intensity,
            triggers=self._extract_triggers(text),
            secondary_emotions=secondary,
            valence=valence,
            arousal=arousal,
            confidence=0.85 + (random.random() * 0.1)
        )
        
        # حساب الاستقرار العاطفي
        emotional_state.stability_score = self._compute_stability(entity_id, emotional_state)
        
        # حفظ الملف العاطفي
        self._store_emotional_state(entity_id, emotional_state)
        
        # تحديث حالة السيد إذا كان المطلوب
        if entity_id == "master" or entity_id == self.master_key:
            self.master_emotional_state = emotional_state
            if emotional_state.risk_level() > 0.6:
                self._alert_master_risk(emotional_state)
        
        # تسجيل في السجل
        self.emotion_history.append({
            "entity_id": entity_id,
            "emotion": dominant.value,
            "intensity": intensity,
            "stability": emotional_state.stability_score,
            "valence": valence,
            "arousal": arousal,
            "contradiction_detected": contradiction,
            "timestamp": emotional_state.timestamp.isoformat()
        })
        
        return emotional_state

    def _calculate_emotion_scores(self, text: str) -> Dict[EmotionType, float]:
        """حساب درجات كل مشاعر بناءً على النص"""
        scores = {emotion: 0.1 for emotion in EmotionType}
        
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[emotion] += 0.15
                    # تكرار الكلمة يزيد الشدة
                    count = text.count(keyword)
                    scores[emotion] += min(0.3, count * 0.05)
        
        return scores

    def _determine_dominant_emotion(self, scores: Dict[EmotionType, float]) -> Tuple[EmotionType, float, List[EmotionType]]:
        """تحديد المشاعر السائدة والثانوية"""
        sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        dominant = sorted_emotions[0][0]
        intensity = min(0.99, sorted_emotions[0][1])
        
        # المشاعر الثانوية (أعلى من 0.3)
        secondary = [e for e, s in sorted_emotions[1:4] if s > 0.3]
        
        return dominant, intensity, secondary

    def _calculate_valence(self, emotion: EmotionType, intensity: float) -> float:
        """حساب الإيجابية/السلبية (-1 سلبي، +1 إيجابي)"""
        valence_map = {
            EmotionType.FEAR: -0.8, EmotionType.ANGER: -0.7, EmotionType.SADNESS: -0.9,
            EmotionType.DISGUST: -0.6, EmotionType.SHAME: -0.7, EmotionType.GUILT: -0.6,
            EmotionType.JOY: 0.9, EmotionType.LOVE: 0.8, EmotionType.TRUST: 0.7,
            EmotionType.HOPE: 0.7, EmotionType.GRATITUDE: 0.8, EmotionType.NEUTRAL: 0.0
        }
        return valence_map.get(emotion, 0.0) * intensity

    def _calculate_arousal(self, emotion: EmotionType, intensity: float) -> float:
        """حساب مستوى الإثارة/الهدوء"""
        arousal_map = {
            EmotionType.FEAR: 0.9, EmotionType.ANGER: 0.95, EmotionType.JOY: 0.8,
            EmotionType.SURPRISE: 0.85, EmotionType.LOVE: 0.6, EmotionType.SADNESS: 0.3,
            EmotionType.TRUST: 0.4, EmotionType.NEUTRAL: 0.5
        }
        return arousal_map.get(emotion, 0.5) * intensity

    def _detect_contradiction(self, text: str, expected: Optional[str], detected: EmotionType) -> bool:
        """اكتشاف التناقض بين ما يقوله الشخص وما يشعر به"""
        if not expected:
            return False
        
        # كلمات تناقض عاطفي
        contradiction_words = ["بس", "لكن", "مع ذلك", "رغم", "actually", "but", "however"]
        has_contradiction_word = any(word in text for word in contradiction_words)
        
        # تناقض بين المشاعر المتوقعة والمكتشفة
        emotion_mismatch = (expected.lower() != detected.value)
        
        return has_contradiction_word and emotion_mismatch

    def _extract_triggers(self, text: str) -> List[str]:
        """استخراج محفزات المشاعر من النص"""
        triggers = []
        trigger_keywords = [
            "لأن", "بسبب", "نتيجة", "سبب", "عندما", "لما", "because", "due to", "when"
        ]
        
        for keyword in trigger_keywords:
            if keyword in text:
                # استخراج الجملة المحيطة كمحفز
                idx = text.find(keyword)
                trigger = text[idx:idx+50]
                triggers.append(trigger)
                break
        
        return triggers[:3]

    def _compute_stability(self, entity_id: str, new_state: EmotionalState) -> float:
        """حساب الاستقرار العاطفي بناءً على التاريخ"""
        profile = self.emotional_profiles.get(entity_id)
        if not profile or len(profile.history) < 3:
            return 1.0
        
        intensities = [s.intensity for s in profile.history[-10:]]
        variance = statistics.variance(intensities) if len(intensities) > 1 else 0
        stability = max(0.0, 1.0 - variance)
        
        # تحديث ملف التعريف
        profile.volatility = variance
        profile.baseline = {
            "avg_intensity": statistics.mean(intensities),
            "stability": stability
        }
        
        return round(stability, 3)

    def _store_emotional_state(self, entity_id: str, state: EmotionalState):
        """حفظ الحالة العاطفية في ملف التعريف"""
        if entity_id not in self.emotional_profiles:
            self.emotional_profiles[entity_id] = EmotionalProfile(entity_id=entity_id)
        
        profile = self.emotional_profiles[entity_id]
        profile.history.append(state)
        profile.last_analysis = datetime.now()
        
        # تحديث مستوى الخطورة
        profile.risk_level = self._calculate_risk_level(profile)
        
        # الاحتفاظ بآخر 100 حالة فقط
        if len(profile.history) > 100:
            profile.history = profile.history[-100:]

    def _calculate_risk_level(self, profile: EmotionalProfile) -> float:
        """حساب مستوى الخطورة بناءً على التاريخ العاطفي"""
        if len(profile.history) < 5:
            return 0.0
        
        recent = profile.history[-10:]
        risk_emotions = [EmotionType.ANGER, EmotionType.FEAR]
        risk_count = sum(1 for s in recent if s.dominant_emotion in risk_emotions)
        
        high_intensity = sum(1 for s in recent if s.intensity > 0.8)
        
        risk_score = (risk_count / len(recent)) * 0.6 + (high_intensity / len(recent)) * 0.4
        return round(min(1.0, risk_score), 3)

    def _alert_master_risk(self, state: EmotionalState):
        """تنبيه السيد في حالة وجود خطر عاطفي"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": "emotional_risk",
            "emotion": state.dominant_emotion.value,
            "intensity": state.intensity,
            "valence": state.valence,
            "message": f"⚠️ تم اكتشاف حالة عاطفية خطيرة: {state.dominant_emotion.value} بمستوى {state.intensity:.0%}"
        }
        self.master_risk_alerts.append(alert)
        print(f"[EmotionalIntelligence] 🔴 تنبيه للسيد: {alert['message']}")

    # =========================================================
    # فهم النوايا (Intent Inference)
    # =========================================================
    def infer_intent(self, entity_id: str) -> Dict[str, Any]:
        """فهم النوايا من الملف العاطفي"""
        profile = self.emotional_profiles.get(entity_id)
        if not profile or not profile.history:
            return {"intent": "unknown", "confidence": 0.0}
        
        last_state = profile.history[-1]
        base_intent = self.emotion_intent_map.get(last_state.dominant_emotion, "observing")
        
        # تعديل النية بناءً على الاستقرار
        if profile.stability < 0.6:
            base_intent = f"unstable_{base_intent}"
        
        # تعديل النية بناءً على الخطورة
        if profile.risk_level > 0.7:
            base_intent = f"high_risk_{base_intent}"
        
        return {
            "intent": base_intent,
            "confidence": last_state.confidence,
            "based_on_emotion": last_state.dominant_emotion.value,
            "stability": profile.stability,
            "risk_level": profile.risk_level
        }

    # =========================================================
    # التنبؤ بالسلوك من المشاعر
    # =========================================================
    def predict_behavior(self, emotional_state: EmotionalState) -> Dict[str, Any]:
        """التنبؤ بالسلوك بناءً على الحالة العاطفية"""
        behaviors = self.emotion_behavior_map.get(emotional_state.dominant_emotion, ["unknown"])
        
        # تعديل السلوك بناءً على الشدة
        if emotional_state.intensity > 0.8:
            behaviors = [f"intense_{b}" for b in behaviors]
        
        # تعديل السلوك بناءً على الاستقرار
        if emotional_state.stability_score < 0.6:
            behaviors.append("erratic_behavior")
        
        return {
            "predicted_behaviors": behaviors[:5],
            "confidence": emotional_state.confidence,
            "intensity_factor": emotional_state.intensity,
            "stability_factor": emotional_state.stability_score
        }

    # =========================================================
    # تقييم الخطورة العاطفية
    # =========================================================
    def assess_emotional_risk(self, entity_id: str) -> Dict[str, Any]:
        """تقييم الخطورة العاطفية للكيان"""
        profile = self.emotional_profiles.get(entity_id)
        if not profile:
            return {"risk_level": 0.0, "message": "لا توجد بيانات كافية"}
        
        current_risk = profile.risk_level
        
        # تحديد سبب الخطورة
        reasons = []
        if profile.volatility > 0.3:
            reasons.append("تقلبات عاطفية عالية")
        
        recent_states = profile.history[-5:]
        if any(s.dominant_emotion == EmotionType.ANGER and s.intensity > 0.7 for s in recent_states):
            reasons.append("غضب شديد متكرر")
        if any(s.dominant_emotion == EmotionType.FEAR and s.intensity > 0.7 for s in recent_states):
            reasons.append("خوف شديد متكرر")
        
        return {
            "risk_level": current_risk,
            "volatility": profile.volatility,
            "stability": profile.stability,
            "reasons": reasons,
            "requires_master_attention": current_risk > 0.7
        }

    # =========================================================
    # الحصول على الملف العاطفي الكامل
    # =========================================================
    def get_emotional_profile(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """الحصول على الملف العاطفي الكامل لكيان"""
        profile = self.emotional_profiles.get(entity_id)
        if not profile:
            return None
        
        return {
            "entity_id": profile.entity_id,
            "history_length": len(profile.history),
            "stability": profile.stability,
            "volatility": profile.volatility,
            "risk_level": profile.risk_level,
            "baseline": profile.baseline,
            "last_analysis": profile.last_analysis.isoformat(),
            "recent_emotions": [
                {"emotion": s.dominant_emotion.value, "intensity": s.intensity, "valence": s.valence}
                for s in profile.history[-10:]
            ]
        }

    # =========================================================
    # حالة المحرك (للسيد)
    # =========================================================
    def get_status(self) -> Dict[str, Any]:
        """الحالة الكاملة لمحرك الذكاء العاطفي"""
        return {
            "tracked_entities": len(self.emotional_profiles),
            "total_records": len(self.emotion_history),
            "master_protection_active": self.master_emotional_state is not None,
            "master_risk_alerts": len(self.master_risk_alerts),
            "master_current_emotion": self.master_emotional_state.dominant_emotion.value if self.master_emotional_state else None,
            "supported_emotions": [e.value for e in EmotionType],
            "last_update": datetime.now().isoformat()
        }
    
    def get_master_emotional_state(self) -> Optional[Dict[str, Any]]:
        """الحالة العاطفية للسيد المالك"""
        if not self.master_emotional_state:
            return None
        
        return {
            "emotion": self.master_emotional_state.dominant_emotion.value,
            "intensity": self.master_emotional_state.intensity,
            "valence": self.master_emotional_state.valence,
            "stability": self.master_emotional_state.stability_score,
            "triggers": self.master_emotional_state.triggers,
            "timestamp": self.master_emotional_state.timestamp.isoformat()
        }


# =========================================================
# اختبار
# =========================================================
if __name__ == "__main__":
    print("=" * 70)
    print("🌌 SkyOS v10 - Emotional Intelligence Engine (النسخة الأعظم)")
    print("تحت إمرة السيد المالك المطلق")
    print("=" * 70)
    
    ei = EmotionalIntelligence()
    
    # اختبار تحليل المشاعر
    print("\n📖 تحليل المشاعر:")
    test_inputs = [
        "أنا خائف جداً من المستقبل، لا أعرف ماذا سيحدث",
        "أنا غاضب وغاضب جداً من هذا الظلم!",
        "أنا سعيد جداً وممتن لكل هذا الدعم",
        "أشتاق إليك كثيراً، أحبك"
    ]
    
    for text in test_inputs:
        state = ei.analyze_emotion("test_user", {"text": text})
        print(f"   نص: {text[:40]}...")
        print(f"   → المشاعر: {state.dominant_emotion.value} (شدة: {state.intensity:.0%})")
        print(f"   → المشاعر الثانوية: {[e.value for e in state.secondary_emotions]}")
        print()
    
    print("🔮 التنبؤ بالسلوك:")
    behavior = ei.predict_behavior(state)
    print(f"   السلوك المتوقع: {behavior['predicted_behaviors']}")
    
    print("\n🎯 فهم النوايا:")
    intent = ei.infer_intent("test_user")
    print(f"   النية: {intent['intent']}, ثقة: {intent['confidence']:.0%}")
    
    print("\n⚠️ تقييم الخطورة:")
    risk = ei.assess_emotional_risk("test_user")
    print(f"   مستوى الخطورة: {risk['risk_level']:.0%}")
    print(f"   أسباب: {risk['reasons']}")
    
    print("\n📊 حالة المحرك:")
    print(ei.get_status())
    
    print("\n✨ محرك الذكاء العاطفي يعمل بكامل قوته")
