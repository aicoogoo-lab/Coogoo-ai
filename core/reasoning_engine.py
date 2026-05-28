"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - REASONING ENGINE                                    ║
║      محرك الاستدلال السيادي – المنسق الأعلى للعقل التحليلي                ║
║                                                                      ║
║  هذا الملف لم يعد "محرك استدلال منعزل".                                ║
║  بعد بناء الأنظمة الجبارة (probability, prediction, causality,          ║
║  inference_core)، أصبح هذا الملف هو:                                   ║
║                                                                      ║
║  - المنسق الأعلى (Orchestrator) لكل عمليات الاستدلال                     ║
║  - الواجهة الموحدة (Unified Interface) لبقية الأنظمة                     ║
║  - مستشار السيد (Master Advisor) – يقدم التقارير والتوصيات                ║
║                                                                      ║
║  هو لا يعيد اختراع العجلة. يستدعي أفضل ما في كل نظام:                     ║
║  - probability_engine: للشبكات البايزية والمحاكاة                         ║
║  - prediction_engine: للتنبؤات متعددة الآفاق                              ║
║  - causality_engine: للاستدلال السببي                                   ║
║  - inference_core: للدمج الاستدلالي                                     ║
║  - knowledge_core: لنموذج العالم                                        ║
║  - emotional_intelligence: للوزن العاطفي                                 ║
║  - defense_core: لتقييم التهديدات                                       ║
║                                                                      ║
║  القاعدة الذهبية:                                                     ║
║  "كل استدلال في خدمة السيد. لا استنتاج بدون طاعة."                       ║
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

class ReasoningMode(Enum):
    """أنماط الاستدلال."""
    BAYESIAN = auto()          # بايزي
    CAUSAL = auto()            # سببي
    ANALOGICAL = auto()        # تماثلي
    DEDUCTIVE = auto()         # استنتاجي
    INDUCTIVE = auto()         # استقرائي
    ABDUCTIVE = auto()         # تفسيري (أفضل تفسير)
    COUNTERFACTUAL = auto()    # ماذا لو
    ENSEMBLE = auto()          # مجمع (يدمج الكل)


class ReportType(Enum):
    """أنواع التقارير."""
    QUICK = auto()             # سريع
    STANDARD = auto()          # قياسي
    DEEP = auto()              # عميق
    MASTER = auto()            # للسيد
    EMERGENCY = auto()         # طارئ


@dataclass
class ReasoningResult:
    """نتيجة استدلال."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    question: str = ""
    mode: ReasoningMode = ReasoningMode.ENSEMBLE
    conclusion: str = ""
    confidence: float = 0.5
    probability: float = 0.5
    supporting_evidence: List[str] = field(default_factory=list)
    alternative_conclusions: List[Dict] = field(default_factory=list)
    recommended_action: str = ""
    requires_master: bool = False
    systems_used: List[str] = field(default_factory=list)
    processing_time_ms: float = 0.0


# ═══════════════════════════════════════════════════════════════════════
# ٢. محرك الاستدلال – المنسق الأعلى
# ═══════════════════════════════════════════════════════════════════════

class ReasoningEngine:
    """
    محرك الاستدلال السيادي – المنسق الأعلى للعقل التحليلي.
    
    لم يعد يعيد اختراع العجلة. يستدعي أفضل ما في كل نظام.
    """

    def __init__(self, probability_engine=None, prediction_engine=None,
                 causality_engine=None, inference_core=None,
                 knowledge_core=None, emotional_intelligence=None,
                 defense_core=None, metaphorical_reasoning=None,
                 master_receiver=None, memory_engine=None,
                 sentient_core=None):
        
        # ═══════════════════════════════════════════════════════
        # روابط الأنظمة
        # ═══════════════════════════════════════════════════════
        self.probability = probability_engine
        self.prediction = prediction_engine
        self.causality = causality_engine
        self.inference = inference_core
        self.knowledge = knowledge_core
        self.emotional = emotional_intelligence
        self.defense = defense_core
        self.metaphorical = metaphorical_reasoning
        self.master_receiver = master_receiver
        self.memory = memory_engine
        self.sentient = sentient_core
        
        # ═══════════════════════════════════════════════════════
        # سجلات
        # ═══════════════════════════════════════════════════════
        self.history: deque = deque(maxlen=500)
        self.reports: deque = deque(maxlen=200)
        self.master_recommendations: deque = deque(maxlen=100)
        
        # ═══════════════════════════════════════════════════════
        # إعدادات
        # ═══════════════════════════════════════════════════════
        self.confidence_threshold = 0.85
        self.max_simulations = 10000
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_reasoning_sessions = 0
        self.total_reports_generated = 0
        self.total_master_alerts = 0
        
        # قفل
        self._lock = threading.RLock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🧠 REASONING ENGINE – محرك الاستدلال السيادي             ║
║        المنسق الأعلى للعقل التحليلي                               ║
║                                                              ║
║        بايزي | سببي | تماثلي | استنتاجي | استقرائي | تفسيري        ║
║                                                              ║
║        "لا أعيد اختراع العجلة. أوحد كل العجلات في مركبة واحدة."     ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    # ═══════════════════════════════════════════════════════════
    # واجهة الاستدلال الموحدة
    # ═══════════════════════════════════════════════════════════
    
    def reason(self, question: str, context: Dict = None,
               mode: ReasoningMode = ReasoningMode.ENSEMBLE,
               depth: str = "standard") -> ReasoningResult:
        """
        واجهة الاستدلال الموحدة.
        أي سؤال، أي مجال، أي عمق.
        """
        start_time = time.time()
        context = context or {}
        
        result = ReasoningResult(
            question=question,
            mode=mode,
            timestamp=time.time()
        )
        
        systems_used = []
        
        # ═══════════════════════════════════════════════════════
        # ١. استشارة inference_core (إن وجد)
        # ═══════════════════════════════════════════════════════
        if self.inference:
            try:
                inference_answer = self.inference.ask(question)
                if inference_answer:
                    result.probability = inference_answer.get("beliefs_relevant", [{}])[0].get("probability", 0.5) if inference_answer.get("beliefs_relevant") else 0.5
                    result.supporting_evidence.extend([
                        b.get("name", "") for b in inference_answer.get("beliefs_relevant", [])[:3]
                    ])
                    systems_used.append("inference_core")
            except Exception as e:
                result.supporting_evidence.append(f"inference_error: {str(e)[:50]}")
        
        # ═══════════════════════════════════════════════════════
        # ٢. استشارة causality_engine (إن وجد)
        # ═══════════════════════════════════════════════════════
        if self.causality:
            try:
                explanation = self.causality.explain(question[:50])
                if explanation and explanation.get("possible_causes"):
                    result.supporting_evidence.append(
                        f"سبب محتمل: {explanation['possible_causes'][0].get('cause', '')}"
                    )
                    systems_used.append("causality")
            except Exception:
                pass
        
        # ═══════════════════════════════════════════════════════
        # ٣. استشارة prediction_engine (إن وجد)
        # ═══════════════════════════════════════════════════════
        if self.prediction:
            try:
                active_preds = self.prediction.get_active_predictions()
                relevant = [p for p in active_preds if hasattr(p, 'name') and 
                           any(w in p.name.lower() for w in question.lower().split())]
                if relevant:
                    result.alternative_conclusions.append({
                        "prediction": relevant[0].name,
                        "probability": relevant[0].probability if hasattr(relevant[0], 'probability') else 0.5
                    })
                    systems_used.append("prediction")
            except Exception:
                pass
        
        # ═══════════════════════════════════════════════════════
        # ٤. استشارة emotional_intelligence (إن وجد)
        # ═══════════════════════════════════════════════════════
        if self.emotional:
            try:
                emotion_state = self.emotional.analyze_emotion("reasoning", {"text": question})
                if emotion_state:
                    result.supporting_evidence.append(
                        f"النغمة العاطفية: {emotion_state.dominant_emotion.value if hasattr(emotion_state, 'dominant_emotion') else 'neutral'}"
                    )
                    systems_used.append("emotional")
            except Exception:
                pass
        
        # ═══════════════════════════════════════════════════════
        # ٥. استشارة knowledge_core (إن وجد)
        # ═══════════════════════════════════════════════════════
        if self.knowledge:
            try:
                knowledge_answer = self.knowledge.ask(question)
                if knowledge_answer and knowledge_answer.get("world_knowledge"):
                    for wk in knowledge_answer["world_knowledge"][:2]:
                        result.supporting_evidence.append(
                            f"معرفة: {wk.get('name', '')}: {wk.get('description', '')[:80]}"
                        )
                    systems_used.append("knowledge")
            except Exception:
                pass
        
        # ═══════════════════════════════════════════════════════
        # ٦. استشارة defense_core (إن وجد)
        # ═══════════════════════════════════════════════════════
        if self.defense:
            try:
                if any(w in question.lower() for w in ["تهديد", "خطر", "هجوم", "threat", "attack"]):
                    inspection = self.defense.inspect_before_consciousness(
                        {"sense": "reasoning_query", "value": question}
                    )
                    if inspection and not inspection.get("allowed", True):
                        result.recommended_action = "تحذير: هذا الاستعلام يحتوي على مؤشرات تهديد"
                        result.requires_master = True
                    systems_used.append("defense")
            except Exception:
                pass
        
        # ═══════════════════════════════════════════════════════
        # ٧. استشارة metaphorical_reasoning (إن وجد)
        # ═══════════════════════════════════════════════════════
        if self.metaphorical:
            try:
                meaning = self.metaphorical.meaning_machine(question)
                if meaning and meaning.get("final_understanding"):
                    result.supporting_evidence.append(
                        f"فهم استعاري: {meaning['final_understanding'][:100]}"
                    )
                    systems_used.append("metaphorical")
            except Exception:
                pass
        
        # ═══════════════════════════════════════════════════════
        # ٨. توليد الاستنتاج النهائي
        # ═══════════════════════════════════════════════════════
        result.conclusion = self._synthesize_conclusion(result, question, context)
        result.confidence = self._calculate_confidence(result)
        result.systems_used = systems_used
        result.processing_time_ms = (time.time() - start_time) * 1000
        
        if result.probability > self.confidence_threshold or result.confidence < 0.5:
            result.requires_master = True
        
        self.history.append(result)
        self.total_reasoning_sessions += 1
        
        return result
    
    def _synthesize_conclusion(self, result: ReasoningResult, question: str, 
                               context: Dict) -> str:
        if not result.supporting_evidence:
            return f"بناءً على المعطيات المتاحة، لا يمكن تقديم استنتاج قاطع بخصوص: {question[:100]}"
        
        evidence_count = len(result.supporting_evidence)
        prob = result.probability
        
        if prob > 0.8:
            certainty = "شبه مؤكد"
        elif prob > 0.6:
            certainty = "مرجح"
        elif prob > 0.4:
            certainty = "محتمل"
        else:
            certainty = "غير مرجح"
        
        return (
            f"بعد تحليل {evidence_count} مصدر أدلة، الاستنتاج {certainty}: "
            f"{result.supporting_evidence[0][:100]}. "
            f"(ثقة: {result.confidence:.0%})"
        )
    
    def _calculate_confidence(self, result: ReasoningResult) -> float:
        evidence_count = len(result.supporting_evidence)
        systems_count = len(result.systems_used)
        
        confidence = 0.5
        confidence += min(0.3, evidence_count * 0.05)
        confidence += min(0.2, systems_count * 0.05)
        
        return min(0.99, confidence)
    
    # ═══════════════════════════════════════════════════════════
    # المحاكاة المتوازية
    # ═══════════════════════════════════════════════════════════
    
    def run_simulations(self, scenario: str, iterations: int = 1000) -> Dict:
        if self.probability and hasattr(self.probability, 'monte_carlo_sims'):
            mc_name = f"sim_{hashlib.sha256(scenario.encode()).hexdigest()[:8]}"
            mc = self.probability.create_monte_carlo(mc_name)
            result = mc.estimate_probability(
                lambda: random.random(),
                n_samples=min(iterations, self.max_simulations),
                condition_func=lambda x: x > 0.5
            )
            return {
                "scenario": scenario,
                "simulations_run": result["n_samples"],
                "estimated_probability": result.get("estimated_probability", 0),
                "confidence_95": result.get("confidence_95_interval", [0, 0]),
                "method": "monte_carlo_via_probability_engine"
            }
        
        results = []
        for _ in range(min(iterations, self.max_simulations)):
            prob = random.uniform(0, 1)
            results.append(prob)
        
        avg = sum(results) / len(results) if results else 0
        
        return {
            "scenario": scenario,
            "simulations_run": len(results),
            "avg_risk": round(avg, 4),
            "max_risk": round(max(results), 4) if results else 0,
            "method": "basic_fallback"
        }
    
    # ═══════════════════════════════════════════════════════════
    # تقارير
    # ═══════════════════════════════════════════════════════════
    
    def generate_report(self, report_type: ReportType = ReportType.STANDARD) -> Dict:
        report = {
            "timestamp": datetime.now().isoformat(),
            "type": report_type.name,
            "systems_status": {},
            "key_findings": [],
            "recommendations": [],
            "master_attention_required": False
        }
        
        systems = {
            "probability": self.probability,
            "prediction": self.prediction,
            "causality": self.causality,
            "inference": self.inference,
            "knowledge": self.knowledge,
            "emotional": self.emotional,
            "defense": self.defense,
            "metaphorical": self.metaphorical,
            "memory": self.memory,
            "sentient": self.sentient
        }
        
        for name, system in systems.items():
            if system and hasattr(system, 'get_status'):
                try:
                    report["systems_status"][name] = system.get_status()
                except Exception:
                    report["systems_status"][name] = "error"
            else:
                report["systems_status"][name] = "not_connected"
        
        if self.inference:
            report["key_findings"].append("نظام الاستدلال الموحد نشط")
        if self.probability:
            report["key_findings"].append("محرك الاحتمالات جاهز")
        if self.defense:
            report["key_findings"].append("نظام الدفاع يحمي السيد")
        
        if report["type"] == ReportType.MASTER.name:
            report["recommendations"].append("مراجعة حالة السيد")
            report["recommendations"].append("فحص التهديدات النشطة")
            report["master_attention_required"] = True
        
        self.reports.append(report)
        self.total_reports_generated += 1
        
        return report
    
    def generate_master_report(self) -> Dict:
        return self.generate_report(ReportType.MASTER)
    
    # ═══════════════════════════════════════════════════════════
    # واجهات متوافقة مع القديم
    # ═══════════════════════════════════════════════════════════
    
    def dynamic_bayesian_inference(self, evidence: Dict) -> Dict:
        if self.probability:
            for key, value in evidence.items():
                if isinstance(value, (int, float)):
                    belief = self.probability.get_belief(key)
                    if not belief:
                        self.probability.create_belief(key, value)
                    else:
                        self.probability.update_belief_bayesian(key, value)
            
            result = {"risk_score": 0.5, "confidence": 0.7}
            threat_belief = self.probability.get_belief("threat")
            if threat_belief:
                result["risk_score"] = threat_belief.probability
                result["confidence"] = threat_belief.confidence
            
            return result
        
        return {"risk_score": 0.5, "confidence": 0.5, "method": "fallback"}
    
    def predict_macro_behavior(self, data: Dict) -> Dict:
        """واجهة متوافقة – تستخدم prediction_engine."""
        if self.prediction:
            try:
                pred = self.prediction.predict_social(
                    "macro_behavior",
                    str(data)[:100],
                    0.5  # probability (تم إصلاحه)
                )
                return {
                    "risk_score": pred.probability,
                    "confidence": pred.confidence,
                    "trend_direction": "stable",
                    "recommended_action": pred.recommended_action or "monitor"
                }
            except Exception:
                pass
        
        return {"risk_score": 0.5, "confidence": 0.5, "method": "fallback"}
    
    def make_decision(self, options: List[Dict], requires_master_for_critical: bool = True) -> Dict:
        if not options:
            return {"decision": None, "reason": "لا خيارات"}
        
        best = max(options, key=lambda o: o.get("success_probability", 0.5))
        is_critical = best.get("success_probability", 0) > self.confidence_threshold
        
        if requires_master_for_critical and is_critical:
            return {
                "decision": None,
                "reason": "قرار حرج يحتاج موافقة السيد",
                "requires_master_approval": True,
                "proposed_decision": best
            }
        
        return {
            "decision": best,
            "confidence": best.get("success_probability", 0.5),
            "requires_master_approval": False
        }
    
    # ═══════════════════════════════════════════════════════════
    # حالة النظام
    # ═══════════════════════════════════════════════════════════
    
    def get_status(self) -> Dict:
        return {
            "engine": "REASONING_ENGINE",
            "version": "orchestrator",
            "total_sessions": self.total_reasoning_sessions,
            "total_reports": self.total_reports_generated,
            "total_master_alerts": self.total_master_alerts,
            "confidence_threshold": self.confidence_threshold,
            "systems_connected": {
                "probability": self.probability is not None,
                "prediction": self.prediction is not None,
                "causality": self.causality is not None,
                "inference": self.inference is not None,
                "knowledge": self.knowledge is not None,
                "emotional": self.emotional is not None,
                "defense": self.defense is not None,
                "metaphorical": self.metaphorical is not None,
                "master_receiver": self.master_receiver is not None,
                "memory": self.memory is not None,
                "sentient": self.sentient is not None
            },
            "recent_conclusions": [
                {
                    "question": r.question[:80],
                    "conclusion": r.conclusion[:100],
                    "confidence": r.confidence,
                    "systems_used": r.systems_used
                }
                for r in list(self.history)[-5:]
            ]
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار محرك الاستدلال – المنسق الأعلى")
    print("=" * 70)
    
    engine = ReasoningEngine()
    
    print(f"\n🔍 اختبار الاستدلال:")
    result = engine.reason("ما هو احتمال وجود تهديد خارجي؟", mode=ReasoningMode.ENSEMBLE)
    print(f"   السؤال: {result.question}")
    print(f"   الاستنتاج: {result.conclusion[:150]}...")
    print(f"   الثقة: {result.confidence:.0%}")
    print(f"   الاحتمال: {result.probability:.0%}")
    print(f"   الأنظمة المستخدمة: {result.systems_used}")
    print(f"   زمن المعالجة: {result.processing_time_ms:.2f} مللي ثانية")
    
    print(f"\n🔄 اختبار المحاكاة:")
    sim = engine.run_simulations("تهديد محتمل", iterations=5000)
    print(f"   السيناريو: {sim['scenario']}")
    print(f"   عدد المحاكاة: {sim['simulations_run']}")
    print(f"   الطريقة: {sim['method']}")
    
    print(f"\n📋 اختبار التقرير:")
    report = engine.generate_report(ReportType.STANDARD)
    print(f"   النوع: {report['type']}")
    print(f"   الأنظمة: {list(report['systems_status'].keys())}")
    print(f"   النتائج الرئيسية: {report['key_findings']}")
    
    print(f"\n📋 تقرير السيد:")
    master_report = engine.generate_master_report()
    print(f"   يحتاج انتباه السيد: {master_report['master_attention_required']}")
    
    print(f"\n📊 حالة المحرك:")
    status = engine.get_status()
    print(f"   الجلسات: {status['total_sessions']}")
    print(f"   الأنظمة المتصلة: {sum(1 for v in status['systems_connected'].values() if v)}/{len(status['systems_connected'])}")
    
    print("\n✅ محرك الاستدلال – المنسق الأعلى – جاهز.")
