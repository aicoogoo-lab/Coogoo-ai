// static/script.js - Sky AI | النسخة النهائية v5.1
// واجهة مليئة بالحب والطمأنينة والسعادة

class SkyInterface {
    constructor() {
        this.elements = this._getElements();
        this.sessionId = localStorage.getItem('sky_session_v5') || this._generateUUID();
        this.selectedModel = localStorage.getItem('sky_model') || 'groq';
        this.storageKey = `sky_history_${this.sessionId}`;
        this.isLoading = false;

        this.init();
    }

    _getElements() {
        return {
            chatArea: document.querySelector('#chat-area') || document.querySelector('#chat-container'),
            messages: document.querySelector('#messages'),
            input: document.querySelector('#message-input') || document.querySelector('#userInput'),
            sendBtn: document.querySelector('#send-btn') || document.querySelector('#sendBtn'),
            typing: document.querySelector('#typing-indicator') || document.querySelector('#typing'),
            msgCount: document.querySelector('#msg-count'),
            charCounter: document.querySelector('#char-counter'),
            fileUpload: document.querySelector('#file-upload'),
            uploadLabel: document.querySelector('#upload-label'),
            urlTrigger: document.querySelector('#url-trigger'),
            clearBtn: document.querySelector('#clear-chat'),
            scrollDownBtn: document.querySelector('#scrollDown'),
            settingsBtn: document.querySelector('#settings-drawer-btn'),
            settingsPanel: document.querySelector('#settings-drawer'),
            closeSettings: document.querySelector('#close-drawer'),
            themeToggle: document.querySelector('#theme-toggle'),
            themeSelect: document.querySelector('#theme-select'),
            fontSizeSelect: document.querySelector('#font-size-select'),
            modelBtns: document.querySelectorAll('.model-pill')
        };
    }

    init() {
        this.bindEvents();
        this.restoreSession();
        this.applySavedTheme();
        this.applySavedFontSize();
        this.updateUI();
        this.showWelcomeIfEmpty();
    }

    _generateUUID() {
        const id = 'sky-' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('sky_session_v5', id);
        return id;
    }

    // ==================== المؤثرات الصوتية (ناعمة ودافئة) ====================
    playSound(type) {
        try {
            const audio = new (window.AudioContext || window.webkitAudioContext)();
            const osc = audio.createOscillator();
            const gain = audio.createGain();
            const filter = audio.createBiquadFilter();

            osc.type = 'sine';
            filter.type = 'lowpass';
            filter.frequency.value = 1400;

            let freq = 620;
            let vol = 0.07;
            let dur = 0.35;

            if (type === 'send') { freq = 540; dur = 0.25; }
            else if (type === 'receive') { freq = 720; vol = 0.06; dur = 0.5; }
            else if (type === 'reaction') { freq = 880; vol = 0.05; dur = 0.2; }
            else if (type === 'clear') { freq = 420; vol = 0.05; dur = 0.6; }

            osc.frequency.value = freq;
            gain.gain.value = vol;

            osc.connect(filter);
            filter.connect(gain);
            gain.connect(audio.destination);

            const now = audio.currentTime;
            osc.start(now);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + dur);
            osc.stop(now + dur + 0.1);
        } catch (_) {}
    }

    // ==================== ربط الأحداث ====================
    bindEvents() {
        this.elements.sendBtn?.addEventListener('click', () => this.handleSendMessage());
        this.elements.input?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.handleSendMessage(); }
        });
        this.elements.input?.addEventListener('input', () => {
            if (this.elements.charCounter) this.elements.charCounter.textContent = `${this.elements.input.value.length} / 2000`;
            this.autoExpandInput();
        });

        this.elements.modelBtns.forEach(btn => btn.addEventListener('click', () => this.switchModel(btn)));
        this.elements.uploadLabel?.addEventListener('click', () => this.elements.fileUpload?.click());
        this.elements.fileUpload?.addEventListener('change', (e) => {
            if (e.target.files[0]) { this.handleFileUpload(e.target.files[0]); e.target.value = ''; }
        });

        this.elements.urlTrigger?.addEventListener('click', () => this.handleUrlPaste());
        this.elements.clearBtn?.addEventListener('click', () => this.handleClearChat());

        this.elements.settingsBtn?.addEventListener('click', () => this.toggleSettings());
        this.elements.closeSettings?.addEventListener('click', () => this.toggleSettings(false));
        this.elements.settingsPanel?.addEventListener('click', (e) => {
            if (e.target === this.elements.settingsPanel) this.toggleSettings(false);
        });

        this.elements.themeToggle?.addEventListener('click', () => this.toggleTheme());
        this.elements.themeSelect?.addEventListener('change', (e) => this.applyTheme(e.target.value));
        this.elements.fontSizeSelect?.addEventListener('change', (e) => this.applyFontSize(e.target.value));

        this.elements.scrollDownBtn?.addEventListener('click', () => this.scrollToBottom(true));
        this.elements.chatArea?.addEventListener('scroll', () => this.toggleScrollButton());

        this.elements.input?.focus();
    }

    // ==================== إرسال الرسالة ====================
    async handleSendMessage() {
        const text = this.elements.input.value.trim();
        if (!text || this.isLoading) return;

        this.addMessage(text, 'user');
        this.playSound('send');
        this.elements.input.value = '';
        this.autoExpandInput();
        this.setLoading(true);

        try {
            const res = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, ai_type: this.selectedModel, session_id: this.sessionId })
            });
            const data = await res.json();
            this.setLoading(false);

            if (data.reply) {
                this.addMessage(data.reply, 'assistant', true);
            } else {
                this.addMessage('أنا هنا يا سيدي، هل تحب أن نتحدث عن شيء آخر؟', 'assistant');
            }
        } catch {
            this.setLoading(false);
            this.addMessage('أشعر ببعض الانقطاع... هل أنت بخير يا سيدي؟', 'assistant');
        }
    }

    // ==================== رفع الملفات ====================
    async handleFileUpload(file) {
        if (!file) return;
        this.addMessage(`📎 جاري تحليل ${file.name}...`, 'user');
        this.setLoading(true);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', this.sessionId);

        try {
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const data = await res.json();
            this.setLoading(false);
            this.addMessage(data.reply || 'تم تحليل الملف بنجاح.', 'assistant');
        } catch {
            this.setLoading(false);
            this.addMessage('واجهت صعوبة في تحليل الملف، لكنني سعيدة بمحاولتك.', 'assistant');
        }
    }

    handleUrlPaste() {
        const url = prompt('ألصق الرابط هنا:');
        if (url?.startsWith('http')) {
            this.elements.input.value = url;
            this.handleSendMessage();
        }
    }

    async handleClearChat() {
        if (!confirm('هل تريد أن نبدأ صفحة جديدة معاً؟')) return;

        this.elements.messages.innerHTML = '';
        localStorage.removeItem(this.storageKey);
        this.playSound('clear');

        try {
            await fetch('/clear', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
        } catch (_) {}

        this.sessionId = this._generateUUID();
        this.storageKey = `sky_history_${this.sessionId}`;
        this.addMessage('✨ تم مسح كل شيء. أنا هنا من جديد، جاهزة لك بكل حب.', 'assistant');
    }

    // ==================== إضافة رسالة + تفاعل ====================
    addMessage(content, sender, canReact = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender} animate-slide-up`;

        msgDiv.innerHTML = this.formatContent(content);

        if (sender === 'assistant') {
            // زر النسخ
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn-v2';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.onclick = () => {
                navigator.clipboard.writeText(content).then(() => {
                    copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => copyBtn.innerHTML = '<i class="fas fa-copy"></i>', 1600);
                });
            };
            msgDiv.appendChild(copyBtn);

            this.playSound('receive');

            // نظام التفاعل (RLHF)
            if (canReact) {
                const reactions = document.createElement('div');
                reactions.className = 'message-reactions';
                reactions.innerHTML = `
                    <button class="reaction-btn" data-score="1">💚</button>
                    <button class="reaction-btn" data-score="-0.5">🫂</button>
                `;

                reactions.querySelectorAll('.reaction-btn').forEach(btn => {
                    btn.addEventListener('click', async () => {
                        const score = parseFloat(btn.dataset.score);
                        this.playSound('reaction');

                        btn.style.transform = 'scale(1.4)';
                        setTimeout(() => btn.style.transform = 'scale(1)', 180);

                        try {
                            await fetch('/feedback', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    session_id: this.sessionId,
                                    score: score,
                                    comment: score > 0 ? "شعرت بالراحة" : "أحتاج تحسين"
                                })
                            });

                            if (score > 0) {
                                msgDiv.style.boxShadow = '0 0 0 4px rgba(52, 211, 153, 0.25)';
                                setTimeout(() => msgDiv.style.boxShadow = '', 1400);
                            }
                        } catch (_) {}
                    });
                });

                msgDiv.appendChild(reactions);
            }
        }

        this.elements.messages.appendChild(msgDiv);
        this.scrollToBottom();
        this.saveToLocal();
        this.updateMsgCount();
    }

    // ==================== تنسيق الرسائل (يدعم الإيموجي بشكل جميل) ====================
    formatContent(text) {
        let formatted = text
            .replace(/\n/g, '<br>')
            .replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');

        // تحسين عرض الإيموجي
        formatted = formatted.replace(/([\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}])/gu, 
            '<span style="font-size:1.15em; vertical-align:middle;">$1</span>');

        return formatted;
    }

    setLoading(isLoading) {
        this.isLoading = isLoading;
        if (this.elements.typing) this.elements.typing.classList.toggle('hidden', !isLoading);
        if (this.elements.sendBtn) {
            this.elements.sendBtn.disabled = isLoading;
            this.elements.sendBtn.style.opacity = isLoading ? '0.55' : '1';
        }
    }

    scrollToBottom(smooth = true) {
        if (!this.elements.chatArea) return;
        this.elements.chatArea.scrollTo({ top: this.elements.chatArea.scrollHeight, behavior: smooth ? 'smooth' : 'auto' });
    }

    toggleScrollButton() {
        if (!this.elements.scrollDownBtn) return;
        const nearBottom = this.elements.chatArea.scrollHeight - this.elements.chatArea.scrollTop - this.elements.chatArea.clientHeight < 100;
        this.elements.scrollDownBtn.classList.toggle('hidden', nearBottom);
    }

    autoExpandInput() {
        if (!this.elements.input) return;
        this.elements.input.style.height = 'auto';
        this.elements.input.style.height = Math.min(this.elements.input.scrollHeight, 130) + 'px';
    }

    updateMsgCount() {
        if (this.elements.msgCount) {
            const count = this.elements.messages.querySelectorAll('.message').length;
            this.elements.msgCount.textContent = `${count} رسالة`;
        }
    }

    updateUI() {
        this.updateMsgCount();
        this.elements.input?.focus();
    }

    showWelcomeIfEmpty() {
        if (this.elements.messages.children.length === 0) {
            this.addMessage('مرحباً بك يا سيدي... أنا سماء، وأنا سعيدة جداً بوجودك هنا معي.', 'assistant');
        }
    }

    saveToLocal() {
        const data = [];
        this.elements.messages.querySelectorAll('.message').forEach(m => {
            const text = m.innerText.replace(/نسخ|💚|🫂/g, '').trim();
            if (text) data.push({ content: text, sender: m.classList.contains('user') ? 'user' : 'assistant' });
        });
        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    restoreSession() {
        const saved = localStorage.getItem(this.storageKey);
        if (!saved) return;
        try {
            const history = JSON.parse(saved);
            this.elements.messages.innerHTML = '';
            history.forEach(m => this.addMessage(m.content, m.sender));
        } catch {
            this.showWelcomeIfEmpty();
        }
    }

    switchModel(target) {
        this.elements.modelBtns.forEach(b => b.classList.remove('active'));
        target.classList.add('active');
        this.selectedModel = target.dataset.model;
        localStorage.setItem('sky_model', this.selectedModel);
    }

    toggleTheme() {
        const isDark = document.documentElement.classList.contains('dark');
        this.applyTheme(isDark ? 'light' : 'dark');
    }

    applyTheme(theme) {
        document.documentElement.classList.toggle('dark', theme === 'dark');
        localStorage.setItem('sky_theme', theme);
        if (this.elements.themeSelect) this.elements.themeSelect.value = theme;
    }

    applySavedTheme() {
        const saved = localStorage.getItem('sky_theme') || 'light';
        this.applyTheme(saved);
    }

    applyFontSize(size) {
        document.querySelectorAll('.message').forEach(m => m.style.fontSize = `${size}rem`);
        localStorage.setItem('sky_font_size', size);
    }

    applySavedFontSize() {
        const saved = localStorage.getItem('sky_font_size') || '1';
        this.applyFontSize(saved);
    }

    toggleSettings(show = null) {
        if (!this.elements.settingsPanel) return;
        const shouldShow = show !== null ? show : !this.elements.settingsPanel.classList.contains('open');
        this.elements.settingsPanel.classList.toggle('open', shouldShow);
        this.elements.settingsPanel.classList.toggle('hidden', !shouldShow);
    }
}

// ==================== تشغيل ====================
document.addEventListener('DOMContentLoaded', () => {
    window.SkyUI = new SkyInterface();
});
