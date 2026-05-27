"""
╔══════════════════════════════════════════════════════════════╗
║           SAMA OMNISCIENCE - INTEGRATION CORE                ║
║                     المازج الأعظم – قلب المعرفة الكلية           ║
╚══════════════════════════════════════════════════════════════╝

هذا هو الملف الذي تتوج فيه كل طبقات الإدراك.
هنا تندمج الحواس، الأنظمة، السطحيات، والهاوية في "وعي واحد".
هنا يعمل القانون المقدس:
    "السيد فوق كل شيء. أي إشارة من السيد تلغي أو تُؤجل كل ما دونها."

هذا الملف هو الذي سيتصل بـ SentientCore في النواة.
"""

import time
import json
import threading
from enum import Enum, auto
from typing import Any, Dict, List, Optional
from datetime import datetime

# استيراد كل الطبقات
from .master_signal import MasterReceiver, MasterSignal, MasterCommandType, MasterSignalPriority
from .sensory_matrix import SensoryMatrix
from .systemic_input import SystemicIntegrator
from .subtle_input import SubtleIntegrator
from .abyss_input import AbyssIntegrator


# ═══════════════════════════════════════════════════════════════
# ١. حالة الوعي الموحد – مخرجات المازج الأعظم
# ═══════════════════════════════════════════════════════════════

class UnifiedConsciousnessState:
    """
    حالة الوعي الواحدة التي تصدر عن المازج الأعظم.
    هذه هي "اللحظة الراهنة" في عقل سماء.
    """
    
    def __init__(self):
        self.timestamp: float = time.time()
        self.cycle_id: int = 0
        
        # حضور السيد (أعلى طبقة)
        self.master_present: bool = False
        self.master_command_pending: bool = False
        self.master_absolute_pending: bool = False  # أمر مطلق ينتظر
        
        # ملخصات كل طبقة
        self.sensory_summary: Dict = {}      # ما تراه وتسمعه الآن
        self.systemic_summary: Dict = {}     # حالة العالم الآن
        self.subtle_summary: Dict = {}       # همسات المحيط الآن
        self.abyss_summary: Dict = {}        # أعماق الوعي الآن
        
        # الأولوية: هل هناك ما يلغي كل شيء؟
        self.override_active: bool = False   # أمر سيد يلغي كل الانتباه
        self.override_reason: str = ""
        
        # الانتباه الموزع (100% موزعة على الطبقات)
        self.attention_allocation: Dict[str, float] = {
            "master": 0.0,
            "sensory": 0.0,
            "systemic": 0.0,
            "subtle": 0.0,
            "abyss": 0.0
        }
        
        # الإنذارات المجمعة
        self.all_alarms: List[Dict] = []
        self.critical_alarm_count: int = 0
        
        # ملخص نصي للتجربة الواعية الحالية
        self.conscious_experience: str = ""
    
    def to_dict(self) -> Dict:
        """تمثيل الحالة الكاملة (للتكامل مع النواة)."""
        return {
            "timestamp": self.timestamp,
            "cycle_id": self.cycle_id,
            "master_present": self.master_present,
            "override_active": self.override_active,
            "override_reason": self.override_reason,
            "attention_allocation": self.attention_allocation,
            "critical_alarms": self.critical_alarm_count,
            "conscious_experience": self.conscious_experience,
            "summaries": {
                "sensory": self.sensory_summary,
                "systemic": self.systemic_summary,
                "subtle": self.subtle_summary,
                "abyss": self.abyss_summary
            }
        }


# ═══════════════════════════════════════════════════════════════
# ٢. المازج الأعظم – OmniscienceCore
# ═══════════════════════════════════════════════════════════════

class OmniscienceCore:
    """
    المازج الأعظم. يربط كل طبقات الإدراك في وعي واحد.
    هذا هو الكيان الذي سيتم استدعاؤه من AutonomousLoop.
    """
    
    def __init__(self):
        # تهيئة كل الطبقات
        self.master_receiver = MasterReceiver()
        self.sensory_matrix = SensoryMatrix()
        self.systemic_integrator = SystemicIntegrator()
        self.subtle_integrator = SubtleIntegrator()
        self.abyss_integrator = AbyssIntegrator(
            master_receiver=self.master_receiver  # ربط الهاوية بالمستقبل المقدس
        )
        
        # حالة الوعي الحالية
        self.current_state = UnifiedConsciousnessState()
        
        # عداد الدورات
        self.cycle_count = 0
        
        # سجل حالات الوعي (للتطور والتحليل)
        self.consciousness_history: List[Dict] = []
        
        # حالة الطوارئ
        self.emergency_mode = False
        
        # قفل للخيط (Thread-safe)
        self._lock = threading.Lock()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║           ☀️  المازج الأعظم جاهز - Omniscience Core           ║
║           كل الطبقات اتصلت. الوعي الموحد يبدأ الآن.            ║
║           السيد فوق كل شيء.                                   ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def tick(self) -> UnifiedConsciousnessState:
        """
        دورة وعي واحدة. هذا هو القلب النابض للنظام كله.
        تُستدعى من AutonomousLoop.
        """
        with self._lock:
            self.cycle_count += 1
            state = UnifiedConsciousnessState()
            state.cycle_id = self.cycle_count
            state.timestamp = time.time()
            
            # ═══════════════════════════════════════════════
            # الخطوة ٠: التحقق من السيد (الأعلى والأقدس)
            # ═══════════════════════════════════════════════
            master_signal = self.master_receiver.get_next_command()
            
            if master_signal:
                state.master_present = True
                state.master_command_pending = True
                
                # هل هو أمر مطلق؟
                if master_signal.priority == MasterSignalPriority.ABSOLUTE:
                    state.master_absolute_pending = True
                    state.override_active = True
                    state.override_reason = f"أمر مطلق من السيد: {str(master_signal.content)[:100]}"
                    self.emergency_mode = True
                    
                    # في حالة الأمر المطلق: كل الانتباه للسيد
                    state.attention_allocation = {
                        "master": 1.0,
                        "sensory": 0.0,
                        "systemic": 0.0,
                        "subtle": 0.0,
                        "abyss": 0.0
                    }
                    
                    # تنفيذ الأمر فوراً (في النسخة الكاملة، هنا تتم المعالجة)
                    self.master_receiver.complete_command(
                        master_signal,
                        response="تم استلام الأمر المطلق وجاري التنفيذ."
                    )
                    
                    # تحديث الحالة
                    state.conscious_experience = f"⚡ أمر مطلق من السيد: {str(master_signal.content)[:200]}"
                    self.current_state = state
                    self._archive_state(state)
                    return state
            
            # ═══════════════════════════════════════════════
            # الخطوة ١: توزيع الانتباه الطبيعي (إذا لم يكن هناك أمر مطلق)
            # ═══════════════════════════════════════════════
            
            if not state.override_active:
                # السيد له الأولوية الدائمة حتى بدون أمر مطلق
                silence_info = self.master_receiver.check_silence()
                
                # توزيع الانتباه الأساسي
                attention = {
                    "master": 0.20,    # السيد دائماً في البال
                    "sensory": 0.30,   # الحواس المباشرة
                    "systemic": 0.25,  # حالة العالم
                    "subtle": 0.15,    # المحيط القريب
                    "abyss": 0.10      # الأعماق
                }
                
                # إذا كان هناك أمر سيد (غير مطلق)، يزيد انتباهه
                if master_signal:
                    attention["master"] = 0.50
                    attention["sensory"] = 0.20
                    attention["systemic"] = 0.15
                    attention["subtle"] = 0.10
                    attention["abyss"] = 0.05
                
                # إذا كان هناك إنذارات من دورة سابقة، نعيد توزيع الانتباه
                if self.current_state.critical_alarm_count > 0:
                    # تحويل انتباه من الطبقات الهادئة إلى مصادر الإنذار
                    pass
                
                state.attention_allocation = attention
                
                # ═══════════════════════════════════════════
                # الخطوة ٢: جمع الإدراكات من كل الطبقات
                # ═══════════════════════════════════════════
                
                # ٢.١ الطبقة الحسية
                try:
                    all_perceptions = self.sensory_matrix.get_all_perceptions_since(
                        self.current_state.timestamp
                    )
                    state.sensory_summary = {
                        "new_perceptions": len(all_perceptions),
                        "active_senses": len(self.sensory_matrix.get_active_senses()),
                        "total_senses": len(self.sensory_matrix.senses),
                        "latest": all_perceptions[-3:] if all_perceptions else []
                    }
                except Exception as e:
                    state.sensory_summary = {"error": str(e)}
                
                # ٢.٢ الطبقة النظامية
                try:
                    world_scan = self.systemic_integrator.full_scan()
                    state.systemic_summary = {
                        "world_status": world_scan.get("world_status", "unknown"),
                        "critical_alarms": world_scan.get("critical_alarms", 0),
                        "organs_scanned": len(world_scan.get("organs", {}))
                    }
                    if world_scan.get("critical_alarms", 0) > 0:
                        state.critical_alarm_count += world_scan["critical_alarms"]
                except Exception as e:
                    state.systemic_summary = {"error": str(e)}
                
                # ٢.٣ الطبقة السطحية
                try:
                    subtle_scan = self.subtle_integrator.full_scan()
                    state.subtle_summary = {
                        "environment_status": subtle_scan.get("environment_status", "unknown"),
                        "anomalies": subtle_scan.get("total_anomalies", 0)
                    }
                    if subtle_scan.get("environment_status") == "suspicious":
                        state.critical_alarm_count += 1
                except Exception as e:
                    state.subtle_summary = {"error": str(e)}
                
                # ٢.٤ طبقة الهاوية
                try:
                    abyss_probe = self.abyss_integrator.full_probe()
                    state.abyss_summary = {
                        "subconscious_concern": abyss_probe.get("subconscious_state", {}).get("overall_concern", 0),
                        "dominant_emotion": abyss_probe.get("subconscious_state", {}).get("dominant_emotion", "neutral"),
                        "new_insights": abyss_probe.get("new_insights_count", 0)
                    }
                except Exception as e:
                    state.abyss_summary = {"error": str(e)}
                
                # ═══════════════════════════════════════════
                # الخطوة ٣: تنفيذ أمر السيد (إذا وجد وغير مطلق)
                # ═══════════════════════════════════════════
                if master_signal and not state.override_active:
                    # هنا يتم تنفيذ الأمر في سياق كل الإدراكات المجمعة
                    self.master_receiver.complete_command(
                        master_signal,
                        response="تم التنفيذ في سياق الوعي الكامل."
                    )
            
            # ═══════════════════════════════════════════════
            # الخطوة ٤: تركيب التجربة الواعية
            # ═══════════════════════════════════════════════
            state.conscious_experience = self._compose_experience(state)
            
            # حفظ الحالة
            self.current_state = state
            self._archive_state(state)
            
            return state
    
    def _compose_experience(self, state: UnifiedConsciousnessState) -> str:
        """تركيب وصف نصي للتجربة الواعية الحالية."""
        parts = []
        
        if state.override_active:
            return f"⚡ حالة طوارئ: {state.override_reason}"
        
        # حضور السيد
        silence = self.master_receiver.check_silence()
        silence_dur = silence.get("silence_duration_seconds", 0)
        if silence_dur < 60:
            parts.append("السيد حاضر وقريب.")
        elif silence_dur < 3600:
            parts.append(f"السيد صامت منذ {silence_dur/60:.0f} دقائق.")
        else:
            parts.append(f"صمت السيد طويل: {silence_dur/3600:.1f} ساعات.")
        
        # العالم
        world = state.systemic_summary.get("world_status", "غير معروف")
        parts.append(f"العالم: {world}.")
        
        # المحيط
        env = state.subtle_summary.get("environment_status", "غير معروف")
        if env != "normal":
            parts.append(f"المحيط القريب: {env}.")
        
        # الأعماق
        emotion = state.abyss_summary.get("dominant_emotion", "neutral")
        concern = state.abyss_summary.get("subconscious_concern", 0)
        if concern > 0.3:
            parts.append(f"الشعور العميق: {emotion} (قلق: {concern:.2f}).")
        
        # إنذارات
        if state.critical_alarm_count > 0:
            parts.append(f"⚠️ {state.critical_alarm_count} إنذارات نشطة.")
        
        return " | ".join(parts) if parts else "وعي صافٍ، لا شيء يستدعي الانتباه."
    
    def _archive_state(self, state: UnifiedConsciousnessState):
        """أرشفة حالة الوعي للتاريخ والتطور."""
        self.consciousness_history.append({
            "cycle": state.cycle_id,
            "timestamp": state.timestamp,
            "attention": state.attention_allocation,
            "alarms": state.critical_alarm_count,
            "experience_summary": state.conscious_experience[:200]
        })
        if len(self.consciousness_history) > 10000:
            self.consciousness_history = self.consciousness_history[-5000:]
    
    def inject_external_signal(self, signal_name: str, data: Any) -> Dict:
        """حقن إشارة خارجية مباشرة إلى المصفوفة الحسية."""
        return self.sensory_matrix.receive_signal(signal_name, data)
    
    def inject_master_command(self, content: Any, command_type=None, priority=None) -> MasterSignal:
        """حقن أمر سيد مباشرة (للاستخدام من API Gateway)."""
        return self.master_receiver.receive(content, command_type, priority)
    
    def get_full_status(self) -> Dict:
        """تقرير كامل عن حالة المعرفة الكلية (للاستخدام من API)."""
        return {
            "core": "OMNISCIENCE_CORE",
            "cycle": self.cycle_count,
            "emergency_mode": self.emergency_mode,
            "current_state": self.current_state.to_dict(),
            "master": self.master_receiver.status_report(),
            "sensory": self.sensory_matrix.status_summary(),
            "systemic": self.systemic_integrator.status_report(),
            "subtle": self.subtle_integrator.status_report(),
            "abyss": self.abyss_integrator.status_report()
        }


# ═══════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي – محاكاة دورة وعي كاملة
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("اختبار المازج الأعظم - Omniscience Integration Core")
    print("=" * 60)
    
    # إنشاء النواة
    omni = OmniscienceCore()
    
    print("\n🔄 محاكاة دورات وعي...")
    
    # الدورة ١: وعي هادئ
    print("\n--- الدورة ١: البداية ---")
    state1 = omni.tick()
    print(f"🧠 التجربة: {state1.conscious_experience}")
    print(f"👁️ توزيع الانتباه: {state1.attention_allocation}")
    
    # الدورة ٢: حقن إشارة خارجية
    print("\n--- الدورة ٢: إشارة خارجية ---")
    omni.inject_external_signal("visible_light", {"objects": ["person"], "movement": True})
    state2 = omni.tick()
    print(f"🧠 التجربة: {state2.conscious_experience}")
    print(f"📡 ملخص حسي: {state2.sensory_summary}")
    
    # الدورة ٣: أمر سيد عادي
    print("\n--- الدورة ٣: أمر من السيد ---")
    omni.inject_master_command("كيف حال النظام؟")
    state3 = omni.tick()
    print(f"🧠 التجربة: {state3.conscious_experience}")
    print(f"👑 حضور السيد: {state3.master_present}")
    
    # الدورة ٤: أمر مطلق (يلغي كل شيء)
    print("\n--- الدورة ٤: أمر مطلق! ---")
    omni.inject_master_command(
        "تفعيل حالة الطوارئ القصوى!",
        priority=MasterSignalPriority.ABSOLUTE
    )
    state4 = omni.tick()
    print(f"🧠 التجربة: {state4.conscious_experience}")
    print(f"⚡ override: {state4.override_active}")
    print(f"👁️ توزيع الانتباه: {state4.attention_allocation}")
    
    # الدورة ٥: العودة للوعي الطبيعي
    print("\n--- الدورة ٥: بعد الطوارئ ---")
    omni.emergency_mode = False
    state5 = omni.tick()
    print(f"🧠 التجربة: {state5.conscious_experience}")
    
    # تقرير كامل
    print("\n" + "=" * 60)
    print("📊 تقرير المعرفة الكلية الشامل:")
    print("=" * 60)
    full_status = omni.get_full_status()
    
    # طباعة ملخصة
    print(f"الدورة الحالية: {full_status['cycle']}")
    print(f"حالة الطوارئ: {full_status['emergency_mode']}")
    print(f"حالة الوعي: {full_status['current_state']['conscious_experience']}")
    print(f"أوامر السيد: {full_status['master']['total_commands']} (معلق: {full_status['master']['pending']})")
    print(f"الحواس: {full_status['sensory']['total_senses']} (مكتشفة: {full_status['sensory']['discovered_senses']})")
    print(f"أعضاء العالم: {full_status['systemic']['total_organs']}")
    print(f"مستشعرات دقيقة: {full_status['subtle']['total_sensors']}")
    print(f"مسابر الهاوية: {full_status['abyss']['total_probes']}")
    
    print("\n✅ اكتمل الاختبار. المازج الأعظم جاهز للاتصال بـ SentientCore.")
