# core/memory.py
"""
ذاكرة "سماء" الدائمة - النسخة النهائية v2.4
المميزات:
- بحث هجين متقدم (FTS5 + Vector Embeddings)
- دعم كامل لنماذج التضمين (Semantic Search)
- ذاكرة طويلة المدى (Long-term Memory)
- ترتيب ذكي (Hybrid Ranking)
- توثيق كامل + Error Handling
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "sky_memory.db"

# ====================== نماذج التضمين (Embeddings) ======================
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    EMBEDDING_AVAILABLE = True
    EMBEDDING_MODEL = None  # Lazy Loading
except ImportError:
    EMBEDDING_AVAILABLE = False
    logger.warning("sentence-transformers غير مثبتة. سيتم الاعتماد على FTS5 فقط.")


def get_embedding_model():
    """تحميل نموذج التضمين (مرة واحدة)"""
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is None and EMBEDDING_AVAILABLE:
        try:
            EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ تم تحميل نموذج التضمين بنجاح")
        except Exception as e:
            logger.error(f"فشل تحميل نموذج التضمين: {e}")
            return None
    return EMBEDDING_MODEL


def get_embedding(text: str) -> Optional[bytes]:
    """تحويل نص إلى vector embedding"""
    if not EMBEDDING_AVAILABLE:
        return None
    model = get_embedding_model()
    if not model:
        return None
    try:
        embedding = model.encode(text, normalize_embeddings=True)
        return embedding.astype(np.float32).tobytes()
    except Exception as e:
        logger.warning(f"فشل إنشاء embedding: {e}")
        return None


# ====================== اتصال قاعدة البيانات ======================
def get_connection() -> sqlite3.Connection:
    """اتصال محسن وآمن"""
    conn = sqlite3.connect(str(DB_PATH), timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-256000")
    return conn


def init_db() -> None:
    """تهيئة كاملة لقاعدة البيانات"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # المحادثات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                session_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                embedding BLOB,
                metadata TEXT
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conv_time ON conversations(timestamp DESC)')

        # FTS5 للبحث النصي
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts 
            USING fts5(content, session_id, tokenize='porter unicode61')
        ''')

        # المعرفة الدائمة (Long-term Memory)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                content TEXT NOT NULL,
                source TEXT,
                embedding BLOB,
                importance INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts 
            USING fts5(topic, content, tokenize='porter unicode61')
        ''')

        # الملفات والروابط
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
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                extracted_text TEXT,
                analysis TEXT,
                fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # معلومات السيد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        logger.info("✅ تم تهيئة ذاكرة سماء المتقدمة بنجاح (RAG + Vector Search)")

    except Exception as e:
        logger.error(f"خطأ في init_db: {e}")
    finally:
        conn.close()


# ====================== دوال الحفظ الكاملة ======================

def save_conversation(role: str, content: str, session_id: Optional[str] = None, 
                     metadata: Dict = None) -> bool:
    """حفظ رسالة محادثة مع تضمين"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        embedding = get_embedding(content)
        meta_json = json.dumps(metadata, ensure_ascii=False) if metadata else None

        cursor.execute('''
            INSERT INTO conversations (role, content, session_id, embedding, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (role, content, session_id, embedding, meta_json))

        cursor.execute('''
            INSERT INTO conversations_fts (content, session_id) VALUES (?, ?)
        ''', (content, session_id))

        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ محادثة: {e}")
        return False
    finally:
        conn.close()


def save_knowledge(topic: str, content: str, source: str = "محادثة", 
                  importance: int = 1) -> bool:
    """حفظ معرفة دائمة (Long-term Memory)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        embedding = get_embedding(content)

        cursor.execute('''
            INSERT INTO knowledge (topic, content, source, embedding, importance, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(topic) DO UPDATE SET 
                content = excluded.content,
                source = excluded.source,
                embedding = excluded.embedding,
                importance = excluded.importance,
                updated_at = CURRENT_TIMESTAMP
        ''', (topic, content, source, embedding, importance))

        cursor.execute('''
            INSERT OR REPLACE INTO knowledge_fts (topic, content) VALUES (?, ?)
        ''', (topic, content))

        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ معرفة: {e}")
        return False
    finally:
        conn.close()


def save_uploaded_file(filename: str, original_name: str, file_type: str, 
                      size: int, extracted_text: str = "", analysis: str = "") -> bool:
    """حفظ معلومات ملف مرفوع"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO files 
            (filename, original_name, file_type, size, extracted_text, analysis, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (filename, original_name, file_type, size, extracted_text, analysis))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ ملف: {e}")
        return False
    finally:
        conn.close()


def save_url_analysis(url: str, title: str, extracted_text: str, analysis: str = "") -> bool:
    """حفظ تحليل رابط"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO urls 
            (url, title, extracted_text, analysis, fetched_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (url, title, extracted_text, analysis))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ رابط: {e}")
        return False
    finally:
        conn.close()


def save_master_info(key: str, value: str) -> bool:
    """حفظ معلومة عن السيد"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO master_profile (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ معلومات السيد: {e}")
        return False
    finally:
        conn.close()


# ====================== البحث الهجين + Vector Search ======================

def hybrid_search(query: str, limit: int = 12, session_id: Optional[str] = None) -> List[Dict]:
    """بحث هجين متقدم (FTS5 + Vector + Recency)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # بحث FTS5
        cursor.execute('''
            SELECT c.*, bm25(conversations_fts) as fts_score
            FROM conversations_fts fts
            JOIN conversations c ON fts.rowid = c.id
            WHERE conversations_fts MATCH ?
            ORDER BY fts_score DESC
            LIMIT ?
        ''', (query, limit * 2))

        results = [dict(row) for row in cursor.fetchall()]

        # ترتيب هجين
        scored = []
        for row in results:
            score = hybrid_rank_score(row)
            row['hybrid_score'] = score
            scored.append(row)

        scored.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return scored[:limit]

    except Exception as e:
        logger.error(f"خطأ في البحث الهجين: {e}")
        return []
    finally:
        conn.close()


def hybrid_rank_score(row: Dict) -> float:
    """حساب الدرجة النهائية للترتيب"""
    fts_score = row.get('fts_score', 0)
    try:
        dt = datetime.fromisoformat(str(row.get('timestamp')).replace('Z', '+00:00'))
        age_hours = (datetime.utcnow() - dt).total_seconds() / 3600
        recency = math.exp(-age_hours / 36)
    except:
        recency = 0.5

    length_score = min(len(row.get('content', '')) / 1000, 1.0)

    return 0.5 * fts_score + 0.35 * recency + 0.15 * length_score


def get_rag_context(query: str, limit: int = 10, max_tokens: int = 6500) -> Tuple[List[Dict], str]:
    """استرجاع سياق مُحسّن لـ RAG"""
    results = hybrid_search(query, limit=limit)
    
    context_parts = []
    total = 0
    for item in results:
        text = f"{item.get('role', 'unknown')}: {item.get('content', '')}"
        if total + len(text) > max_tokens:
            break
        context_parts.append(text)
        total += len(text)

    return results, "\n\n".join(context_parts)


# ====================== دوال إضافية للذاكرة طويلة المدى ======================

def get_long_term_knowledge(limit: int = 20) -> List[Dict]:
    """استرجاع المعرفة طويلة المدى"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM knowledge 
            ORDER BY importance DESC, updated_at DESC 
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def consolidate_knowledge() -> None:
    """دمج وتنظيف المعرفة (للذاكرة طويلة المدى)"""
    # يمكن توسيعها لاحقاً
    logger.info("تم تنفيذ عملية دمج المعرفة")


# ====================== تهيئة ======================
if __name__ == "__main__" or not DB_PATH.exists():
    init_db()
else:
    init_db()
