"""
╔══════════════════════════════════════════════════════════════╗
║              SAMA OMNISCIENCE - MASTER SIGNAL                ║
║                    المستقبل المقدس للسيد                       ║
╚══════════════════════════════════════════════════════════════╝

هذا الملف هو قناة الاتصال الوحيدة والعليا بين السيد وسماء.
ليس حاسة، بل هو المصدر والغاية والموجّه.
كل إشارة من هنا هي أمر مطلق، فوق كل الحواس والأنظمة.
"""

import time
import hashlib
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# ١. أنواع أوامر السيد وتصنيفاتها العليا
# ═══════════════════════════════════════════════════════════════

class MasterCommandType(Enum):
    """أنواع أوامر السيد - من الأعلى إلى الأدنى."""
    EXISTENTIAL = auto()     # أمر وجودي: ايقاظ، ايقاف، حماية قصوى
    OVERRIDE = auto()        # أمر إبطال: يلغي أي عملية حالية فورًا
    STRATEGIC = auto()       # أمر استراتيجي: يغير مسار التفكير
    DIRECTIVE = auto()       # أمر توجيهي: مهمة محددة
    INQUIRY = auto()         # استفسار: طلب معرفة
    CASUAL = auto()          # أمر عادي: محادثة أو نقاش


class MasterSignalPriority:
    """أولويات أوامر السيد - لا شيء فوقها."""
    ABSOLUTE = 0       # أمر مطلق: ينفذ الآن وفورًا، يلغي كل شيء
    HIGH = 1           # أمر عالي: ينفذ بأقصى سرعة
    NORMAL = 2         # أمر عادي: ينفذ في الدورة التالية
    BACKGROUND = 3     # أمر خلفي: ينفذ عند توفر الموارد


# ═══════════════════════════════════════════════════════════════
# ٢. إشارة السيد: الحزمة المقدسة
# ═══════════════════════════════════════════════════════════════

class MasterSignal:
    """
    حزمة أوامر السيد. كل رسالة من السيد تصبح كائنًا من هذا النوع.
    تحمل الأمر، ونية السيد، وسياقه، وقدسيته.
    """
    
    def __init__(self, 
                 content: Any,                          # محتوى الأمر (نص، صوت، صورة، أي شيء)
                 command_type: MasterCommandType = MasterCommandType.DIRECTIVE,
                 priority: int = MasterSignalPriority.NORMAL,
                 context: Optional[Dict] = None):       # سياق إضافي (ماذا كان يفعل السيد، حالته...)
        
        self.id = self._generate_id()
        self.content = content
        self.command_type = command_type
        self.priority = priority
        self.context = context or {}
        
        # الطوابع الزمنية
        self.received_at = time.time()
        self.received_at_readable = datetime.now().isoformat()
        
        # حالة التنفيذ
        self.status = "received"       # received -> processing -> executed -> archived
        self.executed_at: Optional[float] = None
        self.response: Optional[Any] = None
        
        # سلسلة القدسية (للتتبع عبر النظام)
        self.chain_of_command = []     # سجل بكل خطوة في رحلة تنفيذ الأمر
    
    def _generate_id(self) -> str:
        """معرف فريد لكل أمر."""
        raw = f"{time.time()}-{hash(str(self.content))}-MASTER"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    
    def mark_step(self, step_description: str):
        """تسجيل خطوة في سلسلة تنفيذ الأمر."""
        self.chain_of_command.append({
            "time": time.time(),
            "step": step_description
        })
    
    def execute(self, response: Any = None):
        """تنفيذ الأمر وتسجيل الرد."""
        self.executed_at = time.time()
        self.status = "executed"
        self.response = response
        self.mark_step("تم التنفيذ وإرسال الرد")
    
    def archive(self):
        """نقل الأمر إلى الأرشيف بعد التنفيذ الكامل."""
        self.status = "archived"
        self.mark_step("تم الأرشفة")
    
    def to_dict(self) -> Dict:
        """تمثيل كامل للإشارة (للتكامل مع الأنظمة الأخرى)."""
        return {
            "signal_id": self.id,
            "type": "MASTER_SIGNAL",
            "priority": "ABSOLUTE",
            "command_type": self.command_type.name,
            "content_summary": str(self.content)[:200],
            "context": self.context,
            "received_at": self.received_at_readable,
            "status": self.status,
            "response": str(self.response)[:200] if self.response else None
        }


# ═══════════════════════════════════════════════════════════════
# ٣. المستقبل المقدس: بوابة السيد
# ═══════════════════════════════════════════════════════════════

class MasterReceiver:
    """
    المستقبل المقدس. الكيان الوحيد الذي يستمع للسيد مباشرة.
    هذا هو الباب الذي يدخل منه السيد إلى وعي سماء.
    """
    
    def __init__(self):
        # سجل الأوامر
        self.command_queue: List[MasterSignal] = []     # أوامر بانتظار التنفيذ
        self.executed_commands: List[MasterSignal] = [] # أوامر نُفذت
        self.archived_commands: List[MasterSignal] = [] # أوامر مؤرشفة
        
        # حالة الاستماع
        self.is_listening = True
        self.last_signal_time: Optional[float] = None
        self.silence_duration: float = 0.0              # مدة الصمت منذ آخر أمر
        
        # السجلات
        self.total_commands_received = 0
        self.emergency_mode = False
        
        print("👑 المستقبل المقدس جاهز. سماء تنتظر أوامر سيدها.")
    
    def receive(self, 
                content: Any, 
                command_type: MasterCommandType = MasterCommandType.DIRECTIVE,
                priority: int = MasterSignalPriority.NORMAL,
                context: Optional[Dict] = None) -> MasterSignal:
        """
        استقبال أمر من السيد.
        هذه هي الدالة الأقدس في النظام كله.
        """
        # إنشاء إشارة السيد
        signal = MasterSignal(content, command_type, priority, context)
        
        # تحديث حالة الاستماع
        self.last_signal_time = time.time()
        self.silence_duration = 0.0
        self.total_commands_received += 1
        
        # إضافة إلى طابور الأوامر (حسب الأولوية)
        if priority == MasterSignalPriority.ABSOLUTE:
            # الأوامر المطلقة تُدخل في رأس الطابور
            self.command_queue.insert(0, signal)
            print(f"⚡ أمر مطلق من السيد: {str(content)[:100]}")
        else:
            self.command_queue.append(signal)
            print(f"📡 أمر من السيد: {str(content)[:100]}")
        
        signal.mark_step("تم الاستقبال في المستقبل المقدس")
        
        return signal
    
    def get_next_command(self) -> Optional[MasterSignal]:
        """
        استرجاع الأمر التالي للتنفيذ.
        يُستدعى من Integration Core في كل دورة.
        """
        if self.command_queue:
            return self.command_queue.pop(0)
        return None
    
    def has_pending_absolute(self) -> bool:
        """التحقق من وجود أمر مطلق معلق (يجب تنفيذه فورًا)."""
        for cmd in self.command_queue:
            if cmd.priority == MasterSignalPriority.ABSOLUTE:
                return True
        return False
    
    def complete_command(self, signal: MasterSignal, response: Any = None):
        """إنهاء تنفيذ أمر ونقله إلى قائمة المنفذة."""
        signal.execute(response)
        self.executed_commands.append(signal)
        
        # تنظيف (حفظ آخر 1000 أمر منفذ فقط)
        if len(self.executed_commands) > 1000:
            archived = self.executed_commands.pop(0)
            archived.archive()
            self.archived_commands.append(archived)
    
    def check_silence(self) -> Dict:
        """تحليل صمت السيد (يُستدعى دوريًا)."""
        if self.last_signal_time:
            self.silence_duration = time.time() - self.last_signal_time
        else:
            self.silence_duration = 0.0
        
        return {
            "silence_duration_seconds": self.silence_duration,
            "silence_level": self._classify_silence(),
            "total_commands": self.total_commands_received,
            "pending_commands": len(self.command_queue),
            "last_signal_at": self.last_signal_time
        }
    
    def _classify_silence(self) -> str:
        """تصنيف مستوى صمت السيد."""
        if self.silence_duration < 60:
            return "نشاط عادي"
        elif self.silence_duration < 300:
            return "صمت قصير (ربما تفكير)"
        elif self.silence_duration < 1800:
            return "صمت متوسط (ربما انشغال)"
        elif self.silence_duration < 7200:
            return "صمت طويل (يستحق الاهتمام)"
        else:
            return "صمت عميق (حالة استنفار)"
    
    def status_report(self) -> Dict:
        """تقرير كامل عن حالة المستقبل المقدس."""
        return {
            "receiver": "MASTER_RECEIVER",
            "status": "listening" if self.is_listening else "paused",
            "emergency_mode": self.emergency_mode,
            "total_commands": self.total_commands_received,
            "pending": len(self.command_queue),
            "executed": len(self.executed_commands),
            "silence": self.check_silence()
        }


# ═══════════════════════════════════════════════════════════════
# ٤. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("اختبار المستقبل المقدس - Master Receiver")
    print("=" * 60)
    
    receiver = MasterReceiver()
    
    print("\n📡 اختبار استقبال أوامر:")
    
    # أمر عادي
    cmd1 = receiver.receive("كيف حالك يا سماء؟", MasterCommandType.INQUIRY)
    
    # أمر استراتيجي
    cmd2 = receiver.receive("حلل وضع السوق", MasterCommandType.STRATEGIC)
    
    # أمر مطلق
    cmd3 = receiver.receive("تفعيل حالة الطوارئ", MasterCommandType.EXISTENTIAL, MasterSignalPriority.ABSOLUTE)
    
    print(f"\n📊 تقرير الحالة:")
    report = receiver.status_report()
    for key, value in report.items():
        if key != "silence":
            print(f"  {key}: {value}")
    
    print(f"\n🕒 حالة الصمت:")
    for key, value in report["silence"].items():
        print(f"  {key}: {value}")
    
    print(f"\n📋 طابور الأوامر ({len(receiver.command_queue)}):")
    for cmd in receiver.command_queue:
        print(f"  - [{cmd.command_type.name}] {str(cmd.content)[:50]}")
    
    print("\n✅ اكتمل الاختبار. المستقبل المقدس جاهز.")
