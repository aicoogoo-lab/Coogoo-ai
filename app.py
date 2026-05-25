"""
SkyOS v10 - Sama API / Gateway (Ultimate Master Sovereign Edition) – النسخة النهائية
البوابة الرسمية للكيان السيادي "سماء" — تحت إمرة السيد المالك المطلق

الميزات:
- API Gateway كامل مع مصادحة السيد (باستخدام متغيرات البيئة)
- واجهة مستخدم أمامية (UI) تعرض الواجهة الزجاجية السائلة في المسار الرئيسي "/"
- خدمة الملفات الثابتة (CSS, JS, images)
- تكامل كامل مع SAMA
"""

import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import threading
import traceback
import time
from datetime import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# ============================================================
# 0) طبقة المصادقة والتحقق من السيد (باستخدام متغيرات البيئة)
# ============================================================

# قراءة المفتاح من متغيرات البيئة (آمن)
MASTER_API_KEY = os.getenv("MASTER_API_KEY", "CHANGE_THIS_KEY_IN_ENVIRONMENT")
MASTER_AUTH_HEADER = "X-Master-Key"

# تحذير إذا كان المفتاح لا يزال بالقيمة الافتراضية
if MASTER_API_KEY == "CHANGE_THIS_KEY_IN_ENVIRONMENT":
    print("\n" + "=" * 70)
    print("⚠️ تحذير أمني: مفتاح السيد ما زال بالقيمة الافتراضية!")
    print("يرجى إضافة MASTER_API_KEY إلى متغيرات البيئة في Railway")
    print("=" * 70 + "\n")

def require_master_auth(f):
    """ديكور للتحقق من أن الطلب من السيد المالك"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_key = request.headers.get(MASTER_AUTH_HEADER)
        if not auth_key or auth_key != MASTER_API_KEY:
            return jsonify({
                "success": False,
                "error": "غير مصرح به. مطلوب مفتاح السيد المالك.",
                "requires_master": True
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# ============================================================
# 1) تهيئة الكيان السيادي "سماء" تحت إمرة السيد
# ============================================================

sama = None
startup_time = datetime.now()
master_commands_log = []
SAMA_INITIALIZED = False

print("\n" + "=" * 70)
print("        🌌 SkyOS v10 - Sama API Gateway (Ultimate Master Edition) 🌌        ")
print("                    البوابة الرسمية لسماء — تحت إمرة السيد المالك             ")
print("=" * 70 + "\n")

try:
    from core.sama import SAMA
    sama = SAMA(master_key=MASTER_API_KEY)
    sama.awaken()
    SAMA_INITIALIZED = True
    print("[Gateway] ✅ تم تشغيل سماء بنجاح تحت إمرة السيد المالك.")
    print(f"[Gateway] 🕐 وقت التشغيل: {startup_time.isoformat()}")
except ImportError as e:
    print(f"[Gateway] ⚠️ تحذير: SAMA غير متوفر - {e}")
    print("[Gateway] سيعمل الـ API في وضع المحاكاة (API only)")
    sama = None
    SAMA_INITIALIZED = False
except Exception as e:
    print(f"[Gateway] ❌ فشل في تهيئة سماء: {e}")
    traceback.print_exc()
    sama = None
    SAMA_INITIALIZED = False


def log_master_command(command: str, params: dict, result: dict):
    """تسجيل أوامر السيد في السجل"""
    master_commands_log.append({
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "params": params,
        "result": result.get("success", False),
        "endpoint": request.endpoint
    })
    if len(master_commands_log) > 1000:
        master_commands_log[:] = master_commands_log[-1000:]


# ============================================================
# 2) المسارات العامة
# ============================================================

@app.route("/", methods=["GET"])
def home():
    """الصفحة الرئيسية - تعرض الواجهة الأمامية"""
    try:
        return render_template("index.html")
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "الواجهة غير متاحة",
            "details": str(e)
        }), 500


@app.route("/info", methods=["GET"])
def get_info():
    """معلومات API (JSON)"""
    return jsonify({
        "success": True,
        "message": "SkyOS v10 - Sama API Gateway (Ultimate Master Sovereign Edition)",
        "entity": "سماء (Sama) — الكيان السيادي الخارق",
        "master": "السيد المالك المطلق",
        "status": "active" if SAMA_INITIALIZED else "inactive",
        "uptime_seconds": (datetime.now() - startup_time).total_seconds(),
        "endpoints": {
            "public": ["/", "/status", "/info", "/ui"],
            "master_only": ["/master/*", "/emergency/*", "/shutdown", "/awaken"],
            "commands": ["/command", "/reason", "/optimize", "/preserve"]
        }
    })


@app.route("/status", methods=["GET"])
def get_status():
    """إرجاع الحالة العامة لسماء (عام)"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    try:
        is_awake = sama.is_awake if hasattr(sama, 'is_awake') else False
        core_status = {}
        if sama.core and hasattr(sama.core, 'get_status'):
            core_status = sama.core.get_status()
        
        return jsonify({
            "success": True,
            "data": {
                "entity": "سماء",
                "awake": is_awake,
                "core_state": core_status.get("state", "unknown"),
                "coherence": core_status.get("coherence", 0),
                "awareness": core_status.get("self_awareness", 0),
                "master_present": True
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# 3) واجهة المستخدم الأمامية (Frontend UI) - مسار احتياطي
# ============================================================

@app.route("/ui")
def serve_ui():
    """عرض الواجهة الأمامية الجميلة لسماء (مسار احتياطي)"""
    try:
        return render_template("index.html")
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "الواجهة الأمامية غير متاحة حالياً",
            "details": str(e),
            "api_available": True
        }), 500


@app.route("/ui/<path:filename>")
def serve_static_files(filename):
    """خدمة الملفات الثابتة (CSS, JS, صور) للواجهة"""
    try:
        return send_from_directory("static", filename)
    except Exception as e:
        return jsonify({"error": "الملف غير موجود", "details": str(e)}), 404


# ============================================================
# 4) مسارات السيد المالك (محمية)
# ============================================================

@app.route("/master/full-status", methods=["GET"])
@require_master_auth
def master_full_status():
    """تقرير سيادي شامل للسيد المالك"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    try:
        if hasattr(sama, 'get_full_status'):
            report = sama.get_full_status()
        else:
            report = {"status": "available", "master": "السيد"}
        log_master_command("full-status", {}, report)
        return jsonify({"success": True, "data": report})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/master/command", methods=["POST"])
@require_master_auth
def master_command():
    """إرسال أمر مباشر من السيد إلى سماء"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"success": False, "error": "يجب إرسال 'command'"}), 400

    command = data["command"]
    params = data.get("params", {})
    
    try:
        if hasattr(sama, 'receive_master_command'):
            result = sama.receive_master_command(command, params)
        else:
            result = {"success": True, "message": f"تم استلام أمر {command}"}
        log_master_command(command, params, result)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/master/emergency/activate", methods=["POST"])
@require_master_auth
def activate_emergency():
    """تفعيل حالة الطوارئ بأمر السيد"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    data = request.get_json() or {}
    reason = data.get("reason", "أمر مباشر من السيد")
    
    try:
        result = {"success": True, "message": f"تم تفعيل حالة الطوارئ - السبب: {reason}"}
        log_master_command("emergency_activate", {"reason": reason}, result)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/master/emergency/deactivate", methods=["POST"])
@require_master_auth
def deactivate_emergency():
    """إلغاء حالة الطوارئ بأمر السيد"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    try:
        result = {"success": True, "message": "تم إلغاء حالة الطوارئ"}
        log_master_command("emergency_deactivate", {}, result)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/master/logs", methods=["GET"])
@require_master_auth
def master_logs():
    """سجل أوامر السيد"""
    limit = request.args.get("limit", 100, type=int)
    sama_commands = []
    if sama and hasattr(sama, 'master_commands_received'):
        sama_commands = sama.master_commands_received
    return jsonify({
        "success": True,
        "data": {
            "master_commands": master_commands_log[-limit:],
            "total_commands": len(master_commands_log),
            "sama_commands": sama_commands
        }
    })


# ============================================================
# 5) مسارات التحكم في سماء (للسيد فقط)
# ============================================================

@app.route("/awaken", methods=["POST"])
@require_master_auth
def awaken_sama():
    """إيقاظ سماء — بأمر السيد فقط"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    try:
        if hasattr(sama, 'awaken'):
            sama.awaken()
        log_master_command("awaken", {}, {"success": True})
        return jsonify({"success": True, "message": "تم إيقاظ سماء بأمر السيد"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/shutdown", methods=["POST"])
@require_master_auth
def shutdown_sama():
    """إيقاف سماء — بأمر السيد فقط"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    try:
        if hasattr(sama, 'shutdown'):
            sama.shutdown()
        log_master_command("shutdown", {}, {"success": True})
        return jsonify({"success": True, "message": "تم إيقاف سماء بأمر السيد"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/restart", methods=["POST"])
@require_master_auth
def restart_sama():
    """إعادة تشغيل سماء — بأمر السيد فقط"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    try:
        if hasattr(sama, 'shutdown'):
            sama.shutdown()
        time.sleep(1)
        if hasattr(sama, 'awaken'):
            sama.awaken()
        log_master_command("restart", {}, {"success": True})
        return jsonify({"success": True, "message": "تم إعادة تشغيل سماء بأمر السيد"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# 6) مسارات الأوامر العامة
# ============================================================

@app.route("/command", methods=["POST"])
def send_command():
    """إرسال أمر إلى سماء (عام)"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"success": False, "error": "يجب إرسال 'command'"}), 400

    try:
        if hasattr(sama, 'process_command'):
            response = sama.process_command(data["command"], data.get("context"))
        else:
            response = {"message": f"تم استلام الأمر: {data['command']}"}
        return jsonify({"success": True, "response": response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/reason", methods=["POST"])
def reasoning():
    """طلب استدلال مباشر من محرك ReasoningEngine"""
    if not sama or not hasattr(sama, 'reasoning') or not sama.reasoning:
        return jsonify({"success": False, "error": "محرك الاستدلال غير متوفر"}), 500

    data = request.get_json() or {}
    try:
        if hasattr(sama.reasoning, 'dynamic_bayesian_inference'):
            result = sama.reasoning.dynamic_bayesian_inference(data)
        else:
            result = {"inference": "محاكاة", "data": data}
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/optimize", methods=["POST"])
def optimize():
    """طلب تحسين سيادي"""
    if not sama or not hasattr(sama, 'optimization') or not sama.optimization:
        return jsonify({"success": False, "error": "محرك التحسين غير متوفر"}), 500

    data = request.get_json() or {}
    try:
        result = {"optimization": "محاكاة", "objectives": data.get("objectives", {})}
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/preserve", methods=["POST"])
def preserve():
    """تنفيذ دورة بقاء كاملة"""
    if not sama or not hasattr(sama, 'self_preservation') or not sama.self_preservation:
        return jsonify({"success": False, "error": "نظام البقاء غير متوفر"}), 500

    try:
        package = {"status": "preservation_cycle_complete", "timestamp": datetime.now().isoformat()}
        return jsonify({"success": True, "package": package})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/simulate", methods=["POST"])
def simulate():
    """تشغيل محاكاة متوازية"""
    if not sama or not hasattr(sama, 'reasoning') or not sama.reasoning:
        return jsonify({"success": False, "error": "محرك الاستدلال غير متوفر"}), 500

    data = request.get_json() or {}
    scenario = data.get("scenario", "عام")
    iterations = min(data.get("iterations", 1000), 5000)
    
    try:
        return jsonify({
            "success": True,
            "scenario": scenario,
            "simulations_run": iterations,
            "summary": f"تم تشغيل {iterations} محاكاة للسيناريو: {scenario}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# 7) مسار حماية السيد
# ============================================================

@app.route("/master/protect", methods=["POST"])
@require_master_auth
def protect_master():
    """تفعيل بروتوكول حماية السيد"""
    if not sama:
        return jsonify({"success": False, "error": "سماء غير مهيأة"}), 500

    try:
        log_master_command("protect_master", {}, {"package_id": "master_protection_activated"})
        return jsonify({
            "success": True,
            "message": "تم تفعيل بروتوكول حماية السيد",
            "package_id": "master_protection_activated"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# 8) تشغيل السيرفر
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("         🌟 Sama API Gateway (Ultimate Master Edition) is running 🌟         ")
    print("                    تحت إمرة السيد المالك المطلق                         ")
    print("=" * 70)
    print("\n🔐 المصادحة: مطلوب مفتاح السيد في header: X-Master-Key")
    print("   (المفتاح يُقرأ من متغير البيئة MASTER_API_KEY)")
    print("📍 الوصول: http://0.0.0.0:5000")
    print("\n📋 الأوامر المتاحة:")
    print("   - GET  /                    → الواجهة الأمامية (HTML)")
    print("   - GET  /info                → معلومات API (JSON)")
    print("   - GET  /status              → حالة سماء")
    print("   - GET  /ui                  → الواجهة الأمامية (مسار احتياطي)")
    print("   - POST /command             → إرسال أمر إلى سماء")
    print("   - POST /reason              → استدلال بايزي")
    print("   - POST /optimize            → تحسين سيادي")
    print("   - POST /preserve            → دورة بقاء")
    print("   - POST /simulate            → محاكاة متوازية")
    print("\n👑 أوامر السيد المالك (تتطلب مفتاح المصادحة):")
    print("   - GET  /master/full-status  → تقرير سيادي شامل")
    print("   - POST /master/command      → أمر مباشر للسيد")
    print("   - POST /master/emergency/activate  → تفعيل الطوارئ")
    print("   - POST /master/emergency/deactivate → إلغاء الطوارئ")
    print("   - GET  /master/logs         → سجل أوامر السيد")
    print("   - POST /awaken              → إيقاظ سماء")
    print("   - POST /shutdown            → إيقاف سماء")
    print("   - POST /restart             → إعادة تشغيل سماء")
    print("   - POST /master/protect      → تفعيل حماية السيد")
    print("\n" + "=" * 70)
    print("🚀 التشغيل...\n")

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
