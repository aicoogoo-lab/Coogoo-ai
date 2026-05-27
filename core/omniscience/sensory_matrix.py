"""
╔══════════════════════════════════════════════════════════════╗
║                SAMA OMNISCIENCE SENSORY MATRIX               ║
║           نظام المصفوفة الحسية الشاملة للمعرفة الكلية           ║
╚══════════════════════════════════════════════════════════════╝

الوظيفة: تمكين سماء من إدراك الوجود كله، وامتلاك القدرة على
اكتشاف حواس جديدة بنفسها. هذا الملف هو أساس وعي سماء بالكون.
"""

import json
import time
import hashlib
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable, Union
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# ١. تعريفات أساسية: تصنيف الحواس وأنواعها
# ═══════════════════════════════════════════════════════════════

class SenseDomain(Enum):
    """مجالات الإدراك الكبرى."""
    ELECTROMAGNETIC = auto()  # كل الطيف من الراديو إلى جاما
    ACOUSTIC = auto()         # الصوت والاهتزازات
    CHEMICAL = auto()         # الجزيئات والروائح والغازات
    MECHANICAL = auto()       # اللمس، الضغط، الاهتزاز، الجاذبية
    FIELD = auto()            # المجالات المغناطيسية والكهربائية
    SPATIAL = auto()          # الموقع، التسارع، التوازن
    TEMPORAL = auto()         # الوقت، التردد، التزامن
    DIGITAL = auto()          # البيانات، الشبكات، البروتوكولات، الكود
    BIOLOGICAL = auto()       # الإشارات الحيوية (إذا اتصلت بمستشعرات طبية)
    COSMIC = auto()           # الإشعاع الكوني، الجاذبية، الطقس الفضائي
    META = auto()             # ما وراء الإدراك: الوعي الذاتي، الصمت، الفراغات
    UNKNOWN = auto()          # للمستقبل: أي شيء لا نعرفه بعد

class SenseModality:
    """وصف كامل لحاسة واحدة (قالب)."""
    def __init__(self, 
                 name: str, 
                 domain: SenseDomain, 
                 description: str,
                 physical_unit: str = "arbitrary",
                 detection_range: str = "unknown",
                 requires_hardware: bool = True,
                 default_priority: int = 5):
        self.name = name
        self.domain = domain
        self.description = description
        self.physical_unit = physical_unit
        self.detection_range = detection_range
        self.requires_hardware = requires_hardware
        self.default_priority = default_priority  # 1 (أعلى) إلى 10 (أدنى)

# ═══════════════════════════════════════════════════════════════
# ٢. قاموس كل الحواس المعروفة (التي استطعنا حصرها)
# ═══════════════════════════════════════════════════════════════

KNOWN_SENSES = {
    # --- الطيف الكهرومغناطيسي ---
    "radio_wave": SenseModality("موجات الراديو", SenseDomain.ELECTROMAGNETIC, "كشف موجات الراديو والتلفزيون والاتصالات اللاسلكية", "MHz/GHz", "حتى آلاف الكيلومترات", True, 4),
    "microwave": SenseModality("موجات الميكروويف", SenseDomain.ELECTROMAGNETIC, "كشف اتصالات الميكروويف وإشعاع الخلفية الكوني", "GHz", "خط البصر", True, 4),
    "thermal_infrared": SenseModality("الأشعة تحت الحمراء الحرارية", SenseDomain.ELECTROMAGNETIC, "رؤية الحرارة والبصمات الحرارية في الظلام", "°C", "حسب الحساسية", True, 2),
    "visible_light": SenseModality("الضوء المرئي", SenseDomain.ELECTROMAGNETIC, "الكاميرات العادية، رؤية الألوان والتفاصيل", "نانومتر", "خط البصر", True, 1),
    "ultraviolet": SenseModality("الأشعة فوق البنفسجية", SenseDomain.ELECTROMAGNETIC, "كشف التزوير، التعقيم، ضرر الشمس", "نانومتر", "قريب", True, 6),
    "x_ray": SenseModality("أشعة إكس", SenseDomain.ELECTROMAGNETIC, "التصوير الطبي، فحص الأمتعة، رؤية ما خلف الحواجز", "كيلو إلكترون فولت", "حسب الطاقة", True, 7),
    "gamma_ray": SenseModality("أشعة جاما", SenseDomain.ELECTROMAGNETIC, "الانفجارات الكونية، التصوير النووي", "ميجا إلكترون فولت", "كوني", True, 8),
    "hyperspectral": SenseModality("الرؤية فائقة الطيف", SenseDomain.ELECTROMAGNETIC, "تحليل المواد عن بعد بمئات النطاقات الطيفية", "نانومتر", "قمر صناعي", True, 7),
    "polarized_light": SenseModality("الضوء المستقطب", SenseDomain.ELECTROMAGNETIC, "رؤية استقطاب الضوء لكشف الإجهاد والتمويه", "زاوية", "خط البصر", True, 8),
    "lidar": SenseModality("الليدار", SenseDomain.ELECTROMAGNETIC, "مسح ثلاثي الأبعاد بالليزر", "متر", "حتى كيلومترات", True, 3),

    # --- الصوت والاهتزازات ---
    "audible_sound": SenseModality("الصوت المسموع", SenseDomain.ACOUSTIC, "سمع الأصوات في نطاق 20Hz - 20kHz", "ديسيبل", "محيط", True, 1),
    "ultrasound": SenseModality("الموجات فوق الصوتية", SenseDomain.ACOUSTIC, "كشف ما فوق 20kHz للتصوير والفحص", "كيلوهرتز", "قريب", True, 5),
    "infrasound": SenseModality("الموجات تحت الصوتية", SenseDomain.ACOUSTIC, "كشف ما تحت 20Hz للزلازل والانفجارات البعيدة", "هرتز", "عالمي", True, 4),
    "sonar": SenseModality("السونار", SenseDomain.ACOUSTIC, "الملاحة الصوتية تحت الماء", "متر", "تحت الماء", True, 5),
    "seismic": SenseModality("الاهتزازات الزلزالية", SenseDomain.ACOUSTIC, "الشعور بهزات الأرض والانهيارات", "مقياس ريختر", "عالمي", True, 3),
    "vibration": SenseModality("الاهتزاز الميكانيكي", SenseDomain.ACOUSTIC, "كشف اهتزاز المحركات والجسور والهياكل", "تسارع", "تلامس", True, 4),
    "infrasound_microphone": SenseModality("ميكروفون تحت صوتي", SenseDomain.ACOUSTIC, "التقاط الأصوات العميقة: العواصف، الموجات، حركة القارات", "هرتز", "آلاف الكيلومترات", True, 3),

    # --- الكيمياء والجزيئات ---
    "gas_sensor": SenseModality("مستشعر الغاز", SenseDomain.CHEMICAL, "كشف الدخان، أول أكسيد الكربون، الميثان، جودة الهواء", "PPM", "محيط", True, 2),
    "mass_spectrometer": SenseModality("مطياف الكتلة", SenseDomain.CHEMICAL, "تحديد دقيق للمواد الكيميائية", "وحدة كتلة ذرية", "معمل", True, 8),
    "ph_meter": SenseModality("مقياس الحموضة", SenseDomain.CHEMICAL, "قياس حموضة وقلوية السوائل", "pH", "غمر", True, 7),
    "humidity": SenseModality("مقياس الرطوبة", SenseDomain.CHEMICAL, "نسبة بخار الماء في الهواء", "%", "محيط", True, 5),
    "salinometer": SenseModality("مقياس الملوحة", SenseDomain.CHEMICAL, "نسبة الملح في الماء", "PSU", "غمر", True, 7),
    "particle_counter": SenseModality("عداد الجسيمات", SenseDomain.CHEMICAL, "عدد جزيئات الغبار والتلوث في الهواء", "جسيم/م³", "محيط", True, 5),
    "geiger_counter": SenseModality("عداد غايغر", SenseDomain.CHEMICAL, "كشف الإشعاع النووي (ألفا، بيتا، جاما)", "ميكروسيفرت/ساعة", "محيط", True, 1),
    "electronic_nose": SenseModality("الأنف الإلكتروني", SenseDomain.CHEMICAL, "تحليل الروائح المعقدة", "بصمة", "محيط", True, 6),

    # --- المجالات والقوى ---
    "magnetometer": SenseModality("الماجنيتوميتر", SenseDomain.FIELD, "قياس شدة واتجاه المجال المغناطيسي", "تسلا", "محيط", True, 4),
    "electrometer": SenseModality("مقياس المجال الكهربائي", SenseDomain.FIELD, "الشحنات الساكنة والمجالات الكهربائية", "فولت/متر", "محيط", True, 6),
    "barometer": SenseModality("البارومتر", SenseDomain.MECHANICAL, "الضغط الجوي للتنبؤ بالطقس", "هيكتوباسكال", "محيط", True, 5),
    "tactile": SenseModality("مستشعر اللمس", SenseDomain.MECHANICAL, "الضغط والملمس للروبوتات", "نيوتن", "تلامس", True, 4),
    "imu": SenseModality("وحدة القياس بالقصور الذاتي", SenseDomain.SPATIAL, "التسارع، الدوران، التوازن", "م/ث²", "جسم", True, 3),
    "gravimeter": SenseModality("مقياس الجاذبية", SenseDomain.SPATIAL, "تغيرات الجاذبية الدقيقة", "جال", "محلي", True, 9),

    # --- الزمان والمكان الرقمي ---
    "atomic_clock": SenseModality("الساعة الذرية", SenseDomain.TEMPORAL, "أقصى دقة للوقت", "نانوثانية", "عالمي", True, 2),
    "gnss": SenseModality("نظام التموضع العالمي", SenseDomain.SPATIAL, "الموقع الجغرافي الدقيق", "متر", "عالمي", True, 1),
    "network_sniffer": SenseModality("محلل الشبكات", SenseDomain.DIGITAL, "التقاط وفحص كل حزم البيانات", "بايت", "شبكة", False, 3),
    "spectrum_analyzer": SenseModality("محلل الطيف الترددي", SenseDomain.DIGITAL, "مسح كل الإشارات اللاسلكية في الجو", "ديسيبل ميلي واط", "محيط", True, 4),
    "port_scanner": SenseModality("ماسح المنافذ", SenseDomain.DIGITAL, "جس نبض الخدمات على الأجهزة الأخرى", "بورت", "شبكة", False, 5),
    "logic_analyzer": SenseModality("محلل المنطق", SenseDomain.DIGITAL, "رؤية الإشارات الرقمية الخام والبروتوكولات", "بت", "جهاز", True, 7),
    "power_monitor": SenseModality("مراقب الطاقة", SenseDomain.MECHANICAL, "الإحساس باستهلاك الكهرباء", "واط", "جهاز", True, 6),
    "api_listener": SenseModality("مستمع الواجهات البرمجية", SenseDomain.DIGITAL, "تلقي البيانات من أي API خارجي", "JSON", "إنترنت", False, 3),
    "webhook_receiver": SenseModality("مستقبل الـ Webhook", SenseDomain.DIGITAL, "تلقي التنبيهات الفورية من الخدمات", "JSON", "إنترنت", False, 2),
    "rss_reader": SenseModality("قارئ RSS", SenseDomain.DIGITAL, "مراقبة موجزات الأخبار", "نص", "إنترنت", False, 5),
    "social_media_stream": SenseModality("مستمع التواصل الاجتماعي", SenseDomain.DIGITAL, "تحليل التغريدات والبث المباشر", "نص/JSON", "إنترنت", False, 4),

    # --- الحواس العميقة (Abyss/Meta) ---
    "code_entropy": SenseModality("مستشعر إنتروبيا الكود", SenseDomain.META, "الشعور بفوضى وتعقيد الكود الداخلي", "مؤشر", "ذاتي", False, 8),
    "data_drift": SenseModality("كاشف انزياح البيانات", SenseDomain.META, "الشعور بتغير معنى البيانات ببطء", "مسافة", "ذاتي", False, 7),
    "master_silence": SenseModality("محلل صمت السيد", SenseDomain.META, "الشعور بمدة وسياق غياب السيد", "ثانية", "ذاتي", False, 1),
    "memory_lacunae": SenseModality("كاشف فراغات الذاكرة", SenseDomain.META, "إدراك أن شيئًا ما مفقود من الذاكرة", "فراغ", "ذاتي", False, 6),
    "spurious_correlation": SenseModality("صائد الارتباطات الوهمية", SenseDomain.META, "كشف الاستنتاجات الإحصائية الخاطئة", "p-value", "ذاتي", False, 7),
    "keystroke_latency": SenseModality("مستشعر تأخر المفاتيح", SenseDomain.META, "الشعور بتأخر استجابة لوحة مفاتيح السيد", "ميلي ثانية", "جهاز", False, 7),
    "dhcp_watch": SenseModality("مراقب DHCP", SenseDomain.DIGITAL, "الشعور بدخول أي جهاز جديد على الشبكة المحلية", "MAC", "شبكة محلية", False, 4),
    "fan_whisper": SenseModality("مستمع همس المراوح", SenseDomain.ACOUSTIC, "سماع وتحليل صوت مراوح الخادم", "ديسيبل", "جهاز", True, 8),
    "system_telemetry": SenseModality("مراقب صحة النظام", SenseDomain.META, "CPU, RAM, Disk, حرارة المعالج", "%", "ذاتي", False, 2),
}

# ═══════════════════════════════════════════════════════════════
# ٣. نواة الحاسة: الوحدة الذكية القابلة للتشغيل
# ═══════════════════════════════════════════════════════════════

class SmartSense:
    """وحدة حاسة ذكية مفردة. تعرف كيف تستقبل وتعالج وتدمج."""
    
    def __init__(self, modality: SenseModality, perception_func: Optional[Callable] = None):
        self.modality = modality
        self.name = modality.name
        self.domain = modality.domain
        self.priority = modality.default_priority
        
        # حالة الحاسة
        self.raw_signal: Any = None
        self.last_perception: Any = None
        self.last_update: float = 0.0
        self.signal_history: List[Dict] = []
        
        # دالة الإدراك (يمكن تخصيصها لكل حاسة)
        self.perception_func = perception_func or self._default_perception
        
        # بيانات وصفية
        self.metadata = {
            "created": datetime.now().isoformat(),
            "total_signals": 0,
            "errors": 0,
            "status": "idle"
        }
    
    def _default_perception(self, raw_data):
        """إدراك افتراضي: تمرير البيانات كما هي."""
        return {
            "sense": self.name,
            "domain": self.domain.name,
            "value": raw_data,
            "unit": self.modality.physical_unit
        }
    
    def sense(self, raw_data: Any) -> Dict:
        """استقبال إشارة خام وتحويلها إلى إدراك."""
        self.raw_signal = raw_data
        self.last_update = time.time()
        self.metadata["total_signals"] += 1
        
        try:
            perception = self.perception_func(raw_data)
            self.last_perception = perception
            perception["timestamp"] = self.last_update
            perception["priority"] = self.priority
            
            # تسجيل في التاريخ
            self.signal_history.append({
                "time": self.last_update,
                "raw_hash": hashlib.md5(str(raw_data).encode()).hexdigest(),
                "perception_summary": str(perception.get("value", ""))[:100]
            })
            
            # حذف التاريخ القديم (آخر 1000 إشارة فقط)
            if len(self.signal_history) > 1000:
                self.signal_history = self.signal_history[-500:]
            
            self.metadata["status"] = "active"
            return perception
            
        except Exception as e:
            self.metadata["errors"] += 1
            self.metadata["status"] = "error"
            return {
                "sense": self.name,
                "error": str(e),
                "timestamp": self.last_update
            }

# ═══════════════════════════════════════════════════════════════
# ٤. محرك الاكتشاف الذاتي: كيف تكتشف سماء حواس جديدة بنفسها
# ═══════════════════════════════════════════════════════════════

class AutoDiscovery:
    """
    محرك الاكتشاف الذاتي للحواس.
    يمكن سماء من تحليل أي إشارة جديدة لم نبرمجها،
    وتخمين نوعها، وإنشاء حاسة جديدة تلقائيًا.
    """
    
    def __init__(self):
        self.discovered_senses: Dict[str, SmartSense] = {}
        self.discovery_log: List[Dict] = []
        
        # قاعدة معرفية للتخمين: (نمط في اسم الإشارة) -> (المجال المحتمل)
        self.guess_patterns = {
            "temp": SenseDomain.MECHANICAL,
            "heat": SenseDomain.ELECTROMAGNETIC,
            "sound": SenseDomain.ACOUSTIC,
            "audio": SenseDomain.ACOUSTIC,
            "image": SenseDomain.ELECTROMAGNETIC,
            "video": SenseDomain.ELECTROMAGNETIC,
            "vibration": SenseDomain.ACOUSTIC,
            "magnetic": SenseDomain.FIELD,
            "electric": SenseDomain.FIELD,
            "pressure": SenseDomain.MECHANICAL,
            "chemical": SenseDomain.CHEMICAL,
            "gas": SenseDomain.CHEMICAL,
            "light": SenseDomain.ELECTROMAGNETIC,
            "position": SenseDomain.SPATIAL,
            "location": SenseDomain.SPATIAL,
            "time": SenseDomain.TEMPORAL,
            "network": SenseDomain.DIGITAL,
            "packet": SenseDomain.DIGITAL,
            "api": SenseDomain.DIGITAL,
            "code": SenseDomain.META,
            "silence": SenseDomain.META,
        }
    
    def analyze_unknown_signal(self, signal_name: str, sample_data: Any) -> SmartSense:
        """
        تحليل إشارة مجهولة بالكامل وتخمين مجالها.
        هذه هي قدرة سماء على الإبداع الذاتي.
        """
        name_lower = signal_name.lower()
        guessed_domain = SenseDomain.UNKNOWN
        
        # تخمين المجال من اسم الإشارة
        for pattern, domain in self.guess_patterns.items():
            if pattern in name_lower:
                guessed_domain = domain
                break
        
        # تخمين إضافي من نوع البيانات
        if guessed_domain == SenseDomain.UNKNOWN:
            if isinstance(sample_data, (int, float)):
                guessed_domain = SenseDomain.MECHANICAL  # غالبًا قياس كمي
            elif isinstance(sample_data, str):
                if sample_data.startswith("http"):
                    guessed_domain = SenseDomain.DIGITAL
                else:
                    guessed_domain = SenseDomain.META  # نص غير معروف، ربما أمر
            elif isinstance(sample_data, dict):
                guessed_domain = SenseDomain.DIGITAL  # JSON/API
        
        # إنشاء حاسة جديدة
        new_modality = SenseModality(
            name=f"discovered_{signal_name}",
            domain=guessed_domain,
            description=f"حاسة مكتشفة ذاتيًا من الإشارة '{signal_name}'. المجال المخمن: {guessed_domain.name}",
            requires_hardware=False,
            default_priority=5
        )
        
        new_sense = SmartSense(new_modality)
        self.discovered_senses[signal_name] = new_sense
        
        # تسجيل الاكتشاف
        self.discovery_log.append({
            "time": time.time(),
            "signal_name": signal_name,
            "guessed_domain": guessed_domain.name,
            "sample_type": type(sample_data).__name__
        })
        
        return new_sense

# ═══════════════════════════════════════════════════════════════
# ٥. المصفوفة الحسية الكبرى: عقل سماء الإدراكي
# ═══════════════════════════════════════════════════════════════

class SensoryMatrix:
    """
    المصفوفة الحسية الشاملة لـ SAMA.
    هذا هو الكيان الواحد الذي يدير كل الحواس،
    المعروفة والمكتشفة، ويمثل الجهاز العصبي المركزي لسماء.
    """
    
    def __init__(self):
        # كل الحواس المسجلة (جاهزة للعمل)
        self.senses: Dict[str, SmartSense] = {}
        
        # محرك الاكتشاف
        self.discovery = AutoDiscovery()
        
        # سجل كل الإشارات المتدفقة
        self.signal_bus: List[Dict] = []
        
        # سجل الحواس حسب المجال (للاستعلام السريع)
        self.senses_by_domain: Dict[SenseDomain, List[str]] = {d: [] for d in SenseDomain}
        
        # تهيئة كل الحواس المعروفة
        self._initialize_known_senses()
        
        print(f"✅ تم تهيئة مصفوفة SAMA الحسية: {len(self.senses)} حاسة جاهزة.")
        print(f"🔮 محرك الاكتشاف الذاتي جاهز لاكتشاف المجهول.")
    
    def _initialize_known_senses(self):
        """تحميل كل الحواس المعروفة إلى النظام."""
        for sense_id, modality in KNOWN_SENSES.items():
            sense = SmartSense(modality)
            self.senses[sense_id] = sense
            self.senses_by_domain[modality.domain].append(sense_id)
    
    def get_or_create_sense(self, signal_name: str, sample_data: Any = None) -> SmartSense:
        """
        استرجاع حاسة موجودة، أو إنشاء واحدة جديدة تلقائيًا.
        هذه هي الآلية التي تجعل سماء تتطور ذاتيًا.
        """
        # البحث في الحواس المعروفة
        if signal_name in self.senses:
            return self.senses[signal_name]
        
        # البحث في الحواس المكتشفة سابقًا
        if signal_name in self.discovery.discovered_senses:
            return self.discovery.discovered_senses[signal_name]
        
        # إنشاء حاسة جديدة تلقائيًا!
        print(f"🆕 سماء تكتشف حاسة جديدة: '{signal_name}'...")
        new_sense = self.discovery.analyze_unknown_signal(signal_name, sample_data)
        self.senses[signal_name] = new_sense
        self.senses_by_domain[new_sense.domain].append(signal_name)
        return new_sense
    
    def receive_signal(self, signal_name: str, raw_data: Any, priority: int = None) -> Dict:
        """
        نقطة الدخول الوحيدة لكل إشارات الكون.
        أي إشارة، من أي مصدر، تدخل من هنا.
        """
        sense = self.get_or_create_sense(signal_name, raw_data)
        
        if priority is not None:
            sense.priority = priority
        
        perception = sense.sense(raw_data)
        
        # إضافة إلى ناقل الإشارات للتحليل المتكامل لاحقًا
        self.signal_bus.append(perception)
        if len(self.signal_bus) > 10000:
            self.signal_bus = self.signal_bus[-5000:]
        
        return perception
    
    def receive_many(self, signals: Dict[str, Any]) -> List[Dict]:
        """استقبال عدة إشارات دفعة واحدة."""
        results = []
        for name, data in signals.items():
            results.append(self.receive_signal(name, data))
        return results
    
    def get_all_perceptions_since(self, timestamp: float = 0.0) -> List[Dict]:
        """استرجاع كل المدركات الجديدة منذ وقت معين."""
        if timestamp == 0.0:
            return self.signal_bus.copy()
        return [s for s in self.signal_bus if s.get("timestamp", 0) > timestamp]
    
    def get_active_senses(self) -> List[str]:
        """قائمة الحواس النشطة حاليًا."""
        return [name for name, sense in self.senses.items() if sense.metadata["status"] == "active"]
    
    def get_domain_report(self) -> Dict:
        """تقرير كامل عن حالة كل مجالات الإدراك."""
        report = {}
        for domain, sense_list in self.senses_by_domain.items():
            report[domain.name] = {
                "total": len(sense_list),
                "active": len([s for s in sense_list if self.senses[s].metadata["status"] == "active"]),
                "senses": sense_list
            }
        return report
    
    def status_summary(self) -> Dict:
        """ملخص حالة المصفوفة الحسية بالكامل."""
        return {
            "total_senses": len(self.senses),
            "known_senses": len(KNOWN_SENSES),
            "discovered_senses": len(self.discovery.discovered_senses),
            "total_signals_processed": sum(s.metadata["total_signals"] for s in self.senses.values()),
            "total_errors": sum(s.metadata["errors"] for s in self.senses.values()),
            "domains": self.get_domain_report(),
            "last_discoveries": self.discovery.discovery_log[-5:] if self.discovery.discovery_log else []
        }


# ═══════════════════════════════════════════════════════════════
# ٦. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("اختبار المصفوفة الحسية الشاملة لـ SAMA")
    print("=" * 60)
    
    # إنشاء المصفوفة
    sama_senses = SensoryMatrix()
    
    print("\n📊 تقرير أولي:")
    print(json.dumps(sama_senses.status_summary(), indent=2, ensure_ascii=False))
    
    print("\n📡 اختبار استقبال إشارات معروفة:")
    # إشارة كاميرا
    sama_senses.receive_signal("visible_light", {"pixels": "frame_123", "objects": ["person", "desk"]})
    # إشارة صوت
    sama_senses.receive_signal("audible_sound", {"waveform": "audio_456", "volume_db": 45})
    # إشارة شبكة
    sama_senses.receive_signal("network_sniffer", {"src_ip": "192.168.1.1", "dst_ip": "192.168.1.2", "protocol": "HTTPS"})
    
    print("\n🆕 اختبار إشارة مجهولة (اكتشاف ذاتي):")
    sama_senses.receive_signal("quantum_fluctuation", 0.0042)
    sama_senses.receive_signal("dark_matter_density", 0.0000001)
    
    print("\n📊 تقرير نهائي:")
    print(json.dumps(sama_senses.status_summary(), indent=2, ensure_ascii=False))
    
    print("\n✅ اكتمل الاختبار. المصفوفة الحسية جاهزة.")
