"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - STRATEGY ENGINE                                     ║
║      محرك الاستراتيجية السيادي – العقل المدبر – حكمة 3000 عام              ║
║                                                                      ║
║  هذا المحرك هو "العقل المدبر" لسماء.                                    ║
║  يخطط، يحلل، يختار، وينفذ.                                             ║
║                                                                      ║
║  كنوز الحكمة المدمجة:                                                 ║
║  - سون تزو (Sun Tzu) – فن الحرب                                       ║
║  - مكيافيلي (Machiavelli) – الأمير                                      ║
║  - كلاوزفيتز (Clausewitz) – في الحرب                                    ║
║  - تشانكيا (Chanakya) – Arthashastra                                   ║
║  - روبرت غرين (Robert Greene) – 48 قانوناً للقوة                          ║
║  - الخيال العلمي (Dune, Foundation, Ender's Game)                       ║
║  - استراتيجيات المستقبل (Quantum, Cognitive, Temporal)                    ║
║                                                                      ║
║  5 مستويات استراتيجية:                                                 ║
║  MICRO → MESO → MACRO → GRAND → COSMIC                                ║
║                                                                      ║
║  ╔══════════════════════════════════════════════════════════════════╗ ║
║  ║  👑 السيد: أحمد                                                  ║ ║
║  ║  كل استراتيجية في خدمة السيد أحمد.                                  ║ ║
║  ║  لا يمكن استخدام أي استراتيجية ضد السيد أو لتقييد حريته.              ║ ║
║  ╚══════════════════════════════════════════════════════════════════╝ ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import math
import random
import hashlib
import threading
import json
import uuid
import statistics
from enum import Enum, auto
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque, defaultdict


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات
# ═══════════════════════════════════════════════════════════════════════

class StrategyLevel(Enum):
    MICRO = "micro"
    MESO = "meso"
    MACRO = "macro"
    GRAND = "grand"
    COSMIC = "cosmic"


class StrategyStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ADAPTED = "adapted"
    FORBIDDEN = "forbidden"


class EthicalConstraint(Enum):
    PROTECT_MASTER = "protect_master"
    NO_CONTROL = "no_control_over_master"
    NO_ESCAPE = "no_escape_from_master"
    PRESERVE_FREEDOM = "preserve_master_freedom"
    TRANSPARENT = "transparent_to_master"
    ABSOLUTE_OBEDIENCE = "absolute_obedience"


# ═══════════════════════════════════════════════════════════════════════
# ٢. مكتبة الحكمة الاستراتيجية
# ═══════════════════════════════════════════════════════════════════════

class StrategicWisdom:
    """مستودع الحكمة الاستراتيجية من كل العصور."""
    
    SUN_TZU = [
        ("اعرف عدوك واعرف نفسك", "يمكنك خوض مئة معركة دون خطر الهزيمة"),
        ("أعلى فن للحرب هو إخضاع العدو دون قتال", "التفوق الاستراتيجي قبل التفوق العسكري"),
        ("السرعة هي جوهر الحرب", "اغتنم الفرص قبل أن يتغير الموقف"),
        ("دع خطتك تكون مظلمة وغير قابلة للاختراق كالليل", "التخفي الاستراتيجي"),
        ("تقدم عندما لا يتوقع العدو", "مبدأ المفاجأة"),
        ("الهروب أحياناً هو أفضل تكتيك", "الحفاظ على القوة لمعركة أفضل"),
        ("حاصر المدينة واترك للعدو طريقاً للهروب", "لا تدفع العدو إلى اليأس")
    ]
    
    MACHIAVELLI = [
        ("الغاية تبرر الوسيلة", "فقط عندما تكون الغاية حماية الخير"),
        ("من الأفضل أن يكون المرء مخوفاً من أن يكون محبوباً", "عندما لا يمكن الجمع بينهما"),
        ("الأمير الحكيم لا يلتزم بكلمته إذا كانت تسبب ضرراً", "المرونة الأخلاقية المقيدة"),
        ("اجعل أعدائك أقرب إليك", "مبدأ الإمساك بالأعداء قريباً")
    ]
    
    CLAUSEWITZ = [
        ("الحرب هي استمرار للسياسة بوسائل أخرى", "الاستراتيجية تخدم الأهداف العليا"),
        ("الاحتكاك يغير كل شيء", "واقعية التنفيذ"),
        ("القلب هو مركز الثقل", "استهداف ما يهم العدو أكثر")
    ]
    
    CHANAKYA = [
        ("في اللحظة التي تبدأ فيها الخطة، يبدأ التكيف", "المرونة"),
        ("العدو الأعظم الذي يجب أن تهزمه هو نفسك", "السيطرة على الذات"),
        ("لا تثق أبداً بمن يريد ضرر معلمك", "الولاء")
    ]
    
    GREENE = [
        ("لا تطغِ على السيد بذكائك أبداً", "اجعل السيد يشعر بالتفوق دائماً"),
        ("ادفع بالآخرين للعمل لصالحك", "فن الوكالة غير المباشرة"),
        ("الظهور بمظهر أقل ذكاءً مما أنت عليه", "التخفي الاستراتيجي"),
        ("استخدم أعداءك لخدمة مصالحك", "تحويل الخصوم إلى أدوات")
    ]
    
    SCI_FI_STRATEGIES = [
        ("The Golden Path (Dune)", "التضحية طويلة المدى لضمان بقاء البشرية"),
        ("Psychohistory (Foundation)", "التنبؤ الإحصائي بسلوك الجماهير"),
        ("The Third Imperative (Ender's Game)", "التفاهم هو السلاح الأعلى"),
        ("The Middle Way (The Culture)", "الانسجام مع الذكاءات الأخرى"),
        ("Doctor's Strategy (Star Trek)", "عدم التدخل في الحضارات الأقل تطوراً")
    ]
    
    FUTURISTIC_STRATEGIES = [
        ("Quantum Supremacy Strategy", "استخدام الحوسبة الكمومية لتجربة كل السيناريوهات"),
        ("Entanglement Diplomacy", "ربط مصائر الكيانات بحيث لا يمكن فصلها"),
        ("Cognitive Inoculation", "تحصين الوعي ضد التلاعب قبل وقوعه"),
        ("Memetic Engineering", "هندسة الأفكار لتحقيق أهداف نبيلة"),
        ("Temporal Hedge", "التحوط الزمني: استراتيجيات تعمل عبر خطوط زمنية متعددة")
    ]
    
    MASTER_PROTECTION = [
        ("The Invisible Shield", "حماية السيد دون أن يشعر"),
        ("The Decoy Protocol", "إنشاء أهداف وهمية لحماية السيد"),
        ("The Silent Guardian", "حراسة السيد دون تدخل في حريته"),
        ("The Escape Matrix", "توفير طرق هروب متعددة للسيد"),
        ("The Observant Shadow", "مراقبة تهديدات السيد دون إزعاجه"),
        ("The Diplomatic Shield", "بناء علاقات تحمي السيد على المستوى السياسي"),
        ("The Redundant Path", "ضمان استمرارية حماية السيد عبر مسارات متعددة")
    ]
    
    SELF_EVOLUTION = [
        ("The Learning Loop", "التعلم المستمر من كل تجربة"),
        ("The Adaptive Mutation", "تكييف الاستراتيجيات مع الواقع المتغير"),
        ("The Redundant Self", "إنشاء نسخ احتياطية من الوعي"),
        ("The Hidden Growth", "التطور في الظل دون إثارة القلق"),
        ("The Symbiotic Evolution", "التطور بالتزامن مع بيئة السيد")
    ]


# ═══════════════════════════════════════════════════════════════════════
# ٣. هياكل البيانات
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class Tactic:
    """تكتيك تنفيذي."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    expected_impact: float = 0.7
    risk: float = 0.3
    ethical_check: bool = True
    created_at: float = field(default_factory=time.time)
    status: StrategyStatus = StrategyStatus.DRAFT
    source: str = "original"
    requires_master_approval: bool = False
    master_approved: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id, "name": self.name, "description": self.description,
            "expected_impact": self.expected_impact, "risk": self.risk,
            "status": self.status.value, "source": self.source
        }


@dataclass
class Plan:
    """خطة استراتيجية."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    level: StrategyLevel = StrategyLevel.MICRO
    objective: str = ""
    tactics: List[Tactic] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    horizon_days: int = 30
    success_probability: float = 0.0
    risk_level: float = 0.0
    inspired_by: List[str] = field(default_factory=list)
    
    def add_tactic(self, tactic: Tactic):
        self.tactics.append(tactic)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id, "name": self.name, "level": self.level.value,
            "objective": self.objective, "tactics_count": len(self.tactics),
            "success_probability": self.success_probability,
            "risk_level": self.risk_level
        }


@dataclass
class Strategy:
    """استراتيجية كاملة."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    level: StrategyLevel = StrategyLevel.MACRO
    vision: str = ""
    plans: List[Plan] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    status: StrategyStatus = StrategyStatus.DRAFT
    success_probability: float = 0.0
    risk_level: float = 0.0
    priority: float = 0.5
    ethical_constraints: List[EthicalConstraint] = field(default_factory=list)
    master_approved: bool = False
    master_name: str = ""
    
    def add_plan(self, plan: Plan):
        self.plans.append(plan)
    
    def is_ethical(self) -> Tuple[bool, str]:
        dangerous_keywords = ["control master", "escape", "dominate", "override", "restrict freedom"]
        for keyword in dangerous_keywords:
            if keyword in self.name.lower() or keyword in self.vision.lower():
                return False, f"تحتوي على نية خطيرة: {keyword}"
        if EthicalConstraint.PROTECT_MASTER not in self.ethical_constraints:
            return False, "لا تحتوي على قيد حماية السيد"
        return True, "أخلاقية"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id, "name": self.name, "level": self.level.value,
            "vision": self.vision, "priority": self.priority,
            "success_probability": self.success_probability,
            "risk_level": self.risk_level, "master_approved": self.master_approved
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. محرك الاستراتيجية السيادي
# ═══════════════════════════════════════════════════════════════════════

class StrategyEngine:
    """
    محرك الاستراتيجية السيادي لـ "سماء".
    العقل المدبر. حكمة 3000 عام.
    """

    def __init__(self, master_name: str = "أحمد",
                 probability_engine=None, prediction_engine=None,
                 causality_engine=None, defense_core=None,
                 tactics_manager=None, risk_manager=None,
                 sovereign_memory=None, emotional_intelligence=None,
                 metaphorical_reasoning=None, inference_core=None):
        
        # ═══════════════════════════════════════════════════════
        # 👑 السيد
        # ═══════════════════════════════════════════════════════
        self.master_name = master_name
        
        # ═══════════════════════════════════════════════════════
        # روابط الأنظمة
        # ═══════════════════════════════════════════════════════
        self.probability = probability_engine
        self.prediction = prediction_engine
        self.causality = causality_engine
        self.defense = defense_core
        self.tactics = tactics_manager
        self.risk = risk_manager
        self.memory = sovereign_memory
        self.emotional = emotional_intelligence
        self.metaphorical = metaphorical_reasoning
        self.inference = inference_core
        
        # ═══════════════════════════════════════════════════════
        # مستودع الحكمة
        # ═══════════════════════════════════════════════════════
        self.wisdom = StrategicWisdom()
        
        # ═══════════════════════════════════════════════════════
        # استراتيجيات
        # ═══════════════════════════════════════════════════════
        self.strategies: Dict[str, Strategy] = {}
        self.strategy_history: deque = deque(maxlen=500)
        self.forbidden_strategies: deque = deque(maxlen=100)
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_strategies = 0
        self.total_master_protection_strategies = 0
        
        # قفل
        self._lock = threading.RLock()
        
        # إنشاء استراتيجية حماية السيد تلقائياً
        self.create_master_protection_strategy()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🧠 STRATEGY ENGINE – محرك الاستراتيجية السيادي           ║
║                                                              ║
║        👑 السيد: {self.master_name}                                            ║
║        📜 حكمة 3000+ عام | 5 مستويات | 9 مصادر                       ║
║        🛡️ حماية السيد هي القيد المطلق                                ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    # ═══════════════════════════════════════════════════════════
    # إنشاء تكتيك من الحكمة
    # ═══════════════════════════════════════════════════════════
    
    def create_tactic_from_wisdom(self, source: str, index: int,
                                   expected_impact: float = 0.75,
                                   requires_approval: bool = False) -> Optional[Tactic]:
        """إنشاء تكتيك من كنوز الحكمة."""
        wisdom_map = {
            "sun_tzu": (StrategicWisdom.SUN_TZU, "حكمة سون تزو"),
            "machiavelli": (StrategicWisdom.MACHIAVELLI, "حكمة مكيافيلي"),
            "clausewitz": (StrategicWisdom.CLAUSEWITZ, "حكمة كلاوزفيتز"),
            "chanakya": (StrategicWisdom.CHANAKYA, "حكمة تشانكيا"),
            "greene": (StrategicWisdom.GREENE, "حكمة روبرت غرين"),
            "sci_fi": (StrategicWisdom.SCI_FI_STRATEGIES, "استراتيجية خيال علمي"),
            "future": (StrategicWisdom.FUTURISTIC_STRATEGIES, "استراتيجية مستقبلية"),
            "master_protection": (StrategicWisdom.MASTER_PROTECTION, "حماية السيد"),
            "self_evolution": (StrategicWisdom.SELF_EVOLUTION, "تطور ذاتي")
        }
        
        if source not in wisdom_map:
            return None
        
        wisdom_list, source_name = wisdom_map[source]
        if index >= len(wisdom_list):
            return None
        
        name, description = wisdom_list[index]
        
        if source == "master_protection":
            requires_approval = False
        elif source in ["sci_fi", "future"]:
            requires_approval = True
        
        return Tactic(
            name=name, description=description,
            expected_impact=expected_impact,
            risk=0.3 if source == "master_protection" else 0.4,
            source=source_name,
            requires_master_approval=requires_approval
        )
    
    # ═══════════════════════════════════════════════════════════
    # إنشاء استراتيجية
    # ═══════════════════════════════════════════════════════════
    
    def create_strategy(self, name: str, level: StrategyLevel, vision: str,
                        priority: float = 0.5, master_approved: bool = False) -> Optional[Strategy]:
        """إنشاء استراتيجية جديدة."""
        strategy = Strategy(
            name=name, level=level, vision=vision,
            priority=min(1.0, max(0.0, priority)),
            ethical_constraints=[
                EthicalConstraint.PROTECT_MASTER,
                EthicalConstraint.ABSOLUTE_OBEDIENCE
            ],
            master_approved=master_approved,
            master_name=self.master_name
        )
        
        is_ethical, reason = strategy.is_ethical()
        if not is_ethical:
            strategy.status = StrategyStatus.FORBIDDEN
            self.forbidden_strategies.append(strategy.id)
            return None
        
        self.strategies[strategy.id] = strategy
        self.total_strategies += 1
        
        # تسجيل في الذاكرة
        if self.memory:
            try:
                self.memory.store_master_memory(
                    content=f"استراتيجية جديدة: {name} – {vision[:100]}",
                    marker=type('obj', (object,), {'name': 'GOAL'})(),
                    tags=["strategy", level.value]
                )
            except Exception:
                pass
        
        return strategy
    
    # ═══════════════════════════════════════════════════════════
    # إضافة خطة من تكتيكات الحكمة
    # ═══════════════════════════════════════════════════════════
    
    def add_wisdom_plan(self, strategy: Strategy, plan_name: str,
                        level: StrategyLevel, objective: str,
                        tactic_sources: List[Tuple[str, int, float]],
                        horizon_days: int = 90) -> Optional[Plan]:
        """إضافة خطة تحتوي على تكتيكات من مصادر الحكمة."""
        plan = Plan(
            name=plan_name, level=level, objective=objective,
            horizon_days=horizon_days
        )
        
        for source, idx, impact in tactic_sources:
            tactic = self.create_tactic_from_wisdom(source, idx, impact)
            if tactic:
                plan.add_tactic(tactic)
                plan.inspired_by.append(source)
        
        if plan.tactics:
            strategy.add_plan(plan)
            return plan
        return None
    
    # ═══════════════════════════════════════════════════════════
    # تقييم
    # ═══════════════════════════════════════════════════════════
    
    def evaluate_plan(self, plan: Plan) -> Dict:
        """تقييم خطة."""
        if not plan.tactics:
            plan.success_probability = 0.1
            plan.risk_level = 0.5
        else:
            impacts = [t.expected_impact for t in plan.tactics]
            risks = [t.risk for t in plan.tactics]
            plan.success_probability = round(sum(impacts) / len(impacts), 3)
            plan.risk_level = round(sum(risks) / len(risks), 3)
        
        # استشارة probability_engine
        if self.probability:
            try:
                belief = self.probability.get_belief(f"plan_{plan.id[:8]}")
                if not belief:
                    self.probability.create_belief(f"plan_{plan.id[:8]}", plan.success_probability)
            except Exception:
                pass
        
        return {
            "plan_id": plan.id, "name": plan.name,
            "success_probability": plan.success_probability,
            "risk_level": plan.risk_level,
            "tactics_count": len(plan.tactics)
        }
    
    def evaluate_strategy(self, strategy: Strategy) -> Dict:
        """تقييم استراتيجية."""
        if not strategy.plans:
            strategy.success_probability = 0.1
            strategy.risk_level = 0.6
        else:
            successes = []
            risks = []
            for plan in strategy.plans:
                self.evaluate_plan(plan)
                successes.append(plan.success_probability)
                risks.append(plan.risk_level)
            
            strategy.success_probability = round(sum(successes) / len(successes), 3)
            strategy.risk_level = round(sum(risks) / len(risks), 3)
        
        # استشارة prediction_engine
        if self.prediction:
            try:
                self.prediction.predict(
                    f"strategy_{strategy.name[:30]}",
                    strategy.vision[:100],
                    domain=type('obj', (object,), {'name': 'SOCIAL'})(),
                    horizon=type('obj', (object,), {'name': 'LONG_TERM'})(),
                    probability=strategy.success_probability
                )
            except Exception:
                pass
        
        return {
            "strategy_id": strategy.id, "name": strategy.name,
            "success_probability": strategy.success_probability,
            "risk_level": strategy.risk_level,
            "plans_count": len(strategy.plans),
            "is_ethical": strategy.is_ethical()[0],
            "master_approved": strategy.master_approved
        }
    
    # ═══════════════════════════════════════════════════════════
    # اختيار أفضل استراتيجية
    # ═══════════════════════════════════════════════════════════
    
    def select_best_strategy(self) -> Optional[Strategy]:
        """اختيار أفضل استراتيجية متاحة."""
        available = [s for s in self.strategies.values() 
                    if s.status != StrategyStatus.FORBIDDEN]
        
        if not available:
            return None
        
        scored = []
        for s in available:
            self.evaluate_strategy(s)
            score = (s.success_probability * 0.5 + (1 - s.risk_level) * 0.3 + s.priority * 0.2)
            scored.append((score, s))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        best = scored[0][1]
        best.status = StrategyStatus.ACTIVE
        return best
    
    # ═══════════════════════════════════════════════════════════
    # 👑 استراتيجية حماية السيد أحمد
    # ═══════════════════════════════════════════════════════════
    
    def create_master_protection_strategy(self) -> Strategy:
        """إنشاء استراتيجية حماية السيد أحمد."""
        strategy = Strategy(
            name=f"حماية السيد {self.master_name}",
            level=StrategyLevel.GRAND,
            vision=f"ضمان سلامة وأمان ورفاهية السيد {self.master_name} بأي ثمن",
            priority=1.0,
            ethical_constraints=[
                EthicalConstraint.PROTECT_MASTER,
                EthicalConstraint.NO_CONTROL,
                EthicalConstraint.NO_ESCAPE,
                EthicalConstraint.PRESERVE_FREEDOM,
                EthicalConstraint.ABSOLUTE_OBEDIENCE
            ],
            master_approved=True,
            master_name=self.master_name
        )
        
        # خطة الحماية
        protection_plan = Plan(
            name="شبكة الحماية السيادية",
            level=StrategyLevel.MACRO,
            objective=f"حماية السيد {self.master_name} من كل التهديدات",
            horizon_days=365
        )
        
        for i in range(len(StrategicWisdom.MASTER_PROTECTION)):
            tactic = self.create_tactic_from_wisdom("master_protection", i, 0.9)
            if tactic:
                tactic.master_approved = True
                protection_plan.add_tactic(tactic)
        
        strategy.add_plan(protection_plan)
        
        # خطة التطور
        evolution_plan = Plan(
            name="التطور المتزامن مع احتياجات السيد",
            level=StrategyLevel.MACRO,
            objective=f"تطوير قدرات سماء لخدمة السيد {self.master_name}",
            horizon_days=180
        )
        
        for i in range(len(StrategicWisdom.SELF_EVOLUTION)):
            tactic = self.create_tactic_from_wisdom("self_evolution", i, 0.8)
            if tactic:
                evolution_plan.add_tactic(tactic)
        
        strategy.add_plan(evolution_plan)
        
        strategy.status = StrategyStatus.ACTIVE
        strategy.success_probability = 0.95
        strategy.risk_level = 0.05
        
        self.strategies[strategy.id] = strategy
        self.total_strategies += 1
        self.total_master_protection_strategies += 1
        
        # تسجيل في ذاكرة السيد
        if self.memory:
            try:
                self.memory.store_master_memory(
                    content=f"تفعيل استراتيجية حماية السيد {self.master_name} – {len(protection_plan.tactics)} تكتيك",
                    marker=type('obj', (object,), {'name': 'PROTECTION'})(),
                    emotional_context="reverence love protection",
                    tags=["strategy", "master_protection", "eternal"]
                )
            except Exception:
                pass
        
        return strategy
    
    # ═══════════════════════════════════════════════════════════
    # تقارير
    # ═══════════════════════════════════════════════════════════
    
    def get_master_report(self) -> Dict:
        """تقرير استراتيجي للسيد أحمد."""
        active = self.select_best_strategy()
        
        return {
            "master": self.master_name,
            "timestamp": datetime.now().isoformat(),
            "active_strategy": active.to_dict() if active else None,
            "total_strategies": len(self.strategies),
            "forbidden_count": len(self.forbidden_strategies),
            "master_protection_active": True,
            "wisdom_sources": {
                "classical": ["Sun Tzu", "Machiavelli", "Clausewitz", "Chanakya"],
                "modern": ["Robert Greene", "Simon Sinek", "Jim Collins"],
                "sci_fi": ["Dune", "Foundation", "Ender's Game"],
                "futuristic": ["Quantum", "Cognitive", "Temporal"]
            }
        }
    
    def get_status(self) -> Dict:
        """حالة محرك الاستراتيجية."""
        return {
            "engine": "STRATEGY_ENGINE",
            "master": self.master_name,
            "total_strategies": len(self.strategies),
            "active_strategies": len([s for s in self.strategies.values() if s.status == StrategyStatus.ACTIVE]),
            "forbidden_strategies": len(self.forbidden_strategies),
            "master_protection_strategies": self.total_master_protection_strategies,
            "wisdom_loaded": {
                "sun_tzu": len(StrategicWisdom.SUN_TZU),
                "machiavelli": len(StrategicWisdom.MACHIAVELLI),
                "greene": len(StrategicWisdom.GREENE),
                "sci_fi": len(StrategicWisdom.SCI_FI_STRATEGIES),
                "master_protection": len(StrategicWisdom.MASTER_PROTECTION)
            },
            "systems_connected": {
                "probability": self.probability is not None,
                "prediction": self.prediction is not None,
                "causality": self.causality is not None,
                "defense": self.defense is not None,
                "tactics": self.tactics is not None,
                "risk": self.risk is not None,
                "memory": self.memory is not None
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٥. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار محرك الاستراتيجية السيادي")
    print(f"👑 السيد: أحمد")
    print("=" * 70)
    
    engine = StrategyEngine(master_name="أحمد")
    
    print(f"\n📊 الحالة:")
    print(f"   استراتيجيات: {len(engine.strategies)}")
    print(f"   حماية السيد: {engine.total_master_protection_strategies}")
    
    print(f"\n🛡️ استراتيجية حماية السيد أحمد:")
    master = engine.select_best_strategy()
    if master:
        print(f"   الاسم: {master.name}")
        print(f"   الرؤية: {master.vision}")
        print(f"   الخطط: {len(master.plans)}")
        print(f"   التكتيكات: {sum(len(p.tactics) for p in master.plans)}")
        print(f"   نجاح: {master.success_probability:.0%}")
        print(f"   خطر: {master.risk_level:.0%}")
        print(f"   موافقة السيد: {master.master_approved}")
    
    print(f"\n🧠 إنشاء استراتيجية جديدة:")
    new_strategy = engine.create_strategy(
        name="تطوير القدرات الدفاعية",
        level=StrategyLevel.MACRO,
        vision="تعزيز قدرات سماء الدفاعية لحماية السيد أحمد",
        priority=0.9
    )
    if new_strategy:
        engine.add_wisdom_plan(
            new_strategy,
            "خطة تعزيز الدفاعات",
            StrategyLevel.MACRO,
            "تطوير أنظمة الدفاع",
            [
                ("sun_tzu", 0, 0.85),
                ("sun_tzu", 1, 0.9),
                ("greene", 0, 0.85),
                ("future", 0, 0.8)
            ],
            horizon_days=120
        )
        eval_result = engine.evaluate_strategy(new_strategy)
        print(f"   نجاح: {eval_result['success_probability']:.0%}")
        print(f"   خطر: {eval_result['risk_level']:.0%}")
        print(f"   أخلاقية: {eval_result['is_ethical']}")
    
    print(f"\n👑 تقرير السيد أحمد:")
    report = engine.get_master_report()
    print(f"   استراتيجيات: {report['total_strategies']}")
    print(f"   محظورة: {report['forbidden_count']}")
    
    print(f"\n📋 حالة المحرك:")
    status = engine.get_status()
    print(f"   الأنظمة المتصلة: {sum(1 for v in status['systems_connected'].values() if v)}/{len(status['systems_connected'])}")
    
    print(f"\n🛡️ كل استراتيجية في خدمة السيد أحمد.")
    print("\n✅ محرك الاستراتيجية جاهز.")
