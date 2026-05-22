// ======================================================
// SkyOS v10 — UI Controller
// ======================================================

const SkyUI = {
  chatMessages: null,

  init() {
    this.chatMessages = document.getElementById('chat-messages');
  },

  // إضافة رسالة جديدة
  addMessage(role, content) {
    if (!this.chatMessages) this.init();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = this.parseContent(content);

    messageDiv.appendChild(contentDiv);
    this.chatMessages.appendChild(messageDiv);

    // التمرير للأسفل
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  },

  // تحويل النص (يدعم الكود حاليًا بشكل بسيط)
  parseContent(text) {
    // يمكن تطويرها لاحقًا لدعم markdown أفضل
    return text.replace(/\n/g, '<br>');
  },

  // إظهار حالة "جاري التفكير"
  showThinking() {
    if (!this.chatMessages) this.init();

    const thinkingDiv = document.createElement('div');
    thinkingDiv.id = 'thinking-indicator';
    thinkingDiv.className = 'message assistant';
    thinkingDiv.innerHTML = `
      <div class="message-content">
        <i class="fas fa-circle-notch fa-spin"></i> 
        <span style="margin-right: 8px;">أفكر...</span>
      </div>
    `;
    this.chatMessages.appendChild(thinkingDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  },

  // إخفاء حالة التفكير
  hideThinking() {
    const thinking = document.getElementById('thinking-indicator');
    if (thinking) thinking.remove();
  },

  showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3000);
  }
};

// تهيئة واجهة المستخدم
document.addEventListener('DOMContentLoaded', () => {
  SkyUI.init();
});
