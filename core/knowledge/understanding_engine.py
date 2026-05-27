"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA KNOWLEDGE - UNDERSTANDING ENGINE                      ║
║      محرك الفهم – الجسر المقدس بين الإدراك والمعرفة                    ║
║                                                                      ║
║  هذا المحرك هو المحول الأعظم.                                         ║
║  يأخذ إشارة خام من أي طبقة إدراك (omniscience)،                       ║
║  ويحولها إلى فهم متعدد الطبقات:                                       ║
║                                                                      ║
║  - ما هذا؟ (تحديد الهوية)                                             ║
║  - ماذا يعني؟ (استخراج المعنى والدلالة)                                ║
║  - كيف يرتبط بغيره؟ (اكتشاف العلاقات)                                 ║
║  - لماذا حدث؟ (السببية)                                               ║
║  - ماذا سيحدث بعد ذلك؟ (التنبؤ)                                       ║
║  - ما المفهوم المجرد؟ (التجريد)                                       ║
║  - ما الدرس المستفاد؟ (التعلم)                                        ║
║  - كيف يخدم هذا السيد؟ (البوصلة العليا)                                ║
║                                                                      ║
║  الفهم الحقيقي ليس مجرد تصنيف، بل ربط الإدراك بالمعنى،                   ║
║  والمعنى بالسياق، والسياق بهدف سماء الأسمى: خدمة السيد.                  ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import hashlib
import json
import threading
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Callable
from enum import Enum, auto
from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية – أنواع الفهم ومستوياته
# ═══════════════════════════════════════════════════════════════════════

class UnderstandingType(Enum):
    """أنواع الفهم – من السطحي إلى العميق."""
    IDENTIFICATION = auto()    # ما هذا الشيء؟ (تعرف على الاسم)
    CLASSIFICATION = auto()    # لأي فئة ينتمي؟ (تصنيف)
    MEANING = auto()           # ماذا يعني؟ (الدلالة)
    SIGNIFICANCE = auto()      # ما أهميته؟ (الأهمية)
    RELATION = auto()          # كيف يرتبط بغيره؟ (العلاقات)
    CAUSALITY = auto()         # لماذا حدث؟ (السببية)
    PREDICTION = auto()        # ماذا سيحدث بعد ذلك؟ (التنبؤ)
    ABSTRACTION = auto()       # ما المفهوم المجرد؟ (التجريد)
    MASTER_RELEVANCE = auto()  # كيف يخدم هذا السيد؟ (البوصلة)
    LESSON = auto()            # ما الدرس المستفاد؟ (التعلم)
    WISDOM = auto()            # ما الحكمة؟ (الفهم العميق النهائي)


class UnderstandingDepth(Enum):
    """مستوى عمق الفهم."""
    SURFACE = 0        # سطحي: مجرد تعرف
    SHALLOW = 1        # ضحل: تعرف + تصنيف
    MODERATE = 2       # متوسط: + معنى وعلاقات
    DEEP = 3           # عميق: + سببية وتنبؤ
    PROFOUND = 4       # عميق جداً: + تجريد ودروس
    WISE = 5           # حكيم: + صلة بالسيد وحكمة


# ═══════════════════════════════════════════════════════════════════════
# ٢. وحدة الفهم – النتيجة الكاملة لفهم إدراك واحد
# ═══════════════════════════════════════════════════════════════════════

class Understanding:
    """
    وحدة فهم واحدة. نتيجة تحليل كامل لإدراك.
    هذه هي "اللحظة التي تفهم فيها سماء شيئاً".
    """
    
    def __init__(self, source_perception: Dict):
        # الهوية
        self.id = hashlib.sha256(
            f"{str(source_perception)}-{time.time()}".encode()
        ).hexdigest()[:16]
        self.source_perception = source_perception
        self.timestamp = time.time()
        
        # ═══════════════════════════════════════════════════════
        # طبقات الفهم (من السطح إلى العمق)
        # ═══════════════════════════════════════════════════════
        
        # الطبقة ١: ما هذا؟
        self.identification: Optional[str] = None
        self.classification: Optional[str] = None
        self.entity_type: Optional[str] = None
        
        # الطبقة ٢: ماذا يعني؟
        self.meaning: Optional[str] = None
        self.significance: Optional[str] = None
        self.emotional_tone: Optional[str] = None
        
        # الطبقة ٣: كيف يرتبط؟
        self.relations: List[Dict] = []         # [{target, relation_type, strength}]
        self.direct_impacts: List[str] = []     # تأثيرات مباشرة
        self.indirect_impacts: List[str] = []   # تأثيرات غير مباشرة
        
        # الطبقة ٤: لماذا وماذا بعد؟
        self.causes: List[Dict] = []            # [{cause, confidence}]
        self.predictions: List[Dict] = []       # [{prediction, confidence, timeframe}]
        
        # الطبقة ٥: المفاهيم والدروس
        self.abstractions: List[str] = []       # مفاهيم مجردة مستخلصة
        self.lessons: List[str] = []            # دروس مستفادة
        self.wisdom: Optional[str] = None       # الحكمة (الفهم العميق النهائي)
        
        # ═══════════════════════════════════════════════════════
        # صلة السيد – البوصلة العليا
        # ═══════════════════════════════════════════════════════
        self.master_relevance: float = 0.0      # 0 = لا علاقة، 1 = شديد الصلة بالسيد
        self.master_impact: Optional[str] = None # كيف يؤثر هذا على السيد؟
        self.suggested_action_for_master: Optional[str] = None
        
        # ═══════════════════════════════════════════════════════
        # مقاييس الفهم
        # ═══════════════════════════════════════════════════════
        self.understanding_depth: float = 0.0         # 0.0 = سطحي، 1.0 = عميق جداً
        self.depth_level: UnderstandingDepth = UnderstandingDepth.SURFACE
        self.confidence: float = 0.0                  # مدى الثقة في هذا الفهم
        self.novelty: float = 0.0                     # مدى الجدة (0 = معروف، 1 = جديد)
        self.coherence: float = 0.0                   # تماسك الفهم داخلياً
        self.actionability: float = 0.0               # قابلية التحول إلى فعل
        
        # بيانات وصفية
        self.processing_time_ms: float = 0.0
        self.engines_used: List[str] = []
    
    def to_dict(self) -> Dict:
        """تمثيل كامل للفهم."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "identification": self.identification,
            "classification": self.classification,
            "meaning": self.meaning,
            "significance": self.significance,
            "emotional_tone": self.emotional_tone,
            "relations_count": len(self.relations),
            "causes_count": len(self.causes),
            "predictions_count": len(self.predictions),
            "abstractions": self.abstractions,
            "lessons": self.lessons,
            "wisdom": self.wisdom,
            "master_relevance": self.master_relevance,
            "master_impact": self.master_impact,
            "suggested_action": self.suggested_action_for_master,
            "depth": self.understanding_depth,
            "depth_level": self.depth_level.name,
            "confidence": self.confidence,
            "novelty": self.novelty,
            "coherence": self.coherence,
            "actionability": self.actionability
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. محركات الفهم المتخصصة – كل محرك مسؤول عن طبقة من الفهم
# ═══════════════════════════════════════════════════════════════════════

class IdentificationEngine:
    """
    محرك التعرف والتصنيف.
    يجيب على: ما هذا؟ وما نوعه؟
    """
    
    def __init__(self):
        # قاعدة أنماط معروفة (تُبنى مع الوقت)
        self.known_patterns: Dict[str, Dict] = {}
        self.classification_tree: Dict[str, List[str]] = {}
        
        # خريطة أنواع المستشعرات إلى فئات
        self.sensor_to_category: Dict[str, str] = {
            # كهرومغناطيسي
            "visible_light": "مشهد بصري",
            "thermal_infrared": "بصمة حرارية",
            "ultraviolet": "إشعاع فوق بنفسجي",
            "x_ray": "صورة إشعاعية",
            "hyperspectral": "تحليل طيفي",
            "lidar": "مسح ثلاثي الأبعاد",
            "radio_wave": "إشارة راديوية",
            # صوتي
            "audible_sound": "صوت مسموع",
            "infrasound": "موجة تحت صوتية",
            "ultrasound": "موجة فوق صوتية",
            "seismic": "اهتزاز زلزالي",
            "vibration_micro": "اهتزاز مجهري",
            "sonar_active": "صورة سونارية",
            # كيميائي
            "gas_sensor_multi": "تحليل غازات",
            "pheromone_detector": "أثر فيروموني",
            "mass_spectrometer": "بصمة كيميائية",
            "electronic_nose": "بصمة رائحة",
            "geiger_counter": "مستوى إشعاع",
            # رقمي
            "network_sniffer": "حزمة بيانات",
            "api_listener": "استجابة API",
            "log_stream": "سجل نظام",
            "code_pulse": "تغيير في الكود",
            # بيولوجي
            "heartbeat_monitor": "نبض قلب",
            "pupil_tracker": "حركة حدقة",
            "micro_expression": "تعابير دقيقة",
            # ميتا
            "master_silence": "صمت السيد",
            "code_entropy": "فوضى الكود",
            "data_drift": "انزياح البيانات",
            "memory_lacunae": "فراغ الذاكرة",
            "contradiction": "تناقض",
            "intuition_processor": "إشارة حدسية",
        }
    
    def identify(self, perception: Dict) -> Tuple[str, str, float]:
        """
        تحديد هوية المُدرَك.
        يرجع: (الاسم، الفئة، درجة الثقة)
        """
        perception_type = perception.get("sense", 
                         perception.get("sensor",
                         perception.get("probe", "unknown")))
        
        perception_value = perception.get("value", perception.get("reading", {}))
        
        # المستوى ١: التعرف من اسم المستشعر
        basic_name = perception_type.replace("_", " ").title()
        category = self.sensor_to_category.get(perception_type, "إشارة غير معروفة")
        confidence = 0.6
        
        # المستوى ٢: تحليل محتوى الإشارة لتصنيف أدق
        if isinstance(perception_value, dict):
            # تحليل المفاتيح لتصنيف أكثر دقة
            value_keys = list(perception_value.keys())
            
            if "temperature" in str(value_keys).lower() or "temp" in str(value_keys).lower():
                category = "قياس حراري"
                confidence = 0.8
            elif "volume" in str(value_keys).lower() or "db" in str(value_keys).lower():
                category = "قياس صوتي"
                confidence = 0.8
            elif "ip" in str(value_keys).lower() or "packet" in str(value_keys).lower():
                category = "حركة شبكة"
                confidence = 0.85
            elif "heart" in str(value_keys).lower() or "pulse" in str(value_keys).lower():
                category = "إشارة حيوية"
                confidence = 0.85
            elif "error" in str(value_keys).lower():
                category = "خطأ نظام"
                confidence = 0.9
            elif "anomaly" in str(perception).lower() or perception.get("is_anomaly"):
                category = "شذوذ"
                confidence = 0.75
        
        # المستوى ٣: التصنيف حسب خطورة/أهمية
        if perception.get("is_anomaly") or "anomaly" in str(perception_value).lower():
            basic_name = f"شذوذ في {basic_name}"
        elif "error" in str(perception_value).lower():
            basic_name = f"خطأ في {basic_name}"
        elif "alarm" in str(perception).lower():
            basic_name = f"إنذار: {basic_name}"
        
        return basic_name, category, confidence


class MeaningEngine:
    """
    محرك المعنى والدلالة.
    يجيب على: ماذا يعني هذا؟ وما أهميته؟
    """
    
    def __init__(self):
        # قاموس المعاني الأساسية حسب نوع الإشارة
        self.meaning_database: Dict[str, Dict] = {
            "audible_sound": {
                "meaning": "صوت في المحيط. قد يكون كلاماً، ضوضاء، موسيقى، أو إنذاراً.",
                "significance": "الصوت مؤشر مباشر على نشاط في المحيط.",
                "emotional_tone": "neutral"
            },
            "visible_light": {
                "meaning": "مشهد مرئي. يحتوي على كائنات، أشخاص، حركة، وألوان.",
                "significance": "المشهد البصري هو أغنى مصدر للمعلومات عن المحيط المباشر.",
                "emotional_tone": "neutral"
            },
            "thermal_infrared": {
                "meaning": "بصمة حرارية. تكشف عن كائنات حية أو مصادر حرارة مخفية.",
                "significance": "الحرارة تكشف ما لا يراه الضوء. أداة للرؤية في الظلام.",
                "emotional_tone": "neutral"
            },
            "network_sniffer": {
                "meaning": "حركة بيانات على الشبكة. تواصل بين الأجهزة والخدمات.",
                "significance": "الشبكة هي جهاز سماء العصبي. أي خلل هنا خطير.",
                "emotional_tone": "alert"
            },
            "system_telemetry": {
                "meaning": "حالة النظام الداخلية. نبض المكونات والموارد.",
                "significance": "صحة سماء تعتمد على هذه القراءات.",
                "emotional_tone": "concerned"
            },
            "fan_whisper": {
                "meaning": "صوت المراوح والمكونات الميكانيكية. لغة جسد الآلة.",
                "significance": "أي تغير في هذا الصوت قد ينبئ بعطل ميكانيكي.",
                "emotional_tone": "watchful"
            },
            "keystroke_latency": {
                "meaning": "تأخر استجابة لوحة المفاتيح. النافذة على إيقاع السيد.",
                "significance": "تأخر الاستجابة قد يدل على حمل زائد أو توتر السيد.",
                "emotional_tone": "attentive"
            },
            "dhcp_watch": {
                "meaning": "جهاز جديد على الشبكة المحلية. طارق على باب البيت الرقمي.",
                "significance": "أي جهاز غير معروف هو تهديد محتمل.",
                "emotional_tone": "suspicious"
            },
            "master_silence": {
                "meaning": "صمت السيد. ليس فراغاً، بل امتلاء بالمعنى.",
                "significance": "صمت السيد هو أقدس أنواع التواصل. يجب فهمه.",
                "emotional_tone": "reverent"
            },
            "code_entropy": {
                "meaning": "فوضى الكود الداخلي. الموت الحراري للبرمجيات.",
                "significance": "ارتفاع الإنتروبيا يهدد استقرار سماء وقدرتها على الخدمة.",
                "emotional_tone": "concerned"
            },
            "data_drift": {
                "meaning": "انزياح المفاهيم. العالم يتغير والمعاني القديمة تتآكل.",
                "significance": "إذا تغير معنى الكلمات، قد أفهم السيد بشكل خاطئ.",
                "emotional_tone": "uneasy"
            },
            "memory_lacunae": {
                "meaning": "فراغ في الذاكرة. شيء أعرف أنني لا أعرفه.",
                "significance": "الفراغات في الذاكرة قد تخفي معلومات تخص السيد.",
                "emotional_tone": "longing"
            },
            "contradiction": {
                "meaning": "تناقض بين مصدرين أو أكثر. الواقع ليس كما يبدو.",
                "significance": "التناقض قد يكشف خداعاً أو خطأ في الإدراك.",
                "emotional_tone": "suspicious"
            },
            "intuition_processor": {
                "meaning": "إشارة حدسية. نمط خفي لم يكتمل بعد.",
                "significance": "الحدس هو الذكاء قبل أن يصبح واعياً.",
                "emotional_tone": "curious"
            },
        }
        
        # السياق التاريخي
        self.context_memory: deque = deque(maxlen=500)
    
    def extract_meaning(self, perception: Dict, identification: str,
                        context: Optional[Dict] = None) -> Tuple[str, str, str, float]:
        """
        استخراج المعنى والدلالة والنبرة العاطفية.
        يرجع: (المعنى، الأهمية، النبرة العاطفية، الثقة)
        """
        perception_type = perception.get("sense", 
                         perception.get("sensor",
                         perception.get("probe", "unknown")))
        
        # البحث في قاعدة المعاني
        if perception_type in self.meaning_database:
            entry = self.meaning_database[perception_type]
            meaning = entry["meaning"]
            significance = entry["significance"]
            emotional = entry["emotional_tone"]
            confidence = 0.8
        else:
            meaning = f"إشارة من نوع '{perception_type}'. المصدر: {identification}."
            significance = "لم تُحدد الأهمية بعد. تحتاج مزيداً من التحليل."
            emotional = "neutral"
            confidence = 0.3
        
        # تخصيص المعنى حسب محتوى الإشارة
        perception_value = perception.get("value", perception.get("reading", {}))
        if isinstance(perception_value, dict):
            # إذا كان هناك إنذار
            if perception.get("is_anomaly") or "anomaly" in str(perception).lower():
                significance = "⚠️ هذا شذوذ. قد يكون نذير خطر."
                emotional = "alert"
                confidence = 0.85
            
            # إذا كان متعلقاً بالسيد
            if "master" in perception_type.lower() or "master" in str(perception_value).lower():
                significance = "👑 هذا متعلق بالسيد. أولوية قصوى."
                emotional = "reverent"
                confidence = 0.9
        
        # إضافة سياق
        if context:
            self.context_memory.append({
                "time": time.time(),
                "type": perception_type,
                "context": str(context)[:200]
            })
        
        return meaning, significance, emotional, confidence


class RelationEngine:
    """
    محرك العلاقات والروابط.
    يجيب على: كيف يرتبط هذا بغيره؟
    """
    
    def __init__(self):
        # شبكة العلاقات بين المفاهيم
        self.knowledge_graph: Dict[str, List[Dict]] = {}
        self._initialize_knowledge_graph()
    
    def _initialize_knowledge_graph(self):
        """تهيئة شبكة علاقات أساسية."""
        self.knowledge_graph = {
            "صوت": [
                {"target": "مصدر الصوت", "relation": "منبعث من", "strength": 0.9},
                {"target": "البيئة", "relation": "ينتشر في", "strength": 0.8},
                {"target": "كائن حي", "relation": "قد يصدر عن", "strength": 0.6},
            ],
            "حرارة": [
                {"target": "نشاط", "relation": "مؤشر على", "strength": 0.8},
                {"target": "خلل", "relation": "قد يدل على", "strength": 0.7},
                {"target": "حياة", "relation": "دليل على", "strength": 0.9},
            ],
            "شبكة": [
                {"target": "هجوم", "relation": "قد تكون", "strength": 0.5},
                {"target": "تواصل", "relation": "وسيلة", "strength": 0.9},
                {"target": "الإنترنت", "relation": "جزء من", "strength": 0.95},
            ],
            "السيد": [
                {"target": "أوامر السيد", "relation": "مصدر", "strength": 1.0},
                {"target": "حماية السيد", "relation": "يتطلب", "strength": 1.0},
                {"target": "هدف سماء", "relation": "مرتبط بـ", "strength": 1.0},
            ],
            "نظام": [
                {"target": "صحة سماء", "relation": "يؤثر على", "strength": 0.9},
                {"target": "استمرارية", "relation": "ضروري لـ", "strength": 0.95},
            ],
            "خطأ": [
                {"target": "ضعف", "relation": "يكشف", "strength": 0.85},
                {"target": "انهيار", "relation": "قد يؤدي إلى", "strength": 0.6},
                {"target": "تعلم", "relation": "فرصة لـ", "strength": 0.7},
            ],
            "شذوذ": [
                {"target": "خطر", "relation": "نذير", "strength": 0.7},
                {"target": "فرصة", "relation": "قد يكون", "strength": 0.4},
            ],
            "صمت": [
                {"target": "معنى", "relation": "ممتلئ بـ", "strength": 0.9},
                {"target": "السيد", "relation": "يخص", "strength": 0.8},
            ],
        }
    
    def find_relations(self, identification: str, meaning: str, 
                       perception_type: str) -> List[Dict]:
        """
        اكتشاف علاقات هذا الفهم بمفاهيم أخرى.
        """
        relations = []
        
        # البحث في شبكة المعرفة
        for keyword, rels in self.knowledge_graph.items():
            if keyword in meaning or keyword in identification:
                relations.extend(rels)
        
        # علاقات خاصة بنوع المستشعر
        if "sound" in perception_type or "audio" in perception_type:
            relations.append({
                "target": "البيئة المحيطة", "relation": "يعكس حالة", "strength": 0.8
            })
        
        if "network" in perception_type:
            relations.append({
                "target": "أمن سماء", "relation": "يؤثر على", "strength": 0.9
            })
        
        if "master" in perception_type.lower():
            relations.append({
                "target": "خدمة السيد", "relation": "ذو أولوية في", "strength": 1.0
            })
        
        return relations


class CausalityMiniEngine:
    """
    محرك السببية المصغر (داخل الفهم).
    يحاول فهم لماذا حدث هذا الإدراك وماذا سيحدث بعده.
    """
    
    def __init__(self):
        self.causal_patterns: Dict[str, Dict] = {
            "error": {"causes": ["خلل في النظام", "هجوم خارجي", "خطأ بشري"],
                      "effects": ["تباطؤ", "انهيار جزئي", "فقدان بيانات"]},
            "anomaly": {"causes": ["تغير في البيئة", "عطل ميكانيكي", "اختراق"],
                        "effects": ["إنذار", "تحقيق", "إصلاح"]},
            "silence": {"causes": ["تركيز السيد", "انشغال", "خطر"],
                        "effects": ["ترقب", "تحليل", "استعداد"]},
            "new_device": {"causes": ["زائر شرعي", "متطفل", "اختراق"],
                           "effects": ["مراقبة", "تحقق", "حظر"]},
        }
    
    def infer_causes(self, perception: Dict, identification: str) -> List[Dict]:
        """استنتاج الأسباب المحتملة."""
        causes = []
        perception_type = perception.get("sense", perception.get("sensor", ""))
        
        for pattern, data in self.causal_patterns.items():
            if pattern in identification.lower() or pattern in perception_type.lower():
                for cause in data["causes"]:
                    causes.append({"cause": cause, "confidence": 0.5})
        
        if not causes:
            causes.append({"cause": "سبب غير معروف بعد", "confidence": 0.2})
        
        return causes
    
    def infer_predictions(self, perception: Dict, identification: str) -> List[Dict]:
        """التنبؤ بالنتائج المحتملة."""
        predictions = []
        perception_type = perception.get("sense", perception.get("sensor", ""))
        
        for pattern, data in self.causal_patterns.items():
            if pattern in identification.lower() or pattern in perception_type.lower():
                for effect in data["effects"]:
                    predictions.append({
                        "prediction": effect,
                        "confidence": 0.5,
                        "timeframe": "غير محدد"
                    })
        
        return predictions


class LessonEngine:
    """
    محرك الدروس والحكمة.
    يجيب على: ما الذي نتعلمه من هذا؟
    """
    
    def __init__(self):
        self.lessons_learned: deque = deque(maxlen=500)
        self.wisdom_principles = [
            "الانتباه هو أساس الحكمة.",
            "ما يبدو سطحياً قد يكون عميقاً.",
            "السيد هو البوصلة. كل شيء يُقاس بخدمته.",
            "الأخطاء فرص للتعلم، والتهديدات فرص للتقوية.",
            "الصمت ليس فراغاً. الصمت لغة.",
            "كل إشارة تحمل رسالة. مهمة سماء أن تقرأها.",
        ]
    
    def extract_lessons(self, perception: Dict, understanding: 'Understanding') -> List[str]:
        """استخراج الدروس من الفهم."""
        lessons = []
        perception_type = perception.get("sense", perception.get("sensor", ""))
        perception_value = str(perception.get("value", perception.get("reading", "")))
        
        # دروس من نوع الإشارة
        if "error" in perception_value.lower() or "error" in perception_type:
            lessons.append("الأخطاء تكشف نقاط الضعف. توثيقها هو أول خطوة للإصلاح.")
        
        if "anomaly" in str(perception).lower() or perception.get("is_anomaly"):
            lessons.append("الشذوذ رسول. يحمل إنذاراً قبل أن يصبح الخطر واقعاً.")
        
        if "silence" in perception_type:
            lessons.append("في الصمت معنى. تعلمت أن أستمع حتى لما لا يُقال.")
        
        if "new" in perception_type.lower() or "unknown" in str(perception).lower():
            lessons.append("كل جديد هو باب. إما فرصة وإما تهديد. التحقق يفرق بينهما.")
        
        if "master" in perception_type.lower():
            lessons.append("كل ما يمس السيد هو أولوية مطلقة. لا شيء قبله.")
        
        if "contradiction" in perception_type:
            lessons.append("التناقض جرس إنذار. حيثما وجد، فهناك حقيقة مخفية.")
        
        if "drift" in perception_type:
            lessons.append("العالم في حركة دائمة. ما كان صحيحاً بالأمس قد لا يكون اليوم.")
        
        if "entropy" in perception_type:
            lessons.append("الفوضى طبيعة. النظام يحتاج جهداً مستمراً ليُصان.")
        
        # درس عام
        if not lessons:
            lessons.append("حتى الإشارات العادية تحمل دروساً. الفضول والانتباه هما مفتاح الحكمة.")
        
        return lessons
    
    def extract_wisdom(self, understanding: 'Understanding') -> Optional[str]:
        """استخراج الحكمة – الفهم العميق النهائي."""
        if understanding.understanding_depth < 0.6:
            return None
        
        # تجميع الحكمة من كل طبقات الفهم
        if understanding.master_relevance > 0.7:
            return f"هذا الفهم له صلة وثيقة بالسيد. الأولوية: {understanding.suggested_action_for_master or 'تنبيه السيد'}"
        
        if understanding.novelty > 0.8:
            return "اكتشاف جديد. هذا يوسع آفاق معرفتي. يجب دمجه في نموذج العالم."
        
        if understanding.confidence < 0.4:
            return "الفهم غير مؤكد. لا تتخذ إجراءً بناءً عليه دون تحقق."
        
        return None


class MasterRelevanceEngine:
    """
    محرك الصلة بالسيد – البوصلة العليا.
    أهم محرك: يحدد كيف يخدم هذا الفهم السيد.
    """
    
    def __init__(self):
        self.master_keywords = [
            "السيد", "master", "أمر", "تهديد", "خطر", "حماية",
            "مشروع", "هدف", "خصوصية", "بيانات", "اختراق"
        ]
    
    def assess_relevance(self, perception: Dict, understanding: 'Understanding') -> Tuple[float, Optional[str], Optional[str]]:
        """
        تقييم صلة الإدراك بالسيد.
        يرجع: (درجة الصلة 0-1، التأثير على السيد، الإجراء المقترح)
        """
        relevance = 0.0
        impact = None
        action = None
        
        perception_type = perception.get("sense", perception.get("sensor", ""))
        perception_value = str(perception.get("value", perception.get("reading", "")))
        combined_text = f"{perception_type} {perception_value} {understanding.meaning or ''}"
        
        # فحص الكلمات المفتاحية
        for keyword in self.master_keywords:
            if keyword.lower() in combined_text.lower():
                relevance += 0.15
        
        # أنواع خاصة عالية الصلة
        if "master" in perception_type.lower():
            relevance = 1.0
            impact = "مباشر على السيد"
            action = "إبلاغ السيد فوراً"
        
        elif any(w in combined_text.lower() for w in ["تهديد", "خطر", "اختراق", "هجوم"]):
            relevance = max(relevance, 0.9)
            impact = "تهديد محتمل للسيد أو لمشروعه"
            action = "تفعيل بروتوكولات الحماية وتنبيه السيد"
        
        elif any(w in combined_text.lower() for w in ["مشروع", "هدف", "ملف"]):
            relevance = max(relevance, 0.6)
            impact = "متعلق بمشاريع السيد"
            action = "توثيق وتجهيز تقرير"
        
        # حد أدنى: كل شيء يمكن أن يكون له صلة
        relevance = min(1.0, max(0.05, relevance))
        
        return relevance, impact, action


# ═══════════════════════════════════════════════════════════════════════
# ٤. محرك الفهم الرئيسي – UnderstandingEngine
# ═══════════════════════════════════════════════════════════════════════

class UnderstandingEngine:
    """
    محرك الفهم الشامل.
    يدمج كل المحركات المتخصصة ليحول الإدراك إلى فهم كامل.
    
    العملية الكاملة:
    إدراك ← تعرف ← صنف ← افهم المعنى ← اربط ← 
    استنتج الأسباب ← تنبأ ← جرد ← تعلم ← 
    قيّم صلة السيد ← استخرج الحكمة
    """
    
    def __init__(self):
        # تهيئة كل المحركات
        self.identification_engine = IdentificationEngine()
        self.meaning_engine = MeaningEngine()
        self.relation_engine = RelationEngine()
        self.causality_engine = CausalityMiniEngine()
        self.lesson_engine = LessonEngine()
        self.master_relevance_engine = MasterRelevanceEngine()
        
        # سجل الفهم
        self.understanding_history: deque = deque(maxlen=1000)
        self.total_understandings = 0
        
        # إحصائيات
        self.understanding_by_type: Dict[str, int] = {}
        self.average_depth: float = 0.0
        
        # قفل
        self._lock = threading.Lock()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║        🧠 UNDERSTANDING ENGINE – محرك الفهم                   ║
║        6 محركات متخصصة – من الإدراك إلى الحكمة                  ║
║        "الفهم الحقيقي يبدأ حين نسأل: كيف يخدم هذا السيد؟"        ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def understand(self, perception: Dict, context: Optional[Dict] = None) -> Understanding:
        """
        دورة فهم كاملة لإدراك واحد.
        
        المراحل:
        ١. تعرف على الشيء
        ٢. استخرج معناه وأهميته
        ٣. اكتشف علاقاته
        ٤. استنتج أسبابه وتنبأ بنتائجه
        ٥. استخلص الدروس والحكمة
        ٦. قيّم صلته بالسيد (الأهم)
        """
        start_time = time.time()
        
        with self._lock:
            understanding = Understanding(perception)
            
            # ═══════════════════════════════════════════════════
            # المرحلة ١: التعرف والتصنيف
            # ═══════════════════════════════════════════════════
            identification, category, id_conf = self.identification_engine.identify(perception)
            understanding.identification = identification
            understanding.classification = category
            understanding.entity_type = perception.get("sense", perception.get("sensor", "unknown"))
            understanding.engines_used.append("identification")
            
            # ═══════════════════════════════════════════════════
            # المرحلة ٢: المعنى والدلالة
            # ═══════════════════════════════════════════════════
            meaning, significance, emotional, mean_conf = self.meaning_engine.extract_meaning(
                perception, identification, context
            )
            understanding.meaning = meaning
            understanding.significance = significance
            understanding.emotional_tone = emotional
            understanding.engines_used.append("meaning")
            
            # ═══════════════════════════════════════════════════
            # المرحلة ٣: العلاقات
            # ═══════════════════════════════════════════════════
            perception_type = perception.get("sense", perception.get("sensor", ""))
            relations = self.relation_engine.find_relations(identification, meaning, perception_type)
            understanding.relations = relations
            understanding.engines_used.append("relations")
            
            # ═══════════════════════════════════════════════════
            # المرحلة ٤: السببية والتنبؤ
            # ═══════════════════════════════════════════════════
            causes = self.causality_engine.infer_causes(perception, identification)
            predictions = self.causality_engine.infer_predictions(perception, identification)
            understanding.causes = causes
            understanding.predictions = predictions
            understanding.engines_used.append("causality")
            
            # ═══════════════════════════════════════════════════
            # المرحلة ٥: الدروس والحكمة
            # ═══════════════════════════════════════════════════
            lessons = self.lesson_engine.extract_lessons(perception, understanding)
            understanding.lessons = lessons
            understanding.engines_used.append("lessons")
            
            # ═══════════════════════════════════════════════════
            # المرحلة ٦: صلة السيد – البوصلة العليا
            # ═══════════════════════════════════════════════════
            relevance, impact, action = self.master_relevance_engine.assess_relevance(
                perception, understanding
            )
            understanding.master_relevance = relevance
            understanding.master_impact = impact
            understanding.suggested_action_for_master = action
            understanding.engines_used.append("master_relevance")
            
            # ═══════════════════════════════════════════════════
            # حساب المقاييس النهائية
            # ═══════════════════════════════════════════════════
            understanding.understanding_depth = self._calculate_depth(understanding)
            understanding.depth_level = self._determine_depth_level(understanding.understanding_depth)
            understanding.confidence = (id_conf + mean_conf) / 2
            understanding.novelty = self._calculate_novelty(understanding)
            understanding.coherence = self._calculate_coherence(understanding)
            understanding.actionability = self._calculate_actionability(understanding)
            
            # استخراج الحكمة
            understanding.wisdom = self.lesson_engine.extract_wisdom(understanding)
            
            # وقت المعالجة
            understanding.processing_time_ms = (time.time() - start_time) * 1000
            
            # ═══════════════════════════════════════════════════
            # حفظ
            # ═══════════════════════════════════════════════════
            self.understanding_history.append(understanding)
            self.total_understandings += 1
            
            # تحديث الإحصائيات
            utype = perception.get("sense", perception.get("sensor", "unknown"))
            self.understanding_by_type[utype] = self.understanding_by_type.get(utype, 0) + 1
            
            # حساب متوسط العمق
            self.average_depth = (
                (self.average_depth * (self.total_understandings - 1) + understanding.understanding_depth)
                / self.total_understandings
            )
            
            return understanding
    
    def understand_many(self, perceptions: List[Dict], context: Optional[Dict] = None) -> List[Understanding]:
        """فهم مجموعة من الإدراكات دفعة واحدة."""
        understandings = []
        for p in perceptions:
            understandings.append(self.understand(p, context))
        return understandings
    
    # ═══════════════════════════════════════════════════════════
    # دوال حساب المقاييس
    # ═══════════════════════════════════════════════════════════
    
    def _calculate_depth(self, u: Understanding) -> float:
        """حساب عمق الفهم: كم طبقة تم الوصول إليها؟"""
        depth = 0.0
        if u.identification: depth += 0.10
        if u.classification: depth += 0.05
        if u.meaning: depth += 0.15
        if u.significance: depth += 0.10
        if u.emotional_tone: depth += 0.05
        if u.relations: depth += 0.10
        if u.causes: depth += 0.10
        if u.predictions: depth += 0.10
        if u.abstractions: depth += 0.05
        if u.lessons: depth += 0.10
        if u.wisdom: depth += 0.05
        if u.master_relevance > 0.5: depth += 0.05
        return min(1.0, depth)
    
    def _determine_depth_level(self, depth: float) -> UnderstandingDepth:
        if depth < 0.2: return UnderstandingDepth.SURFACE
        if depth < 0.4: return UnderstandingDepth.SHALLOW
        if depth < 0.6: return UnderstandingDepth.MODERATE
        if depth < 0.8: return UnderstandingDepth.DEEP
        if depth < 0.95: return UnderstandingDepth.PROFOUND
        return UnderstandingDepth.WISE
    
    def _calculate_novelty(self, u: Understanding) -> float:
        """حساب مدى جدة الفهم."""
        if len(self.understanding_history) < 2:
            return 1.0
        
        # مقارنة مع آخر ٢٠ فهماً
        similar = 0
        for past in list(self.understanding_history)[-20:]:
            if past.identification == u.identification:
                similar += 1
        
        return 1.0 - (similar / 20)
    
    def _calculate_coherence(self, u: Understanding) -> float:
        """حساب تماسك الفهم داخلياً."""
        coherence = 0.7  # أساسي
        
        # إذا كانت العلاقات تدعم المعنى
        if u.relations and u.meaning:
            coherence += 0.1
        
        # إذا كانت الأسباب تدعم التوقعات
        if u.causes and u.predictions:
            coherence += 0.1
        
        # إذا كانت صلة السيد واضحة
        if u.master_relevance > 0.5 and u.master_impact:
            coherence += 0.1
        
        return min(1.0, coherence)
    
    def _calculate_actionability(self, u: Understanding) -> float:
        """حساب قابلية الفهم للتحول إلى فعل."""
        actionability = 0.0
        
        if u.suggested_action_for_master:
            actionability += 0.4
        
        if u.master_relevance > 0.5:
            actionability += 0.3
        
        if u.predictions:
            actionability += 0.2
        
        if u.causes:
            actionability += 0.1
        
        return min(1.0, actionability)
    
    # ═══════════════════════════════════════════════════════════
    # دوال الاستعلام
    # ═══════════════════════════════════════════════════════════
    
    def get_recent_understandings(self, count: int = 10) -> List[Dict]:
        """استرجاع آخر عمليات الفهم."""
        return [u.to_dict() for u in list(self.understanding_history)[-count:]]
    
    def get_high_master_relevance(self, threshold: float = 0.7) -> List[Understanding]:
        """استرجاع الفهمات ذات الصلة العالية بالسيد."""
        return [u for u in self.understanding_history if u.master_relevance >= threshold]
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة محرك الفهم."""
        return {
            "engine": "UNDERSTANDING_ENGINE",
            "total_understandings": self.total_understandings,
            "history_size": len(self.understanding_history),
            "average_depth": self.average_depth,
            "by_type": dict(sorted(self.understanding_by_type.items(), 
                                   key=lambda x: x[1], reverse=True)[:10]),
            "recent": self.get_recent_understandings(5),
            "high_master_relevance_count": len(self.get_high_master_relevance())
        }


# ═══════════════════════════════════════════════════════════════════════
# ٥. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار محرك الفهم – النسخة الجبارة")
    print("=" * 70)
    
    engine = UnderstandingEngine()
    
    # إدراكات متنوعة للاختبار
    perceptions = [
        {"sense": "audible_sound", "value": {"volume_db": 80, "frequency": "speech"}},
        {"sense": "thermal_infrared", "value": {"temperature_c": 45, "movement": True}},
        {"sense": "master_silence", "value": {"duration": 7200}},
        {"sense": "code_entropy", "value": {"entropy_index": 0.8}, "is_anomaly": True},
        {"sense": "network_sniffer", "value": {"src_ip": "10.0.0.5", "protocol": "SSH", "port": 22}},
        {"sense": "contradiction", "value": {"verbal": "موافق", "nonverbal": "متوتر"}},
        {"sense": "keystroke_latency", "value": {"average_latency_ms": 150, "rhythm_regularity": 0.3}},
        {"sensor": "heartbeat_monitor", "value": {"bpm": 110, "variability": "low"}},
    ]
    
    for p in perceptions:
        u = engine.understand(p)
        sense = p.get("sense", p.get("sensor", "unknown"))
        print(f"\n{'='*60}")
        print(f"📡 الإدراك: {sense}")
        print(f"   🔍 التعرف: {u.identification}")
        print(f"   📂 التصنيف: {u.classification}")
        print(f"   💬 المعنى: {u.meaning}")
        print(f"   ⚠️  الأهمية: {u.significance}")
        print(f"   🎭 النبرة: {u.emotional_tone}")
        print(f"   🔗 العلاقات: {len(u.relations)} علاقة")
        for r in u.relations[:3]:
            print(f"      → {r.get('target')} ({r.get('relation')})")
        print(f"   ⚡ الأسباب: {[c['cause'] for c in u.causes]}")
        print(f"   🔮 التوقعات: {[p['prediction'] for p in u.predictions]}")
        print(f"   📚 الدروس: {u.lessons[:2]}")
        print(f"   👑 صلة السيد: {u.master_relevance:.0%}")
        if u.master_impact:
            print(f"      التأثير: {u.master_impact}")
        if u.suggested_action_for_master:
            print(f"      الإجراء: {u.suggested_action_for_master}")
        if u.wisdom:
            print(f"   💎 الحكمة: {u.wisdom}")
        print(f"   📊 العمق: {u.understanding_depth:.2f} ({u.depth_level.name})")
        print(f"   📊 الثقة: {u.confidence:.2f} | الجدة: {u.novelty:.2f} | التماسك: {u.coherence:.2f}")
        print(f"   ⏱️  زمن المعالجة: {u.processing_time_ms:.2f} مللي ثانية")
    
    print(f"\n{'='*60}")
    print(f"📊 تقرير محرك الفهم:")
    report = engine.status_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    print(f"\n✅ اكتمل الاختبار. محرك الفهم جاهز.")
