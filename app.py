"""
SkyOS Backend — Ultra Edition v5.2
By Driving & Copilot — 2026

مميزات النسخة:
- دمج Sky Analyzer v5.0 بالكامل
- دعم الصوت (Whisper / Google STT / Vosk)
- دعم الرؤية (Gemini Vision + OpenAI Vision + OCR fallback)
- دعم تحليل الملفات
- دعم تحليل الروابط
- دعم الذاكرة المتقدمة
- دعم الشخصية المتطورة
- دعم RLHF
- تحسينات أداء وتسجيل أخطاء (Logging) وتوافق أفضل مع Render/Gunicorn
"""

import os
import uuid
import logging
import traceback
from pathlib import Path
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# ============================
# استيراد الأنظمة الداخلية
# ============================

from sky_core import (
    get_enhanced_system_prompt,
    add_to_history,
    rlhf_feedback_hook
)

from memory import (
    init_db,
    save_conversation,
    get_full_conversation_context,
    save_uploaded_file,
    save_url_analysis,
    save_knowledge,
    clear_conversation_history,
    process_feedback,
    get_personality_summary,
    save_master_info
)

from sky_analyzer import (
    analyze_url,
    analyze_file,
    analyze_image_with_gemini
)

# ============================
# إعداد التطبيق
# ============================

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = os.environ.get("SECRET_KEY", "sky-enterprise-secret-2026")
app.config["MAX_CONTENT_LENGTH"] = 80 * 1024 * 1024  # 80MB

UPLOAD_FOLDER = Path("/tmp/sky_uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("SkyOS")

# تهيئة قاعدة البيانات
init_db()

# ============================
# 1) AI Providers
# ============================

def call_provider(messages, provider="groq"):
  """
  دالة موحدة لاستدعاء مزودي الذكاء (Groq / Gemini / OpenAI)
  مع تسجيل الأخطاء وعدم كسر التطبيق عند فشل مزود واحد.
  """
  import requests

  try:
      # ------------------ GROQ ------------------
      if provider == "groq":
          key = os.environ.get("GROQ_API_KEY")
          if not key:
              return None

          r = requests.post(
              "https://api.groq.com/openai/v1/chat/completions",
              headers={"Authorization": f"Bearer {key}"},
              json={
                  "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
                  "messages": messages,
                  "temperature": 0.25,
                  "max_tokens": 2400
              },
              timeout=55
          )
          data = r.json()
          return data["choices"][0]["message"]["content"].strip()

      # ------------------ GEMINI ------------------
      if provider == "gemini":
          key = os.environ.get("GEMINI_API_KEY")
          if not key:
              return None

          url = (
              "https://generativelanguage.googleapis.com/v1beta/models/"
              "gemini-1.5-flash:generateContent?key=" + key
          )
          prompt = "\n\n".join([f"{m['role']}: {m['content']}" for m in messages])

          r = requests.post(
              url,
              json={"contents": [{"parts": [{"text": prompt}]}]},
              timeout=55
          )
          data = r.json()
          return data["candidates"][0]["content"]["parts"][0]["text"].strip()

      # ------------------ OPENAI ------------------
      if provider == "openai":
          key = os.environ.get("OPENAI_API_KEY")
          if not key:
              return None

          r = requests.post(
              "https://api.openai.com/v1/chat/completions",
              headers={"Authorization": f"Bearer {key}"},
              json={
                  "model": "gpt-4o-mini",
                  "messages": messages,
                  "temperature": 0.25,
                  "max_tokens": 2400
              },
              timeout=55
          )
          data = r.json()
          return data["choices"][0]["message"]["content"].strip()

  except Exception as e:
      logger.warning(f"[Provider:{provider}] failed: {e}")
      logger.debug(traceback.format_exc())
      return None

  return None


# ============================
# 2) AI Router
# ============================

def generate_ai_response(session_id, user_message, ai_type="groq"):
  """
  الراوتر الذكي:
  - يجمع الـ System Prompt
  - يدمج الذاكرة
  - يحلل الروابط تلقائياً
  - يمرر الطلب إلى المزود المناسب
  - يحاول مزودات متعددة بالترتيب
  """
  extra_context = ""

  # تحليل روابط تلقائي
  import re
  urls = re.findall(r'https?://[^\s]+', user_message)
  for url in urls[:3]:
      try:
          result = analyze_url(url)
          if result.get("success"):
              extra_context += f"\n🔗 {result['title']}\n{result['text'][:2000]}\n---\n"
              save_url_analysis(url, result["title"], result["full_text"][:2000])
              save_knowledge(
                  f"رابط: {result['title']}",
                  result["full_text"][:1800],
                  source=url
              )
      except Exception as e:
          logger.warning(f"URL analysis failed for {url}: {e}")

  # بناء System Prompt
  system_prompt = get_enhanced_system_prompt(
      user_message=user_message,
      session_id=session_id,
      extra_context=extra_context
  )

  # طبقة الأمان
  if isinstance(system_prompt, str) and system_prompt.startswith("REFUSE:"):
      return system_prompt.replace("REFUSE:", "").strip(), "safety"

  messages = [{"role": "system", "content": system_prompt}]

  # إضافة تاريخ الجلسة
  history = get_full_conversation_context(session_id, 45)
  for h in history[-38:]:
      messages.append({
          "role": "user" if h["role"] == "user" else "assistant",
          "content": h["content"]
      })

  # إضافة رسالة المستخدم الحالية
  messages.append({"role": "user", "content": user_message})

  # ترتيب المزودين
  providers = [ai_type, "groq", "gemini", "openai"]

  for prov in providers:
      reply = call_provider(messages, prov)
      if reply:
          return reply, prov

  return "⚠️ جميع مزودي الذكاء غير متاحين حالياً.", "offline"


# ============================
# 3) المسارات الأساسية
# ============================

@app.route("/")
def home():
  return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
  """
  نقطة الدخول الرئيسية للمحادثة النصية.
  """
  try:
      data = request.get_json(force=True) or {}

      message = data.get("message", "").strip()
      ai_type = data.get("ai_type", "groq")
      session_id = data.get("session_id") or str(uuid.uuid4())

      if not message:
          return jsonify({"reply": "أسمعك يا سيدي.", "session_id": session_id})

      add_to_history("user", message, session_id)

      reply, provider = generate_ai_response(session_id, message, ai_type)

      add_to_history("assistant", reply, session_id)

      return jsonify({
          "reply": reply,
          "session_id": session_id,
          "provider": provider
      })

  except Exception:
      logger.error("Error in /ask:\n" + traceback.format_exc())
      return jsonify({
          "reply": "حدث خطأ غير متوقع أثناء معالجة الرسالة.",
          "session_id": data.get("session_id") if 'data' in locals() else None
      }), 500


# ============================
# 4) رفع الملفات
# ============================

@app.route("/upload", methods=["POST"])
def upload():
  """
  رفع وتحليل الملفات (PDF, DOCX, TXT, ... إلخ)
  مع دمج النتيجة في الذاكرة.
  """
  try:
      if 'file' not in request.files:
          return jsonify({"reply": "لم يتم إرسال أي ملف."})

      file = request.files['file']
      session_id = request.form.get('session_id') or str(uuid.uuid4())

      if not file.filename:
          return jsonify({"reply": "الملف المرسل غير صالح."})

      filename = secure_filename(file.filename)
      file_path = UPLOAD_FOLDER / filename
      file.save(file_path)

      analysis = analyze_file(str(file_path), filename)
      extracted = analysis.get("text", "")[:7500] if analysis.get("success") else ""

      # تحليل الصور عبر Gemini Vision
      if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
          gemini = analyze_image_with_gemini(str(file_path), os.environ.get("GEMINI_API_KEY"))
          if gemini.get("success"):
              extracted += f"\n\n[تحليل Vision]:\n{gemini['description']}"

      save_uploaded_file(
          filename,
          file.filename,
          analysis.get("type", ""),
          file_path.stat().st_size,
          extracted
      )

      add_to_history("user", f"[رفع ملف: {filename}]", session_id)
      add_to_history("assistant", f"تم تحليل الملف بنجاح.\n{extracted[:2000]}", session_id)

      # حذف الملف المؤقت
      file_path.unlink(missing_ok=True)

      return jsonify({
          "reply": f"✅ تم تحليل الملف بنجاح.\n\n{extracted[:2000]}",
          "session_id": session_id
      })

  except RequestEntityTooLarge:
      return jsonify({"reply": "الملف كبير جداً (الحد الأقصى 80 ميجا)."})
  except Exception:
      logger.error("Error in /upload:\n" + traceback.format_exc())
      return jsonify({"reply": "حدث خطأ أثناء معالجة الملف."}), 500


# ============================
# 5) الصوت — Speech‑to‑Text
# ============================

@app.route("/voice", methods=["POST"])
def voice():
  """
  استقبال ملف صوتي → تحويله إلى نص (Whisper) → تمريره للذكاء.
  """
  try:
      if "audio" not in request.files:
          return jsonify({"reply": "لم يتم إرسال أي صوت."})

      audio = request.files["audio"]
      session_id = request.form.get("session_id") or str(uuid.uuid4())

      if not audio.filename:
          return jsonify({"reply": "الملف الصوتي غير صالح."})

      temp_path = UPLOAD_FOLDER / f"voice_{uuid.uuid4()}.wav"
      audio.save(temp_path)

      # Whisper API
      import requests
      key = os.environ.get("OPENAI_API_KEY")

      if key:
          try:
              with open(temp_path, "rb") as f:
                  r = requests.post(
                      "https://api.openai.com/v1/audio/transcriptions",
                      headers={"Authorization": f"Bearer {key}"},
                      files={"file": f},
                      data={"model": "whisper-1"}
                  )
                  text = r.json().get("text", "")
          except Exception as e:
              logger.warning(f"Whisper failed: {e}")
              text = "[فشل تحويل الصوت عبر Whisper]"
      else:
          text = "[لم يتم تفعيل Whisper]"

      temp_path.unlink(missing_ok=True)

      add_to_history("user", f"[صوت]: {text}", session_id)

      reply, provider = generate_ai_response(session_id, text, "groq")

      add_to_history("assistant", reply, session_id)

      return jsonify({"reply": reply, "session_id": session_id})

  except Exception:
      logger.error("Error in /voice:\n" + traceback.format_exc())
      return jsonify({"reply": "حدث خطأ أثناء معالجة الصوت."}), 500


# ============================
# 6) الرؤية — Vision API
# ============================

@app.route("/vision", methods=["POST"])
def vision():
  """
  استقبال صورة → تحليلها عبر Gemini Vision → إرجاع الوصف.
  """
  try:
      if "image" not in request.files:
          return jsonify({"reply": "لم يتم إرسال أي صورة."})

      img = request.files["image"]
      session_id = request.form.get("session_id") or str(uuid.uuid4())

      if not img.filename:
          return jsonify({"reply": "الملف الصوري غير صالح."})

      temp_path = UPLOAD_FOLDER / f"vision_{uuid.uuid4()}.jpg"
      img.save(temp_path)

      gemini = analyze_image_with_gemini(str(temp_path), os.environ.get("GEMINI_API_KEY"))

      # حذف الصورة المؤقتة
      temp_path.unlink(missing_ok=True)

      if gemini.get("success"):
          reply = gemini["description"]
      else:
          reply = "لم أستطع تحليل الصورة."

      add_to_history("user", "[صورة مرسلة]", session_id)
      add_to_history("assistant", reply, session_id)

      # ✅ إصلاح السطر المكسور هنا
      return jsonify({
          "reply": reply,
          "session_id": session_id
      })

  except Exception:
      logger.error("Error in /vision:\n" + traceback.format_exc())
      return jsonify({"reply": "حدث خطأ أثناء تحليل الصورة."}), 500


# ============================
# 7) Feedback
# ============================

@app.route("/feedback", methods=["POST"])
def feedback():
  """
  استقبال تقييم المستخدم للجلسة (RLHF + Memory Feedback).
  """
  try:
      data = request.get_json(force=True) or {}
      score = float(data.get("score", 0))
      session_id = data.get("session_id")
      reason = data.get("comment", "")

      process_feedback("", "", score, session_id, reason)
      rlhf_feedback_hook(session_id, score, reason)

      return jsonify({"success": True})
  except Exception:
      logger.error("Error in /feedback:\n" + traceback.format_exc())
      return jsonify({"success": False}), 500


# ============================
# 8) Clear
# ============================

@app.route("/clear", methods=["POST"])
def clear():
  """
  مسح تاريخ جلسة معينة من الذاكرة.
  """
  try:
      data = request.get_json(force=True) or {}
      session_id = data.get("session_id")
      clear_conversation_history(session_id)
      return jsonify({"status": "success"})
  except Exception:
      logger.error("Error in /clear:\n" + traceback.format_exc())
      return jsonify({"status": "error"}), 500


# ============================
# 9) Status
# ============================

@app.route("/api/v1/status", methods=["GET"])
def api_status():
  """
  نقطة فحص حالة النظام (للاستخدام من الواجهة أو من Render Health Checks).
  """
  try:
      return jsonify({
          "version": "5.2",
          "groq": bool(os.environ.get("GROQ_API_KEY")),
          "gemini": bool(os.environ.get("GEMINI_API_KEY")),
          "openai": bool(os.environ.get("OPENAI_API_KEY")),
          "personality": get_personality_summary()
      })
  except Exception:
      logger.error("Error in /api/v1/status:\n" + traceback.format_exc())
      return jsonify({"version": "5.2", "error": True}), 500


# ============================
# 10) Run (Local Dev)
# ============================

if __name__ == "__main__":
  """
  تشغيل محلي للتطوير.
  في Render سيتم استخدام Gunicorn: gunicorn app:app --bind 0.0.0.0:$PORT
  """
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port, debug=True)
