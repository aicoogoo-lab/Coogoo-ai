// ======================================================
// SkyOS v10 — Core Engine (محسّن)
// ======================================================

const SkyCore = {
  state: {
    currentSessionId: null,
    isProcessing: false,
  },

  init() {
    this.bindEvents();
    this.loadInitialState();
    console.log('%c[SkyCore] Core Engine initialized', 'color:#6366f1');
  },

  bindEvents() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');

    if (sendBtn) {
      sendBtn.addEventListener('click', () => this.sendMessage());
    }

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

  async sendMessage() {
    const input = document.getElementById('user-input');
    if (!input || this.state.isProcessing) return;

    const text = input.value.trim();
    if (!text) return;

    SkyUI.addMessage('user', text);
    input.value = '';
    input.style.height = 'auto';

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
        SkyMind.increaseConfidence(1); // زيادة الثقة عند الرد الناجح
      } else {
        SkyUI.addMessage('assistant', 'لم أتلق ردًا واضحًا.');
      }

    } catch (error) {
      SkyUI.hideThinking();
      SkyUI.addMessage('assistant', 'فشل الاتصال بالعقل الرقمي.');
      console.error(error);
    } finally {
      this.state.isProcessing = false;
    }
  },

  loadInitialState() {
    this.state.currentSessionId = 'session_' + Date.now();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  SkyCore.init();
});
