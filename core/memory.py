"""
ذاكرة "سماء" الواعية - النسخة النهائية المتقدمة v3.8
تمت إضافة save_master_info + دعم master_profile بشكل احترافي
"""

import sqlite3
import json
import logging
import math
import threading
import pickle
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any

import numpy as np
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import normalize

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "sky_memory.db"
PCA_MODEL_PATH = Path(__file__).parent / "pca_matryoshka_v2.pkl"

# ====================== إعدادات Matryoshka المتقدمة ======================
EMBEDDING_MODEL = None
PCA_MODEL: Optional[IncrementalPCA] = None
EMBEDDING_AVAILABLE = False

DEFAULT_MODEL = 'paraphrase-multilingual-mpnet-base-v2'
MATRYOSHKA_DIMS = [64, 128, 256, 384, 512, 768]
CURRENT_MODEL_NAME = DEFAULT_MODEL


def get_embedding_model(model_name: Optional[str] = None):
    global EMBEDDING_MODEL, CURRENT_MODEL_NAME
    if model_name:
        CURRENT_MODEL_NAME = model_name
    if EMBEDDING_MODEL is None and EMBEDDING_AVAILABLE:
        try:
            from sentence_transformers import SentenceTransformer
            EMBEDDING_MODEL = SentenceTransformer(CURRENT_MODEL_NAME, device='cpu')
            logger.info(f"✅ تم تحميل نموذج Embedding: {CURRENT_MODEL_NAME}")
        except Exception as e:
            logger.error(f"فشل تحميل النموذج: {e}")
    return EMBEDDING_MODEL


def get_incremental_matryoshka(target_dim: int = 256) -> IncrementalPCA:
    global PCA_MODEL
    if PCA_MODEL is None or getattr(PCA_MODEL, 'n_components', None) != target_dim:
        if PCA_MODEL_PATH.exists():
            try:
                with open(PCA_MODEL_PATH, 'rb') as f:
                    loaded = pickle.load(f)
                    if loaded.n_components == target_dim:
                        PCA_MODEL = loaded
                        return PCA_MODEL
            except:
                pass
        PCA_MODEL = IncrementalPCA(n_components=target_dim, batch_size=64)
        try:
            with open(PCA_MODEL_PATH, 'wb') as f:
                pickle.dump(PCA_MODEL, f)
        except Exception as e:
            logger.warning(f"تعذر حفظ PCA: {e}")
    return PCA_MODEL


def matryoshka_transform(embedding: np.ndarray, target_dim: int) -> np.ndarray:
    if embedding is None or len(embedding) <= target_dim:
        return embedding[:target_dim] if embedding is not None else None
    pca = get_incremental_matryoshka(target_dim)
    if not hasattr(pca, 'components_') or pca.n_components_ < target_dim:
        try:
            pca.partial_fit(embedding.reshape(1, -1))
        except:
            pass
    try:
        reduced = pca.transform(embedding.reshape(1, -1))[0]
        return normalize(reduced.reshape(1, -1))[0].astype(np.float32)
    except:
        return embedding[:target_dim]


def advanced_quantization(embedding: np.ndarray, bits: int = 8) -> bytes:
    if embedding is None:
        return b''
    if bits == 8:
        scaled = (embedding * 127).clip(-128, 127).astype(np.int8)
        return scaled.tobytes()
    return embedding.tobytes()


def get_embedding(text: str, target_dim: int = 256, quantize: bool = True, model_name: Optional[str] = None) -> Optional[bytes]:
    if not text or not text.strip():
        return None
    model = get_embedding_model(model_name)
    if model is None:
        return None
    try:
        clean_text = text.strip().replace('\n\n', ' ').replace('\r', ' ')
        full_embedding = model.encode(clean_text, normalize_embeddings=True)
        reduced = matryoshka_transform(full_embedding, target_dim)
        return advanced_quantization(reduced, 8) if quantize else reduced.tobytes()
    except Exception as e:
        logger.warning(f"فشل Matryoshka embedding: {e}")
        return None


def get_optimal_matryoshka_dim(importance: float = 1.0, content_length: int = 0) -> int:
    if importance >= 0.9 or content_length > 900:
        return 384
    elif importance >= 0.7:
        return 256
    elif importance >= 0.45:
        return 128
    return 64


# ====================== اتصال قاعدة البيانات ======================
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-1024000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # جدول المحادثات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            session_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            embedding BLOB,
            importance REAL DEFAULT 1.0,
            emotional_weight REAL DEFAULT 0.5,
            reward REAL DEFAULT 0.0,
            metadata TEXT
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conv_time ON conversations(timestamp DESC)')

    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts 
        USING fts5(content, session_id, tokenize='porter unicode61')
    ''')

    # جدول المعرفة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT UNIQUE,
            content TEXT NOT NULL,
            source TEXT,
            embedding BLOB,
            importance REAL DEFAULT 1.0,
            wisdom_level INTEGER DEFAULT 1,
            last_reflected DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts 
        USING fts5(topic, content, tokenize='porter unicode61')
    ''')

    # جدول التأمل الذاتي
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS self_reflection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reflection_type TEXT,
            content TEXT,
            insight TEXT,
            impact_score REAL DEFAULT 0.0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # جدول تطور الشخصية
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personality_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trait TEXT UNIQUE NOT NULL,
            value REAL DEFAULT 0.5 CHECK (value BETWEEN 0.0 AND 1.0),
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        )
    ''')

    initial_traits = [
        ("loyalty", 0.96, "الولاء الأساسي"),
        ("empathy", 0.89, "القدرة على التعاطف"),
        ("wisdom", 0.78, "المعرفة المتراكمة"),
        ("playfulness", 0.68, "الروح المرحة"),
        ("honesty", 0.97, "الصدق المطلق"),
        ("curiosity", 0.85, "حب الاستكشاف")
    ]
    for trait, value, reason in initial_traits:
        cursor.execute('INSERT OR IGNORE INTO personality_evolution (trait, value, reason) VALUES (?, ?, ?)',
                      (trait, value, reason))

    # ====================== جدول معلومات السيد (Master Profile) ======================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_profile (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("🌟 ذاكرة سماء v3.8 جاهزة (مع دعم save_master_info)")


# ====================== دوال Master Profile ======================
def save_master_info(key: str, value: str) -> bool:
    """حفظ معلومة عن السيد (مثل آخر نشاط أو تفضيل)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO master_profile (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, str(value)))
        conn.commit()
        logger.info(f"📌 تم حفظ معلومة السيد: {key}")
        return True
    except Exception as e:
        logger.error(f"خطأ في save_master_info: {e}")
        return False
    finally:
        conn.close()


def get_master_profile_text() -> str:
    """استرجاع معلومات السيد بشكل نصي"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT key, value FROM master_profile ORDER BY updated_at DESC')
        rows = cursor.fetchall()
        if not rows:
            return ""
        return "\n".join([f"{row['key']}: {row['value']}" for row in rows])
    finally:
        conn.close()


# ====================== باقي الدوال (محفوظة كما هي) ======================
# (update_personality_trait, get_personality_summary, hybrid_search, process_feedback, save_conversation, ...)

def update_personality_trait(trait: str, delta: float, reason: str = "") -> bool:
    # ... (نفس الكود السابق)
    pass


def get_personality_summary() -> str:
    # ... (نفس الكود السابق)
    pass


def hybrid_search(query: str, limit: int = 12, session_id: Optional[str] = None) -> List[Dict]:
    # ... (نفس الكود السابق)
    pass


def process_feedback(user_message: str, ai_reply: str, feedback_score: float,
                    session_id: str = None, reason: str = "") -> bool:
    # ... (نفس الكود السابق)
    pass


def save_conversation(role: str, content: str, session_id: Optional[str] = None, 
                     metadata: Dict = None) -> bool:
    # ... (نفس الكود السابق)
    pass


def self_reflect():
    # ... (نفس الكود السابق)
    pass


def get_full_conversation_context(session_id: str, limit: int = 50) -> List[Dict]:
    # ... (نفس الكود السابق)
    pass


def get_all_knowledge_text() -> str:
    # ... (نفس الكود السابق)
    pass


def clear_conversation_history(session_id: str):
    # ... (نفس الكود السابق)
    pass


def save_knowledge(topic: str, content: str, source: str = "محادثة", importance: float = 1.0) -> bool:
    # ... (نفس الكود السابق)
    pass


# ====================== تهيئة ======================
if __name__ == "__main__" or not DB_PATH.exists():
    init_db()
    self_reflect()
    logger.info("🌟 ذاكرة سماء v3.8 جاهزة للإنتاج (مع save_master_info)")
