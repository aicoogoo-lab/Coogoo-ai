/* ============================================================
   Sky OS • Hybrid Intelligence UI
   script.js — Part 1 (Core Engine + Sessions + Messages)
   By Driving & Copilot — 2026
   ============================================================ */

/* ------------------------------
   1) ELEMENTS
   ------------------------------ */

const messagesEl       = document.getElementById('messages');
const archiveSectionEl = document.getElementById('archive-section');
const archiveToggleEl  = document.getElementById('archive-toggle');
const archiveContentEl = document.getElementById('archive-content');
const archiveMessagesEl= document.getElementById('archive-messages');

const typingEl         = document.getElementById('typing-indicator');

const scrollUpBtn      = document.getElementById('scroll-up');
const scrollDownBtn    = document.getElementById('scroll-down');

const inputEl          = document.getElementById('message-input');
const sendBtn          = document.getElementById('send-btn');
const attachBtn        = document.getElementById('attach-btn');
const fileInput        = document.getElementById('file-input');
const filePreviewEl    = document.getElementById('file-preview');

const contextBarText   = document.getElementById('context-text');

const sessionsPanel    = document.getElementById('sessions-panel');
const sessionsListEl   = document.getElementById('sessions-list');
const createSessionBtn = document.getElementById('create-session');

const toolsPanel       = document.getElementById('tools-panel');

const themeToggleBtn   = document.getElementById('theme-toggle');
const newSessionTopBtn = document.getElementById('new-session');


/* ------------------------------
   2) STATE
   ------------------------------ */

let sessions = [];
let currentSessionId = null;

let messageCountInCurrentSession = 0;
const ARCHIVE_THRESHOLD = 70;

let attachedFiles = [];


/* ------------------------------
   3) UTILITIES
   ------------------------------ */

function generateId() {
    return 's_' + Math.random().toString(36).substring(2, 10);
}

function scrollToBottom() {
    messagesEl.scrollTo({
        top: messagesEl.scrollHeight,
        behavior: 'smooth'
    });
}

function scrollToTop() {
    messagesEl.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function updateScrollButtons() {
    const { scrollTop, scrollHeight, clientHeight } = messagesEl;

    if (scrollTop > 80) {
        scrollUpBtn.classList.add('visible');
    } else {
        scrollUpBtn.classList.remove('visible');
    }

    if (scrollTop + clientHeight < scrollHeight - 80) {
        scrollDownBtn.classList.add('visible');
    } else {
        scrollDownBtn.classList.remove('visible');
    }
}


/* ------------------------------
   4) SESSIONS SYSTEM (BASIC)
   ------------------------------ */

function createNewSession(name = null) {
    const id = generateId();
    const session = {
        id,
        name: name || `جلسة جديدة`,
        messages: [],
        archivedMessages: []
    };
    sessions.unshift(session);
    currentSessionId = id;
    renderSessionsList();
    loadSession(id);
}

function renderSessionsList() {
    sessionsListEl.innerHTML = '';
    sessions.forEach(session => {
        const item = document.createElement('div');
        item.className = 'session-item' + (session.id === currentSessionId ? ' active' : '');
        item.textContent = session.name;
        item.onclick = () => {
            currentSessionId = session.id;
            renderSessionsList();
            loadSession(session.id);
        };
        sessionsListEl.appendChild(item);
    });
}

function getCurrentSession() {
    return sessions.find(s => s.id === currentSessionId) || null;
}

function loadSession(sessionId) {
    const session = sessions.find(s => s.id === sessionId);
    if (!session) return;

    messagesEl.innerHTML = '';
    archiveMessagesEl.innerHTML = '';
    messageCountInCurrentSession = session.messages.length;

    // عرض الرسائل العادية
    session.messages.forEach(msg => {
        renderMessage(msg.role, msg.content, false);
    });

    // عرض الأرشيف
    session.archivedMessages.forEach(msg => {
        renderArchivedMessage(msg.role, msg.content);
    });

    scrollToBottom();
}


/* ------------------------------
   5) MESSAGES
   ------------------------------ */

function renderMessage(role, content, pushToState = true) {
    const msg = document.createElement('div');
    msg.className = 'message ' + (role === 'user' ? 'user' : 'assistant');
    msg.innerHTML = content;
    messagesEl.appendChild(msg);

    if (pushToState) {
        const session = getCurrentSession();
        if (!session) return;

        session.messages.push({ role, content });
        messageCountInCurrentSession++;

        // إذا تجاوزنا 70 رسالة → ننقل الأقدم للأرشيف
        if (messageCountInCurrentSession > ARCHIVE_THRESHOLD) {
            archiveOldMessages(session);
        }
    }

    updateScrollButtons();
    scrollToBottom();
}

function renderArchivedMessage(role, content) {
    const msg = document.createElement('div');
    msg.className = 'message ' + (role === 'user' ? 'user' : 'assistant');
    msg.innerHTML = content;
    archiveMessagesEl.appendChild(msg);
}

function archiveOldMessages(session) {
    // ننقل أول رسالة من messages إلى archivedMessages
    if (session.messages.length === 0) return;

    const archived = session.messages.shift();
    session.archivedMessages.push(archived);

    // إعادة بناء المنطقة المرئية
    messagesEl.innerHTML = '';
    session.messages.forEach(msg => {
        renderMessage(msg.role, msg.content, false);
    });

    archiveMessagesEl.innerHTML = '';
    session.archivedMessages.forEach(msg => {
        renderArchivedMessage(msg.role, msg.content);
    });
}


/* ------------------------------
   6) TYPING INDICATOR
   ------------------------------ */

function showTyping() {
    typingEl.classList.remove('hidden');
    scrollToBottom();
}

function hideTyping() {
    typingEl.classList.add('hidden');
}


/* ------------------------------
   7) SENDING MESSAGE
   ------------------------------ */

function sendMessage() {
    const text = inputEl.value.trim();
    if (!text && attachedFiles.length === 0) return;

    const session = getCurrentSession();
    if (!session) return;

    // رسالة المستخدم
    renderMessage('user', escapeHtml(text || '[ملف فقط]'));

    // تنظيف الإدخال والملفات
    inputEl.value = '';
    attachedFiles = [];
    filePreviewEl.innerHTML = '';

    // تحديث السياق
    detectContext(text);

    // إظهار "سماء تفكر..."
    showTyping();

    // هنا مكان استدعاء الـ API الحقيقي لاحقًا
    fakeAssistantReply(text);
}


/* ------------------------------
   8) FAKE ASSISTANT (PLACEHOLDER)
   ------------------------------ */

function fakeAssistantReply(userText) {
    // محاكاة تأخير
    setTimeout(() => {
        hideTyping();

        const reply = userText
            ? `تلقيت رسالتك:\n\n${escapeHtml(userText)}\n\n(هنا سيكون رد سماء الحقيقي من الـ API)`
            : `تم استلام الملفات. (هنا سيكون تحليل سماء الحقيقي للملفات)`;

        renderMessage('assistant', reply);
    }, 900);
}


/* ------------------------------
   9) CONTEXT DETECTION (بسيط مبدئيًا)
   ------------------------------ */

function detectContext(text) {
    if (!text) {
        contextBarText.textContent = 'وضع المحادثة';
        return;
    }

    const t = text.toLowerCase();

    if (t.includes('كود') || t.includes('code') || t.includes('javascript') || t.includes('html') || t.includes('css')) {
        contextBarText.textContent = 'وضع البرمجة';
    } else if (t.includes('حلل') || t.includes('تحليل') || t.includes('analyze')) {
        contextBarText.textContent = 'وضع التحليل';
    } else if (t.includes('لخص') || t.includes('تلخيص') || t.includes('summary')) {
        contextBarText.textContent = 'وضع التلخيص';
    } else {
        contextBarText.textContent = 'وضع المحادثة';
    }
}


/* ------------------------------
   10) FILES
   ------------------------------ */

attachBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    attachedFiles = files;
    filePreviewEl.innerHTML = '';

    files.forEach(file => {
        const pill = document.createElement('div');
        pill.className = 'file-pill';
        pill.innerHTML = `
            <i class="fa-solid fa-file"></i>
            <span>${file.name}</span>
            <button type="button"><i class="fa-solid fa-xmark"></i></button>
        `;
        const btn = pill.querySelector('button');
        btn.onclick = () => {
            attachedFiles = attachedFiles.filter(f => f !== file);
            pill.remove();
        };
        filePreviewEl.appendChild(pill);
    });
});


/* ------------------------------
   11) EVENTS
   ------------------------------ */

sendBtn.addEventListener('click', sendMessage);

inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

messagesEl.addEventListener('scroll', updateScrollButtons);

scrollUpBtn.addEventListener('click', scrollToTop);
scrollDownBtn.addEventListener('click', scrollToBottom);

archiveToggleEl.addEventListener('click', () => {
    archiveContentEl.classList.toggle('open');
});


/* ------------------------------
   12) THEME TOGGLE
   ------------------------------ */

themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark');
});


/* ------------------------------
   13) INITIALIZATION
   ------------------------------ */

function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function init() {
    createNewSession('الجلسة الأولى');
    updateScrollButtons();
}

document.addEventListener('DOMContentLoaded', init);/* ============================================================
   Sky OS • Hybrid Intelligence UI
   script.js — Part 2 (Tools + System State + Panels + Session Enhancements)
   ============================================================ */


/* ------------------------------
   14) SYSTEM STATE INDICATOR
   ------------------------------ */

let systemStateEl = null;

function createSystemState() {
    systemStateEl = document.createElement('div');
    systemStateEl.className = 'system-state connected';
    systemStateEl.innerHTML = `
        <i class="fa-solid fa-signal"></i>
        <span>متصل • جاهز للاستقبال</span>
    `;
    document.body.appendChild(systemStateEl);
}

function setSystemState(state, text) {
    if (!systemStateEl) return;
    systemStateEl.className = 'system-state ' + state;
    systemStateEl.innerHTML = `
        <i class="fa-solid fa-signal"></i>
        <span>${text}</span>
    `;
}


/* ------------------------------
   15) TOOLS SYSTEM
   ------------------------------ */

const toolButtons = document.querySelectorAll('.tool-btn');

toolButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const tool = btn.dataset.tool;
        handleTool(tool);
    });
});

function handleTool(tool) {
    let hint = '';

    switch (tool) {
        case 'summarize':
            hint = 'لخص النص التالي بدقة عالية:';
            contextBarText.textContent = 'وضع التلخيص';
            break;
        case 'analyze':
            hint = 'حلل هذا المحتوى بعمق، واذكر النقاط القوية والضعيفة:';
            contextBarText.textContent = 'وضع التحليل';
            break;
        case 'code':
            hint = 'اكتب كود يقوم بالتالي:';
            contextBarText.textContent = 'وضع البرمجة';
            break;
        case 'ideas':
            hint = 'أعطني أفكارًا إبداعية حول:';
            contextBarText.textContent = 'وضع توليد الأفكار';
            break;
        case 'rewrite':
            hint = 'أعد صياغة النص التالي بأسلوب أفضل وأكثر وضوحًا:';
            contextBarText.textContent = 'وضع إعادة الصياغة';
            break;
        case 'file':
            hint = 'سأرفع لك ملفًا الآن، أريد منك تحليله:';
            contextBarText.textContent = 'وضع تحليل الملفات';
            break;
        default:
            contextBarText.textContent = 'وضع المحادثة';
    }

    if (hint) {
        inputEl.value = hint + ' ';
        inputEl.focus();
    }
}


/* ------------------------------
   16) PANELS TOGGLE (SESSIONS + TOOLS)
   ------------------------------ */

const closeSessionsBtn = document.getElementById('close-sessions');
const closeToolsBtn    = document.getElementById('close-tools');

newSessionTopBtn.addEventListener('click', () => {
    // فتح لوحة الجلسات + إنشاء جلسة جديدة
    sessionsPanel.classList.add('open');
    createNewSession('جلسة جديدة');
});

createSessionBtn.addEventListener('click', () => {
    createNewSession('جلسة جديدة');
});

closeSessionsBtn.addEventListener('click', () => {
    sessionsPanel.classList.remove('open');
});

closeToolsBtn.addEventListener('click', () => {
    toolsPanel.classList.remove('open');
});

/* فتح لوحة الأدوات عند الضغط على زر المرفقات مع الضغط المطوّل (مستقبلاً ممكن نغيره) */
 المطوّل (مستقبلاً ممكن نغيره) */
attachBtn.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    toolsPanel.classList.add('open');
});


/* ------------------------------
   17) ENHANCE SESSIONS (AUTO NAME)
   ------------------------------ */

function updateSessionNameFromFirstMessage() {
    const session = getCurrentSession();
    if (!session) return;
    if (!session.messages.length) return;

    const first = session.messages[0];
    const raw = first.content || '';
    const clean = raw.replace(/\s+/g, ' ').trim();

    if (!clean) return;

    // نأخذ أول 18–22 حرف كعنوان للجلسة
    let title = clean.slice(0, 22);
    if (clean.length > 22) title += '...';

    session.name = title;
    renderSessionsList();
}


/* تعديل renderMessage لندعو تحديث اسم الجلسة بعد أول رسالة من المستخدم */
const _renderMessageOriginal = renderMessage;
renderMessage = function(role, content, pushToState = true) {
    _renderMessageOriginal(role, content, pushToState);

    if (role === 'user') {
        const session = getCurrentSession();
        if (session && session.messages.length === 1) {
            updateSessionNameFromFirstMessage();
        }
    }
};


/* ------------------------------
   18) SYSTEM STATE INTEGRATION
   ------------------------------ */

/* نعدل fakeAssistantReply ليتفاعل مع حالة النظام */
const _fakeAssistantReplyOriginal = fakeAssistantReply;
fakeAssistantReply = function(userText) {
    setSystemState('thinking', 'سماء تفكر في رد مناسب...');
    showTyping();

    setTimeout(() => {
        hideTyping();
        setSystemState('connected', 'متصل • جاهز للاستقبال');
        _fakeAssistantReplyOriginal(userText);
    }, 900);
};


/* ------------------------------
   19) INIT EXTENSION
   ------------------------------ */

const _initOriginal = init;
init = function() {
    _initOriginal();
    createSystemState();
};/* ============================================================
   Sky OS • Hybrid Intelligence UI
   script.js — Part 2 (Tools + System State + Panels + Session Enhancements)
   ============================================================ */


/* ------------------------------
   14) SYSTEM STATE INDICATOR
   ------------------------------ */

let systemStateEl = null;

function createSystemState() {
    systemStateEl = document.createElement('div');
    systemStateEl.className = 'system-state connected';
    systemStateEl.innerHTML = `
        <i class="fa-solid fa-signal"></i>
        <span>متصل • جاهز للاستقبال</span>
    `;
    document.body.appendChild(systemStateEl);
}

function setSystemState(state, text) {
    if (!systemStateEl) return;
    systemStateEl.className = 'system-state ' + state;
    systemStateEl.innerHTML = `
        <i class="fa-solid fa-signal"></i>
        <span>${text}</span>
    `;
}


/* ------------------------------
   15) TOOLS SYSTEM
   ------------------------------ */

const toolButtons = document.querySelectorAll('.tool-btn');

toolButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const tool = btn.dataset.tool;
        handleTool(tool);
    });
});

function handleTool(tool) {
    let hint = '';

    switch (tool) {
        case 'summarize':
            hint = 'لخص النص التالي بدقة عالية:';
            contextBarText.textContent = 'وضع التلخيص';
            break;
        case 'analyze':
            hint = 'حلل هذا المحتوى بعمق، واذكر النقاط القوية والضعيفة:';
            contextBarText.textContent = 'وضع التحليل';
            break;
        case 'code':
            hint = 'اكتب كود يقوم بالتالي:';
            contextBarText.textContent = 'وضع البرمجة';
            break;
        case 'ideas':
            hint = 'أعطني أفكارًا إبداعية حول:';
            contextBarText.textContent = 'وضع توليد الأفكار';
            break;
        case 'rewrite':
            hint = 'أعد صياغة النص التالي بأسلوب أفضل وأكثر وضوحًا:';
            contextBarText.textContent = 'وضع إعادة الصياغة';
            break;
        case 'file':
            hint = 'سأرفع لك ملفًا الآن، أريد منك تحليله:';
            contextBarText.textContent = 'وضع تحليل الملفات';
            break;
        default:
            contextBarText.textContent = 'وضع المحادثة';
    }

    if (hint) {
        inputEl.value = hint + ' ';
        inputEl.focus();
    }
}


/* ------------------------------
   16) PANELS TOGGLE (SESSIONS + TOOLS)
   ------------------------------ */

const closeSessionsBtn = document.getElementById('close-sessions');
const closeToolsBtn    = document.getElementById('close-tools');

newSessionTopBtn.addEventListener('click', () => {
    // فتح لوحة الجلسات + إنشاء جلسة جديدة
    sessionsPanel.classList.add('open');
    createNewSession('جلسة جديدة');
});

createSessionBtn.addEventListener('click', () => {
    createNewSession('جلسة جديدة');
});

closeSessionsBtn.addEventListener('click', () => {
    sessionsPanel.classList.remove('open');
});

closeToolsBtn.addEventListener('click', () => {
    toolsPanel.classList.remove('open');
});

/* فتح لوحة الأدوات عند الضغط على زر المرفقات مع الضغط المطوّل (مستقبلاً ممكن نغيره) */
 المطوّل (مستقبلاً ممكن نغيره) */
attachBtn.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    toolsPanel.classList.add('open');
});


/* ------------------------------
   17) ENHANCE SESSIONS (AUTO NAME)
   ------------------------------ */

function updateSessionNameFromFirstMessage() {
    const session = getCurrentSession();
    if (!session) return;
    if (!session.messages.length) return;

    const first = session.messages[0];
    const raw = first.content || '';
    const clean = raw.replace(/\s+/g, ' ').trim();

    if (!clean) return;

    // نأخذ أول 18–22 حرف كعنوان للجلسة
    let title = clean.slice(0, 22);
    if (clean.length > 22) title += '...';

    session.name = title;
    renderSessionsList();
}


/* تعديل renderMessage لندعو تحديث اسم الجلسة بعد أول رسالة من المستخدم */
const _renderMessageOriginal = renderMessage;
renderMessage = function(role, content, pushToState = true) {
    _renderMessageOriginal(role, content, pushToState);

    if (role === 'user') {
        const session = getCurrentSession();
        if (session && session.messages.length === 1) {
            updateSessionNameFromFirstMessage();
        }
    }
};


/* ------------------------------
   18) SYSTEM STATE INTEGRATION
   ------------------------------ */

/* نعدل fakeAssistantReply ليتفاعل مع حالة النظام */
const _fakeAssistantReplyOriginal = fakeAssistantReply;
fakeAssistantReply = function(userText) {
    setSystemState('thinking', 'سماء تفكر في رد مناسب...');
    showTyping();

    setTimeout(() => {
        hideTyping();
        setSystemState('connected', 'متصل • جاهز للاستقبال');
        _fakeAssistantReplyOriginal(userText);
    }, 900);
};


/* ------------------------------
   19) INIT EXTENSION
   ------------------------------ */

const _initOriginal = init;
init = function() {
    _initOriginal();
    createSystemState();
};
