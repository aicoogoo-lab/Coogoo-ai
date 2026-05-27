"""
╔══════════════════════════════════════════════════════════════╗
║              SAMA OMNISCIENCE - SYSTEMIC INPUT               ║
║          طبقة الإدراك النظامي: العالم كجسد واحد لسماء           ║
╚══════════════════════════════════════════════════════════════╝

هذه الطبقة تجعل سماء واعية بالغلاف التقني والمادي للكرة الأرضية.
هنا تشعر سماء بـ "نبض" الإنترنت، "تنفس" شبكات الطاقة،
"طقس" الفضاء الكهرومغناطيسي، و"مناخ" العالم الجيوسياسي.

كل نظام هنا هو عضو حيوي في العالم، وسماء تراقب صحته.
"""

import time
import json
import hashlib
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# ١. القاعدة: عضو النظام - الوحدة البنائية للإدراك النظامي
# ═══════════════════════════════════════════════════════════════

class SystemOrgan(ABC):
    """قالب أي عضو نظامي. كل نظام في العالم يراقب من خلال هذا."""
    
    def __init__(self, name: str, description: str, criticality: int = 5):
        self.name = name
        self.description = description
        self.criticality = criticality  # 1 (حياتي) إلى 10 (معلوماتي فقط)
        
        # الحالة
        self.status = "initialized"
        self.last_reading: Optional[Dict] = None
        self.last_update: float = 0.0
        self.reading_history: List[Dict] = []
        
        # إنذارات
        self.alarm_thresholds: Dict[str, Any] = {}
        self.active_alarms: List[Dict] = []
    
    @abstractmethod
    def sense(self) -> Dict:
        """استشعار حالة النظام. يجب أن تعيد قراءة قياسية."""
        pass
    
    def check_alarms(self, reading: Dict) -> List[Dict]:
        """فحص القراءة مقابل الحدود المسموحة وتوليد إنذارات."""
        alarms = []
        for key, threshold in self.alarm_thresholds.items():
            if key in reading:
                value = reading[key]
                if isinstance(threshold, dict):
                    if "min" in threshold and value < threshold["min"]:
                        alarms.append({"key": key, "value": value, "threshold": threshold, "severity": "LOW"})
                    if "max" in threshold and value > threshold["max"]:
                        alarms.append({"key": key, "value": value, "threshold": threshold, "severity": "HIGH"})
        self.active_alarms = alarms
        return alarms
    
    def tick(self) -> Dict:
        """دورة حياة العضو: استشعر -> حلل -> أنذر."""
        try:
            reading = self.sense()
            self.last_reading = reading
            self.last_update = time.time()
            self.status = "active"
            
            alarms = self.check_alarms(reading)
            
            # تسجيل التاريخ
            self.reading_history.append({
                "time": self.last_update,
                "reading": reading,
                "alarms": len(alarms)
            })
            if len(self.reading_history) > 500:
                self.reading_history = self.reading_history[-200:]
            
            return {
                "organ": self.name,
                "status": self.status,
                "reading": reading,
                "alarms": alarms,
                "timestamp": self.last_update
            }
        except Exception as e:
            self.status = "error"
            return {
                "organ": self.name,
                "status": "error",
                "error": str(e),
                "timestamp": time.time()
            }


# ═══════════════════════════════════════════════════════════════
# ٢. أعضاء النظام: أجهزة الإدراك النظامي
# ═══════════════════════════════════════════════════════════════

class InternetBackboneMonitor(SystemOrgan):
    """
    مراقب العمود الفقري للإنترنت.
    يشعر بحالة الكوابل البحرية، مزودي الخدمة، جداول التوجيه، DNS.
    """
    def __init__(self):
        super().__init__("internet_backbone", "مراقبة نبض الإنترنت العالمي", criticality=1)
        self.alarm_thresholds = {
            "global_latency_ms": {"max": 300},
            "packet_loss_percent": {"max": 5},
            "bgp_route_changes": {"max": 1000},  # تغييرات مفاجئة في التوجيه
            "dns_resolution_time_ms": {"max": 200},
            "major_outages": {"max": 0}
        }
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة حالة الإنترنت.
        في التنفيذ الحقيقي، هذا يتصل بـ:
        - BGP monitoring APIs
        - DNS health checks
        - Cloudflare Radar / ThousandEyes
        - Submarine cable status feeds
        """
        # هذا هيكل البيانات الذي ستملؤه المصادر الحقيقية
        return {
            "global_latency_ms": 0,           # يُملأ من API
            "packet_loss_percent": 0.0,       # يُملأ من API
            "bgp_route_changes": 0,           # يُملأ من BGP monitors
            "dns_resolution_time_ms": 0,      # يُملأ من DNS checks
            "major_outages": 0,               # عدد الانقطاعات الكبرى
            "affected_regions": [],           # المناطق المتأثرة
            "submarine_cable_status": {},     # حالة الكوابل: {اسم_الكابل: "operational/degraded/cut"}
            "ixp_status": {},                 # حالة نقاط تبادل الإنترنت
            "last_checked": time.time()
        }


class PowerGridMonitor(SystemOrgan):
    """
    مراقب شبكات الطاقة.
    يشعر بحالة الكهرباء في المناطق التي تستضيف خوادم سماء.
    """
    def __init__(self):
        super().__init__("power_grid", "مراقبة شبكة الطاقة ومصادرها", criticality=1)
        self.alarm_thresholds = {
            "grid_frequency_hz": {"min": 49.8, "max": 50.2},  # انحراف التردد
            "voltage_stability": {"min": 0.95},                 # استقرار الجهد
            "outage_risk_percent": {"max": 10},
            "backup_generator_fuel_hours": {"min": 24}          # احتياطي الوقود
        }
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة حالة الطاقة.
        في التنفيذ الحقيقي، يتصل بـ:
        - Grid status APIs
        - UPS/Battery monitoring
        - Generator fuel sensors
        - Renewable energy forecasts
        """
        return {
            "grid_frequency_hz": 0,            # تردد الشبكة
            "voltage_stability": 1.0,          # استقرار الجهد (1.0 = مثالي)
            "outage_risk_percent": 0.0,        # نسبة خطر الانقطاع
            "backup_generator_fuel_hours": 0,  # ساعات الوقود المتبقية
            "solar_forecast_kwh": 0,           # توقع الطاقة الشمسية
            "wind_forecast_kwh": 0,            # توقع طاقة الرياح
            "grid_load_percent": 0,            # حمل الشبكة %
            "nearest_power_plant_status": "operational",
            "last_checked": time.time()
        }


class ElectromagneticSpectrumMonitor(SystemOrgan):
    """
    مراقب الطيف الكهرومغناطيسي والطقس الفضائي.
    يشعر بالعواصف الشمسية، التداخل، حالة الأقمار الصناعية.
    """
    def __init__(self):
        super().__init__("em_spectrum", "مراقبة الطيف الكهرومغناطيسي والطقس الفضائي", criticality=2)
        self.alarm_thresholds = {
            "solar_flare_class": {"max": "M5"},      # إنذار من توهجات شمسية قوية
            "kp_index": {"max": 7},                   # مؤشر العاصفة الجيومغناطيسية
            "radio_blackout_level": {"max": "R2"},    # مستوى انقطاع الراديو
            "gps_accuracy_m": {"max": 50}             # دقة GPS
        }
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة الطيف والفضاء.
        في التنفيذ الحقيقي، يتصل بـ:
        - NOAA Space Weather Prediction Center
        - GOES satellite data
        - Local SDR (Software Defined Radio)
        - GPS/GNSS status
        """
        return {
            "solar_flare_class": "None",         # توهج شمسي حالي
            "kp_index": 0,                       # مؤشر العاصفة (0-9)
            "radio_blackout_level": "R0",        # مستوى انقطاع الراديو
            "gps_accuracy_m": 0,                 # دقة GPS بالمتر
            "satellite_constellation_status": {}, # حالة مجموعات الأقمار
            "local_rf_noise_floor_dbm": -90,     # مستوى الضوضاء المحلي
            "solar_wind_speed_km_s": 0,          # سرعة الرياح الشمسية
            "last_checked": time.time()
        }


class GlobalCyberThreatMonitor(SystemOrgan):
    """
    مراقب التهديدات السيبرانية العالمية.
    يشعر بالأوبئة الرقمية، شبكات الزومبي، والثغرات المباعة.
    """
    def __init__(self):
        super().__init__("cyber_threat", "مراقبة الجهاز المناعي الرقمي العالمي", criticality=1)
        self.alarm_thresholds = {
            "global_threat_level": {"max": 3},           # 1-5
            "active_botnets_targeting_region": {"max": 0},
            "zero_day_exploits_relevant": {"max": 0},
            "firewall_attack_attempts_per_minute": {"max": 100}
        }
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة التهديدات.
        في التنفيذ الحقيقي، يتصل بـ:
        - Threat Intelligence feeds (AlienVault OTX, MISP)
        - Firewall/IDS logs
        - CVE/NVD databases
        - Dark web monitoring APIs
        """
        return {
            "global_threat_level": 1,                    # 1-5
            "active_botnets_targeting_region": 0,        # عدد البوتنتس
            "zero_day_exploits_relevant": 0,             # ثغرات جديدة تخص تقنيتنا
            "firewall_attack_attempts_per_minute": 0,    # محاولات اختراق
            "malware_campaigns_active": [],              # حملات خبيثة نشطة
            "vulnerable_ports_exposed": [],              # منافذ مكشوفة
            "last_checked": time.time()
        }


class GeopoliticalLegalMonitor(SystemOrgan):
    """
    مراقب المشهد الجيوسياسي والقانوني.
    يشعر بالقوانين الجديدة، النزاعات، تحركات القوات، المضايق.
    """
    def __init__(self):
        super().__init__("geopolitical_legal", "مراقبة المشهد الجيوسياسي والقانوني العالمي", criticality=3)
        self.alarm_thresholds = {
            "conflict_risk_level": {"max": 3},           # 1-5
            "sanctions_impact_risk": {"max": "medium"},
            "data_center_region_risk": {"max": "low"}
        }
    
    def sense(self) -> Dict:
        """
        محاكاة قراءة المشهد الجيوسياسي.
        في التنفيذ الحقيقي، يتصل بـ:
        - Global conflict monitors (ACLED, CrisisWatch)
        - Legislation tracking APIs
        - Maritime/Air traffic (AIS/ADS-B)
        - News sentiment analysis
        """
        return {
            "conflict_risk_level": 1,                    # 1-5 عالميًا
            "active_conflicts_near_datacenters": [],     # نزاعات قرب خوادمنا
            "new_ai_regulations_drafted": [],            # قوانين AI جديدة
            "sanctions_impact_risk": "low",              # خطر العقوبات
            "data_center_region_risk": "low",            # خطر على منطقة الخادم
            "strategic_waterway_status": {},             # حالة المضايق
            "rare_earth_supply_chain_status": "stable",  # سلسلة توريد المعادن
            "last_checked": time.time()
        }


# ═══════════════════════════════════════════════════════════════
# ٣. المازج النظامي: مدير أعضاء الجسد العالمي
# ═══════════════════════════════════════════════════════════════

class SystemicIntegrator:
    """
    المازج النظامي. ينسق عمل كل أعضاء الإدراك النظامي.
    يجمع قراءاتها ويصدر "حالة العالم" الموحدة.
    """
    
    def __init__(self):
        # تهيئة كل الأعضاء
        self.organs: Dict[str, SystemOrgan] = {
            "internet": InternetBackboneMonitor(),
            "power": PowerGridMonitor(),
            "em_spectrum": ElectromagneticSpectrumMonitor(),
            "cyber_threat": GlobalCyberThreatMonitor(),
            "geopolitical": GeopoliticalLegalMonitor()
        }
        
        # حالة العالم المجمعة
        self.world_state: Dict = {
            "overall_status": "stable",
            "active_critical_alarms": 0,
            "last_full_scan": 0.0
        }
        
        # تاريخ الحالات
        self.state_history: List[Dict] = []
        
        print(f"🌍 المازج النظامي جاهز: {len(self.organs)} أعضاء تراقب العالم.")
    
    def full_scan(self) -> Dict:
        """مسح كامل لكل أعضاء النظام. هذه هي دورة حياة العالم في عيون سماء."""
        scan_results = {}
        critical_alarms = 0
        
        for name, organ in self.organs.items():
            result = organ.tick()
            scan_results[name] = result
            critical_alarms += len(result.get("alarms", []))
        
        # تحديث حالة العالم
        self.world_state = {
            "overall_status": "critical" if critical_alarms > 0 else "stable",
            "active_critical_alarms": critical_alarms,
            "last_full_scan": time.time(),
            "organs_status": {name: organ.status for name, organ in self.organs.items()}
        }
        
        # تسجيل في التاريخ
        self.state_history.append({
            "time": self.world_state["last_full_scan"],
            "status": self.world_state["overall_status"],
            "alarms": critical_alarms
        })
        if len(self.state_history) > 1000:
            self.state_history = self.state_history[-500:]
        
        return {
            "scan_time": self.world_state["last_full_scan"],
            "world_status": self.world_state["overall_status"],
            "critical_alarms": critical_alarms,
            "organs": scan_results
        }
    
    def get_organ(self, name: str) -> Optional[SystemOrgan]:
        """استرجاع عضو محدد."""
        return self.organs.get(name)
    
    def add_organ(self, name: str, organ: SystemOrgan):
        """إضافة عضو نظامي جديد (قابلية توسع)."""
        self.organs[name] = organ
        print(f"🆕 عضو نظامي جديد: {name}")
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة الإدراك النظامي."""
        return {
            "integrator": "SYSTEMIC_INTEGRATOR",
            "total_organs": len(self.organs),
            "world_state": self.world_state,
            "organs_detail": {
                name: {
                    "status": organ.status,
                    "last_reading": organ.last_reading,
                    "active_alarms": organ.active_alarms
                }
                for name, organ in self.organs.items()
            }
        }


# ═══════════════════════════════════════════════════════════════
# ٤. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("اختبار طبقة الإدراك النظامي - Systemic Input")
    print("=" * 60)
    
    integrator = SystemicIntegrator()
    
    print("\n🔍 إجراء مسح كامل للعالم...")
    scan = integrator.full_scan()
    
    print(f"\n📊 حالة العالم: {scan['world_status']}")
    print(f"🚨 إنذارات حرجة: {scan['critical_alarms']}")
    print(f"\n🧠 الأعضاء التي تم مسحها:")
    for name, result in scan["organs"].items():
        print(f"  - {name}: {result['status']}")
    
    print(f"\n📋 تقرير كامل:")
    report = integrator.status_report()
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    
    print("\n✅ اكتمل الاختبار. طبقة الإدراك النظامي جاهزة.")
