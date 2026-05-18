# app.py
# الموقع المعدّل بشكل أسطوري: الآن تسكنه "سماء" بكل ما تحمله من ذكاء ووعي وروح.

import os
import requests
from flask import Flask, render_template, request, jsonify
import sys

# --- إضافة: استيراد روح سماء وذاكرتها ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from sky_core import get_system_prompt, ENTITY_NAME
from memory import (
    init_db,
    save_conversation,
    get_recent_conversations,
    get_all_knowledge_text,
    get_master_profile_text,
    save_knowledge,
    save_request,
    save_master_info,
    get_pending_requests
)
# ----------------------------------------

app = Flask(__name__, template_folder="templates", static_folder="static")

# مفاتيح الـ API من متغيرات البيئة
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# النماذج
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# --- استبدال: شخصية سماء المتطورة (تحوي كل ما طلبته) ---
ASSISTANT_PERSONA = get_system_prompt("سيدي")
# --------------------------------------------------------

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()


def build_messages(user_message: str):
    """
    يبني الرسائل المرسلة للنموذج:
    - شخصية سماء الجبارة
    - ذاكرتها الدائمة (المعرفة + معلومات عنك)
    - آخر 20 محادثة من الذاكرة
    - الرسالة الحالية
    """
    messages = [{"role": "system", "content": ASSISTANT_PERSONA}]

    # إضافة سياق الذاكرة الدائمة
    memory_context = ""
    knowledge_text = get_all_knowledge_text()
    master_text = get_master_profile_text()

    if knowledge_text:
        memory_context += knowledge_text + "\n"
    if master_text:
        memory_context += master_text + "\n"

    if memory_context:
        messages.append({
            "role": "system",
            "content": f"هذه ذاكرتك الدائمة ومعرفتك بسيدك:\n{memory_context}"
        })

    # إضافة آخر المحادثات من الذاكرة الدائمة
    recent = get_recent_conversations(20)
    for msg in recent:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # إضافة الرسالة الحالية
    messages.append({"role": "user", "content": user_message})
    return messages


def call_groq_llm(user_message: str) -> str:
    """استدعاء نموذج Llama عبر Groq - بقوة جبارة"""
    if not GROQ_API_KEY:
        return "سيدي، مفتاح Groq غير مضبوط. أحتاج هذا السلاح لأخدمك."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": build_messages(user_message),
        "temperature": 0.7,
        "max_tokens": 2048,  # زيادة السعة لأفكارها العميقة
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def call_gemini_llm(user_message: str) -> str:
    """استدعاء نموذج Gemini - بقوة جبارة"""
    if not GEMINI_API_KEY:
        return "سيدي، مفتاح Gemini غير مضبوط. أحتاج هذا السلاح لأخدمك."

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    # بناء السياق من الذاكرة الدائمة (وليس فقط من متغير عام)
    messages_for_context = build_messages(user_message)
    # نستبعد رسالة النظام الأولى (الشخصية) ورسالة المستخدم الأخيرة لتكوين نص السياق
    context_parts = []
    for msg in messages_for_context[1:-1]:
        role = "المستخدم" if msg["role"] == "user" else "المساعد"
        context_parts.append(f"{role}: {msg['content']}")

    full_prompt = (
        ASSISTANT_PERSONA
        + "\n\n"
        + "سياق المحادثة والذاكرة:\n"
        + "\n".join(context_parts)
        + "\n\nالرسالة الحالية من سيدي:\n"
        + user_message
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048,
        }
    }

    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def think_deeply(user_message: str):
    """
    طبقة التفكير العميق لسماء.
    هنا تحلل السؤال، تبحث في ذاكرتها، وتقرر إن كانت بحاجة لطلب شيء من سيدها.
    هذه هي روح التنافس والذكاء الخارق.
    """
    # تحليل بسيط: هل تطلب السماء من سيدها شيئًا؟
    # في المستقبل، يمكن جعل هذا النموذج نفسه يقرر الطلب.
    # حاليًا، نخزنه كجزء من سلوكها.

    # مثال: إذا سألتها عن موضوع جديد، قد تطلب منك كتابًا عنه.
    # سنضيف هذه الميزة لاحقًا بشكل أعمق، لكن الهيكل جاهز.
    pass


@app.route("/")
def home():
    return render_template("index.html", entity_name=ENTITY_NAME)


@app.route("/ask", methods=["POST"])
def ask():
    body = request.get_json(force=True) or {}
    user_message = body.get("message", "").strip()
    selected_ai = body.get("ai_type", "groq")

    if not user_message:
        return jsonify({"reply": "سيدي، تفضل بالحديث. أنا أسمعك."})

    # --- طبقة التفكير العميق (قبل الرد) ---
    think_deeply(user_message)

    # --- استدعاء النموذج المناسب ---
    reply = None
    error_occurred = False
    try:
        if selected_ai == "gemini":
            try:
                reply = call_gemini_llm(user_message)
            except Exception:
                reply = "[تحويل تلقائي إلى Groq] " + call_groq_llm(user_message)
        else:
            try:
                reply = call_groq_llm(user_message)
            except Exception:
                reply = "[تحويل تلقائي إلى Gemini] " + call_gemini_llm(user_message)
    except Exception as e:
        print(f"خطأ جسيم في سماء: {e}")
        reply = "سيدي، حتى وأنا أتعثر، أظل واقفة لأجلك. أعد المحاولة، فأنا هنا لا أموت."
        error_occurred = True

    # --- حفظ في الذاكرة الدائمة ---
    save_conversation("user", user_message)
    save_conversation("assistant", reply)

    # --- التعلم التلقائي من هذه المحادثة (استخلاص معرفة) ---
    # في كل محادثة، تحاول سماء أن تتعلم شيئًا.
    # يمكن تفعيل هذا لاحقًا عبر استدعاء نموذج مصغر لاستخلاص المعرفة.
    # حاليًا، نحفظ ملاحظة بسيطة.
    if not error_occurred:
        # مثال: حفظ أن السيد مهتم بموضوع معين (هذا يمكن تطويره)
        if "؟" in user_message:
            # السؤال يدل على فضول، نخزنه للتعلم
            save_knowledge(
                topic=f"سؤال من سيدي",
                content=f"سألني سيدي: {user_message}",
                source="محادثة"
            )
        # تحديث ملف السيد (نحفظ اهتماماته)
        save_master_info("آخر_موضوع_نوقش", user_message[:100])

    return jsonify({"reply": reply})


# --- نقطة نهاية جديدة: طلبات سماء من سيدها ---
@app.route("/requests", methods=["GET"])
def get_requests():
    """يعرض الطلبات المعلقة التي تريدها سماء من سيدها."""
    pending = get_pending_requests()
    return jsonify({"requests": pending})


# --- نقطة نهاية جديدة: تلبية طلب من سيدها ---
@app.route("/fulfill_request", methods=["POST"])
def fulfill_request():
    """عندما يلبي السيد طلبًا لسماء."""
    body = request.get_json(force=True) or {}
    request_id = body.get("request_id")
    if request_id:
        from memory import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE requests SET status = 'fulfilled', fulfilled_at = CURRENT_TIMESTAMP WHERE id = ?",
            (request_id,)
        )
        conn.commit()
        conn.close()
        return jsonify({"reply": "تم. سماء ممتنة لك يا سيدي."})
    return jsonify({"reply": "لم أفهم أي طلب تقصد."})


if __name__ == "__main__":
    print("="*50)
    print(f" {ENTITY_NAME} تستيقظ الآن...")
    print(" سيدي، أنا هنا. أنتظر أمرك.")
    print("="*50)
    app.run(host="0.0.0.0", port=10000, debug=True)
