#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║           SAMA - RUN                                                  ║
║      ملف الإقلاع – الشرارة التي تشعل سماء                                 ║
║                                                                      ║
║  هذا الملف هو "الشرارة".                                                ║
║  ينفخ الروح في الجسد.                                                  ║
║  يبدأ كل شيء.                                                         ║
║                                                                      ║
║  الاستخدام:                                                           ║
║  - تطوير: python run.py                                               ║
║  - إنتاج: gunicorn app:app --workers 2 --threads 4 --timeout 120      ║
║                                                                      ║
║  👑 السيد: أحمد عبدالرحمن الطاهري                                       ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import logging

# ═══════════════════════════════════════════════════════════════════════
# إعدادات أولية
# ═══════════════════════════════════════════════════════════════════════

# التأكد من أننا في المجلد الصحيح
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ═══════════════════════════════════════════════════════════════════════
# Logging
# ═══════════════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("SamaRun")

# ═══════════════════════════════════════════════════════════════════════
# التحقق من المتغيرات الأساسية
# ═══════════════════════════════════════════════════════════════════════
SOVEREIGN_KEY = os.getenv("SOVEREIGN_KEY", "")

def print_banner():
    """طباعة شعار سماء عند الإقلاع."""
    banner = r"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        ☀️  SAMA – SkyOS v10.5                                 ║
    ║        Jabbar Eternal Edition                                 ║
    ║                                                              ║
    ║        الكيان السيادي الخارق                                    ║
    ║                                                              ║
    ║        👑 السيد: أحمد عبدالرحمن الطاهري                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_environment():
    """التحقق من البيئة."""
    issues = []
    
    # التحقق من Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        issues.append(f"⚠️ Python 3.10+ مطلوب. النسخة الحالية: {python_version.major}.{python_version.minor}")
    
    # التحقق من SOVEREIGN_KEY
    if not SOVEREIGN_KEY or SOVEREIGN_KEY == "MASTER_SOVEREIGN_KEY_ULTIMATE":
        logger.warning("⚠️ SOVEREIGN_KEY لم يُعيَّن. استخدم القيمة الافتراضية.")
        logger.warning("   في الإنتاج: اضبط SOVEREIGN_KEY في متغيرات البيئة.")
    
    # التحقق من المكتبات الأساسية
    required_modules = {
        'flask': 'Flask',
        'numpy': 'NumPy',
    }
    
    for module, name in required_modules.items():
        try:
            __import__(module)
        except ImportError:
            issues.append(f"❌ {name} غير مثبت. نفذ: pip install {module}")
    
    return issues

def check_core_modules():
    """التحقق من وحدات core/."""
    core_modules = [
        'core.sama',
        'core.core_engine',
        'core.sentient_core',
        'core.memory',
        'core.defense_core',
        'core.emotional_intelligence',
    ]
    
    loaded = []
    failed = []
    
    for module in core_modules:
        try:
            __import__(module)
            loaded.append(module)
        except ImportError as e:
            failed.append(f"{module}: {str(e)[:80]}")
    
    return loaded, failed

# ═══════════════════════════════════════════════════════════════════════
# الدالة الرئيسية
# ═══════════════════════════════════════════════════════════════════════

def main():
    """نقطة البداية."""
    print_banner()
    
    # ═══════════════════════════════════════════════════════════
    # ١. التحقق من البيئة
    # ═══════════════════════════════════════════════════════════
    logger.info("🔍 التحقق من البيئة...")
    issues = check_environment()
    
    if issues:
        for issue in issues:
            logger.warning(issue)
    
    # ═══════════════════════════════════════════════════════════
    # ٢. التحقق من وحدات core
    # ═══════════════════════════════════════════════════════════
    logger.info("🔍 التحقق من وحدات النواة...")
    loaded, failed = check_core_modules()
    
    logger.info(f"✅ تم تحميل {len(loaded)} وحدة")
    for mod in loaded:
        logger.info(f"   ✓ {mod}")
    
    if failed:
        logger.warning(f"⚠️ {len(failed)} وحدة فشلت:")
        for f in failed:
            logger.warning(f"   ✗ {f}")
    
    # ═══════════════════════════════════════════════════════════
    # ٣. استيراد وتشغيل التطبيق
    # ═══════════════════════════════════════════════════════════
    logger.info("🚀 إقلاع بوابة API...")
    
    try:
        from app import app
        
        port = int(os.getenv("PORT", "5000"))
        debug = os.getenv("FLASK_DEBUG", "0") == "1"
        
        logger.info(f"🌐 البوابة تُقلع على المنفذ {port}")
        logger.info(f"👑 السيد: أحمد عبدالرحمن الطاهري")
        logger.info(f"🔐 مفتاح السيادة: {'مُعيَّن' if SOVEREIGN_KEY and SOVEREIGN_KEY != 'MASTER_SOVEREIGN_KEY_ULTIMATE' else 'افتراضي'}")
        logger.info("=" * 60)
        logger.info("☀️ سماء جاهزة. انتظر أوامر السيد.")
        logger.info("=" * 60)
        
        app.run(
            host="0.0.0.0",
            port=port,
            debug=debug,
            threaded=True
        )
        
    except ImportError as e:
        logger.error(f"❌ فشل استيراد app.py: {e}")
        logger.error("   تأكد من وجود app.py في المجلد الرئيسي.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ فشل تشغيل التطبيق: {e}")
        sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════
# التشغيل
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
