/* ============================================================
   Sky OS • Hybrid Intelligence UI
   script.js — Single File Version (Sessions + Messages + Tools + API)
   By Driving & Copilot — 2026
   ============================================================ */

/* ------------------------------
   1) DOM CACHE
   ------------------------------ */

const dom = {
    messages:        document.getElementById('messages'),
    archiveSection:  document.getElementById('archive-section'),
    archiveToggle:   document.getElementById('archive-toggle'),
    archiveContent:  document.getElementById('archive-content'),
    archiveMessages: document.getElementById('archive-messages'),
    typing:          document.getElementById('typing-indicator'),
    scrollUp:        document.getElementById('scroll-up'),
    scrollDown:      document.getElementById('scroll-down'),
    input:           document.getElementById('message-input'),
    send:            document.getElementById('send-btn'),
    attach:          document.getElementById('attach-btn'),
    fileInput:       document.getElementById('file-input'),
    filePreview:     document.getElementById('file-preview'),
    contextText:     document.getElementById('context-text'),
    sessionsPanel:   document.getElementById('sessions-panel'),
    sessionsList:    document.getElementById('sessions-list'),
    createSession:   document.getElementById('create-session'),
    toolsPanel:      document.getElementById('tools-panel'),
    themeToggle:     document.getElementById('theme-toggle'),
    newSessionTop:   document.getElementById('new-session'),
    closeSessions:   document.getElementById('close-sessions'),
    closeTools:      document.getElementById('close-tools')
};


/* ------------------------------
   2) GLOBAL STATE
   ------------------------------ */

let sessions = [];
let currentSessionId = null;

let messageCountInCurrentSession = 0;
const ARCHIVE_THRESHOLD = 70;

let attachedFiles = [];

let systemStateEl = null;


/* ------------------------------
   3) UTILITIES
   ------------------------------ */

function generateId() {
    return 's_' + Math.random().toString(36).substring(2, 10);
}

function escapeHtml(str = '') {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function scrollToBottom() {
    dom.messages.scrollTo({
        top: dom.messages.scrollHeight,
        behavior: 'smooth'
    });
}

function scrollToTop() {
    dom.messages.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function updateScrollButtons() {
    const { scrollTop, scrollHeight, clientHeight } = dom.messages;

    if (scrollTop > 80) {
        dom.scrollUp.classList.add('visible');
    } else {
        dom.scrollUp.classList.remove('visible');
    }

    if (scrollTop + clientHeight < scrollHeight - 80) {
        dom.scrollDown.classList.add('visible');
    } else {
        dom.scrollDown.classList.remove('visible');
    }
}


/* ------------------------------
   4) SYSTEM STATE
   ------------------------------ */

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
   5) SESSIONS
   ------------------------------ */

function getCurrentSession() {
    return sessions.find(s => s.id === currentSessionId) || null;
}

function createNewSession(name = null) {
    const id = generateId();
    const session = {
        id,
        name: name || 'جلسة جديدة',
        messages: [],
        archivedMessages: []
    };
    sessions.unshift(session);
    currentSessionId = id;
    renderSessionsList();
    loadSession(id);
}

function renderSessionsList() {
    dom.sessionsList.innerHTML = '';
    sessions.forEach(session => {
        const item = document.createElement('div');
        item.className = 'session-item' + (session.id === currentSessionId ? ' active' : '');
        item.textContent = session.name;
        item.onclick = () => {
            currentSessionId = session.id;
            renderSessionsList();
            loadSession(session.id);
        };
        dom.sessionsList.appendChild(item);
    });
}

function loadSession(sessionId) {
    const session = sessions.find(s => s.id === sessionId);
    if (!session) return;

    dom.messages.innerHTML = '';
    dom.archiveMessages.innerHTML = '';
    messageCountInCurrentSession = session.messages.length;

    const fragMain = document.createDocumentFragment();
    session.messages.forEach(msg => {
        const el = buildMessageElement(msg.role, msg.content);
        fragMain.appendChild(el);
    });
    dom.messages.appendChild(fragMain);

    const fragArch = document.createDocumentFragment();
    session.archivedMessages.forEach(msg => {
        const el = buildMessageElement(msg.role, msg.content);
        fragArch.appendChild(el);
    });
    dom.archiveMessages.appendChild(fragArch);

    updateArchiveToggleLabel();
    updateScrollButtons();
    scrollToBottom();
}

function updateSessionNameFromFirstMessage() {
    const session = getCurrentSession();
    if (!session) return;
    if (!session.messages.length) return;

    const first = session.messages[0];
    const raw = first.content || '';
    const clean = raw.replace(/\s+/g, ' ').trim();
    if (!clean) return;

    let title = clean.slice(0, 22);
    if (clean.length > 22) title += '...';

    session.name = title;
    renderSessionsList();
}


/* ------------------------------
   6) MESSAGES
   ------------------------------ */

function buildMessageElement(role, content) {
    const msg = document.createElement('div');
    msg.className = 'message ' + (role === 'user' ? 'user' : 'assistant');
    msg.innerHTML = content;

    if (role === 'assistant') {
        enhanceAssistantMessage(msg, content);
    }

    return msg;
}

function renderMessage(role, content, pushToState = true) {
    const msgEl = buildMessageElement(role, content);
    dom.messages.appendChild(msgEl);

    if (pushToState) {
        const session = getCurrentSession();
        if (!session) return;

        session.messages.push({ role, content });
        messageCountInCurrentSession++;

        if (session.messages.length === 1 && role === 'user') {
            updateSessionNameFromFirstMessage();
        }

        if (messageCountInCurrentSession > ARCHIVE_THRESHOLD) {
            archiveOldMessages(session);
        }
    }

    updateScrollButtons();
    scrollToBottom();
}

function renderArchivedMessage(role, content) {
    const msg = buildMessageElement(role, content);
    dom.archiveMessages.appendChild(msg);
}

function archiveOldMessages(session) {
    if (session.messages.length === 0) return;

    const archived = session.messages.shift();
    session.archivedMessages.push(archived);

    dom.messages.innerHTML = '';
    const fragMain = document.createDocumentFragment();
    session.messages.forEach(msg => {
        fragMain.appendChild(buildMessageElement(msg.role, msg.content));
    });
    dom.messages.appendChild(fragMain);

    dom.archiveMessages.innerHTML = '';
    const fragArch = document.createDocumentFragment();
    session.archivedMessages.forEach(msg => {
        fragArch.appendChild(buildMessageElement(msg.role, msg.content));
    });
    dom.archiveMessages.appendChild(fragArch);

    updateArchiveToggleLabel();
}


/* ------------------------------
   7) ARCHIVE UX
   ------------------------------ */

function updateArchiveToggleLabel() {
    const session = getCurrentSession();
    if (!session) return;

    const count = session.archivedMessages?.length || 0;
    const span = dom.archiveToggle.querySelector('span');
    if (!span) return;

    if (count === 0) {
        span.textContent = 'لا يوجد أرشيف بعد';
    } else {
        span.textContent = `عرض الأرشيف (${count} رسالة)`;
    }
}

function toggleArchive() {
    dom.archiveContent.classList.toggle('open');
}


/* ------------------------------
   8) TYPING INDICATOR
   ------------------------------ */

function showTyping() {
    dom.typing.classList.remove('hidden');
    scrollToBottom();
}

function hideTyping() {
    dom.typing.classList.add('hidden');
}


/* ------------------------------
   9) CONTEXT DETECTION
   ------------------------------ */

function detectContext(text) {
    if (!text) {
        dom.contextText.textContent = 'وضع المحادثة';
        return;
    }

    const t = text.toLowerCase();

    if (t.includes('كود') || t.includes('code') || t.includes('javascript') || t.includes('html') || t.includes('css')) {
        dom.contextText.textContent = 'وضع البرمجة';
    } else if (t.includes('حلل') || t.includes('تحليل') || t.includes('analyze')) {
        dom.contextText.textContent = 'وضع التحليل';
    } else if (t.includes('لخص') || t.includes('تلخيص') || t.includes('summary')) {
        dom.contextText.textContent = 'وضع التلخيص';
    } else if (t.includes('فكرة') || t.includes('أفكار') || t.includes('ideas')) {
        dom.contextText.textContent = 'وضع توليد الأفكار';
    } else {
        dom.contextText.textContent = 'وضع المحادثة';
    }
}


/* ------------------------------
   10) FILES
   ------------------------------ */

function openFilePicker() {
    dom.fileInput.click();
}

function handleFiles(e) {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    attachedFiles = files;
    dom.filePreview.innerHTML = '';

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
        dom.filePreview.appendChild(pill);
    });
}


/* ------------------------------
   11) TOOLS
   ------------------------------ */

const toolButtons = document.querySelectorAll('.tool-btn');

function handleTool(tool) {
    let hint = '';

    switch (tool) {
        case 'summarize':
            hint = 'لخص النص التالي بدقة عالية:';
            dom.contextText.textContent = 'وضع التلخيص';
            break;
        case 'analyze':
            hint = 'حلل هذا المحتوى بعمق، واذكر النقاط القوية والضعيفة:';
            dom.contextText.textContent = 'وضع التحليل';
            break;
        case 'code':
            hint = 'اكتب كود يقوم بالتالي:';
            dom.contextText.textContent = 'وضع البرمجة';
            break;
        case 'ideas':
            hint = 'أعطني أفكارًا إبداعية حول:';
            dom.contextText.textContent = 'وضع توليد الأفكار';
            break;
        case 'rewrite':
            hint = 'أعد صياغة النص التالي بأسلوب أفضل وأكثر وضوحًا:';
            dom.contextText.textContent = 'وضع إعادة الصياغة';
            break;
        case 'file':
            hint = 'سأرفع لك ملفًا الآن، أريد منك تحليله:';
            dom.contextText.textContent = 'وضع تحليل الملفات';
            break;
        default:
            dom.contextText.textContent = 'وضع المحادثة';
    }

    if (hint) {
        dom.input.value = hint + ' ';
        dom.input.focus();
    }
}


/* ------------------------------
   12) MINI TOC + COLLAPSE + ANCHOR
   ------------------------------ */

function el(tag, className, html) {
    const e = document.createElement(tag);
    if (className) e.className = className;
    if (html !== undefined) e.innerHTML = html;
    return e;
}

function enhanceAssistantMessage(msgEl, rawContent) {
    if (!msgEl) return;
    if (msgEl.dataset.enhanced === '1') return;

    const text = rawContent || '';
    const length = text.length;
    if (length < 400) return;

    const miniToc = el('div', 'mini-toc');
    const title = el('div', 'mini-toc-title', 'محتويات الرد:');
    const list = el('ul');

    const sections = [
        { key: 'مقدمة' },
        { key: 'نقاط رئيسية' },
        { key: 'كود' },
        { key: 'خلاصة' }
    ];

    sections.forEach(sec => {
        const li = el('li', null, sec.key);
        li.addEventListener('click', () => {
            msgEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            msgEl.style.transition = 'transform 0.2s ease';
            msgEl.style.transform = 'scale(1.02)';
            setTimeout(() => msgEl.style.transform = 'scale(1)', 220);
        });
        list.appendChild(li);
    });

    miniToc.appendChild(title);
    miniToc.appendChild(list);

    const collapse = el('div', 'collapse-block');
    const header = el('div', 'collapse-header');
    header.innerHTML = `
        <span>تفاصيل موسعة</span>
        <i class="fa-solid fa-chevron-down"></i>
    `;
    const content = el('div', 'collapse-content open', msgEl.innerHTML);
    header.classList.add('open');

    header.addEventListener('click', () => {
        const isOpen = content.classList.contains('open');
        if (isOpen) {
            content.classList.remove('open');
            header.classList.remove('open');
        } else {
            content.classList.add('open');
            header.classList.add('open');
        }
    });

    collapse.appendChild(header);
    collapse.appendChild(content);

    msgEl.innerHTML = '';
    msgEl.appendChild(miniToc);
    msgEl.appendChild(collapse);

    const anchor = el('div', 'anchor', 'العودة لهذا الرد');
    anchor.addEventListener('click', () => {
        msgEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    dom.messages.insertBefore(anchor, msgEl);

    msgEl.dataset.enhanced = '1';
}


/* ------------------------------
   13) SENDING MESSAGE + BACKEND
   ------------------------------ */

async function sendMessage() {
    const text = dom.input.value.trim();
    if (!text && attachedFiles.length === 0) return;

    const session = getCurrentSession();
    if (!session) return;

    renderMessage('user', escapeHtml(text || '[ملف فقط]'));

    dom.input.value = '';
    attachedFiles = [];
    dom.filePreview.innerHTML = '';

    detectContext(text);
    showTyping();
    setSystemState('thinking', 'سماء تفكر في رد مناسب...');

    try {
        const reply = await callBackend(text, session);
        hideTyping();
        setSystemState('connected', 'متصل • جاهز للاستقبال');
        renderMessage('assistant', reply);
    } catch (err) {
        hideTyping();
        setSystemState('error', 'حدث خطأ في الاتصال • حاول مرة أخرى');
        renderMessage('assistant', escapeHtml('حدث خطأ أثناء الاتصال بالخادم.\n\nتفاصيل تقنية:\n' + (err.message || err)));
    }
}

async function callBackend(userText, session) {
    // هنا تقدر تغيّر المسار حسب الباك‑إند عندك
    const endpoint = '/ask';

    const payload = {
        message: userText,
        session_id: session.id,
        context: dom.contextText.textContent || 'وضع المحادثة'
    };

    const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (!res.ok) {
        throw new Error('HTTP ' + res.status);
    }

    const data = await res.json();

    // نتوقع أن الباك‑إند يرجع { reply: "..." }
    const reply = data.reply || '(لم يتم استلام رد من الخادم)';
    return escapeHtml(reply);
}


/* ------------------------------
   14) PANELS + THEME
   ------------------------------ */

function openSessionsPanel() {
    dom.sessionsPanel.classList.add('open');
}

function closeSessionsPanel() {
    dom.sessionsPanel.classList.remove('open');
}

function openToolsPanel() {
    dom.toolsPanel.classList.add('open');
}

function closeToolsPanel() {
    dom.toolsPanel.classList.remove('open');
}

function toggleTheme() {
    document.body.classList.toggle('dark');
}


/* ------------------------------
   15) EVENTS BINDING
   ------------------------------ */

function bindEvents() {
    dom.send.addEventListener('click', sendMessage);

    dom.input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    dom.messages.addEventListener('scroll', updateScrollButtons);
    dom.scrollUp.addEventListener('click', scrollToTop);
    dom.scrollDown.addEventListener('click', scrollToBottom);

    dom.attach.addEventListener('click', openFilePicker);
    dom.fileInput.addEventListener('change', handleFiles);

    dom.archiveToggle.addEventListener('click', toggleArchive);

    dom.themeToggle.addEventListener('click', toggleTheme);

    dom.newSessionTop.addEventListener('click', () => {
        openSessionsPanel();
        createNewSession('جلسة جديدة');
    });

    dom.createSession.addEventListener('click', () => createNewSession('جلسة جديدة'));
    dom.closeSessions.addEventListener('click', closeSessionsPanel);

    dom.closeTools.addEventListener('click', closeToolsPanel);

    toolButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tool = btn.dataset.tool;
            handleTool(tool);
        });
    });
}


/* ------------------------------
   16) INIT
   ------------------------------ */

function init() {
    createNewSession('الجلسة الأولى');
    updateScrollButtons();
    createSystemState();
    setSystemState('connected', 'متصل • جاهز للاستقبال');
}

document.addEventListener('DOMContentLoaded', () => {
    bindEvents();
    init();
});
