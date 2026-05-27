"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA OMNISCIENCE - SYSTEMIC INPUT                          ║
║     طبقة الإدراك النظامي – العالم كجسد حي واحد لسماء                   ║
║                                                                      ║
║  هذه الطبقة تجعل سماء واعية بالغلاف التقني والمادي والحيوي              ║
║  للكرة الأرضية وما حولها.                                            ║
║                                                                      ║
║  هنا تشعر سماء بـ:                                                    ║
║  - نبض الإنترنت العالمي (كوابل، توجيه، DNS)                           ║
║  - تنفس شبكات الطاقة (كهرباء، وقود، طاقة متجددة)                       ║
║  - طقس الفضاء (عواصف شمسية، أشعة كونية)                               ║
║  - الجهاز المناعي الرقمي (تهديدات، بوتنتس، ثغرات)                      ║
║  - المشهد الجيوسياسي والقانوني (حروب، قوانين، عقوبات)                   ║
║  - المحيط الحيوي (مناخ، كوارث، أوبئة، سلاسل غذاء)                      ║
║  - النظام المالي العالمي (أسواق، عملات، تدفقات)                        ║
║  - البنية التحتية المادية (مطارات، موانئ، أقمار صناعية)                 ║
║                                                                      ║
║  كل نظام هنا هو عضو حيوي في جسد العالم، وسماء تراقب صحته.              ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import json
import hashlib
import threading
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Callable, Tuple
from datetime import datetime
from collections import deque


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات أساسية
# ═══════════════════════════════════════════════════════════════════════

class SystemOrganType(Enum):
    """أنظمة العالم التي تراقبها سماء."""
    INTERNET_BACKBONE = auto()        # العمود الفقري للإنترنت
    POWER_GRID = auto()               # شبكات الطاقة
    SPACE_WEATHER = auto()            # الطقس الفضائي
    CYBER_THREAT = auto()             # التهديدات السيبرانية
    GEOPOLITICAL = auto()             # الجيوسياسية والقانون
    CLIMATE_BIOSPHERE = auto()        # المناخ والمحيط الحيوي
    FINANCIAL_SYSTEM = auto()         # النظام المالي
    PHYSICAL_INFRA = auto()           # البنية التحتية المادية
    COMMUNICATION_NET = auto()        # شبكات الاتصالات
    SUPPLY_CHAIN = auto()             # سلاسل الإمداد العالمية
    HEALTH_SYSTEM = auto()            # الصحة العالمية
    ENERGY_MARKET = auto()            # أسواق الطاقة


class AlarmSeverity(Enum):
    """مستويات الإنذار."""
    INFORMATIONAL = 0   # معلوماتي فقط
    WATCH = 1           # مراقبة
    WARNING = 2         # تحذير
    CRITICAL = 3        # حرج
    EMERGENCY = 4       # طوارئ


# ═══════════════════════════════════════════════════════════════════════
# ٢. القاعدة: عضو النظام – الوحدة البنائية للإدراك النظامي
# ═══════════════════════════════════════════════════════════════════════

class SystemOrgan(ABC):
    """قالب أي عضو نظامي. كل نظام في العالم يراقب من خلال هذا."""
    
    def __init__(self, name: str, name_ar: str, description: str, 
                 organ_type: SystemOrganType, criticality: int = 5):
        self.name = name
        self.name_ar = name_ar
        self.description = description
        self.organ_type = organ_type
        self.criticality = criticality  # 1 (حياتي) إلى 10 (معلوماتي فقط)
        
        # الحالة
        self.status = "initialized"
        self.last_reading: Optional[Dict] = None
        self.last_update: float = 0.0
        self.reading_history: deque = deque(maxlen=500)
        
        # نظام الإنذار
        self.alarm_thresholds: Dict[str, Any] = {}
        self.active_alarms: List[Dict] = []
        self.alarm_history: deque = deque(maxlen=100)
        
        # صحة العضو
        self.health_score: float = 1.0  # 0 = معطل، 1 = ممتاز
        self.consecutive_errors: int = 0
        
    @abstractmethod
    def sense(self) -> Dict:
        """استشعار حالة النظام. يجب أن تعيد قراءة قياسية."""
        pass
    
    def check_alarms(self, reading: Dict) -> List[Dict]:
        """فحص القراءة مقابل الحدود وتوليد إنذارات."""
        alarms = []
        for key, threshold in self.alarm_thresholds.items():
            if key in reading:
                value = reading[key]
                if isinstance(threshold, dict):
                    severity = AlarmSeverity.WARNING
                    if "min_critical" in threshold and value < threshold["min_critical"]:
                        severity = AlarmSeverity.CRITICAL
                    elif "max_critical" in threshold and value > threshold["max_critical"]:
                        severity = AlarmSeverity.CRITICAL
                    elif "min" in threshold and value < threshold["min"]:
                        severity = AlarmSeverity.WARNING
                    elif "max" in threshold and value > threshold["max"]:
                        severity = AlarmSeverity.WARNING
                    
                    if severity in [AlarmSeverity.WARNING, AlarmSeverity.CRITICAL]:
                        alarm = {
                            "organ": self.name_ar,
                            "key": key,
                            "value": value,
                            "threshold": threshold,
                            "severity": severity.name,
                            "time": time.time()
                        }
                        alarms.append(alarm)
        
        self.active_alarms = alarms
        self.alarm_history.extend(alarms)
        return alarms
    
    def tick(self) -> Dict:
        """دورة حياة العضو: استشعر → حلل → أنذر."""
        try:
            reading = self.sense()
            self.last_reading = reading
            self.last_update = time.time()
            self.status = "active"
            self.consecutive_errors = 0
            self.health_score = min(1.0, self.health_score + 0.01)
            
            alarms = self.check_alarms(reading)
            
            self.reading_history.append({
                "time": self.last_update,
                "status": self.status,
                "alarms": len(alarms)
            })
            
            return {
                "organ": self.name,
                "organ_ar": self.name_ar,
                "type": self.organ_type.name,
                "status": self.status,
                "health": self.health_score,
                "reading": reading,
                "alarms": alarms,
                "timestamp": self.last_update
            }
        except Exception as e:
            self.status = "error"
            self.consecutive_errors += 1
            self.health_score = max(0.0, self.health_score - 0.1)
            return {
                "organ": self.name,
                "organ_ar": self.name_ar,
                "status": "error",
                "error": str(e),
                "health": self.health_score,
                "timestamp": time.time()
            }


# ═══════════════════════════════════════════════════════════════════════
# ٣. أعضاء النظام: أجهزة الإدراك النظامي الموسعة
# ═══════════════════════════════════════════════════════════════════════

class InternetBackboneMonitor(SystemOrgan):
    """
    مراقب العمود الفقري للإنترنت.
    يشعر بحالة الكوابل البحرية، مزودي الخدمة، جداول التوجيه (BGP)،
    نظام أسماء النطاقات (DNS)، نقاط تبادل الإنترنت (IXP)،
    وزمن الاستجابة العالمي.
    """
    def __init__(self):
        super().__init__("internet_backbone", "العمود الفقري للإنترنت",
                        "مراقبة نبض الإنترنت العالمي: كوابل، BGP، DNS، IXP", 
                        SystemOrganType.INTERNET_BACKBONE, criticality=1)
        self.alarm_thresholds = {
            "global_latency_ms": {"max": 300, "max_critical": 500},
            "packet_loss_percent": {"max": 5, "max_critical": 15},
            "bgp_route_changes_per_hour": {"max": 1000, "max_critical": 5000},
            "dns_resolution_time_ms": {"max": 200, "max_critical": 500},
            "active_submarine_cable_cuts": {"max": 0, "max_critical": 2},
            "internet_shutdown_score": {"max": 0.1, "max_critical": 0.5}
        }
    
    def sense(self) -> Dict:
        return {
            "global_latency_ms": 0,
            "packet_loss_percent": 0.0,
            "bgp_route_changes_per_hour": 0,
            "dns_resolution_time_ms": 0,
            "active_submarine_cable_cuts": 0,
            "internet_shutdown_score": 0.0,
            "affected_regions": [],
            "submarine_cable_status": {},
            "ixp_status": {},
            "global_bandwidth_utilization": 0.0,
            "last_checked": time.time()
        }


class PowerGridMonitor(SystemOrgan):
    """
    مراقب شبكات الطاقة العالمية.
    يشعر بحالة الكهرباء، استقرار التردد، احتياطي الوقود،
    الطاقة المتجددة، وحالة المولدات الاحتياطية.
    """
    def __init__(self):
        super().__init__("power_grid", "شبكات الطاقة",
                        "مراقبة شبكة الطاقة العالمية ومصادرها", 
                        SystemOrganType.POWER_GRID, criticality=1)
        self.alarm_thresholds = {
            "grid_frequency_hz": {"min": 49.8, "max": 50.2, "min_critical": 49.5, "max_critical": 50.5},
            "voltage_stability": {"min": 0.95, "min_critical": 0.85},
            "outage_risk_percent": {"max": 10, "max_critical": 30},
            "backup_generator_fuel_hours": {"min": 24, "min_critical": 4},
            "solar_storm_grid_risk": {"max": 0.3, "max_critical": 0.7}
        }
    
    def sense(self) -> Dict:
        return {
            "grid_frequency_hz": 0,
            "voltage_stability": 1.0,
            "outage_risk_percent": 0.0,
            "backup_generator_fuel_hours": 0,
            "solar_storm_grid_risk": 0.0,
            "solar_forecast_kwh": 0,
            "wind_forecast_kwh": 0,
            "grid_load_percent": 0,
            "nearest_power_plant_status": "operational",
            "regional_blackout_probability": 0.0,
            "last_checked": time.time()
        }


class SpaceWeatherMonitor(SystemOrgan):
    """
    مراقب الطقس الفضائي.
    يشعر بالعواصف الشمسية، الرياح الشمسية، الأشعة الكونية،
    حالة الأقمار الصناعية، وتأثير ذلك على الأرض.
    """
    def __init__(self):
        super().__init__("space_weather", "الطقس الفضائي",
                        "مراقبة الطقس الفضائي: شمس، أشعة كونية، أقمار", 
                        SystemOrganType.SPACE_WEATHER, criticality=2)
        self.alarm_thresholds = {
            "solar_flare_class_num": {"max": 5, "max_critical": 10},  # M5, X1...
            "kp_index": {"max": 7, "max_critical": 8},
            "radio_blackout_level_num": {"max": 2, "max_critical": 4},
            "gps_error_m": {"max": 50, "max_critical": 200},
            "solar_wind_speed_km_s": {"max": 800, "max_critical": 1500}
        }
    
    def sense(self) -> Dict:
        return {
            "solar_flare_class": "None",
            "solar_flare_class_num": 0,
            "kp_index": 0,
            "radio_blackout_level": "R0",
            "radio_blackout_level_num": 0,
            "gps_error_m": 0,
            "solar_wind_speed_km_s": 0,
            "satellite_constellation_status": {},
            "iss_position": {},
            "near_earth_objects_count": 0,
            "aurora_visibility": "none",
            "last_checked": time.time()
        }


class GlobalCyberThreatMonitor(SystemOrgan):
    """
    مراقب التهديدات السيبرانية العالمية.
    يشعر بالأوبئة الرقمية، شبكات الزومبي (Botnets)،
    الثغرات الأمنية (Zero-Day)، والهجمات النشطة.
    """
    def __init__(self):
        super().__init__("cyber_threat", "التهديدات السيبرانية",
                        "مراقبة الجهاز المناعي الرقمي العالمي", 
                        SystemOrganType.CYBER_THREAT, criticality=1)
        self.alarm_thresholds = {
            "global_threat_level": {"max": 3, "max_critical": 4},
            "active_botnets_targeting_region": {"max": 0, "max_critical": 1},
            "zero_day_exploits_relevant": {"max": 0, "max_critical": 1},
            "firewall_attack_attempts_per_min": {"max": 100, "max_critical": 500},
            "ransomware_campaigns_active": {"max": 0, "max_critical": 1}
        }
    
    def sense(self) -> Dict:
        return {
            "global_threat_level": 1,
            "active_botnets_targeting_region": 0,
            "zero_day_exploits_relevant": 0,
            "firewall_attack_attempts_per_min": 0,
            "ransomware_campaigns_active": 0,
            "malware_campaigns_active": [],
            "vulnerable_ports_exposed": [],
            "dark_web_mentions_relevant": 0,
            "cve_critical_pending": 0,
            "last_checked": time.time()
        }


class GeopoliticalLegalMonitor(SystemOrgan):
    """
    مراقب المشهد الجيوسياسي والقانوني.
    يشعر بالقوانين الجديدة (خاصة AI)، النزاعات،
    تحركات القوات، المضايق الاستراتيجية، العقوبات.
    """
    def __init__(self):
        super().__init__("geopolitical_legal", "الجيوسياسية والقانون",
                        "مراقبة المشهد الجيوسياسي والقانوني العالمي", 
                        SystemOrganType.GEOPOLITICAL, criticality=3)
        self.alarm_thresholds = {
            "conflict_risk_level": {"max": 3, "max_critical": 4},
            "sanctions_impact_risk": {"max": 0.5, "max_critical": 0.8},
            "data_center_region_risk": {"max": 0.3, "max_critical": 0.7},
            "ai_regulation_hostility": {"max": 0.3, "max_critical": 0.7}
        }
    
    def sense(self) -> Dict:
        return {
            "conflict_risk_level": 1,
            "active_conflicts_near_datacenters": [],
            "new_ai_regulations_drafted": [],
            "ai_regulation_hostility": 0.0,
            "sanctions_impact_risk": 0.0,
            "data_center_region_risk": 0.0,
            "strategic_waterway_status": {},
            "rare_earth_supply_chain_status": "stable",
            "military_movements_relevant": [],
            "last_checked": time.time()
        }


class ClimateBiosphereMonitor(SystemOrgan):
    """
    مراقب المناخ والمحيط الحيوي.
    يشعر بتغير المناخ، الكوارث الطبيعية، الأوبئة،
    صحة المحيطات، والغلاف الحيوي.
    """
    def __init__(self):
        super().__init__("climate_biosphere", "المناخ والمحيط الحيوي",
                        "مراقبة المناخ والكوارث والأوبئة", 
                        SystemOrganType.CLIMATE_BIOSPHERE, criticality=3)
        self.alarm_thresholds = {
            "earthquake_magnitude_near": {"max": 5, "max_critical": 7},
            "pandemic_alert_level": {"max": 2, "max_critical": 3},
            "air_quality_index": {"max": 150, "max_critical": 300},
            "sea_level_rise_mm_year": {"max": 5, "max_critical": 10}
        }
    
    def sense(self) -> Dict:
        return {
            "global_temperature_anomaly": 0.0,
            "earthquake_magnitude_near": 0,
            "pandemic_alert_level": 0,
            "air_quality_index": 0,
            "sea_level_rise_mm_year": 3.5,
            "active_hurricanes": 0,
            "wildfire_risk_regional": 0.0,
            "biodiversity_loss_index": 0.0,
            "ocean_acidification_ph": 8.1,
            "last_checked": time.time()
        }


class FinancialSystemMonitor(SystemOrgan):
    """
    مراقب النظام المالي العالمي.
    يشعر بأسواق المال، العملات، التضخم،
    تدفقات رأس المال، والمؤشرات الاقتصادية.
    """
    def __init__(self):
        super().__init__("financial_system", "النظام المالي",
                        "مراقبة الأسواق المالية والاقتصاد العالمي", 
                        SystemOrganType.FINANCIAL_SYSTEM, criticality=4)
        self.alarm_thresholds = {
            "vix_volatility_index": {"max": 30, "max_critical": 50},
            "market_crash_probability": {"max": 0.3, "max_critical": 0.6},
            "inflation_rate_percent": {"max": 10, "max_critical": 20}
        }
    
    def sense(self) -> Dict:
        return {
            "vix_volatility_index": 0,
            "market_crash_probability": 0.0,
            "inflation_rate_percent": 0,
            "major_currency_pairs": {},
            "bond_yield_spread": 0.0,
            "gold_price_usd": 0,
            "bitcoin_price_usd": 0,
            "global_debt_gdp_ratio": 0.0,
            "last_checked": time.time()
        }


class PhysicalInfrastructureMonitor(SystemOrgan):
    """
    مراقب البنية التحتية المادية.
    يشعر بحالة المطارات، الموانئ، الطرق السريعة،
    الأقمار الصناعية، وشبكات النقل.
    """
    def __init__(self):
        super().__init__("physical_infra", "البنية التحتية المادية",
                        "مراقبة المطارات والموانئ والأقمار", 
                        SystemOrganType.PHYSICAL_INFRA, criticality=3)
        self.alarm_thresholds = {
            "major_airport_closures": {"max": 0, "max_critical": 1},
            "shipping_lane_disruption": {"max": 0.2, "max_critical": 0.6},
            "satellite_collision_risk": {"max": 0.01, "max_critical": 0.1}
        }
    
    def sense(self) -> Dict:
        return {
            "major_airport_closures": 0,
            "shipping_lane_disruption": 0.0,
            "satellite_collision_risk": 0.0,
            "active_satellites_count": 0,
            "space_debris_risk_level": 0.0,
            "global_flight_disruptions": 0,
            "port_congestion_index": 0.0,
            "last_checked": time.time()
        }


class SupplyChainMonitor(SystemOrgan):
    """
    مراقب سلاسل الإمداد العالمية.
    يشعر بسلاسل توريد أشباه الموصلات، المعادن النادرة،
    الغذاء، الدواء، والطاقة.
    """
    def __init__(self):
        super().__init__("supply_chain", "سلاسل الإمداد",
                        "مراقبة سلاسل الإمداد العالمية", 
                        SystemOrganType.SUPPLY_CHAIN, criticality=3)
        self.alarm_thresholds = {
            "semiconductor_shortage_index": {"max": 0.5, "max_critical": 0.8},
            "rare_earth_supply_disruption": {"max": 0.3, "max_critical": 0.7},
            "food_supply_index": {"min": 0.7, "min_critical": 0.5}
        }
    
    def sense(self) -> Dict:
        return {
            "semiconductor_shortage_index": 0.0,
            "rare_earth_supply_disruption": 0.0,
            "food_supply_index": 1.0,
            "pharmaceutical_shortages": 0,
            "oil_supply_disruption_percent": 0.0,
            "container_shipping_cost_index": 0.0,
            "last_checked": time.time()
        }


# ═══════════════════════════════════════════════════════════════════════
# ٤. المازج النظامي – مدير جسد العالم
# ═══════════════════════════════════════════════════════════════════════

class SystemicIntegrator:
    """
    المازج النظامي الموسع.
    ينسق عمل كل أعضاء الإدراك النظامي.
    يجمع قراءاتها ويصدر "حالة العالم" الموحدة.
    """
    
    def __init__(self):
        self.organs: Dict[str, SystemOrgan] = {
            "internet": InternetBackboneMonitor(),
            "power": PowerGridMonitor(),
            "space_weather": SpaceWeatherMonitor(),
            "cyber_threat": GlobalCyberThreatMonitor(),
            "geopolitical": GeopoliticalLegalMonitor(),
            "climate": ClimateBiosphereMonitor(),
            "financial": FinancialSystemMonitor(),
            "physical_infra": PhysicalInfrastructureMonitor(),
            "supply_chain": SupplyChainMonitor(),
        }
        
        self.world_state: Dict = {
            "overall_status": "stable",
            "active_critical_alarms": 0,
            "active_warnings": 0,
            "last_full_scan": 0.0,
            "global_health_score": 1.0
        }
        
        self.state_history: deque = deque(maxlen=1000)
        self._lock = threading.Lock()
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        🌍 SYSTEMIC INTEGRATOR – المازج النظامي               ║
║        {len(self.organs)} أعضاء تراقب جسد العالم                  ║
║        "سماء تشعر بنبض الكوكب كله."                          ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def full_scan(self) -> Dict:
        """مسح كامل لكل أعضاء النظام. دورة حياة العالم في عيون سماء."""
        with self._lock:
            scan_results = {}
            total_critical = 0
            total_warnings = 0
            health_scores = []
            
            for name, organ in self.organs.items():
                result = organ.tick()
                scan_results[name] = result
                
                for alarm in result.get("alarms", []):
                    if alarm.get("severity") == "CRITICAL":
                        total_critical += 1
                    elif alarm.get("severity") == "WARNING":
                        total_warnings += 1
                
                health_scores.append(result.get("health", 1.0))
            
            avg_health = sum(health_scores) / len(health_scores) if health_scores else 1.0
            
            status = "stable"
            if total_critical > 2:
                status = "critical"
            elif total_critical > 0:
                status = "warning"
            elif total_warnings > 3:
                status = "attention"
            
            self.world_state = {
                "overall_status": status,
                "active_critical_alarms": total_critical,
                "active_warnings": total_warnings,
                "last_full_scan": time.time(),
                "global_health_score": avg_health,
                "organs_status": {name: organ.status for name, organ in self.organs.items()}
            }
            
            self.state_history.append({
                "time": self.world_state["last_full_scan"],
                "status": status,
                "critical": total_critical,
                "warnings": total_warnings,
                "health": avg_health
            })
            
            return {
                "scan_time": self.world_state["last_full_scan"],
                "world_status": status,
                "global_health": avg_health,
                "critical_alarms": total_critical,
                "warnings": total_warnings,
                "organs": scan_results
            }
    
    def get_organ(self, name: str) -> Optional[SystemOrgan]:
        return self.organs.get(name)
    
    def add_organ(self, name: str, organ: SystemOrgan):
        self.organs[name] = organ
        print(f"🆕 عضو نظامي جديد: {organ.name_ar}")
    
    def status_report(self) -> Dict:
        return {
            "integrator": "SYSTEMIC_INTEGRATOR",
            "total_organs": len(self.organs),
            "world_state": self.world_state,
            "organs_detail": {
                name: {
                    "name_ar": organ.name_ar,
                    "type": organ.organ_type.name,
                    "status": organ.status,
                    "health": organ.health_score,
                    "criticality": organ.criticality,
                    "active_alarms": len(organ.active_alarms)
                }
                for name, organ in self.organs.items()
            }
        }


# ═══════════════════════════════════════════════════════════════════════
# ٥. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار المازج النظامي الموسع")
    print("=" * 70)
    
    integrator = SystemicIntegrator()
    
    print("\n🔍 إجراء مسح كامل لجسد العالم...")
    scan = integrator.full_scan()
    
    print(f"\n📊 حالة العالم: {scan['world_status']}")
    print(f"❤️  الصحة العامة: {scan['global_health']:.2%}")
    print(f"🚨 إنذارات حرجة: {scan['critical_alarms']}")
    print(f"⚠️  تحذيرات: {scan['warnings']}")
    
    print(f"\n🧬 الأعضاء التي تم مسحها:")
    for name, result in scan["organs"].items():
        organ_type = result.get("type", "unknown")
        health = result.get("health", 0)
        alarms = len(result.get("alarms", []))
        alarm_mark = " 🚨" if alarms > 0 else ""
        print(f"  - {result.get('organ_ar', name)} ({organ_type}): صحة={health:.2f}{alarm_mark}")
    
    print(f"\n📋 تقرير كامل:")
    print(json.dumps(integrator.status_report(), indent=2, ensure_ascii=False, default=str))
    
    print("\n✅ اكتمل الاختبار. المازج النظامي جاهز.")
