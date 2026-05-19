# أضف هذه الدوال إلى ملف core/memory.py الموجود

def get_full_conversation_context(session_id: str = None, limit: int = 50) -> list:
    """استرجاع السياق الكامل للمحادثة مع إمكانية التصفية حسب الجلسة"""
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

def get_conversation_by_session(session_id: str, limit: int = 50) -> list:
    """استرجاع محادثات جلسة محددة"""
    return get_full_conversation_context(session_id, limit)

def clear_conversation_history(session_id: str = None):
    """مسح تاريخ المحادثات لجلسة محددة أو كلها"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if session_id:
        cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
    else:
        cursor.execute('DELETE FROM conversations')
    
    conn.commit()
    conn.close()

# تحديث دالة save_conversation لدعم session_id
def save_conversation(role, content, session_id=None):
    """حفظ رسالة مع معرف الجلسة"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # إضافة عمود session_id إذا لم يكن موجوداً
    try:
        cursor.execute('ALTER TABLE conversations ADD COLUMN session_id TEXT')
    except:
        pass  # العمود موجود بالفعل
    
    cursor.execute(
        'INSERT INTO conversations (role, content, session_id, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)',
        (role, content, session_id)
    )
    conn.commit()
    conn.close()

# تحديث دالة get_recent_conversations لدعم session_id
def get_recent_conversations(limit=20, session_id=None):
    """استرجاع آخر المحادثات مع فلتر حسب الجلسة"""
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
