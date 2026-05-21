import os
import logging
import telebot  # تأكد من تثبيت pyTelegramBotAPI

# الاتصال بنظام تسجيل الأخطاء الموحد
logger = logging.getLogger("MainApp.Bot")

# =====================================================================
# 1. جلب رمز التشغيل (Token) بأمان
# =====================================================================
# يقوم النظام بجلب التوكن من السيرفر تلقائياً، ضع التوكن الافتراضي للتجربة المحلية فقط
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

# =====================================================================
# 2. إعداد وهيكلة وظائف البوت الرئيسية
# =====================================================================
def run_bot():
    """الدالة الرئيسية لتشغيل البوت والتي يتم استدعاؤها من ملف app.py"""
    
    if not TOKEN or TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("[❌] خطأ: لم يتم العثور على TELEGRAM_BOT_TOKEN في إعدادات البيئة! يرجى ضبطه أولاً.")
        return

    logger.info("[🤖] جاري تهيئة نظام البوت الذكي...")
    bot = telebot.TeleBot(TOKEN)

    # --- [أمر البدء /start] ---
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        user_name = message.from_user.first_name or "المستخدم"
        logger.info(f"استجابة لأمر البدء من المستخدم: {user_name} (ID: {message.chat.id})")
        
        welcome_text = (
            f"أهلاً بك يا {user_name} في نظام المساعد الذكي الموحد! 🚗💨\n\n"
            "النظام الآن يعمل بأعلى كفاءة مستقرة 24/7 وبدون أي انقطاع.\n"
            "جاهز لاستقبال أوامرك وتنسيق العمليات."
        )
        bot.reply_to(message, welcome_text)

    # --- [معالج الرسائل العامة والمشاوير] ---
    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        chat_id = message.chat.id
        text = message.text
        logger.info(f"رسالة واردة من {chat_id}: {text}")
        
        # هنا يمكنك وضع وتوسيع شروط التوصيل، التنسيق، أو البوت الوسيط مستقبلاً
        reply_text = f"⚙️ تم استلام طلبك بنجاح وجاري المعالجة الذكية...\nنص الرسالة: {text}"
        bot.reply_to(message, reply_text)

    # =====================================================================
    # 3. إطلاق البوت بنظام حلقة الاتصال اللانهائية الآمنة
    # =====================================================================
    logger.info("[🚀] البوت جاهز تماماً الآن ويستمع للرسائل...")
    try:
        # infinity_polling تمنع انهيار التطبيق عند حدوث أخطاء شبكة أو مهلات (Timeouts)
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        logger.critical(f"[💥] خطأ غير متوقع تسبب في توقف البوت: {e}", exc_info=True)
