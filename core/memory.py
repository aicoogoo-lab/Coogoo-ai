# core/memory.py
# ذاكرة "سماء" الجبارة - تدعم الجلسات المتعددة والذاكرة الدائمة

import sqlite3
import os
import json
from datetime import datetime

# قاعدة البيانات ستُحفظ في ملف محلي داخل مجلد core
DB_PATH = os.path.join(os.path.dirname(__file__), 'sky_memory.db')

def get_connection():
    """إنشاء اتصال بقاعدة البيانات."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """تهيئة جداول الذاكرة. تستدعى مرة واحدة عند بدء التطبيق."""
    conn = get_connection()
    cursor = conn.cursor()

    # جدول المحادثات (يدعم session_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            session_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول المعرفة المستخلصة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            content TEXT NOT NULL,
            source TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول الطلبات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            title TEXT,
            description TEXT,
            status TEXT DEFAULT 'pending',
            requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            fulfilled_at DATETIME
        )
    ''')

    # جدول خاص بالسيد
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

    # تهيئة جداول الوسائط والروابط
    init_media_tables()

    # التأكد من وجود عمود session_id في الإصدارات القديمة
    _ensure_session_id_column()

def _ensure_session_id_column():
    """إضافة عمود session_id إذا لم يكن موجوداً (للتوافق مع قواعد البيانات القديمة)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('ALTER TABLE conversations ADD COLUMN session_id TEXT')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        pass  # العمود موجود مسبقاً

# --- جداول الملفات والروابط ---
def init_media_tables():
    """تهيئة جداول الملفات والروابط."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            file_type TEXT,
            size INTEGER,
            extracted_text TEXT,
            analysis TEXT,
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            extracted_text TEXT,
            analysis TEXT,
            fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_uploaded_file(filename, original_name, file_type, size, extracted_text="", analysis=""):
    """حفظ معلومات ملف مرفوع."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO files (filename, original_name, file_type, size, extracted_text, analysis) VALUES (?, ?, ?, ?, ?, ?)',
        (filename, original_name, file_type, size, extracted_text, analysis)
    )
    conn.commit()
    conn.close()

def save_url_analysis(url, title, extracted_text, analysis=""):
    """حفظ تحليل رابط."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO urls (url, title, extracted_text, analysis) VALUES (?, ?, ?, ?)',
        (url, title, extracted_text, analysis)
    )
    conn.commit()
    conn.close()

# --- دوال الحفظ (محدثة لدعم session_id) ---

def save_conversation(role, content, session_id=None):
    """حفظ رسالة مع إمكانية تحديد معرف الجلسة."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO conversations (role, content, session_id) VALUES (?, ?, ?)',
        (role, content, session_id)
    )
    conn.commit()
    conn.close()

def save_knowledge(topic, content, source="محادثة"):
    """حفظ معرفة جديدة تعلمتها سماء."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM knowledge WHERE topic = ?', (topic,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute(
            'UPDATE knowledge SET content = ?, source = ?, updated_at = CURRENT_TIMESTAMP WHERE topic = ?',
            (content, source, topic)
        )
    else:
        cursor.execute(
            'INSERT INTO knowledge (topic, content, source) VALUES (?, ?, ?)',
            (topic, content, source)
        )
    conn.commit()
    conn.close()

def save_request(type_, title, description):
    """حفظ طلب من سماء لسيدها."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO requests (type, title, description) VALUES (?, ?, ?)',
        (type_, title, description)
    )
    conn.commit()
    conn.close()

def save_master_info(key, value):
    """حفظ معلومة عن السيد."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR REPLACE INTO master_profile (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
        (key, value)
    )
    conn.commit()
    conn.close()

# --- دوال الاسترجاع (محدثة لدعم session_id) ---

def get_recent_conversations(limit=20, session_id=None):
    """استرجاع آخر المحادثات (يمكن تصفيتها حسب الجلسة)."""
    conn = get_connection()
    cursor = conn.cursor()
    if session_id:
        cursor.execute(
            'SELECT role, content FROM conversations WHERE session_id = ? ORDER BY id DESC LIMIT ?',
            (session_id, limit)
        )
    else:
        cursor.execute(
            'SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?',
            (limit,)
        )
    rows = cursor.fetchall()
    conn.close()
    return list(reversed([dict(row) for row in rows]))

def get_full_conversation_context(session_id=None, limit=50):
    """استرجاع السياق الكامل للمحادثة مع إمكانية التصفية حسب الجلسة."""
    conn = get_connection()
    cursor = conn.cursor()
    if session_id:
        cursor.execute(
            'SELECT role, content, timestamp FROM conversations WHERE session_id = ? ORDER BY id DESC LIMIT ?',
            (session_id, limit)
        )
    else:
        cursor.execute(
            'SELECT role, content, timestamp FROM conversations ORDER BY id DESC LIMIT ?',
            (limit,)
        )
    rows = cursor.fetchall()
    conn.close()
    return list(reversed([dict(row) for row in rows]))

def get_conversation_by_session(session_id, limit=50):
    """استرجاع محادثات جلسة محددة (اختصار)."""
    return get_full_conversation_context(session_id, limit)

def get_knowledge(topic=None):
    """استرجاع المعرفة."""
    conn = get_connection()
    cursor = conn.cursor()
    if topic:
        cursor.execute('SELECT * FROM knowledge WHERE topic = ?', (topic,))
    else:
        cursor.execute('SELECT * FROM knowledge ORDER BY updated_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_pending_requests():
    """استرجاع الطلبات المعلقة."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests WHERE status = "pending" ORDER BY requested_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_master_profile():
    """استرجاع كل معلومات السيد."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM master_profile ORDER BY updated_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return {row['key']: row['value'] for row in rows}

def get_all_knowledge_text():
    """تجميع كل المعرفة في نص واحد."""
    knowledge_items = get_knowledge()
    if not knowledge_items:
        return ""
    text = "معرفتي الحالية:\n"
    for item in knowledge_items:
        text += f"- {item['topic']}: {item['content']}\n"
    return text

def get_master_profile_text():
    """تجميع معلومات السيد في نص واحد."""
    profile = get_master_profile()
    if not profile:
        return ""
    text = "ما أعرفه عن سيدي:\n"
    for key, value in profile.items():
        text += f"- {key}: {value}\n"
    return text

# --- دوال المسح ---

def clear_conversation_history(session_id=None):
    """مسح تاريخ المحادثات لجلسة محددة أو كلها."""
    conn = get_connection()
    cursor = conn.cursor()
    if session_id:
        cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
    else:
        cursor.execute('DELETE FROM conversations')
    conn.commit()
    conn.close()

# --- التهيئة التلقائية ---
init_db()
