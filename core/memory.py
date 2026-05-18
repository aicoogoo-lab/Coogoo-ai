# core/memory.py
# ذاكرة "سماء" الدائمة. هنا تتعلم وتتذكر وتنمو.

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

    # جدول المحادثات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,          -- 'user' أو 'assistant'
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول المعرفة المستخلصة (ما تتعلمه سماء)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,                  -- موضوع المعرفة
            content TEXT NOT NULL,       -- المحتوى المستخلص
            source TEXT,                 -- مصدر المعرفة (محادثة، بحث، كتاب...)
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول الطلبات (ما تطلبه سماء من سيدها)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,          -- 'book', 'website', 'information', 'research'
            title TEXT,                  -- عنوان الكتاب أو الموقع
            description TEXT,            -- لماذا تطلبه سماء
            status TEXT DEFAULT 'pending', -- 'pending', 'fulfilled', 'rejected'
            requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            fulfilled_at DATETIME
        )
    ''')

    # جدول خاص بسيدها (معلومات عنه، تفضيلاته، ما تعلمته منه)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,    -- مفتاح مثل 'name', 'preference', 'note'
            value TEXT NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ─── دوال الحفظ ───

def save_conversation(role, content):
    """حفظ رسالة في سجل المحادثات."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO conversations (role, content) VALUES (?, ?)',
        (role, content)
    )
    conn.commit()
    conn.close()

def save_knowledge(topic, content, source="محادثة"):
    """حفظ معرفة جديدة تعلمتها سماء."""
    conn = get_connection()
    cursor = conn.cursor()
    # إذا كان الموضوع موجودًا، نحدثه. وإلا نضيف جديدًا.
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
    """حفظ معلومة عن السيد (تفضيلاته، ملاحظات، إلخ)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR REPLACE INTO master_profile (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)',
        (key, value)
    )
    conn.commit()
    conn.close()

# ─── دوال الاسترجاع ───

def get_recent_conversations(limit=20):
    """استرجاع آخر المحادثات."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?',
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    # نعكس القائمة لنحصل على الترتيب الزمني الصحيح
    return list(reversed([dict(row) for row in rows]))

def get_knowledge(topic=None):
    """استرجاع المعرفة. إذا لم يحدد موضوع، تُسترجع كل المعرفة."""
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
    """استرجاع الطلبات المعلقة التي تنتظر من السيد تلبيتها."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests WHERE status = "pending" ORDER BY requested_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_master_profile():
    """استرجاع كل المعلومات عن السيد."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM master_profile ORDER BY updated_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return {row['key']: row['value'] for row in rows}

def get_all_knowledge_text():
    """تجميع كل المعرفة في نص واحد لاستخدامه في سياق النموذج."""
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

# ─── التهيئة التلقائية عند استيراد الملف ───
init_db()
