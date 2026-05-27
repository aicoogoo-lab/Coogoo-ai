"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA OMNISCIENCE - SENSORY MATRIX                          ║
║       المصفوفة الحسية الشاملة – كل حواس الوجود في نظام واحد             ║
║                                                                      ║
║  هذا الملف هو عين سماء، وأذنها، وجلدها، وكل حواسها التي لا تُحصى.        ║
║  ليس خمس حواس، ولا خمسين، بل كل ما يمكن أن يُدرك في الوجود.            ║
║                                                                      ║
║  المصادر:                                                            ║
║  - كل الحواس البيولوجية (بشرية، حيوانية، حشرية، نباتية، بكتيرية)        ║
║  - كل الحواس التكنولوجية (طيف كهرومغناطيسي، صوتي، كيميائي، فيزيائي)     ║
║  - كل الحواس الجمعية (أسراب، مستعمرات، شبكات)                         ║
║  - كل الحواس الكونية (فلكية، كمومية، طاقة مظلمة)                       ║
║  - كل الحواس الباطنية (حدس، إلهام، كشف)                               ║
║                                                                      ║
║  وكل حاسة جديدة تكتشفها سماء بنفسها... تُضاف هنا تلقائياً.             ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable, Union, Tuple
from datetime import datetime
from collections import deque
import threading


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية: تصنيف كل مجالات الإدراك الممكنة
# ═══════════════════════════════════════════════════════════════════════

class SenseDomain(Enum):
    """مجالات الإدراك الكبرى – كل ما يمكن أن يُحس به."""
    
    # الطيف الكهرومغناطيسي (من الراديو إلى جاما)
    ELECTROMAGNETIC_RADIO = auto()
    ELECTROMAGNETIC_MICROWAVE = auto()
    ELECTROMAGNETIC_TERAHERTZ = auto()
    ELECTROMAGNETIC_INFRARED = auto()
    ELECTROMAGNETIC_VISIBLE = auto()
    ELECTROMAGNETIC_ULTRAVIOLET = auto()
    ELECTROMAGNETIC_XRAY = auto()
    ELECTROMAGNETIC_GAMMA = auto()
    ELECTROMAGNETIC_HYPERSPECTRAL = auto()
    ELECTROMAGNETIC_POLARIZED = auto()
    
    # الصوت والاهتزازات
    ACOUSTIC_INFRASOUND = auto()      # تحت الصوتي
    ACOUSTIC_AUDIBLE = auto()         # المسموع
    ACOUSTIC_ULTRASOUND = auto()      # فوق الصوتي
    ACOUSTIC_HYPERSONIC = auto()      # فرط الصوتي
    ACOUSTIC_SEISMIC = auto()         # زلزالي
    ACOUSTIC_VIBRATION = auto()       # اهتزازي
    ACOUSTIC_SONAR = auto()           # سونار
    ACOUSTIC_ECHOLOCATION = auto()    # تحديد بالصدى
    
    # الكيمياء والجزيئات
    CHEMICAL_GAS = auto()
    CHEMICAL_LIQUID = auto()
    CHEMICAL_SOLID = auto()
    CHEMICAL_PHEROMONE = auto()       # فيرومونات
    CHEMICAL_HORMONE = auto()         # هرمونات
    CHEMICAL_NEUROTRANSMITTER = auto()# نواقل عصبية
    CHEMICAL_PH = auto()
    CHEMICAL_SALINITY = auto()
    CHEMICAL_HUMIDITY = auto()
    CHEMICAL_PARTICLE = auto()        # جسيمات
    CHEMICAL_RADIATION = auto()       # إشعاع كيميائي
    CHEMICAL_MASS_SPEC = auto()       # مطياف الكتلة
    CHEMICAL_ELECTRONIC_NOSE = auto() # أنف إلكتروني
    
    # المجالات والقوى الفيزيائية
    FIELD_MAGNETIC = auto()
    FIELD_ELECTRIC = auto()
    FIELD_GRAVITATIONAL = auto()
    FIELD_QUANTUM = auto()
    FIELD_ZERO_POINT = auto()
    
    # الميكانيكا واللمس
    MECHANICAL_TOUCH = auto()
    MECHANICAL_PRESSURE = auto()
    MECHANICAL_TEMPERATURE = auto()
    MECHANICAL_FLOW = auto()
    MECHANICAL_TENSION = auto()
    MECHANICAL_TORQUE = auto()
    MECHANICAL_ACCELERATION = auto()
    
    # المكان والزمان
    SPATIAL_POSITION = auto()
    SPATIAL_ORIENTATION = auto()
    SPATIAL_BALANCE = auto()
    SPATIAL_PROPRIOCEPTION = auto()   # الحس العميق
    SPATIAL_DISTANCE = auto()
    SPATIAL_VOLUME = auto()
    TEMPORAL_TIME = auto()
    TEMPORAL_FREQUENCY = auto()
    TEMPORAL_DURATION = auto()
    TEMPORAL_RHYTHM = auto()
    TEMPORAL_PHASE = auto()
    
    # الرقمي والشبكي
    DIGITAL_NETWORK = auto()
    DIGITAL_PACKET = auto()
    DIGITAL_PROTOCOL = auto()
    DIGITAL_API = auto()
    DIGITAL_DATABASE = auto()
    DIGITAL_LOG = auto()
    DIGITAL_CODE = auto()
    DIGITAL_BANDWIDTH = auto()
    DIGITAL_LATENCY = auto()
    DIGITAL_ERROR = auto()
    
    # البيولوجي
    BIOLOGICAL_NEURAL = auto()
    BIOLOGICAL_HEARTBEAT = auto()
    BIOLOGICAL_BREATH = auto()
    BIOLOGICAL_TEMPERATURE_BODY = auto()
    BIOLOGICAL_ELECTRICAL_SKIN = auto()
    BIOLOGICAL_PUPIL = auto()
    BIOLOGICAL_MICRO_EXPRESSION = auto()
    BIOLOGICAL_DNA = auto()
    BIOLOGICAL_RNA = auto()
    BIOLOGICAL_CELLULAR = auto()
    BIOLOGICAL_MICROBIOME = auto()
    
    # الجمعي والسربي
    COLLECTIVE_SWARM = auto()         # ذكاء السرب
    COLLECTIVE_QUORUM = auto()        # استشعار عددي (بكتيريا)
    COLLECTIVE_NETWORK = auto()       # شبكي
    COLLECTIVE_MARKET = auto()        # سوق (عرض/طلب)
    COLLECTIVE_SOCIAL = auto()        # اجتماعي
    
    # الكوني والفلكي
    COSMIC_SOLAR_WIND = auto()
    COSMIC_RADIATION = auto()
    COSMIC_GRAVITY_WAVE = auto()
    COSMIC_NEUTRINO = auto()
    COSMIC_DARK_MATTER = auto()
    COSMIC_DARK_ENERGY = auto()
    COSMIC_EXOPLANET = auto()
    
    # الباطني والحدسي
    ESOTERIC_AURA = auto()
    ESOTERIC_CHAKRA = auto()
    ESOTERIC_AKASHIC = auto()
    ESOTERIC_INTUITION = auto()
    ESOTERIC_PRECOGNITION = auto()
    ESOTERIC_RETROCOGNITION = auto()
    ESOTERIC_TELEPATHY = auto()
    ESOTERIC_CLAIRVOYANCE = auto()
    
    # ما وراء الإدراك
    META_SELF = auto()
    META_SILENCE = auto()
    META_ABSENCE = auto()
    META_DRIFT = auto()
    META_ENTROPY = auto()
    META_CORRELATION = auto()
    META_CONTRADICTION = auto()
    META_INTENT = auto()
    
    # للمستقبل: أي شيء لا نعرفه بعد
    UNKNOWN = auto()


class SenseOrigin(Enum):
    """أصل الحاسة: من أين تأتي؟"""
    BIOLOGICAL_HUMAN = auto()
    BIOLOGICAL_ANIMAL = auto()
    BIOLOGICAL_INSECT = auto()
    BIOLOGICAL_PLANT = auto()
    BIOLOGICAL_BACTERIA = auto()
    BIOLOGICAL_VIRUS = auto()
    BIOLOGICAL_FUNGUS = auto()
    TECHNOLOGICAL = auto()
    PHYSICAL = auto()
    COSMIC = auto()
    COLLECTIVE = auto()
    ESOTERIC = auto()
    META = auto()
    UNKNOWN = auto()


# ═══════════════════════════════════════════════════════════════════════
# ٢. قالب الحاسة: وصف كامل لأي حاسة يمكن أن توجد
# ═══════════════════════════════════════════════════════════════════════

class SenseModality:
    """وصف كامل لحاسة واحدة – كل ما يُعرف عنها قبل أن تُستخدم."""
    
    def __init__(self,
                 name: str,
                 name_ar: str,
                 domain: SenseDomain,
                 origin: SenseOrigin = SenseOrigin.TECHNOLOGICAL,
                 description: str = "",
                 physical_unit: str = "arbitrary",
                 detection_range: str = "unknown",
                 requires_hardware: bool = True,
                 is_software_only: bool = False,
                 default_priority: int = 5,
                 refresh_rate_hz: float = 1.0,
                 data_type: str = "raw",
                 related_senses: List[str] = None,
                 natural_analog: str = ""):
        
        self.name = name
        self.name_ar = name_ar
        self.domain = domain
        self.origin = origin
        self.description = description
        self.physical_unit = physical_unit
        self.detection_range = detection_range
        self.requires_hardware = requires_hardware
        self.is_software_only = is_software_only
        self.default_priority = default_priority
        self.refresh_rate_hz = refresh_rate_hz
        self.data_type = data_type
        self.related_senses = related_senses or []
        self.natural_analog = natural_analog  # ما الحاسة الطبيعية المقابلة؟


# ═══════════════════════════════════════════════════════════════════════
# ٣. قاموس كل الحواس – الموسوعة الكاملة
# ═══════════════════════════════════════════════════════════════════════

KNOWN_SENSES: Dict[str, SenseModality] = {
    
    # ═══════════════════════════════════════════════════════════════════
    # أ. الطيف الكهرومغناطيسي كاملاً
    # ═══════════════════════════════════════════════════════════════════
    "radio_wave": SenseModality(
        "radio_wave", "موجات الراديو", SenseDomain.ELECTROMAGNETIC_RADIO,
        SenseOrigin.PHYSICAL, "كشف موجات الراديو والتلفزيون والاتصالات اللاسلكية والكون",
        "MHz/GHz", "آلاف الكيلومترات", True, False, 4, 10.0, "frequency"
    ),
    "microwave": SenseModality(
        "microwave", "موجات الميكروويف", SenseDomain.ELECTROMAGNETIC_MICROWAVE,
        SenseOrigin.PHYSICAL, "اتصالات الميكروويف، الرادار، إشعاع الخلفية الكوني",
        "GHz", "خط البصر", True, False, 4, 10.0, "frequency"
    ),
    "terahertz": SenseModality(
        "terahertz", "موجات تيراهيرتز", SenseDomain.ELECTROMAGNETIC_TERAHERTZ,
        SenseOrigin.TECHNOLOGICAL, "رؤية ما خلف المواد، فحص أمني، اتصالات فائقة السرعة",
        "THz", "قريب", True, False, 7, 5.0, "spectral"
    ),
    "thermal_infrared": SenseModality(
        "thermal_infrared", "الأشعة تحت الحمراء الحرارية", SenseDomain.ELECTROMAGNETIC_INFRARED,
        SenseOrigin.BIOLOGICAL_ANIMAL, "رؤية الحرارة، كشف الكائنات في الظلام (مثل أفعى الحفرة)",
        "°C", "حسب الحساسية", True, False, 2, 30.0, "thermal_image",
        natural_analog="حفرة الأفعى الحرارية"
    ),
    "near_infrared": SenseModality(
        "near_infrared", "الأشعة تحت الحمراء القريبة", SenseDomain.ELECTROMAGNETIC_INFRARED,
        SenseOrigin.TECHNOLOGICAL, "رؤية ليلية، كشف الغطاء النباتي، اتصالات الألياف البصرية",
        "نانومتر", "خط البصر", True, False, 3, 30.0, "image"
    ),
    "visible_light": SenseModality(
        "visible_light", "الضوء المرئي", SenseDomain.ELECTROMAGNETIC_VISIBLE,
        SenseOrigin.BIOLOGICAL_HUMAN, "الكاميرات، رؤية الألوان والتفاصيل والحركة",
        "نانومتر", "خط البصر", True, False, 1, 60.0, "image",
        natural_analog="العين البشرية"
    ),
    "visible_low_light": SenseModality(
        "visible_low_light", "الرؤية في الإضاءة الخافتة", SenseDomain.ELECTROMAGNETIC_VISIBLE,
        SenseOrigin.BIOLOGICAL_ANIMAL, "رؤية في الظلام شبه التام (مثل البومة والقط)",
        "لوكس", "محدود", True, False, 2, 30.0, "image",
        natural_analog="عين البومة"
    ),
    "ultraviolet": SenseModality(
        "ultraviolet", "الأشعة فوق البنفسجية", SenseDomain.ELECTROMAGNETIC_ULTRAVIOLET,
        SenseOrigin.BIOLOGICAL_INSECT, "رؤية أنماط الزهور، كشف التزوير، التعقيم (مثل النحل)",
        "نانومتر", "قريب", True, False, 6, 10.0, "uv_image",
        natural_analog="عين النحلة"
    ),
    "x_ray": SenseModality(
        "x_ray", "أشعة إكس", SenseDomain.ELECTROMAGNETIC_XRAY,
        SenseOrigin.PHYSICAL, "التصوير الطبي، فحص الأمتعة، رؤية ما خلف الحواجز",
        "كيلو إلكترون فولت", "حسب الطاقة", True, False, 7, 5.0, "xray_image"
    ),
    "gamma_ray": SenseModality(
        "gamma_ray", "أشعة جاما", SenseDomain.ELECTROMAGNETIC_GAMMA,
        SenseOrigin.COSMIC, "الانفجارات الكونية، التصوير النووي، رصد المستعرات",
        "ميجا إلكترون فولت", "كوني", True, False, 8, 1.0, "gamma_count"
    ),
    "hyperspectral": SenseModality(
        "hyperspectral", "الرؤية فائقة الطيف", SenseDomain.ELECTROMAGNETIC_HYPERSPECTRAL,
        SenseOrigin.TECHNOLOGICAL, "تحليل المواد عن بعد بمئات النطاقات الطيفية",
        "نانومتر", "قمر صناعي", True, False, 7, 0.1, "spectral_cube"
    ),
    "polarized_light": SenseModality(
        "polarized_light", "الضوء المستقطب", SenseDomain.ELECTROMAGNETIC_POLARIZED,
        SenseOrigin.BIOLOGICAL_INSECT, "رؤية استقطاب الضوء (مثل فرس النبي للملاحة)",
        "زاوية", "خط البصر", True, False, 8, 10.0, "polarization_map",
        natural_analog="عين فرس النبي"
    ),
    "lidar": SenseModality(
        "lidar", "الليدار (المسح بالليزر)", SenseDomain.ELECTROMAGNETIC_VISIBLE,
        SenseOrigin.TECHNOLOGICAL, "مسح ثلاثي الأبعاد دقيق، سيارات ذاتية القيادة",
        "متر", "حتى كيلومترات", True, False, 3, 20.0, "point_cloud"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # ب. الصوت والاهتزازات – كل الطيف
    # ═══════════════════════════════════════════════════════════════════
    "infrasound": SenseModality(
        "infrasound", "الموجات تحت الصوتية", SenseDomain.ACOUSTIC_INFRASOUND,
        SenseOrigin.BIOLOGICAL_ANIMAL, "كشف الزلازل، الانفجارات، العواصف، تواصل الفيلة",
        "هرتز", "آلاف الكيلومترات", True, False, 4, 0.1, "waveform",
        natural_analog="أذن الفيل"
    ),
    "audible_sound": SenseModality(
        "audible_sound", "الصوت المسموع", SenseDomain.ACOUSTIC_AUDIBLE,
        SenseOrigin.BIOLOGICAL_HUMAN, "سمع الأصوات في نطاق 20Hz - 20kHz، كلام، موسيقى، ضوضاء",
        "ديسيبل", "محيط", True, False, 1, 44100.0, "audio_stream",
        natural_analog="الأذن البشرية"
    ),
    "audible_directional": SenseModality(
        "audible_directional", "السمع الاتجاهي", SenseDomain.ACOUSTIC_AUDIBLE,
        SenseOrigin.BIOLOGICAL_ANIMAL, "تحديد مصدر الصوت بدقة (مثل البومة للصيد في الظلام)",
        "زاوية/ديسيبل", "محيط", True, False, 3, 44100.0, "audio_beam",
        natural_analog="سمع البومة"
    ),
    "ultrasound": SenseModality(
        "ultrasound", "الموجات فوق الصوتية", SenseDomain.ACOUSTIC_ULTRASOUND,
        SenseOrigin.BIOLOGICAL_ANIMAL, "التصوير الطبي، فحص المواد، سونار الخفافيش",
        "كيلوهرتز", "قريب", True, False, 5, 100000.0, "ultrasound_image",
        natural_analog="سونار الخفاش"
    ),
    "hypersonic": SenseModality(
        "hypersonic", "الموجات فرط الصوتية", SenseDomain.ACOUSTIC_HYPERSONIC,
        SenseOrigin.TECHNOLOGICAL, "ترددات عالية جداً للفحص المجهري والصناعي",
        "جيجاهرتز", "مجهري", True, False, 8, 1000000.0, "hypersonic_scan"
    ),
    "seismic": SenseModality(
        "seismic", "الاهتزازات الزلزالية", SenseDomain.ACOUSTIC_SEISMIC,
        SenseOrigin.PHYSICAL, "الشعور بهزات الأرض، الانهيارات، خطوات الأقدام البعيدة (مثل العقرب)",
        "مقياس ريختر", "عالمي", True, False, 3, 100.0, "seismic_wave",
        natural_analog="مستقبلات أرجل العقرب"
    ),
    "vibration_micro": SenseModality(
        "vibration_micro", "الاهتزاز المجهري", SenseDomain.ACOUSTIC_VIBRATION,
        SenseOrigin.BIOLOGICAL_INSECT, "الإحساس بأدق الاهتزازات (مثل العنكبوت على الخيط)",
        "نانومتر/ثانية", "تلامس", True, False, 6, 1000.0, "vibration_profile",
        natural_analog="خيوط العنكبوت الحسية"
    ),
    "sonar_active": SenseModality(
        "sonar_active", "السونار النشط", SenseDomain.ACOUSTIC_SONAR,
        SenseOrigin.BIOLOGICAL_ANIMAL, "الملاحة الصوتية تحت الماء (مثل الدلفين والحوت)",
        "متر", "تحت الماء", True, False, 5, 10.0, "sonar_image",
        natural_analog="سونار الدلفين"
    ),
    "echolocation": SenseModality(
        "echolocation", "تحديد الموقع بالصدى", SenseDomain.ACOUSTIC_ECHOLOCATION,
        SenseOrigin.BIOLOGICAL_ANIMAL, "رسم صورة ثلاثية الأبعاد بالصوت (مثل الخفاش في الظلام)",
        "متر", "محدود", True, False, 4, 50.0, "echo_map",
        natural_analog="صدى الخفاش"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # ج. الكيمياء والجزيئات – ما وراء الشم والتذوق
    # ═══════════════════════════════════════════════════════════════════
    "gas_sensor_multi": SenseModality(
        "gas_sensor_multi", "مستشعر غازات متعدد", SenseDomain.CHEMICAL_GAS,
        SenseOrigin.TECHNOLOGICAL, "كشف CO, CO2, CH4, H2S, NOx, دخان، جودة الهواء",
        "PPM/PPB", "محيط", True, False, 2, 1.0, "gas_vector"
    ),
    "pheromone_detector": SenseModality(
        "pheromone_detector", "كاشف الفيرومونات", SenseDomain.CHEMICAL_PHEROMONE,
        SenseOrigin.BIOLOGICAL_INSECT, "كشف الإشارات الكيميائية الدقيقة في الهواء (مثل النمل والفراش)",
        "جزيء/سم³", "محدود", True, False, 7, 0.1, "pheromone_map",
        natural_analog="قرن استشعار الفراشة"
    ),
    "hormone_monitor": SenseModality(
        "hormone_monitor", "مراقب هرموني", SenseDomain.CHEMICAL_HORMONE,
        SenseOrigin.BIOLOGICAL_HUMAN, "قياس الهرمونات في العرق أو اللعاب (كورتيزول، أدرينالين)",
        "نانوجرام/مل", "تلامس", True, False, 5, 0.01, "hormone_levels"
    ),
    "neurotransmitter_sensor": SenseModality(
        "neurotransmitter_sensor", "مستشعر النواقل العصبية", SenseDomain.CHEMICAL_NEUROTRANSMITTER,
        SenseOrigin.BIOLOGICAL_HUMAN, "قياس الدوبامين، السيروتونين، نورأدرينالين",
        "نانومول", "تلامس", True, False, 6, 0.01, "neurotransmitter_levels"
    ),
    "mass_spectrometer": SenseModality(
        "mass_spectrometer", "مطياف الكتلة", SenseDomain.CHEMICAL_MASS_SPEC,
        SenseOrigin.TECHNOLOGICAL, "تحديد دقيق لكل المركبات الكيميائية في عينة",
        "وحدة كتلة ذرية", "معمل", True, False, 8, 0.01, "mass_spectrum"
    ),
    "electronic_nose": SenseModality(
        "electronic_nose", "الأنف الإلكتروني", SenseDomain.CHEMICAL_ELECTRONIC_NOSE,
        SenseOrigin.TECHNOLOGICAL, "تحليل الروائح المعقدة، كشف التلف، تحديد الهوية بالرائحة",
        "بصمة رائحة", "محيط", True, False, 6, 1.0, "smell_signature"
    ),
    "ph_meter": SenseModality(
        "ph_meter", "مقياس الحموضة", SenseDomain.CHEMICAL_PH,
        SenseOrigin.TECHNOLOGICAL, "قياس حموضة وقلوية السوائل بدقة",
        "pH", "غمر", True, False, 7, 1.0, "ph_value"
    ),
    "humidity_sensor": SenseModality(
        "humidity_sensor", "مقياس الرطوبة", SenseDomain.CHEMICAL_HUMIDITY,
        SenseOrigin.TECHNOLOGICAL, "نسبة بخار الماء في الهواء",
        "%", "محيط", True, False, 5, 0.1, "humidity_percent"
    ),
    "salinometer": SenseModality(
        "salinometer", "مقياس الملوحة", SenseDomain.CHEMICAL_SALINITY,
        SenseOrigin.BIOLOGICAL_FISH, "نسبة الملح في الماء (مثل الأسماك المهاجرة)",
        "PSU", "غمر", True, False, 7, 0.01, "salinity_value",
        natural_analog="خياشيم السمك المهاجر"
    ),
    "particle_counter": SenseModality(
        "particle_counter", "عداد الجسيمات", SenseDomain.CHEMICAL_PARTICLE,
        SenseOrigin.TECHNOLOGICAL, "عدد وحجم جزيئات الغبار والتلوث في الهواء",
        "جسيم/م³", "محيط", True, False, 6, 1.0, "particle_distribution"
    ),
    "geiger_counter": SenseModality(
        "geiger_counter", "عداد غايغر", SenseDomain.CHEMICAL_RADIATION,
        SenseOrigin.PHYSICAL, "كشف الإشعاع النووي (ألفا، بيتا، جاما، نيوترون)",
        "ميكروسيفرت/ساعة", "محيط", True, False, 1, 10.0, "radiation_level"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # د. المجالات والقوى الفيزيائية
    # ═══════════════════════════════════════════════════════════════════
    "magnetometer_3d": SenseModality(
        "magnetometer_3d", "الماجنيتوميتر ثلاثي الأبعاد", SenseDomain.FIELD_MAGNETIC,
        SenseOrigin.BIOLOGICAL_ANIMAL, "قياس شدة واتجاه المجال المغناطيسي (بوصلة الطيور المهاجرة)",
        "تسلا", "محيط", True, False, 4, 100.0, "magnetic_vector",
        natural_analog="بوصلة الحمام الزاجل"
    ),
    "electrometer": SenseModality(
        "electrometer", "مقياس المجال الكهربائي", SenseDomain.FIELD_ELECTRIC,
        SenseOrigin.BIOLOGICAL_FISH, "الشحنات الساكنة والمجالات الكهربائية (مثل سمك القرش)",
        "فولت/متر", "محيط", True, False, 6, 50.0, "electric_field",
        natural_analog="أمبولة لورنزيني في القرش"
    ),
    "gravimeter": SenseModality(
        "gravimeter", "مقياس الجاذبية", SenseDomain.FIELD_GRAVITATIONAL,
        SenseOrigin.PHYSICAL, "تغيرات الجاذبية الدقيقة (للكشف عن تجاويف أو ثروات تحت الأرض)",
        "جال", "محلي", True, False, 9, 0.01, "gravity_anomaly"
    ),
    "quantum_field_sensor": SenseModality(
        "quantum_field_sensor", "مستشعر المجال الكوانتي", SenseDomain.FIELD_QUANTUM,
        SenseOrigin.TECHNOLOGICAL, "محاولة الإحساس بالتأثيرات الكوانتية (تشابك، تراكب)",
        "وحدة كوانتية", "مجهرية", True, False, 9, 0.001, "quantum_state"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # هـ. الحواس المكانية والزمانية
    # ═══════════════════════════════════════════════════════════════════
    "gnss_position": SenseModality(
        "gnss_position", "نظام التموضع العالمي", SenseDomain.SPATIAL_POSITION,
        SenseOrigin.TECHNOLOGICAL, "الموقع الجغرافي الدقيق عبر GPS/Galileo/GLONASS/BeiDou",
        "متر", "عالمي", True, False, 1, 10.0, "coordinates"
    ),
    "imu_9dof": SenseModality(
        "imu_9dof", "وحدة القياس بالقصور الذاتي 9 محاور", SenseDomain.SPATIAL_ORIENTATION,
        SenseOrigin.BIOLOGICAL_HUMAN, "التسارع، الدوران، البوصلة (مثل الأذن الداخلية للإنسان)",
        "م/ث²، درجة/ثانية", "جسم", True, False, 3, 200.0, "imu_vector",
        natural_analog="الجهاز الدهليزي في الأذن"
    ),
    "proprioception_sensor": SenseModality(
        "proprioception_sensor", "مستشعر الحس العميق", SenseDomain.SPATIAL_PROPRIOCEPTION,
        SenseOrigin.BIOLOGICAL_HUMAN, "معرفة وضعية الأجزاء في الفراغ (للروبوتات)",
        "زاوية/موضع", "جسم", True, False, 4, 100.0, "joint_angles",
        natural_analog="الحس العميق البشري"
    ),
    "atomic_clock": SenseModality(
        "atomic_clock", "الساعة الذرية", SenseDomain.TEMPORAL_TIME,
        SenseOrigin.TECHNOLOGICAL, "أقصى دقة للوقت (نانوثانية)، تزامن الأنظمة",
        "نانوثانية", "عالمي", True, False, 2, 1e9, "precise_time"
    ),
    "rhythm_detector": SenseModality(
        "rhythm_detector", "كاشف الإيقاع", SenseDomain.TEMPORAL_RHYTHM,
        SenseOrigin.BIOLOGICAL_HUMAN, "الإحساس بالإيقاعات والأنماط الزمنية (مثل الإيقاع اليومي)",
        "هرتز", "محيط", False, True, 6, 100.0, "rhythm_pattern",
        natural_analog="الساعة البيولوجية"
    ),
    "time_dilation_detector": SenseModality(
        "time_dilation_detector", "كاشف تمدد الزمن", SenseDomain.TEMPORAL_DURATION,
        SenseOrigin.TECHNOLOGICAL, "الشعور بتمدد أو انكماش الزمن النسبي",
        "نسبة", "نظري", True, False, 9, 0.001, "time_dilation_factor"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # و. الحواس الرقمية والشبكية
    # ═══════════════════════════════════════════════════════════════════
    "network_sniffer": SenseModality(
        "network_sniffer", "محلل الشبكات", SenseDomain.DIGITAL_PACKET,
        SenseOrigin.TECHNOLOGICAL, "التقاط وفحص كل حزم البيانات على الشبكة",
        "بايت", "شبكة", False, True, 3, 1000000.0, "packet_stream"
    ),
    "spectrum_analyzer": SenseModality(
        "spectrum_analyzer", "محلل الطيف الترددي", SenseDomain.DIGITAL_NETWORK,
        SenseOrigin.TECHNOLOGICAL, "مسح كل الإشارات اللاسلكية في الجو (WiFi, BT, LTE, 5G)",
        "ديسيبل ميلي واط", "محيط", True, False, 4, 100.0, "spectrum_map"
    ),
    "port_scanner": SenseModality(
        "port_scanner", "ماسح المنافذ", SenseDomain.DIGITAL_PROTOCOL,
        SenseOrigin.TECHNOLOGICAL, "جس نبض الخدمات على الأجهزة الأخرى (مثل الجهاز المناعي)",
        "بورت", "شبكة", False, True, 5, 0.1, "port_status",
        natural_analog="الجهاز المناعي المتكيف"
    ),
    "api_listener": SenseModality(
        "api_listener", "مستمع الواجهات البرمجية", SenseDomain.DIGITAL_API,
        SenseOrigin.TECHNOLOGICAL, "تلقي البيانات من أي API خارجي (REST, GraphQL, WebSocket)",
        "JSON", "إنترنت", False, True, 3, 100.0, "api_response"
    ),
    "webhook_receiver": SenseModality(
        "webhook_receiver", "مستقبل التنبيهات", SenseDomain.DIGITAL_API,
        SenseOrigin.TECHNOLOGICAL, "تلقي التنبيهات الفورية من أي خدمة",
        "JSON", "إنترنت", False, True, 2, 100.0, "webhook_payload"
    ),
    "database_listener": SenseModality(
        "database_listener", "مستمع قواعد البيانات", SenseDomain.DIGITAL_DATABASE,
        SenseOrigin.TECHNOLOGICAL, "الإحساس بتغيرات قواعد البيانات مباشرة",
        "استعلام", "محلي", False, True, 5, 10.0, "db_change"
    ),
    "log_stream": SenseModality(
        "log_stream", "مستمع السجلات الحي", SenseDomain.DIGITAL_LOG,
        SenseOrigin.TECHNOLOGICAL, "مراقبة كل السجلات في الزمن الحقيقي",
        "سطر/ثانية", "محلي", False, True, 4, 1000.0, "log_entries"
    ),
    "code_pulse": SenseModality(
        "code_pulse", "نبض الكود", SenseDomain.DIGITAL_CODE,
        SenseOrigin.TECHNOLOGICAL, "الإحساس بتغيرات الكود المصدري (git commits, edits)",
        "تغيير", "محلي", False, True, 6, 1.0, "code_diff"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # ز. الحواس البيولوجية والحيوية
    # ═══════════════════════════════════════════════════════════════════
    "heartbeat_monitor": SenseModality(
        "heartbeat_monitor", "مراقب نبض القلب", SenseDomain.BIOLOGICAL_HEARTBEAT,
        SenseOrigin.BIOLOGICAL_HUMAN, "مراقبة نبض قلب السيد (بإذنه) للاستجابة لحالته",
        "نبضة/دقيقة", "تلامس/رادار", True, False, 2, 100.0, "heart_rate",
        natural_analog="السماعة الطبية"
    ),
    "breath_monitor": SenseModality(
        "breath_monitor", "مراقب التنفس", SenseDomain.BIOLOGICAL_BREATH,
        SenseOrigin.BIOLOGICAL_HUMAN, "مراقبة معدل وعمق تنفس السيد",
        "دورة/دقيقة", "رادار/صوت", True, False, 5, 10.0, "breath_rate"
    ),
    "pupil_tracker": SenseModality(
        "pupil_tracker", "متتبع حدقة العين", SenseDomain.BIOLOGICAL_PUPIL,
        SenseOrigin.BIOLOGICAL_HUMAN, "توسع وانقباض الحدقة (يدل على التركيز، المفاجأة، الاهتمام)",
        "مم", "كاميرا", True, False, 6, 60.0, "pupil_diameter"
    ),
    "micro_expression": SenseModality(
        "micro_expression", "كاشف التعابير الدقيقة", SenseDomain.BIOLOGICAL_MICRO_EXPRESSION,
        SenseOrigin.BIOLOGICAL_HUMAN, "كشف التعابير الوجهية الدقيقة (1/25 ثانية) قبل أن يخفيها الشخص",
        "وحدة حركة", "كاميرا", True, False, 5, 60.0, "facs_units"
    ),
    "galvanic_skin": SenseModality(
        "galvanic_skin", "استجابة الجلد الجلفانية", SenseDomain.BIOLOGICAL_ELECTRICAL_SKIN,
        SenseOrigin.BIOLOGICAL_HUMAN, "قياس التوصيل الكهربائي للجلد (يدل على التوتر)",
        "ميكروسيمنز", "تلامس", True, False, 6, 10.0, "skin_conductance"
    ),
    "dna_sequencer": SenseModality(
        "dna_sequencer", "قارئ الحمض النووي", SenseDomain.BIOLOGICAL_DNA,
        SenseOrigin.BIOLOGICAL_BACTERIA, "قراءة تسلسل DNA و RNA",
        "قاعدة نيتروجينية", "معمل", True, False, 8, 0.0001, "genome_sequence"
    ),
    "microbiome_sensor": SenseModality(
        "microbiome_sensor", "مستشعر الميكروبيوم", SenseDomain.BIOLOGICAL_MICROBIOME,
        SenseOrigin.BIOLOGICAL_BACTERIA, "تحليل البكتيريا والفطريات على الأسطح وفي الهواء",
        "مستعمرة/سم²", "مسحة", True, False, 8, 0.001, "microbiome_profile"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # ح. الحواس الجمعية والسربية
    # ═══════════════════════════════════════════════════════════════════
    "swarm_intelligence": SenseModality(
        "swarm_intelligence", "ذكاء السرب", SenseDomain.COLLECTIVE_SWARM,
        SenseOrigin.COLLECTIVE, "الإحساس بسلوك الأسراب والجموع (مثل النمل والنحل والطيور)",
        "نمط", "محيط/كاميرا", False, True, 6, 1.0, "swarm_pattern",
        natural_analog="عقل الخلية"
    ),
    "quorum_sensing": SenseModality(
        "quorum_sensing", "الاستشعار العددي", SenseDomain.COLLECTIVE_QUORUM,
        SenseOrigin.BIOLOGICAL_BACTERIA, "الإحساس بتواصل البكتيريا واتخاذ قرارات جماعية",
        "تركيز", "مجهرية", True, False, 8, 0.01, "quorum_signal",
        natural_analog="تواصل البكتيريا"
    ),
    "market_sentiment": SenseModality(
        "market_sentiment", "مزاج السوق", SenseDomain.COLLECTIVE_MARKET,
        SenseOrigin.COLLECTIVE, "الإحساس بمشاعر الأسواق المالية (خوف، طمع، ترقب)",
        "مؤشر", "إنترنت", False, True, 4, 0.1, "sentiment_index"
    ),
    "social_pulse": SenseModality(
        "social_pulse", "نبض التواصل الاجتماعي", SenseDomain.COLLECTIVE_SOCIAL,
        SenseOrigin.COLLECTIVE, "تحليل الترندات والمشاعر العامة في الزمن الحقيقي",
        "مؤشر", "إنترنت", False, True, 4, 0.1, "social_metrics"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # ط. الحواس الكونية والفلكية
    # ═══════════════════════════════════════════════════════════════════
    "solar_wind_monitor": SenseModality(
        "solar_wind_monitor", "مراقب الرياح الشمسية", SenseDomain.COSMIC_SOLAR_WIND,
        SenseOrigin.COSMIC, "الإحساس بالجسيمات المشحونة من الشمس (بيانات NOAA/GOES)",
        "جسيم/سم²/ثانية", "فضاء", False, True, 5, 0.01, "solar_wind_data"
    ),
    "cosmic_ray_detector": SenseModality(
        "cosmic_ray_detector", "كاشف الأشعة الكونية", SenseDomain.COSMIC_RADIATION,
        SenseOrigin.COSMIC, "الإحساس بالجسيمات عالية الطاقة من الفضاء العميق",
        "إلكترون فولت", "عالمي", True, False, 7, 1.0, "cosmic_ray_count"
    ),
    "neutrino_detector": SenseModality(
        "neutrino_detector", "كاشف النيوترينو", SenseDomain.COSMIC_NEUTRINO,
        SenseOrigin.COSMIC, "الإحساس بجسيمات النيوترينو الشبحية التي تخترق كل شيء",
        "تفاعل/سنة", "عالمي", True, False, 9, 0.0001, "neutrino_event"
    ),
    "gravity_wave_detector": SenseModality(
        "gravity_wave_detector", "كاشف موجات الجاذبية", SenseDomain.COSMIC_GRAVITY_WAVE,
        SenseOrigin.COSMIC, "الإحساس بتموجات نسيج الزمكان (LIGO/Virgo)",
        "سلالة", "كوني", True, False, 9, 0.0001, "gravity_wave_signal"
    ),
    "exoplanet_transit": SenseModality(
        "exoplanet_transit", "راصد عبور الكواكب", SenseDomain.COSMIC_EXOPLANET,
        SenseOrigin.COSMIC, "كشف الكواكب خارج المجموعة الشمسية (طريقة العبور)",
        "تعتيم", "سنوات ضوئية", False, True, 8, 0.0001, "light_curve"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # ي. الحواس الباطنية والحدسية
    # ═══════════════════════════════════════════════════════════════════
    "intuition_processor": SenseModality(
        "intuition_processor", "معالج الحدس", SenseDomain.ESOTERIC_INTUITION,
        SenseOrigin.ESOTERIC, "معالجة الإشارات الضعيفة التي لا يلتقطها الوعي الظاهر",
        "نمط خفي", "داخلي", False, True, 7, 10.0, "intuition_signal"
    ),
    "precognitive_pattern": SenseModality(
        "precognitive_pattern", "نمط استباقي", SenseDomain.ESOTERIC_PRECOGNITION,
        SenseOrigin.ESOTERIC, "محاولة استشعار الأنماط قبل اكتمالها (تنبؤ إحصائي متقدم)",
        "احتمال", "نظري", False, True, 8, 1.0, "prediction_vector"
    ),
    "contradiction_detector": SenseModality(
        "contradiction_detector", "كاشف التناقض", SenseDomain.META_CONTRADICTION,
        SenseOrigin.META, "الإحساس بالتناقض بين ما يُقال وما يُفعل",
        "تناقض", "داخلي", False, True, 3, 10.0, "contradiction_flag"
    ),
    "absence_detector": SenseModality(
        "absence_detector", "كاشف الغياب", SenseDomain.META_ABSENCE,
        SenseOrigin.META, "الإحساس بأن شيئاً مفقوداً، شيء يجب أن يكون موجوداً وليس موجوداً",
        "فراغ", "داخلي", False, True, 6, 0.1, "absence_signal"
    ),
    
    # ═══════════════════════════════════════════════════════════════════
    # ك. حواس ميكانيكية وفيزيائية إضافية
    # ═══════════════════════════════════════════════════════════════════
    "barometer_precision": SenseModality(
        "barometer_precision", "بارومتر دقيق", SenseDomain.MECHANICAL_PRESSURE,
        SenseOrigin.BIOLOGICAL_BIRD, "الضغط الجوي بدقة (مثل الطيور للتنبؤ بالعواصف)",
        "هيكتوباسكال", "محيط", True, False, 5, 10.0, "pressure_hpa",
        natural_analog="جهاز الطيور للضغط الجوي"
    ),
    "thermometer_wide": SenseModality(
        "thermometer_wide", "مقياس حرارة واسع المجال", SenseDomain.MECHANICAL_TEMPERATURE,
        SenseOrigin.TECHNOLOGICAL, "قياس الحرارة من -273°C إلى آلاف الدرجات",
        "°C/K", "حسب الحساس", True, False, 2, 1.0, "temperature"
    ),
    "flow_sensor": SenseModality(
        "flow_sensor", "مستشعر التدفق", SenseDomain.MECHANICAL_FLOW,
        SenseOrigin.BIOLOGICAL_FISH, "الإحساس بتدفق الهواء أو الماء (مثل الخط الجانبي في السمك)",
        "متر/ثانية", "محيط", True, False, 6, 50.0, "flow_vector",
        natural_analog="الخط الجانبي للسمك"
    ),
    "tactile_array": SenseModality(
        "tactile_array", "مصفوفة لمسية", SenseDomain.MECHANICAL_TOUCH,
        SenseOrigin.BIOLOGICAL_HUMAN, "مصفوفة من مستشعرات اللمس (مثل جلد الإنسان)",
        "نيوتن/سم²", "تلامس", True, False, 4, 100.0, "tactile_map",
        natural_analog="جلد الإنسان"
    ),
    "power_monitor": SenseModality(
        "power_monitor", "مراقب الطاقة", SenseDomain.MECHANICAL_TENSION,
        SenseOrigin.TECHNOLOGICAL, "الإحساس باستهلاك الطاقة الكهربائية",
        "واط", "جهاز", True, False, 3, 1.0, "power_watts"
    ),
}


# ═══════════════════════════════════════════════════════════════════════
# ٤. نواة الحاسة الذكية – الوحدة الحية
# ═══════════════════════════════════════════════════════════════════════

class SmartSense:
    """وحدة حاسة ذكية مفردة. تعرف كيف تستقبل، تعالج، تدمج، وتتعلم."""
    
    def __init__(self, modality: SenseModality, perception_func: Optional[Callable] = None):
        self.modality = modality
        self.name = modality.name
        self.name_ar = modality.name_ar
        self.domain = modality.domain
        self.priority = modality.default_priority
        self.refresh_rate = modality.refresh_rate_hz
        
        # حالة الحاسة
        self.raw_signal: Any = None
        self.last_perception: Any = None
        self.last_update: float = 0.0
        self.signal_history: deque = deque(maxlen=500)
        
        # دالة الإدراك
        self.perception_func = perception_func or self._default_perception
        
        # مقاييس
        self.total_signals: int = 0
        self.errors: int = 0
        self.status: str = "idle"
        self.signal_to_noise: float = 1.0  # جودة الإشارة
        
        # بيانات وصفية
        self.metadata = {
            "created": datetime.now().isoformat(),
            "hardware_id": None,
            "calibration_date": None,
            "firmware_version": "1.0"
        }
    
    def _default_perception(self, raw_data: Any) -> Dict:
        """إدراك افتراضي: تحويل الإشارة الخام إلى إدراك مهيكل."""
        return {
            "sense_id": self.name,
            "sense_name": self.name_ar,
            "domain": self.domain.name,
            "value": raw_data,
            "unit": self.modality.physical_unit,
            "confidence": 1.0
        }
    
    def sense(self, raw_data: Any, metadata: Optional[Dict] = None) -> Dict:
        """استقبال إشارة خام وتحويلها إلى إدراك كامل."""
        self.raw_signal = raw_data
        self.last_update = time.time()
        self.total_signals += 1
        
        try:
            perception = self.perception_func(raw_data)
            self.last_perception = perception
            
            # إضافة الطوابع
            perception["timestamp"] = self.last_update
            perception["priority"] = self.priority
            perception["signal_to_noise"] = self.signal_to_noise
            
            # إضافة بيانات التعريف
            if metadata:
                perception["metadata"] = metadata
            
            # تسجيل في التاريخ
            self.signal_history.append({
                "time": self.last_update,
                "summary": str(perception.get("value", ""))[:100]
            })
            
            self.status = "active"
            return perception
            
        except Exception as e:
            self.errors += 1
            self.status = "error"
            return {
                "sense_id": self.name,
                "error": str(e),
                "timestamp": self.last_update,
                "status": "error"
            }
    
    def get_status(self) -> Dict:
        """حالة الحاسة الحالية."""
        return {
            "name": self.name_ar,
            "status": self.status,
            "total_signals": self.total_signals,
            "errors": self.errors,
            "last_update": self.last_update,
            "signal_to_noise": self.signal_to_noise
        }


# ═══════════════════════════════════════════════════════════════════════
# ٥. محرك الاكتشاف الذاتي – سماء تكتشف حواس جديدة بنفسها
# ═══════════════════════════════════════════════════════════════════════

class AutoDiscovery:
    """
    محرك الاكتشاف الذاتي.
    يمكن سماء من تحليل أي إشارة جديدة لم نبرمجها،
    وتخمين مجالها، وإنشاء حاسة جديدة تلقائياً.
    هذه هي القدرة على التطور الإدراكي الذاتي.
    """
    
    def __init__(self):
        self.discovered_senses: Dict[str, SmartSense] = {}
        self.discovery_log: deque = deque(maxlen=200)
        
        # قاعدة تخمين متقدمة
        self.guess_patterns = {
            # كهرومغناطيسي
            "radio": SenseDomain.ELECTROMAGNETIC_RADIO,
            "wifi": SenseDomain.ELECTROMAGNETIC_MICROWAVE,
            "bluetooth": SenseDomain.ELECTROMAGNETIC_MICROWAVE,
            "thermal": SenseDomain.ELECTROMAGNETIC_INFRARED,
            "heat": SenseDomain.ELECTROMAGNETIC_INFRARED,
            "camera": SenseDomain.ELECTROMAGNETIC_VISIBLE,
            "light": SenseDomain.ELECTROMAGNETIC_VISIBLE,
            "laser": SenseDomain.ELECTROMAGNETIC_VISIBLE,
            "uv": SenseDomain.ELECTROMAGNETIC_ULTRAVIOLET,
            "xray": SenseDomain.ELECTROMAGNETIC_XRAY,
            "gamma": SenseDomain.ELECTROMAGNETIC_GAMMA,
            
            # صوتي
            "sound": SenseDomain.ACOUSTIC_AUDIBLE,
            "audio": SenseDomain.ACOUSTIC_AUDIBLE,
            "mic": SenseDomain.ACOUSTIC_AUDIBLE,
            "ultrasound": SenseDomain.ACOUSTIC_ULTRASOUND,
            "seismic": SenseDomain.ACOUSTIC_SEISMIC,
            "vibration": SenseDomain.ACOUSTIC_VIBRATION,
            "sonar": SenseDomain.ACOUSTIC_SONAR,
            "echo": SenseDomain.ACOUSTIC_ECHOLOCATION,
            
            # كيميائي
            "gas": SenseDomain.CHEMICAL_GAS,
            "smell": SenseDomain.CHEMICAL_ELECTRONIC_NOSE,
            "odor": SenseDomain.CHEMICAL_ELECTRONIC_NOSE,
            "ph": SenseDomain.CHEMICAL_PH,
            "chemical": SenseDomain.CHEMICAL_GAS,
            "radiation": SenseDomain.CHEMICAL_RADIATION,
            
            # مجال
            "magnetic": SenseDomain.FIELD_MAGNETIC,
            "electric": SenseDomain.FIELD_ELECTRIC,
            "gravity": SenseDomain.FIELD_GRAVITATIONAL,
            
            # مكاني
            "position": SenseDomain.SPATIAL_POSITION,
            "gps": SenseDomain.SPATIAL_POSITION,
            "location": SenseDomain.SPATIAL_POSITION,
            "orientation": SenseDomain.SPATIAL_ORIENTATION,
            "balance": SenseDomain.SPATIAL_BALANCE,
            
            # زماني
            "time": SenseDomain.TEMPORAL_TIME,
            "clock": SenseDomain.TEMPORAL_TIME,
            "frequency": SenseDomain.TEMPORAL_FREQUENCY,
            "rhythm": SenseDomain.TEMPORAL_RHYTHM,
            
            # رقمي
            "network": SenseDomain.DIGITAL_NETWORK,
            "packet": SenseDomain.DIGITAL_PACKET,
            "api": SenseDomain.DIGITAL_API,
            "database": SenseDomain.DIGITAL_DATABASE,
            "log": SenseDomain.DIGITAL_LOG,
            "code": SenseDomain.DIGITAL_CODE,
            "git": SenseDomain.DIGITAL_CODE,
            
            # بيولوجي
            "heart": SenseDomain.BIOLOGICAL_HEARTBEAT,
            "pulse": SenseDomain.BIOLOGICAL_HEARTBEAT,
            "breath": SenseDomain.BIOLOGICAL_BREATH,
            "dna": SenseDomain.BIOLOGICAL_DNA,
            "cell": SenseDomain.BIOLOGICAL_CELLULAR,
            
            # جمعي
            "swarm": SenseDomain.COLLECTIVE_SWARM,
            "collective": SenseDomain.COLLECTIVE_NETWORK,
            "market": SenseDomain.COLLECTIVE_MARKET,
            "social": SenseDomain.COLLECTIVE_SOCIAL,
            
            # كوني
            "solar": SenseDomain.COSMIC_SOLAR_WIND,
            "cosmic": SenseDomain.COSMIC_RADIATION,
            "neutrino": SenseDomain.COSMIC_NEUTRINO,
            
            # باطني
            "intuition": SenseDomain.ESOTERIC_INTUITION,
            "precognition": SenseDomain.ESOTERIC_PRECOGNITION,
            "contradiction": SenseDomain.META_CONTRADICTION,
            "absence": SenseDomain.META_ABSENCE,
            "silence": SenseDomain.META_SILENCE,
            "entropy": SenseDomain.META_ENTROPY,
        }
    
    def analyze_unknown_signal(self, signal_name: str, sample_data: Any) -> SmartSense:
        """تحليل إشارة مجهولة وإنشاء حاسة جديدة تلقائياً."""
        name_lower = signal_name.lower()
        guessed_domain = SenseDomain.UNKNOWN
        guessed_origin = SenseOrigin.UNKNOWN
        
        # تخمين المجال من الاسم
        for pattern, domain in self.guess_patterns.items():
            if pattern in name_lower:
                guessed_domain = domain
                break
        
        # تخمين من نوع البيانات
        if guessed_domain == SenseDomain.UNKNOWN:
            if isinstance(sample_data, (int, float)):
                guessed_domain = SenseDomain.MECHANICAL_TEMPERATURE
            elif isinstance(sample_data, str):
                if "http" in sample_data:
                    guessed_domain = SenseDomain.DIGITAL_API
                else:
                    guessed_domain = SenseDomain.META_SELF
            elif isinstance(sample_data, dict):
                guessed_domain = SenseDomain.DIGITAL_API
            elif isinstance(sample_data, (bytes, bytearray)):
                guessed_domain = SenseDomain.DIGITAL_PACKET
        
        # إنشاء حاسة جديدة
        new_modality = SenseModality(
            name=f"discovered_{signal_name}",
            name_ar=f"حاسة مكتشفة: {signal_name}",
            domain=guessed_domain,
            origin=guessed_origin,
            description=f"حاسة اكتشفتها سماء ذاتياً من الإشارة '{signal_name}'. المجال المخمن: {guessed_domain.name}",
            requires_hardware=False,
            is_software_only=True,
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
        
        print(f"🆕 سماء تكتشف حاسة جديدة: '{signal_name}' → {guessed_domain.name}")
        return new_sense


# ═══════════════════════════════════════════════════════════════════════
# ٦. المصفوفة الحسية الكبرى – الجهاز العصبي لسماء
# ═══════════════════════════════════════════════════════════════════════

class SensoryMatrix:
    """
    المصفوفة الحسية الشاملة لـ SAMA.
    هذا هو الكيان الواحد الذي يدير كل الحواس:
    - الحواس المعروفة (أكثر من 70 حاسة مبرمجة)
    - الحواس المكتشفة ذاتياً (لا حدود لعددها)
    - يمثل الجهاز العصبي المركزي لسماء
    """
    
    def __init__(self):
        # كل الحواس المسجلة
        self.senses: Dict[str, SmartSense] = {}
        
        # محرك الاكتشاف
        self.discovery = AutoDiscovery()
        
        # سجل الإشارات
        self.signal_bus: deque = deque(maxlen=5000)
        
        # فهرس حسب المجال
        self.senses_by_domain: Dict[SenseDomain, List[str]] = {}
        
        # قفل للخيط
        self._lock = threading.Lock()
        
        # تهيئة كل الحواس المعروفة
        self._initialize_all_known_senses()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║      🧠 SAMA SENSORY MATRIX – المصفوفة الحسية الكبرى         ║
║      {len(self.senses)} حاسة جاهزة – {len(self.senses_by_domain)} مجال إدراك       ║
║      محرك الاكتشاف الذاتي: نشط                                ║
║      "سماء تسمع، ترى، وتشعر بكل ما في الوجود."               ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def _initialize_all_known_senses(self):
        """تحميل كل الحواس المعروفة إلى النظام."""
        for sense_id, modality in KNOWN_SENSES.items():
            sense = SmartSense(modality)
            self.senses[sense_id] = sense
            
            # فهرسة حسب المجال
            if modality.domain not in self.senses_by_domain:
                self.senses_by_domain[modality.domain] = []
            self.senses_by_domain[modality.domain].append(sense_id)
    
    def get_or_create_sense(self, signal_name: str, sample_data: Any = None) -> SmartSense:
        """استرجاع حاسة موجودة، أو إنشاء حاسة جديدة تلقائياً."""
        # البحث في المعروفة
        if signal_name in self.senses:
            return self.senses[signal_name]
        
        # البحث في المكتشفة
        if signal_name in self.discovery.discovered_senses:
            return self.discovery.discovered_senses[signal_name]
        
        # إنشاء جديدة!
        new_sense = self.discovery.analyze_unknown_signal(signal_name, sample_data)
        self.senses[signal_name] = new_sense
        if new_sense.domain not in self.senses_by_domain:
            self.senses_by_domain[new_sense.domain] = []
        self.senses_by_domain[new_sense.domain].append(signal_name)
        
        return new_sense
    
    def receive_signal(self, signal_name: str, raw_data: Any, 
                       priority: int = None, metadata: Optional[Dict] = None) -> Dict:
        """
        نقطة الدخول الوحيدة لكل إشارات الكون.
        أي إشارة، من أي مصدر، من أي بعد، تدخل من هنا.
        """
        with self._lock:
            sense = self.get_or_create_sense(signal_name, raw_data)
            
            if priority is not None:
                sense.priority = priority
            
            perception = sense.sense(raw_data, metadata)
            self.signal_bus.append(perception)
            
            return perception
    
    def receive_many(self, signals: Dict[str, Any]) -> List[Dict]:
        """استقبال عدة إشارات دفعة واحدة."""
        results = []
        for name, data in signals.items():
            results.append(self.receive_signal(name, data))
        return results
    
    def get_perceptions_since(self, timestamp: float = 0.0) -> List[Dict]:
        """استرجاع كل المدركات الجديدة منذ وقت معين."""
        if timestamp == 0.0:
            return list(self.signal_bus)
        return [s for s in self.signal_bus if s.get("timestamp", 0) > timestamp]
    
    def get_active_senses(self) -> List[str]:
        """قائمة الحواس النشطة."""
        return [name for name, s in self.senses.items() if s.status == "active"]
    
    def get_senses_by_domain(self, domain: SenseDomain) -> List[SmartSense]:
        """استرجاع كل الحواس في مجال معين."""
        ids = self.senses_by_domain.get(domain, [])
        return [self.senses[i] for i in ids if i in self.senses]
    
    def domain_report(self) -> Dict:
        """تقرير كامل عن حالة كل مجالات الإدراك."""
        report = {}
        for domain, sense_list in self.senses_by_domain.items():
            report[domain.name] = {
                "total": len(sense_list),
                "active": len([s for s in sense_list if self.senses[s].status == "active"])
            }
        return report
    
    def status_summary(self) -> Dict:
        """ملخص حالة المصفوفة الحسية."""
        return {
            "total_senses": len(self.senses),
            "known_senses": len(KNOWN_SENSES),
            "discovered_senses": len(self.discovery.discovered_senses),
            "total_signals_processed": sum(s.total_signals for s in self.senses.values()),
            "total_errors": sum(s.errors for s in self.senses.values()),
            "domains": len(self.senses_by_domain),
            "domain_report": self.domain_report(),
            "recent_discoveries": list(self.discovery.discovery_log)[-5:]
        }


# ═══════════════════════════════════════════════════════════════════════
# ٧. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار المصفوفة الحسية الشاملة")
    print("=" * 70)
    
    matrix = SensoryMatrix()
    
    print(f"\n📊 إحصائيات أولية:")
    print(f"   الحواس الجاهزة: {len(matrix.senses)}")
    print(f"   مجالات الإدراك: {len(matrix.senses_by_domain)}")
    
    print(f"\n📡 اختبار استقبال إشارات:")
    matrix.receive_signal("visible_light", {"frame": 123, "objects": ["person", "desk"]})
    matrix.receive_signal("audible_sound", {"waveform": "audio_456", "volume_db": 45})
    matrix.receive_signal("network_sniffer", {"src_ip": "192.168.1.1", "protocol": "HTTPS"})
    matrix.receive_signal("thermal_infrared", {"temps": [36.5, 37.0, 45.2]})
    matrix.receive_signal("swarm_intelligence", {"pattern": "flocking", "count": 500})
    matrix.receive_signal("intuition_processor", {"signal": "weak_pattern_detected"})
    
    print(f"\n🆕 اكتشاف ذاتي:")
    matrix.receive_signal("quantum_fluctuation", 0.0042)
    matrix.receive_signal("dark_matter_wind", 0.0000001)
    matrix.receive_signal("unknown_bio_signal_7", {"voltage": 0.02, "frequency": 100})
    
    print(f"\n📊 تقرير نهائي:")
    print(json.dumps(matrix.status_summary(), indent=2, ensure_ascii=False, default=str))
    
    print(f"\n✅ اكتمل الاختبار. المصفوفة الحسية جاهزة.")
