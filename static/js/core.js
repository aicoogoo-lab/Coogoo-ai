// ======================================================
// SkyOS v10 — Core Engine (مع الإدخال الصوتي)
// ======================================================

const SkyCore = {
  state: {
    currentSessionId: null,
    sessions: [],
    isProcessing: false,
  },

  init() {
    this.bindEvents();
    this.loadSessionsFromStorage();
    this.initFirstSession();
  },

  bindEvents() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const newSessionBtn = document.getElementById('new-session-btn');
    const voiceBtn = document.getElementById('voice-btn');

    if (sendBtn) sendBtn.addEventListener('click', () => this.sendMessage());
    if (newSessionBtn) newSessionBtn.addEventListener('click', () => this.createNewSession());

    if (userInput) {
      userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    // زر الصوت
    if (voiceBtn) {
      voiceBtn.addEventListener('click', () => this.startVoiceInput());
    }
  },

  startVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      SkyUI.showToast("المتصفح لا يدعم الإدخال الصوتي");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const input = document.getElementById('user-input');
      input.value = transcript;
      this.sendMessage();
    };

    recognition.onerror = () => {
      SkyUI.showToast("حدث خطأ أثناء الاستماع");
    };

    recognition.start();
    SkyUI.showToast("جاري الاستماع...");
  },

  createNewSession() {
    const id = 'session_' + Date.now();
    const newSession = {
      id,
      title: 'جلسة جديدة',
      messages: [],
      createdAt: new Date()
    };

    this.state.sessions.unshift(newSession);
    this.state.currentSessionId = id;
    this.saveSessionsToStorage();
    this.renderSessions();
    this.clearChat();
  },

  switchSession(id) {
    this.state.currentSessionId = id;
    this.saveSessionsToStorage();
    this.renderSessions();
    this.loadCurrentSessionMessages();
  },

  renderSessions() {
    const container = document.getElementById('session-list');
    if (!container) return;
    container.innerHTML = '';

    this.state.sessions.forEach(session => {
      const div = document.createElement('div');
      div.className = `session-item ${session.id === this.state.currentSessionId ? 'active' : ''}`;
      div.innerHTML = `
        <span>${session.title}</span>
        <button class="delete-btn"><i class="fas fa-trash"></i></button>
      `;

      div.addEventListener('click', (e) => {
        if (!e.target.closest('.delete-btn')) this.switchSession(session.id);
      });

      const delBtn = div.querySelector('.delete-btn');
      delBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.deleteSession(session.id);
      });

      container.appendChild(div);
    });
  },

  deleteSession(id) {
    this.state.sessions = this.state.sessions.filter(s => s.id !== id);
    if (this.state.currentSessionId === id) {
      this.state.currentSessionId = this.state.sessions[0]?.id || null;
    }
    this.saveSessionsToStorage();
    this.renderSessions();
    this.loadCurrentSessionMessages();
  },

  loadCurrentSessionMessages() {
    const chat = document.getElementById('chat-messages');
    chat.innerHTML = '';
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current?.messages) {
      current.messages.forEach(msg => SkyUI.addMessage(msg.role, msg.content));
    }
  },

  async sendMessage() {
    const input = document.getElementById('user-input');
    if (!input || this.state.isProcessing || !this.state.currentSessionId) return;

    const text = input.value.trim();
    if (!text) return;

    SkyUI.addMessage('user', text);
    input.value = '';
    input.style.height = 'auto';

    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current) {
      current.messages.push({ role: 'user', content: text });
      if (current.messages.length === 1) {
        current.title = text.substring(0, 30) + '...';
        this.renderSessions();
      }
    }

    this.state.isProcessing = true;
    SkyUI.showThinking();

    try {
      const res = await fetch(window.SKY_CONFIG.endpoints.chat, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: this.state.currentSessionId })
      });

      const data = await res.json();
      SkyUI.hideThinking();

      if (data.reply) {
        SkyUI.addMessage('assistant', data.reply);
        if (current) current.messages.push({ role: 'assistant', content: data.reply });
        SkyMind.increaseConfidence(1);
      }

      this.saveSessionsToStorage();
    } catch {
      SkyUI.hideThinking();
      SkyUI.addMessage('assistant', 'فشل الاتصال بالعقل الرقمي.');
    } finally {
      this.state.isProcessing = false;
    }
  },

  initFirstSession() {
    if (this.state.sessions.length === 0) {
      this.createNewSession();
    } else {
      this.state.currentSessionId = this.state.sessions[0].id;
      this.renderSessions();
      this.loadCurrentSessionMessages();
    }
  },

  loadSessionsFromStorage() {
    const saved = localStorage.getItem('skyos_sessions');
    if (saved) this.state.sessions = JSON.parse(saved);
  },

  saveSessionsToStorage() {
    localStorage.setItem('skyos_sessions', JSON.stringify(this.state.sessions));
  },

  clearChat() {
    document.getElementById('chat-messages').innerHTML = '';
  }
};

document.addEventListener('DOMContentLoaded', () => {
  SkyCore.init();
});
