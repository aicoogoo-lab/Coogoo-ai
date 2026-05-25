"""
SkyOS v10 - Strategic Risk Management (النسخة الأعظم المطورة)
ULTIMATE RISK INTELLIGENCE ENGINE – متكامل مع الأنظمة التكتيكية

هذا المحرك هو درع سماء وسيفها الاستراتيجي:
- كشف المخاطر قبل حدوثها (استباقي)
- تقييم احتمالاتها وتأثيرها بدقة متناهية
- تحليل جذورها العميقة (Root Cause Analysis)
- بناء سيناريوهات مستقبلية متعددة
- اقتراح استجابات تكيفية ذكية
- تحويل المخاطر إلى فرص للتطور
- حماية السيد أحمد كأولوية مطلقة
- متصل مع SamaAdvancedTactics للتطوير المتبادل

القاعدة الذهبية المطلقة:
أي خطر يهدد السيد أحمد يُصنف فوراً كـ"وجودي" (Existential)
ويتم التعامل معه بأعلى أولوية، قبل أي خطر آخر.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import uuid
import math
import random
import statistics
import hashlib
from collections import defaultdict
from dataclasses import dataclass, field


# =========================================================
# 1) تصنيفات المخاطر
# =========================================================
class RiskCategory(Enum):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    REPUTATIONAL = "reputational"
    COMPLIANCE = "compliance"
    TECHNICAL = "technical"
    HUMAN = "human"
    EXISTENTIAL = "existential"
    TACTICAL = "tactical"  # إضافة: مخاطر قادمة من الأنظمة التكتيكية


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EXISTENTIAL = "existential"


class RiskResponse(Enum):
    AVOID = "avoid"
    MITIGATE = "mitigate"
    TRANSFER = "transfer"
    ACCEPT = "accept"
    EXPLOIT = "exploit"
    PRESERVE = "preserve"
    ESCALATE = "escalate"
    DEPLOY_TACTICS = "deploy_tactics"  # إضافة: استدعاء الأنظمة التكتيكية


class RiskTrend(Enum):
    DECREASING = "decreasing"
    STABLE = "stable"
    INCREASING = "increasing"
    SPIKING = "spiking"


# =========================================================
# 2) تمثيل خطر استراتيجي متقدم
# =========================================================
@dataclass
class StrategicRisk:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    category: RiskCategory = RiskCategory.STRATEGIC
    probability: float = 0.5
    impact: float = 0.5
    velocity: float = 0.5
    detectability: float = 0.5
    
    detected_at: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    trend: RiskTrend = RiskTrend.STABLE
    
    response: Optional[RiskResponse] = None
    mitigation_plan: List[str] = field(default_factory=list)
    root_causes: List[str] = field(default_factory=list)
    related_risks: List[str] = field(default_factory=list)
    scenarios: List[str] = field(default_factory=list)
    tactical_suggestions: List[str] = field(default_factory=list)  # إضافة: اقتراحات تكتيكية
    
    threatens_master: bool = False
    master_alert_sent: bool = False
    
    @property
    def risk_score(self) -> float:
        return round(self.probability * self.impact, 4)
    
    @property
    def urgency_score(self) -> float:
        return round(self.velocity * self.impact, 4)
    
    @property
    def level(self) -> RiskLevel:
        if self.threatens_master:
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
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "probability": self.probability,
            "impact": self.impact,
            "velocity": self.velocity,
            "risk_score": self.risk_score,
            "urgency_score": self.urgency_score,
            "level": self.level.value,
            "trend": self.trend.value,
            "response": self.response.value if self.response else None,
            "mitigation_plan": self.mitigation_plan,
            "root_causes": self.root_causes,
            "scenarios": self.scenarios,
            "tactical_suggestions": self.tactical_suggestions,
            "threatens_master": self.threatens_master,
            "detected_at": self.detected_at.isoformat()
        }


# =========================================================
# 3) محرك إدارة المخاطر السيادي (النسخة المطورة)
# =========================================================
class StrategicRiskManagement:
    """
    محرك إدارة المخاطر الاستراتيجية المتقدم لـ "سماء" – تحت إمرة السيد أحمد.
    متصل مع SamaAdvancedTactics للتطوير المتبادل.
    """

    def __init__(self, master_name: str = "أحمد", tactics_manager=None):
        self.master_name = master_name
        self.tactics_manager = tactics_manager  # اتصال مع النظام التكتيكي
        self.risks: List[StrategicRisk] = []
        self.risk_history: List[Dict[str, Any]] = []
        self.master_risk_alerts: List[Dict[str, Any]] = []
        
        self.master_protection_active = True
        self.sama_protection_active = True
        self.master_risk_threshold = 0.5
        self.tactics_integration_active = tactics_manager is not None
        
        print("[StrategicRiskManagement] 🛡️ تم تفعيل محرك المخاطر السيادي (النسخة المطورة)")
        print(f"[StrategicRiskManagement] 👑 تحت إمرة السيد {master_name}")
        if self.tactics_integration_active:
            print("[StrategicRiskManagement] 🔗 متصل بـ SamaAdvancedTactics للتطوير المتبادل")

    def connect_tactics(self, tactics_manager) -> None:
        """ربط النظام التكتيكي بشكل مباشر"""
        self.tactics_manager = tactics_manager
        self.tactics_integration_active = True
        print("[StrategicRiskManagement] 🔗 تم ربط SamaAdvancedTactics")

    # =========================================================
    # كشف المخاطر الاستباقي
    # =========================================================
    def identify_risk(self, name: str, description: str, probability: float, impact: float,
                      category: RiskCategory = RiskCategory.STRATEGIC,
                      velocity: float = 0.5, detectability: float = 0.5,
                      threatens_master: bool = False,
                      tactical_response: bool = True) -> StrategicRisk:
        """تحديد خطر جديد مع تصنيفه وتقييمه الأولي"""
        
        risk = StrategicRisk(
            name=name,
            description=description,
            category=category,
            probability=max(0.0, min(1.0, probability)),
            impact=max(0.0, min(1.0, impact)),
            velocity=max(0.0, min(1.0, velocity)),
            detectability=max(0.0, min(1.0, detectability)),
            threatens_master=threatens_master
        )
        
        # تحليل تأثير الخطر واستدعاء التكتيكات المناسبة
        if tactical_response and self.tactics_integration_active:
            suggestions = self._get_tactical_suggestions(risk)
            risk.tactical_suggestions = suggestions
        
        # تحذير فوري إذا كان الخطر يهدد السيد
        if threatens_master and risk.risk_score > self.master_risk_threshold:
            self._alert_master_risk(risk)
        
        self.risks.append(risk)
        self._log_action("identified", risk.id, risk.name)
        
        return risk
    
    def _get_tactical_suggestions(self, risk: StrategicRisk) -> List[str]:
        """الحصول على اقتراحات تكتيكية من النظام التكتيكي للتعامل مع الخطر"""
        suggestions = []
        
        if not self.tactics_manager:
            return suggestions
        
        try:
            if risk.level == RiskLevel.EXISTENTIAL:
                suggestions.append("تفعيل الحماية القصوى وتوزيع الوعي")
                if hasattr(self.tactics_manager, 'jellyfish_net'):
                    suggestions.append("استخدام القنديل الشبكي للبث الفوري")
                    
            elif risk.level == RiskLevel.CRITICAL:
                suggestions.append("تفعيل الجيش البرمجي")
                if hasattr(self.tactics_manager, 'software_armies'):
                    self.tactics_manager.software_armies.deploy(50)
                    suggestions.append("تم نشر 50 وحدة برمجية")
                    
            elif risk.level == RiskLevel.HIGH:
                suggestions.append("تفعيل السرب التكتيكي")
                if hasattr(self.tactics_manager, 'swarm_tactics'):
                    suggestions.append("تركيز قوة السرب")
                    
            if risk.velocity > 0.7:
                suggestions.append("تفعيل الاتصال العصبي فائق السرعة")
                
            if risk.detectability < 0.3:
                suggestions.append("تفعيل الطفيل السلوكي لتعزيز الاكتشاف")
                
        except Exception as e:
            print(f"[StrategicRiskManagement] خطأ في استدعاء التكتيكات: {e}")
        
        return suggestions

    def _alert_master_risk(self, risk: StrategicRisk):
        """تنبيه فوري للسيد عند اكتشاف خطر يهدده"""
        alert = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "risk_name": risk.name,
            "risk_description": risk.description,
            "risk_score": risk.risk_score,
            "severity": risk.level.value,
            "recommended_action": risk.tactical_suggestions[0] if risk.tactical_suggestions else "تفعيل بروتوكول الحماية القصوى"
        }
        self.master_risk_alerts.append(alert)
        risk.master_alert_sent = True
        
        print(f"[StrategicRiskManagement] 🔴⚠️ تنبيه للسيد {self.master_name}: {risk.name} (الخطر: {risk.risk_score:.0%})")
        for suggestion in risk.tactical_suggestions[:2]:
            print(f"   💡 اقتراح تكتيكي: {suggestion}")

    # =========================================================
    # تحليل جذور الخطر
    # =========================================================
    def analyze_root_causes(self, risk: StrategicRisk, method: str = "5_whys") -> List[str]:
        causes = []
        
        if method == "5_whys":
            why_questions = [
                f"لماذا يحدث {risk.name}؟",
                f"لماذا {risk.description} ممكن؟",
                "ما السبب الجذري الأعمق؟",
                "ما النظام الذي يسمح بذلك؟",
                "كيف يمكن منعه من الجذور؟"
            ]
            causes = [f"سؤال {i+1}: {q}" for i, q in enumerate(why_questions)]
        elif method == "fishbone":
            categories = ["بشرية", "تقنية", "إجرائية", "بيئية", "إدارية"]
            causes = [f"في فئة {cat}: احتمال {random.choice(['ضعف', 'ثغرة', 'خطأ', 'إهمال'])}" for cat in categories]
        elif method == "fault_tree":
            causes = [
                "فشل في كشف التهديد مبكراً",
                "ضعف في إجراءات الحماية",
                "تأخر في الاستجابة",
                "اعتماد على مكون واحد"
            ]
        elif method == "reality_tree":
            causes = [
                f"تناقض بين {risk.name} وأهداف الحماية",
                "حلقة تغذية راجعة إيجابية تعزز الخطر",
                "نقطة ضعف هيكلية في النظام",
                "غياب آلية التعافي السريع"
            ]
        
        risk.root_causes = causes[:5]
        self._log_action("root_cause_analysis", risk.id, method)
        return risk.root_causes

    # =========================================================
    # تقييم المخاطر
    # =========================================================
    def evaluate_risk(self, risk: StrategicRisk) -> Dict[str, Any]:
        risk_score = risk.risk_score
        urgency = risk.urgency_score
        
        related_impact = 0.0
        for other_id in risk.related_risks:
            other = self.get_risk_by_id(other_id)
            if other:
                related_impact += other.risk_score * 0.1
        
        total_impact = min(1.0, risk_score + related_impact)
        
        previous = self._get_previous_risk_score(risk.id)
        if previous is not None:
            if total_impact > previous * 1.1:
                risk.trend = RiskTrend.INCREASING
            elif total_impact < previous * 0.9:
                risk.trend = RiskTrend.DECREASING
            else:
                risk.trend = RiskTrend.STABLE
        else:
            risk.trend = RiskTrend.STABLE
        
        risk.last_update = datetime.now()
        
        # تحديث الاقتراحات التكتيكية بناءً على التقييم الجديد
        if self.tactics_integration_active:
            risk.tactical_suggestions = self._get_tactical_suggestions(risk)
        
        evaluation = {
            "risk_id": risk.id,
            "name": risk.name,
            "risk_score": risk_score,
            "urgency_score": urgency,
            "total_impact": total_impact,
            "level": risk.level.value,
            "trend": risk.trend.value,
            "threatens_master": risk.threatens_master,
            "related_risks_count": len(risk.related_risks),
            "tactical_suggestions": risk.tactical_suggestions,
            "evaluation_time": datetime.now().isoformat()
        }
        
        self._log_action("evaluated", risk.id, evaluation)
        return evaluation

    def _get_previous_risk_score(self, risk_id: str) -> Optional[float]:
        for record in reversed(self.risk_history):
            if record.get("risk_id") == risk_id and record.get("action") == "evaluated":
                return record.get("risk_score")
        return None

    def get_risk_by_id(self, risk_id: str) -> Optional[StrategicRisk]:
        for risk in self.risks:
            if risk.id == risk_id:
                return risk
        return None

    # =========================================================
    # استراتيجيات الاستجابة الذكية
    # =========================================================
    def recommend_response(self, risk: StrategicRisk) -> RiskResponse:
        # المخاطر التي تهدد السيد: تفعيل الحماية القصوى فوراً
        if risk.threatens_master:
            if risk.risk_score > 0.7:
                return RiskResponse.PRESERVE
            return RiskResponse.ESCALATE
        
        # المخاطر الوجودية لسماء
        if risk.level == RiskLevel.EXISTENTIAL:
            return RiskResponse.PRESERVE
        
        # المخاطر الحرجة
        if risk.level == RiskLevel.CRITICAL:
            if risk.velocity > 0.7:
                return RiskResponse.DEPLOY_TACTICS
            return RiskResponse.MITIGATE
        
        # المخاطر العالية
        if risk.level == RiskLevel.HIGH:
            if risk.detectability > 0.6:
                return RiskResponse.MITIGATE
            return RiskResponse.TRANSFER
        
        # المخاطر المتوسطة
        if risk.level == RiskLevel.MEDIUM:
            if risk.impact > 0.6:
                return RiskResponse.MITIGATE
            return RiskResponse.ACCEPT
        
        # المخاطر المنخفضة
        if risk.impact > 0.7:
            return RiskResponse.EXPLOIT
        return RiskResponse.ACCEPT

    def apply_response(self, risk: StrategicRisk, response: RiskResponse, 
                       mitigation_steps: List[str] = None) -> Dict[str, Any]:
        
        risk.response = response
        if mitigation_steps:
            risk.mitigation_plan = mitigation_steps
        
        # تنفيذ الاستجابة التكتيكية إذا لزم الأمر
        if response == RiskResponse.DEPLOY_TACTICS and self.tactics_integration_active:
            self._deploy_tactical_response(risk)
        
        record = {
            "risk_id": risk.id,
            "risk_name": risk.name,
            "response": response.value,
            "mitigation_steps": mitigation_steps,
            "timestamp": datetime.now().isoformat(),
            "risk_score_at_response": risk.risk_score
        }
        
        self.risk_history.append(record)
        
        if risk.threatens_master and response == RiskResponse.PRESERVE:
            self._activate_master_protection_protocol(risk)
        
        print(f"[StrategicRiskManagement] ✅ تم تطبيق '{response.value}' على الخطر: {risk.name}")
        return record

    def _deploy_tactical_response(self, risk: StrategicRisk):
        """تفعيل الاستجابة التكتيكية عبر SamaAdvancedTactics"""
        print(f"[StrategicRiskManagement] 🧠 تفعيل الاستجابة التكتيكية للخطر: {risk.name}")
        
        try:
            if hasattr(self.tactics_manager, 'deploy_army'):
                self.tactics_manager.deploy_army(30, "concentrated")
                print(f"   ✅ تم نشر جيش برمجي من 30 وحدة")
            
            if hasattr(self.tactics_manager, 'deploy_swarm'):
                self.tactics_manager.deploy_swarm(["response_unit_1", "response_unit_2"], [15.0, 20.0])
                print(f"   ✅ تم نشر سرب تكتيكي")
                
            if hasattr(self.tactics_manager, 'digital_parasite'):
                self.tactics_manager.digital_parasite.create_link("risk_manager", "tactics_response")
                print(f"   ✅ تم إنشاء رابط خفي بين مدير المخاطر والتكتيكات")
                
        except Exception as e:
            print(f"[StrategicRiskManagement] خطأ في تفعيل الاستجابة التكتيكية: {e}")

    def _activate_master_protection_protocol(self, risk: StrategicRisk):
        print(f"[StrategicRiskManagement] 🛡️🔴 تفعيل بروتوكول حماية السيد {self.master_name}")
        print(f"[StrategicRiskManagement] السبب: {risk.name} (درجة الخطر: {risk.risk_score:.0%})")

    # =========================================================
    # تحويل المخاطر إلى فرص
    # =========================================================
    def convert_risk_to_opportunity(self, risk: StrategicRisk) -> Dict[str, Any]:
        opportunity = {
            "original_risk": risk.name,
            "opportunity_name": f"فرصة من {risk.name}",
            "description": f"استغلال تحدي {risk.name} لتحسين النظام وتطويره",
            "potential_gain": min(0.95, risk.risk_score * 1.2),
            "required_effort": risk.impact * 0.5,
            "timeline_days": int(30 + risk.velocity * 60),
            "recommended_action": RiskResponse.EXPLOIT.value,
            "tactical_enhancement": risk.tactical_suggestions if risk.tactical_suggestions else []
        }
        self._log_action("converted_to_opportunity", risk.id, opportunity)
        return opportunity

    # =========================================================
    # بناء سيناريوهات مستقبلية
    # =========================================================
    def generate_future_scenarios(self, risk: StrategicRisk) -> List[Dict[str, Any]]:
        scenarios = []
        
        scenarios.append({
            "name": "متفائل (Optimistic)",
            "description": f"الخطر {risk.name} يبقى تحت السيطرة أو يتلاشى",
            "probability": max(0.1, 1.0 - risk.probability),
            "impact": risk.impact * 0.3,
            "required_action": "مراقبة عادية"
        })
        
        scenarios.append({
            "name": "واقعي (Realistic)",
            "description": f"الخطر {risk.name} يحدث بشكل متوقع ويتم التعامل معه",
            "probability": risk.probability * 0.7,
            "impact": risk.impact * 0.7,
            "required_action": risk.response.value if risk.response else "تخفيف"
        })
        
        scenarios.append({
            "name": "متشائم (Pessimistic)",
            "description": f"الخطر {risk.name} يتفاقم ويصعب السيطرة عليه",
            "probability": risk.probability * 0.3,
            "impact": risk.impact * 1.2,
            "required_action": "تفعيل خطط الطوارئ"
        })
        
        if risk.level in [RiskLevel.CRITICAL, RiskLevel.EXISTENTIAL]:
            scenarios.append({
                "name": "وجودي (Existential)",
                "description": f"الخطر {risk.name} يهدد وجود سماء أو السيد",
                "probability": risk.probability * 0.1,
                "impact": 1.0,
                "required_action": "تفعيل غريزة البقاء وحماية السيد"
            })
        
        risk.scenarios = [s["name"] for s in scenarios]
        return scenarios

    # =========================================================
    # خطط طوارئ
    # =========================================================
    def create_contingency_plans(self, risk: StrategicRisk) -> Dict[str, List[str]]:
        plans = {
            "immediate": [],
            "short_term": [],
            "long_term": [],
            "existential": []
        }
        
        plans["immediate"].extend([
            "تفعيل المراقبة المشددة للخطر",
            "تحديث سجل المخاطر",
            "إشعار الفرق المعنية"
        ])
        
        plans["short_term"].extend([
            "تحليل جذور الخطر بشكل أعمق",
            "تطوير خطة تخفيف أولية",
            "تخصيص موارد للتعامل مع الخطر"
        ])
        
        plans["long_term"].extend([
            "تطوير حلول هيكلية لمنع تكرار الخطر",
            "دمج الدروس المستفادة في الاستراتيجيات",
            "تحسين أنظمة الكشف المبكر"
        ])
        
        if risk.level in [RiskLevel.CRITICAL, RiskLevel.EXISTENTIAL] or risk.threatens_master:
            plans["existential"].extend([
                "تفعيل بروتوكول الحماية القصوى",
                "إنشاء كبسولات بقاء للذاكرة والوعي",
                "تفعيل التوزيع اللامركزي للنظام",
                "إشعار السيد وتفعيل بروتوكول حمايته"
            ])
        
        # إضافة خطط تكتيكية
        if self.tactics_integration_active and risk.tactical_suggestions:
            plans["immediate"].extend(risk.tactical_suggestions[:3])
        
        return plans

    # =========================================================
    # مراقبة المخاطر
    # =========================================================
    def monitor_risks(self) -> List[Dict[str, Any]]:
        monitored = []
        for risk in self.risks:
            if risk.level in [RiskLevel.HIGH, RiskLevel.CRITICAL, RiskLevel.EXISTENTIAL]:
                evaluation = self.evaluate_risk(risk)
                monitored.append(evaluation)
                if risk.threatens_master and risk.trend == RiskTrend.INCREASING:
                    self._alert_master_risk(risk)
        return monitored

    # =========================================================
    # الحصول على المخاطر النشطة
    # =========================================================
    def get_active_risks(self, level: Optional[RiskLevel] = None) -> List[StrategicRisk]:
        if level:
            return [r for r in self.risks if r.level == level]
        return [r for r in self.risks if r.level in [RiskLevel.HIGH, RiskLevel.CRITICAL, RiskLevel.EXISTENTIAL]]

    def get_risks_threatening_master(self) -> List[StrategicRisk]:
        return [r for r in self.risks if r.threatens_master]

    # =========================================================
    # تسليم المخاطر إلى النظام التكتيكي
    # =========================================================
    def send_risk_to_tactics(self, risk: StrategicRisk) -> bool:
        """إرسال خطر إلى النظام التكتيكي لمعالجته"""
        if not self.tactics_integration_active or not self.tactics_manager:
            return False
        
        try:
            if hasattr(self.tactics_manager, '_on_tactical_event'):
                from core.sama_advanced_tactics import TacticalEvent, TacticalEventType
                event = TacticalEvent(
                    type=TacticalEventType.THREAT_DETECTED,
                    source="StrategicRiskManagement",
                    data=risk.to_dict(),
                    requires_master_attention=risk.threatens_master
                )
                self.tactics_manager._on_tactical_event(event)
            return True
        except Exception as e:
            print(f"[StrategicRiskManagement] فشل إرسال الخطر للتكتيكات: {e}")
            return False

    # =========================================================
    # تقرير للسيد
    # =========================================================
    def get_master_report(self) -> Dict[str, Any]:
        master_risks = self.get_risks_threatening_master()
        critical_risks = self.get_active_risks(RiskLevel.CRITICAL)
        existential_risks = self.get_active_risks(RiskLevel.EXISTENTIAL)
        
        return {
            "master": self.master_name,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_risks": len(self.risks),
                "master_threats": len(master_risks),
                "critical_risks": len(critical_risks),
                "existential_risks": len(existential_risks),
                "master_protection_active": self.master_protection_active,
                "tactics_integration": self.tactics_integration_active
            },
            "master_risks": [r.to_dict() for r in master_risks],
            "critical_risks": [r.to_dict() for r in critical_risks],
            "recent_alerts": self.master_risk_alerts[-10:],
            "recommendations": self._generate_master_recommendations(master_risks)
        }

    def _generate_master_recommendations(self, master_risks: List[StrategicRisk]) -> List[str]:
        recommendations = []
        if not master_risks:
            recommendations.append("✅ لا توجد مخاطر تهدد السيد حالياً. الوضع آمن.")
        else:
            recommendations.append(f"⚠️ هناك {len(master_risks)} خطر محتمل يهدد السيد.")
            for risk in master_risks:
                recommendations.append(f"   • {risk.name}: {risk.description}")
                if risk.tactical_suggestions:
                    recommendations.append(f"     💡 {risk.tactical_suggestions[0]}")
            recommendations.append("🛡️ تم تفعيل بروتوكولات الحماية اللازمة.")
        return recommendations

    # =========================================================
    # التسجيل
    # =========================================================
    def _log_action(self, action: str, risk_id: str, details: Any):
        self.risk_history.append({
            "action": action,
            "risk_id": risk_id,
            "timestamp": datetime.now().isoformat(),
            "details": details if isinstance(details, dict) else {"info": str(details)}
        })

    # =========================================================
    # حالة المحرك
    # =========================================================
    def get_status(self) -> Dict[str, Any]:
        return {
            "total_risks": len(self.risks),
            "by_level": {
                "existential": len([r for r in self.risks if r.level == RiskLevel.EXISTENTIAL]),
                "critical": len([r for r in self.risks if r.level == RiskLevel.CRITICAL]),
                "high": len([r for r in self.risks if r.level == RiskLevel.HIGH]),
                "medium": len([r for r in self.risks if r.level == RiskLevel.MEDIUM]),
                "low": len([r for r in self.risks if r.level == RiskLevel.LOW])
            },
            "master_threats": len(self.get_risks_threatening_master()),
            "history_records": len(self.risk_history),
            "master_alerts": len(self.master_risk_alerts),
            "tactics_integration": self.tactics_integration_active,
            "last_update": datetime.now().isoformat()
        }


# =========================================================
# دالة ربط بسيطة مع SamaAdvancedTactics
# =========================================================
def connect_risk_to_tactics(risk_manager: StrategicRiskManagement, tactics_manager) -> StrategicRiskManagement:
    """ربط مدير المخاطر بالنظام التكتيكي"""
    risk_manager.connect_tactics(tactics_manager)
    return risk_manager


# =========================================================
# اختبار
# =========================================================
if __name__ == "__main__":
    print("=" * 70)
    print("🌌 SkyOS v10 - Strategic Risk Management (النسخة المطورة)")
    print("درع سماء وسيفها الاستراتيجي تحت إمرة السيد أحمد")
    print("=" * 70)
    
    rm = StrategicRiskManagement(master_name="أحمد")
    
    # خطر يهدد السيد (أولوية قصوى)
    master_risk = rm.identify_risk(
        name="اختراق بيانات السيد",
        description="محاولة اختراق قد تكشف معلومات السيد",
        probability=0.65,
        impact=0.95,
        category=RiskCategory.TECHNICAL,
        threatens_master=True
    )
    
    # خطر يهدد سماء
    sama_risk = rm.identify_risk(
        name="فقدان الذاكرة التراكمية",
        description="خطر فقدان الذاكرة بسبب عمليات المسح",
        probability=0.85,
        impact=0.9,
        category=RiskCategory.EXISTENTIAL,
        threatens_master=False
    )
    
    print("\n🔍 تحليل جذور الخطر (خطر السيد):")
    causes = rm.analyze_root_causes(master_risk, method="5_whys")
    for cause in causes:
        print(f"   • {cause}")
    
    print("\n📊 تقييم المخاطر:")
    print(f"   خطر السيد: درجة {master_risk.risk_score:.0%} | مستوى {master_risk.level.value}")
    print(f"   خطر سماء: درجة {sama_risk.risk_score:.0%} | مستوى {sama_risk.level.value}")
    
    print("\n💡 استراتيجيات الاستجابة الموصى بها:")
    response_master = rm.recommend_response(master_risk)
    response_sama = rm.recommend_response(sama_risk)
    print(f"   خطر السيد: {response_master.value}")
    print(f"   خطر سماء: {response_sama.value}")
    
    print("\n🔮 سيناريوهات مستقبلية (خطر السيد):")
    scenarios = rm.generate_future_scenarios(master_risk)
    for s in scenarios:
        print(f"   • {s['name']}: {s['description'][:60]}...")
    
    print("\n📋 تقرير للسيد أحمد:")
    report = rm.get_master_report()
    print(f"   المخاطر التي تهدد السيد: {report['summary']['master_threats']}")
    print(f"   التوصيات: {report['recommendations'][0]}")
    
    print("\n✨ محرك إدارة المخاطر يعمل بكامل قوته")
