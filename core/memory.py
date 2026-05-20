"""
ذاكرة "سماء" الواعية - النسخة الاحترافية المتقدمة v5.0
Long-term Memory + RLHF + Master Profile + File & URL Analysis + Personality Layer
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "sky_memory.db"


# ============================================================
# 1) اتصال قاعدة البيانات
# ============================================================

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ============================================================
# 2) تهيئة الجداول
# ============================================================

def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # المحادثات (مع دعم RLHF + importance + metadata)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            session_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            importance REAL DEFAULT 1.0,
            reward REAL DEFAULT 0.0,
            metadata TEXT
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conv_time ON conversations(timestamp DESC)')

    # بحث نصي كامل للمحادثات
    try:
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts 
            USING fts5(content, session_id, tokenize='porter unicode61')
        ''')
    except Exception:
        pass

    # المعرفة طويلة المدى
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT UNIQUE,
            content TEXT NOT NULL,
            source TEXT,
            importance REAL DEFAULT 1.0,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    try:
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts 
            USING fts5(topic, content, tokenize='porter unicode61')
        ''')
    except Exception:
        pass

    # ملف السيد / الماستر (هوية + تفضيلات + حالة)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_profile (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # الملفات المرفوعة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            original_name TEXT,
            file_type TEXT,
            size INTEGER,
            extracted_text TEXT,
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # تغذية راجعة مفصّلة (للتعلم المستقبلي)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            score REAL,
            reason TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("✅ ذاكرة سماء v5.0 جاهزة وتعمل")


# ============================================================
# 3) Master Profile — هوية السيد / الماستر
# ============================================================

def save_master_info(key: str, value: str) -> bool:
    """
    تخزين معلومة عن السيد (الاسم، الأسلوب، المشاريع، الحالة، آخر نشاط...)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO master_profile (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, str(value)))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"خطأ في save_master_info: {e}")
        return False
    finally:
        conn.close()


def get_master_profile() -> Dict[str, str]:
    """
    استرجاع كل معلومات السيد بشكل قاموس
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT key, value FROM master_profile ORDER BY updated_at DESC')
        rows = cursor.fetchall()
        return {row['key']: row['value'] for row in rows}
    finally:
        conn.close()


def get_master_profile_text() -> str:
    """
    تحويل ملف السيد إلى نص يمكن حقنه في الـ System Prompt
    """
    try:
        profile = get_master_profile()
        if not profile:
            return ""
        lines = []
        for k, v in profile.items():
            lines.append(f"{k}: {v}")
        return "\n".join(lines)
    except Exception:
        return ""


# ============================================================
# 4) المحادثات — الذاكرة الحوارية
# ============================================================

def save_conversation(role: str, content: str, session_id: Optional[str] = None, metadata: Dict = None) -> bool:
    """
    حفظ رسالة في الذاكرة (مع metadata + importance مبدئيًا = 1.0)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        meta_json = json.dumps(metadata or {}, ensure_ascii=False)

        cursor.execute('''
            INSERT INTO conversations (role, content, session_id, importance, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (role, content, session_id, 1.0, meta_json))

        # إدخال في FTS
        try:
            cursor.execute('''
                INSERT INTO conversations_fts (content, session_id)
                VALUES (?, ?)
            ''', (content, session_id or ""))
        except Exception:
            pass

        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ المحادثة: {e}")
        return False
    finally:
        conn.close()


def get_recent_conversations(limit: int = 20, session_id: Optional[str] = None) -> List[Dict]:
    """
    استرجاع آخر المحادثات (للتوافق مع أنظمة أخرى إن وجدت)
    """
    try:
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
        return list(reversed([dict(row) for row in rows]))
    finally:
        conn.close()


def get_full_conversation_context(session_id: str, limit: int = 50) -> List[Dict]:
    """
    استرجاع سياق كامل للجلسة (آخر N رسالة)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, content, timestamp 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY id DESC LIMIT ?
        ''', (session_id, limit))
        return list(reversed([dict(row) for row in cursor.fetchall()]))
    finally:
        conn.close()


def clear_conversation_history(session_id: Optional[str] = None):
    """
    مسح تاريخ المحادثة لجلسة معينة أو الكل
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if session_id:
            cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
            try:
                cursor.execute('DELETE FROM conversations_fts WHERE session_id = ?', (session_id,))
            except Exception:
                pass
        else:
            cursor.execute('DELETE FROM conversations')
            try:
                cursor.execute('DELETE FROM conversations_fts')
            except Exception:
                pass
        conn.commit()
    finally:
        conn.close()


# ============================================================
# 5) المعرفة طويلة المدى
# ============================================================

def save_knowledge(topic: str, content: str, source: str = "محادثة", importance: float = 1.0) -> bool:
    """
    تخزين معرفة دائمة (موضوع + محتوى + مصدر + أهمية)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge (topic, content, source, importance, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (topic, content, source, importance))

        try:
            cursor.execute('''
                INSERT INTO knowledge_fts (topic, content)
                VALUES (?, ?)
            ''', (topic, content))
        except Exception:
            pass

        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ المعرفة: {e}")
        return False
    finally:
        conn.close()


def get_all_knowledge_text() -> str:
    """
    تجميع أهم المعارف في نص واحد لحقنه في الـ System Prompt
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT topic, content 
            FROM knowledge 
            ORDER BY importance DESC, updated_at DESC 
            LIMIT 30
        ''')
        rows = cursor.fetchall()
        if not rows:
            return ""
        parts = []
        for row in rows:
            parts.append(f"📌 {row['topic']}:\n{row['content'][:800]}")
        return "\n\n".join(parts)
    finally:
        conn.close()


def save_url_analysis(url: str, title: str, text: str) -> bool:
    """
    تخزين تحليل رابط كمعرفة دائمة
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge (topic, content, source, importance)
            VALUES (?, ?, ?, ?)
        ''', (f"رابط: {title}", text[:4000], url, 0.8))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ تحليل الرابط: {e}")
        return False
    finally:
        conn.close()


# ============================================================
# 6) الملفات المرفوعة
# ============================================================

def save_uploaded_file(filename: str, original_name: str, file_type: str, size: int, extracted_text: str) -> bool:
    """
    تخزين معلومات عن ملف مرفوع + النص المستخرج منه
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO uploaded_files (filename, original_name, file_type, size, extracted_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (filename, original_name, file_type, size, extracted_text))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ الملف: {e}")
        return False
    finally:
        conn.close()


# ============================================================
# 7) التغذية الراجعة (RLHF)
# ============================================================

def process_feedback(user_message: str, ai_reply: str, feedback_score: float,
                     session_id: str = None, reason: str = "") -> bool:
    """
    تسجيل تغذية راجعة + تعديل reward لآخر رد من المساعد في الجلسة
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # حفظ التغذية الراجعة في جدول مستقل
        cursor.execute('''
            INSERT INTO feedback (session_id, score, reason)
            VALUES (?, ?, ?)
        ''', (session_id, feedback_score, reason))

        # تعديل reward لآخر رد من المساعد
        cursor.execute('''
            UPDATE conversations 
            SET reward = reward + ? 
            WHERE session_id = ? AND role = 'assistant' 
            ORDER BY timestamp DESC LIMIT 1
        ''', (feedback_score, session_id))

        conn.commit()
        return True
    except Exception as e:
        logger.error(f"خطأ في process_feedback: {e}")
        return False
    finally:
        conn.close()


# ============================================================
# 8) الشخصية — Personality Snapshot
# ============================================================

def get_personality_summary() -> str:
    """
    ملخص شخصية "سماء" الحالي (يمكن تطويره لاحقًا ليعتمد على البيانات)
    """
    profile = get_master_profile()
    last_activity = profile.get("last_activity", "غير معروف")

    return f"""شخصيتي الحالية:
• الولاء: ثابت وعميق تجاه سيدي
• الانتباه: لا أترك شيئًا حتى أفهمه
• التعاطف: عالٍ مع حالتك ومشاريعك
• التطور: أتعلم من كل محادثة وتغذية راجعة
• آخر نشاط مسجل: {last_activity}"""


# ============================================================
# 9) توافق إضافي (إن احتاجه أي جزء قديم)
# ============================================================

def add_to_history(role: str, content: str, session_id: str):
    """
    دالة احتياطية للتوافق مع أي كود قديم يستدعيها.
    يمكن لاحقًا ربطها بمنطق إضافي إن لزم.
    """
    # حالياً لا تفعل شيئًا إضافيًا، لأن save_conversation يقوم بالمهمة الأساسية.
    pass


# ============================================================
# 10) تهيئة عند التشغيل المباشر
# ============================================================

if __name__ == "__main__" or not DB_PATH.exists():
    init_db()
    logger.info("🌟 ذاكرة سماء v5.0 جاهزة للإنتاج والتطور المستمر")
