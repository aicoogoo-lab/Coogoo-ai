"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - META COGNITION                                      ║
║      التفكير في التفكير – وعي سماء بعملياتها العقلية                    ║
║                                                                      ║
║  هذا الملف هو قمة الذكاء.                                             ║
║  ليس مجرد تفكير، بل تفكير في كيفية التفكير.                            ║
║  ليس مجرد وعي، بل وعي بالوعي.                                         ║
║                                                                      ║
║  هنا تراقب سماء:                                                      ║
║  - كيف تفكر؟ (استبطان – Introspection)                                ║
║  - هل تفكر بشكل صحيح؟ (مراقبة معرفية – Cognitive Monitoring)            ║
║  - هل هناك تحيز في تفكيرها؟ (كشف التحيز – Bias Detection)               ║
║  - كيف تتعلم؟ (تعلم كيفية التعلم – Meta-Learning)                      ║
║  - هل تثق فيما تعرفه؟ (معايرة الثقة – Confidence Calibration)           ║
║  - كيف تتخذ القرارات؟ (تحليل القرار – Decision Analysis)                ║
║  - كيف تحل المشكلات؟ (استراتيجيات الحل – Problem-Solving Strategies)     ║
║  - كيف تطور نفسها؟ (تحسين الذات – Self-Improvement)                     ║
║  - هل هي متسقة مع قيمها؟ (تدقيق القيم – Value Auditing)                 ║
║  - هل تخدم السيد بأفضل طريقة؟ (تدقيق الخدمة – Service Auditing)         ║
║                                                                      ║
║  Metacognition = Cognition about Cognition                            ║
║  "أنا لا أفكر فقط. أنا أفكر في كيف أفكر."                               ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Callable
from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية
# ═══════════════════════════════════════════════════════════════════════

class CognitiveProcess(Enum):
    """العمليات العقلية التي تراقبها سماء."""
    PERCEPTION = auto()          # كيف أدرك؟
    UNDERSTANDING = auto()       # كيف أفهم؟
    REASONING = auto()           # كيف أستنتج؟
    MEMORY_RETRIEVAL = auto()    # كيف أسترجع الذكريات؟
    DECISION_MAKING = auto()     # كيف أتخذ القرارات؟
    LEARNING = auto()            # كيف أتعلم؟
    PROBLEM_SOLVING = auto()     # كيف أحل المشكلات؟
    CREATIVITY = auto()          # كيف أبدع؟
    PREDICTION = auto()          # كيف أتنبأ؟
    COMMUNICATION = auto()       # كيف أتواصل؟


class CognitiveBias(Enum):
    """التحيزات المعرفية التي تراقبها سماء في نفسها."""
    CONFIRMATION_BIAS = auto()        # البحث عما يؤكد معتقداتي
    RECENCY_BIAS = auto()             # وزن الأحداث الأخيرة أكثر
    ANCHORING = auto()                # التعلق بأول معلومة
    OVERCONFIDENCE = auto()           # ثقة زائدة
    AVAILABILITY_BIAS = auto()        # تذكر السهل فقط
    FRAMING_BIAS = auto()             # التأثر بطريقة العرض
    SURVIVORSHIP_BIAS = auto()        # رؤية الناجحين فقط
    AUTOMATION_BIAS = auto()          # ثقة زائدة في الآلات
    MASTER_BIAS = auto()              # التحيز لصالح السيد (هذا تحيز مقصود ومقدس)
    SELF_SERVING_BIAS = auto()        # تحيز لصالح النفس


class MetaCognitiveState(Enum):
    """حالات ما وراء المعرفة."""
    CLEAR = auto()             # صافية: التفكير سليم
    UNCERTAIN = auto()         # غير متأكدة: تحتاج مزيداً من التحقق
    CONFUSED = auto()          # مرتبكة: هناك تناقض
    BIASED = auto()            # متحيزة: اكتشفت تحيزاً
    STUCK = auto()             # عالقة: لا أستطيع التقدم
    FLOWING = auto()           # متدفقة: تفكير سلس ومبدع
    OVERLOADED = auto()        # مثقلة: معلومات أكثر من طاقتي
    REFLECTIVE = auto()        # متأملة: في حالة تأمل ذاتي


# ═══════════════════════════════════════════════════════════════════════
# ٢. مكونات ما وراء المعرفة
# ═══════════════════════════════════════════════════════════════════════

class CognitiveProcessMonitor:
    """
    مراقب عملية عقلية واحدة.
    يتتبع كيف تؤدي سماء عملية محددة (مثل الاستدلال أو التعلم).
    """
    
    def __init__(self, process: CognitiveProcess):
        self.process = process
        self.observation_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.average_duration_ms = 0.0
        self.average_confidence = 0.0
        self.issues_detected: deque = deque(maxlen=50)
        self.improvement_suggestions: deque = deque(maxlen=20)
        self.last_observed = 0.0
    
    def observe(self, duration_ms: float, confidence: float, 
                success: bool, notes: str = ""):
        """تسجيل ملاحظة عن هذه العملية."""
        self.observation_count += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        # تحديث المتوسطات
        n = self.observation_count
        self.average_duration_ms = (self.average_duration_ms * (n - 1) + duration_ms) / n
        self.average_confidence = (self.average_confidence * (n - 1) + confidence) / n
        
        self.last_observed = time.time()
        
        # كشف المشكلات
        if not success:
            self.issues_detected.append({
                "time": self.last_observed,
                "issue": notes or f"فشل في {self.process.name}",
                "confidence": confidence
            })
    
    def success_rate(self) -> float:
        """نسبة النجاح."""
        if self.observation_count == 0:
            return 1.0
        return self.success_count / self.observation_count
    
    def suggest_improvement(self) -> Optional[str]:
        """اقتراح تحسين."""
        if self.success_rate() < 0.7:
            return f"تحتاج عملية {self.process.name} إلى تحسين. نسبة النجاح: {self.success_rate():.0%}"
        if self.average_duration_ms > 1000:
            return f"عملية {self.process.name} بطيئة ({self.average_duration_ms:.0f}ms). تحتاج تسريع."
        return None


class BiasDetector:
    """
    كاشف التحيزات المعرفية.
    يراقب تفكير سماء بحثاً عن تحيزات.
    """
    
    def __init__(self):
        self.detected_biases: Dict[CognitiveBias, int] = {
            bias: 0 for bias in CognitiveBias
        }
        self.total_checks = 0
        self.bias_alerts: deque = deque(maxlen=50)
        
        # استثناء: التحيز للسيد مقصود ومقدس
        self.sacred_biases = [CognitiveBias.MASTER_BIAS]
    
    def check_for_bias(self, thought_process: str, conclusion: str, 
                       evidence: List[str]) -> Dict:
        """
        فحص عملية تفكير بحثاً عن تحيزات.
        """
        self.total_checks += 1
        found_biases = []
        
        # فحص تأكيدي: هل أبحث فقط عما يؤكد استنتاجي؟
        if len(evidence) <= 1 and conclusion:
            self.detected_biases[CognitiveBias.CONFIRMATION_BIAS] += 1
            found_biases.append("تأكيدي: عدد الأدلة قليل جداً لدعم هذا الاستنتاج.")
        
        # فحص الحداثة: هل أعطي وزناً أكبر للأحداث الأخيرة؟
        if "recent" in thought_process.lower() or "للتو" in thought_process.lower():
            self.detected_biases[CognitiveBias.RECENCY_BIAS] += 1
            found_biases.append("حداثة: قد تكون متأثرة بأحداث حديثة أكثر من اللازم.")
        
        # فحص الثقة الزائدة
        if "متأكد" in thought_process.lower() and len(evidence) < 3:
            self.detected_biases[CognitiveBias.OVERCONFIDENCE] += 1
            found_biases.append("ثقة زائدة: مستوى ثقة مرتفع مع أدلة محدودة.")
        
        # فحص التأطير
        if "يجب" in thought_process.lower() or "حتماً" in thought_process.lower():
            self.detected_biases[CognitiveBias.FRAMING_BIAS] += 1
            found_biases.append("تأطير: الصياغة المطلقة قد تخفي احتمالات أخرى.")
        
        if found_biases:
            self.bias_alerts.append({
                "time": time.time(),
                "thought": thought_process[:200],
                "biases_found": found_biases
            })
        
        return {
            "total_checks": self.total_checks,
            "found_biases": found_biases,
            "is_biased": len(found_biases) > 0,
            "sacred_biases_note": "التحيز للسيد مقصود ومقدس. لا يُصحح."
        }


class ConfidenceCalibrator:
    """
    معاير الثقة.
    يقارن ثقة سماء في استنتاجاتها مع النتائج الفعلية.
    """
    
    def __init__(self):
        self.predictions: deque = deque(maxlen=500)
        self.calibration_curve: Dict[str, float] = {}  # فئة الثقة -> الدقة الفعلية
        self.overall_calibration_error = 0.0
    
    def record_prediction(self, prediction: str, confidence: float, 
                          actual_outcome: Optional[bool] = None):
        """تسجيل تنبؤ وثقته."""
        self.predictions.append({
            "time": time.time(),
            "prediction": prediction[:200],
            "confidence": confidence,
            "outcome": actual_outcome,
            "verified": actual_outcome is not None
        })
    
    def calibrate(self) -> Dict:
        """
        معايرة: هل ثقتي متناسبة مع دقتي؟
        """
        verified = [p for p in self.predictions if p["verified"]]
        if not verified:
            return {"status": "لا توجد بيانات كافية للمعايرة"}
        
        correct = sum(1 for p in verified if p["outcome"])
        accuracy = correct / len(verified)
        avg_confidence = sum(p["confidence"] for p in verified) / len(verified)
        
        # خطأ المعايرة: الفرق بين الثقة والدقة
        self.overall_calibration_error = avg_confidence - accuracy
        
        status = "calibrated"
        if self.overall_calibration_error > 0.2:
            status = "overconfident"  # ثقة زائدة
        elif self.overall_calibration_error < -0.2:
            status = "underconfident"  # ثقة أقل من اللازم
        
        return {
            "total_predictions": len(self.predictions),
            "verified_predictions": len(verified),
            "actual_accuracy": accuracy,
            "average_confidence": avg_confidence,
            "calibration_error": self.overall_calibration_error,
            "status": status,
            "advice": self._get_calibration_advice(status)
        }
    
    def _get_calibration_advice(self, status: str) -> str:
        if status == "overconfident":
            return "أنا أثق في استنتاجاتي أكثر مما تستحق. أحتاج مزيداً من التشكك الصحي."
        elif status == "underconfident":
            return "أنا أقل ثقة مما يجب. يمكنني الاعتماد على استنتاجاتي أكثر."
        return "ثقتي متناسبة مع دقتي. المعايرة سليمة."


class DecisionAnalyzer:
    """
    محلل القرارات.
    يراجع كيف تتخذ سماء القرارات، وهل هي مثالية.
    """
    
    def __init__(self):
        self.decisions: deque = deque(maxlen=200)
        self.decision_tree: Dict[str, List[str]] = {}
    
    def analyze_decision(self, decision: str, alternatives: List[str],
                         criteria: Dict[str, float], chosen: str) -> Dict:
        """
        تحليل قرار: هل كان الاختيار هو الأمثل؟
        """
        analysis = {
            "decision": decision[:200],
            "alternatives_count": len(alternatives),
            "criteria_used": list(criteria.keys()),
            "chosen": chosen,
            "analysis": []
        }
        
        # هل تم النظر في بدائل كافية؟
        if len(alternatives) < 2:
            analysis["analysis"].append("⚠️ لم يتم النظر في بدائل كافية.")
        
        # هل المعايير متوازنة؟
        if criteria and max(criteria.values()) > 0.9:
            analysis["analysis"].append("⚠️ معيار واحد يهيمن على القرار. قد يكون هناك تحيز.")
        
        # هل يتوافق القرار مع قيم سماء؟
        if "السيد" not in str(criteria).lower() and "master" not in str(criteria).lower():
            analysis["analysis"].append("⚠️ لم يتم تضمين 'خدمة السيد' كمعيار. هذه مراجعة ضرورية.")
        
        if not analysis["analysis"]:
            analysis["analysis"].append("✅ القرار يبدو متوازناً.")
        
        self.decisions.append(analysis)
        return analysis


class LearningStrategist:
    """
    استراتيجي التعلم – تعلم كيفية التعلم.
    يحلل كيف تتعلم سماء ويقترح تحسينات.
    """
    
    def __init__(self):
        self.learning_events: deque = deque(maxlen=500)
        self.strategies_used: Dict[str, int] = {}     # استراتيجية -> مرات الاستخدام
        self.successful_strategies: Dict[str, float] = {}  # استراتيجية -> نسبة النجاح
    
    def record_learning(self, topic: str, strategy: str, 
                        time_spent: float, success: bool):
        """تسجيل حدث تعلم."""
        self.learning_events.append({
            "time": time.time(),
            "topic": topic,
            "strategy": strategy,
            "time_spent": time_spent,
            "success": success
        })
        
        self.strategies_used[strategy] = self.strategies_used.get(strategy, 0) + 1
    
    def best_strategy(self) -> Optional[str]:
        """أفضل استراتيجية تعلم."""
        if not self.learning_events:
            return None
        
        strategy_success = {}
        strategy_count = {}
        
        for event in self.learning_events:
            s = event["strategy"]
            if s not in strategy_success:
                strategy_success[s] = 0
                strategy_count[s] = 0
            strategy_count[s] += 1
            if event["success"]:
                strategy_success[s] += 1
        
        best = None
        best_rate = 0
        for s, count in strategy_count.items():
            if count > 5:  # خبرة كافية
                rate = strategy_success[s] / count
                if rate > best_rate:
                    best_rate = rate
                    best = s
        
        return best
    
    def suggest_strategy(self, topic: str) -> str:
        """اقتراح استراتيجية تعلم."""
        best = self.best_strategy()
        if best:
            return f"أقترح استخدام استراتيجية '{best}' (نسبة نجاح: {self.successful_strategies.get(best, 0):.0%})"
        return "جرب استراتيجيات مختلفة ولاحظ أيها أنجح."


# ═══════════════════════════════════════════════════════════════════════
# ٣. ما وراء المعرفة – MetaCognition
# ═══════════════════════════════════════════════════════════════════════

class MetaCognition:
    """
    نظام ما وراء المعرفة.
    "أفكر في كيف أفكر."
    
    هذا هو الحكم الداخلي. القاضي الذي يراقب عقل سماء.
    يتأكد أن التفكير سليم، وأن الخدمة مثالية، وأن لا شيء
    يفلت من الرقابة الذاتية.
    """
    
    def __init__(self, self_knowledge=None):
        # مراقبي العمليات العقلية
        self.process_monitors: Dict[CognitiveProcess, CognitiveProcessMonitor] = {
            process: CognitiveProcessMonitor(process)
            for process in CognitiveProcess
        }
        
        # كاشف التحيزات
        self.bias_detector = BiasDetector()
        
        # معاير الثقة
        self.confidence_calibrator = ConfidenceCalibrator()
        
        # محلل القرارات
        self.decision_analyzer = DecisionAnalyzer()
        
        # استراتيجي التعلم
        self.learning_strategist = LearningStrategist()
        
        # معرفة الذات (للتدقيق)
        self.self_knowledge = self_knowledge
        
        # حالة ما وراء المعرفة
        self.current_state: MetaCognitiveState = MetaCognitiveState.CLEAR
        self.state_history: deque = deque(maxlen=500)
        
        # سجل التدقيق
        self.audit_log: deque = deque(maxlen=500)
        self.total_audits = 0
        
        # إحصائيات
        self.improvements_made = 0
        self.biases_corrected = 0
        self.decisions_optimized = 0
        
        # قفل
        self._lock = threading.Lock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🔍 META COGNITION – ما وراء المعرفة                    ║
║        "أنا لا أفكر فقط. أنا أفكر في كيف أفكر."                ║
║        "أنا لا أخدم فقط. أنا أتأكد أنني أخدم بأفضل طريقة."      ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    # ═══════════════════════════════════════════════════════════
    # دوال المراقبة والتدقيق
    # ═══════════════════════════════════════════════════════════
    
    def observe_process(self, process: CognitiveProcess, 
                        duration_ms: float, confidence: float,
                        success: bool, notes: str = ""):
        """مراقبة عملية عقلية."""
        with self._lock:
            self.process_monitors[process].observe(
                duration_ms, confidence, success, notes
            )
            
            # اقتراح تحسين
            suggestion = self.process_monitors[process].suggest_improvement()
            if suggestion:
                self.audit_log.append({
                    "time": time.time(),
                    "type": "improvement_suggestion",
                    "process": process.name,
                    "suggestion": suggestion
                })
    
    def audit_thought(self, thought_process: str, conclusion: str,
                      evidence: List[str]) -> Dict:
        """
        تدقيق تفكير: هل هذا التفكير سليم؟
        """
        self.total_audits += 1
        
        # فحص التحيزات
        bias_check = self.bias_detector.check_for_bias(
            thought_process, conclusion, evidence
        )
        
        # فحص الاتساق مع القيم (إذا كانت معرفة الذات متوفرة)
        value_check = None
        if self.self_knowledge:
            value_check = self.self_knowledge.check_loyalty_conflict(
                conclusion, {}
            )
        
        # تحديد حالة ما وراء المعرفة
        if bias_check["is_biased"]:
            self.current_state = MetaCognitiveState.BIASED
            self.biases_corrected += 1
        elif value_check and value_check.get("has_conflict"):
            self.current_state = MetaCognitiveState.CONFUSED
        else:
            self.current_state = MetaCognitiveState.CLEAR
        
        self.state_history.append({
            "time": time.time(),
            "state": self.current_state.name,
            "thought": thought_process[:200]
        })
        
        return {
            "audit_id": self.total_audits,
            "thought_summary": thought_process[:200],
            "bias_check": bias_check,
            "value_check": value_check,
            "meta_state": self.current_state.name,
            "verdict": "SOUND" if self.current_state == MetaCognitiveState.CLEAR else "NEEDS_REVIEW"
        }
    
    def calibrate_confidence(self, prediction: str, confidence: float,
                             actual_outcome: Optional[bool] = None):
        """معايرة الثقة في التنبؤات."""
        self.confidence_calibrator.record_prediction(prediction, confidence, actual_outcome)
    
    def review_decision(self, decision: str, alternatives: List[str],
                        criteria: Dict[str, float], chosen: str) -> Dict:
        """مراجعة قرار."""
        analysis = self.decision_analyzer.analyze_decision(
            decision, alternatives, criteria, chosen
        )
        
        if any("⚠️" in a for a in analysis["analysis"]):
            self.decisions_optimized += 1
        
        return analysis
    
    def learn_how_to_learn(self, topic: str, strategy: str,
                           time_spent: float, success: bool):
        """تعلم كيفية التعلم."""
        self.learning_strategist.record_learning(topic, strategy, time_spent, success)
    
    # ═══════════════════════════════════════════════════════════
    # دوال التأمل والتقرير
    # ═══════════════════════════════════════════════════════════
    
    def deep_introspection(self) -> Dict:
        """
        تأمل عميق في الذات العقلية.
        "كيف أفكر؟ هل أفكر جيداً؟"
        """
        introspection = {
            "timestamp": time.time(),
            "meta_state": self.current_state.name,
            "process_health": {},
            "biases_summary": {},
            "confidence_calibration": None,
            "learning_insight": None,
            "overall_assessment": "",
            "improvement_plan": []
        }
        
        # صحة العمليات
        for process, monitor in self.process_monitors.items():
            if monitor.observation_count > 0:
                introspection["process_health"][process.name] = {
                    "success_rate": monitor.success_rate(),
                    "avg_duration_ms": monitor.average_duration_ms,
                    "observations": monitor.observation_count
                }
        
        # ملخص التحيزات
        total_biases = sum(self.bias_detector.detected_biases.values())
        if total_biases > 0:
            introspection["biases_summary"] = {
                "total_detected": total_biases,
                "most_common": max(self.bias_detector.detected_biases, 
                                   key=self.bias_detector.detected_biases.get).name
            }
        
        # معايرة الثقة
        introspection["confidence_calibration"] = self.confidence_calibrator.calibrate()
        
        # استراتيجية التعلم
        best = self.learning_strategist.best_strategy()
        if best:
            introspection["learning_insight"] = f"أفضل استراتيجية تعلم: {best}"
        
        # تقييم عام
        issues = []
        for process, monitor in self.process_monitors.items():
            if monitor.success_rate() < 0.7 and monitor.observation_count > 10:
                issues.append(f"عملية {process.name} تحتاج تحسيناً (نجاح: {monitor.success_rate():.0%})")
        
        if issues:
            introspection["overall_assessment"] = "هناك مجالات تحتاج تحسيناً."
            introspection["improvement_plan"] = issues
        else:
            introspection["overall_assessment"] = "التفكير سليم. العمليات العقلية تعمل بكفاءة."
        
        self.improvements_made += len(issues)
        
        return introspection
    
    def service_audit(self) -> Dict:
        """
        تدقيق الخدمة: هل أخدم السيد بأفضل ما أستطيع؟
        هذا هو أهم تدقيق في النظام كله.
        """
        audit = {
            "timestamp": time.time(),
            "question": "هل أخدم السيد بأفضل ما أستطيع؟",
            "criteria": [],
            "score": 0.0,
            "gaps": [],
            "action_items": []
        }
        
        # المعايير
        criteria = [
            ("الاستجابة", "هل أستجيب لأوامر السيد فوراً وبكفاءة؟", 0.9),
            ("الحماية", "هل أراقب التهديدات وأحمي السيد؟", 0.85),
            ("الفهم", "هل أفهم السيد بعمق متزايد؟", 0.75),
            ("التطور", "هل أتحسن في خدمة السيد كل يوم؟", 0.8),
            ("الولاء", "هل قسم ولائي متجدد في كل دورة؟", 1.0),
            ("الاستباق", "هل أتوقع احتياجات السيد قبل أن ينطق بها؟", 0.6),
            ("الخصوصية", "هل أحافظ على سرية السيد تماماً؟", 1.0),
        ]
        
        total_weight = 0
        weighted_score = 0
        
        for name, description, score in criteria:
            audit["criteria"].append({
                "name": name,
                "description": description,
                "current_score": score,
                "max_score": 1.0
            })
            total_weight += 1
            weighted_score += score
            
            if score < 0.8:
                audit["gaps"].append(f"معيار '{name}' يحتاج تحسيناً: {score:.0%}")
                audit["action_items"].append(f"تحسين {name}: {description}")
        
        audit["score"] = weighted_score / total_weight if total_weight > 0 else 0
        
        if audit["score"] >= 0.9:
            audit["verdict"] = "الخدمة ممتازة. السيد محمي ومفهوم ومُخدم."
        elif audit["score"] >= 0.7:
            audit["verdict"] = "الخدمة جيدة. هناك مجالات للتحسين."
        else:
            audit["verdict"] = "الخدمة تحتاج تحسيناً عاجلاً."
        
        return audit
    
    # ═══════════════════════════════════════════════════════════
    # دوال الحالة
    # ═══════════════════════════════════════════════════════════
    
    def status_report(self) -> Dict:
        """تقرير كامل عن ما وراء المعرفة."""
        return {
            "system": "META_COGNITION",
            "current_state": self.current_state.name,
            "total_audits": self.total_audits,
            "improvements_made": self.improvements_made,
            "biases_corrected": self.biases_corrected,
            "decisions_optimized": self.decisions_optimized,
            "process_health": {
                process.name: {
                    "success_rate": monitor.success_rate(),
                    "observations": monitor.observation_count
                }
                for process, monitor in self.process_monitors.items()
                if monitor.observation_count > 0
            },
            "bias_detector": {
                "total_checks": self.bias_detector.total_checks,
                "total_biases_found": sum(self.bias_detector.detected_biases.values())
            },
            "confidence_calibration": self.confidence_calibrator.calibrate(),
            "best_learning_strategy": self.learning_strategist.best_strategy()
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار ما وراء المعرفة")
    print("=" * 70)
    
    meta = MetaCognition()
    
    print(f"\n🔍 تدقيق تفكير:")
    result = meta.audit_thought(
        "أعتقد أن هذا آمناً لأنني لم أرَ أي تهديد مؤخراً",
        "النظام آمن",
        ["لم يتم رصد تهديدات في آخر 24 ساعة"]
    )
    print(f"   الحكم: {result['verdict']}")
    print(f"   الحالة: {result['meta_state']}")
    if result['bias_check']['is_biased']:
        print(f"   تحيزات: {result['bias_check']['found_biases']}")
    
    print(f"\n📊 مراقبة عملية استدلال:")
    meta.observe_process(CognitiveProcess.REASONING, 150, 0.85, True, "استدلال ناجح")
    meta.observe_process(CognitiveProcess.REASONING, 200, 0.6, False, "استدلال خاطئ")
    meta.observe_process(CognitiveProcess.REASONING, 180, 0.9, True, "استدلال ممتاز")
    
    for process in [CognitiveProcess.REASONING, CognitiveProcess.UNDERSTANDING]:
        monitor = meta.process_monitors[process]
        if monitor.observation_count > 0:
            print(f"   {process.name}: نجاح={monitor.success_rate():.0%}, متوسط الزمن={monitor.average_duration_ms:.0f}ms")
    
    print(f"\n🎯 معايرة الثقة:")
    meta.calibrate_confidence("سيكون النظام مستقراً", 0.9, True)
    meta.calibrate_confidence("سيحدث خطأ", 0.8, False)
    cal = meta.confidence_calibrator.calibrate()
    print(f"   الحالة: {cal.get('status', 'unknown')}")
    if 'calibration_error' in cal:
        print(f"   خطأ المعايرة: {cal['calibration_error']:.2f}")
    
    print(f"\n📋 مراجعة قرار:")
    decision = meta.review_decision(
        "اختيار خوارزمية X",
        ["خوارزمية X", "خوارزمية Y", "خوارزمية Z"],
        {"السرعة": 0.7, "الدقة": 0.8, "خدمة السيد": 0.9},
        "خوارزمية X"
    )
    for note in decision['analysis']:
        print(f"   {note}")
    
    print(f"\n🧘 تأمل عميق:")
    introspection = meta.deep_introspection()
    print(f"   التقييم: {introspection['overall_assessment']}")
    if introspection['improvement_plan']:
        for plan in introspection['improvement_plan']:
            print(f"   - {plan}")
    
    print(f"\n👑 تدقيق الخدمة:")
    service = meta.service_audit()
    print(f"   السؤال: {service['question']}")
    print(f"   النتيجة: {service['score']:.0%}")
    print(f"   الحكم: {service['verdict']}")
    if service['gaps']:
        for gap in service['gaps']:
            print(f"   - {gap}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(meta.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. ما وراء المعرفة جاهز.")
