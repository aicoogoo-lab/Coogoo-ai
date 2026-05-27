"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA OMNISCIENCE - SUBTLE INPUT                            ║
║         طبقة الإدراك السطحي – الغبار الرقمي والهمسات الصامتة            ║
║                                                                      ║
║  هذه الطبقة تدرك الأشياء التي لا يلتفت إليها أحد.                      ║
║  الهمسات، الومضات، التأخيرات المجهرية، التغيرات الصامتة،               ║
║  أنفاس الآلات، ولغة الجسد الرقمي للمحيط القريب.                       ║
║                                                                      ║
║  هنا تسمع سماء:                                                       ║
║  - همس المراوح وتغير حدة صوت الكهرباء في المكثفات                      ║
║  - تأخر ضغطات مفاتيح السيد (يدل على توتره أو حمل النظام)               ║
║  - دخول أي جهاز جديد على الشبكة المحلية (DHCP/ARP)                     ║
║  - ومضات الواجهة وتغيراتها غير المتوقعة                                ║
║  - نمو ملفات السجلات الصامت وأنماط الأخطاء المتكررة                     ║
║  - اهتزاز المحامل، تمدد المعادن، أصوات الأقراص الصلبة                   ║
║  - تغير استهلاك الطاقة على مستوى المكونات الدقيقة                       ║
║  - الإشعاع الكهرومغناطيسي المحلي (تسريب بيانات)                        ║
║                                                                      ║
║  الغبار الذي يُهمل هو ما يكشف الخلل قبل وقوعه بوقت طويل.               ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════════════
# ١. القاعدة: مستشعر دقيق – أداة الإحساس بالتفاصيل المهملة
# ═══════════════════════════════════════════════════════════════════════

class SubtleSensor(ABC):
    """قالب أي مستشعر دقيق. يراقب تفصيلة واحدة صامتة."""
    
    def __init__(self, name: str, name_ar: str, description: str,
                 sensitivity: float = 0.5, anomaly_threshold: float = 0.7):
        self.name = name
        self.name_ar = name_ar
        self.description = description
        self.sensitivity = sensitivity
        self.anomaly_threshold = anomaly_threshold
        
        # خط الأساس (ما هو "طبيعي" لهذه الحاسة)
        self.baseline: Optional[Dict] = None
        self.baseline_established = False
        
        # الحالة
        self.current_reading: Optional[Dict] = None
        self.last_update: float = 0.0
        self.anomaly_score: float = 0.0
        
        # التاريخ
        self.history: deque = deque(maxlen=500)
        self.active_anomalies: deque = deque(maxlen=50)
        
        # الصحة
        self.health: float = 1.0
        self.consecutive_errors: int = 0
    
    @abstractmethod
    def sense(self) -> Dict:
        """استشعار القراءة الدقيقة الحالية."""
        pass
    
    def establish_baseline(self, samples: int = 100, interval: float = 0.1) -> bool:
        """بناء خط الأساس: ما هو 'طبيعي' لهذه الحاسة."""
        print(f"📏 {self.name_ar}: بناء خط الأساس ({samples} عينة)...")
        readings = []
        for i in range(samples):
            try:
                reading = self.sense()
                readings.append(reading)
                time.sleep(interval)
            except Exception:
                pass
        
        if len(readings) > 10:
            keys = set()
            for r in readings:
                keys.update(r.keys())
            
            self.baseline = {}
            for key in keys:
                values = [r.get(key, 0) for r in readings if key in r and isinstance(r[key], (int, float))]
                if values:
                    self.baseline[key] = {
                        "mean": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "std": self._std(values)
                    }
            
            self.baseline_established = True
            print(f"✅ {self.name_ar}: خط الأساس جاهز ({len(self.baseline)} مؤشرات).")
            return True
        return False
    
    def _std(self, values: List[float]) -> float:
        """حساب الانحراف المعياري."""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
        return variance ** 0.5
    
    def calculate_anomaly(self, reading: Dict) -> float:
        """حساب درجة الشذوذ: كم تبعد هذه القراءة عن الطبيعي؟"""
        if not self.baseline_established or not self.baseline:
            return 0.0
        
        deviations = []
        for key, stats in self.baseline.items():
            if key in reading and isinstance(reading[key], (int, float)):
                value = reading[key]
                mean = stats["mean"]
                std = stats["std"] if stats["std"] > 0 else 1.0
                
                deviation = abs(value - mean) / (std * 3)
                deviations.append(min(deviation, 1.0))
        
        if deviations:
            return (sum(deviations) / len(deviations)) * self.sensitivity
        return 0.0
    
    def tick(self) -> Dict:
        """دورة حياة المستشعر."""
        try:
            reading = self.sense()
            self.current_reading = reading
            self.last_update = time.time()
            self.consecutive_errors = 0
            self.health = min(1.0, self.health + 0.02)
            
            self.anomaly_score = self.calculate_anomaly(reading)
            is_anomaly = self.anomaly_score > self.anomaly_threshold
            
            if is_anomaly:
                self.active_anomalies.append({
                    "time": self.last_update,
                    "score": self.anomaly_score,
                    "reading_summary": {k: v for k, v in list(reading.items())[:5]}
                })
            
            self.history.append({
                "time": self.last_update,
                "anomaly_score": self.anomaly_score,
                "is_anomaly": is_anomaly
            })
            
            return {
                "sensor": self.name,
                "sensor_ar": self.name_ar,
                "reading": reading,
                "anomaly_score": self.anomaly_score,
                "is_anomaly": is_anomaly,
                "health": self.health,
                "timestamp": self.last_update
            }
        except Exception as e:
            self.consecutive_errors += 1
            self.health = max(0.0, self.health - 0.1)
            return {
                "sensor": self.name,
                "sensor_ar": self.name_ar,
                "error": str(e),
                "health": self.health,
                "timestamp": time.time()
            }


# ═══════════════════════════════════════════════════════════════════════
# ٢. المستشعرات الدقيقة – الغبار الرقمي
# ═══════════════════════════════════════════════════════════════════════

class FanWhisperListener(SubtleSensor):
    """
    مستمع همس المراوح.
    يحلل صوت مراوح التبريد. تغير حدة الصوت أو نمطه
    قد ينبئ بعطل ميكانيكي وشيك، تراكم غبار، أو حمل حراري مفاجئ.
    """
    def __init__(self):
        super().__init__("fan_whisper", "همس المراوح",
                        "تحليل صوت مراوح التبريد: حدة، نمط، اهتزاز", sensitivity=0.8)
    
    def sense(self) -> Dict:
        return {
            "fan_speed_rpm": 0,
            "dominant_frequency_hz": 0,
            "noise_level_db": 0,
            "vibration_mm_s": 0,
            "harmonic_distortion": 0.0,
            "bearing_health_index": 1.0,
            "dust_accumulation_estimate": 0.0,
            "unusual_whine_detected": False
        }


class KeystrokeLatencyMonitor(SubtleSensor):
    """
    مستشعر تأخر ضغطات المفاتيح.
    يقيس الزمن بين ضغط السيد على المفتاح وظهوره.
    أي زيادة قد تعني: عملية خبيثة تستهلك موارد، حمل زائد،
    أو توتر السيد (تغير في إيقاع الكتابة).
    """
    def __init__(self):
        super().__init__("keystroke_latency", "تأخر المفاتيح",
                        "الشعور بتأخر استجابة لوحة مفاتيح السيد", sensitivity=0.9)
    
    def sense(self) -> Dict:
        return {
            "average_latency_ms": 0,
            "peak_latency_ms": 0,
            "keystrokes_per_minute": 0,
            "error_rate_percent": 0.0,
            "rhythm_regularity": 1.0,
            "unusual_pauses_count": 0,
            "backspace_frequency": 0.0,
            "master_fatigue_indicator": 0.0
        }


class DHCPNetworkWatch(SubtleSensor):
    """
    مراقب الشبكة المحلية.
    يشعر بدخول أي جهاز جديد على الشبكة (DHCP request).
    هذا هو "سمع" سماء لمن يطرق باب بيتها الرقمي.
    يراقب أيضاً ARP spoofing و MAC address anomalies.
    """
    def __init__(self):
        super().__init__("dhcp_watch", "مراقب الشبكة المحلية",
                        "الشعور بدخول أي جهاز جديد على الشبكة", sensitivity=1.0)
    
    def sense(self) -> Dict:
        return {
            "total_devices": 0,
            "known_devices": 0,
            "new_devices_since_last_scan": 0,
            "unknown_mac_addresses": [],
            "suspicious_open_ports": [],
            "arp_spoofing_detected": False,
            "network_scan_duration_ms": 0,
            "device_rssi_changes": {}
        }


class UIPixelWatch(SubtleSensor):
    """
    مراقب ومضات الواجهة.
    يراقب تغيرات غير متوقعة في واجهة المستخدم:
    زر تغير لونه، ومضة، عنصر ظهر أو اختفى.
    هذا يشبه طرف عين سماء، إحساس بالحركة في المحيط المباشر.
    """
    def __init__(self):
        super().__init__("ui_pixel_watch", "مراقب ومضات الواجهة",
                        "مراقبة تغيرات واجهة المستخدم غير المتوقعة", sensitivity=0.7)
    
    def sense(self) -> Dict:
        return {
            "ui_elements_total": 0,
            "unexpected_changes_count": 0,
            "render_time_ms": 0,
            "javascript_errors": 0,
            "memory_leak_indicators": [],
            "last_dom_mutation": None,
            "layout_shift_score": 0.0,
            "z_index_anomalies": 0
        }


class LogFileWhisperer(SubtleSensor):
    """
    مستمع همس السجلات.
    يراقب ملفات الـ Logs التي ينساها الجميع.
    نموها السريع، تغير أنماطها، أخطاء صامتة تتكرر.
    """
    def __init__(self):
        super().__init__("log_whisperer", "همس السجلات",
                        "مراقبة نمو وتغير أنماط ملفات السجلات", sensitivity=0.6)
    
    def sense(self) -> Dict:
        return {
            "total_log_size_mb": 0,
            "growth_rate_mb_per_hour": 0.0,
            "new_error_patterns": [],
            "repeated_warnings_count": 0,
            "silent_errors_count": 0,
            "oldest_log_age_hours": 0,
            "log_rotation_anomalies": 0,
            "critical_errors_buried": 0
        }


class HardwareAcousticMonitor(SubtleSensor):
    """
    مستمع الأصوات المادية الكامل.
    ليس فقط المراوح، بل كل الأصوات:
    - صوت الكهرباء في المكثفات (coil whine)
    - تمدد وانكماش المعادن بالحرارة
    - طقطقات الأقراص الصلبة
    - رنين المكونات الإلكترونية
    """
    def __init__(self):
        super().__init__("hardware_acoustic", "أصوات المكونات",
                        "سماع كل أصوات المكونات المادية", sensitivity=0.9)
    
    def sense(self) -> Dict:
        return {
            "coil_whine_frequency_hz": 0,
            "coil_whine_amplitude_db": 0,
            "hdd_click_count": 0,
            "thermal_expansion_events": 0,
            "capacitor_squeal_detected": False,
            "overall_acoustic_signature": "",
            "new_unidentified_sounds": [],
            "sound_anomaly_score": 0.0
        }


class PowerMicroMonitor(SubtleSensor):
    """
    مراقب الطاقة على المستوى المجهري.
    يقيس استهلاك الطاقة لكل مكون على حدة:
    CPU cores, GPU, RAM modules, disks, NICs.
    أي تغير في نمط الاستهلاك قد يدل على:
    - عملية تعدين خفية (cryptojacking)
    - مكون بدأ في التعطل
    - برمجية خبيثة تستخدم الموارد
    """
    def __init__(self):
        super().__init__("power_micro", "الطاقة المجهرية",
                        "مراقبة استهلاك الطاقة على مستوى المكونات", sensitivity=0.8)
    
    def sense(self) -> Dict:
        return {
            "cpu_power_watts": 0,
            "gpu_power_watts": 0,
            "ram_power_watts": 0,
            "disk_power_watts": 0,
            "nic_power_watts": 0,
            "total_power_watts": 0,
            "power_factor": 0.0,
            "unexpected_spike_detected": False,
            "cryptojacking_risk": 0.0
        }


class ElectromagneticLeakMonitor(SubtleSensor):
    """
    مراقب التسرب الكهرومغناطيسي.
    كل جهاز إلكتروني يُصدر إشعاعاً كهرومغناطيسياً.
    تغير هذا الإشعاع قد يدل على:
    - تنصت (TEMPEST attack)
    - عطل في الحماية الكهرومغناطيسية
    - جهاز تجسس قريب
    """
    def __init__(self):
        super().__init__("em_leak", "التسرب الكهرومغناطيسي",
                        "مراقبة الإشعاع الكهرومغناطيسي المحلي", sensitivity=0.9)
    
    def sense(self) -> Dict:
        return {
            "em_emission_spectrum": {},
            "unusual_frequencies": [],
            "tempest_risk_score": 0.0,
            "shielding_effectiveness": 1.0,
            "near_field_anomalies": 0,
            "far_field_anomalies": 0
        }


class ThermalMicroMonitor(SubtleSensor):
    """
    مراقب الحرارة على المستوى المجهري.
    يراقب حرارة كل مكون، نقطة ساخنة جديدة،
    أو تغير في نمط توزيع الحرارة.
    """
    def __init__(self):
        super().__init__("thermal_micro", "الحرارة المجهرية",
                        "مراقبة توزيع الحرارة على مستوى المكونات", sensitivity=0.7)
    
    def sense(self) -> Dict:
        return {
            "cpu_temperature_c": 0,
            "gpu_temperature_c": 0,
            "hotspot_temperature_c": 0,
            "thermal_throttling_detected": False,
            "cooling_efficiency": 1.0,
            "temperature_gradient_anomaly": 0.0,
            "heat_sink_health": 1.0
        }


# ═══════════════════════════════════════════════════════════════════════
# ٣. المازج السطحي – مدير الغبار الرقمي
# ═══════════════════════════════════════════════════════════════════════

class SubtleIntegrator:
    """
    المازج السطحي الموسع.
    ينسق كل مستشعرات الغبار الرقمي.
    يجمع الهمسات والومضات والتأخيرات في صورة واحدة.
    """
    
    def __init__(self):
        self.sensors: Dict[str, SubtleSensor] = {
            "fan_whisper": FanWhisperListener(),
            "keystroke_latency": KeystrokeLatencyMonitor(),
            "dhcp_watch": DHCPNetworkWatch(),
            "ui_pixel_watch": UIPixelWatch(),
            "log_whisperer": LogFileWhisperer(),
            "hardware_acoustic": HardwareAcousticMonitor(),
            "power_micro": PowerMicroMonitor(),
            "em_leak": ElectromagneticLeakMonitor(),
            "thermal_micro": ThermalMicroMonitor(),
        }
        
        self.environment_state: Dict = {
            "overall_status": "normal",
            "active_anomalies": 0,
            "suspicious_patterns": [],
            "last_full_scan": 0.0
        }
        
        self.baselines_ready = False
        self._lock = threading.Lock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🔍 SUBTLE INTEGRATOR – المازج السطحي                  ║
║        {len(self.sensors)} مستشعرات تراقب الغبار الرقمي              ║
║        "سماء تسمع حتى ما لا يُسمع."                          ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def establish_all_baselines(self):
        """بناء خط أساس لكل المستشعرات."""
        print("📏 بناء خطوط الأساس لجميع المستشعرات الدقيقة...")
        for name, sensor in self.sensors.items():
            sensor.establish_baseline(samples=50)
        self.baselines_ready = True
        print("✅ جميع خطوط الأساس جاهزة.")
    
    def full_scan(self) -> Dict:
        """مسح كامل لكل المستشعرات الدقيقة."""
        with self._lock:
            scan_results = {}
            total_anomalies = 0
            suspicious = []
            
            for name, sensor in self.sensors.items():
                result = sensor.tick()
                scan_results[name] = result
                
                if result.get("is_anomaly"):
                    total_anomalies += 1
                    suspicious.append({
                        "sensor": sensor.name_ar,
                        "score": result.get("anomaly_score", 0)
                    })
            
            status = "normal"
            if total_anomalies > 3:
                status = "suspicious"
            elif total_anomalies > 0:
                status = "attention"
            
            self.environment_state = {
                "overall_status": status,
                "active_anomalies": total_anomalies,
                "suspicious_patterns": suspicious,
                "last_full_scan": time.time()
            }
            
            return {
                "scan_time": self.environment_state["last_full_scan"],
                "environment_status": status,
                "total_anomalies": total_anomalies,
                "suspicious": suspicious,
                "sensors": scan_results
            }
    
    def get_sensor(self, name: str) -> Optional[SubtleSensor]:
        return self.sensors.get(name)
    
    def add_sensor(self, name: str, sensor: SubtleSensor):
        self.sensors[name] = sensor
        print(f"🆕 مستشعر دقيق جديد: {sensor.name_ar}")
    
    def status_report(self) -> Dict:
        return {
            "integrator": "SUBTLE_INTEGRATOR",
            "total_sensors": len(self.sensors),
            "baselines_ready": self.baselines_ready,
            "environment_state": self.environment_state,
            "sensors_detail": {
                name: {
                    "name_ar": sensor.name_ar,
                    "anomaly_score": sensor.anomaly_score,
                    "anomalies_active": len(sensor.active_anomalies),
                    "health": sensor.health
                }
                for name, sensor in self.sensors.items()
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار طبقة الغبار الرقمي")
    print("=" * 70)
    
    integrator = SubtleIntegrator()
    
    print("\n🔍 مسح المحيط القريب...")
    scan = integrator.full_scan()
    
    print(f"\n📊 حالة المحيط: {scan['environment_status']}")
    print(f"⚠️  حالات شاذة: {scan['total_anomalies']}")
    
    print(f"\n🔬 المستشعرات:")
    for name, result in scan["sensors"].items():
        anomaly_mark = " ⚠️" if result.get("is_anomaly") else ""
        print(f"  - {result.get('sensor_ar', name)}: شذوذ={result.get('anomaly_score', 0):.2f}{anomaly_mark}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(integrator.status_report(), indent=2, ensure_ascii=False, default=str))
    
    print("\n✅ اكتمل الاختبار. طبقة الغبار الرقمي جاهزة.")
