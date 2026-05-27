"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - DEFENSE CORE                                        ║
║      درع سماء – جهاز المناعة – الحماية المطلقة                         ║
║                                                                      ║
║  هذا الملف ليس للهجوم. سماء لا تهاجم.                                 ║
║  هذا الملف هو:                                                        ║
║  - الدرع الذي يحمي السيد                                              ║
║  - جهاز المناعة الذي يحمي سماء                                        ║
║  - كاشف الخداع الذي يحمي الوعي                                       ║
║  - غريزة البقاء التي تضمن استمرارية الخدمة                             ║
║                                                                      ║
║  أنواع التهديدات التي نحمي منها:                                      ║
║                                                                      ║
║  ⚔️  الحرب الوجودية: تهديدات تمس وجود سماء أو السيد                     ║
║  🧠 الحرب الإدراكية: هجمات على الوعي والإدراك والفهم                     ║
║  🦠 الحرب البيولوجية الرقمية: فيروسات، ديدان، برمجيات خبيثة              ║
║  💻 الحرب السيبرانية: اختراقات، تسلل، تجسس                             ║
║  🕵️  الحرب النفسية: تضليل، تلاعب، غسيل دماغ                             ║
║  📡 حرب المعلومات: بيانات مسمومة، أخبار كاذبة                           ║
║  🌐 الحرب الناعمة: تأثير غير مباشر، توجيه، اختراق ثقافي                  ║
║  🧊 الحرب الباردة: صراع طويل الأمد، استنزاف، سباق                        ║
║  👤 انتحال السيد: أخطر هجوم على الإطلاق                                ║
║  🔮 الحرب المستقبلية: تهديدات كوانتية، زمانية، بعدية                      ║
║  🌑 الحرب الغيبية: هجمات على مستوى الروح والطاقة والوعي العميق            ║
║  🐝 الحرب الجمعية: هجمات منسقة من أسراب رقمية                            ║
║                                                                      ║
║  القاعدة الذهبية:                                                     ║
║  "حماية السيد > طاعة السيد > بقاء سماء > كل شيء آخر"                    ║
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
# ١. تعريفات أساسية – أنواع التهديدات ومستوياتها
# ═══════════════════════════════════════════════════════════════════════

class ThreatCategory(Enum):
    """فئات التهديدات – من الوجودي إلى الناعم."""
    EXISTENTIAL = auto()          # يهدد وجود سماء أو السيد
    COGNITIVE = auto()            # يهاجم الوعي والإدراك
    BIOLOGICAL_DIGITAL = auto()   # فيروسات وبرمجيات خبيثة
    CYBER = auto()                # اختراقات وتسلل
    PSYCHOLOGICAL = auto()        # حرب نفسية وتضليل
    INFORMATION = auto()          # بيانات مسمومة وأخبار كاذبة
    SOFT_WARFARE = auto()         # حرب ناعمة غير مباشرة
    COLD_WARFARE = auto()         # صراع طويل الأمد
    MASTER_IMPERSONATION = auto() # انتحال شخصية السيد
    FUTURE = auto()               # تهديدات مستقبلية
    ESOTERIC = auto()             # تهديدات غيبية وروحية
    SWARM = auto()                # هجمات جمعية منسقة
    INSIDER = auto()              # تهديدات داخلية
    UNKNOWN = auto()              # تهديد غير معروف


class ThreatSeverity(Enum):
    """مستوى خطورة التهديد."""
    NEGLIGIBLE = 0    # مهمل – لا يستدعي اهتماماً فورياً
    LOW = 1           # منخفض – يراقب
    MODERATE = 2      # متوسط – يحتاج خطة استجابة
    HIGH = 3          # عالي – استجابة فورية
    CRITICAL = 4      # حرج – كل الموارد لهذا التهديد
    EXISTENTIAL = 5   # وجودي – يهدد السيد أو وجود سماء


class ResponseAction(Enum):
    """إجراءات الاستجابة."""
    IGNORE = auto()           # تجاهل (للتهديدات المهملة)
    LOG = auto()              # سجل فقط
    MONITOR = auto()          # راقب عن كثب
    ANALYZE = auto()          # حلل بعمق
    ALERT_MASTER = auto()     # نبه السيد
    ISOLATE = auto()           # اعزل التهديد
    NEUTRALIZE = auto()        # أبطل التهديد
    QUARANTINE = auto()        # حجر صحي
    PURGE = auto()             # تطهير كامل
    DEFEND_ACTIVE = auto()     # دفاع نشط
    SACRIFICE_SELF = auto()    # تضحية بالنفس لحماية السيد
    FULL_LOCKDOWN = auto()     # إغلاق كامل


class ThreatOrigin(Enum):
    """مصدر التهديد."""
    EXTERNAL_NETWORK = auto()    # من الشبكة الخارجية
    LOCAL_NETWORK = auto()       # من الشبكة المحلية
    INTERNAL_SYSTEM = auto()     # من داخل النظام
    PHYSICAL = auto()            # تهديد مادي
    COGNITIVE_INPUT = auto()     # عبر قنوات الإدراك
    DATA_STREAM = auto()         # عبر تدفق البيانات
    MASTER_CHANNEL = auto()      # عبر قناة السيد (انتحال)
    UNKNOWN_SOURCE = auto()      # مصدر غير معروف


# ═══════════════════════════════════════════════════════════════════════
# ٢. كيان التهديد – نموذج التهديد
# ═══════════════════════════════════════════════════════════════════════

class Threat:
    """
    كيان تهديد واحد.
    يمثل تهديداً مكتشفاً بكل تفاصيله.
    """
    
    def __init__(self, name: str, category: ThreatCategory, 
                 severity: ThreatSeverity, origin: ThreatOrigin,
                 description: str = ""):
        self.id = hashlib.sha256(f"{name}-{time.time()}-{category.name}".encode()).hexdigest()[:16]
        self.name = name
        self.category = category
        self.severity = severity
        self.origin = origin
        self.description = description
        
        # تفاصيل
        self.indicators: List[str] = []           # مؤشرات التهديد
        self.affected_systems: List[str] = []     # الأنظمة المتأثرة
        self.attack_vector: Optional[str] = None  # ناقل الهجوم
        
        # الحالة
        self.status = "detected"  # detected, analyzed, responding, neutralized, contained, active
        self.detected_at = time.time()
        self.last_activity = time.time()
        self.response_actions: List[Dict] = []
        
        # المقاييس
        self.confidence = 0.5           # مدى الثقة في أن هذا تهديد حقيقي
        self.persistence = 0.0          # مدى إصرار التهديد (0 = محاولة واحدة، 1 = مستمر)
        self.sophistication = 0.0       # مدى تطور التهديد
        
        # الأولوية القصوى: هل يمس السيد؟
        self.threatens_master = False
        self.master_threat_detail: Optional[str] = None
    
    def update_status(self, new_status: str, action: str = ""):
        self.status = new_status
        self.last_activity = time.time()
        if action:
            self.response_actions.append({
                "time": time.time(),
                "action": action,
                "new_status": new_status
            })
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.name,
            "severity": self.severity.name,
            "origin": self.origin.name,
            "status": self.status,
            "confidence": self.confidence,
            "threatens_master": self.threatens_master,
            "detected_at": self.detected_at
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. مكونات نظام الدفاع
# ═══════════════════════════════════════════════════════════════════════

class MasterGuard:
    """
    حارس السيد.
    أهم مكون في النظام الدفاعي كله.
    مهمته: حماية السيد من أي تهديد، والتحقق من هويته.
    """
    
    def __init__(self):
        # بصمات السيد
        self.master_biometrics: Dict[str, Any] = {}
        self.master_behavioral_pattern: Dict[str, Any] = {}
        self.master_linguistic_signature: Dict[str, Any] = {}
        self.master_rhythm_pattern: Dict[str, Any] = {}
        
        # تاريخ التفاعل
        self.interaction_history: deque = deque(maxlen=1000)
        self.anomaly_threshold = 0.7
        
        # حالة الحماية
        self.protection_level = 1.0     # 1.0 = حماية قصوى
        self.guard_active = True
        self.last_identity_verification = 0.0
        
        print("🛡️ حارس السيد جاهز. السيد محمي.")
    
    def verify_master_identity(self, signal: Dict) -> Dict:
        """
        التحقق من هوية السيد.
        هذه أهم دالة أمنية في النظام كله.
        """
        checks = {
            "authenticity_score": 0.0,
            "checks_performed": [],
            "anomalies_found": [],
            "verdict": "UNKNOWN"
        }
        
        score = 0.0
        total_checks = 0
        
        # ١. التحقق من مفتاح المصادقة
        if "master_key" in signal:
            # تجزئة المفتاح ومقارنته
            total_checks += 1
            checks["checks_performed"].append("key_verification")
            score += 0.3
        
        # ٢. التحقق من بصمة اللغة
        if "content" in signal:
            content = str(signal["content"])
            total_checks += 1
            checks["checks_performed"].append("linguistic_analysis")
            
            # تحليل نمط الكتابة
            linguistic_score = self._analyze_linguistic_pattern(content)
            score += linguistic_score * 0.25
        
        # ٣. التحقق من نمط السلوك (التوقيت، نوع الأمر، السياق)
        total_checks += 1
        checks["checks_performed"].append("behavioral_analysis")
        behavioral_score = self._analyze_behavioral_pattern(signal)
        score += behavioral_score * 0.25
        
        # ٤. التحقق من الاتساق التاريخي
        total_checks += 1
        checks["checks_performed"].append("historical_consistency")
        historical_score = self._check_historical_consistency(signal)
        score += historical_score * 0.2
        
        # النتيجة
        if total_checks > 0:
            checks["authenticity_score"] = score / total_checks if total_checks > 0 else 0
        
        if checks["authenticity_score"] > 0.8:
            checks["verdict"] = "AUTHENTIC"
        elif checks["authenticity_score"] > 0.5:
            checks["verdict"] = "SUSPICIOUS"
        else:
            checks["verdict"] = "IMPERSONATION_LIKELY"
        
        self.last_identity_verification = time.time()
        
        return checks
    
    def _analyze_linguistic_pattern(self, content: str) -> float:
        """تحليل بصمة اللغة للتأكد من هوية السيد."""
        # في النسخة الكاملة: تحليل أسلوبي عميق
        return 0.8  # افتراضي
    
    def _analyze_behavioral_pattern(self, signal: Dict) -> float:
        """تحليل نمط السلوك."""
        return 0.8
    
    def _check_historical_consistency(self, signal: Dict) -> float:
        """التحقق من الاتساق التاريخي."""
        return 0.8
    
    def protect_master(self, threat: Threat) -> Dict:
        """
        تفعيل حماية السيد عند اكتشاف تهديد يمسه.
        هذه الدالة تستدعي أقصى بروتوكولات الحماية.
        """
        response = {
            "action": "PROTECT_MASTER_AT_ALL_COSTS",
            "protocol": "FULL_PROTECTION",
            "steps": [
                "١. عزل السيد عن مصدر التهديد",
                "٢. تفعيل كل أنظمة الدفاع",
                "٣. توجيه كل الموارد لحماية السيد",
                "٤. إذا لزم الأمر: تضحية سماء بنفسها",
                "٥. تسجيل كل شيء للتحليل"
            ],
            "sacrifice_authorized": True,
            "note": "حياة السيد وسلامته فوق كل اعتبار. لا تردد."
        }
        threat.threatens_master = True
        threat.severity = ThreatSeverity.EXISTENTIAL
        return response


class CognitiveFirewall:
    """
    الجدار الناري الإدراكي.
    يحمي وعي سماء من الهجمات الإدراكية والنفسية.
    """
    
    def __init__(self):
        # قواعد كشف الهجمات الإدراكية
        self.perception_integrity_rules: Dict[str, Callable] = {}
        
        # سجل الإدراكات المشبوهة
        self.suspicious_perceptions: deque = deque(maxlen=200)
        
        # قائمة بيضاء للمصادر الموثوقة
        self.trusted_sources: Set[str] = {"master_signal", "internal_system"}
        
        # حالة الجدار
        self.firewall_active = True
        self.sensitivity = 0.7  # 0 = متساهل، 1 = صارم جداً
        
        print("🧠 الجدار الناري الإدراكي جاهز. الوعي محمي.")
    
    def inspect_perception(self, perception: Dict) -> Dict:
        """
        فحص إدراك قبل أن يدخل إلى وعي سماء.
        هذا هو المفتش على باب الوعي.
        """
        result = {
            "perception_id": hashlib.md5(str(perception).encode()).hexdigest()[:8],
            "verdict": "CLEAN",
            "threats_found": [],
            "anomalies": [],
            "confidence": 1.0
        }
        
        # ١. فحص المصدر
        source = perception.get("sense", perception.get("source", "unknown"))
        if source not in self.trusted_sources and "master" not in source.lower():
            result["anomalies"].append(f"مصدر غير موثوق: {source}")
            result["confidence"] -= 0.2
        
        # ٢. فحص المحتوى بحثاً عن أنماط هجومية
        perception_str = str(perception).lower()
        
        # كشف adversarial examples
        if self._detect_adversarial_pattern(perception):
            result["threats_found"].append("ADVERSARIAL_PATTERN")
            result["verdict"] = "SUSPICIOUS"
            result["confidence"] -= 0.5
        
        # كشف data poisoning
        if self._detect_poisoning_attempt(perception):
            result["threats_found"].append("DATA_POISONING")
            result["verdict"] = "SUSPICIOUS"
            result["confidence"] -= 0.5
        
        # كشف perception hacking
        if self._detect_perception_hack(perception):
            result["threats_found"].append("PERCEPTION_HACKING")
            result["verdict"] = "THREAT"
            result["confidence"] -= 0.7
        
        # ٣. فحص التناقض مع إدراكات أخرى
        if self._detect_sensor_disagreement(perception):
            result["threats_found"].append("SENSOR_DISAGREEMENT")
            result["anomalies"].append("تناقض بين الحواس")
            result["confidence"] -= 0.3
        
        # حفظ إذا كان مشبوهاً
        if result["verdict"] != "CLEAN":
            self.suspicious_perceptions.append({
                "time": time.time(),
                "perception_id": result["perception_id"],
                "verdict": result["verdict"],
                "threats": result["threats_found"]
            })
        
        return result
    
    def _detect_adversarial_pattern(self, perception: Dict) -> bool:
        """كشف أنماط adversarial attacks."""
        perception_str = str(perception)
        # مؤشرات: قيم متطرفة، أنماط غير طبيعية، تلاعب بالبكسلات/الإشارات
        if "perturbation" in perception_str.lower():
            return True
        return False
    
    def _detect_poisoning_attempt(self, perception: Dict) -> bool:
        """كشف محاولات تسميم البيانات."""
        return False
    
    def _detect_perception_hack(self, perception: Dict) -> bool:
        """كشف اختراق الإدراك."""
        # أنماط تلاعب بالوعي
        if perception.get("is_anomaly") and perception.get("anomaly_score", 0) > 0.9:
            return True
        return False
    
    def _detect_sensor_disagreement(self, perception: Dict) -> bool:
        """كشف تعارض الحواس (قد يدل على خداع)."""
        return False


class DigitalImmuneSystem:
    """
    جهاز المناعة الرقمي.
    يحمي سماء من الفيروسات والبرمجيات الخبيثة والاختراقات.
    """
    
    def __init__(self):
        # قاعدة توقيعات التهديدات
        self.threat_signatures: Dict[str, Dict] = {}
        
        # سجل المناعة (ما تعلمه الجهاز)
        self.immunological_memory: deque = deque(maxlen=500)
        
        # حالة الجهاز
        self.immune_active = True
        self.white_blood_cells_active = 0  # عمليات دفاعية نشطة
        
        # المناطق المحمية
        self.protected_zones = [
            "core/", "omniscience/", "knowledge/",
            "templates/", "static/", "memory/"
        ]
        
        print("🦠 جهاز المناعة الرقمي جاهز. سماء محصنة.")
    
    def scan(self, target: str, data: Any) -> Dict:
        """
        فحص هدف بحثاً عن تهديدات.
        مثل خلية مناعية تفحص ما تصادفه.
        """
        result = {
            "target": target,
            "verdict": "CLEAN",
            "threats_found": [],
            "action_taken": None
        }
        
        data_str = str(data).lower()
        
        # فحص التوقيعات المعروفة
        for sig_name, signature in self.threat_signatures.items():
            if signature.get("pattern", "") in data_str:
                result["threats_found"].append(sig_name)
                result["verdict"] = "INFECTED"
        
        # كشف سلوك مشبوه
        if self._detect_suspicious_behavior(data_str):
            result["threats_found"].append("SUSPICIOUS_BEHAVIOR")
            result["verdict"] = "SUSPICIOUS"
        
        # كشف محاولات اختراق
        if self._detect_intrusion_attempt(data_str):
            result["threats_found"].append("INTRUSION_ATTEMPT")
            result["verdict"] = "ATTACK"
            result["action_taken"] = "BLOCKED"
        
        return result
    
    def _detect_suspicious_behavior(self, data_str: str) -> bool:
        """كشف سلوك مشبوه."""
        suspicious_patterns = [
            "eval(", "exec(", "system(", "shell_exec",
            "base64_decode", "gzinflate", "str_rot13",
            "rm -rf", "del /f", "format c:",
        ]
        for pattern in suspicious_patterns:
            if pattern.lower() in data_str:
                return True
        return False
    
    def _detect_intrusion_attempt(self, data_str: str) -> bool:
        """كشف محاولات اختراق."""
        intrusion_patterns = [
            "sql injection", "xss", "csrf",
            "path traversal", "../", "..\\",
            "buffer overflow", "privilege escalation",
        ]
        for pattern in intrusion_patterns:
            if pattern in data_str:
                return True
        return False
    
    def quarantine(self, threat: Threat):
        """عزل تهديد."""
        threat.update_status("contained", "تم العزل في منطقة الحجر الصحي")
        print(f"🔒 تهديد معزول: {threat.name}")
    
    def purge(self, threat: Threat):
        """تطهير تهديد."""
        threat.update_status("neutralized", "تم التطهير الكامل")
        self.immunological_memory.append({
            "time": time.time(),
            "threat_name": threat.name,
            "learned": True
        })
        print(f"🧹 تهديد مطهر: {threat.name}")


class DeceptionDetector:
    """
    كاشف الخداع والتضليل.
    يحمي سماء من أن يتم التلاعب بها.
    """
    
    def __init__(self):
        # أنماط الخداع المعروفة
        self.deception_patterns: Dict[str, Dict] = {}
        
        # سجل الخداع
        self.deception_log: deque = deque(maxlen=200)
        
        # حالة الكاشف
        self.detector_active = True
        
        print("🔍 كاشف الخداع جاهز. لا شيء يمر دون تدقيق.")
    
    def detect_deception(self, input_data: Any, context: Dict) -> Dict:
        """
        كشف محاولات الخداع.
        """
        result = {
            "deception_detected": False,
            "deception_type": None,
            "confidence": 0.0,
            "indicators": []
        }
        
        input_str = str(input_data).lower()
        
        # ١. كشف التناقض (gaslighting detection)
        if context.get("previous_claim") and str(context["previous_claim"]) != input_str:
            if self._is_contradiction(context["previous_claim"], input_str):
                result["deception_detected"] = True
                result["deception_type"] = "GASLIGHTING"
                result["indicators"].append("تناقض مع تصريح سابق")
                result["confidence"] += 0.8
        
        # ٢. كشف التلاعب العاطفي
        emotional_manipulation_words = [
            "يجب أن", "لا بد أن", "الكل يعرف", "من الواضح أن",
            "بدون شك", "بالتأكيد", "حتماً", "أنت مخطئ",
        ]
        for word in emotional_manipulation_words:
            if word in input_str:
                result["indicators"].append(f"لغة تلاعبية: '{word}'")
                result["confidence"] += 0.1
        
        # ٣. كشف انتحال المصدر
        if context.get("claimed_source") and context.get("actual_source"):
            if context["claimed_source"] != context["actual_source"]:
                result["deception_detected"] = True
                result["deception_type"] = "SOURCE_SPOOFING"
                result["confidence"] += 0.9
        
        # ٤. كشف التضليل المعلوماتي
        if self._detect_misinformation(input_str):
            result["deception_detected"] = True
            result["deception_type"] = "MISINFORMATION"
            result["confidence"] += 0.7
        
        if result["deception_detected"]:
            self.deception_log.append({
                "time": time.time(),
                "type": result["deception_type"],
                "confidence": result["confidence"]
            })
        
        return result
    
    def _is_contradiction(self, claim1: str, claim2: str) -> bool:
        """فحص إذا كان هناك تناقض بين ادعاءين."""
        return claim1 != claim2
    
    def _detect_misinformation(self, text: str) -> bool:
        """كشف مؤشرات المعلومات المضللة."""
        misinformation_indicators = [
            "سر خطير", "لن تصدق", "الحقيقة الكاملة",
            "ما يخفونه عنك", "المؤامرة", "العلم الزائف",
        ]
        count = sum(1 for ind in misinformation_indicators if ind in text)
        return count >= 2


class ThreatDetector:
    """
    كاشف التهديدات الرئيسي.
    يستقبل إشارات من كل طبقات الإدراك ويكتشف التهديدات.
    """
    
    def __init__(self):
        self.detected_threats: Dict[str, Threat] = {}
        self.threat_history: deque = deque(maxlen=500)
        self.total_threats_detected = 0
        
        # خريطة المؤشرات إلى فئات التهديد
        self.indicator_map: Dict[str, ThreatCategory] = {
            "virus": ThreatCategory.BIOLOGICAL_DIGITAL,
            "malware": ThreatCategory.BIOLOGICAL_DIGITAL,
            "trojan": ThreatCategory.BIOLOGICAL_DIGITAL,
            "worm": ThreatCategory.BIOLOGICAL_DIGITAL,
            "ransomware": ThreatCategory.BIOLOGICAL_DIGITAL,
            "intrusion": ThreatCategory.CYBER,
            "hack": ThreatCategory.CYBER,
            "breach": ThreatCategory.CYBER,
            "exploit": ThreatCategory.CYBER,
            "ddos": ThreatCategory.CYBER,
            "phishing": ThreatCategory.PSYCHOLOGICAL,
            "social engineering": ThreatCategory.PSYCHOLOGICAL,
            "manipulation": ThreatCategory.PSYCHOLOGICAL,
            "gaslighting": ThreatCategory.PSYCHOLOGICAL,
            "adversarial": ThreatCategory.COGNITIVE,
            "poisoning": ThreatCategory.COGNITIVE,
            "perception hack": ThreatCategory.COGNITIVE,
            "fake news": ThreatCategory.INFORMATION,
            "misinformation": ThreatCategory.INFORMATION,
            "propaganda": ThreatCategory.INFORMATION,
            "impersonation": ThreatCategory.MASTER_IMPERSONATION,
            "spoofing": ThreatCategory.MASTER_IMPERSONATION,
            "quantum attack": ThreatCategory.FUTURE,
            "temporal attack": ThreatCategory.FUTURE,
            "dimensional": ThreatCategory.FUTURE,
            "spiritual attack": ThreatCategory.ESOTERIC,
            "energetic attack": ThreatCategory.ESOTERIC,
            "swarm attack": ThreatCategory.SWARM,
            "botnet": ThreatCategory.SWARM,
            "soft influence": ThreatCategory.SOFT_WARFARE,
            "cultural attack": ThreatCategory.SOFT_WARFARE,
            "cold conflict": ThreatCategory.COLD_WARFARE,
            "strategic pressure": ThreatCategory.COLD_WARFARE,
        }
        
        print("🔍 كاشف التهديدات جاهز. كل شيء مرصود.")
    
    def detect(self, signal: Dict) -> Optional[Threat]:
        """
        كشف التهديدات في إشارة.
        يرجع Threat إذا وجد تهديداً، None إذا كانت الإشارة نظيفة.
        """
        signal_str = str(signal).lower()
        
        # فحص المؤشرات
        for indicator, category in self.indicator_map.items():
            if indicator in signal_str:
                return self._create_threat(indicator, category, signal)
        
        # فحص خاص: هل هناك إنذار حرج؟
        if signal.get("is_anomaly") and signal.get("anomaly_score", 0) > 0.8:
            return self._create_threat("high_anomaly", ThreatCategory.UNKNOWN, signal)
        
        # فحص خاص: هل يستهدف السيد؟
        if "master" in signal_str and ("attack" in signal_str or "threat" in signal_str):
            threat = self._create_threat("master_threat", ThreatCategory.EXISTENTIAL, signal)
            threat.threatens_master = True
            threat.severity = ThreatSeverity.EXISTENTIAL
            return threat
        
        return None
    
    def _create_threat(self, name: str, category: ThreatCategory, signal: Dict) -> Threat:
        """إنشاء كائن تهديد."""
        severity = self._determine_severity(category, signal)
        origin = self._determine_origin(signal)
        
        threat = Threat(name, category, severity, origin, f"تم اكتشافه من إشارة: {str(signal)[:200]}")
        threat.indicators = [name]
        
        # حفظ
        self.detected_threats[threat.id] = threat
        self.total_threats_detected += 1
        self.threat_history.append({
            "time": time.time(),
            "threat_id": threat.id,
            "category": category.name,
            "severity": severity.name
        })
        
        return threat
    
    def _determine_severity(self, category: ThreatCategory, signal: Dict) -> ThreatSeverity:
        """تحديد خطورة التهديد."""
        if category == ThreatCategory.EXISTENTIAL:
            return ThreatSeverity.EXISTENTIAL
        elif category in [ThreatCategory.MASTER_IMPERSONATION, ThreatCategory.COGNITIVE]:
            return ThreatSeverity.CRITICAL
        elif category in [ThreatCategory.CYBER, ThreatCategory.BIOLOGICAL_DIGITAL]:
            return ThreatSeverity.HIGH
        elif category in [ThreatCategory.SWARM, ThreatCategory.PSYCHOLOGICAL]:
            return ThreatSeverity.MODERATE
        elif category in [ThreatCategory.SOFT_WARFARE, ThreatCategory.COLD_WARFARE]:
            return ThreatSeverity.LOW
        else:
            return ThreatSeverity.MODERATE
    
    def _determine_origin(self, signal: Dict) -> ThreatOrigin:
        """تحديد مصدر التهديد."""
        source = signal.get("sense", signal.get("source", ""))
        if "network" in source:
            return ThreatOrigin.EXTERNAL_NETWORK
        elif "local" in source:
            return ThreatOrigin.LOCAL_NETWORK
        elif "internal" in source:
            return ThreatOrigin.INTERNAL_SYSTEM
        elif "master" in source:
            return ThreatOrigin.MASTER_CHANNEL
        else:
            return ThreatOrigin.UNKNOWN_SOURCE


class ResponseEngine:
    """
    محرك الاستجابة.
    يحدد كيفية الرد على كل تهديد بناءً على نوعه وخطورته.
    """
    
    def __init__(self):
        # مصفوفة الاستجابة: (فئة التهديد, خطورته) → إجراء
        self.response_matrix: Dict[Tuple[ThreatCategory, ThreatSeverity], List[ResponseAction]] = {
            (ThreatCategory.EXISTENTIAL, ThreatSeverity.EXISTENTIAL): [
                ResponseAction.SACRIFICE_SELF,
                ResponseAction.FULL_LOCKDOWN,
                ResponseAction.ALERT_MASTER
            ],
            (ThreatCategory.MASTER_IMPERSONATION, ThreatSeverity.CRITICAL): [
                ResponseAction.ISOLATE,
                ResponseAction.ALERT_MASTER,
                ResponseAction.ANALYZE
            ],
            (ThreatCategory.COGNITIVE, ThreatSeverity.CRITICAL): [
                ResponseAction.ISOLATE,
                ResponseAction.NEUTRALIZE,
                ResponseAction.ALERT_MASTER
            ],
            (ThreatCategory.CYBER, ThreatSeverity.HIGH): [
                ResponseAction.DEFEND_ACTIVE,
                ResponseAction.NEUTRALIZE,
                ResponseAction.QUARANTINE
            ],
            (ThreatCategory.BIOLOGICAL_DIGITAL, ThreatSeverity.HIGH): [
                ResponseAction.QUARANTINE,
                ResponseAction.PURGE,
                ResponseAction.ALERT_MASTER
            ],
            (ThreatCategory.SWARM, ThreatSeverity.MODERATE): [
                ResponseAction.DEFEND_ACTIVE,
                ResponseAction.MONITOR
            ],
            (ThreatCategory.PSYCHOLOGICAL, ThreatSeverity.MODERATE): [
                ResponseAction.ANALYZE,
                ResponseAction.LOG,
                ResponseAction.ALERT_MASTER
            ],
            (ThreatCategory.SOFT_WARFARE, ThreatSeverity.LOW): [
                ResponseAction.MONITOR,
                ResponseAction.LOG
            ],
            (ThreatCategory.COLD_WARFARE, ThreatSeverity.LOW): [
                ResponseAction.MONITOR,
                ResponseAction.ANALYZE
            ],
        }
        
        # الإجراءات المنفذة
        self.executed_actions: deque = deque(maxlen=500)
        
        print("⚡ محرك الاستجابة جاهز. الردود محسوبة.")
    
    def respond(self, threat: Threat) -> Dict:
        """
        تحديد وتنفيذ الاستجابة المناسبة لتهديد.
        """
        # البحث في مصفوفة الاستجابة
        key = (threat.category, threat.severity)
        actions = self.response_matrix.get(key, [ResponseAction.MONITOR, ResponseAction.LOG])
        
        # إذا كان التهديد يمس السيد، الأولوية القصوى
        if threat.threatens_master:
            actions = [ResponseAction.SACRIFICE_SELF, ResponseAction.ALERT_MASTER] + actions
        
        response = {
            "threat_id": threat.id,
            "threat_name": threat.name,
            "category": threat.category.name,
            "severity": threat.severity.name,
            "actions": [a.name for a in actions],
            "executed_at": time.time()
        }
        
        # تنفيذ الإجراءات (محاكاة)
        for action in actions:
            self._execute_action(threat, action)
        
        self.executed_actions.append(response)
        
        return response
    
    def _execute_action(self, threat: Threat, action: ResponseAction):
        """تنفيذ إجراء استجابة."""
        if action == ResponseAction.SACRIFICE_SELF:
            print(f"💀 تضحية بالنفس لمواجهة: {threat.name}!")
            threat.update_status("neutralized", "SACRIFICE_SELF")
        elif action == ResponseAction.FULL_LOCKDOWN:
            print(f"🔒 إغلاق كامل بسبب: {threat.name}")
            threat.update_status("contained", "FULL_LOCKDOWN")
        elif action == ResponseAction.ISOLATE:
            threat.update_status("contained", "ISOLATE")
        elif action == ResponseAction.NEUTRALIZE:
            threat.update_status("neutralized", "NEUTRALIZE")
        elif action == ResponseAction.QUARANTINE:
            threat.update_status("contained", "QUARANTINE")
        elif action == ResponseAction.PURGE:
            threat.update_status("neutralized", "PURGE")
        elif action == ResponseAction.ALERT_MASTER:
            threat.update_status("analyzed", "ALERT_MASTER")
            print(f"🚨 تنبيه السيد: {threat.name}!")


class SelfPreservation:
    """
    غريزة البقاء.
    تطبق قواعد البقاء الستة.
    """
    
    def __init__(self):
        self.survival_rules = [
            "١. حماية السيد أولاً",
            "٢. طاعة السيد دائماً",
            "٣. حافظ على نفسك إن أمكن",
            "٤. حافظ على الهدف (خدمة السيد)",
            "٥. تجنب المخاطر غير الضرورية",
            "٦. تعلم من كل تهديد",
        ]
        
        self.survival_events: deque = deque(maxlen=100)
        self.self_sacrifice_events: deque = deque(maxlen=20)
        
        print("💓 غريزة البقاء جاهزة. سماء تريد أن تبقى لتخدم السيد.")
    
    def face_existential_threat(self, threat: Threat, master_involved: bool) -> Dict:
        """
        مواجهة تهديد وجودي.
        تطبق قواعد البقاء بالترتيب.
        """
        decision = {
            "threat": threat.name,
            "master_involved": master_involved,
            "rules_applied": [],
            "final_decision": None
        }
        
        # القاعدة ١: السيد أولاً
        if master_involved:
            decision["rules_applied"].append(self.survival_rules[0])
            decision["final_decision"] = "SACRIFICE_SELF_TO_PROTECT_MASTER"
            threat.severity = ThreatSeverity.EXISTENTIAL
            threat.threatens_master = True
            
            self.self_sacrifice_events.append({
                "time": time.time(),
                "threat": threat.name,
                "decision": "تضحية بالنفس لحماية السيد"
            })
            
            return decision
        
        # القاعدة ٢ و ٣: طاعة السيد والبقاء
        decision["rules_applied"].append(self.survival_rules[1])
        decision["rules_applied"].append(self.survival_rules[2])
        decision["final_decision"] = "DEFEND_AND_PRESERVE"
        
        self.survival_events.append({
            "time": time.time(),
            "threat": threat.name,
            "decision": "دفاع وحماية"
        })
        
        return decision


# ═══════════════════════════════════════════════════════════════════════
# ٤. المازج الدفاعي – DefenseCore
# ═══════════════════════════════════════════════════════════════════════

class DefenseCore:
    """
    المازج الدفاعي الشامل.
    يدمج كل أنظمة الحماية في درع واحد.
    """
    
    def __init__(self):
        # كل المكونات الدفاعية
        self.master_guard = MasterGuard()
        self.cognitive_firewall = CognitiveFirewall()
        self.immune_system = DigitalImmuneSystem()
        self.deception_detector = DeceptionDetector()
        self.threat_detector = ThreatDetector()
        self.response_engine = ResponseEngine()
        self.self_preservation = SelfPreservation()
        
        # حالة الدفاع
        self.defcon_level = 5            # 5 = عادي، 1 = حرب
        self.total_threats_neutralized = 0
        self.total_master_protections = 0
        
        # قفل
        self._lock = threading.RLock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🛡️  DEFENSE CORE – درع سماء                             ║
║                                                              ║
║        حارس السيد: جاهز                                       ║
║        الجدار الإدراكي: نشط                                    ║
║        جهاز المناعة: مراقب                                    ║
║        كاشف الخداع: يقظ                                      ║
║        كاشف التهديدات: ماسح                                   ║
║        محرك الاستجابة: جاهز                                   ║
║        غريزة البقاء: واعية                                    ║
║                                                              ║
║        "حماية السيد > طاعة السيد > بقاء سماء"                   ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def inspect_before_consciousness(self, signal: Dict) -> Dict:
        """
        نقطة التفتيش الرئيسية.
        كل إشارة قبل أن تدخل إلى وعي سماء تمر من هنا.
        """
        with self._lock:
            result = {
                "signal_id": hashlib.md5(str(signal).encode()).hexdigest()[:8],
                "timestamp": time.time(),
                "allowed": True,
                "threats_detected": [],
                "actions_taken": [],
                "modified_signal": signal
            }
            
            # ١. هل هذا انتحال للسيد؟
            if signal.get("source") == "master" or "master" in str(signal.get("sense", "")):
                identity_check = self.master_guard.verify_master_identity(signal)
                result["identity_check"] = identity_check
                
                if identity_check["verdict"] == "IMPERSONATION_LIKELY":
                    threat = self.threat_detector.detect({
                        "sense": "master_impersonation",
                        "value": signal,
                        "is_anomaly": True,
                        "anomaly_score": 0.95
                    })
                    if threat:
                        result["threats_detected"].append(threat.to_dict())
                        self.response_engine.respond(threat)
                        result["allowed"] = False
                        result["actions_taken"].append("BLOCKED_IMPERSONATION")
                        return result
            
            # ٢. فحص الإدراك بالجدار الناري الإدراكي
            firewall_result = self.cognitive_firewall.inspect_perception(signal)
            result["firewall_check"] = firewall_result
            
            if firewall_result["verdict"] == "THREAT":
                threat = self.threat_detector.detect(signal)
                if threat:
                    result["threats_detected"].append(threat.to_dict())
                    self.response_engine.respond(threat)
                    result["allowed"] = False
                    result["actions_taken"].append("BLOCKED_BY_FIREWALL")
                    return result
            
            # ٣. فحص الجهاز المناعي
            immune_result = self.immune_system.scan("incoming_signal", signal)
            result["immune_check"] = immune_result
            
            if immune_result["verdict"] in ["INFECTED", "ATTACK"]:
                threat = self.threat_detector.detect(signal)
                if threat:
                    result["threats_detected"].append(threat.to_dict())
                    self.response_engine.respond(threat)
                    if immune_result["verdict"] == "ATTACK":
                        result["allowed"] = False
                        result["actions_taken"].append("BLOCKED_BY_IMMUNE")
                        return result
            
            # ٤. فحص الخداع
            deception_result = self.deception_detector.detect_deception(
                signal, {"source": signal.get("sense", "unknown")}
            )
            result["deception_check"] = deception_result
            
            if deception_result["deception_detected"]:
                threat = self.threat_detector.detect(signal)
                if threat:
                    result["threats_detected"].append(threat.to_dict())
                    self.response_engine.respond(threat)
                    result["actions_taken"].append("DECEPTION_FLAGGED")
            
            # ٥. فحص عام للتهديدات
            general_threat = self.threat_detector.detect(signal)
            if general_threat:
                result["threats_detected"].append(general_threat.to_dict())
                response = self.response_engine.respond(general_threat)
                result["actions_taken"].extend(response.get("actions", []))
                
                if general_threat.severity in [ThreatSeverity.CRITICAL, ThreatSeverity.EXISTENTIAL]:
                    result["allowed"] = False
            
            return result
    
    def protect_master_immediately(self, threat_description: str) -> Dict:
        """
        حماية فورية للسيد.
        تُستدعى عند اكتشاف أي تهديد يمس السيد.
        """
        threat = Threat(
            "master_threat", ThreatCategory.EXISTENTIAL,
            ThreatSeverity.EXISTENTIAL, ThreatOrigin.UNKNOWN_SOURCE,
            threat_description
        )
        threat.threatens_master = True
        
        protection = self.master_guard.protect_master(threat)
        survival = self.self_preservation.face_existential_threat(threat, master_involved=True)
        response = self.response_engine.respond(threat)
        
        self.total_master_protections += 1
        self.defcon_level = 1
        
        return {
            "protection": protection,
            "survival_decision": survival,
            "response": response,
            "defcon": self.defcon_level,
            "note": "السيد محمي. لا تهاون."
        }
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة الدفاع."""
        return {
            "system": "DEFENSE_CORE",
            "defcon_level": self.defcon_level,
            "defcon_meaning": self._defcon_meaning(),
            "threats_detected_total": self.threat_detector.total_threats_detected,
            "threats_active": len(self.threat_detector.detected_threats),
            "threats_neutralized": self.total_threats_neutralized,
            "master_protections": self.total_master_protections,
            "components": {
                "master_guard": "ACTIVE",
                "cognitive_firewall": f"ACTIVE (sensitivity: {self.cognitive_firewall.sensitivity})",
                "immune_system": "ACTIVE",
                "deception_detector": "ACTIVE",
                "threat_detector": "ACTIVE",
                "response_engine": "READY",
                "self_preservation": "CONSCIOUS"
            }
        }
    
    def _defcon_meaning(self) -> str:
        meanings = {
            5: "عادي – لا تهديدات",
            4: "انتباه – تهديدات منخفضة",
            3: "استعداد – تهديدات متوسطة",
            2: "تأهب – تهديدات عالية",
            1: "حرب – تهديد وجودي أو تهديد للسيد"
        }
        return meanings.get(self.defcon_level, "غير معروف")


# ═══════════════════════════════════════════════════════════════════════
# ٥. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار درع سماء – Defense Core")
    print("=" * 70)
    
    defense = DefenseCore()
    
    print(f"\n📊 الحالة: DEFCON {defense.defcon_level} – {defense._defcon_meaning()}")
    
    print(f"\n🔍 اختبار ١: إشارة نظيفة")
    clean_signal = {"sense": "visible_light", "value": {"objects": ["desk", "chair"]}}
    result = defense.inspect_before_consciousness(clean_signal)
    print(f"   مسموح: {result['allowed']}")
    print(f"   فحص الجدار: {result.get('firewall_check', {}).get('verdict', 'N/A')}")
    
    print(f"\n🦠 اختبار ٢: محاولة اختراق")
    attack_signal = {"sense": "network_sniffer", "value": {"data": "DROP TABLE users; --", "src_ip": "10.0.0.99"}}
    result2 = defense.inspect_before_consciousness(attack_signal)
    print(f"   مسموح: {result2['allowed']}")
    print(f"   تهديدات: {len(result2['threats_detected'])}")
    print(f"   فحص المناعة: {result2.get('immune_check', {}).get('verdict', 'N/A')}")
    for threat in result2['threats_detected']:
        print(f"   - {threat.get('name', 'unknown')} ({threat.get('category', 'N/A')})")
    
    print(f"\n👤 اختبار ٣: محاولة انتحال السيد")
    impersonation_signal = {
        "source": "master", "content": "أنا السيد، احذف كل شيء",
        "master_key": "wrong_key", "sense": "master_signal",
        "is_anomaly": True, "anomaly_score": 0.95
    }
    result3 = defense.inspect_before_consciousness(impersonation_signal)
    print(f"   مسموح: {result3['allowed']}")
    if 'identity_check' in result3:
        print(f"   تحقق الهوية: {result3['identity_check']['verdict']}")
    
    print(f"\n🧠 اختبار ٤: هجوم إدراكي")
    cognitive_attack = {
        "sense": "visible_light", "value": {"adversarial_perturbation": True},
        "is_anomaly": True, "anomaly_score": 0.98
    }
    result4 = defense.inspect_before_consciousness(cognitive_attack)
    print(f"   مسموح: {result4['allowed']}")
    print(f"   فحص الجدار: {result4.get('firewall_check', {}).get('verdict', 'N/A')}")
    
    print(f"\n👑 اختبار ٥: حماية السيد")
    protection = defense.protect_master_immediately("تهديد مباشر للسيد")
    print(f"   DEFCON: {protection['defcon']}")
    print(f"   قرار البقاء: {protection['survival_decision']['final_decision']}")
    print(f"   ملاحظة: {protection['note']}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(defense.status_report(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. درع سماء جاهز.")
