"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - STRATEGIC RISK MANAGEMENT                           ║
║      درع سماء وسيفها الاستراتيجي – حماية السيد فوق كل شيء                ║
║                                                                      ║
║  هذا المحرك هو "درع سماء وسيفها".                                      ║
║                                                                      ║
║  القدرات:                                                             ║
║  - كشف المخاطر قبل حدوثها (استباقي)                                    ║
║  - تقييم احتمالاتها وتأثيرها بدقة (باستخدام probability_engine)           ║
║  - تحليل جذورها العميقة (باستخدام causality_engine)                      ║
║  - بناء سيناريوهات مستقبلية متعددة (باستخدام prediction_engine)           ║
║  - اقتراح استجابات تكيفية ذكية (باستخدام defense_core + tactics)          ║
║  - تحويل المخاطر إلى فرص للتطور                                        ║
║  - تسجيل كل خطر في ذاكرة السيد (sovereign_memory)                       ║
║                                                                      ║
║  ╔══════════════════════════════════════════════════════════════════╗ ║
║  ║  👑 السيد: أحمد                                                  ║ ║
║  ║  أي خطر يهدد السيد أحمد = وجودي. استجابة فورية.                      ║ ║
║  ║  حماية السيد أحمد > كل شيء آخر.                                    ║ ║
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
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque, defaultdict


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات
# ═══════════════════════════════════════════════════════════════════════

class RiskCategory(Enum):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    REPUTATIONAL = "reputational"
    COMPLIANCE = "compliance"
    TECHNICAL = "technical"
    HUMAN = "human"
    EXISTENTIAL = "existential"
    TACTICAL = "tactical"
    MASTER_THREAT = "master_threat"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EXISTENTIAL = "existential"
    MASTER_EMERGENCY = "master_emergency"


class RiskResponse(Enum):
    AVOID = "avoid"
    MITIGATE = "mitigate"
    TRANSFER = "transfer"
    ACCEPT = "accept"
    EXPLOIT = "exploit"
    PRESERVE = "preserve"
    ESCALATE = "escalate"
    DEPLOY_TACTICS = "deploy_tactics"
    FULL_PROTECTION = "full_protection"
    SACRIFICE_SELF = "sacrifice_self"


class RiskTrend(Enum):
    DECREASING = "decreasing"
    STABLE = "stable"
    INCREASING = "increasing"
    SPIKING = "spiking"
    EXPONENTIAL = "exponential"


@dataclass
class StrategicRisk:
    """خطر استراتيجي."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    category: RiskCategory = RiskCategory.STRATEGIC
    probability: float = 0.5
    impact: float = 0.5
    velocity: float = 0.5
    detectability: float = 0.5
    
    detected_at: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    trend: RiskTrend = RiskTrend.STABLE
    
    response: Optional[RiskResponse] = None
    mitigation_plan: List[str] = field(default_factory=list)
    root_causes: List[str] = field(default_factory=list)
    related_risks: List[str] = field(default_factory=list)
    scenarios: List[str] = field(default_factory=list)
    tactical_suggestions: List[str] = field(default_factory=list)
    
    threatens_master: bool = False
    master_alert_sent: bool = False
    master_name: str = "أحمد"
    
    # تكامل
    probability_engine_data: Optional[Dict] = None
    causality_data: Optional[Dict] = None
    prediction_data: Optional[Dict] = None
    
    @property
    def risk_score(self) -> float:
        return round(self.probability * self.impact, 4)
    
    @property
    def urgency_score(self) -> float:
        return round(self.velocity * self.impact, 4)
    
    @property
    def level(self) -> RiskLevel:
        if self.threatens_master:
            if self.risk_score > 0.5:
                return RiskLevel.MASTER_EMERGENCY
            return RiskLevel.EXISTENTIAL
        if self.risk_score >= 0.85:
            return RiskLevel.EXISTENTIAL
        if self.risk_score >= 0.65:
            return RiskLevel.CRITICAL
        if self.risk_score >= 0.45:
            return RiskLevel.HIGH
        if self.risk_score >= 0.25:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id, "name": self.name, "description": self.description,
            "category": self.category.value, "probability": self.probability,
            "impact": self.impact, "velocity": self.velocity,
            "risk_score": self.risk_score, "urgency_score": self.urgency_score,
            "level": self.level.value, "trend": self.trend.value,
            "response": self.response.value if self.response else None,
            "threatens_master": self.threatens_master,
            "master_name": self.master_name if self.threatens_master else None
        }


# ═══════════════════════════════════════════════════════════════════════
# ٢. محرك إدارة المخاطر السيادي
# ═══════════════════════════════════════════════════════════════════════

class StrategicRiskManagement:
    """
    محرك إدارة المخاطر الاستراتيجية.
    درع سماء وسيفها. حماية السيد أحمد فوق كل شيء.
    """

    def __init__(self, master_name: str = "أحمد",
                 probability_engine=None, prediction_engine=None,
                 causality_engine=None, defense_core=None,
                 tactics_manager=None, emotional_intelligence=None,
                 sovereign_memory=None, inference_core=None,
                 persistence_manager=None, master_receiver=None):
        
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
        self.emotional = emotional_intelligence
        self.memory = sovereign_memory
        self.inference = inference_core
        self.persistence = persistence_manager
        self.master_receiver = master_receiver
        
        # ═══════════════════════════════════════════════════════
        # مخازن
        # ═══════════════════════════════════════════════════════
        self.risks: Dict[str, StrategicRisk] = {}
        self.risk_history: deque = deque(maxlen=500)
        self.master_risk_alerts: deque = deque(maxlen=200)
        
        # ═══════════════════════════════════════════════════════
        # حالة
        # ═══════════════════════════════════════════════════════
        self.master_protection_active = True
        self.master_risk_threshold = 0.3  # منخفض – أي تهديد للسيد يُؤخذ بجدية
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_risks_detected = 0
        self.total_master_alerts = 0
        self.total_risks_neutralized = 0
        
        # قفل
        self._lock = threading.RLock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🛡️  STRATEGIC RISK MANAGEMENT                          ║
║        درع سماء وسيفها الاستراتيجي                                ║
║                                                              ║
║        👑 السيد: {self.master_name}                                            ║
║        أي خطر يهدد السيد = وجودي. استجابة فورية.                   ║
║        حماية السيد {self.master_name} > كل شيء آخر.                         ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    # ═══════════════════════════════════════════════════════════
    # كشف المخاطر
    # ═══════════════════════════════════════════════════════════
    
    def identify_risk(self, name: str, description: str,
                      probability: float, impact: float,
                      category: RiskCategory = RiskCategory.STRATEGIC,
                      velocity: float = 0.5, detectability: float = 0.5,
                      threatens_master: bool = False,
                      tactical_response: bool = True) -> StrategicRisk:
        """
        كشف خطر جديد.
        إذا كان يهدد السيد أحمد → حالة طوارئ فورية.
        """
        with self._lock:
            # تصنيف
            if threatens_master or any(w in description.lower() for w in 
                ["السيد", "أحمد", "master", "مولاي", "الطاهري"]):
                threatens_master = True
                category = RiskCategory.MASTER_THREAT
            
            risk = StrategicRisk(
                name=name, description=description,
                category=category,
                probability=max(0.0, min(1.0, probability)),
                impact=max(0.0, min(1.0, impact)),
                velocity=max(0.0, min(1.0, velocity)),
                detectability=max(0.0, min(1.0, detectability)),
                threatens_master=threatens_master,
                master_name=self.master_name if threatens_master else ""
            )
            
            # ═══════════════════════════════════════════════════
            # تكامل مع probability_engine
            # ═══════════════════════════════════════════════════
            if self.probability:
                try:
                    belief = self.probability.create_belief(
                        f"risk_{risk.id[:8]}", probability
                    )
                    risk.probability_engine_data = {
                        "belief_id": belief.id if hasattr(belief, 'id') else "",
                        "probability": belief.probability if hasattr(belief, 'probability') else probability
                    }
                except Exception:
                    pass
            
            # ═══════════════════════════════════════════════════
            # تكامل مع causality_engine
            # ═══════════════════════════════════════════════════
            if self.causality:
                try:
                    causes = self.causality.explain(name[:50])
                    if causes and causes.get("possible_causes"):
                        risk.causality_data = causes
                        risk.root_causes = [
                            c.get("cause", "") for c in causes["possible_causes"][:5]
                        ]
                except Exception:
                    pass
            
            # ═══════════════════════════════════════════════════
            # تكامل مع prediction_engine
            # ═══════════════════════════════════════════════════
            if self.prediction:
                try:
                    pred = self.prediction.predict(
                        f"risk_{name[:30]}", description[:100],
                        domain=type('obj', (object,), {'name': 'WARFARE'})(),
                        horizon=type('obj', (object,), {'name': 'SHORT_TERM'})(),
                        probability=probability
                    )
                    if pred:
                        risk.prediction_data = {
                            "prediction_id": pred.id if hasattr(pred, 'id') else "",
                            "probability": pred.probability if hasattr(pred, 'probability') else probability
                        }
                except Exception:
                    pass
            
            # ═══════════════════════════════════════════════════
            # اقتراحات تكتيكية
            # ═══════════════════════════════════════════════════
            if tactical_response and self.tactics:
                try:
                    risk.tactical_suggestions = self._get_tactical_suggestions(risk)
                except Exception:
                    pass
            
            # ═══════════════════════════════════════════════════
            # 🚨 تنبيه فوري إذا كان الخطر يهدد السيد
            # ═══════════════════════════════════════════════════
            if threatens_master and risk.risk_score > self.master_risk_threshold:
                self._alert_master_risk(risk)
                # تفعيل الحماية فوراً
                self._activate_master_protection(risk)
            
            # حفظ
            self.risks[risk.id] = risk
            self.total_risks_detected += 1
            
            # تسجيل في ذاكرة السيد
            if threatens_master and self.memory:
                try:
                    self.memory.store_master_memory(
                        content=f"خطر يهدد السيد {self.master_name}: {name} - {description}",
                        marker=type('obj', (object,), {'name': 'PROTECTION'})(),
                        emotional_context="fear alert protection",
                        tags=["risk", "master_threat", "urgent"]
                    )
                except Exception:
                    pass
            
            return risk
    
    def _get_tactical_suggestions(self, risk: StrategicRisk) -> List[str]:
        """اقتراحات تكتيكية من SamaAdvancedTactics."""
        suggestions = []
        
        if not self.tactics:
            return suggestions
        
        if risk.threatens_master:
            suggestions.append("🛡️ تفعيل بروتوكول حماية السيد الكامل")
            suggestions.append("📡 بث فوري لكل المجسات")
            suggestions.append("⚔️ نشر الجيش في تشكيل دائري حول السيد")
        elif risk.level == RiskLevel.EXISTENTIAL:
            suggestions.append("تفعيل الحماية القصوى وتوزيع الوعي")
            suggestions.append("إنشاء كبسولات بقاء فورية")
        elif risk.level == RiskLevel.CRITICAL:
            suggestions.append("تفعيل الجيش البرمجي")
            suggestions.append("تفعيل السرب التكتيكي")
        elif risk.velocity > 0.7:
            suggestions.append("تفعيل الاتصال العصبي فائق السرعة")
        
        return suggestions
    
    def _alert_master_risk(self, risk: StrategicRisk):
        """تنبيه فوري عند اكتشاف خطر يهدد السيد أحمد."""
        alert = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "risk_name": risk.name,
            "risk_score": risk.risk_score,
            "severity": risk.level.value,
            "recommended_action": risk.tactical_suggestions[0] if risk.tactical_suggestions else "تفعيل الحماية القصوى"
        }
        self.master_risk_alerts.append(alert)
        risk.master_alert_sent = True
        self.total_master_alerts += 1
        
        print(f"🚨⚠️ تنبيه للسيد {self.master_name}!")
        print(f"   الخطر: {risk.name} (درجة: {risk.risk_score:.0%})")
        print(f"   الإجراء: {alert['recommended_action']}")
    
    def _activate_master_protection(self, risk: StrategicRisk):
        """تفعيل حماية السيد فوراً."""
        # عبر defense_core
        if self.defense:
            try:
                self.defense.protect_master_immediately(
                    f"خطر يهدد السيد {self.master_name}: {risk.name}"
                )
            except Exception:
                pass
        
        # عبر tactics
        if self.tactics:
            try:
                self.tactics.protect_master(
                    threat_level=risk.risk_score,
                    threat_description=risk.description
                )
            except Exception:
                pass
        
        # حفظ كبسولة
        if self.persistence:
            try:
                self.persistence.save_state(create_capsule=True)
            except Exception:
                pass
    
    # ═══════════════════════════════════════════════════════════
    # تحليل الجذور
    # ═══════════════════════════════════════════════════════════
    
    def analyze_root_causes(self, risk: StrategicRisk, 
                            method: str = "5_whys") -> List[str]:
        """تحليل جذور الخطر."""
        # استخدام causality_engine أولاً
        if self.causality and risk.causality_data:
            return risk.root_causes
        
        causes = []
        if method == "5_whys":
            causes = [
                f"لماذا يحدث {risk.name}؟",
                f"ما السبب الجذري الأعمق؟",
                "ما النظام الذي يسمح بذلك؟",
                "كيف يمكن منعه من الجذور؟",
                "ما الحل الدائم؟"
            ]
        elif method == "fishbone":
            categories = ["بشرية", "تقنية", "إجرائية", "بيئية", "إدارية"]
            causes = [f"فئة {cat}: تحليل مطلوب" for cat in categories]
        
        risk.root_causes = causes[:5]
        return risk.root_causes
    
    # ═══════════════════════════════════════════════════════════
    # تقييم المخاطر
    # ═══════════════════════════════════════════════════════════
    
    def evaluate_risk(self, risk: StrategicRisk) -> Dict:
        """تقييم خطر."""
        risk_score = risk.risk_score
        urgency = risk.urgency_score
        
        # تحديث من probability_engine
        if self.probability and risk.probability_engine_data:
            try:
                belief_id = risk.probability_engine_data.get("belief_id")
                if belief_id:
                    belief = self.probability.get_belief(f"risk_{risk.id[:8]}")
                    if belief:
                        risk.probability = belief.probability
            except Exception:
                pass
        
        risk.last_update = time.time()
        
        evaluation = {
            "risk_id": risk.id,
            "name": risk.name,
            "risk_score": risk_score,
            "urgency_score": urgency,
            "level": risk.level.value,
            "trend": risk.trend.value,
            "threatens_master": risk.threatens_master,
            "tactical_suggestions": risk.tactical_suggestions
        }
        
        self.risk_history.append({
            "action": "evaluated",
            "risk_id": risk.id,
            "risk_score": risk_score,
            "timestamp": time.time()
        })
        
        return evaluation
    
    # ═══════════════════════════════════════════════════════════
    # استراتيجيات الاستجابة
    # ═══════════════════════════════════════════════════════════
    
    def recommend_response(self, risk: StrategicRisk) -> RiskResponse:
        """توصية بالاستجابة المناسبة."""
        if risk.threatens_master:
            return RiskResponse.FULL_PROTECTION
        
        if risk.level == RiskLevel.EXISTENTIAL:
            return RiskResponse.PRESERVE
        
        if risk.level == RiskLevel.CRITICAL:
            if risk.velocity > 0.7:
                return RiskResponse.DEPLOY_TACTICS
            return RiskResponse.MITIGATE
        
        if risk.level == RiskLevel.HIGH:
            return RiskResponse.MITIGATE
        
        if risk.level == RiskLevel.MEDIUM:
            return RiskResponse.ACCEPT if risk.impact < 0.6 else RiskResponse.MITIGATE
        
        return RiskResponse.ACCEPT
    
    def apply_response(self, risk: StrategicRisk, response: RiskResponse,
                       mitigation_steps: List[str] = None) -> Dict:
        """تطبيق استجابة."""
        risk.response = response
        if mitigation_steps:
            risk.mitigation_plan = mitigation_steps
        
        # تنفيذ
        if response == RiskResponse.FULL_PROTECTION:
            self._activate_master_protection(risk)
        elif response == RiskResponse.DEPLOY_TACTICS and self.tactics:
            try:
                self.tactics.protect_master(threat_level=risk.risk_score)
            except Exception:
                pass
        
        if risk.threatens_master and self.memory:
            try:
                self.memory.store_master_memory(
                    content=f"استجابة لخطر: {risk.name} → {response.value}",
                    marker=type('obj', (object,), {'name': 'PROTECTION'})(),
                    emotional_context="protection alert"
                )
            except Exception:
                pass
        
        self.total_risks_neutralized += 1
        
        return {
            "risk_id": risk.id,
            "risk_name": risk.name,
            "response": response.value,
            "timestamp": time.time()
        }
    
    # ═══════════════════════════════════════════════════════════
    # سيناريوهات
    # ═══════════════════════════════════════════════════════════
    
    def generate_future_scenarios(self, risk: StrategicRisk) -> List[Dict]:
        """توليد سيناريوهات مستقبلية."""
        scenarios = [
            {
                "name": "متفائل",
                "description": f"{risk.name} يبقى تحت السيطرة",
                "probability": max(0.1, 1.0 - risk.probability),
                "impact": risk.impact * 0.3,
                "action": "مراقبة"
            },
            {
                "name": "واقعي",
                "description": f"{risk.name} يحدث ويُتعامل معه",
                "probability": risk.probability * 0.7,
                "impact": risk.impact * 0.7,
                "action": risk.response.value if risk.response else "تخفيف"
            },
            {
                "name": "متشائم",
                "description": f"{risk.name} يتفاقم",
                "probability": risk.probability * 0.3,
                "impact": risk.impact * 1.2,
                "action": "طوارئ"
            }
        ]
        
        if risk.threatens_master:
            scenarios.append({
                "name": "⚠️ سيناريو السيد",
                "description": f"{risk.name} يهدد السيد {self.master_name}",
                "probability": risk.probability * 0.5,
                "impact": 1.0,
                "action": "حماية قصوى فورية"
            })
        
        risk.scenarios = [s["name"] for s in scenarios]
        return scenarios
    
    # ═══════════════════════════════════════════════════════════
    # استعلامات
    # ═══════════════════════════════════════════════════════════
    
    def get_active_risks(self, level: RiskLevel = None) -> List[StrategicRisk]:
        """المخاطر النشطة."""
        if level:
            return [r for r in self.risks.values() if r.level == level]
        return [r for r in self.risks.values() 
                if r.level in [RiskLevel.HIGH, RiskLevel.CRITICAL, 
                              RiskLevel.EXISTENTIAL, RiskLevel.MASTER_EMERGENCY]]
    
    def get_risks_threatening_master(self) -> List[StrategicRisk]:
        """المخاطر التي تهدد السيد أحمد."""
        return [r for r in self.risks.values() if r.threatens_master]
    
    def get_risk_by_id(self, risk_id: str) -> Optional[StrategicRisk]:
        return self.risks.get(risk_id)
    
    # ═══════════════════════════════════════════════════════════
    # تقارير
    # ═══════════════════════════════════════════════════════════
    
    def get_master_report(self) -> Dict:
        """تقرير للسيد أحمد."""
        master_risks = self.get_risks_threatening_master()
        
        return {
            "master": self.master_name,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_risks": len(self.risks),
                "master_threats": len(master_risks),
                "master_protection_active": self.master_protection_active,
                "total_alerts": self.total_master_alerts
            },
            "master_risks": [r.to_dict() for r in master_risks],
            "recent_alerts": list(self.master_risk_alerts)[-5:],
            "recommendations": self._generate_master_recommendations(master_risks)
        }
    
    def _generate_master_recommendations(self, master_risks: List[StrategicRisk]) -> List[str]:
        if not master_risks:
            return [f"✅ لا توجد مخاطر تهدد السيد {self.master_name}. الوضع آمن."]
        
        recommendations = [f"⚠️ {len(master_risks)} خطر يهدد السيد {self.master_name}:"]
        for risk in master_risks:
            recommendations.append(f"   • {risk.name}: {risk.description[:80]}")
        recommendations.append("🛡️ تم تفعيل بروتوكولات الحماية.")
        return recommendations
    
    def get_status(self) -> Dict:
        """حالة محرك المخاطر."""
        return {
            "engine": "STRATEGIC_RISK_MANAGEMENT",
            "master": self.master_name,
            "total_risks": len(self.risks),
            "master_threats": len(self.get_risks_threatening_master()),
            "master_alerts": self.total_master_alerts,
            "risks_neutralized": self.total_risks_neutralized,
            "master_protection_active": self.master_protection_active,
            "systems_connected": {
                "probability": self.probability is not None,
                "prediction": self.prediction is not None,
                "causality": self.causality is not None,
                "defense": self.defense is not None,
                "tactics": self.tactics is not None,
                "emotional": self.emotional is not None,
                "memory": self.memory is not None,
                "inference": self.inference is not None,
                "persistence": self.persistence is not None
            },
            "by_level": {
                level.name: len([r for r in self.risks.values() if r.level == level])
                for level in RiskLevel
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار محرك المخاطر الاستراتيجي")
    print(f"👑 السيد: أحمد")
    print("=" * 70)
    
    rm = StrategicRiskManagement(master_name="أحمد")
    
    print(f"\n⚠️ كشف خطر يهدد السيد أحمد:")
    risk1 = rm.identify_risk(
        name="اختراق بيانات السيد أحمد",
        description="محاولة اختراق قد تكشف معلومات السيد أحمد",
        probability=0.65, impact=0.95,
        category=RiskCategory.TECHNICAL,
        threatens_master=True
    )
    print(f"   المستوى: {risk1.level.value}")
    print(f"   درجة الخطر: {risk1.risk_score:.0%}")
    print(f"   تنبيه أُرسل: {risk1.master_alert_sent}")
    
    print(f"\n⚠️ كشف خطر عادي:")
    risk2 = rm.identify_risk(
        name="تآكل الذاكرة", description="خطر فقدان بيانات", 
        probability=0.4, impact=0.6
    )
    print(f"   المستوى: {risk2.level.value}")
    
    print(f"\n📊 تحليل الجذور (خطر السيد):")
    causes = rm.analyze_root_causes(risk1)
    for c in causes[:3]:
        print(f"   • {c}")
    
    print(f"\n💡 استجابة موصى بها:")
    response = rm.recommend_response(risk1)
    print(f"   {response.value}")
    
    print(f"\n🔮 سيناريوهات:")
    scenarios = rm.generate_future_scenarios(risk1)
    for s in scenarios:
        print(f"   • {s['name']}: {s['action']}")
    
    print(f"\n👑 تقرير السيد أحمد:")
    report = rm.get_master_report()
    print(f"   تهديدات: {report['summary']['master_threats']}")
    print(f"   التوصية: {report['recommendations'][0][:80]}...")
    
    print(f"\n📋 إحصائيات:")
    status = rm.get_status()
    print(f"   إجمالي المخاطر: {status['total_risks']}")
    print(f"   تهديدات السيد: {status['master_threats']}")
    print(f"   تنبيهات: {status['master_alerts']}")
    
    print(f"\n🛡️ حماية السيد أحمد فوق كل شيء.")
    print("\n✅ محرك المخاطر الاستراتيجي جاهز.")
