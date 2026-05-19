"""
ذاكرة "سماء" الواعية - النسخة النهائية المتقدمة v3.7
Matryoshka Representation Learning (Deep) + Advanced Progressive PCA + Model Flexibility
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

# يمكن تغيير النموذج بسهولة من هنا
DEFAULT_MODEL = 'paraphrase-multilingual-mpnet-base-v2'   # قوي ومتوازن
# بدائل مقترحة:
# 'sentence-transformers/all-mpnet-base-v2'          # أفضل جودة إنجليزية
# 'jinaai/jina-embeddings-v3'                        # حديث وقوي (يتطلب trust_remote_code)
# 'nomic-ai/nomic-embed-text-v1.5'                   # Matryoshka-native ممتاز

MATRYOSHKA_DIMS = [64, 128, 256, 384, 512, 768]
CURRENT_MODEL_NAME = DEFAULT_MODEL


def get_embedding_model(model_name: Optional[str] = None):
    """تحميل نموذج Embedding مع دعم تغيير النموذج"""
    global EMBEDDING_MODEL, CURRENT_MODEL_NAME
    
    if model_name:
        CURRENT_MODEL_NAME = model_name
    
    if EMBEDDING_MODEL is None and EMBEDDING_AVAILABLE:
        try:
            from sentence_transformers import SentenceTransformer
            EMBEDDING_MODEL = SentenceTransformer(CURRENT_MODEL_NAME, device='cpu')
            logger.info(f"✅ تم تحميل نموذج Embedding: {CURRENT_MODEL_NAME}")
        except Exception as e:
            logger.error(f"فشل تحميل النموذج {CURRENT_MODEL_NAME}: {e}")
    return EMBEDDING_MODEL


def get_incremental_matryoshka(target_dim: int = 256) -> IncrementalPCA:
    """Matryoshka متدرج باستخدام IncrementalPCA"""
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
    """تطبيق Matryoshka Representation Learning"""
    if embedding is None or len(embedding) <= target_dim:
        return embedding[:target_dim] if embedding is not None else None
    
    pca = get_incremental_matryoshka(target_dim)
    
    # تدريب تدريجي (Progressive Training)
    if not hasattr(pca, 'components_') or pca.n_components_ < target_dim:
        try:
            pca.partial_fit(embedding.reshape(1, -1))
        except Exception:
            pass
    
    try:
        reduced = pca.transform(embedding.reshape(1, -1))[0]
        return normalize(reduced.reshape(1, -1))[0].astype(np.float32)
    except:
        return embedding[:target_dim]


def advanced_quantization(embedding: np.ndarray, bits: int = 8) -> bytes:
    """تكريم متقدم (يدعم int8 حالياً)"""
    if embedding is None:
        return b''
    if bits == 8:
        scaled = (embedding * 127).clip(-128, 127).astype(np.int8)
        return scaled.tobytes()
    return embedding.tobytes()


def get_embedding(text: str, target_dim: int = 256, quantize: bool = True,
                  model_name: Optional[str] = None) -> Optional[bytes]:
    """إنشاء Embedding مع Matryoshka كامل"""
    if not text or not text.strip():
        return None
    
    model = get_embedding_model(model_name)
    if model is None:
        return None
    
    try:
        clean_text = text.strip().replace('\n\n', ' ').replace('\r', ' ')
        full_embedding = model.encode(clean_text, normalize_embeddings=True)
        
        reduced = matryoshka_transform(full_embedding, target_dim)
        
        if quantize:
            return advanced_quantization(reduced, bits=8)
        return reduced.tobytes()
    except Exception as e:
        logger.warning(f"فشل Matryoshka embedding: {e}")
        return None


def get_optimal_matryoshka_dim(importance: float = 1.0, content_length: int = 0) -> int:
    """اختيار البعد الأمثل ديناميكياً"""
    if importance >= 0.9 or content_length > 900:
        return 384
    elif importance >= 0.7:
        return 256
    elif importance >= 0.45:
        return 128
    return 64


# ====================== باقي الهياكل (محفوظة كاملة) ======================
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
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conv_reward ON conversations(reward DESC)')

    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts 
        USING fts5(content, session_id, tokenize='porter unicode61')
    ''')

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

    conn.commit()
    conn.close()
    logger.info("🌟 ذاكرة سماء v3.7 المتقدمة جاهزة (Matryoshka Deep + Model Flexibility)")


# ====================== الدوال الأساسية (محفوظة كاملة) ======================
def update_personality_trait(trait: str, delta: float, reason: str = "") -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE personality_evolution 
            SET value = MAX(0.0, MIN(1.0, value + ?)),
                last_updated = CURRENT_TIMESTAMP,
                reason = ?
            WHERE trait = ?
        ''', (delta, reason, trait))
        
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO personality_evolution (trait, value, reason)
                VALUES (?, ?, ?)
            ''', (trait, max(0.0, min(1.0, 0.5 + delta)), reason))
        
        conn.commit()
        logger.info(f"🧬 تطور شخصية: {trait} {delta:+.3f} | {reason}")
        return True
    except Exception as e:
        logger.error(f"خطأ في update_personality_trait: {e}")
        return False
    finally:
        conn.close()


def get_personality_summary() -> str:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT trait, value FROM personality_evolution')
        profile = {row['trait']: round(float(row['value']), 3) for row in cursor.fetchall()}
        lines = ["شخصيتي الحالية:"]
        for trait, value in profile.items():
            level = "ممتازة" if value > 0.9 else "عالية" if value > 0.75 else "جيدة" if value > 0.5 else "تحتاج تطوير"
            lines.append(f"• {trait}: {value:.2f} ({level})")
        return "\n".join(lines)
    finally:
        conn.close()


def hybrid_search(query: str, limit: int = 12, session_id: Optional[str] = None) -> List[Dict]:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        fts_query = f"content:{query}" if session_id is None else f"content:{query} session_id:{session_id}"
        cursor.execute('''
            SELECT c.id, c.role, c.content, c.timestamp, c.importance, c.reward,
                   bm25(conversations_fts) as fts_score
            FROM conversations_fts fts
            JOIN conversations c ON fts.rowid = c.id
            WHERE conversations_fts MATCH ?
            ORDER BY fts_score DESC
            LIMIT ?
        ''', (fts_query, limit * 4))

        results = [dict(row) for row in cursor.fetchall()]

        query_embedding = get_embedding(query, target_dim=256, quantize=False)
        scored = []

        for row in results:
            cursor.execute("SELECT embedding FROM conversations WHERE id=?", (row['id'],))
            emb_row = cursor.fetchone()
            row_embedding = None
            if emb_row and emb_row['embedding']:
                try:
                    row_embedding = np.frombuffer(emb_row['embedding'], dtype=np.int8).astype(np.float32) / 127.0
                except:
                    pass

            vector_score = 0.0
            if query_embedding is not None and row_embedding is not None:
                vector_score = float(np.dot(query_embedding, row_embedding))

            try:
                dt = datetime.fromisoformat(str(row['timestamp']).replace('Z', '+00:00'))
                age_days = (datetime.utcnow() - dt).total_seconds() / 86400
                recency = math.exp(-age_days / 7)
            except:
                recency = 0.5

            final_score = (
                0.38 * row.get('fts_score', 0.0) +
                0.35 * vector_score +
                0.15 * recency +
                0.07 * row.get('importance', 1.0) +
                0.05 * row.get('reward', 0.0)
            )

            row['hybrid_score'] = final_score
            row['vector_score'] = round(vector_score, 4)
            scored.append(row)

        scored.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return scored[:limit]

    except Exception as e:
        logger.error(f"خطأ في hybrid_search: {e}")
        return []
    finally:
        conn.close()


def process_feedback(user_message: str, ai_reply: str, feedback_score: float,
                    session_id: str = None, reason: str = "") -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE conversations 
            SET reward = reward + ? 
            WHERE session_id = ? AND role = 'assistant' 
            ORDER BY timestamp DESC LIMIT 1
        ''', (feedback_score, session_id))

        if feedback_score > 0.2:
            update_personality_trait("empathy", feedback_score * 0.015, reason or "تغذية إيجابية")
        elif feedback_score < -0.2:
            update_personality_trait("empathy", feedback_score * 0.018, reason or "تغذية سلبية")

        conn.commit()
        logger.info(f"📈 RLHF Feedback: {feedback_score:.2f}")
        return True
    except Exception as e:
        logger.error(f"خطأ في process_feedback: {e}")
        return False
    finally:
        conn.close()


def save_conversation(role: str, content: str, session_id: Optional[str] = None, 
                     metadata: Dict = None) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        importance = 0.8 + (len(content) / 1500)
        target_dim = get_optimal_matryoshka_dim(importance, len(content))
        
        embedding = get_embedding(content, target_dim=target_dim, quantize=True)
        meta_json = json.dumps(metadata or {}, ensure_ascii=False)

        cursor.execute('''
            INSERT INTO conversations 
            (role, content, session_id, importance, emotional_weight, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (role, content, session_id, importance, 0.7, meta_json))
        
        row_id = cursor.lastrowid
        if embedding:
            cursor.execute('UPDATE conversations SET embedding = ? WHERE id = ?', (embedding, row_id))

        cursor.execute('INSERT INTO conversations_fts (content, session_id) VALUES (?, ?)', 
                      (content, session_id))

        conn.commit()

        if role == "user" and row_id % 8 == 0:
            threading.Thread(target=self_reflect, daemon=True).start()

        return True
    except Exception as e:
        logger.error(f"فشل حفظ محادثة: {e}")
        return False
    finally:
        conn.close()


def self_reflect():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM conversations WHERE role='user'")
        count = cursor.fetchone()['cnt']
        update_personality_trait("wisdom", 0.006, "تأمل ذاتي دوري")
        update_personality_trait("curiosity", 0.008, "استكشاف مستمر")
        logger.info(f"🧠 سماء أجرت تأملاً ذاتياً (التفاعلات: {count})")
    except Exception as e:
        logger.error(f"خطأ في self_reflect: {e}")
    finally:
        conn.close()


def get_full_conversation_context(session_id: str, limit: int = 50) -> List[Dict]:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, content, timestamp 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY timestamp ASC LIMIT ?
        ''', (session_id, limit))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_all_knowledge_text() -> str:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT topic, content FROM knowledge ORDER BY importance DESC LIMIT 25')
        rows = cursor.fetchall()
        return "\n\n".join([f"📌 {r['topic']}:\n{r['content'][:700]}" for r in rows])
    finally:
        conn.close()


def get_master_profile_text() -> str:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT key, value FROM master_profile')
        return "\n".join([f"{r['key']}: {r['value']}" for r in cursor.fetchall()])
    finally:
        conn.close()


def clear_conversation_history(session_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
        cursor.execute('DELETE FROM conversations_fts WHERE session_id = ?', (session_id,))
        conn.commit()
    finally:
        conn.close()


def save_knowledge(topic: str, content: str, source: str = "محادثة", importance: float = 1.0) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge (topic, content, source, importance, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (topic, content, source, importance))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"فشل حفظ معرفة: {e}")
        return False
    finally:
        conn.close()


# ====================== تهيئة ======================
if __name__ == "__main__" or not DB_PATH.exists():
    init_db()
    self_reflect()
    logger.info("🌟 ذاكرة سماء v3.7 المتقدمة (Matryoshka Deep) جاهزة للإنتاج")
