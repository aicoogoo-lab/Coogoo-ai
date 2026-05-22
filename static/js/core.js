// ======================================================
// SkyOS v10 — Core Engine (مع إدارة الجلسات)
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
    console.log('%c[SkyCore] Core initialized with session support', 'color:#6366f1');
  },

  bindEvents() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const newSessionBtn = document.getElementById('new-session-btn');

    if (sendBtn) sendBtn.addEventListener('click', () => this.sendMessage());
    if (newSessionBtn) newSessionBtn.addEventListener('click', () => this.createNewSession());

    if (userInput) {
      userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
      userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 140) + 'px';
      });
    }
  },

  createNewSession() {
    const id = 'session_' + Date.now();
    const newSession = {
      id: id,
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
        if (!e.target.closest('.delete-btn')) {
          this.switchSession(session.id);
        }
      });

      // زر الحذف
      const deleteBtn = div.querySelector('.delete-btn');
      deleteBtn.addEventListener('click', (e) => {
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
    const chatWindow = document.getElementById('chat-messages');
    chatWindow.innerHTML = '';

    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current && current.messages) {
      current.messages.forEach(msg => {
        SkyUI.addMessage(msg.role, msg.content);
      });
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

    // حفظ الرسالة في الجلسة الحالية
    const currentSession = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (currentSession) {
      currentSession.messages.push({ role: 'user', content: text });
      if (currentSession.messages.length === 1) {
        currentSession.title = text.substring(0, 30) + '...';
        this.renderSessions();
      }
    }

    this.state.isProcessing = true;
    SkyUI.showThinking();

    try {
      const response = await fetch(window.SKY_CONFIG.endpoints.chat, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: this.state.currentSessionId
        })
      });

      const data = await response.json();
      SkyUI.hideThinking();

      if (data.reply) {
        SkyUI.addMessage('assistant', data.reply);
        if (currentSession) {
          currentSession.messages.push({ role: 'assistant', content: data.reply });
        }
        SkyMind.increaseConfidence(1);
      }

      this.saveSessionsToStorage();

    } catch (error) {
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
    if (saved) {
      this.state.sessions = JSON.parse(saved);
    }
  },

  saveSessionsToStorage() {
    localStorage.setItem('skyos_sessions', JSON.stringify(this.state.sessions));
  },

  clearChat() {
    const chatWindow = document.getElementById('chat-messages');
    chatWindow.innerHTML = '';
  }
};

document.addEventListener('DOMContentLoaded', () => {
  SkyCore.init();
});
