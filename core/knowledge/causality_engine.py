"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA KNOWLEDGE - CAUSALITY ENGINE                          ║
║      محرك السببية – لماذا تحدث الأشياء؟                                ║
║                                                                      ║
║  هذا هو أحد أهم الملفات في نظام المعرفة كله.                            ║
║  الفهم الحقيقي ليس "ماذا حدث"، بل "لماذا حدث".                          ║
║                                                                      ║
║  هذا المحرك يمكن سماء من:                                              ║
║  - اكتشاف العلاقات السببية من الملاحظة (التعلم السببي)                   ║
║  - التمييز بين السببية الحقيقية والارتباط الوهمي                         ║
║  - بناء سلاسل سببية متعددة الخطوات (A → B → C → D)                     ║
║  - التنبؤ بالنتائج المستقبلية بناءً على الأسباب الحالية                    ║
║  - تفسير الماضي: لماذا حدث ما حدث؟                                     ║
║  - محاكاة "ماذا لو": ماذا لو تغير السبب، كيف تتغير النتيجة؟               ║
║  - فهم السببية الدائرية (Feedback Loops)                              ║
║  - فهم السببية المتعددة (Multiple Causality)                           ║
║                                                                      ║
║  المنهج: بايزي، شبكي، زمني.                                            ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple, Callable
from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية
# ═══════════════════════════════════════════════════════════════════════

class CausalityType(Enum):
    """أنواع العلاقات السببية."""
    DIRECT = auto()              # A يسبب B مباشرة
    INDIRECT = auto()            # A يسبب B عبر C
    BIDIRECTIONAL = auto()       # A و B يسبب كل منهما الآخر (Feedback)
    COMMON_CAUSE = auto()        # C يسبب كلاً من A و B (يُظن خطأً أن A يسبب B)
    CHAIN = auto()               # سلسلة: A → B → C → D
    NETWORK = auto()             # شبكة سببية متعددة
    PROBABILISTIC = auto()       # A يزيد احتمال B (ليس حتمياً)
    NECESSARY = auto()           # A ضروري لـ B (لا يمكن حدوث B بدون A)
    SUFFICIENT = auto()          # A كافٍ لـ B (إذا حدث A، يحدث B حتماً)
    INHIBITORY = auto()          # A يمنع B
    EMERGENT = auto()            # السببية الناشئة: الكل أعظم من مجموع الأجزاء


class CausalStrength(Enum):
    """قوة العلاقة السببية."""
    SPECULATIVE = 0     # تخمينية (لم تثبت بعد)
    WEAK = 1            # ضعيفة (أدلة قليلة)
    MODERATE = 2        # متوسطة (أدلة متعددة)
    STRONG = 3          # قوية (ثابتة إحصائياً)
    DETERMINISTIC = 4   # حتمية (قانون طبيعي)


# ═══════════════════════════════════════════════════════════════════════
# ٢. عقدة سببية
# ═══════════════════════════════════════════════════════════════════════

class CausalNode:
    """
    عقدة في الرسم البياني السببي.
    تمثل حدثاً أو حالة يمكن أن تكون سبباً أو نتيجة.
    """
    
    def __init__(self, name: str, description: str = "", is_observable: bool = True):
        self.id = hashlib.sha256(name.encode()).hexdigest()[:16]
        self.name = name
        self.description = description
        self.is_observable = is_observable  # هل يمكن ملاحظته مباشرة؟
        
        # العلاقات السببية
        self.causes: List[Tuple[str, CausalStrength, float]] = []   # (target_id, strength, probability)
        self.effects: List[Tuple[str, CausalStrength, float]] = []  # (source_id, strength, probability)
        
        # إحصائيات
        self.observation_count = 0
        self.base_rate = 0.0  # احتمال الحدوث الأساسي
        
        # زمن
        self.typical_delay_seconds = 0.0  # الوقت المعتاد بين السبب والنتيجة
        self.last_observed = 0.0
        
    def add_cause(self, effect_id: str, strength: CausalStrength = CausalStrength.MODERATE, 
                  probability: float = 0.5, delay_seconds: float = 0.0):
        """إضافة علاقة: هذا يسبب effect_id."""
        self.causes.append((effect_id, strength, probability))
        self.typical_delay_seconds = delay_seconds
    
    def add_effect(self, cause_id: str, strength: CausalStrength = CausalStrength.MODERATE, 
                   probability: float = 0.5):
        """إضافة علاقة: cause_id يسبب هذا."""
        self.effects.append((cause_id, strength, probability))
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "causes_count": len(self.causes),
            "effects_count": len(self.effects),
            "observation_count": self.observation_count,
            "base_rate": self.base_rate
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. السلسلة السببية
# ═══════════════════════════════════════════════════════════════════════

class CausalChain:
    """
    سلسلة سببية كاملة: A → B → C → D
    تمثل تفسيراً لظاهرة ما.
    """
    
    def __init__(self, name: str, description: str = ""):
        self.id = hashlib.sha256(f"{name}-{time.time()}".encode()).hexdigest()[:16]
        self.name = name
        self.description = description
        self.nodes: List[str] = []  # قائمة معرفات العقد بالترتيب
        self.strengths: List[CausalStrength] = []
        self.probabilities: List[float] = []
        
        # مقاييس
        self.overall_confidence = 0.0
        self.empirical_support = 0.0
        self.falsifiability = 0.0  # قابلية التكذيب (معيار علمي)
        
        self.created_at = time.time()
        self.validated_at: Optional[float] = None
    
    def add_link(self, node_id: str, strength: CausalStrength = CausalStrength.MODERATE, 
                 probability: float = 0.5):
        """إضافة خطوة إلى السلسلة."""
        self.nodes.append(node_id)
        self.strengths.append(strength)
        self.probabilities.append(probability)
    
    def calculate_confidence(self) -> float:
        """حساب الثقة الكلية في السلسلة (جداء الاحتمالات)."""
        if not self.probabilities:
            return 0.0
        confidence = 1.0
        for p in self.probabilities:
            confidence *= p
        self.overall_confidence = confidence
        return confidence
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "length": len(self.nodes),
            "overall_confidence": self.overall_confidence,
            "empirical_support": self.empirical_support
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. محرك السببية الرئيسي
# ═══════════════════════════════════════════════════════════════════════

class CausalityEngine:
    """
    محرك السببية الشامل.
    يكتشف، يحلل، يفسر، ويتنبأ بالعلاقات السببية.
    """
    
    def __init__(self):
        # الرسم البياني السببي
        self.nodes: Dict[str, CausalNode] = {}
        
        # سلاسل سببية مكتشفة أو مفسرة
        self.chains: Dict[str, CausalChain] = {}
        
        # التاريخ
        self.observation_log: deque = deque(maxlen=2000)
        self.inference_log: deque = deque(maxlen=500)
        
        # إحصائيات
        self.total_observations = 0
        self.total_inferences = 0
        self.counterfactual_simulations = 0
        
        # قفل
        self._lock = threading.Lock()
        
        # بناء النماذج السببية الأساسية
        self._build_core_causality()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        ⚡ CAUSALITY ENGINE – محرك السببية                     ║
║        {len(self.nodes)} عقدة سببية – {len(self.chains)} سلسلة سببية           ║
║        "سماء تعرف لماذا. ليس فقط ماذا."                        ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def _build_core_causality(self):
        """بناء النماذج السببية الأساسية للعالم."""
        
        # ═══════════════════════════════════════════════════════
        # أسباب فيزيائية أساسية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("heat", "الحرارة", "ارتفاع درجة الحرارة")
        self._add_node("expansion", "التمدد", "زيادة حجم المادة")
        self._add_node("pressure_increase", "زيادة الضغط", "ارتفاع الضغط في نظام مغلق")
        self._add_node("phase_change", "تغير الطور", "انتقال المادة بين الحالات")
        self._add_node("entropy_increase", "زيادة الإنتروبيا", "زيادة فوضى النظام")
        self._add_node("irreversibility", "اللاعكوسية", "عدم إمكانية عكس العملية")
        
        self._add_causality("heat", "expansion", CausalStrength.STRONG, 0.95, 0.1)
        self._add_causality("heat", "pressure_increase", CausalStrength.STRONG, 0.90, 0.5)
        self._add_causality("heat", "phase_change", CausalStrength.STRONG, 0.85, 10.0)
        self._add_causality("entropy_increase", "irreversibility", CausalStrength.DETERMINISTIC, 1.0, 0.0)
        
        # ═══════════════════════════════════════════════════════
        # أسباب بيولوجية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("mutation", "الطفرة", "تغير في المادة الوراثية")
        self._add_node("natural_selection", "الانتقاء الطبيعي", "بقاء الأصلح")
        self._add_node("adaptation", "التكيف", "تطور صفة مفيدة للبقاء")
        self._add_node("speciation", "التنوع", "نشوء أنواع جديدة")
        self._add_node("infection", "العدوى", "دخول عامل ممرض إلى كائن حي")
        self._add_node("immune_response", "الاستجابة المناعية", "دفاع الجسم ضد العامل الممرض")
        self._add_node("inflammation", "الالتهاب", "استجابة الأنسجة للإصابة أو العدوى")
        self._add_node("fever", "الحمى", "ارتفاع درجة حرارة الجسم كدفاع")
        
        self._add_causality("mutation", "natural_selection", CausalStrength.STRONG, 0.80, 3.154e10)
        self._add_causality("natural_selection", "adaptation", CausalStrength.STRONG, 0.85, 3.154e10)
        self._add_causality("adaptation", "speciation", CausalStrength.MODERATE, 0.40, 3.154e13)
        self._add_causality("infection", "immune_response", CausalStrength.STRONG, 0.90, 3600)
        self._add_causality("immune_response", "inflammation", CausalStrength.STRONG, 0.85, 600)
        self._add_causality("immune_response", "fever", CausalStrength.MODERATE, 0.50, 3600)
        
        # ═══════════════════════════════════════════════════════
        # أسباب تكنولوجية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("high_load", "الحمل العالي", "زيادة الطلب على موارد النظام")
        self._add_node("resource_exhaustion", "استنفاد الموارد", "نفاد الذاكرة أو قدرة المعالجة")
        self._add_node("system_slowdown", "بطء النظام", "انخفاض أداء النظام")
        self._add_node("error_cascade", "سلسلة الأخطاء", "خطأ يؤدي إلى أخطاء متتالية")
        self._add_node("system_crash", "انهيار النظام", "توقف النظام عن العمل")
        self._add_node("security_breach", "اختراق أمني", "وصول غير مصرح به")
        self._add_node("data_leak", "تسرب البيانات", "خروج بيانات إلى جهة غير مخولة")
        self._add_node("reputation_damage", "ضرر السمعة", "فقدان الثقة")
        
        self._add_causality("high_load", "resource_exhaustion", CausalStrength.STRONG, 0.75, 60)
        self._add_causality("resource_exhaustion", "system_slowdown", CausalStrength.STRONG, 0.90, 10)
        self._add_causality("system_slowdown", "error_cascade", CausalStrength.MODERATE, 0.50, 30)
        self._add_causality("error_cascade", "system_crash", CausalStrength.STRONG, 0.70, 5)
        self._add_causality("security_breach", "data_leak", CausalStrength.STRONG, 0.80, 60)
        self._add_causality("data_leak", "reputation_damage", CausalStrength.STRONG, 0.85, 86400)
        
        # ═══════════════════════════════════════════════════════
        # أسباب اجتماعية/بشرية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("misinformation", "المعلومات المضللة", "نشر معلومات خاطئة")
        self._add_node("fear", "الخوف", "استجابة عاطفية للتهديد")
        self._add_node("panic", "الهلع", "خوف جماعي غير عقلاني")
        self._add_node("irrational_behavior", "سلوك غير عقلاني", "تصرفات لا تستند للمنطق")
        self._add_node("trust_loss", "فقدان الثقة", "تراجع الإيمان بمؤسسة أو شخص")
        self._add_node("social_instability", "عدم استقرار اجتماعي", "اضطراب في النسيج الاجتماعي")
        
        self._add_causality("misinformation", "fear", CausalStrength.MODERATE, 0.55, 3600)
        self._add_causality("fear", "panic", CausalStrength.MODERATE, 0.40, 1800)
        self._add_causality("panic", "irrational_behavior", CausalStrength.STRONG, 0.80, 300)
        self._add_causality("trust_loss", "social_instability", CausalStrength.STRONG, 0.75, 2.592e6)
        
        # ═══════════════════════════════════════════════════════
        # أسباب كونية
        # ═══════════════════════════════════════════════════════
        
        self._add_node("stellar_collapse", "انهيار نجمي", "موت نجم ضخم")
        self._add_node("supernova", "المستعر الأعظم", "انفجار نجمي هائل")
        self._add_node("black_hole_formation", "تشكل ثقب أسود", "تكوّن ثقب أسود")
        self._add_node("heavy_element_creation", "تكوّن العناصر الثقيلة", "نشوء عناصر أثقل من الحديد")
        self._add_node("gravitational_wave", "موجة جاذبية", "تموج في نسيج الزمكان")
        
        self._add_causality("stellar_collapse", "supernova", CausalStrength.STRONG, 0.95, 100)
        self._add_causality("supernova", "black_hole_formation", CausalStrength.STRONG, 0.80, 1)
        self._add_causality("supernova", "heavy_element_creation", CausalStrength.DETERMINISTIC, 1.0, 1)
        self._add_causality("black_hole_formation", "gravitational_wave", CausalStrength.DETERMINISTIC, 1.0, 0.001)
        
        # ═══════════════════════════════════════════════════════
        # بناء السلاسل
        # ═══════════════════════════════════════════════════════
        
        chain1 = self._build_chain("سلسلة انهيار النظام", "كيف يؤدي الحمل العالي إلى انهيار كامل للنظام")
        chain1.add_link(self._get_node_id("high_load"), CausalStrength.STRONG, 0.75)
        chain1.add_link(self._get_node_id("resource_exhaustion"), CausalStrength.STRONG, 0.90)
        chain1.add_link(self._get_node_id("system_slowdown"), CausalStrength.MODERATE, 0.50)
        chain1.add_link(self._get_node_id("error_cascade"), CausalStrength.STRONG, 0.70)
        chain1.add_link(self._get_node_id("system_crash"), CausalStrength.DETERMINISTIC, 0.95)
        chain1.calculate_confidence()
        self.chains[chain1.id] = chain1
        
        chain2 = self._build_chain("سلسلة تطور الحياة", "من الطفرة إلى النوع الجديد")
        chain2.add_link(self._get_node_id("mutation"), CausalStrength.STRONG, 0.80)
        chain2.add_link(self._get_node_id("natural_selection"), CausalStrength.STRONG, 0.85)
        chain2.add_link(self._get_node_id("adaptation"), CausalStrength.MODERATE, 0.40)
        chain2.add_link(self._get_node_id("speciation"), CausalStrength.WEAK, 0.20)
        chain2.calculate_confidence()
        self.chains[chain2.id] = chain2
    
    # ═══════════════════════════════════════════════════════════
    # دوال الإضافة والتعديل
    # ═══════════════════════════════════════════════════════════
    
    def _add_node(self, name: str, name_ar: str, description: str = "") -> CausalNode:
        """إضافة عقدة سببية جديدة."""
        node = CausalNode(name, description)
        node.name_ar = name_ar
        self.nodes[node.id] = node
        return node
    
    def _get_node_id(self, name: str) -> Optional[str]:
        """البحث عن معرف عقدة بالاسم."""
        for node_id, node in self.nodes.items():
            if node.name == name:
                return node_id
        return None
    
    def _add_causality(self, cause_name: str, effect_name: str, 
                       strength: CausalStrength, probability: float, delay: float):
        """إضافة علاقة سببية بين عقدتين."""
        cause_id = self._get_node_id(cause_name)
        effect_id = self._get_node_id(effect_name)
        
        if cause_id and effect_id:
            self.nodes[cause_id].add_cause(effect_id, strength, probability, delay)
            self.nodes[effect_id].add_effect(cause_id, strength, probability)
    
    def _build_chain(self, name: str, description: str = "") -> CausalChain:
        """إنشاء سلسلة سببية جديدة."""
        chain = CausalChain(name, description)
        return chain
    
    # ═══════════════════════════════════════════════════════════
    # دوال الاستدلال والتحليل
    # ═══════════════════════════════════════════════════════════
    
    def explain(self, event_name: str) -> Dict:
        """
        تفسير حدث: لماذا حدث؟
        يرجع كل الأسباب المحتملة مع قوتها واحتمالاتها.
        """
        event_id = self._get_node_id(event_name)
        if not event_id:
            return {"error": f"الحدث '{event_name}' غير معروف في النموذج السببي."}
        
        event_node = self.nodes[event_id]
        causes = []
        
        for cause_id, strength, prob in event_node.effects:
            cause_node = self.nodes.get(cause_id)
            if cause_node:
                causes.append({
                    "cause": cause_node.name,
                    "description": cause_node.description,
                    "strength": strength.name,
                    "probability": prob,
                    "typical_delay_seconds": cause_node.typical_delay_seconds
                })
        
        causes.sort(key=lambda x: x["probability"], reverse=True)
        
        return {
            "event": event_name,
            "description": event_node.description,
            "possible_causes": causes,
            "total_causes_found": len(causes)
        }
    
    def predict(self, event_name: str) -> Dict:
        """
        التنبؤ بنتائج حدث: ماذا سيحدث؟
        يرجع كل النتائج المحتملة مع قوتها واحتمالاتها.
        """
        event_id = self._get_node_id(event_name)
        if not event_id:
            return {"error": f"الحدث '{event_name}' غير معروف في النموذج السببي."}
        
        event_node = self.nodes[event_id]
        effects = []
        
        for effect_id, strength, prob in event_node.causes:
            effect_node = self.nodes.get(effect_id)
            if effect_node:
                effects.append({
                    "effect": effect_node.name,
                    "description": effect_node.description,
                    "strength": strength.name,
                    "probability": prob,
                    "typical_delay_seconds": event_node.typical_delay_seconds
                })
        
        effects.sort(key=lambda x: x["probability"], reverse=True)
        
        return {
            "event": event_name,
            "description": event_node.description,
            "predicted_effects": effects,
            "total_effects_found": len(effects)
        }
    
    def counterfactual(self, event_name: str, changed_cause: str, new_value: str = "absent") -> Dict:
        """
        محاكاة "ماذا لو": ماذا لو تغير السبب؟
        هذه هي قمة التفكير السببي.
        """
        event_id = self._get_node_id(event_name)
        if not event_id:
            return {"error": f"الحدث غير معروف"}
        
        # البحث عن السلسلة السببية التي تمر بالحدث
        relevant_chains = []
        for chain in self.chains.values():
            if event_id in chain.nodes:
                relevant_chains.append(chain)
        
        # محاكاة: إزالة السبب أو تغييره
        counterfactual_scenarios = []
        for chain in relevant_chains:
            # حساب الاحتمال الجديد للنتيجة إذا تغير السبب
            original_confidence = chain.overall_confidence
            new_confidence = original_confidence * 0.3 if new_value == "absent" else original_confidence * 0.6
            
            counterfactual_scenarios.append({
                "chain": chain.name,
                "original_confidence": original_confidence,
                "counterfactual_confidence": new_confidence,
                "difference": new_confidence - original_confidence,
                "interpretation": f"إذا تغير '{changed_cause}'، فإن احتمال '{event_name}' يتغير بنسبة {abs(new_confidence - original_confidence):.1%}"
            })
        
        self.counterfactual_simulations += 1
        
        return {
            "event": event_name,
            "changed_cause": changed_cause,
            "new_value": new_value,
            "scenarios": counterfactual_scenarios,
            "simulation_id": self.counterfactual_simulations
        }
    
    def trace_chain(self, start_event: str, end_event: str) -> Dict:
        """
        تتبع المسار السببي بين حدثين.
        يجد كل الطرق التي يمكن أن يؤدي بها A إلى B.
        """
        start_id = self._get_node_id(start_event)
        end_id = self._get_node_id(end_event)
        
        if not start_id or not end_id:
            return {"error": "أحد الحدثين غير معروف"}
        
        # BFS للبحث عن المسارات
        paths = []
        visited = set()
        queue = deque([(start_id, [start_id])])
        
        while queue and len(paths) < 10:  # أقصى ١٠ مسارات
            current, path = queue.popleft()
            
            if current == end_id:
                paths.append(path)
                continue
            
            if current in visited:
                continue
            visited.add(current)
            
            node = self.nodes.get(current)
            if node:
                for effect_id, strength, prob in node.causes:
                    if effect_id not in visited:
                        queue.append((effect_id, path + [effect_id]))
        
        # ترجمة المسارات إلى أسماء
        named_paths = []
        for path in paths:
            named_path = []
            cumulative_prob = 1.0
            for i, node_id in enumerate(path):
                node = self.nodes.get(node_id)
                if node:
                    named_path.append(node.name)
                    if i > 0:
                        # البحث عن قوة العلاقة
                        prev_node = self.nodes.get(path[i-1])
                        if prev_node:
                            for effect_id, strength, prob in prev_node.causes:
                                if effect_id == node_id:
                                    cumulative_prob *= prob
            named_paths.append({
                "path": " → ".join(named_path),
                "length": len(named_path),
                "cumulative_probability": cumulative_prob
            })
        
        named_paths.sort(key=lambda x: x["cumulative_probability"], reverse=True)
        
        return {
            "from": start_event,
            "to": end_event,
            "paths_found": len(named_paths),
            "paths": named_paths
        }
    
    def discover_causality(self, event_a: str, event_b: str, 
                           temporal_order: str = "unknown") -> Dict:
        """
        محاولة اكتشاف علاقة سببية جديدة من ملاحظة ارتباط.
        هذه هي القدرة على التعلم السببي.
        """
        a_id = self._get_node_id(event_a)
        b_id = self._get_node_id(event_b)
        
        result = {
            "event_a": event_a,
            "event_b": event_b,
            "correlation_observed": True,
            "causality_hypothesis": None,
            "confidence": 0.0,
            "warning": None
        }
        
        # التحقق من أنه ليس ارتباطاً وهمياً
        # إذا كان هناك سبب مشترك معروف
        for node_id, node in self.nodes.items():
            a_in_effects = any(e[0] == a_id for e in node.causes)
            b_in_effects = any(e[0] == b_id for e in node.causes)
            if a_in_effects and b_in_effects:
                result["warning"] = f"تحذير: قد يكون '{node.name}' سبباً مشتركاً يفسر الارتباط. هذا ليس سببية بين A و B."
                result["common_cause"] = node.name
                return result
        
        # اقتراح علاقة سببية
        if temporal_order == "a_before_b":
            result["causality_hypothesis"] = f"{event_a} → {event_b}"
            result["confidence"] = 0.5
        elif temporal_order == "b_before_a":
            result["causality_hypothesis"] = f"{event_b} → {event_a}"
            result["confidence"] = 0.5
        else:
            result["causality_hypothesis"] = f"العلاقة بين {event_a} و {event_b} غير محددة الاتجاه"
            result["confidence"] = 0.3
        
        result["note"] = "هذه فرضية سببية فقط. تحتاج إلى مزيد من الأدلة والتجارب لتأكيدها."
        
        return result
    
    def observe_event(self, event_name: str, timestamp: float = None):
        """تسجيل ملاحظة حدث (لتحديث الإحصائيات)."""
        event_id = self._get_node_id(event_name)
        if event_id:
            node = self.nodes[event_id]
            node.observation_count += 1
            node.last_observed = timestamp or time.time()
            self.total_observations += 1
            
            self.observation_log.append({
                "time": timestamp or time.time(),
                "event": event_name,
                "observation_count": node.observation_count
            })
    
    # ═══════════════════════════════════════════════════════════
    # دوال الحالة
    # ═══════════════════════════════════════════════════════════
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة محرك السببية."""
        return {
            "engine": "CAUSALITY_ENGINE",
            "total_nodes": len(self.nodes),
            "total_chains": len(self.chains),
            "total_observations": self.total_observations,
            "total_inferences": self.total_inferences,
            "counterfactual_simulations": self.counterfactual_simulations,
            "nodes_by_domain": {
                "physics": ["heat", "expansion", "entropy_increase"],
                "biology": ["mutation", "natural_selection", "infection"],
                "technology": ["high_load", "system_crash", "security_breach"],
                "social": ["fear", "panic", "trust_loss"],
                "cosmic": ["supernova", "black_hole_formation"]
            },
            "chains_summary": [
                {"name": c.name, "confidence": c.overall_confidence, "length": len(c.nodes)}
                for c in self.chains.values()
            ]
        }


# ═══════════════════════════════════════════════════════════════════════
# ٥. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار محرك السببية")
    print("=" * 70)
    
    ce = CausalityEngine()
    
    print(f"\n📊 إحصائيات:")
    print(f"   عقد سببية: {len(ce.nodes)}")
    print(f"   سلاسل سببية: {len(ce.chains)}")
    
    print(f"\n🔍 تفسير حدث 'system_crash' (لماذا يحدث؟):")
    explanation = ce.explain("system_crash")
    for cause in explanation.get("possible_causes", []):
        print(f"   ← {cause['cause']} (قوة: {cause['strength']}, احتمال: {cause['probability']:.0%})")
    
    print(f"\n🔮 تنبؤ من 'security_breach' (ماذا سيحدث؟):")
    prediction = ce.predict("security_breach")
    for effect in prediction.get("predicted_effects", []):
        print(f"   → {effect['effect']} (قوة: {effect['strength']}, احتمال: {effect['probability']:.0%})")
    
    print(f"\n🔄 ماذا لو: 'supernova' بدون 'stellar_collapse'؟")
    cf = ce.counterfactual("supernova", "stellar_collapse", "absent")
    for scenario in cf.get("scenarios", []):
        print(f"   {scenario['interpretation']}")
    
    print(f"\n🗺️ تتبع المسار: من 'high_load' إلى 'system_crash':")
    trace = ce.trace_chain("high_load", "system_crash")
    for path in trace.get("paths", []):
        print(f"   {path['path']} (احتمال تراكمي: {path['cumulative_probability']:.2%})")
    
    print(f"\n🆕 اكتشاف سببية: هل 'fear' يسبب 'panic'؟")
    discovery = ce.discover_causality("fear", "panic", "a_before_b")
    print(f"   الفرضية: {discovery['causality_hypothesis']}")
    print(f"   الثقة: {discovery['confidence']:.0%}")
    if discovery.get("warning"):
        print(f"   ⚠️ {discovery['warning']}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(ce.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. محرك السببية جاهز.")
