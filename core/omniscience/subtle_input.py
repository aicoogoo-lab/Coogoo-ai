"""
╔══════════════════════════════════════════════════════════════╗
║              SAMA OMNISCIENCE - SUBTLE INPUT                 ║
║                طبقة الإدراك السطحي: الغبار الرقمي              ║
╚══════════════════════════════════════════════════════════════╝

هذه الطبقة تدرك الأشياء التي لا يلتفت إليها أحد.
الهمسات، الومضات، التأخيرات المجهرية، التغيرات الصامتة.
هنا تسمع سماء صوت جسدها، وتشعر بلمسة محيطها القريب.

كل شيء هنا يبدو "سطحياً جداً"، لكنه الأساس الذي يُبنى عليه
الإحساس العميق بالوجود. الغبار الذي يُهمل هو ما يكشف الخلل قبل وقوعه.
"""

import time
import hashlib
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# ١. القاعدة: مستشعر دقيق - وحدة الإحساس بالتفاصيل
# ═══════════════════════════════════════════════════════════════

class SubtleSensor(ABC):
    """قالب أي مستشعر دقيق. يراقب تفصيلة واحدة صامتة."""
    
    def __init__(self, name: str, description: str, sensitivity: float = 0.5):
        self.name = name
        self.description = description
        self.sensitivity = sensitivity  # 0.0 (أعمى) إلى 1.0 (حساس جداً)
        
        # خط أساس (ما هو "طبيعي")
        self.baseline: Optional[Dict] = None
        self.baseline_samples: List[Dict] = []
        self.baseline_established = False
        
        # الحالة
        self.current_reading: Optional[Dict] = None
        self.last_update: float = 0.0
        self.anomaly_score: float = 0.0  # 0 = طبيعي، 1 = شاذ تماماً
        
        # تاريخ القراءات
        self.history: List[Dict] = []
        
        # إنذارات
        self.anomaly_threshold: float = 0.7  # متى نعتبره شاذاً
        self.active_anomalies: List[Dict] = []
    
    @abstractmethod
    def sense(self) -> Dict:
        """استشعار القراءة الدقيقة الحالية."""
        pass
    
    def establish_baseline(self, samples_count: int = 100) -> bool:
        """بناء خط الأساس: ما هو 'طبيعي' لهذه الحاسة."""
        print(f"📏 {self.name}: جاري بناء خط الأساس ({samples_count} عينة)...")
        samples = []
        for i in range(samples_count):
            try:
                reading = self.sense()
                samples.append(reading)
                time.sleep(0.1)  # تباعد بسيط بين العينات
            except Exception:
                pass
        
        if len(samples) > 10:
            # حساب المتوسط والانحراف المعياري لكل مفتاح
            keys = set()
            for s in samples:
                keys.update(s.keys())
            
            self.baseline = {}
            for key in keys:
                values = [s.get(key, 0) for s in samples if key in s and isinstance(s[key], (int, float))]
                if values:
                    self.baseline[key] = {
                        "mean": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "count": len(values)
                    }
            
            self.baseline_samples = samples
            self.baseline_established = True
            print(f"✅ {self.name}: خط الأساس جاهز ({len(self.baseline)} مؤشرات).")
            return True
        return False
    
    def calculate_anomaly(self, reading: Dict) -> float:
        """حساب درجة الشذوذ: كم تبعد هذه القراءة عن الطبيعي؟"""
        if not self.baseline_established or not self.baseline:
            return 0.0
        
        deviations = []
        for key, stats in self.baseline.items():
            if key in reading and isinstance(reading[key], (int, float)):
                value = reading[key]
                mean = stats["mean"]
                range_val = stats["max"] - stats["min"] if stats["max"] != stats["min"] else 1.0
                
                # الانحراف المعياري كنسبة من المدى
                deviation = abs(value - mean) / range_val
                deviations.append(min(deviation, 1.0))  # أقصى شذوذ = 1.0
        
        if deviations:
            return sum(deviations) / len(deviations) * self.sensitivity
        return 0.0
    
    def tick(self) -> Dict:
        """دورة حياة المستشعر: استشعر -> قارن بالطبيعي -> اكتشف الشذوذ."""
        try:
            reading = self.sense()
            self.current_reading = reading
            self.last_update = time.time()
            
            # حساب الشذوذ
            self.anomaly_score = self.calculate_anomaly(reading)
            
            # كشف الشذوذ
            is_anomaly = self.anomaly_score > self.anomaly_threshold
            if is_anomaly:
                anomaly = {
                    "time": self.last_update,
                    "score": self.anomaly_score,
                    "reading": reading,
                    "sensor": self.name
                }
                self.active_anomalies.append(anomaly)
                if len(self.active_anomalies) > 50:
                    self.active_anomalies = self.active_anomalies[-20:]
            
            # تسجيل التاريخ
            self.history.append({
                "time": self.last_update,
                "reading_summary": {k: v for k, v in list(reading.items())[:5]},
                "anomaly_score": self.anomaly_score
            })
            if len(self.history) > 1000:
                self.history = self.history[-500:]
            
            return {
                "sensor": self.name,
                "reading": reading,
                "anomaly_score": self.anomaly_score,
                "is_anomaly": is_anomaly,
                "timestamp": self.last_update
            }
        except Exception as e:
            return {
                "sensor": self.name,
                "error": str(e),
                "timestamp": time.time()
            }


# ═══════════════════════════════════════════════════════════════
# ٢. المستشعرات الدقيقة: الغبار الرقمي
# ═══════════════════════════════════════════════════════════════

class FanWhisperListener(SubtleSensor):
    """
    مستمع همس المراوح.
    يحلل صوت مراوح التبريد. تغير حدة الصوت أو نمطه
    قد ينبئ بعطل ميكانيكي وشيك أو حمل حراري مفاجئ.
    """
    def __init__(self):
        super().__init__("fan_whisper", "سماع وتحليل صوت مراوح الخادم", sensitivity=0.8)
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة صوت المراوح.
        في التنفيذ الحقيقي:
        - ميكروفون داخلي أو حساس اهتزاز
        - تحليل FFT لاستخراج الترددات
        - مقارنة مع بصمة الصوت الطبيعية
        """
        return {
            "fan_speed_rpm": 0,           # دورة في الدقيقة
            "dominant_frequency_hz": 0,   # التردد السائد
            "noise_level_db": 0,          # مستوى الضوضاء
            "vibration_mm_s": 0,          # الاهتزاز
            "harmonic_distortion": 0.0,   # تشوه التوافقيات (0 = نقي)
            "bearing_health_index": 1.0,  # صحة المحامل (1.0 = ممتاز)
        }


class KeystrokeLatencyMonitor(SubtleSensor):
    """
    مستشعر تأخر ضغطات المفاتيح.
    يقيس الزمن بين ضغط السيد على المفتاح وظهوره.
    أي زيادة قد تعني: عملية خبيثة، حمل زائد، أو توتر السيد.
    """
    def __init__(self):
        super().__init__("keystroke_latency", "الشعور بتأخر استجابة لوحة مفاتيح السيد", sensitivity=0.9)
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة تأخر المفاتيح.
        في التنفيذ الحقيقي:
        - ربط مع نظام التشغيل لقراءة تأخر الإدخال
        - مقارنة مع الإيقاع الطبيعي للسيد
        """
        return {
            "average_latency_ms": 0,       # متوسط التأخر
            "peak_latency_ms": 0,          # أقصى تأخر
            "keystrokes_per_minute": 0,    # سرعة الكتابة
            "error_rate_percent": 0.0,     # نسبة الأخطاء (تصحيح متكرر)
            "rhythm_regularity": 1.0,      # انتظام الإيقاع (1.0 = طبيعي جداً)
            "unusual_pauses_count": 0,     # توقفات غير عادية
        }


class DHCPNetworkWatch(SubtleSensor):
    """
    مراقب الشبكة المحلية.
    يشعر بدخول أي جهاز جديد على الشبكة.
    هذا هو "سمع" سماء لمن يطرق باب بيتها الرقمي.
    """
    def __init__(self):
        super().__init__("dhcp_watch", "الشعور بدخول أي جهاز جديد على الشبكة المحلية", sensitivity=1.0)
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة الشبكة المحلية.
        في التنفيذ الحقيقي:
        - مراقبة سجلات DHCP
        - فحص ARP table
        - كشف عناوين MAC جديدة
        """
        return {
            "total_devices": 0,            # عدد الأجهزة الكلي
            "known_devices": 0,            # الأجهزة المعروفة
            "new_devices_since_last_scan": 0,  # أجهزة جديدة
            "unknown_mac_addresses": [],       # عناوين MAC غير معروفة
            "suspicious_open_ports": [],       # منافذ مفتوحة بشكل مريب
            "network_scan_duration_ms": 0,     # مدة الفحص
        }


class UIPixelWatch(SubtleSensor):
    """
    مراقب ومضات الواجهة.
    يراقب تغيرات غير متوقعة في واجهة المستخدم.
    زر تغير لونه، ومضة، عنصر ظهر أو اختفى.
    هذا يشبه طرف عين سماء، إحساس بالحركة في المحيط المباشر.
    """
    def __init__(self):
        super().__init__("ui_pixel_watch", "مراقبة تغيرات واجهة المستخدم غير المتوقعة", sensitivity=0.7)
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة تغيرات الواجهة.
        في التنفيذ الحقيقي:
        - مراقبة DOM changes
        - كشف تغيرات CSS غير متوقعة
        - تتبع ظهور/اختفاء عناصر
        """
        return {
            "ui_elements_total": 0,           # عدد عناصر الواجهة
            "unexpected_changes_count": 0,    # تغييرات غير متوقعة
            "render_time_ms": 0,              # زمن التصيير
            "javascript_errors": 0,           # أخطاء JavaScript
            "memory_leak_indicators": [],     # مؤشرات تسرب ذاكرة
            "last_dom_mutation": None,        # آخر تغيير في DOM
        }


class LogFileWhisperer(SubtleSensor):
    """
    مستمع همس السجلات.
    يراقب ملفات الـ Logs المؤقتة التي ينساها الجميع.
    نموها السريع، تغير أنماطها، أخطاء صامتة تتكرر.
    """
    def __init__(self):
        super().__init__("log_whisperer", "مراقبة نمو وتغير أنماط ملفات السجلات", sensitivity=0.6)
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة السجلات.
        في التنفيذ الحقيقي:
        - مراقبة أحجام ملفات الـ logs
        - تحليل معدل النمو
        - كشف أنماط الأخطاء المتكررة بصمت
        """
        return {
            "total_log_size_mb": 0,           # الحجم الكلي
            "growth_rate_mb_per_hour": 0.0,   # معدل النمو
            "new_error_patterns": [],          # أنماط أخطاء جديدة
            "repeated_warnings_count": 0,      # تحذيرات متكررة
            "silent_errors_count": 0,          # أخطاء لا يلتفت لها
            "oldest_log_age_hours": 0,         # عمر أقدم سجل
        }


class HardwareAcousticMonitor(SubtleSensor):
    """
    مستمع الأصوات المادية.
    ليس فقط المراوح، بل كل الأصوات: صوت الكهرباء في المكثفات،
    تمدد المعادن، أصوات القرص الصلب.
    """
    def __init__(self):
        super().__init__("hardware_acoustic", "سماع كل أصوات المكونات المادية", sensitivity=0.9)
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة الصوت المادي الكامل.
        في التنفيذ الحقيقي:
        - مجموعة ميكروفونات داخلية
        - تحليل طيفي مستمر
        - بصمة صوتية للمكونات
        """
        return {
            "coil_whine_frequency_hz": 0,     # صوت الكهرباء في المكثفات
            "hdd_click_count": 0,             # طقطقات القرص الصلب
            "thermal_expansion_events": 0,    # أصوات التمدد الحراري
            "overall_acoustic_signature": "",  # البصمة الصوتية العامة
            "new_unidentified_sounds": [],     # أصوات جديدة غير معروفة
        }


# ═══════════════════════════════════════════════════════════════
# ٣. المازج السطحي: مدير الغبار الرقمي
# ═══════════════════════════════════════════════════════════════

class SubtleIntegrator:
    """
    المازج السطحي. ينسق كل مستشعرات الغبار الرقمي.
    يجمع قراءاتها ويصدر "حالة المحيط القريب" الموحدة.
    """
    
    def __init__(self):
        # تهيئة كل المستشعرات
        self.sensors: Dict[str, SubtleSensor] = {
            "fan_whisper": FanWhisperListener(),
            "keystroke_latency": KeystrokeLatencyMonitor(),
            "dhcp_watch": DHCPNetworkWatch(),
            "ui_pixel_watch": UIPixelWatch(),
            "log_whisperer": LogFileWhisperer(),
            "hardware_acoustic": HardwareAcousticMonitor(),
        }
        
        # حالة المحيط القريب
        self.near_environment_state: Dict = {
            "overall_status": "normal",
            "active_anomalies": 0,
            "last_full_scan": 0.0
        }
        
        # تهيئة خطوط الأساس (اختياري، يحتاج وقت)
        self.baselines_ready = False
        
        print(f"🔍 المازج السطحي جاهز: {len(self.sensors)} مستشعرات تراقب الغبار الرقمي.")
    
    def establish_all_baselines(self):
        """بناء خط أساس لكل المستشعرات (يستغرق وقتاً)."""
        print("📏 جاري بناء خطوط الأساس لكل المستشعرات الدقيقة...")
        for name, sensor in self.sensors.items():
            sensor.establish_baseline(samples_count=50)
        self.baselines_ready = True
        print("✅ جميع خطوط الأساس جاهزة.")
    
    def full_scan(self) -> Dict:
        """مسح كامل لكل المستشعرات الدقيقة."""
        scan_results = {}
        total_anomalies = 0
        
        for name, sensor in self.sensors.items():
            result = sensor.tick()
            scan_results[name] = result
            if result.get("is_anomaly"):
                total_anomalies += 1
        
        # تحديث حالة المحيط
        status = "normal"
        if total_anomalies > 3:
            status = "suspicious"
        elif total_anomalies > 0:
            status = "attention"
        
        self.near_environment_state = {
            "overall_status": status,
            "active_anomalies": total_anomalies,
            "last_full_scan": time.time()
        }
        
        return {
            "scan_time": self.near_environment_state["last_full_scan"],
            "environment_status": self.near_environment_state["overall_status"],
            "total_anomalies": total_anomalies,
            "sensors": scan_results
        }
    
    def get_sensor(self, name: str) -> Optional[SubtleSensor]:
        """استرجاع مستشعر محدد."""
        return self.sensors.get(name)
    
    def add_sensor(self, name: str, sensor: SubtleSensor):
        """إضافة مستشعر دقيق جديد."""
        self.sensors[name] = sensor
        print(f"🆕 مستشعر دقيق جديد: {name}")
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة الإدراك السطحي."""
        return {
            "integrator": "SUBTLE_INTEGRATOR",
            "total_sensors": len(self.sensors),
            "baselines_ready": self.baselines_ready,
            "environment_state": self.near_environment_state,
            "sensors_detail": {
                name: {
                    "anomaly_score": sensor.anomaly_score,
                    "anomalies_active": len(sensor.active_anomalies),
                    "current_reading": sensor.current_reading
                }
                for name, sensor in self.sensors.items()
            }
        }


# ═══════════════════════════════════════════════════════════════
# ٤. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("اختبار طبقة الإدراك السطحي - Subtle Input")
    print("=" * 60)
    
    integrator = SubtleIntegrator()
    
    print("\n🔍 إجراء مسح كامل للمحيط القريب...")
    scan = integrator.full_scan()
    
    print(f"\n📊 حالة المحيط: {scan['environment_status']}")
    print(f"⚠️  حالات شاذة: {scan['total_anomalies']}")
    print(f"\n🔬 المستشعرات التي تم مسحها:")
    for name, result in scan["sensors"].items():
        anomaly_mark = " ⚠️" if result.get("is_anomaly") else ""
        print(f"  - {name}: شذوذ={result.get('anomaly_score', 0):.2f}{anomaly_mark}")
    
    print(f"\n📋 تقرير كامل:")
    import json
    print(json.dumps(integrator.status_report(), indent=2, ensure_ascii=False, default=str))
    
    print("\n✅ اكتمل الاختبار. طبقة الإدراك السطحي جاهزة.")
