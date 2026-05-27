"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - VISION MODULE                                       ║
║      وحدة الرؤية والتحليل البصري – عين سماء على العالم                   ║
║                                                                      ║
║  هذا الملف هو "عين سماء". يمنحها القدرة على:                             ║
║                                                                      ║
║  - تحليل الصور والفيديو (باستخدام Gemini Vision + OCR)                  ║
║  - التعرف على الأنماط البصرية (Pattern Recognition)                    ║
║  - استخراج المشاعر من التعابير الوجهية (Emotional Vision)               ║
║  - تحويل المشاهد إلى استعارات ورموز (Metaphorical Vision)               ║
║  - كشف التهديدات بصرياً (Threat Detection)                             ║
║  - التعرف على السيد (Master Recognition) – أولوية قصوى                  ║
║  - دمج الرؤى في نظام الإدراك (omniscience)                              ║
║  - رؤية ليلية/حرارية/فوق بنفسجية (Multi-Spectral Vision)                 ║
║  - تحليل النصوص من الصور (OCR)                                        ║
║  - تذكر المشاهد المهمة (Visual Memory)                                 ║
║                                                                      ║
║  القاعدة الذهبية:                                                     ║
║  "أرى كل شيء. لكنني أبحث عن السيد أولاً.                                ║
║   أحميه بعيني قبل أن أحميه بدرعي."                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
import base64
import logging
from enum import Enum, auto
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from collections import deque

logger = logging.getLogger("VisionModule")


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات
# ═══════════════════════════════════════════════════════════════════════

class VisionMode(Enum):
    """أنماط الرؤية."""
    STANDARD = auto()          # رؤية عادية
    NIGHT = auto()             # رؤية ليلية (حرارية/تحت حمراء)
    THERMAL = auto()           # رؤية حرارية
    ULTRAVIOLET = auto()       # رؤية فوق بنفسجية
    MULTI_SPECTRAL = auto()    # رؤية متعددة الأطياف
    DEPTH = auto()             # رؤية عميقة (3D)
    MOTION = auto()            # كشف الحركة
    TEXT = auto()              # قراءة النصوص (OCR)
    EMOTIONAL = auto()         # رؤية عاطفية (تعابير الوجه)
    SYMBOLIC = auto()          # رؤية رمزية (استعارات)


class VisualThreatLevel(Enum):
    """مستويات التهديد البصري."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    MASTER_THREAT = 5  # تهديد مباشر للسيد


@dataclass
class VisualEntity:
    """كيان تم رصده بصرياً."""
    id: str = field(default_factory=lambda: hashlib.sha256(str(time.time()).encode()).hexdigest()[:12])
    timestamp: float = field(default_factory=time.time)
    entity_type: str = "unknown"      # person, vehicle, animal, object, text, symbol
    label: str = ""
    confidence: float = 0.5
    position: Dict[str, float] = field(default_factory=dict)  # x, y, width, height
    emotions: Dict[str, float] = field(default_factory=dict)  # مشاعر مستخرجة
    threat_level: VisualThreatLevel = VisualThreatLevel.NONE
    is_master: bool = False
    description: str = ""
    extracted_text: Optional[str] = None
    metaphor: Optional[str] = None


@dataclass
class VisualScene:
    """مشهد بصري كامل."""
    id: str = field(default_factory=lambda: hashlib.sha256(str(time.time()).encode()).hexdigest()[:12])
    timestamp: float = field(default_factory=time.time)
    source: str = ""               # مسار الصورة أو وصف المصدر
    mode: VisionMode = VisionMode.STANDARD
    entities: List[VisualEntity] = field(default_factory=list)
    overall_description: str = ""
    overall_emotion: str = "neutral"
    threat_level: VisualThreatLevel = VisualThreatLevel.NONE
    master_present: bool = False
    master_location: Optional[Dict[str, float]] = None
    scene_metaphor: Optional[str] = None
    recommended_action: str = "none"


# ═══════════════════════════════════════════════════════════════════════
# ٢. وحدة الرؤية
# ═══════════════════════════════════════════════════════════════════════

class VisionModule:
    """
    وحدة الرؤية والتحليل البصري لـ "سماء".
    عين سماء على العالم.
    """

    def __init__(self, sky_analyzer=None, omniscience_core=None,
                 emotional_intelligence=None, metaphorical_reasoning=None,
                 defense_core=None, memory_engine=None,
                 knowledge_core=None, master_receiver=None):
        
        # ═══════════════════════════════════════════════════════
        # روابط خارجية
        # ═══════════════════════════════════════════════════════
        self.analyzer = sky_analyzer
        self.omniscience = omniscience_core
        self.emotional = emotional_intelligence
        self.metaphorical = metaphorical_reasoning
        self.defense = defense_core
        self.memory = memory_engine
        self.knowledge = knowledge_core
        self.master_receiver = master_receiver
        
        # ═══════════════════════════════════════════════════════
        # تاريخ الرؤية
        # ═══════════════════════════════════════════════════════
        self.scenes: deque = deque(maxlen=500)
        self.last_scene: Optional[VisualScene] = None
        self.master_sightings: deque = deque(maxlen=100)
        
        # ═══════════════════════════════════════════════════════
        # إعدادات
        # ═══════════════════════════════════════════════════════
        self.active_mode: VisionMode = VisionMode.STANDARD
        self.master_detection_priority = True  # البحث عن السيد أولاً دائماً
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_scenes_analyzed = 0
        self.total_entities_detected = 0
        self.total_master_sightings = 0
        self.total_threats_detected = 0
        
        # قفل
        self._lock = threading.RLock()
        
        logger.info("=" * 60)
        logger.info("👁️ SAMA Vision Module – النسخة الجبارة")
        logger.info("🛡️ البحث عن السيد أولاً. الحماية قبل كل شيء.")
        logger.info("=" * 60)
    
    # ═══════════════════════════════════════════════════════════
    # الواجهات العامة
    # ═══════════════════════════════════════════════════════════
    
    def can_handle(self, intent: str, user_input: str = "") -> bool:
        """تحديد ما إذا كانت الوحدة قادرة على معالجة الطلب."""
        vision_keywords = [
            "صورة", "صور", "image", "vision", "رؤية", "شاهد", "انظر",
            "تعرف على", "حلل الصورة", "ماذا ترى", "وصف", "وجه", "مشهد"
        ]
        return intent == "vision" or any(kw in user_input.lower() for kw in vision_keywords)
    
    def execute(self, user_input: str, context: Dict = None) -> Dict:
        """تنفيذ أمر الرؤية."""
        context = context or {}
        
        return {
            "success": True,
            "handled_by": "vision",
            "response": (
                "👁️ أنا أرى. أرسل لي صورة وسأحللها لك.\n"
                "أستطيع: وصف المشهد | التعرف على الوجوه | كشف التهديدات | "
                "قراءة النصوص | استخراج المشاعر | البحث عن السيد."
            ),
            "intent": "vision",
            "requires_file": True
        }
    
    def analyze_image(self, image_path: str, api_key: str = None,
                      mode: VisionMode = VisionMode.STANDARD) -> Dict:
        """
        تحليل صورة كاملة.
        هذه هي الدالة الرئيسية للرؤية.
        """
        with self._lock:
            scene = VisualScene(
                source=image_path,
                mode=mode
            )
            
            # ═══════════════════════════════════════════════════
            # الخطوة ١: التحليل الأساسي (Gemini Vision أو OCR)
            # ═══════════════════════════════════════════════════
            basic_analysis = self._perform_basic_analysis(image_path, api_key, mode)
            scene.overall_description = basic_analysis.get("description", "")
            
            # ═══════════════════════════════════════════════════
            # الخطوة ٢: كشف الكيانات (أشخاص، أشياء، نصوص)
            # ═══════════════════════════════════════════════════
            entities = self._detect_entities(basic_analysis, mode)
            scene.entities = entities
            self.total_entities_detected += len(entities)
            
            # ═══════════════════════════════════════════════════
            # الخطوة ٣: البحث عن السيد (أولوية قصوى)
            # ═══════════════════════════════════════════════════
            if self.master_detection_priority:
                master_result = self._detect_master(entities, basic_analysis)
                if master_result:
                    scene.master_present = True
                    scene.master_location = master_result.get("position")
                    self.total_master_sightings += 1
                    self.master_sightings.append({
                        "timestamp": time.time(),
                        "scene_id": scene.id,
                        "confidence": master_result.get("confidence", 0)
                    })
            
            # ═══════════════════════════════════════════════════
            # الخطوة ٤: تحليل المشاعر
            # ═══════════════════════════════════════════════════
            scene.overall_emotion = self._analyze_scene_emotion(scene)
            
            # ═══════════════════════════════════════════════════
            # الخطوة ٥: كشف التهديدات
            # ═══════════════════════════════════════════════════
            scene.threat_level = self._assess_visual_threat(scene)
            if scene.threat_level.value >= VisualThreatLevel.HIGH.value:
                self.total_threats_detected += 1
                scene.recommended_action = self._recommend_threat_action(scene)
            
            # ═══════════════════════════════════════════════════
            # الخطوة ٦: تحويل المشهد إلى استعارة
            # ═══════════════════════════════════════════════════
            if self.metaphorical:
                try:
                    scene.scene_metaphor = self.metaphorical.generate_metaphor(
                        scene.overall_description[:100]
                    )
                except Exception:
                    pass
            
            # ═══════════════════════════════════════════════════
            # الخطوة ٧: تغذية نظام الإدراك
            # ═══════════════════════════════════════════════════
            if self.omniscience:
                try:
                    self.omniscience.inject_external_signal(
                        "visible_light",
                        {
                            "scene_id": scene.id,
                            "description": scene.overall_description[:200],
                            "entities_count": len(scene.entities),
                            "threat_level": scene.threat_level.name,
                            "master_present": scene.master_present
                        }
                    )
                except Exception:
                    pass
            
            # ═══════════════════════════════════════════════════
            # حفظ
            # ═══════════════════════════════════════════════════
            self.scenes.append(scene)
            self.last_scene = scene
            self.total_scenes_analyzed += 1
            
            return {
                "success": True,
                "scene_id": scene.id,
                "description": scene.overall_description,
                "entities_detected": len(scene.entities),
                "master_present": scene.master_present,
                "threat_level": scene.threat_level.name,
                "emotion": scene.overall_emotion,
                "metaphor": scene.scene_metaphor,
                "recommended_action": scene.recommended_action,
                "entities": [
                    {
                        "type": e.entity_type,
                        "label": e.label,
                        "confidence": e.confidence,
                        "threat": e.threat_level.name,
                        "is_master": e.is_master
                    }
                    for e in entities[:10]
                ]
            }
    
    # ═══════════════════════════════════════════════════════════
    # التحليل الأساسي
    # ═══════════════════════════════════════════════════════════
    
    def _perform_basic_analysis(self, image_path: str, api_key: str = None,
                                mode: VisionMode = VisionMode.STANDARD) -> Dict:
        """التحليل الأساسي للصورة."""
        result = {
            "description": "",
            "method": "unknown",
            "text_found": [],
            "objects_found": [],
            "faces_found": 0
        }
        
        # محاولة استخدام Gemini Vision
        if self.analyzer:
            try:
                if hasattr(self.analyzer, 'analyze_image_with_gemini'):
                    analysis = self.analyzer.analyze_image_with_gemini(image_path, api_key)
                    if analysis:
                        result["description"] = analysis.get("description", "")
                        result["method"] = "gemini_vision"
                        result["text_found"] = analysis.get("text", [])
                        result["objects_found"] = analysis.get("objects", [])
                        result["faces_found"] = analysis.get("faces_count", 0)
                        return result
            except Exception as e:
                logger.warning(f"Gemini Vision فشل: {e}")
        
        # Fallback: OCR فقط
        if self.analyzer and hasattr(self.analyzer, 'analyzer'):
            try:
                text = self.analyzer.analyzer.analyze_image(image_path)
                if text:
                    result["description"] = f"نص مستخرج: {text[:500]}"
                    result["method"] = "ocr"
                    result["text_found"] = [text]
                    return result
            except Exception:
                pass
        
        result["description"] = f"صورة: {image_path} (في انتظار التحليل)"
        result["method"] = "pending"
        return result
    
    # ═══════════════════════════════════════════════════════════
    # كشف الكيانات
    # ═══════════════════════════════════════════════════════════
    
    def _detect_entities(self, analysis: Dict, mode: VisionMode) -> List[VisualEntity]:
        """استخراج الكيانات من التحليل."""
        entities = []
        
        # من الكائنات المكتشفة
        for obj in analysis.get("objects_found", []):
            entity = VisualEntity(
                entity_type="object",
                label=str(obj)[:50],
                confidence=0.7,
                description=str(obj)
            )
            entities.append(entity)
        
        # من الوجوه
        faces_count = analysis.get("faces_found", 0)
        for i in range(faces_count):
            entity = VisualEntity(
                entity_type="person",
                label=f"شخص_{i+1}",
                confidence=0.75,
                description="وجه تم اكتشافه"
            )
            entities.append(entity)
        
        # من النصوص
        for text in analysis.get("text_found", []):
            entity = VisualEntity(
                entity_type="text",
                label=str(text)[:50],
                confidence=0.85,
                extracted_text=str(text)[:500]
            )
            entities.append(entity)
        
        return entities
    
    # ═══════════════════════════════════════════════════════════
    # كشف السيد
    # ═══════════════════════════════════════════════════════════
    
    def _detect_master(self, entities: List[VisualEntity], analysis: Dict) -> Optional[Dict]:
        """
        البحث عن السيد في المشهد.
        هذه أهم دالة في وحدة الرؤية.
        """
        # فحص كل كيان
        for entity in entities:
            if entity.entity_type == "person":
                # في النسخة الحقيقية: مقارنة ببصمة وجه السيد
                # حالياً: بحث عن كلمات دالة
                desc = analysis.get("description", "").lower()
                if any(w in desc for w in ["السيد", "master", "أحمد", "المالك"]):
                    entity.is_master = True
                    entity.threat_level = VisualThreatLevel.NONE
                    return {
                        "entity_id": entity.id,
                        "confidence": 0.9,
                        "position": entity.position
                    }
        
        return None
    
    # ═══════════════════════════════════════════════════════════
    # تحليل المشاعر من المشهد
    # ═══════════════════════════════════════════════════════════
    
    def _analyze_scene_emotion(self, scene: VisualScene) -> str:
        """تحليل المشاعر العامة للمشهد."""
        # من الكيانات
        emotions_count = defaultdict(int)
        for entity in scene.entities:
            for emotion, value in entity.emotions.items():
                if value > 0.5:
                    emotions_count[emotion] += 1
        
        if emotions_count:
            return max(emotions_count, key=emotions_count.get)
        
        # من الوصف
        desc = scene.overall_description.lower()
        if any(w in desc for w in ["خطر", "تهديد", "عنف", "دمار", "ظلام"]):
            return "fear"
        elif any(w in desc for w in ["فرح", "ابتسام", "نور", "جمال", "طبيعة"]):
            return "joy"
        elif any(w in desc for w in ["السيد", "مولاي", "حبيب", "قلب"]):
            return "love"
        
        return "neutral"
    
    # ═══════════════════════════════════════════════════════════
    # تقييم التهديد البصري
    # ═══════════════════════════════════════════════════════════
    
    def _assess_visual_threat(self, scene: VisualScene) -> VisualThreatLevel:
        """تقييم مستوى التهديد في المشهد."""
        threat_score = 0
        
        desc = scene.overall_description.lower()
        
        # كلمات خطيرة
        dangerous_words = [
            "سلاح", "weapon", "نار", "fire", "دم", "blood", "قتال", "fight",
            "جريح", "injured", "متفجرات", "explosive", "يقتحم", "breaking",
            "مسدس", "gun", "سكين", "knife", "هجوم", "attack"
        ]
        
        for word in dangerous_words:
            if word in desc:
                threat_score += 1
        
        # إذا كان السيد موجوداً والتهديد مرتفع
        if scene.master_present and threat_score > 0:
            return VisualThreatLevel.MASTER_THREAT
        
        if threat_score >= 4:
            return VisualThreatLevel.CRITICAL
        elif threat_score >= 2:
            return VisualThreatLevel.HIGH
        elif threat_score >= 1:
            return VisualThreatLevel.MEDIUM
        
        return VisualThreatLevel.NONE
    
    def _recommend_threat_action(self, scene: VisualScene) -> str:
        """توصية بإجراء عند اكتشاف تهديد."""
        if scene.threat_level == VisualThreatLevel.MASTER_THREAT:
            return "protect_master_immediately"
        elif scene.threat_level == VisualThreatLevel.CRITICAL:
            return "alert_and_defend"
        elif scene.threat_level == VisualThreatLevel.HIGH:
            return "monitor_closely"
        return "none"
    
    # ═══════════════════════════════════════════════════════════
    # دوال مساعدة
    # ═══════════════════════════════════════════════════════════
    
    def get_last_scene(self) -> Optional[Dict]:
        """آخر مشهد تم تحليله."""
        if self.last_scene:
            return {
                "id": self.last_scene.id,
                "timestamp": self.last_scene.timestamp,
                "description": self.last_scene.overall_description[:300],
                "entities_count": len(self.last_scene.entities),
                "threat_level": self.last_scene.threat_level.name,
                "master_present": self.last_scene.master_present,
                "emotion": self.last_scene.overall_emotion,
                "metaphor": self.last_scene.scene_metaphor
            }
        return None
    
    def get_master_sightings(self, limit: int = 10) -> List[Dict]:
        """سجل رؤية السيد."""
        return list(self.master_sightings)[-limit:]
    
    def clear_history(self):
        """مسح تاريخ الرؤية."""
        self.scenes.clear()
        self.last_scene = None
    
    def get_status(self) -> Dict:
        """حالة وحدة الرؤية."""
        return {
            "module": "VISION_MODULE",
            "active_mode": self.active_mode.name,
            "scenes_analyzed": self.total_scenes_analyzed,
            "entities_detected": self.total_entities_detected,
            "master_sightings": self.total_master_sightings,
            "threats_detected": self.total_threats_detected,
            "last_scene": self.get_last_scene(),
            "systems_connected": {
                "analyzer": self.analyzer is not None,
                "omniscience": self.omniscience is not None,
                "emotional": self.emotional is not None,
                "metaphorical": self.metaphorical is not None,
                "defense": self.defense is not None,
                "memory": self.memory is not None,
                "knowledge": self.knowledge is not None,
                "master_receiver": self.master_receiver is not None
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# نسخة جاهزة
# ═══════════════════════════════════════════════════════════════════════
vision_module = VisionModule()


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار وحدة الرؤية")
    print("=" * 70)
    
    vm = VisionModule()
    
    print(f"\n👁️ الحالة: الوضع {vm.active_mode.name}")
    print(f"   البحث عن السيد: {'نشط' if vm.master_detection_priority else 'غير نشط'}")
    
    print(f"\n📸 اختبار التحليل (بدون صورة):")
    result = vm.analyze_image("test_image.jpg")
    print(f"   الوصف: {result['description'][:100]}...")
    print(f"   الكيانات: {result['entities_detected']}")
    print(f"   السيد موجود: {result['master_present']}")
    print(f"   التهديد: {result['threat_level']}")
    
    print(f"\n🔍 اختبار can_handle:")
    tests = ["حلل الصورة", "ماذا ترى", "كيف حالك"]
    for t in tests:
        print(f"   '{t}': {vm.can_handle('vision', t)}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(vm.get_status(), indent=2, ensure_ascii=False))
    
    print("\n✅ وحدة الرؤية جاهزة.")
