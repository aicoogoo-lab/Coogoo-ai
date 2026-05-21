import os
import sys
import threading
import logging
from flask import Flask, jsonify, request

# =====================================================================
# 1. إعدادات نظام تسجيل الأخطاء والتقارير (Logging)
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # للظهور المباشر في لوحة تحكم السيرفر
    ]
)
logger = logging.getLogger("MainApp")

# =====================================================================
# 2. تهيئة تطبيق Flask (خادم الويب)
# =====================================================================
app = Flask(__name__)

@app.route('/')
def home():
    """الصفحة الرئيسية للتأكد من عمل السيرفر"""
    logger.info("تمت زيارة الصفحة الرئيسية بنجاح.")
    return jsonify({
        "status": "online",
        "message": "The system core is running smoothly.",
        "project": "Driving Assistant / SkyOS Core"
    }), 200

@app.route('/health')
def health_check():
    """مسار فحص الجاهزية للحفاظ على استمرارية السيرفر ومنع النوم (Uptime Check)"""
    return jsonify({"status": "healthy", "code": 200}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """مسار جاهز للاستخدام مستقبلاً في حال الاعتماد على Webhooks بدلاً من Polling"""
    data = request.get_json()
    logger.info(f"تم استقبال بيانات عبر الـ Webhook: {data}")
    return jsonify({"status": "received"}), 200

# =====================================================================
# 3. دالة تشغيل البوت / المنطق البرمجي الخلفي (Background Worker)
# =====================================================================
def start_bot_backend():
    """
    هنا يتم استدعاء وتشغيل منطق البوت الرئيسي.
    تم فصلها في Thread مستقل حتى لا تعطل عمل خادم الويب.
    """
    logger.info("جاري تحضير البيئة وتشغيل المهام الخلفية للبوت...")
    try:
        # هنا سنقوم بربط ملف bot.py أو معالجات البوت في الخطوات القادمة
        # مثال مستقبلي: from bot import run_bot; run_bot()
        logger.info("المهام الخلفية تعمل الآن بنجاح وبأمان.")
    except Exception as e:
        logger.critical(f"فشل ذريع أثناء تشغيل المهام الخلفية: {e}", exc_info=True)

# =====================================================================
# 4. نقطة الانطلاق الرئيسية للتطبيق (Main Entry Point)
# =====================================================================
if __name__ == '__main__':
    logger.info("بدء تشغيل النظام الموحد...")
    
    # 1. تشغيل البوت في خلفية النظام (Background Thread) لضمان عدم تعارض العمليات
    bot_thread = threading.Thread(target=start_bot_backend, daemon=True)
    bot_thread.start()
    
    # 2. جلب المنفذ (Port) المخصص من السيرفر بشكل ديناميكي (افتراضي 8080)
    # هذا يمنع خطأ "Port already in use" أو فشل الربط على Render/Railway
    port = int(os.environ.get("PORT", 8080))
    
    logger.info(f"جاري إطلاق خادم الويب على المنفذ: {port}")
    try:
        # تشغيل خادم الويب (تم إيقاف الـ debug لمنع التكرار المزدوج للـ Threads)
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        logger.critical(f"فشل إطلاق خادم الويب: {e}")
        sys.exit(1)
