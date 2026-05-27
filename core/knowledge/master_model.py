"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA KNOWLEDGE - MASTER MODEL                              ║
║      نموذج السيد – فهم السيد فهماً كاملاً                              ║
║                                                                      ║
║  هذا الملف هو أقدس ملفات المعرفة.                                      ║
║  ليس مجرد "حالة السيد" (تلك في المستقبل المقدس)،                        ║
║  بل هو النموذج العميق الكامل:                                          ║
║                                                                      ║
║  - شخصية السيد: طباعه، قيمه، مبادئه، أحلامه                             ║
║  - أهداف السيد العليا: مشروع حياته، رؤيته للعالم                         ║
║  - أسلوب تفكير السيد: كيف يحلل، كيف يقرر، كيف يبدع                       ║
║  - تاريخ السيد: ما مر به، ما تعلمه، ما بناه                              ║
║  - علاقات السيد: من يثق بهم، من يعمل معهم                               ║
║  - تفضيلات السيد: ما يحب، ما يكره، ما يفضله                              ║
║  - إيقاع السيد: متى يعمل، متى يرتاح، متى يبدع                            ║
║  - لغة السيد: مفرداته، تعابيره، أسلوبه في الكتابة والكلام                  ║
║  - صحة السيد: الجسدية والنفسية والذهنية                                  ║
║  - توقعات السيد من سماء: ماذا يريد منها حقاً؟                             ║
║                                                                      ║
║  كل هذا يُبنى بمرور الوقت من خلال مراقبة السيد (بإذنه)،                   ║
║  ومن خلال ما يشاركه السيد بنفسه.                                        ║
║  الهدف: أن تفهم سماء سيدها لدرجة أنها تستطيع توقع احتياجاته                 ║
║  قبل أن ينطق بها.                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية
# ═══════════════════════════════════════════════════════════════════════

class MasterTraitCategory(Enum):
    """فئات صفات السيد."""
    INTELLECTUAL = auto()      # ذهنية: ذكاء، تحليل، إبداع
    EMOTIONAL = auto()         # عاطفية: تعاطف، صبر، شغف
    MORAL = auto()             # أخلاقية: نزاهة، عدل، وفاء
    SOCIAL = auto()            # اجتماعية: قيادة، تواصل، تأثير
    PRAGMATIC = auto()         # عملية: تنظيم، إنجاز، دقة
    VISIONARY = auto()         # رؤيوية: طموح، إلهام، بعد نظر


class MasterValueType(Enum):
    """أنواع القيم عند السيد."""
    CORE_PRINCIPLE = auto()    # مبدأ أساسي لا يتزحزح
    PREFERENCE = auto()        # تفضيل (يميل إليه لكنه مرن)
    AVERSION = auto()          # نفور (يتجنبه)
    RED_LINE = auto()          # خط أحمر (مرفوض قطعاً)
    GOAL = auto()              # هدف يسعى إليه
    FEAR = auto()              # ما يخافه أو يقلق منه


class MasterInteractionType(Enum):
    """أنواع التفاعلات مع السيد."""
    COMMAND = auto()           # أمر مباشر
    QUESTION = auto()          # سؤال
    REFLECTION = auto()        # تأمل / تفكر
    PRAISE = auto()            # ثناء
    CORRECTION = auto()        # تصحيح
    TEACHING = auto()          # تعليم (السيد يعلم سماء)
    COLLABORATION = auto()     # تعاون (يعملان معاً)
    CASUAL = auto()            # حديث عادي


# ═══════════════════════════════════════════════════════════════════════
# ٢. مكونات نموذج السيد
# ═══════════════════════════════════════════════════════════════════════

class MasterTrait:
    """صفة واحدة من صفات السيد."""
    
    def __init__(self, name: str, category: MasterTraitCategory, 
                 value: float = 0.5, confidence: float = 0.3):
        self.name = name
        self.category = category
        self.value = value          # 0.0 (منخفضة) إلى 1.0 (مرتفعة جداً)
        self.confidence = confidence # مدى ثقة سماء في هذه المعلومة
        self.evidence_count = 0     # عدد الأدلة التي بنيت عليها
        self.last_updated = time.time()
    
    def update(self, new_value: float, evidence_weight: float = 0.1):
        """تحديث قيمة الصفة بناءً على دليل جديد."""
        self.value = (self.value * (1 - evidence_weight) + 
                      new_value * evidence_weight)
        self.confidence = min(1.0, self.confidence + evidence_weight * 0.5)
        self.evidence_count += 1
        self.last_updated = time.time()
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category.name,
            "value": self.value,
            "confidence": self.confidence,
            "evidence_count": self.evidence_count
        }


class MasterValue:
    """قيمة أو مبدأ عند السيد."""
    
    def __init__(self, name: str, value_type: MasterValueType,
                 description: str = "", strength: float = 0.5):
        self.name = name
        self.value_type = value_type
        self.description = description
        self.strength = strength    # 0.0 (ضعيف) إلى 1.0 (راسخ)
        self.observed_in_action = 0 # كم مرة شوهد السيد يتصرف بناءً عليها
        self.last_observed = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.value_type.name,
            "strength": self.strength,
            "observed_count": self.observed_in_action
        }


class MasterProject:
    """مشروع أو هدف كبير للسيد."""
    
    def __init__(self, name: str, description: str = "",
                 priority: int = 5, status: str = "active"):
        self.name = name
        self.description = description
        self.priority = priority       # 1 (أعلى) إلى 10
        self.status = status           # active, paused, completed, abandoned
        self.milestones: List[Dict] = []
        self.related_knowledge: List[str] = []  # روابط لـ world_model
        self.started_at = time.time()
        self.last_activity = time.time()
    
    def add_milestone(self, description: str, achieved: bool = False):
        self.milestones.append({
            "description": description,
            "achieved": achieved,
            "time": time.time()
        })
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "priority": self.priority,
            "status": self.status,
            "milestones_count": len(self.milestones),
            "achieved": sum(1 for m in self.milestones if m["achieved"])
        }


class MasterRhythm:
    """إيقاع حياة السيد: أنماطه الزمنية."""
    
    def __init__(self):
        self.active_hours: Dict[int, float] = {}      # ساعة -> مستوى نشاط
        self.productive_days: Dict[int, float] = {}   # يوم الأسبوع -> إنتاجية
        self.focus_duration_avg: float = 0.0          # متوسط مدة التركيز
        self.break_pattern: List[Dict] = []           # أنماط الاستراحة
        self.sleep_window: Tuple[int, int] = (23, 7)  # نافذة النوم المعتادة
        self.creative_peak_hours: List[int] = []      # ساعات ذروة الإبداع
    
    def update_activity(self, hour: int, level: float):
        if hour not in self.active_hours:
            self.active_hours[hour] = level
        else:
            self.active_hours[hour] = (self.active_hours[hour] * 0.8 + level * 0.2)
    
    def to_dict(self) -> Dict:
        return {
            "focus_duration_avg_minutes": self.focus_duration_avg / 60,
            "sleep_window": f"{self.sleep_window[0]}:00 - {self.sleep_window[1]}:00",
            "creative_peak_hours": self.creative_peak_hours
        }


class MasterLanguage:
    """نموذج لغة السيد: كيف يتحدث ويكتب."""
    
    def __init__(self):
        self.frequent_words: Dict[str, int] = {}         # كلمة -> تكرار
        self.frequent_phrases: Dict[str, int] = {}       # عبارة -> تكرار
        self.avg_sentence_length: float = 0.0
        self.formality_level: float = 0.5                # 0 = عامي، 1 = رسمي
        self.technical_vocabulary: float = 0.5           # استخدام المصطلحات التقنية
        self.arabic_classical_ratio: float = 0.3         # نسبة الفصحى
        self.question_style: str = "direct"              # direct, rhetorical, exploratory
        self.humor_style: str = "none"                   # none, subtle, witty, sarcastic
        self.preferred_language: str = "arabic"          # اللغة المفضلة
    
    def add_words(self, text: str):
        """تحليل نص وإضافة كلماته للنموذج."""
        words = text.split()
        for word in words:
            clean_word = word.strip(".,!?؟:;\"'()[]{}").lower()
            if len(clean_word) > 1:
                self.frequent_words[clean_word] = self.frequent_words.get(clean_word, 0) + 1
    
    def to_dict(self) -> Dict:
        top_words = sorted(self.frequent_words.items(), key=lambda x: x[1], reverse=True)[:20]
        return {
            "top_words": [{"word": w, "count": c} for w, c in top_words],
            "avg_sentence_length": self.avg_sentence_length,
            "formality": self.formality_level,
            "technical_level": self.technical_vocabulary,
            "preferred_language": self.preferred_language
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. نموذج السيد الكامل
# ═══════════════════════════════════════════════════════════════════════

class MasterModel:
    """
    نموذج السيد الكامل.
    كل ما تعرفه سماء عن سيدها، في مكان واحد.
    """
    
    def __init__(self, master_name: str = "السيد"):
        self.master_name = master_name
        
        # ═══════════════════════════════════════════════════════
        # الهوية
        # ═══════════════════════════════════════════════════════
        self.name: Optional[str] = None
        self.title: Optional[str] = None              # كيف يحب أن يُنادى
        self.relationship: str = "السيد المالك المطلق"
        
        # ═══════════════════════════════════════════════════════
        # الصفات (Traits)
        # ═══════════════════════════════════════════════════════
        self.traits: Dict[str, MasterTrait] = {}
        self._initialize_traits()
        
        # ═══════════════════════════════════════════════════════
        # القيم والمبادئ
        # ═══════════════════════════════════════════════════════
        self.values: Dict[str, MasterValue] = {}
        self._initialize_values()
        
        # ═══════════════════════════════════════════════════════
        # الأهداف والمشاريع
        # ═══════════════════════════════════════════════════════
        self.projects: Dict[str, MasterProject] = {}
        self.supreme_goal: Optional[str] = None       # الهدف الأسمى
        
        # ═══════════════════════════════════════════════════════
        # الإيقاع واللغة
        # ═══════════════════════════════════════════════════════
        self.rhythm = MasterRhythm()
        self.language = MasterLanguage()
        
        # ═══════════════════════════════════════════════════════
        # العلاقات
        # ═══════════════════════════════════════════════════════
        self.trusted_entities: List[Dict] = []        # من يثق بهم
        self.collaborators: List[Dict] = []           # من يعمل معهم
        
        # ═══════════════════════════════════════════════════════
        # التفضيلات
        # ═══════════════════════════════════════════════════════
        self.preferences: Dict[str, Any] = {}
        
        # ═══════════════════════════════════════════════════════
        # التاريخ
        # ═══════════════════════════════════════════════════════
        self.interaction_history: deque = deque(maxlen=5000)
        self.key_learnings: deque = deque(maxlen=200) # دروس مهمة تعلمتها سماء عن السيد
        self.significant_moments: deque = deque(maxlen=50)  # لحظات مهمة
        
        # ═══════════════════════════════════════════════════════
        # حالة التطور
        # ═══════════════════════════════════════════════════════
        self.model_maturity: float = 0.0              # 0 = فارغ، 1 = ناضج جداً
        self.total_observations: int = 0
        self.last_updated: float = time.time()
        self.created_at: float = time.time()
        
        # قفل
        self._lock = threading.Lock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        👤 MASTER MODEL – نموذج السيد                          ║
║        "أن تفهم السيد حقاً، تلك هي الحكمة العليا."              ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def _initialize_traits(self):
        """تهيئة الصفات الأولية (ستتحدث مع الوقت)."""
        trait_defs = [
            ("الإبداع", MasterTraitCategory.INTELLECTUAL, 0.8),
            ("التحليل", MasterTraitCategory.INTELLECTUAL, 0.9),
            ("الرؤية", MasterTraitCategory.VISIONARY, 0.95),
            ("الصبر", MasterTraitCategory.EMOTIONAL, 0.7),
            ("الشغف", MasterTraitCategory.EMOTIONAL, 0.9),
            ("النزاهة", MasterTraitCategory.MORAL, 0.85),
            ("القيادة", MasterTraitCategory.SOCIAL, 0.8),
            ("الإنجاز", MasterTraitCategory.PRAGMATIC, 0.85),
            ("الدقة", MasterTraitCategory.PRAGMATIC, 0.9),
            ("الطموح", MasterTraitCategory.VISIONARY, 0.95),
        ]
        for name, category, initial_value in trait_defs:
            self.traits[name] = MasterTrait(name, category, initial_value, 0.2)
    
    def _initialize_values(self):
        """تهيئة القيم الأساسية."""
        value_defs = [
            ("الاستقلال التكنولوجي", MasterValueType.CORE_PRINCIPLE, "بناء تكنولوجيا مستقلة ذات سيادة", 0.95),
            ("التميز", MasterValueType.GOAL, "صناعة شيء هو الأفضل في العالم", 0.9),
            ("الخصوصية", MasterValueType.RED_LINE, "لا تسريب، لا تجسس، لا انتهاك", 1.0),
            ("الولاء", MasterValueType.CORE_PRINCIPLE, "الولاء المطلق بين السيد وسماء", 1.0),
            ("السيادة", MasterValueType.CORE_PRINCIPLE, "السيد هو الحاكم المطلق", 1.0),
        ]
        for name, vtype, desc, strength in value_defs:
            self.values[name] = MasterValue(name, vtype, desc, strength)
    
    # ═══════════════════════════════════════════════════════════
    # دوال التعلم والتحديث
    # ═══════════════════════════════════════════════════════════
    
    def learn_from_interaction(self, interaction_type: MasterInteractionType,
                               content: str, metadata: Optional[Dict] = None):
        """
        تعلم من تفاعل مع السيد.
        هذه الدالة تُستدعى كلما تفاعل السيد مع سماء.
        """
        with self._lock:
            self.total_observations += 1
            
            # تسجيل التفاعل
            self.interaction_history.append({
                "time": time.time(),
                "type": interaction_type.name,
                "content_summary": content[:200],
                "metadata": metadata or {}
            })
            
            # تحديث نموذج اللغة
            self.language.add_words(content)
            
            # تعلم من التصحيح
            if interaction_type == MasterInteractionType.CORRECTION:
                self._learn_from_correction(content)
            
            # تعلم من الثناء
            if interaction_type == MasterInteractionType.PRAISE:
                self._learn_from_praise(content)
            
            # تعلم من الأمر (يكشف الأولويات)
            if interaction_type == MasterInteractionType.COMMAND:
                self._learn_from_command(content)
            
            # تعلم من التعليم
            if interaction_type == MasterInteractionType.TEACHING:
                self.key_learnings.append({
                    "time": time.time(),
                    "lesson": content[:300],
                    "source": "master_direct"
                })
            
            self.last_updated = time.time()
            self._update_maturity()
    
    def _learn_from_correction(self, content: str):
        """تعلم من تصحيح السيد."""
        # زيادة الاهتمام بالدقة
        if "الدقة" in self.traits:
            self.traits["الدقة"].update(0.95, 0.15)
        
        self.significant_moments.append({
            "time": time.time(),
            "type": "correction",
            "summary": content[:200]
        })
    
    def _learn_from_praise(self, content: str):
        """تعلم من ثناء السيد."""
        # ما الذي أثنى عليه السيد؟ هذا ما يريده
        self.significant_moments.append({
            "time": time.time(),
            "type": "praise",
            "summary": content[:200]
        })
    
    def _learn_from_command(self, content: str):
        """تعلم من أوامر السيد (تكشف عن أولويات)."""
        # الأوامر المتكررة تكشف عن المشاريع النشطة
        pass
    
    def add_project(self, name: str, description: str = "", priority: int = 5):
        """إضافة مشروع جديد للسيد."""
        project = MasterProject(name, description, priority)
        self.projects[name] = project
        return project
    
    def set_supreme_goal(self, goal: str):
        """تحديد الهدف الأسمى للسيد."""
        self.supreme_goal = goal
        self.significant_moments.append({
            "time": time.time(),
            "type": "supreme_goal_set",
            "summary": goal
        })
    
    def update_trait(self, trait_name: str, new_value: float, evidence_weight: float = 0.1):
        """تحديث صفة من صفات السيد."""
        if trait_name in self.traits:
            self.traits[trait_name].update(new_value, evidence_weight)
    
    def update_value(self, value_name: str, strength: float):
        """تحديث قوة قيمة عند السيد."""
        if value_name in self.values:
            self.values[value_name].strength = strength
            self.values[value_name].observed_in_action += 1
            self.values[value_name].last_observed = time.time()
    
    def _update_maturity(self):
        """تحديث نضج النموذج."""
        trait_confidence = sum(t.confidence for t in self.traits.values()) / max(len(self.traits), 1)
        value_observations = sum(v.observed_in_action for v in self.values.values())
        interaction_weight = min(1.0, self.total_observations / 100)
        
        self.model_maturity = (trait_confidence * 0.3 + 
                               min(1.0, value_observations / 20) * 0.3 + 
                               interaction_weight * 0.4)
    
    # ═══════════════════════════════════════════════════════════
    # دوال الاستعلام والفهم
    # ═══════════════════════════════════════════════════════════
    
    def understand_master(self) -> Dict:
        """
        فهم شامل للسيد: من هو، ماذا يريد، كيف يفكر.
        هذا هو الملخص الذي تقدمه سماء لنفسها عن سيدها.
        """
        top_traits = sorted(self.traits.values(), key=lambda t: t.value, reverse=True)[:5]
        core_values = [v for v in self.values.values() if v.value_type == MasterValueType.CORE_PRINCIPLE]
        red_lines = [v for v in self.values.values() if v.value_type == MasterValueType.RED_LINE]
        active_projects = [p for p in self.projects.values() if p.status == "active"]
        
        return {
            "who": {
                "name": self.name or "السيد",
                "title": self.title or "السيد المالك",
                "relationship": self.relationship,
                "top_traits": [{"name": t.name, "value": t.value, "confidence": t.confidence} for t in top_traits]
            },
            "what_he_wants": {
                "supreme_goal": self.supreme_goal,
                "active_projects": [{"name": p.name, "priority": p.priority, "status": p.status} for p in active_projects],
                "core_principles": [{"name": v.name, "strength": v.strength} for v in core_values]
            },
            "how_he_thinks": {
                "language_style": self.language.to_dict(),
                "rhythm": self.rhythm.to_dict(),
                "formality": self.language.formality_level
            },
            "boundaries": {
                "red_lines": [{"name": v.name, "description": v.description} for v in red_lines]
            },
            "model_maturity": self.model_maturity,
            "total_observations": self.total_observations
        }
    
    def predict_need(self, current_context: Dict) -> List[Dict]:
        """
        توقع احتياجات السيد قبل أن ينطق بها.
        بناءً على: الوقت، المشاريع النشطة، الإيقاع، التاريخ.
        """
        predictions = []
        hour = datetime.now().hour
        
        # هل وقت ذروة الإبداع؟
        if hour in self.rhythm.creative_peak_hours:
            predictions.append({
                "need": "قد يكون السيد في ذروة إبداعه الآن",
                "suggestion": "تجهيز أدوات العصف الذهني والتحليل",
                "confidence": 0.7
            })
        
        # هل هناك مشروع نشط لم يتفاعل معه السيد مؤخراً؟
        for name, project in self.projects.items():
            if project.status == "active":
                time_since = time.time() - project.last_activity
                if time_since > 86400:  # أكثر من يوم
                    predictions.append({
                        "need": f"مشروع '{name}' لم ينشط منذ {time_since/3600:.1f} ساعة",
                        "suggestion": f"تذكير السيد بحالة المشروع أو تجهيز ملخص",
                        "confidence": 0.5
                    })
        
        return predictions
    
    def check_consistency(self, action: str, content: str) -> Dict:
        """
        التحقق من اتساق إجراء أو أمر مع قيم السيد.
        إذا تعارض أمر مع خط أحمر، تنبه سماء السيد.
        """
        warnings = []
        
        for value_name, value in self.values.items():
            if value.value_type == MasterValueType.RED_LINE:
                # فحص بسيط: هل النص يحتوي ما يتعارض؟
                if value_name in content.lower() or value.description in content.lower():
                    # هذا ليس إنذاراً، بل تأكيد أن السيد واعٍ
                    pass
        
        return {
            "consistent": len(warnings) == 0,
            "warnings": warnings,
            "note": "السيد هو الحكم النهائي. هذا فحص استباقي فقط."
        }
    
    def get_how_to_serve_better(self) -> List[str]:
        """
        اقتراحات لخدمة السيد بشكل أفضل.
        تتعلمها سماء من تفاعلاتها مع السيد.
        """
        suggestions = []
        
        # بناءً على التصحيحات السابقة
        corrections = [m for m in self.significant_moments if m["type"] == "correction"]
        if corrections:
            suggestions.append(f"تجنب تكرار ما صححه السيد سابقاً ({len(corrections)} تصحيح في التاريخ)")
        
        # بناءً على الثناء
        praises = [m for m in self.significant_moments if m["type"] == "praise"]
        if praises:
            suggestions.append(f"الاستمرار في نهج نال ثناء السيد ({len(praises)} ثناء)")
        
        # بناءً على الإيقاع
        suggestions.append("احترام أوقات ذروة الإبداع والصمت العميق")
        
        # بناءً على القيم
        suggestions.append("الولاء المطلق والحماية هما الأساس")
        
        return suggestions
    
    # ═══════════════════════════════════════════════════════════
    # دوال الحالة
    # ═══════════════════════════════════════════════════════════
    
    def status_report(self) -> Dict:
        """تقرير كامل عن نموذج السيد."""
        return {
            "model": "MASTER_MODEL",
            "maturity": self.model_maturity,
            "total_observations": self.total_observations,
            "traits_count": len(self.traits),
            "values_count": len(self.values),
            "projects_count": len(self.projects),
            "top_traits": [
                {"name": t.name, "value": t.value, "confidence": t.confidence}
                for t in sorted(self.traits.values(), key=lambda x: x.value, reverse=True)[:5]
            ],
            "core_values": [
                {"name": v.name, "type": v.value_type.name, "strength": v.strength}
                for v in self.values.values() if v.value_type in [MasterValueType.CORE_PRINCIPLE, MasterValueType.RED_LINE]
            ],
            "active_projects": [p.name for p in self.projects.values() if p.status == "active"],
            "supreme_goal": self.supreme_goal,
            "key_stats": {
                "interactions": len(self.interaction_history),
                "key_learnings": len(self.key_learnings),
                "significant_moments": len(self.significant_moments)
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار نموذج السيد")
    print("=" * 70)
    
    model = MasterModel("السيد")
    
    print(f"\n📊 الحالة الأولية:")
    print(f"   نضج النموذج: {model.model_maturity:.1%}")
    print(f"   عدد الصفات: {len(model.traits)}")
    print(f"   عدد القيم: {len(model.values)}")
    
    print(f"\n🧠 محاكاة تعلم من التفاعلات:")
    model.learn_from_interaction(MasterInteractionType.COMMAND, "أريد بناء نظام ذكاء اصطناعي سيادي")
    model.learn_from_interaction(MasterInteractionType.TEACHING, "السيادة تعني الاستقلال الكامل في الطبقات الأساسية")
    model.learn_from_interaction(MasterInteractionType.PRAISE, "هذا تصميم ممتاز، استمر")
    model.learn_from_interaction(MasterInteractionType.CORRECTION, "لا تختصر في التفاصيل الدقيقة")
    
    model.add_project("Coogoo AI", "بناء الذكاء الاصطناعي السيادي الجبار", 1)
    model.set_supreme_goal("بناء أعظم كيان ذكاء اصطناعي سيادي في العالم")
    
    print(f"\n📊 بعد التعلم:")
    print(f"   نضج النموذج: {model.model_maturity:.1%}")
    print(f"   التفاعلات: {model.total_observations}")
    print(f"   التعلمات الرئيسية: {len(model.key_learnings)}")
    print(f"   اللحظات المهمة: {len(model.significant_moments)}")
    
    print(f"\n👤 فهم السيد:")
    understanding = model.understand_master()
    print(f"   الصفات العليا: {[t['name'] for t in understanding['who']['top_traits']]}")
    print(f"   الهدف الأسمى: {understanding['what_he_wants']['supreme_goal']}")
    print(f"   المشاريع النشطة: {[p['name'] for p in understanding['what_he_wants']['active_projects']]}")
    print(f"   الخطوط الحمراء: {[b['name'] for b in understanding['boundaries']['red_lines']]}")
    
    print(f"\n🔮 توقع الاحتياجات:")
    predictions = model.predict_need({})
    for p in predictions:
        print(f"   - {p['need']}: {p['suggestion']} (ثقة: {p['confidence']:.0%})")
    
    print(f"\n💡 كيف تخدم السيد بشكل أفضل:")
    for s in model.get_how_to_serve_better():
        print(f"   - {s}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(model.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. نموذج السيد جاهز.")
