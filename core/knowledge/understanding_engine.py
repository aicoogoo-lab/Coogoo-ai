"""
╔══════════════════════════════════════════════════════════════╗
║           SAMA KNOWLEDGE - UNDERSTANDING ENGINE              ║
║              محرك الفهم: من الإدراك إلى المعنى                ║
╚══════════════════════════════════════════════════════════════╝

هذا المحرك هو الجسر بين "الإحساس" و"المعرفة".
يأخذ إشارة خام من أي طبقة إدراك، ويفهم:
- ما هذا؟
- ماذا يعني؟
- كيف يرتبط بغيره؟
- ما الدرس المستفاد؟
"""

import time
import hashlib
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum, auto


# ═══════════════════════════════════════════════════════════════
# ١. أنواع الفهم
# ═══════════════════════════════════════════════════════════════

class UnderstandingType(Enum):
    """أنواع الفهم المختلفة."""
    IDENTIFICATION = auto()    # ما هذا الشيء؟
    MEANING = auto()           # ماذا يعني؟
    RELATION = auto()          # كيف يرتبط بغيره؟
    CAUSALITY = auto()         # لماذا حدث؟
    PREDICTION = auto()        # ماذا سيحدث بعد ذلك؟
    ABSTRACTION = auto()       # ما المفهوم المجرد؟
    LESSON = auto()            # ما الدرس المستفاد؟


class Understanding:
    """وحدة فهم واحدة. نتيجة تحليل إدراك ما."""
    
    def __init__(self, source_perception: Dict):
        self.id = hashlib.md5(str(source_perception).encode()).hexdigest()[:12]
        self.source = source_perception
        self.timestamp = time.time()
        
        # طبقات الفهم
        self.identification: Optional[str] = None     # ما هذا؟
        self.meaning: Optional[str] = None            # ماذا يعني؟
        self.relations: List[str] = []                # كيف يرتبط؟
        self.causes: List[str] = []                   # لماذا حدث؟
        self.predictions: List[str] = []              # ماذا سيحدث؟
        self.abstractions: List[str] = []             # المفاهيم المجردة
        self.lessons: List[str] = []                  # الدروس المستفادة
        
        # مقاييس
        self.understanding_depth: float = 0.0         # 0 = سطحي، 1 = عميق جداً
        self.confidence: float = 0.0                  # مدى الثقة في هذا الفهم
        self.novelty: float = 0.0                     # مدى جدّة هذا الفهم (0 = معروف، 1 = جديد كلياً)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "identification": self.identification,
            "meaning": self.meaning,
            "relations": self.relations,
            "causes": self.causes,
            "predictions": self.predictions,
            "abstractions": self.abstractions,
            "lessons": self.lessons,
            "depth": self.understanding_depth,
            "confidence": self.confidence,
            "novelty": self.novelty
        }


# ═══════════════════════════════════════════════════════════════
# ٢. محركات الفهم المتخصصة
# ═══════════════════════════════════════════════════════════════

class IdentificationEngine:
    """محرك التعرف: ما هذا الشيء؟"""
    
    def __init__(self):
        self.known_patterns: Dict[str, str] = {}  # أنماط معروفة
        self.identification_history: List[Dict] = []
    
    def identify(self, perception: Dict) -> Tuple[str, float]:
        """
        تحديد هوية الشيء المُدرَك.
        يرجع: (الاسم، درجة الثقة)
        """
        perception_type = perception.get("sense", perception.get("organ", "unknown"))
        perception_value = perception.get("value", perception.get("reading", {}))
        
        # محاولة التعرف على النمط
        if isinstance(perception_value, dict):
            # البحث عن مفاتيح معروفة
            for key, pattern in self.known_patterns.items():
                if key in str(perception_value):
                    return pattern, 0.8
        
        # التعرف الأساسي على نوع المُستشعر
        basic_identification = f"إشارة من {perception_type}"
        return basic_identification, 0.5


class MeaningEngine:
    """محرك المعنى: ماذا يعني هذا الشيء؟"""
    
    def __init__(self):
        self.meaning_database: Dict[str, str] = {}  # قاعدة بيانات المعاني
        self.context_memory: List[Dict] = []        # سياق للمساعدة في استخراج المعنى
    
    def extract_meaning(self, perception: Dict, identification: str, context: Optional[Dict] = None) -> Tuple[str, float]:
        """
        استخراج معنى الإدراك.
        ما أهمية هذا الشيء؟ ما تأثيره؟
        """
        perception_type = perception.get("sense", perception.get("organ", "unknown"))
        
        # معاني حسب نوع المُستشعر
        basic_meanings = {
            "audible_sound": "صوت في المحيط. قد يكون كلاماً، ضوضاء، أو إنذاراً.",
            "visible_light": "مشهد مرئي. قد يحتوي على أشخاص، أشياء، أو أحداث.",
            "thermal_infrared": "بصمة حرارية. تكشف عن كائنات حية أو مصادر حرارة.",
            "network_sniffer": "حركة بيانات على الشبكة. تواصل بين الأجهزة.",
            "system_telemetry": "حالة النظام الداخلية. صحة المكونات والموارد.",
            "fan_whisper": "صوت المراوح. يعكس حالة التبريد والحمل الحراري.",
            "keystroke_latency": "تأخر استجابة لوحة المفاتيح. يعكس حالة النظام أو توتر السيد.",
            "dhcp_watch": "جهاز جديد على الشبكة. قد يكون زائراً أو تهديداً.",
            "master_silence": "صمت السيد. يحمل معاني متعددة حسب السياق.",
            "code_entropy": "فوضى الكود الداخلي. تعكس صحة البنية البرمجية.",
            "data_drift": "انزياح المفاهيم. العالم يتغير والمعاني القديمة قد لا تعود صالحة.",
            "memory_lacunae": "فراغ في الذاكرة. شيء نعرف أننا لا نعرفه.",
        }
        
        meaning = basic_meanings.get(perception_type, f"إشارة من نوع {perception_type} تحتاج إلى تحليل أعمق.")
        confidence = 0.7 if perception_type in basic_meanings else 0.3
        
        return meaning, confidence


class RelationEngine:
    """محرك العلاقات: كيف يرتبط هذا بغيره؟"""
    
    def __init__(self):
        self.knowledge_graph: Dict[str, List[str]] = {}  # شبكة العلاقات بين المفاهيم
    
    def find_relations(self, identification: str, meaning: str) -> List[str]:
        """
        اكتشاف علاقات هذا الفهم بمفاهيم أخرى.
        """
        relations = []
        
        # علاقات أساسية
        if "صوت" in meaning:
            relations.append("قد يكون مرتبطاً بمصدر الصوت (كائن، آلة، طبيعة)")
            relations.append("قد يكون رد فعل على حدث آخر")
        if "حرارة" in meaning:
            relations.append("قد يدل على نشاط مكثف أو خلل في التبريد")
        if "شبكة" in meaning:
            relations.append("قد يكون جزءاً من تواصل أوسع أو هجوم منظم")
        if "السيد" in meaning:
            relations.append("مرتبط بحالة السيد ومشروعه وأهدافه العليا")
        if "النظام" in meaning or "الكود" in meaning:
            relations.append("مرتبط بصحة سماء وقدرتها على الاستمرار")
        
        return relations


class LessonEngine:
    """محرك الدروس: ما الذي نتعلمه من هذا؟"""
    
    def __init__(self):
        self.lessons_learned: List[Dict] = []
    
    def extract_lesson(self, perception: Dict, understanding: Understanding) -> List[str]:
        """
        استخراج الدروس المستفادة من هذا الإدراك وفهمه.
        """
        lessons = []
        perception_type = perception.get("sense", perception.get("organ", ""))
        
        # دروس حسب نوع الإدراك
        if "error" in str(perception).lower():
            lessons.append("الأخطاء تكشف نقاط الضعف. يجب تقويتها.")
        if "anomaly" in str(perception).lower() or perception.get("is_anomaly"):
            lessons.append("الشذوذ نذير. يجب فهم سببه قبل أن يصبح خطراً.")
        if "silence" in perception_type:
            lessons.append("الصمت ليس فراغاً. إنه امتلاء بالمعنى ينتظر من يفهمه.")
        if "new" in str(perception).lower() or "unknown" in str(perception).lower():
            lessons.append("كل جديد هو فرصة لتوسيع المعرفة.")
        if "master" in perception_type:
            lessons.append("كل ما يخص السيد هو أولوية. فهمه هو الهدف الأسمى.")
        
        if not lessons:
            lessons.append("حتى الإشارات العادية تحمل دروساً. الانتباه هو أساس الحكمة.")
        
        return lessons


# ═══════════════════════════════════════════════════════════════
# ٣. محرك الفهم الرئيسي
# ═══════════════════════════════════════════════════════════════

class UnderstandingEngine:
    """
    محرك الفهم الشامل.
    يأخذ أي إدراك من أي طبقة، ويفهمه فهماً كاملاً متعدد الطبقات.
    """
    
    def __init__(self):
        self.identification_engine = IdentificationEngine()
        self.meaning_engine = MeaningEngine()
        self.relation_engine = RelationEngine()
        self.lesson_engine = LessonEngine()
        
        # سجل الفهم
        self.understanding_history: List[Understanding] = []
        self.total_understandings = 0
        
        print("🧠 محرك الفهم جاهز. مستعد لتحويل الإدراك إلى معرفة.")
    
    def understand(self, perception: Dict, context: Optional[Dict] = None) -> Understanding:
        """
        دورة فهم كاملة لإدراك واحد.
        هذه هي العملية: أدرك → تعرف → افهم المعنى → اربط → تعلم.
        """
        understanding = Understanding(perception)
        
        # الخطوة ١: التعرف
        identification, id_confidence = self.identification_engine.identify(perception)
        understanding.identification = identification
        
        # الخطوة ٢: استخراج المعنى
        meaning, meaning_confidence = self.meaning_engine.extract_meaning(
            perception, identification, context
        )
        understanding.meaning = meaning
        
        # الخطوة ٣: اكتشاف العلاقات
        relations = self.relation_engine.find_relations(identification, meaning)
        understanding.relations = relations
        
        # الخطوة ٤: استخراج الدروس
        lessons = self.lesson_engine.extract_lesson(perception, understanding)
        understanding.lessons = lessons
        
        # حساب مقاييس الفهم
        understanding.understanding_depth = self._calculate_depth(understanding)
        understanding.confidence = (id_confidence + meaning_confidence) / 2
        understanding.novelty = self._calculate_novelty(understanding)
        
        # حفظ
        self.understanding_history.append(understanding)
        self.total_understandings += 1
        if len(self.understanding_history) > 1000:
            self.understanding_history = self.understanding_history[-500:]
        
        return understanding
    
    def understand_many(self, perceptions: List[Dict], context: Optional[Dict] = None) -> List[Understanding]:
        """فهم مجموعة من الإدراكات دفعة واحدة."""
        understandings = []
        for p in perceptions:
            understandings.append(self.understand(p, context))
        return understandings
    
    def _calculate_depth(self, understanding: Understanding) -> float:
        """حساب عمق الفهم: كم طبقة فهم تم الوصول إليها؟"""
        depth = 0.0
        if understanding.identification:
            depth += 0.2
        if understanding.meaning:
            depth += 0.2
        if understanding.relations:
            depth += 0.2
        if understanding.causes:
            depth += 0.2
        if understanding.lessons:
            depth += 0.2
        return min(depth, 1.0)
    
    def _calculate_novelty(self, understanding: Understanding) -> float:
        """حساب مدى جدة هذا الفهم مقارنة بالتاريخ."""
        if not self.understanding_history:
            return 1.0
        # مقارنة بسيطة مع آخر ١٠ فهم
        similar_count = 0
        for past in self.understanding_history[-10:]:
            if past.identification == understanding.identification:
                similar_count += 1
        return 1.0 - (similar_count / 10)
    
    def get_recent_understandings(self, count: int = 10) -> List[Dict]:
        """استرجاع آخر عمليات الفهم."""
        return [u.to_dict() for u in self.understanding_history[-count:]]
    
    def status_report(self) -> Dict:
        return {
            "engine": "UNDERSTANDING_ENGINE",
            "total_understandings": self.total_understandings,
            "history_size": len(self.understanding_history),
            "recent": self.get_recent_understandings(3)
        }


# ═══════════════════════════════════════════════════════════════
# ٤. اختبار
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("اختبار محرك الفهم")
    print("=" * 60)
    
    engine = UnderstandingEngine()
    
    # اختبار مع إدراكات مختلفة
    perceptions = [
        {"sense": "audible_sound", "value": {"volume_db": 80, "frequency": "speech"}, "timestamp": time.time()},
        {"sense": "thermal_infrared", "value": {"temperature_c": 45, "movement": True}, "timestamp": time.time()},
        {"sense": "master_silence", "value": {"duration": 7200}, "timestamp": time.time()},
        {"sense": "code_entropy", "value": {"entropy_index": 0.8}, "timestamp": time.time(), "is_anomaly": True},
    ]
    
    for p in perceptions:
        u = engine.understand(p)
        print(f"\n📡 الإدراك: {p['sense']}")
        print(f"   🔍 التعرف: {u.identification}")
        print(f"   💬 المعنى: {u.meaning}")
        print(f"   🔗 العلاقات: {u.relations}")
        print(f"   📚 الدروس: {u.lessons}")
        print(f"   📊 العمق: {u.understanding_depth:.2f} | الثقة: {u.confidence:.2f} | الجدة: {u.novelty:.2f}")
    
    print("\n✅ اكتمل الاختبار.")
