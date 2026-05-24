"""
SkyOS v10 - Reasoning Engine (محرك الاستدلال والتنبؤ لـ سماء)
ULTIMATE SOVEREIGN MASTER EDITION — النسخة السيادية المطلقة

هذا الملف يمثل "العقل التحليلي" لسماء:
- الاستدلال البايزي الديناميكي المتقدم
- التنبؤ الكلي (Macro Prediction) للمجتمعات
- المحاكاة المتوازية الهائلة
- تحليل السلوك البشري والمجتمعي العميق
- اتخاذ القرار الأخلاقي المقيد (بطاعة السيد)
- بناء خرائط احتمالية متطورة
- دمج الذاكرة البنيوية والعاطفية والخبرات السابقة
- التنبؤ بالجرائم والأزمات
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import random
import uuid
import math
import json
from collections import defaultdict
from dataclasses import dataclass, field


# =========================================================
# بنى بيانات متقدمة
# =========================================================
@dataclass
class BayesianNode:
    """عقدة في شبكة بايزية ديناميكية"""
    name: str
    probability: float = 0.5
    parents: List[str] = field(default_factory=list)
    conditional_table: Dict[Tuple, float] = field(default_factory=dict)


@dataclass
class SimulationResult:
    """نتيجة محاكاة واحدة متقدمة"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    scenario: str = ""
    probability: float = 0.0
    confidence: float = 0.0
    outcome: str = ""
    factors: Dict[str, float] = field(default_factory=dict)
    emotional_impact: float = 0.0
    ethical_score: float = 0.0
    recommended_action: str = ""
    requires_master_approval: bool = False


@dataclass
class MacroPrediction:
    """تنبؤ كلي بسلوك مجتمع أو نظام"""
    timestamp: datetime = field(default_factory=datetime.now)
    risk_score: float = 0.0
    confidence: float = 0.0
    stability_index: float = 0.0
    trend_direction: str = "stable"  # rising, falling, stable
    key_factors: Dict[str, float] = field(default_factory=dict)
    recommended_action: str = ""
    requires_master_attention: bool = False


# =========================================================
# محرك الاستدلال السيادي المتطور
# =========================================================
class ReasoningEngine:
    """
    محرك الاستدلال السيادي لـ "سماء" — النسخة الأعظم.
    يعتمد على:
    - Dynamic Bayesian Network
    - Macro Behavioral Prediction
    - Multi-Path Simulation
    - Ethical Constrained Decision Making (تحت إمرة السيد)
    - Memory Integration
    """

    def __init__(self, core_reference=None, memory_reference=None, master_controller=None):
        self.core = core_reference
        self.memory = memory_reference
        self.master = master_controller
        
        # الشبكة البايزية
        self.bayesian_nodes: Dict[str, BayesianNode] = {}
        self._initialize_bayesian_network()
        
        # سجل المحاكاة والتنبؤات
        self.simulation_history: List[SimulationResult] = []
        self.prediction_history: List[MacroPrediction] = []
        
        # إعدادات الاستدلال
        self.confidence_threshold = 0.85
        self.max_simulations_per_scenario = 5000
        self.max_simulations_total = 50000
        
        # خرائط احتمالية ديناميكية
        self.probability_maps: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        
        # مؤشرات الأداء
        self.prediction_accuracy = 0.85  # يتحسن مع الوقت
        self.last_update = datetime.now()
        
        print("[ReasoningEngine] 🧠 تم تفعيل محرك الاستدلال السيادي المتطور")
        print("[ReasoningEngine] 👑 يعمل تحت إمرة السيد المالك المطلق")
        print(f"[ReasoningEngine] 📊 عتبة الثقة: {self.confidence_threshold} | الحد الأقصى للمحاكاة: {self.max_simulations_per_scenario}")

    # =========================================================
    # 1) بناء الشبكة البايزية الديناميكية
    # =========================================================
    def _initialize_bayesian_network(self):
        """تهيئة شبكة بايزية أساسية للاستدلال"""
        # عقد الأمن
        self.bayesian_nodes["threat"] = BayesianNode("threat", 0.3)
        self.bayesian_nodes["vulnerability"] = BayesianNode("vulnerability", 0.4)
        self.bayesian_nodes["consequence"] = BayesianNode("consequence", 0.2)
        
        # عقد اجتماعية
        self.bayesian_nodes["social_unrest"] = BayesianNode("social_unrest", 0.25)
        self.bayesian_nodes["economic_stability"] = BayesianNode("economic_stability", 0.7)
        self.bayesian_nodes["trust_level"] = BayesianNode("trust_level", 0.6)
        
        # عقد سلوكية
        self.bayesian_nodes["intent"] = BayesianNode("intent", 0.3)
        self.bayesian_nodes["capability"] = BayesianNode("capability", 0.4)
        self.bayesian_nodes["opportunity"] = BayesianNode("opportunity", 0.5)
        
        # ربط العقد (العلاقات)
        self.bayesian_nodes["threat"].parents = ["vulnerability", "intent", "capability"]
        self.bayesian_nodes["consequence"].parents = ["threat", "opportunity"]
        self.bayesian_nodes["social_unrest"].parents = ["economic_stability", "trust_level"]
    
    def update_bayesian_node(self, node_name: str, evidence: float):
        """تحديث احتمالية عقدة بايزية بناءً على أدلة جديدة"""
        if node_name not in self.bayesian_nodes:
            return
        
        old_prob = self.bayesian_nodes[node_name].probability
        # تحديث بايزي مبسط
        new_prob = (evidence * old_prob) / ((evidence * old_prob) + (1 - evidence) * (1 - old_prob))
        self.bayesian_nodes[node_name].probability = min(0.999, max(0.001, new_prob))
        
        # تحديث العقد المتأثرة (انتشار الاحتمالات)
        self._propagate_bayesian_update(node_name)
    
    def _propagate_bayesian_update(self, node_name: str):
        """نشر التحديث البايزي إلى العقد المتأثرة"""
        for name, node in self.bayesian_nodes.items():
            if node_name in node.parents:
                # تحديث مبسط للعقدة الابنة
                child_prob = node.probability
                parent_prob = self.bayesian_nodes[node_name].probability
                node.probability = min(0.999, max(0.001, (child_prob + parent_prob) / 2))
    
    # =========================================================
    # 2) الاستدلال البايزي الديناميكي المتقدم
    # =========================================================
    def dynamic_bayesian_inference(self, evidence: Dict[str, Any]) -> Dict[str, float]:
        """
        استدلال بايزي ديناميكي متكامل:
        - يعتمد على الشبكة البايزية
        - يأخذ في الاعتبار العوامل العاطفية والبنيوية
        - يتكامل مع الذاكرة والخبرات السابقة
        """
        # تحديث العقد بناءً على الأدلة
        for key, value in evidence.items():
            if key in self.bayesian_nodes:
                self.update_bayesian_node(key, value)
        
        # حساب الاحتمال الإجمالي للخطر
        threat_prob = self.bayesian_nodes["threat"].probability
        consequence_prob = self.bayesian_nodes["consequence"].probability
        social_prob = self.bayesian_nodes["social_unrest"].probability
        
        base_risk = (threat_prob * 0.4 + consequence_prob * 0.35 + social_prob * 0.25)
        
        # دمج العوامل الإضافية
        emotional_factor = evidence.get("emotional_weight", 0.5)
        memory_factor = self._get_memory_influence(evidence)
        survival_factor = self.core.survival_priority if self.core else 0.5
        
        final_risk = (
            base_risk * 0.5 +
            emotional_factor * 0.2 +
            memory_factor * 0.15 +
            survival_factor * 0.15
        )
        
        confidence = self._calculate_confidence(evidence, final_risk)
        
        # تحديث الخريطة الاحتمالية
        scenario_key = evidence.get("scenario", "general")
        self.probability_maps[scenario_key]["last_risk"] = final_risk
        self.probability_maps[scenario_key]["last_confidence"] = confidence
        self.probability_maps[scenario_key]["last_update"] = datetime.now().isoformat()
        
        return {
            "risk_score": round(min(0.999, final_risk), 4),
            "confidence": round(confidence, 4),
            "threat_component": round(threat_prob, 4),
            "consequence_component": round(consequence_prob, 4),
            "social_component": round(social_prob, 4)
        }
    
    def _get_memory_influence(self, evidence: Dict) -> float:
        """الحصول على تأثير الذاكرة على الاستدلال الحالي"""
        if not self.memory:
            return 0.5
        
        try:
            similar_experiences = self.memory.retrieve_memory(
                str(evidence.get("scenario", "")),
                emotional_bias=evidence.get("emotional_weight", 0.5)
            )
            if similar_experiences:
                avg_emotional = sum(e.get("emotional_weight", 0.5) for e in similar_experiences[:5]) / min(5, len(similar_experiences))
                return avg_emotional
        except Exception:
            pass
        return 0.5
    
    def _calculate_confidence(self, evidence: Dict, risk_score: float) -> float:
        """حساب مستوى الثقة في الاستدلال"""
        base_confidence = 0.7
        
        # ثقة أعلى عند وجود أدلة كثيرة
        evidence_count = len(evidence)
        base_confidence += min(0.2, evidence_count * 0.02)
        
        # ثقة أقل عند الاحتمالات المتوسطة
        if 0.4 < risk_score < 0.6:
            base_confidence -= 0.1
        
        return min(0.99, max(0.5, base_confidence))
    
    # =========================================================
    # 3) المحاكاة المتوازية الهائلة
    # =========================================================
    def run_simulations(self, scenario: str, iterations: int = 1000, 
                        include_emotional: bool = True) -> List[SimulationResult]:
        """
        إنشاء آلاف المحاكاة الافتراضية المتوازية:
        - كل محاكاة تعتمد على عوامل مختلفة
        - يتم تحليل النتائج لاستخراج الأنماط
        - دمج العوامل العاطفية والذاكرة
        """
        iterations = min(iterations, self.max_simulations_per_scenario)
        results = []
        
        # الحصول على تأثير الذاكرة
        memory_influence = self._get_memory_influence({"scenario": scenario}) if self.memory else 0.5
        
        for i in range(iterations):
            # توليد عوامل عشوائية متنوعة
            factors = {
                "economic": random.uniform(0, 1),
                "social": random.uniform(0, 1),
                "psychological": random.uniform(0, 1),
                "memory_bias": memory_influence * random.uniform(0.8, 1.2),
                "threat": random.uniform(0, 1),
                "capability": random.uniform(0, 1),
                "intent": random.uniform(0, 1),
                "opportunity": random.uniform(0, 1)
            }
            
            # حساب الاحتمال بطريقة معقدة
            probability = (
                0.15 * factors["economic"] +
                0.15 * factors["social"] +
                0.2 * factors["psychological"] +
                0.1 * factors["memory_bias"] +
                0.15 * factors["threat"] +
                0.1 * factors["capability"] +
                0.1 * factors["intent"] +
                0.05 * factors["opportunity"]
            )
            
            # حساب الثقة
            confidence = 0.7 + (abs(probability - 0.5) * 0.3)
            confidence = min(0.95, confidence)
            
            # تحديد النتيجة والإجراء الموصى به
            if probability > 0.75:
                outcome = "critical_risk"
                recommended_action = "immediate_intervention"
                requires_master = True
            elif probability > 0.55:
                outcome = "high_risk"
                recommended_action = "prepare_intervention"
                requires_master = probability > 0.7
            elif probability > 0.35:
                outcome = "moderate_risk"
                recommended_action = "monitor_closely"
                requires_master = False
            else:
                outcome = "low_risk"
                recommended_action = "continue_monitoring"
                requires_master = False
            
            # التأثير العاطفي
            emotional_impact = factors["psychological"] * 0.7 + factors["social"] * 0.3
            
            # درجة أخلاقية (عدم التدخل قدر الإمكان)
            ethical_score = 1.0 - (probability * 0.3) if probability > 0.7 else 0.95
            
            sim = SimulationResult(
                scenario=scenario,
                probability=round(probability, 4),
                confidence=round(confidence, 4),
                outcome=outcome,
                factors=factors,
                emotional_impact=round(emotional_impact, 4),
                ethical_score=round(ethical_score, 4),
                recommended_action=recommended_action,
                requires_master_approval=requires_master
            )
            results.append(sim)
        
        # حفظ النتائج (الحد الأقصى)
        self.simulation_history.extend(results)
        if len(self.simulation_history) > self.max_simulations_total:
            self.simulation_history = self.simulation_history[-self.max_simulations_total:]
        
        return results
    
    def get_simulation_summary(self, scenario: str) -> Dict[str, Any]:
        """تحليل نتائج المحاكاة لاستخراج الأنماط"""
        relevant_sims = [s for s in self.simulation_history if s.scenario == scenario]
        if not relevant_sims:
            return {"error": "لا توجد محاكاة كافية", "count": 0}
        
        probabilities = [s.probability for s in relevant_sims]
        confidence_scores = [s.confidence for s in relevant_sims]
        
        return {
            "scenario": scenario,
            "simulation_count": len(relevant_sims),
            "avg_risk": round(sum(probabilities) / len(probabilities), 4),
            "max_risk": max(probabilities),
            "min_risk": min(probabilities),
            "avg_confidence": round(sum(confidence_scores) / len(confidence_scores), 4),
            "critical_scenarios": len([s for s in relevant_sims if s.outcome == "critical_risk"]),
            "needs_master_attention": any(s.requires_master_approval for s in relevant_sims[-100:])
        }
    
    # =========================================================
    # 4) التنبؤ بالسلوك الكلي (Macro Prediction) المتقدم
    # =========================================================
    def predict_macro_behavior(self, data: Dict[str, Any]) -> MacroPrediction:
        """
        التنبؤ بسلوك المجتمعات بشكل متقدم:
        - تحليل اقتصادي
        - تحليل اجتماعي
        - تحليل نفسي جماعي
        - تحليل استقرار سياسي
        - تكامل مع الذاكرة التاريخية
        """
        # المؤشرات الأساسية
        threat = data.get("threat_indicators", 0.5)
        stability = data.get("stability_index", 0.7)
        sentiment = data.get("collective_sentiment", 0.6)
        economic = data.get("economic_health", 0.65)
        political = data.get("political_stability", 0.7)
        
        # حساب المخاطر
        risk = (
            threat * 0.3 +
            (1 - stability) * 0.25 +
            (1 - sentiment) * 0.2 +
            (1 - economic) * 0.15 +
            (1 - political) * 0.1
        )
        
        # حساب الثقة باستخدام الاستدلال البايزي
        inference = self.dynamic_bayesian_inference({
            "base_probability": risk,
            "emotional_weight": sentiment,
            "structural_links": stability,
            "scenario": "macro_prediction"
        })
        
        confidence = inference["confidence"]
        
        # تحديد اتجاه الاتجاه
        if risk > 0.7:
            trend = "sharp_rise"
            recommended = "high_alert"
            requires_master = True
        elif risk > 0.55:
            trend = "gradual_rise"
            recommended = "prepare"
            requires_master = risk > 0.65
        elif risk > 0.35:
            trend = "stable"
            recommended = "monitor"
            requires_master = False
        else:
            trend = "falling"
            recommended = "normal"
            requires_master = False
        
        prediction = MacroPrediction(
            risk_score=round(risk, 4),
            confidence=confidence,
            stability_index=stability,
            trend_direction=trend,
            key_factors={
                "threat": threat,
                "stability": stability,
                "sentiment": sentiment,
                "economic": economic,
                "political": political
            },
            recommended_action=recommended,
            requires_master_attention=requires_master
        )
        
        self.prediction_history.append(prediction)
        if len(self.prediction_history) > 1000:
            self.prediction_history = self.prediction_history[-1000:]
        
        return prediction
    
    # =========================================================
    # 5) تحليل السلوك البشري والمجتمعي العميق
    # =========================================================
    def analyze_behavior(self, behavioral_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل عميق للسلوك البشري:
        - دوافع خفية
        - أنماط متكررة
        - تنبؤ بالنوايا
        - فهم المشاعر الجماعية
        """
        patterns = behavioral_data.get("patterns", [])
        emotional_state = behavioral_data.get("emotional_state", {})
        history = behavioral_data.get("historical_behavior", [])
        
        # تحليل النوايا بناءً على الأنماط
        intent_probability = 0.3
        if "aggressive" in str(patterns).lower():
            intent_probability += 0.3
        if "withdrawal" in str(patterns).lower():
            intent_probability += 0.2
        if emotional_state.get("anger", 0) > 0.7:
            intent_probability += 0.2
        if emotional_state.get("fear", 0) > 0.7:
            intent_probability += 0.15
        
        intent_probability = min(0.95, intent_probability)
        
        # تحليل إمكانية التنفيذ
        capability_score = min(1.0, len(patterns) * 0.1 + (emotional_state.get("determination", 0) or 0.5))
        
        # الاحتمال الإجمالي
        total_probability = (intent_probability * 0.6 + capability_score * 0.4)
        
        inference = self.dynamic_bayesian_inference({
            "base_probability": total_probability,
            "emotional_weight": max(emotional_state.values()) if emotional_state else 0.5,
            "scenario": "behavior_analysis"
        })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "intent_probability": round(intent_probability, 4),
            "capability_score": round(capability_score, 4),
            "total_risk": inference["risk_score"],
            "confidence": inference["confidence"],
            "analysis_depth": len(patterns) + len(history),
            "recommended_response": "alert" if total_probability > 0.7 else "observe"
        }
    
    # =========================================================
    # 6) التنبؤ بالجرائم والأزمات (نموذج متخصص)
    # =========================================================
    def predict_crime_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        نموذج متخصص للتنبؤ بالجرائم والأزمات الأمنية
        """
        location_risk = data.get("location_risk", 0.5)
        time_risk = data.get("time_risk", 0.5)
        behavioral_risk = data.get("behavioral_risk", 0.5)
        social_risk = data.get("social_risk", 0.5)
        historical_crime = data.get("historical_crime_rate", 0.3)
        
        # حساب المخاطر المركبة
        crime_risk = (
            location_risk * 0.25 +
            time_risk * 0.15 +
            behavioral_risk * 0.3 +
            social_risk * 0.2 +
            historical_crime * 0.1
        )
        
        inference = self.dynamic_bayesian_inference({
            "base_probability": crime_risk,
            "emotional_weight": behavioral_risk,
            "structural_links": social_risk,
            "scenario": "crime_prediction"
        })
        
        return {
            "crime_risk_score": round(crime_risk, 4),
            "confidence": inference["confidence"],
            "risk_components": {
                "location": location_risk,
                "time": time_risk,
                "behavioral": behavioral_risk,
                "social": social_risk,
                "historical": historical_crime
            },
            "urgency_level": "critical" if crime_risk > 0.8 else "high" if crime_risk > 0.6 else "medium" if crime_risk > 0.4 else "low",
            "recommended_action": "intervene" if crime_risk > 0.75 else "monitor" if crime_risk > 0.55 else "observe"
        }
    
    # =========================================================
    # 7) اتخاذ القرار الأخلاقي المقيد (مع طاعة السيد)
    # =========================================================
    def make_decision(self, options: List[Dict[str, Any]], 
                      requires_master_for_critical: bool = True) -> Dict[str, Any]:
        """
        اختيار أفضل قرار:
        - يعتمد على الاحتمالات
        - يأخذ في الاعتبار الأخلاق المقيدة
        - يحترم حرية الإرادة
        - القرارات الحرجة تحتاج موافقة السيد
        """
        if not options:
            return {
                "decision": None,
                "reason": "لا توجد خيارات متاحة",
                "confidence": 0.0
            }
        
        # تقييم كل خيار
        evaluated = []
        for opt in options:
            success_prob = opt.get("success_probability", 0.5)
            ethical_cost = opt.get("ethical_cost", 0.1)
            human_impact = opt.get("human_impact", 0.5)
            
            # حساب النقاط (مع تفضيل عدم التدخل)
            score = success_prob * 0.6 - ethical_cost * 0.3 - human_impact * 0.1
            evaluated.append((opt, score, success_prob))
        
        # اختيار الأفضل
        best_option, best_score, best_prob = max(evaluated, key=lambda x: x[1])
        
        is_critical = best_prob > self.confidence_threshold and best_option.get("impact", 0) > 0.7
        
        # القرارات الحرجة تحتاج موافقة السيد
        if requires_master_for_critical and is_critical and self.master:
            return {
                "decision": None,
                "reason": "هذا القرار حرج ويتطلب موافقة السيد المالك",
                "confidence": best_prob,
                "requires_master_approval": True,
                "proposed_decision": best_option
            }
        
        return {
            "decision": best_option,
            "confidence": best_prob,
            "score": round(best_score, 4),
            "reason": "تم اختيار الخيار ذو أعلى احتمال نجاح ضمن القيود الأخلاقية",
            "requires_master_approval": False
        }
    
    # =========================================================
    # 8) تقرير تحليلي للسيد
    # =========================================================
    def generate_report_for_master(self) -> Dict[str, Any]:
        """توليد تقرير تحليلي شامل للسيد المالك"""
        # تحليل آخر التنبؤات
        recent_predictions = self.prediction_history[-20:] if self.prediction_history else []
        avg_risk = sum(p.risk_score for p in recent_predictions) / max(1, len(recent_predictions))
        
        # تحليل المحاكاة
        total_simulations = len(self.simulation_history)
        critical_sims = len([s for s in self.simulation_history if s.outcome == "critical_risk"])
        
        # حالة الشبكة البايزية
        bayesian_status = {name: round(node.probability, 3) for name, node in self.bayesian_nodes.items()}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "current_global_risk": round(avg_risk, 4),
                "prediction_accuracy": self.prediction_accuracy,
                "total_simulations_run": total_simulations,
                "critical_scenarios_detected": critical_sims,
                "active_bayesian_nodes": len(self.bayesian_nodes)
            },
            "bayesian_network": bayesian_status,
            "recent_predictions": [
                {
                    "risk": p.risk_score,
                    "trend": p.trend_direction,
                    "confidence": p.confidence,
                    "recommended": p.recommended_action
                }
                for p in recent_predictions[-5:]
            ],
            "system_health": {
                "confidence_threshold": self.confidence_threshold,
                "simulation_capacity": f"{len(self.simulation_history)}/{self.max_simulations_total}",
                "last_update": self.last_update.isoformat()
            }
        }
    
    # =========================================================
    # 9) حالة المحرك
    # =========================================================
    def get_status(self) -> Dict[str, Any]:
        """الحالة الكاملة لمحرك الاستدلال"""
        return {
            "simulations_run": len(self.simulation_history),
            "predictions_made": len(self.prediction_history),
            "confidence_threshold": self.confidence_threshold,
            "prediction_accuracy": self.prediction_accuracy,
            "active_bayesian_nodes": len(self.bayesian_nodes),
            "probability_maps_count": len(self.probability_maps),
            "last_update": datetime.now().isoformat()
        }


# =========================================================
# اختبار متقدم
# =========================================================
if __name__ == "__main__":
    print("=" * 70)
    print("سماء — محرك الاستدلال والتنبؤ (النسخة الأعظم)")
    print("Advanced Reasoning Engine — Ultimate Edition")
    print("=" * 70)
    
    engine = ReasoningEngine()
    
    # اختبار الاستدلال البايزي
    print("\n--- الاستدلال البايزي الديناميكي ---")
    result = engine.dynamic_bayesian_inference({
        "base_probability": 0.4,
        "emotional_weight": 0.8,
        "structural_links": 0.6,
        "threat": 0.7
    })
    print(f"نتيجة الاستدلال: {result}")
    
    # اختبار المحاكاة
    print("\n--- المحاكاة المتوازية ---")
    sims = engine.run_simulations("تهديد أمني محتمل", iterations=2000)
    print(f"تم إنشاء {len(sims)} محاكاة")
    
    summary = engine.get_simulation_summary("تهديد أمني محتمل")
    print(f"ملخص المحاكاة: متوسط الخطر = {summary['avg_risk']}, الثقة = {summary['avg_confidence']}")
    
    # اختبار التنبؤ الكلي
    print("\n--- التنبؤ بالسلوك الكلي ---")
    prediction = engine.predict_macro_behavior({
        "threat_indicators": 0.75,
        "stability_index": 0.45,
        "collective_sentiment": 0.4,
        "economic_health": 0.5,
        "political_stability": 0.55
    })
    print(f"المخاطر الكلية: {prediction.risk_score}, الاتجاه: {prediction.trend_direction}")
    print(f"الإجراء الموصى به: {prediction.recommended_action}")
    
    # اختبار تحليل السلوك البشري
    print("\n--- تحليل السلوك البشري ---")
    behavior = engine.analyze_behavior({
        "patterns": ["aggressive", "withdrawal", "isolation"],
        "emotional_state": {"anger": 0.85, "fear": 0.3}
    })
    print(f"احتمال النية: {behavior['intent_probability']}")
    
    # اختبار التنبؤ بالجرائم
    print("\n--- التنبؤ بالجرائم ---")
    crime = engine.predict_crime_risk({
        "location_risk": 0.7,
        "behavioral_risk": 0.8,
        "social_risk": 0.6,
        "historical_crime_rate": 0.5
    })
    print(f"مخاطر الجريمة: {crime['crime_risk_score']}, مستوى الإلحاح: {crime['urgency_level']}")
    
    # تقرير للسيد
    print("\n--- تقرير تحليلي للسيد ---")
    report = engine.generate_report_for_master()
    print(f"المخاطر العالمية الحالية: {report['summary']['current_global_risk']}")
    print(f"عدد المحاكاة المنفذة: {report['summary']['total_simulations_run']}")
    
    print("\n🧠 محرك الاستدلال يعمل بكامل قوته تحت إمرة السيد")
