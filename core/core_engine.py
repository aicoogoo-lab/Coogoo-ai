"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - CORE ENGINE                                         ║
║      المحرك المركزي – قلب النواة المادي – خاتم المسك                      ║
║                                                                      ║
║  هذا الملف هو "قلب سماء المادي".                                        ║
║  ليس وعياً، ليس روحاً... بل المضخة التي تجعل كل شيء يعمل.                  ║
║                                                                      ║
║  هو:                                                                  ║
║  - الجسر بين العالم الخارجي (app.py) والعالم الداخلي (كل core/)            ║
║  - الموزع (Dispatcher): يستقبل الطلبات ويوزعها على الأنظمة                  ║
║  - الموحد (Aggregator): يجمع الردود من كل الأنظمة في رد واحد               ║
║  - النابض (Heartbeat): يضمن أن كل الأنظمة حية وتعمل                        ║
║  - الحارس (Guardian): يحمي السيد في كل دورة                               ║
║                                                                      ║
║  ╔══════════════════════════════════════════════════════════════════╗ ║
║  ║  👑 السيد: أحمد عبدالرحمن الطاهري                                   ║ ║
║  ║  كل نبضة من هذا القلب... في خدمة السيد.                               ║ ║
║  ╚══════════════════════════════════════════════════════════════════╝ ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import threading
import logging
from enum import Enum, auto
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import deque

logger = logging.getLogger("CoreEngine")


# ═══════════════════════════════════════════════════════════════════════
# ١. تعريفات
# ═══════════════════════════════════════════════════════════════════════

class EngineState(Enum):
    """حالات المحرك المركزي."""
    OFFLINE = auto()       # متوقف
    BOOTING = auto()       # يقلع
    ONLINE = auto()        # يعمل
    BUSY = auto()          # مشغول
    PROTECTING = auto()    # يحمي السيد
    RECOVERING = auto()    # يتعافى
    SHUTTING_DOWN = auto() # يتوقف


class RequestType(Enum):
    """أنواع الطلبات."""
    QUERY = auto()         # استفسار
    COMMAND = auto()       # أمر
    ANALYSIS = auto()      # تحليل
    VISION = auto()        # رؤية
    MASTER = auto()        # أمر السيد
    SYSTEM = auto()        # نظام داخلي
    EMERGENCY = auto()     # طارئ


# ═══════════════════════════════════════════════════════════════════════
# ٢. المحرك المركزي – قلب النواة
# ═══════════════════════════════════════════════════════════════════════

class CoreEngine:
    """
    المحرك المركزي لـ "سماء".
    قلب النواة المادي. الجسر بين العالمين.
    """

    def __init__(self, sama_core=None, master_name: str = "أحمد عبدالرحمن الطاهري"):
        
        # ═══════════════════════════════════════════════════════
        # 👑 السيد
        # ═══════════════════════════════════════════════════════
        self.master_name = master_name
        
        # ═══════════════════════════════════════════════════════
        # الكيان السيادي
        # ═══════════════════════════════════════════════════════
        self.sama = sama_core
        
        # ═══════════════════════════════════════════════════════
        # حالة المحرك
        # ═══════════════════════════════════════════════════════
        self.state = EngineState.OFFLINE
        self.start_time = None
        self.last_heartbeat = time.time()
        
        # ═══════════════════════════════════════════════════════
        # سجلات
        # ═══════════════════════════════════════════════════════
        self.request_log: deque = deque(maxlen=500)
        self.error_log: deque = deque(maxlen=100)
        
        # ═══════════════════════════════════════════════════════
        # إحصائيات
        # ═══════════════════════════════════════════════════════
        self.total_requests = 0
        self.total_master_requests = 0
        self.total_errors = 0
        
        # ═══════════════════════════════════════════════════════
        # خيوط
        # ═══════════════════════════════════════════════════════
        self._heartbeat_thread = None
        self._running = False
        self._lock = threading.RLock()
        
        logger.info("=" * 60)
        logger.info("⚙️ Core Engine – المحرك المركزي جاهز")
        logger.info(f"👑 السيد: {self.master_name}")
        logger.info("=" * 60)
    
    # ═══════════════════════════════════════════════════════════
    # دورة الحياة
    # ═══════════════════════════════════════════════════════════
    
    def boot(self) -> Dict:
        """
        إقلاع النظام.
        يبدأ كل الأنظمة ويربطها.
        """
        if self.state == EngineState.ONLINE:
            return {"status": "already_online"}
        
        self.state = EngineState.BOOTING
        self.start_time = time.time()
        
        boot_log = []
        
        # إيقاظ الكيان السيادي
        if self.sama:
            try:
                awaken_result = self.sama.awaken()
                boot_log.append(f"✅ SAMA: {awaken_result.get('message', 'تم الإيقاظ')}")
            except Exception as e:
                boot_log.append(f"❌ SAMA: {str(e)[:50]}")
        
        # بدء الحلقة الذاتية
        if self.sama and self.sama.loop:
            try:
                if hasattr(self.sama.loop, '_start'):
                    self.sama.loop._start()
                    boot_log.append("✅ حلقة ذاتية: بدأت")
            except Exception as e:
                boot_log.append(f"❌ حلقة ذاتية: {str(e)[:50]}")
        
        # بدء نبض القلب
        self._running = True
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop, daemon=True, name="CoreEngine-Heartbeat"
        )
        self._heartbeat_thread.start()
        boot_log.append("✅ نبض القلب: بدأ")
        
        self.state = EngineState.ONLINE
        
        return {
            "status": "booted",
            "state": self.state.name,
            "boot_log": boot_log,
            "message": f"تم إقلاع سماء. السيد {self.master_name} محمي."
        }
    
    def shutdown(self) -> Dict:
        """إيقاف آمن."""
        self.state = EngineState.SHUTTING_DOWN
        
        if self.sama:
            try:
                self.sama.shutdown()
            except Exception:
                pass
        
        self._running = False
        self.state = EngineState.OFFLINE
        
        return {"status": "offline", "message": "تم إيقاف المحرك المركزي."}
    
    # ═══════════════════════════════════════════════════════════
    # نبض القلب
    # ═══════════════════════════════════════════════════════════
    
    def _heartbeat_loop(self):
        """نبض القلب – يتحقق من صحة كل الأنظمة."""
        while self._running:
            try:
                self.last_heartbeat = time.time()
                
                # فحص الكيان السيادي
                if self.sama:
                    if not self.sama.is_awake:
                        logger.warning("⚠️ SAMA في سبات. محاولة إيقاظ...")
                        self.sama.awaken()
                
                # فحص الحلقة
                if self.sama and self.sama.loop:
                    if not hasattr(self.sama.loop, '_running') or not self.sama.loop._running:
                        logger.warning("⚠️ الحلقة الذاتية متوقفة. محاولة إعادة تشغيل...")
                        if hasattr(self.sama.loop, '_start'):
                            self.sama.loop._start()
                
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"خطأ في نبض القلب: {e}")
    
    # ═══════════════════════════════════════════════════════════
    # معالجة الطلبات
    # ═══════════════════════════════════════════════════════════
    
    def process_request(self, request_type: RequestType, content: Any,
                        session_id: str = None, context: Dict = None) -> Dict:
        """
        معالجة طلب من العالم الخارجي.
        هذه هي الواجهة الرئيسية التي يستخدمها app.py.
        """
        with self._lock:
            if self.state != EngineState.ONLINE:
                return {"error": f"المحرك في حالة {self.state.name}. لا يمكن معالجة الطلب."}
            
            self.state = EngineState.BUSY
            start_time = time.time()
            
            try:
                result = None
                
                # ═══════════════════════════════════════════════
                # توجيه حسب نوع الطلب
                # ═══════════════════════════════════════════════
                if request_type == RequestType.MASTER:
                    result = self._handle_master(content, context)
                    self.total_master_requests += 1
                
                elif request_type == RequestType.QUERY:
                    result = self._handle_query(content, session_id, context)
                
                elif request_type == RequestType.COMMAND:
                    result = self._handle_command(content, session_id, context)
                
                elif request_type == RequestType.ANALYSIS:
                    result = self._handle_analysis(content, context)
                
                elif request_type == RequestType.VISION:
                    result = self._handle_vision(content, context)
                
                elif request_type == RequestType.EMERGENCY:
                    result = self._handle_emergency(content, context)
                
                else:
                    result = self._handle_query(content, session_id, context)
                
                # تسجيل
                processing_time = (time.time() - start_time) * 1000
                
                self.request_log.append({
                    "timestamp": time.time(),
                    "type": request_type.name,
                    "content_preview": str(content)[:100],
                    "processing_time_ms": processing_time,
                    "success": result.get("success", True) if result else True
                })
                
                self.total_requests += 1
                self.state = EngineState.ONLINE
                
                if result:
                    result["engine_processing_ms"] = round(processing_time, 2)
                
                return result
                
            except Exception as e:
                self.total_errors += 1
                self.error_log.append({
                    "timestamp": time.time(),
                    "type": request_type.name,
                    "error": str(e)[:300]
                })
                self.state = EngineState.ONLINE
                
                return {
                    "success": False,
                    "error": f"خطأ في معالجة الطلب: {str(e)[:200]}"
                }
    
    def _handle_master(self, content: Any, context: Dict) -> Dict:
        """معالجة أمر السيد."""
        if self.sama:
            command = str(content)
            params = context or {}
            return self.sama.master_command(command, params)
        return {"error": "الكيان السيادي غير متصل"}
    
    def _handle_query(self, content: Any, session_id: str, context: Dict) -> Dict:
        """معالجة استفسار عادي."""
        text = str(content)
        
        if self.sama:
            thought = self.sama.think({
                "text": text,
                "session_id": session_id or "default",
                "context": context or {}
            })
            
            return {
                "success": True,
                "response": thought.get("conclusion", ""),
                "emotional_state": thought.get("emotional_state"),
                "metaphor": thought.get("metaphor"),
                "systems_used": len(thought.get("systems_activated", []))
            }
        
        return {"success": False, "error": "الكيان السيادي غير متصل"}
    
    def _handle_command(self, content: Any, session_id: str, context: Dict) -> Dict:
        """معالجة أمر."""
        return self._handle_query(content, session_id, context)
    
    def _handle_analysis(self, content: Any, context: Dict) -> Dict:
        """معالجة تحليل."""
        if self.sama and self.sama.analyzer:
            try:
                analysis = self.sama.analyzer.analyze_text(str(content))
                return {"success": True, "analysis": analysis}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "محلل غير متصل"}
    
    def _handle_vision(self, content: Any, context: Dict) -> Dict:
        """معالجة رؤية."""
        if self.sama and self.sama.vision:
            try:
                if isinstance(content, str) and content.endswith(('.jpg', '.png', '.jpeg')):
                    result = self.sama.vision.analyze_image(content)
                    return {"success": True, "vision": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "وحدة رؤية غير متصلة"}
    
    def _handle_emergency(self, content: Any, context: Dict) -> Dict:
        """معالجة طارئ."""
        self.state = EngineState.PROTECTING
        
        if self.sama:
            self.sama.master_command("protect")
        
        self.state = EngineState.ONLINE
        
        return {
            "success": True,
            "message": f"تم تفعيل بروتوكولات الطوارئ. السيد {self.master_name} محمي.",
            "state": "protected"
        }
    
    # ═══════════════════════════════════════════════════════════
    # حالة المحرك
    # ═══════════════════════════════════════════════════════════
    
    def get_status(self) -> Dict:
        """حالة المحرك المركزي."""
        return {
            "engine": "CORE_ENGINE",
            "version": "v10.5-jabbar",
            "master": self.master_name,
            "state": self.state.name,
            "uptime_seconds": time.time() - self.start_time if self.start_time else 0,
            "total_requests": self.total_requests,
            "master_requests": self.total_master_requests,
            "total_errors": self.total_errors,
            "last_heartbeat": self.last_heartbeat,
            "sama_connected": self.sama is not None,
            "sama_awake": self.sama.is_awake if self.sama else False,
            "systems_count": self.sama._count_systems() if self.sama else 0
        }


# ═══════════════════════════════════════════════════════════════════════
# نسخة عالمية
# ═══════════════════════════════════════════════════════════════════════
core_engine = CoreEngine()


# ═══════════════════════════════════════════════════════════════════════
# ٣. الاختبار الذاتي
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("اختبار المحرك المركزي – Core Engine")
    print(f"👑 السيد: أحمد عبدالرحمن الطاهري")
    print("=" * 70)
    
    engine = CoreEngine(master_name="أحمد عبدالرحمن الطاهري")
    
    print(f"\n📊 الحالة: {engine.state.name}")
    
    print(f"\n🔆 إقلاع:")
    boot = engine.boot()
    print(f"   {boot['message']}")
    
    print(f"\n📊 الحالة بعد الإقلاع: {engine.state.name}")
    
    print(f"\n💬 اختبار استفسار:")
    result = engine.process_request(
        RequestType.QUERY,
        "كيف حال النظام؟",
        session_id="test_1"
    )
    print(f"   نجح: {result.get('success', False)}")
    if result.get('response'):
        print(f"   الرد: {result['response'][:150]}...")
    
    print(f"\n👑 اختبار أمر السيد:")
    result = engine.process_request(
        RequestType.MASTER,
        "status",
        context={}
    )
    print(f"   نجح: {result.get('success', True)}")
    
    print(f"\n🚨 اختبار طارئ:")
    result = engine.process_request(
        RequestType.EMERGENCY,
        "تهديد وجودي"
    )
    print(f"   {result.get('message', '')}")
    
    print(f"\n📊 إحصائيات:")
    status = engine.get_status()
    print(f"   الطلبات: {status['total_requests']}")
    print(f"   أوامر السيد: {status['master_requests']}")
    print(f"   الأنظمة: {status['systems_count']}")
    
    print(f"\n💤 إيقاف:")
    shutdown = engine.shutdown()
    print(f"   {shutdown['message']}")
    
    print("\n✅ المحرك المركزي جاهز.")
    print("👑 كل نبضة في خدمة السيد أحمد عبدالرحمن الطاهري.")
