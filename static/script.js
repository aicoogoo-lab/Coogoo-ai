// static/script.js - Sky AI Professional Frontend Engine v2.0 (متكامل)

class SkyInterface {
    constructor() {
        this.elements = {
            chatArea: document.querySelector('#chat-area') || document.querySelector('#chat-container'),
            messages: document.querySelector('#messages'),
            input: document.querySelector('#message-input') || document.querySelector('#userInput'),
            sendBtn: document.querySelector('#send-btn') || document.querySelector('#sendBtn'),
            typing: document.querySelector('#typing-indicator') || document.querySelector('#typing'),
            msgCount: document.querySelector('#msg-count'),
            charCounter: document.querySelector('#char-counter'),
            fileUpload: document.querySelector('#file-upload'),
            uploadLabel: document.querySelector('#upload-label'),
            urlTrigger: document.querySelector('#url-trigger') || document.querySelector('#url-btn'),
            clearBtn: document.querySelector('#clear-chat') || document.querySelector('#clearChat'),
            scrollDownBtn: document.querySelector('#scrollDown') || document.querySelector('#scrollTopBtn'),
            settingsBtn: document.querySelector('#settings-drawer-btn') || document.querySelector('#settingsToggle'),
            settingsPanel: document.querySelector('#settings-drawer') || document.querySelector('#settingsPanel'),
            closeSettings: document.querySelector('#close-drawer') || document.querySelector('#closeSettings'),
            themeToggle: document.querySelector('#theme-toggle'),
            themeSelect: document.querySelector('#theme-select'),
            fontSizeSelect: document.querySelector('#font-size-select'),
            defaultModelSelect: document.querySelector('#default-model-select') || document.querySelector('#default-model'),
            modelBtns: document.querySelectorAll('.model-pill')
        };

        this.sessionId = localStorage.getItem('sky_session_v2') || this.generateUUID();
        this.selectedModel = localStorage.getItem('sky_model') || 'groq';
        this.storageKey = `history_${this.sessionId}`;

        this.init();
    }

    init() {
        this.bindEvents();
        this.restoreSession();
        this.applySavedTheme();
        this.applySavedFontSize();
        this.updateUI();
        console.log(`🔥 Sky Engine Active. Session: ${this.sessionId}`);
    }

    generateUUID() {
        const id = 'sky-' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
        localStorage.setItem('sky_session_v2', id);
        return id;
    }

    // ========== ربط الأحداث ==========
    bindEvents() {
        // إرسال
        if (this.elements.sendBtn) {
            this.elements.sendBtn.addEventListener('click', () => this.handleSendMessage());
        }
        if (this.elements.input) {
            this.elements.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSendMessage();
                }
            });
            this.elements.input.addEventListener('input', () => {
                if (this.elements.charCounter) {
                    this.elements.charCounter.innerText = `${this.elements.input.value.length} / 2000`;
                }
                this.autoExpandInput();
            });
        }

        // النماذج
        this.elements.modelBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchModel(e.currentTarget));
        });
        if (this.elements.defaultModelSelect) {
            this.elements.defaultModelSelect.value = this.selectedModel;
            this.elements.defaultModelSelect.addEventListener('change', (e) => {
                this.switchModelByValue(e.target.value);
            });
        }

        // رفع ملفات
        if (this.elements.uploadLabel && this.elements.fileUpload) {
            this.elements.uploadLabel.addEventListener('click', () => this.elements.fileUpload.click());
        }
        if (this.elements.fileUpload) {
            this.elements.fileUpload.addEventListener('change', (e) => {
                if (e.target.files[0]) {
                    this.handleFileUpload(e.target.files[0]);
                    this.elements.fileUpload.value = '';
                }
            });
        }

        // روابط
        if (this.elements.urlTrigger) {
            this.elements.urlTrigger.addEventListener('click', () => this.handleUrlPaste());
        }

        // مسح
        if (this.elements.clearBtn) {
            this.elements.clearBtn.addEventListener('click', () => this.handleClearChat());
        }

        // إعدادات
        if (this.elements.settingsBtn && this.elements.settingsPanel) {
            this.elements.settingsBtn.addEventListener('click', () => {
                this.elements.settingsPanel.classList.toggle('open');
                this.elements.settingsPanel.classList.toggle('hidden');
            });
        }
        if (this.elements.closeSettings && this.elements.settingsPanel) {
            this.elements.closeSettings.addEventListener('click', () => {
                this.elements.settingsPanel.classList.remove('open');
                this.elements.settingsPanel.classList.add('hidden');
            });
        }
        if (this.elements.settingsPanel) {
            this.elements.settingsPanel.addEventListener('click', (e) => {
                if (e.target === this.elements.settingsPanel) {
                    this.elements.settingsPanel.classList.remove('open');
                    this.elements.settingsPanel.classList.add('hidden');
                }
            });
        }

        // ثيم
        if (this.elements.themeToggle) {
            this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
        if (this.elements.themeSelect) {
            this.elements.themeSelect.addEventListener('change', (e) => this.applyTheme(e.target.value));
        }

        // حجم الخط
        if (this.elements.fontSizeSelect) {
            this.elements.fontSizeSelect.addEventListener('change', (e) => this.applyFontSize(e.target.value));
        }

        // زر النزول للأسفل
        if (this.elements.scrollDownBtn && this.elements.chatArea) {
            this.elements.chatArea.addEventListener('scroll', () => {
                const nearBottom = this.elements.chatArea.scrollHeight - this.elements.chatArea.scrollTop - this.elements.chatArea.clientHeight < 80;
                this.elements.scrollDownBtn.classList.toggle('hidden', nearBottom);
            });
            this.elements.scrollDownBtn.addEventListener('click', () => this.scrollToBottom());
        }

        // التركيز
        if (this.elements.input) this.elements.input.focus();
    }

    // ========== الإرسال ==========
    async handleSendMessage() {
        const text = this.elements.input.value.trim();
        if (!text) return;

        this.addMessage(text, 'user');
        this.elements.input.value = '';
        this.autoExpandInput();
        this.setLoading(true);

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    ai_type: this.selectedModel,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();
            this.setLoading(false);

            if (data.reply) {
                this.addMessage(data.reply, 'assistant');
            } else {
                this.addMessage('⚠️ لم يصل رد من سماء.', 'assistant');
            }
        } catch (error) {
            this.setLoading(false);
            this.addMessage('⚠️ فشل الاتصال بالخادم. تأكد من الإنترنت.', 'assistant');
        }
    }

    // ========== رفع الملفات ==========
    async handleFileUpload(file) {
        if (!file) return;
        this.addMessage(`📎 جاري رفع وتحليل: ${file.name}`, 'user');
        this.setLoading(true);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', this.sessionId);

        try {
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const data = await res.json();
            this.setLoading(false);
            this.addMessage(data.reply || 'تم استلام الملف.', 'assistant');
        } catch (e) {
            this.setLoading(false);
            this.addMessage('⚠️ فشل رفع الملف.', 'assistant');
        }
    }

    // ========== روابط ==========
    handleUrlPaste() {
        const url = prompt('🔗 ألصق الرابط هنا:');
        if (url && url.startsWith('http')) {
            this.elements.input.value = url;
            this.handleSendMessage();
        } else if (url) {
            alert('يرجى إدخال رابط صحيح يبدأ بـ http:// أو https://');
        }
    }

    // ========== مسح ==========
    async handleClearChat() {
        if (!confirm('هل تريد مسح كل المحادثة؟')) return;
        this.elements.messages.innerHTML = '';
        localStorage.removeItem(this.storageKey);

        try {
            await fetch('/clear', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
        } catch (e) {}

        this.sessionId = this.generateUUID();
        this.storageKey = `history_${this.sessionId}`;
        this.addMessage('✨ تم مسح المحادثة. ابدأ من جديد.', 'assistant');
    }

    // ========== واجهة ==========
    addMessage(content, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender} animate-slide-up`;

        const formatted = this.formatContent(content);
        msgDiv.innerHTML = formatted;

        if (sender === 'assistant') {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn-v2';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.title = 'نسخ';
            copyBtn.onclick = () => {
                navigator.clipboard.writeText(content).then(() => {
                    copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => copyBtn.innerHTML = '<i class="fas fa-copy"></i>', 2000);
                });
            };
            msgDiv.appendChild(copyBtn);
        }

        this.elements.messages.appendChild(msgDiv);
        this.scrollToBottom();
        this.saveToLocal();
        this.updateMsgCount();
    }

    formatContent(text) {
        let formatted = text
            .replace(/\n/g, '<br>')
            .replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>')
            .replace(/`([^`]+)`/g, '<code>$1</code>');
        return formatted;
    }

    setLoading(isLoading) {
        if (this.elements.typing) {
            this.elements.typing.classList.toggle('hidden', !isLoading);
        }
        if (this.elements.sendBtn) {
            this.elements.sendBtn.disabled = isLoading;
            this.elements.sendBtn.style.opacity = isLoading ? '0.5' : '1';
        }
    }

    scrollToBottom() {
        if (this.elements.chatArea) {
            this.elements.chatArea.scrollTo({
                top: this.elements.chatArea.scrollHeight,
                behavior: 'smooth'
            });
        }
    }

    autoExpandInput() {
        if (this.elements.input) {
            this.elements.input.style.height = 'auto';
            this.elements.input.style.height = this.elements.input.scrollHeight + 'px';
        }
    }

    updateMsgCount() {
        if (this.elements.msgCount) {
            const count = this.elements.messages.querySelectorAll('.message').length;
            this.elements.msgCount.innerText = `${count} رسالة`;
        }
    }

    saveToLocal() {
        const data = [];
        this.elements.messages.querySelectorAll('.message').forEach(m => {
            const text = m.innerText.replace(/نسخ|📋|✅|✓/g, '').trim();
            if (text) {
                data.push({
                    content: text,
                    sender: m.classList.contains('user') ? 'user' : 'assistant'
                });
            }
        });
        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    restoreSession() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved) {
            try {
                const history = JSON.parse(saved);
                this.elements.messages.innerHTML = '';
                history.forEach(m => this.addMessage(m.content, m.sender));
            } catch (e) {
                this.addMessage('✨ مرحباً بك في سماء! ✨', 'assistant');
            }
        }
    }

    // ========== النماذج ==========
    switchModel(target) {
        this.elements.modelBtns.forEach(b => b.classList.remove('active'));
        target.classList.add('active');
        this.selectedModel = target.dataset.model;
        localStorage.setItem('sky_model', this.selectedModel);
        if (this.elements.defaultModelSelect) this.elements.defaultModelSelect.value = this.selectedModel;
    }

    switchModelByValue(model) {
        this.selectedModel = model;
        localStorage.setItem('sky_model', model);
        this.elements.modelBtns.forEach(b => {
            b.classList.toggle('active', b.dataset.model === model);
        });
    }

    // ========== الثيم ==========
    toggleTheme() {
        const current = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = current === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }

    applyTheme(theme) {
        if (theme === 'dark') document.documentElement.classList.add('dark');
        else document.documentElement.classList.remove('dark');
        localStorage.setItem('sky_theme', theme);
        if (this.elements.themeSelect) this.elements.themeSelect.value = theme;
    }

    applySavedTheme() {
        const saved = localStorage.getItem('sky_theme') || 'light';
        this.applyTheme(saved);
    }

    // ========== حجم الخط ==========
    applyFontSize(size) {
        document.querySelectorAll('.message').forEach(m => m.style.fontSize = `${size}rem`);
        localStorage.setItem('sky_font_size', size);
        if (this.elements.fontSizeSelect) this.elements.fontSizeSelect.value = size;
    }

    applySavedFontSize() {
        const saved = localStorage.getItem('sky_font_size') || '1';
        this.applyFontSize(saved);
    }

    // ========== تحديث الواجهة ==========
    updateUI() {
        this.updateMsgCount();
        if (this.elements.input) this.elements.input.focus();
    }
}

// ========== بدء التشغيل ==========
document.addEventListener('DOMContentLoaded', () => {
    window.SkyUI = new SkyInterface();
});
