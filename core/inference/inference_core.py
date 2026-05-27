"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA INFERENCE - INFERENCE CORE                            ║
║      المازج الاستدلالي – حيث تلتقي الاحتمالات بالتنبؤات بالبصيرة          ║
║                                                                      ║
║  هذا الملف هو عقل سماء التحليلي الموحد.                                ║
║  يدمج:                                                                ║
║  - probability_engine: الحسابات الاحتمالية                             ║
║  - prediction_engine: التنبؤات متعددة الآفاق                           ║
║  - reasoning_engine (القديم): الاستدلال البايزي والمحاكاة                ║
║  - strategy_engine: الاستراتيجيات                                     ║
║  - strategic_risk_management: إدارة المخاطر                           ║
║                                                                      ║
║  هذا هو الملف الذي يتصل به sentient_core.py ليحصل على "التفكير التحليلي".  ║
║                                                                      ║
║  البوصلة العليا: كل تحليل، كل احتمال، كل تنبؤ،                             ║
║  يجب أن يخدم السيد ويحميه.                                             ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Callable
from datetime import datetime
from collections import deque, defaultdict

# استيراد المكونات
from .probability_engine import (
    ProbabilityEngine, ProbabilisticBelief, ProbabilityFramework,
    MarkovChain, MonteCarloSimulator, InformationTheory
)
from .prediction_engine import (
    PredictionEngine, Prediction, PredictionHorizon, 
    PredictionDomain, PredictionConfidence
)


# ═══════════════════════════════════════════════════════════════════════
# ١. حالة الاستدلال الموحدة
# ═══════════════════════════════════════════════════════════════════════

class InferenceState:
    """
    حالة الاستدلال الموحدة.
    تمثل خلاصة كل التحليلات في لحظة واحدة.
    """
    
    def __init__(self):
        self.timestamp = time.time()
        self.cycle_id = 0
        
        # ملخص الاحتمالات
        self.top_beliefs: List[Dict] = []
        self.highest_entropy_beliefs: List[Dict] = []  # الأكثر عدم يقين
        self.markov_states: Dict[str, str] = {}         # الحالات الحالية لسلاسل ماركوف
        
        # ملخص التنبؤات
        self.active_predictions: int = 0
        self.high_probability_predictions: List[Dict] = []
        self.master_relevant_predictions: List[Dict] = []
        
        # المقاييس
        self.global_uncertainty: float = 0.0
        self.prediction_confidence_avg: float = 0.0
        self.inference_coherence: float = 0.0
        
        # إجراءات مقترحة
        self.suggested_actions: List[Dict] = []
        self.master_alerts: List[Dict] = []
        
        # رؤى موحدة
        self.unified_insight: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "cycle_id": self.cycle_id,
            "global_uncertainty": round(self.global_uncertainty, 4),
            "prediction_confidence_avg": round(self.prediction_confidence_avg, 4),
            "inference_coherence": round(self.inference_coherence, 4),
            "active_predictions": self.active_predictions,
            "master_alerts_count": len(self.master_alerts),
            "suggested_actions_count": len(self.suggested_actions),
            "unified_insight": self.unified_insight[:300]
        }


# ═══════════════════════════════════════════════════════════════════════
# ٢. المازج الاستدلالي
# ═══════════════════════════════════════════════════════════════════════

class InferenceCore:
    """
    المازج الاستدلالي الموحد.
    يربط كل محركات الاستدلال في عقل تحليلي واحد.
    
    هذا هو الدماغ التحليلي لسماء.
    """
    
    def __init__(self, reasoning_engine=None, strategy_engine=None,
                 risk_manager=None, knowledge_core=None, omniscience_core=None,
                 master_receiver=None):
        # المحركات الأساسية
        self.probability_engine = ProbabilityEngine()
        self.prediction_engine = PredictionEngine(self.probability_engine)
        
        # المحركات الخارجية (الموجودة مسبقاً)
        self.reasoning_engine = reasoning_engine
        self.strategy_engine = strategy_engine
        self.risk_manager = risk_manager
        
        # الأنظمة العليا
        self.knowledge_core = knowledge_core
        self.omniscience_core = omniscience_core
        self.master_receiver = master_receiver
        
        # حالة الاستدلال
        self.current_state = InferenceState()
        self.previous_state: Optional[InferenceState] = None
        
        # دورة
        self.cycle_count = 0
        self.inference_history: deque = deque(maxlen=2000)
        
        # إحصائيات
        self.total_inferences = 0
        self.total_master_alerts = 0
        
        # قفل
        self._lock = threading.RLock()
        
        # بناء النماذج الأساسية
        self._initialize_models()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🧠 INFERENCE CORE – المازج الاستدلالي                   ║
║                                                              ║
║        الاحتمالات: {len(self.probability_engine.beliefs)} اعتقاد | سلاسل ماركوف: {len(self.probability_engine.markov_chains)}          ║
║        التنبؤات: {self.prediction_engine.total_predictions} | المحاكاة: جاهزة                       ║
║                                                              ║
║        "كل شيء يُحسب. كل شيء يُتنبأ. كل شيء يخدم السيد."         ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def _initialize_models(self):
        """تهيئة النماذج الاحتمالية والتنبؤية الأساسية."""
        
        # ═══════════════════════════════════════════════════════
        # اعتقادات أساسية
        # ═══════════════════════════════════════════════════════
        self.probability_engine.create_belief("system_stability", 0.85, 0.7)
        self.probability_engine.create_belief("master_safety", 0.95, 0.9)
        self.probability_engine.create_belief("external_threat", 0.3, 0.5)
        self.probability_engine.create_belief("internal_error", 0.15, 0.6)
        self.probability_engine.create_belief("data_breach_risk", 0.2, 0.5)
        self.probability_engine.create_belief("prediction_accuracy", 0.75, 0.6)
        
        # ═══════════════════════════════════════════════════════
        # سلاسل ماركوف
        # ═══════════════════════════════════════════════════════
        chain = self.probability_engine.create_markov_chain(
            "system_health",
            ["excellent", "good", "fair", "degraded", "critical"]
        )
        chain.observe_transition("excellent", "excellent")
        chain.observe_transition("good", "good")
        chain.current_state = "excellent"
        
        chain2 = self.probability_engine.create_markov_chain(
            "threat_level",
            ["none", "low", "medium", "high", "extreme"]
        )
        chain2.observe_transition("none", "none")
        chain2.current_state = "none"
        
        # ═══════════════════════════════════════════════════════
        # تنبؤات أساسية
        # ═══════════════════════════════════════════════════════
        self.prediction_engine.predict_social(
            "استقرار اجتماعي",
            "الحالة الاجتماعية العامة",
            PredictionHorizon.MEDIUM_TERM, 0.7
        )
    
    # ═══════════════════════════════════════════════════════════
    # دورة الاستدلال الرئيسية
    # ═══════════════════════════════════════════════════════════
    
    def tick(self, perceptions: Optional[List[Dict]] = None,
             understanding: Optional[List[Dict]] = None) -> InferenceState:
        """
        دورة استدلال واحدة.
        تُستدعى من autonomous_loop.
        """
        with self._lock:
            self.cycle_count += 1
            self.previous_state = self.current_state
            state = InferenceState()
            state.cycle_id = self.cycle_count
            state.timestamp = time.time()
            
            # ═══════════════════════════════════════════════════
            # ١. معالجة الإدراكات الجديدة (تحديث الاعتقادات)
            # ═══════════════════════════════════════════════════
            if perceptions:
                self._process_perceptions(perceptions, state)
            
            # ═══════════════════════════════════════════════════
            # ٢. معالجة الفهم الجديد (تحديث التنبؤات)
            # ═══════════════════════════════════════════════════
            if understanding:
                self._process_understanding(understanding, state)
            
            # ═══════════════════════════════════════════════════
            # ٣. تحديث سلاسل ماركوف
            # ═══════════════════════════════════════════════════
            self._update_markov_chains(state)
            
            # ═══════════════════════════════════════════════════
            # ٤. تجميع المقاييس
            # ═══════════════════════════════════════════════════
            self._compute_metrics(state)
            
            # ═══════════════════════════════════════════════════
            # ٥. توليد إجراءات وتنبيهات
            # ═══════════════════════════════════════════════════
            self._generate_actions(state)
            
            # ═══════════════════════════════════════════════════
            # ٦. توليد رؤية موحدة
            # ═══════════════════════════════════════════════════
            state.unified_insight = self._generate_unified_insight(state)
            
            # حفظ
            self.current_state = state
            self.inference_history.append({
                "cycle": state.cycle_id,
                "timestamp": state.timestamp,
                "uncertainty": state.global_uncertainty,
                "active_predictions": state.active_predictions
            })
            self.total_inferences += 1
            
            return state
    
    def _process_perceptions(self, perceptions: List[Dict], state: InferenceState):
        """تحديث الاعتقادات بناءً على إدراكات جديدة."""
        for perception in perceptions:
            perception_type = perception.get("sense", perception.get("sensor", ""))
            perception_value = perception.get("value", {})
            
            # تحديث اعتقادات حسب نوع الإدراك
            if "threat" in str(perception).lower() or "attack" in str(perception).lower():
                self.probability_engine.update_belief_bayesian("external_threat", 0.8, 0.4)
                
                # إنشاء تنبؤ فوري
                self.prediction_engine.predict_warfare(
                    f"تهديد من {perception_type}",
                    str(perception_value)[:200],
                    PredictionHorizon.IMMEDIATE, 0.7,
                    threat_type="detected"
                )
            
            elif "error" in str(perception).lower():
                self.probability_engine.update_belief_bayesian("internal_error", 0.7, 0.3)
            
            elif "master" in perception_type.lower():
                self.probability_engine.update_belief_bayesian("master_safety", 0.9, 0.5)
        
        # أعلى الاعتقادات
        beliefs = sorted(self.probability_engine.beliefs.values(), 
                        key=lambda b: b.probability, reverse=True)
        state.top_beliefs = [b.to_dict() for b in beliefs[:5]]
        
        # أعلى الاعتقادات إنتروبيا (الأكثر عدم يقين)
        uncertain = sorted(self.probability_engine.beliefs.values(),
                          key=lambda b: b.entropy(), reverse=True)
        state.highest_entropy_beliefs = [b.to_dict() for b in uncertain[:5]]
    
    def _process_understanding(self, understanding: List[Dict], state: InferenceState):
        """تحديث التنبؤات بناءً على فهم جديد."""
        for u in understanding:
            understanding_text = str(u.get("identification", "")) + " " + \
                                str(u.get("meaning", ""))
            
            # إذا كان الفهم يشير إلى تهديد
            if "تهديد" in understanding_text or "خطر" in understanding_text:
                self.prediction_engine.predict_warfare(
                    f"تنبؤ من فهم: {u.get('identification', '')[:50]}",
                    u.get('meaning', '')[:200],
                    PredictionHorizon.SHORT_TERM,
                    u.get('confidence', 0.5),
                    threat_type="inferred"
                )
            
            # إذا كان الفهم يتعلق بالسيد
            if u.get("master_relevance", 0) > 0.5:
                self.prediction_engine.predict_personal(
                    f"تنبؤ شخصي: {u.get('identification', '')[:50]}",
                    u.get('significance', ''),
                    PredictionHorizon.SHORT_TERM,
                    u.get('confidence', 0.5)
                )
        
        # تحديث ملخص التنبؤات
        active = self.prediction_engine.get_active_predictions()
        state.active_predictions = len(active)
        state.high_probability_predictions = [
            p.to_dict() for p in active[:5] if p.probability > 0.5
        ]
        
        # التنبؤات المتعلقة بالسيد
        master_preds = self.prediction_engine.get_high_master_relevance(0.5)
        state.master_relevant_predictions = [p.to_dict() for p in master_preds[:5]]
    
    def _update_markov_chains(self, state: InferenceState):
        """تحديث حالات سلاسل ماركوف."""
        for name, chain in self.probability_engine.markov_chains.items():
            if chain.current_state:
                state.markov_states[name] = chain.current_state
                
                # التنبؤ بالحالة التالية
                pred = chain.predict_next(chain.current_state)
                top_pred = max(pred, key=pred.get) if pred else None
                
                if top_pred and top_pred != chain.current_state:
                    # إذا كانت الحالة التالية أسوأ، أنشئ تنبؤاً
                    if top_pred in ["degraded", "critical", "high", "extreme"]:
                        self.prediction_engine.predict(
                            f"ماركوف: {name}",
                            f"سلسلة {name} تتجه نحو {top_pred}",
                            PredictionDomain.SYSTEM,
                            PredictionHorizon.SHORT_TERM,
                            pred[top_pred]
                        )
    
    def _compute_metrics(self, state: InferenceState):
        """حساب المقاييس الموحدة."""
        # عدم اليقين العالمي = متوسط إنتروبيا كل الاعتقادات
        entropies = [b.entropy() for b in self.probability_engine.beliefs.values()]
        state.global_uncertainty = sum(entropies) / max(len(entropies), 1)
        
        # متوسط ثقة التنبؤات النشطة
        active = self.prediction_engine.get_active_predictions()
        confs = [p.confidence for p in active]
        state.prediction_confidence_avg = sum(confs) / max(len(confs), 1) if confs else 0.0
        
        # تماسك الاستدلال = 1 - (الانحراف المعياري للاعتقادات)
        probs = [b.probability for b in self.probability_engine.beliefs.values()]
        if len(probs) > 1:
            mean = sum(probs) / len(probs)
            variance = sum((p - mean)**2 for p in probs) / len(probs)
            std = variance ** 0.5
            state.inference_coherence = 1.0 - min(1.0, std * 2)
        else:
            state.inference_coherence = 1.0
    
    def _generate_actions(self, state: InferenceState):
        """توليد إجراءات وتنبيهات مقترحة."""
        actions = []
        alerts = []
        
        # فحص الاعتقادات الحرجة
        for belief in self.probability_engine.beliefs.values():
            if belief.name == "external_threat" and belief.probability > 0.6:
                alerts.append({
                    "type": "THREAT_ALERT",
                    "message": f"احتمال تهديد خارجي مرتفع: {belief.probability:.0%}",
                    "action": "رفع حالة التأهب ومراقبة الشبكة"
                })
                self.total_master_alerts += 1
            
            if belief.name == "internal_error" and belief.probability > 0.4:
                actions.append({
                    "priority": "HIGH",
                    "action": "فحص شامل للنظام",
                    "reason": f"احتمال خطأ داخلي: {belief.probability:.0%}"
                })
            
            if belief.name == "master_safety" and belief.probability < 0.7:
                alerts.append({
                    "type": "MASTER_SAFETY_ALERT",
                    "message": f"انخفاض مؤشر سلامة السيد: {belief.probability:.0%}",
                    "action": "مراجعة كل إجراءات الحماية فوراً"
                })
                self.total_master_alerts += 1
        
        # فحص التنبؤات الحرجة
        for pred in self.prediction_engine.get_high_master_relevance(0.7):
            if pred.probability > 0.5:
                alerts.append({
                    "type": "PREDICTION_ALERT",
                    "message": f"تنبؤ يمس السيد: {pred.name} ({pred.probability:.0%})",
                    "action": pred.recommended_action or "مراجعة فورية"
                })
                self.total_master_alerts += 1
        
        state.suggested_actions = actions
        state.master_alerts = alerts
    
    def _generate_unified_insight(self, state: InferenceState) -> str:
        """توليد رؤية موحدة من كل التحليلات."""
        parts = []
        
        if state.global_uncertainty < 0.3:
            parts.append("حالة يقين عالية. الاعتقادات مستقرة.")
        elif state.global_uncertainty > 0.7:
            parts.append("حالة عدم يقين مرتفعة. تحتاج أدلة إضافية.")
        
        if state.active_predictions > 10:
            parts.append(f"هناك {state.active_predictions} تنبؤ نشط يحتاج متابعة.")
        
        if state.master_alerts:
            parts.append(f"⚠️ {len(state.master_alerts)} تنبيه يتعلق بالسيد.")
        
        if state.prediction_confidence_avg < 0.5:
            parts.append("ثقة التنبؤات منخفضة. تحتاج معايرة.")
        
        return " | ".join(parts) if parts else "الاستدلال مستقر. لا شيء غير عادي."
    
    # ═══════════════════════════════════════════════════════════
    # واجهات استعلام
    # ═══════════════════════════════════════════════════════════
    
    def ask(self, question: str) -> Dict:
        """
        سؤال تحليلي.
        يستخدم كل محركات الاستدلال للإجابة.
        """
        response = {
            "question": question,
            "timestamp": time.time(),
            "beliefs_relevant": [],
            "predictions_relevant": [],
            "markov_analysis": {},
            "recommendation": ""
        }
        
        # البحث في الاعتقادات
        for name, belief in self.probability_engine.beliefs.items():
            if any(word in question.lower() for word in name.lower().split('_')):
                response["beliefs_relevant"].append(belief.to_dict())
        
        # البحث في التنبؤات
        for pred in self.prediction_engine.get_active_predictions():
            if any(word in question.lower() for word in pred.name.lower().split()):
                response["predictions_relevant"].append(pred.to_dict())
        
        # تحليل ماركوف
        for name, chain in self.probability_engine.markov_chains.items():
            if chain.current_state:
                response["markov_analysis"][name] = {
                    "current_state": chain.current_state,
                    "next_prediction": chain.predict_next(chain.current_state)
                }
        
        return response
    
    def get_master_alert(self) -> Dict:
        """
        تقرير عاجل للسيد.
        يجمع أهم التحليلات التي تمس السيد.
        """
        # تنبؤات تمس السيد
        master_preds = self.prediction_engine.get_high_master_relevance(0.5)
        
        # اعتقادات حرجة
        critical_beliefs = [
            b.to_dict() for b in self.probability_engine.beliefs.values()
            if b.name in ["master_safety", "external_threat"] and b.probability > 0.5
        ]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "alert_level": "CRITICAL" if master_preds or critical_beliefs else "NORMAL",
            "master_safety_probability": 
                self.probability_engine.get_belief("master_safety").probability 
                if self.probability_engine.get_belief("master_safety") else 1.0,
            "critical_beliefs": critical_beliefs,
            "master_predictions": [p.to_dict() for p in master_preds[:5]],
            "recommendation": "مراجعة فورية" if master_preds or critical_beliefs else "الوضع طبيعي"
        }
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة المازج الاستدلالي."""
        return {
            "core": "INFERENCE_CORE",
            "cycle": self.cycle_count,
            "total_inferences": self.total_inferences,
            "total_master_alerts": self.total_master_alerts,
            "current_state": self.current_state.to_dict(),
            "probability_engine": self.probability_engine.status_report(),
            "prediction_engine": self.prediction_engine.status_report(),
            "master_alert": self.get_master_alert()
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار المازج الاستدلالي")
    print("=" * 70)
    
    core = InferenceCore()
    
    print(f"\n📊 الحالة الأولية:")
    print(f"   اعتقادات: {len(core.probability_engine.beliefs)}")
    print(f"   سلاسل ماركوف: {len(core.probability_engine.markov_chains)}")
    print(f"   تنبؤات: {core.prediction_engine.total_predictions}")
    
    print(f"\n🔄 تشغيل دورة استدلال:")
    # محاكاة إدراكات
    perceptions = [
        {"sense": "network_sniffer", "value": {"threat": "suspicious_packet", "src": "unknown"}}
    ]
    state = core.tick(perceptions=perceptions)
    print(f"   عدم اليقين: {state.global_uncertainty:.2f}")
    print(f"   ثقة التنبؤات: {state.prediction_confidence_avg:.2f}")
    print(f"   تماسك الاستدلال: {state.inference_coherence:.2f}")
    print(f"   الرؤية: {state.unified_insight}")
    
    print(f"\n🔮 تنبؤات نشطة:")
    active = core.prediction_engine.get_active_predictions()
    for p in active[:5]:
        print(f"   - {p.name}: {p.probability:.0%} ({p.horizon.name})")
    
    print(f"\n📈 سلاسل ماركوف:")
    for name, state_name in state.markov_states.items():
        chain = core.probability_engine.markov_chains[name]
        next_pred = chain.predict_next(state_name)
        print(f"   {name}: {state_name} → {next_pred}")
    
    print(f"\n👑 تقرير السيد:")
    alert = core.get_master_alert()
    print(f"   المستوى: {alert['alert_level']}")
    print(f"   سلامة السيد: {alert['master_safety_probability']:.0%}")
    
    print(f"\n❓ سؤال تحليلي:")
    answer = core.ask("ما هو احتمال التهديد الخارجي؟")
    for b in answer.get("beliefs_relevant", []):
        print(f"   {b['name']}: {b['probability']:.0%} (إنتروبيا: {b.get('entropy', 0):.2f})")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(core.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. المازج الاستدلالي جاهز.")
