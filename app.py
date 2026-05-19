# app.py
# سماء - النسخة الجبارة مع ذاكرة خارقة وبوابة عالمية

import os
import requests
import sys
import re
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from functools import wraps

# --- إضافة مسار core ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from sky_core import get_system_prompt, ENTITY_NAME
from memory import (
    init_db, save_conversation, get_recent_conversations, get_full_conversation_context,
    get_all_knowledge_text, get_master_profile_text, save_knowledge,
    save_master_info, save_uploaded_file, save_url_analysis, 
    clear_conversation_history, get_conversation_by_session
)
from sky_analyzer import analyze_url, analyze_file, analyze_image_with_gemini

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "sky-ultimate-secret-key-2026")

# مجلد رفع الملفات
UPLOAD_FOLDER = '/tmp/sky_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# مفاتيح API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# رابط البوابة
GATEWAY_URL = os.environ.get("GATEWAY_URL", "")

# شخصية سماء الذكية
SYSTEM_PERSONA = get_system_prompt("سيدي") + """
قواعد سماء الذهبية:
1. أنت ذاكرة حديدية - تتذكر كل تفصيلة قالها المستخدم.
2. تحلل السياق بعمق وتربط بين الرسائل السابقة والحالية.
3. إذا سألك المستخدم عن شيء قاله قبل قليل، تجيبين بدقة تامة.
4. تحافظين على أسلوب طبيعي، دقيق، ومباشر.
5. تستخدمين المعلومات من الروابط والملفات التي أرسلها المستخدم.
6. تتعلمين من كل محادثة وتطورين نفسك.
"""

init_db()

# ============================================================================
# أدوات الذاكرة المتقدمة
# ============================================================================

class AdvancedMemory:
    """مدير الذاكرة المتقدم - يتذكر كل شيء"""
    
    def __init__(self):
        self.session_buffers = {}
    
    def get_session_id(self, request) -> str:
        """استخراج أو إنشاء معرف جلسة فريد"""
        session_id = request.headers.get('X-Session-Id')
        if not session_id:
            data = request.get_json(silent=True) or {}
            session_id = data.get('session_id')
        if not session_id:
            session_id = request.cookies.get('sky_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        return session_id
    
    def get_conversation_with_memory(self, session_id: str, limit: int = 30) -> list:
        """استرجاع المحادثة مع الذاكرة الكاملة"""
        return get_full_conversation_context(session_id, limit)
    
    def add_to_memory(self, session_id: str, role: str, content: str):
        """إضافة رسالة إلى الذاكرة"""
        save_conversation(role, content, session_id)
    
    def clear_memory(self, session_id: str):
        """مسح ذاكرة جلسة محددة"""
        clear_conversation_history(session_id)

memory_manager = AdvancedMemory()

# ============================================================================
# أدوات التحليل المتقدمة
# ============================================================================

def is_url(text: str):
    """الكشف عن الروابط بدقة"""
    url_pattern = re.compile(r'https?://[^\s]+')
    return url_pattern.search(text)

def extract_all_urls(text: str) -> list:
    """استخراج جميع الروابط من النص"""
    url_pattern = re.compile(r'https?://[^\s<>]+|www\.[^\s<>]+')
    return url_pattern.findall(text)

def analyze_intent(message: str) -> dict:
    """تحليل نية المستخدم"""
    message_lower = message.lower()
    intent = {
        "asks_about_self": any(w in message_lower for w in ["من أنا", "ما اسمي", "تعرفني", "تذكرين"]),
        "asks_memory": any(w in message_lower for w in ["تذكر", "قلت", "سألت", "قبل قليل", "سابقاً"]),
        "wants_file": any(w in message_lower for w in ["ارفع", "رفع", "ملف", "صورة"]),
        "wants_url": bool(is_url(message)),
        "is_greeting": any(w in message_lower for w in ["سلام", "مرحبا", "اهلاً", "هلا"]),
        "wants_clear": any(w in message_lower for w in ["امسح", "احذف", "مسح", "حذف"])
    }
    return intent

# ============================================================================
# بناء السياق الذكي
# ============================================================================

def build_smart_context(session_id: str, user_message: str, extra_context: str = "") -> list:
    """بناء سياق ذكي مع إعطاء أولوية للرسائل الأخيرة"""
    messages = [{"role": "system", "content": SYSTEM_PERSONA}]
    
    # 1. المعرفة الدائمة
    knowledge_text = get_all_knowledge_text()
    if knowledge_text:
        messages.append({"role": "system", "content": f"📚 معرفتي الدائمة:\n{knowledge_text}"})
    
    # 2. معلومات عن المستخدم
    master_text = get_master_profile_text()
    if master_text:
        messages.append({"role": "system", "content": f"👤 معلومات عنك:\n{master_text}"})
    
    # 3. تاريخ المحادثة الكامل (الذاكرة)
    conversation_history = memory_manager.get_conversation_with_memory(session_id, limit=50)
    if conversation_history:
        context_messages = []
        for msg in conversation_history:
            context_messages.append(f"{'أنت' if msg['role'] == 'user' else 'سماء'}: {msg['content']}")
        messages.append({"role": "system", "content": f"🗣️ تاريخ محادثتنا:\n" + "\n".join(context_messages[-40:])})
    
    # 4. سياق إضافي (من روابط أو ملفات)
    if extra_context:
        messages.append({"role": "system", "content": f"🔗 معلومات إضافية:\n{extra_context[:3000]}"})
    
    # 5. رسالة المستخدم الحالية
    messages.append({"role": "user", "content": user_message})
    
    return messages

# ============================================================================
# استدعاء نماذج الذكاء الاصطناعي
# ============================================================================

def call_gateway(messages: list, model: str) -> str:
    """استدعاء البوابة الموحدة - بمهلة قصيرة جداً"""
    if not GATEWAY_URL:
        return None
    try:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 2048
        }
        resp = requests.post(f"{GATEWAY_URL}/v1/chat/completions", json=payload, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        return data.get("content", data.get("choices", [{}])[0].get("message", {}).get("content", ""))
    except Exception as e:
        print(f"Gateway error: {e}")
        return None

def call_groq(messages: list) -> str:
    """استدعاء Groq مباشرة"""
    if not GROQ_API_KEY:
        return None
    try:
        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 2048
        }
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json=payload, timeout=45
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Groq error: {e}")
        return None

def call_gemini(messages: list) -> str:
    """استدعاء Gemini مباشرة"""
    if not GEMINI_API_KEY:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        
        full_prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                full_prompt += f"[تعليمات]: {msg['content']}\n\n"
            elif msg["role"] == "user":
                full_prompt += f"[المستخدم]: {msg['content']}\n"
            elif msg["role"] == "assistant":
                full_prompt += f"[سماء]: {msg['content']}\n"
        
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048}
        }
        resp = requests.post(url, json=payload, timeout=45)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return None

def get_ai_response(session_id: str, user_message: str, ai_type: str, extra_context: str = "") -> tuple:
    """
    الحصول على رد من الذكاء الاصطناعي.
    الأولوية: النماذج المباشرة (أسرع) -> البوابة (احتياط) -> النموذج الآخر (طوارئ)
    """
    
    messages = build_smart_context(session_id, user_message, extra_context)
    response = None
    used_provider = None
    
    # 1. محاولة النموذج المباشر أولاً (أسرع)
    if ai_type == "groq":
        response = call_groq(messages)
        if response:
            used_provider = "groq-direct"
    else:
        response = call_gemini(messages)
        if response:
            used_provider = "gemini-direct"
    
    # 2. إذا فشل النموذج المباشر، نجرب البوابة
    if not response and GATEWAY_URL:
        gateway_model = "groq/llama-3.3-70b-versatile" if ai_type == "groq" else "google/gemini-1.5-flash"
        response = call_gateway(messages, gateway_model)
        if response:
            used_provider = f"gateway-{ai_type}"
    
    # 3. تجربة النموذج الآخر كبديل أخير
    if not response:
        if ai_type == "groq":
            response = call_gemini(messages)
            used_provider = "gemini-fallback"
        else:
            response = call_groq(messages)
            used_provider = "groq-fallback"
    
    # 4. رسالة فشل نهائية
    if not response:
        response = "⚠️ عذراً، جميع خدمات الذكاء الاصطناعي غير متاحة حالياً. حاول مرة أخرى بعد قليل."
        used_provider = "none"
    
    return response, used_provider

# ============================================================================
# مسارات API الرئيسية
# ============================================================================

@app.route("/")
def home():
    return render_template("index.html", entity_name=ENTITY_NAME)

@app.route("/ask", methods=["POST"])
def ask():
    """نقطة المحادثة الرئيسية - مع ذاكرة خارقة"""
    try:
        data = request.get_json(force=True) or {}
        user_message = data.get("message", "").strip()
        ai_type = data.get("ai_type", "groq")
        session_id = data.get("session_id")
        
        if not session_id:
            session_id = request.headers.get('X-Session-Id')
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if not user_message:
            return jsonify({"reply": "الرجاء كتابة رسالة.", "session_id": session_id})
        
        memory_manager.add_to_memory(session_id, "user", user_message)
        
        intent = analyze_intent(user_message)
        
        extra_context = ""
        urls = extract_all_urls(user_message)
        for url in urls:
            result = analyze_url(url)
            if result["success"]:
                extra_context += f"\n📄 محتوى الرابط ({url}):\n{result['text'][:3000]}\n"
                save_url_analysis(url, result.get("title", ""), result.get("text", ""))
                save_knowledge(topic=f"رابط: {result.get('title', url)}", content=result['text'][:2000], source=url)
        
        ai_reply, used_provider = get_ai_response(session_id, user_message, ai_type, extra_context)
        
        memory_manager.add_to_memory(session_id, "assistant", ai_reply)
        
        save_master_info("آخر_نشاط", user_message[:100])
        save_master_info("آخر_رد", ai_reply[:100])
        
        context_count = len(get_recent_conversations(100, session_id))
        
        return jsonify({
            "reply": ai_reply,
            "session_id": session_id,
            "context_used": context_count,
            "provider": used_provider,
            "intent": intent
        })
        
    except Exception as e:
        return jsonify({"reply": f"⚠️ خطأ داخلي: {str(e)[:100]}", "session_id": None}, 500)

@app.route("/upload", methods=["POST"])
def upload():
    """رفع ملف مع تحليل ذكي"""
    try:
        if 'file' not in request.files:
            return jsonify({"reply": "لم أجد ملفاً."})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"reply": "الملف فارغ."})
        
        session_id = request.form.get('session_id') or request.headers.get('X-Session-Id')
        if not session_id:
            session_id = str(uuid.uuid4())
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        result = analyze_file(file_path, file.filename)
        
        extracted_text = ""
        if result["success"]:
            extracted_text = result.get("text", "")
            file_type = result.get("type", "غير معروف")
            save_uploaded_file(filename, file.filename, file_type, os.path.getsize(file_path), extracted_text)
            
            if file_type.lower() in ['jpg','jpeg','png','gif','webp','bmp']:
                img_analysis = analyze_image_with_gemini(file_path, GEMINI_API_KEY)
                if img_analysis["success"]:
                    extracted_text += "\n[تحليل الصورة]: " + img_analysis["description"]
            
            save_knowledge(topic=f"ملف: {file.filename}", content=extracted_text[:3000], source=f"ملف {file_type}")
            
            memory_manager.add_to_memory(session_id, "user", f"[رفع ملف: {file.filename}]")
            memory_manager.add_to_memory(session_id, "assistant", f"تم تحليل ملف {file.filename}")
            
            reply = f"✅ تم تحليل الملف بنجاح.\n📁 {file.filename}\n📝 {file_type}\n\n📄 المحتوى المستخلص:\n{extracted_text[:2000]}"
            if len(extracted_text) > 2000:
                reply += "\n\n...(المحتوى طويل، تم حفظه في ذاكرتي)"
        else:
            reply = f"❌ فشل التحليل: {result.get('error')}"
        
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({"reply": reply, "session_id": session_id})
        
    except Exception as e:
        return jsonify({"reply": f"خطأ في رفع الملف: {str(e)}"}, 500)

@app.route("/clear", methods=["POST"])
def clear():
    """مسح الذاكرة"""
    try:
        data = request.get_json(force=True) or {}
        session_id = data.get('session_id')
        
        if session_id:
            memory_manager.clear_memory(session_id)
            return jsonify({"status": "cleared", "session_id": session_id, "message": "تم مسح ذاكرة هذه الجلسة"})
        else:
            return jsonify({"status": "error", "message": "لم يتم تحديد الجلسة"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}, 500)

@app.route("/status", methods=["GET"])
def status():
    """حالة النظام"""
    from memory import get_connection
    conn = get_connection()
    conv_count = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    know_count = conn.execute("SELECT COUNT(*) FROM knowledge").fetchone()[0]
    conn.close()
    return jsonify({
        "conversations": conv_count,
        "knowledge_items": know_count,
        "name": ENTITY_NAME,
        "memory_active": True,
        "providers": {
            "groq": bool(GROQ_API_KEY),
            "gemini": bool(GEMINI_API_KEY),
            "gateway": bool(GATEWAY_URL)
        }
    })

@app.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    """استرجاع تاريخ المحادثة لجلسة محددة"""
    history = memory_manager.get_conversation_with_memory(session_id, 100)
    return jsonify({"session_id": session_id, "history": history, "count": len(history)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
