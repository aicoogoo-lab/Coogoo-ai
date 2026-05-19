// static/script.js - عقل سماء الأمامي الجبار

let currentSessionId = localStorage.getItem('sky_session_id') || null;
let selectedModel = localStorage.getItem('sky_selected_model') || 'groq';
const STORAGE_KEY = 'sky_messages_v4';

// عناصر DOM الأساسية
const messagesEl = document.getElementById('messages');
const chatContainer = document.getElementById('chat-container') || document.getElementById('chat-area');
const typingEl = document.getElementById('typing') || document.getElementById('typing-indicator');
const inputEl = document.getElementById('message-input') || document.getElementById('userInput');
const sendBtn = document.getElementById('send-btn') || document.getElementById('sendBtn');
const msgCountSpan = document.getElementById('msg-count');

// ============================================================================
// 1. إدارة الذاكرة المحلية
// ============================================================================

function saveMessagesToLocal() {
    const msgs = [];
    document.querySelectorAll('#messages .message, #messages .message-bubble').forEach(el => {
        const sender = el.classList.contains('user') ? 'user' : (el.dataset.sender || 'assistant');
        let text = el.querySelector('.text')?.innerText || el.innerText || '';
        text = text.replace(/[📋✅✓]|نسخ/gi, '').trim();
        if (text && !text.startsWith('…')) msgs.push({ sender, text });
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(msgs));
    if (currentSessionId) localStorage.setItem('sky_session_id', currentSessionId);
}

function restoreMessages() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) {
        addMessage('✨ مرحباً بك في سماء! أنا مساعدك الذكي المتصل بالعالم. أسألني أي شيء، وسأتذكر كل تفاصيل محادثتنا. ✨', 'assistant');
        return;
    }
    try {
        const msgs = JSON.parse(saved);
        messagesEl.innerHTML = '';
        msgs.forEach(m => addMessage(m.text, m.sender, false));
    } catch (e) {
        addMessage('✨ مرحباً بك في سماء! ✨', 'assistant');
    }
    updateMsgCount();
    if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
}

function updateMsgCount() {
    if (!msgCountSpan) return;
    const count = document.querySelectorAll('#messages .message, #messages .message-bubble').length;
    msgCountSpan.innerText = `${count} رسالة`;
}

// ============================================================================
// 2. إدارة الرسائل في الواجهة
// ============================================================================

function addMessage(text, sender = 'assistant', save = true) {
    const row = document.createElement('div');
    row.classList.add('message-row', sender);
    row.classList.add('message'); // للتوافق مع التنسيق القديم

    const bubble = document.createElement('div');
    bubble.classList.add('message-bubble', sender);
    bubble.dataset.sender = sender;

    const span = document.createElement('div');
    span.classList.add('text');
    span.innerText = text;
    bubble.appendChild(span);

    // زر النسخ
    if (sender === 'assistant') {
        const copyBtn = document.createElement('button');
        copyBtn.classList.add('copy-btn');
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.title = 'نسخ';
        copyBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            navigator.clipboard.writeText(text).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => copyBtn.innerHTML = '<i class="fas fa-copy"></i>', 1500);
            });
        });
        bubble.appendChild(copyBtn);
    }

    row.appendChild(bubble);
    messagesEl.appendChild(row);

    if (save) saveMessagesToLocal();
    if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
    updateMsgCount();
}

function scrollToBottom() {
    if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ============================================================================
// 3. الاتصال بالخادم
// ============================================================================

async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    inputEl.value = '';
    if (inputEl.style) inputEl.style.height = 'auto';

    // إظهار مؤشر التفكير
    if (typingEl) typingEl.classList.remove('hidden');

    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-Id': currentSessionId || ''
            },
            body: JSON.stringify({
                message: text,
                ai_type: selectedModel,
                session_id: currentSessionId
            })
        });

        const data = await res.json();

        if (typingEl) typingEl.classList.add('hidden');

        // تحديث معرف الجلسة
        if (data.session_id && !currentSessionId) {
            currentSessionId = data.session_id;
            localStorage.setItem('sky_session_id', currentSessionId);
        }

        let replyText = data.reply || 'لم يصل رد من سماء.';
        addMessage(replyText, 'assistant');

    } catch (e) {
        if (typingEl) typingEl.classList.add('hidden');
        addMessage('⚠️ تعذر الاتصال بسماء. تأكد من اتصال الإنترنت.', 'assistant');
    }
}

// ============================================================================
// 4. رفع الملفات والروابط
// ============================================================================

async function uploadFile(file) {
    if (!file) return;
    addMessage(`📎 جاري رفع وتحليل: ${file.name}`, 'user');
    if (typingEl) typingEl.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);
    if (currentSessionId) formData.append('session_id', currentSessionId);

    try {
        const res = await fetch('/upload', {
            method: 'POST',
            body: formData,
            headers: { 'X-Session-Id': currentSessionId || '' }
        });
        const data = await res.json();
        if (typingEl) typingEl.classList.add('hidden');
        if (data.session_id && !currentSessionId) {
            currentSessionId = data.session_id;
            localStorage.setItem('sky_session_id', currentSessionId);
        }
        addMessage(data.reply || 'تم استلام الملف.', 'assistant');
    } catch (e) {
        if (typingEl) typingEl.classList.add('hidden');
        addMessage('⚠️ فشل رفع الملف.', 'assistant');
    }
}

function sendUrl() {
    const url = prompt('ألصق الرابط هنا:');
    if (url && url.startsWith('http')) {
        inputEl.value = url;
        sendMessage();
    } else if (url) {
        alert('الرجاء إدخال رابط صحيح يبدأ بـ http:// أو https://');
    }
}

// ============================================================================
// 5. مسح المحادثة
// ============================================================================

async function clearConversation() {
    if (!confirm('هل تريد مسح كل المحادثة؟ سيتم حذف الذاكرة بالكامل.')) return;
    messagesEl.innerHTML = '';
    localStorage.removeItem(STORAGE_KEY);

    if (currentSessionId) {
        try {
            await fetch('/clear', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: currentSessionId })
            });
        } catch (e) {}
    }

    currentSessionId = null;
    localStorage.removeItem('sky_session_id');
    addMessage('✨ تم مسح المحادثة والذاكرة بالكامل. يمكنك البدء من جديد. ✨', 'assistant');
}

// ============================================================================
// 6. تبديل النموذج والإعدادات
// ============================================================================

function setModel(model) {
    selectedModel = model;
    localStorage.setItem('sky_selected_model', model);
    document.querySelectorAll('.model-pill, .model-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.model === model);
    });
    const defaultModelSelect = document.getElementById('default-model-select') || document.getElementById('default-model');
    if (defaultModelSelect) defaultModelSelect.value = model;
}

// ============================================================================
// 7. ربط الأحداث العامة
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // أزرار الإرسال
    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (inputEl) {
        inputEl.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        inputEl.addEventListener('input', () => {
            if (inputEl.style) {
                inputEl.style.height = 'auto';
                inputEl.style.height = inputEl.scrollHeight + 'px';
            }
        });
        inputEl.focus();
    }

    // أزرار النماذج
    document.querySelectorAll('.model-pill, .model-btn').forEach(btn => {
        btn.addEventListener('click', () => setModel(btn.dataset.model));
    });

    // مسح المحادثة
    const clearBtn = document.getElementById('clear-chat') || document.getElementById('clearChat');
    if (clearBtn) clearBtn.addEventListener('click', clearConversation);

    // رفع الملفات
    const fileUpload = document.getElementById('file-upload');
    const uploadLabel = document.getElementById('upload-label');
    if (uploadLabel && fileUpload) {
        uploadLabel.addEventListener('click', () => fileUpload.click());
    }
    if (fileUpload) {
        fileUpload.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                uploadFile(e.target.files[0]);
                fileUpload.value = '';
            }
        });
    }

    // الروابط
    const urlBtn = document.getElementById('url-trigger') || document.getElementById('url-btn');
    if (urlBtn) urlBtn.addEventListener('click', sendUrl);

    // الإعدادات
    const settingsBtn = document.getElementById('settings-drawer-btn') || document.getElementById('settingsToggle');
    const settingsPanel = document.getElementById('settings-drawer') || document.getElementById('settingsPanel');
    const closeSettings = document.getElementById('close-drawer') || document.getElementById('closeSettings');
    
    if (settingsBtn && settingsPanel) {
        settingsBtn.addEventListener('click', () => settingsPanel.classList.toggle('open'));
    }
    if (closeSettings && settingsPanel) {
        closeSettings.addEventListener('click', () => settingsPanel.classList.remove('open'));
    }
    if (settingsPanel) {
        settingsPanel.addEventListener('click', (e) => {
            if (e.target === settingsPanel) settingsPanel.classList.remove('open');
        });
    }

    // النموذج الافتراضي في الإعدادات
    const defaultModelSelect = document.getElementById('default-model-select') || document.getElementById('default-model');
    if (defaultModelSelect) {
        defaultModelSelect.value = selectedModel;
        defaultModelSelect.addEventListener('change', (e) => setModel(e.target.value));
    }

    // الثيم (يدعم الأزرار القديمة والجديدة)
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
            const newTheme = current === 'light' ? 'dark' : 'light';
            document.documentElement.classList.toggle('dark', newTheme === 'dark');
            localStorage.setItem('sky_theme', newTheme);
        });
    }

    // زر النزول للأسفل
    const scrollDownBtn = document.getElementById('scrollDown');
    if (scrollDownBtn && chatContainer) {
        chatContainer.addEventListener('scroll', () => {
            const nearBottom = chatContainer.scrollHeight - chatContainer.scrollTop - chatContainer.clientHeight < 80;
            scrollDownBtn.classList.toggle('hidden', nearBottom);
        });
        scrollDownBtn.addEventListener('click', scrollToBottom);
    }

    // بدء التشغيل
    restoreMessages();
    setModel(selectedModel);
});
