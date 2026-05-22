// ======================================================
// SkyOS v10 — Core Engine (Frontend)
// ======================================================

const SkyCore = {
  state: {
    currentSessionId: null,
    messages: [],
    isProcessing: false,
  },

  // تهيئة المحرك
  init() {
    this.bindEvents();
    this.loadInitialState();
    console.log('%c[SkyCore] Frontend Core initialized', 'color:#6366f1');
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

      // Auto resize textarea
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

    // عرض الرسالة فورًا
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
          session_id: this.state.currentSessionId || 'default'
        })
      });

      const data = await response.json();

      SkyUI.hideThinking();

      if (data.reply) {
        SkyUI.addMessage('assistant', data.reply);
      } else {
        SkyUI.addMessage('assistant', 'لم أتلقَ ردًا واضحًا من النواة.');
      }

    } catch (error) {
      SkyUI.hideThinking();
      SkyUI.addMessage('assistant', 'حدث خطأ في الاتصال بالعقل الرقمي.');
      console.error(error);
    } finally {
      this.state.isProcessing = false;
    }
  },

  loadInitialState() {
    // يمكن تطويرها لاحقًا لتحميل الجلسة السابقة
    this.state.currentSessionId = 'session_' + Date.now();
  }
};

// تشغيل المحرك عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
  SkyCore.init();
});
