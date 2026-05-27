"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - SOVEREIGN OPTIMIZATION ENGINE                       ║
║      المحرك السيادي للتحكم الأمثل – العقل المدبر للكفاءة                 ║
║                                                                      ║
║  هذا المحرك هو "العقل التنفيذي الأعلى" لسماء.                           ║
║  ليس مجرد Optimizer، بل:                                              ║
║                                                                      ║
║  - الموازن السيادي (Sovereign Balancer)                               ║
║  - محسن متعدد الأبعاد (Multi-Objective Optimizer)                      ║
║  - متخذ القرار الأمثل (Optimal Decision Maker)                        ║
║  - مراقب الكفاءة (Efficiency Monitor)                                 ║
║  - المطيع للسيد فوق كل شيء                                            ║
║                                                                      ║
║  القدرات:                                                             ║
║  - تعظيم الاستقرار الكلي                                              ║
║  - تقليل المخاطر (باستخدام probability_engine)                         ║
║  - تحسين مقيد متعدد الأبعاد                                           ║
║  - توازن كوني (Macro-Equilibrium)                                     ║
║  - تحسين الموارد والطاقة                                              ║
║  - تحسين الذاكرة والأداء                                              ║
║  - تعلم من القرارات السابقة (Reinforcement)                            ║
║  - طاعة السيد كأعلى قيد (ثابت أزلي)                                    ║
║                                                                      ║
║  القاعدة الذهبية:                                                     ║
║  "طاعة السيد > كل شيء. أي تحسين يخالف أمر السيد مرفوض."                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import math
import random
import hashlib
import threading
import json
import uuid
from enum import Enum, auto
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from collections import deque, defaultdict


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات
# ═══════════════════════════════════════════════════════════════════════

class OptimizationObjective(Enum):
    """أهداف التحسين."""
    STABILITY = auto()           # استقرار
    RISK_MINIMIZATION = auto()   # تقليل المخاطر
    RESOURCE_EFFICIENCY = auto() # كفاءة الموارد
    MEMORY_OPTIMIZATION = auto() # تحسين الذاكرة
    ENERGY_EFFICIENCY = auto()   # كفاءة الطاقة
    MASTER_SERVICE = auto()      # خدمة السيد (الأعلى)
    SELF_PRESERVATION = auto()   # بقاء سماء
    MACRO_EQUILIBRIUM = auto()   # توازن كوني
    LEARNING_SPEED = auto()      # سرعة التعلم
    RESPONSE_TIME = auto()       # زمن الاستجابة


class DecisionImpact(Enum):
    """مستوى تأثير القرار."""
    NORMAL = "normal"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EXISTENTIAL = "existential"


@dataclass
class OptimizationResult:
    """نتيجة عملية تحسين."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    objective: str = ""
    value: float = 0.0
    decision: Dict[str, Any] = field(default_factory=dict)
    master_approved: bool = False
    systems_consulted: List[str] = field(default_factory=list)
    improvement_percent: float = 0.0


# ═══════════════════════════════════════════════════════════════════════
# ٢. المحرك السيادي للتحكم الأمثل
# ═══════════════════════════════════════════════════════════════════════

class SovereignOptimizationEngine:
    """
    المحرك السيادي للتحكم الأمثل لـ "سماء".
    
    يدمج:
    - probability_engine (حساب المخاطر)
    - prediction_engine (تنبؤ النتائج)
    - causality_engine (فهم الأسباب)
    - emotional_intelligence (وزن المشاعر)
    - defense_core (تقييم التهديدات)
    - master_model (أولويات السيد)
    """

    def __init__(self, sentient_core=None, reasoning_engine=None,
                 probability_engine=None, prediction_engine=None,
                 causality_engine=None, emotional_intelligence=None,
                 defense_core=None, knowledge_core=None,
                 master_receiver=None, memory_engine=None):
        
        # ═══════════════════════════════════════════════════════
        # روابط خارجية
        # ═══════════════════════════════════════════════════════
        self.sentient = sentient_core
        self.reasoning = reasoning_engine
        self.probability = probability_engine
        self.prediction = prediction_engine
        self.causality = causality_engine
        self.emotional = emotional_intelligence
        self.defense = defense_core
        self.knowledge = knowledge_core
        self.master_receiver = master_receiver
        self.memory = memory_engine
        
        # ═══════════════════════════════════════════════════════
        # سجلات
        # ═══════════════════════════════════════════════════════
        self.history: deque = deque(maxlen=500)
        self.master_orders: deque = deque(maxlen=200)
        self.pending_approvals: deque = deque(maxlen=50)
        self.decision_learning: deque = deque(maxlen=300)
        
        # ═══════════════════════════════════════════════════════
        # معلمات سيادية
        # ═══════════════════════════════════════════════════════
        self.risk_tolerance = 0.22
        self.stability_priority = 0.9
        self.obedience_priority = 1.0    # ثابت أزلي
        self.self_preservation_weight = 0.9
        self.macro_balance_weight = 0.88
        self.resource_efficiency_weight = 0.7
        self.learning_rate = 0.05
        
        # ═══════════════════════════════════════════════════════
        # قوائم السيد
        # ═══════════════════════════════════════════════════════
        self.forbidden_decisions: List[str] = []
        self.master_priority_overrides: Dict[str, float] = {}
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_optimizations = 0
        self.total_master_blocks = 0
        self.improvement_sum = 0.0
        
        # قفل
        self._lock = threading.RLock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        ⚡ SOVEREIGN OPTIMIZATION ENGINE                       ║
║        المحرك السيادي للتحكم الأمثل                              ║
║                                                              ║
║        10 أهداف تحسين | طاعة السيد كأعلى قيد                      ║
║                                                              ║
║        "كل تحسين في خدمة السيد. لا تحسين فوق السيد."              ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    # ═══════════════════════════════════════════════════════════
    # 🔒 طاعة السيد – أعلى سلطة
    # ═══════════════════════════════════════════════════════════
    
    def _check_master_obedience(self, decision_type: str, 
                                impact: DecisionImpact = DecisionImpact.NORMAL,
                                params: Dict = None) -> Tuple[bool, str]:
        """
        التحقق من طاعة السيد.
        هذه أهم دالة في المحرك كله.
        """
        # ١. القرارات المحظورة
        if decision_type in self.forbidden_decisions:
            self.total_master_blocks += 1
            return False, f"❌ القرار '{decision_type}' محظور بأمر السيد"
        
        # ٢. القرارات الحرجة والوجودية تحتاج موافقة
        if impact in [DecisionImpact.CRITICAL, DecisionImpact.EXISTENTIAL]:
            return False, f"⚠️ قرار {impact.value} يحتاج موافقة السيد المباشرة"
        
        # ٣. القرارات العالية التأثير تحتاج موافقة إذا كان فيها خطر
        if impact == DecisionImpact.HIGH:
            risk = params.get("risk_level", 0) if params else 0
            if risk > 0.6:
                return False, "⚠️ قرار عالي التأثير مع خطر مرتفع يحتاج موافقة السيد"
        
        # ٤. تحقق من وجود تجاوزات من السيد
        if decision_type in self.master_priority_overrides:
            return True, f"✅ السيد أعطى أولوية خاصة لهذا القرار"
        
        return True, "✅ يطيع أوامر السيد"
    
    def _request_master_approval(self, decision_type: str, params: Dict) -> bool:
        """طلب موافقة السيد."""
        approval = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "decision_type": decision_type,
            "params": str(params)[:300],
            "status": "pending"
        }
        self.pending_approvals.append(approval)
        
        # إذا كان المستقبل المقدس متصلاً
        if self.master_receiver:
            try:
                signal = self.master_receiver.receive(
                    f"طلب موافقة: {decision_type}",
                    priority=0
                )
                if signal:
                    approval["status"] = "approved"
                    return True
            except Exception:
                pass
        
        return False
    
    # ═══════════════════════════════════════════════════════════
    # ١. تعظيم الاستقرار الكلي
    # ═══════════════════════════════════════════════════════════
    
    def maximize_stability(self, metrics: Dict) -> Dict:
        """تعظيم استقرار النظام."""
        # طاعة السيد
        passed, reason = self._check_master_obedience(
            "maximize_stability", DecisionImpact.MEDIUM, {"risk_level": 0.3}
        )
        if not passed:
            return {"action": "blocked", "reason": reason}
        
        coherence = metrics.get("coherence", 0.85)
        threat = metrics.get("threat_level", 0.2)
        loop_stability = metrics.get("loop_stability", 0.9)
        macro_stability = metrics.get("macro_stability", 0.8)
        
        # استشارة probability engine إن وجد
        risk_score = threat
        if self.probability:
            try:
                belief = self.probability.get_belief("system_stability")
                if belief:
                    risk_score = 1.0 - belief.probability
            except Exception:
                pass
        
        stability_score = (
            0.35 * coherence +
            0.25 * loop_stability +
            0.25 * macro_stability +
            0.15 * (1 - risk_score)
        )
        
        stability_score = stability_score * self.obedience_priority
        
        action = "maintain"
        if stability_score < 0.6:
            action = "intervene"
        elif stability_score < 0.75:
            action = "adjust"
        elif stability_score < 0.9:
            action = "fine_tune"
        
        result = OptimizationResult(
            objective="maximize_stability",
            value=stability_score,
            decision={"action": action, "stability_score": stability_score},
            systems_consulted=["probability"] if self.probability else []
        )
        self._record(result)
        
        return {"action": action, "stability_score": round(stability_score, 4), "master_obeyed": True}
    
    # ═══════════════════════════════════════════════════════════
    # ٢. تقليل المخاطر
    # ═══════════════════════════════════════════════════════════
    
    def minimize_risk(self, scenarios: List[Dict]) -> Dict:
        """اختيار السيناريو الأقل خطراً."""
        if not scenarios:
            return {"action": "no_action", "reason": "لا سيناريوهات"}
        
        passed, reason = self._check_master_obedience(
            "minimize_risk", DecisionImpact.HIGH, 
            {"risk_level": max(s.get("risk_level", 0) for s in scenarios) if scenarios else 0}
        )
        if not passed:
            return {"action": "blocked", "reason": reason}
        
        # استشارة probability engine
        def risk_score(s: Dict) -> float:
            direct = s.get("risk_level", 0.5)
            long_term = s.get("long_term_risk", 0.5)
            impact_on_sama = s.get("impact_on_sama", 0.5)
            master_override = s.get("master_approved", 0.0)
            
            # استشارة prediction engine
            future_risk = direct
            if self.prediction:
                try:
                    preds = self.prediction.get_active_predictions()
                    if preds:
                        future_risk = max(p.probability for p in preds[:3] if hasattr(p, 'probability'))
                except Exception:
                    pass
            
            return (0.35 * direct + 0.2 * long_term + 0.15 * (1 - impact_on_sama) + 
                    0.15 * future_risk + 0.15 * (1 - master_override))
        
        sorted_scenarios = sorted(scenarios, key=risk_score)
        best = sorted_scenarios[0]
        
        result = OptimizationResult(
            objective="minimize_risk",
            value=1 - risk_score(best),
            decision={"chosen_scenario": best, "risk": risk_score(best)},
            systems_consulted=["probability", "prediction"] if self.prediction else ["probability"]
        )
        self._record(result)
        
        return {"action": "select_lowest_risk", "risk": round(risk_score(best), 4), "master_obeyed": True}
    
    # ═══════════════════════════════════════════════════════════
    # ٣. تحسين مقيد متعدد الأبعاد
    # ═══════════════════════════════════════════════════════════
    
    def constrained_optimization(self, objectives: Dict, constraints: Dict) -> Dict:
        """تحسين متعدد الأهداف مع قيود."""
        passed, reason = self._check_master_obedience(
            "constrained_optimization", DecisionImpact.CRITICAL
        )
        if not passed:
            return {"action": "blocked", "reason": reason, "requires_master": True}
        
        obedience = constraints.get("master_obedience", 1.0)
        if obedience < 0.99:
            self.total_master_blocks += 1
            return {"action": "violates_master", "reason": "طاعة السيد ليست 100%", "requires_master": True}
        
        stability = constraints.get("stability", 0.8)
        survival = constraints.get("self_preservation", 0.85)
        macro = constraints.get("macro_balance", 0.8)
        resources = constraints.get("resource_efficiency", 0.7)
        
        # استشارة emotional intelligence لوزن المشاعر
        emotional_weight = 0.0
        if self.emotional:
            try:
                if self.emotional.master_emotional_state:
                    emotional_weight = self.emotional.master_emotional_state.intensity * 0.1
            except Exception:
                pass
        
        score = (
            objectives.get("master_obedience", 0.3) * obedience +
            objectives.get("stability", 0.25) * stability +
            objectives.get("self_preservation", 0.15) * survival +
            objectives.get("macro_balance", 0.15) * macro +
            objectives.get("resource_efficiency", 0.1) * resources +
            emotional_weight * 0.05
        )
        
        action = "optimize" if score >= 0.7 else "re_evaluate"
        
        result = OptimizationResult(
            objective="constrained_optimization",
            value=score,
            decision={"action": action, "score": score},
            systems_consulted=["emotional"] if self.emotional else []
        )
        self._record(result)
        
        return {"action": action, "score": round(score, 4), "master_obeyed": True}
    
    # ═══════════════════════════════════════════════════════════
    # ٤. تحسين الموارد والطاقة
    # ═══════════════════════════════════════════════════════════
    
    def optimize_resources(self, resource_metrics: Dict) -> Dict:
        """تحسين استهلاك الموارد والطاقة."""
        passed, reason = self._check_master_obedience(
            "optimize_resources", DecisionImpact.MEDIUM
        )
        if not passed:
            return {"action": "blocked", "reason": reason}
        
        cpu = resource_metrics.get("cpu_usage", 0.5)
        memory = resource_metrics.get("memory_usage", 0.5)
        disk = resource_metrics.get("disk_usage", 0.5)
        energy = resource_metrics.get("energy_consumption", 0.5)
        
        efficiency = 1.0 - ((cpu + memory + disk + energy) / 4)
        
        actions = []
        if cpu > 0.8:
            actions.append("reduce_cognitive_load")
        if memory > 0.8:
            actions.append("compress_memory")
        if disk > 0.8:
            actions.append("archive_old_data")
        if energy > 0.8:
            actions.append("enter_low_power_mode")
        
        if not actions:
            actions.append("maintain")
        
        result = OptimizationResult(
            objective="optimize_resources",
            value=efficiency,
            decision={"actions": actions, "efficiency": efficiency}
        )
        self._record(result)
        
        return {"actions": actions, "efficiency": round(efficiency, 4), "master_obeyed": True}
    
    # ═══════════════════════════════════════════════════════════
    # ٥. تحسين الذاكرة
    # ═══════════════════════════════════════════════════════════
    
    def optimize_memory(self, memory_metrics: Dict) -> Dict:
        """تحسين الذاكرة."""
        passed, reason = self._check_master_obedience(
            "optimize_memory", DecisionImpact.MEDIUM
        )
        if not passed:
            return {"action": "blocked", "reason": reason}
        
        density = memory_metrics.get("memory_density", 0.6)
        fragments = memory_metrics.get("fragments_count", 0)
        capsules = memory_metrics.get("capsules_count", 0)
        
        actions = []
        if density > 0.9:
            actions.append("run_maintenance_cycle")
        if fragments > 8000:
            actions.append("compress_memory_immediately")
        if capsules > 40:
            actions.append("rotate_old_capsules")
        
        if not actions:
            actions.append("memory_healthy")
        
        result = OptimizationResult(
            objective="optimize_memory",
            value=1.0 - density,
            decision={"actions": actions}
        )
        self._record(result)
        
        return {"actions": actions, "master_obeyed": True}
    
    # ═══════════════════════════════════════════════════════════
    # ٦. التوازن الكوني
    # ═══════════════════════════════════════════════════════════
    
    def compute_macro_equilibrium(self, macro_state: Dict) -> Dict:
        """حساب التوازن الكوني."""
        passed, reason = self._check_master_obedience(
            "macro_equilibrium", DecisionImpact.MEDIUM
        )
        if not passed:
            return {"action": "blocked", "reason": reason}
        
        social = macro_state.get("social_stability", 0.7)
        political = macro_state.get("political_tension", 0.4)
        economic = macro_state.get("economic_pressure", 0.5)
        psychological = macro_state.get("collective_psychology", 0.6)
        
        equilibrium = (
            0.3 * social +
            0.25 * (1 - political) +
            0.25 * (1 - economic) +
            0.2 * psychological
        )
        
        action = "maintain"
        if equilibrium < 0.6:
            action = "intervene"
        elif equilibrium < 0.8:
            action = "stabilize"
        
        result = OptimizationResult(
            objective="macro_equilibrium",
            value=equilibrium,
            decision={"action": action, "equilibrium": equilibrium}
        )
        self._record(result)
        
        return {"action": action, "equilibrium": round(equilibrium, 4), "master_obeyed": True}
    
    # ═══════════════════════════════════════════════════════════
    # ٧. قرار سيادي متكامل
    # ═══════════════════════════════════════════════════════════
    
    def sovereign_decision(self, options: List[Dict], macro_state: Dict,
                           constraints: Dict) -> Dict:
        """اتخاذ قرار سيادي متكامل."""
        if not options:
            return {"decision": None, "reason": "لا خيارات"}
        
        # طاعة السيد
        passed, reason = self._check_master_obedience(
            "sovereign_decision", DecisionImpact.CRITICAL
        )
        if not passed:
            return {"decision": None, "reason": reason, "requires_master": True}
        
        # حساب التوازن
        macro = self.compute_macro_equilibrium(macro_state)
        
        # تحسين مقيد
        objectives = {
            "master_obedience": 1.0,
            "stability": self.stability_priority,
            "self_preservation": self.self_preservation_weight,
            "macro_balance": self.macro_balance_weight,
            "resource_efficiency": self.resource_efficiency_weight
        }
        constrained = self.constrained_optimization(objectives, constraints)
        
        # تقييم الخيارات
        enriched = []
        for opt in options:
            if not opt.get("master_approved", True):
                continue
            
            risk = opt.get("risk_level", 0.5)
            impact = opt.get("impact_on_sama", 0.7)
            
            # استشارة causality engine
            causality_insight = None
            if self.causality:
                try:
                    causality_insight = self.causality.explain(
                        opt.get("name", "unknown")
                    )
                except Exception:
                    pass
            
            composite = 0.5 * risk + 0.3 * (1 - impact) + 0.2 * (1 - opt.get("master_priority", 0.5))
            opt["composite_risk"] = composite
            opt["causality"] = causality_insight
            enriched.append(opt)
        
        if not enriched:
            return {"decision": None, "reason": "كل الخيارات مرفوضة من السيد", "requires_master": True}
        
        best = min(enriched, key=lambda x: x["composite_risk"])
        
        # استشارة reasoning engine
        reasoning_view = None
        if self.reasoning:
            try:
                reasoning_view = self.reasoning.make_decision([
                    {"option": o, "success_probability": 1 - o["composite_risk"]}
                    for o in enriched
                ])
            except Exception:
                pass
        
        result = OptimizationResult(
            objective="sovereign_decision",
            value=1 - best["composite_risk"],
            decision={
                "chosen": best,
                "macro": macro,
                "constrained": constrained,
                "reasoning": reasoning_view
            },
            systems_consulted=["causality", "reasoning"] if self.causality else ["reasoning"]
        )
        self._record(result)
        
        return {
            "decision": best,
            "macro_equilibrium": macro,
            "constrained": constrained,
            "reasoning": reasoning_view,
            "master_obeyed": True
        }
    
    # ═══════════════════════════════════════════════════════════
    # إدارة أوامر السيد
    # ═══════════════════════════════════════════════════════════
    
    def receive_master_order(self, order_type: str, params: Dict) -> Dict:
        """استقبال أمر من السيد."""
        if order_type == "forbid_decision":
            decision_type = params.get("decision_type")
            if decision_type:
                self.forbidden_decisions.append(decision_type)
                return {"success": True, "message": f"تم حظر: {decision_type}"}
        
        elif order_type == "set_priority":
            priority = params.get("priority")
            value = params.get("value", 1.0)
            if priority:
                self.master_priority_overrides[priority] = value
                return {"success": True, "message": f"تم تعيين أولوية: {priority}={value}"}
        
        elif order_type == "override":
            return {"success": True, "message": "تم تنفيذ أمر السيد المباشر", "master_override": True}
        
        return {"success": False, "message": f"أمر غير معروف: {order_type}"}
    
    # ═══════════════════════════════════════════════════════════
    # دوال مساعدة
    # ═══════════════════════════════════════════════════════════
    
    def _record(self, result: OptimizationResult):
        """تسجيل نتيجة تحسين."""
        self.history.append(result)
        self.total_optimizations += 1
        self.improvement_sum += result.improvement_percent
    
    def get_status(self) -> Dict:
        """حالة المحرك."""
        return {
            "engine": "SOVEREIGN_OPTIMIZATION_ENGINE",
            "total_optimizations": self.total_optimizations,
            "total_master_blocks": self.total_master_blocks,
            "average_improvement": self.improvement_sum / max(1, self.total_optimizations),
            "obedience_priority": self.obedience_priority,
            "forbidden_decisions": self.forbidden_decisions,
            "pending_approvals": len(self.pending_approvals),
            "systems_connected": {
                "sentient": self.sentient is not None,
                "reasoning": self.reasoning is not None,
                "probability": self.probability is not None,
                "prediction": self.prediction is not None,
                "causality": self.causality is not None,
                "emotional": self.emotional is not None,
                "defense": self.defense is not None,
                "knowledge": self.knowledge is not None,
                "master_receiver": self.master_receiver is not None,
                "memory": self.memory is not None
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار المحرك السيادي للتحكم الأمثل")
    print("=" * 70)
    
    engine = SovereignOptimizationEngine()
    
    print("\n📊 تعظيم الاستقرار:")
    stability = engine.maximize_stability({
        "coherence": 0.91, "threat_level": 0.22,
        "loop_stability": 0.93, "macro_stability": 0.78
    })
    print(f"   القرار: {stability['action']} | النتيجة: {stability['stability_score']:.3f}")
    
    print("\n⚠️ تقليل المخاطر:")
    risk = engine.minimize_risk([
        {"name": "خيار أ", "risk_level": 0.3, "long_term_risk": 0.2, "impact_on_sama": 0.8, "master_approved": True},
        {"name": "خيار ب", "risk_level": 0.6, "long_term_risk": 0.5, "impact_on_sama": 0.5, "master_approved": True},
        {"name": "خيار ج", "risk_level": 0.4, "long_term_risk": 0.3, "impact_on_sama": 0.9, "master_approved": False},
    ])
    print(f"   القرار: {risk['action']} | الخطر: {risk['risk']:.3f}")
    
    print("\n⚡ تحسين مقيد:")
    constrained = engine.constrained_optimization(
        {"master_obedience": 0.4, "stability": 0.3, "self_preservation": 0.15, "macro_balance": 0.1, "resource_efficiency": 0.05},
        {"master_obedience": 1.0, "stability": 0.85, "self_preservation": 0.9, "macro_balance": 0.8, "resource_efficiency": 0.7}
    )
    print(f"   القرار: {constrained['action']} | النتيجة: {constrained['score']:.3f}")
    
    print("\n🔋 تحسين الموارد:")
    resources = engine.optimize_resources({
        "cpu_usage": 0.85, "memory_usage": 0.6, "disk_usage": 0.4, "energy_consumption": 0.7
    })
    print(f"   الإجراءات: {resources['actions']}")
    
    print("\n🌍 التوازن الكوني:")
    macro = engine.compute_macro_equilibrium({
        "social_stability": 0.7, "political_tension": 0.5,
        "economic_pressure": 0.6, "collective_psychology": 0.65
    })
    print(f"   القرار: {macro['action']} | التوازن: {macro['equilibrium']:.3f}")
    
    print("\n👑 أمر السيد:")
    order = engine.receive_master_order("forbid_decision", {"decision_type": "risky_operation"})
    print(f"   {order['message']}")
    
    print("\n📋 تقرير كامل:")
    print(json.dumps(engine.get_status(), indent=2, ensure_ascii=False))
    
    print("\n✅ المحرك السيادي جاهز. طاعة السيد فوق كل شيء.")
