// ======================================================
// SkyOS v10 — UI Controller (محسّن)
// ======================================================

const SkyUI = {
  chatMessages: null,

  init() {
    this.chatMessages = document.getElementById('chat-messages');
  },

  // إضافة رسالة جديدة مع دعم أفضل للكود
  addMessage(role, content) {
    if (!this.chatMessages) this.init();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = this.parseMarkdown(content);

    messageDiv.appendChild(contentDiv);
    this.chatMessages.appendChild(messageDiv);

    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  },

  // تحويل النص مع دعم الكود
  parseMarkdown(text) {
    if (!text) return '';

    // دعم كتل الكود
    text = text.replace(/```([\s\S]*?)```/g, (match, code) => {
      return `<div class="sky-code-container">
                <div class="sky-code-header">
                  <span><i class="fas fa-code"></i> كود</span>
                  <button onclick="SkyUI.copyCode(this)" class="sky-code-copy-btn">
                    <i class="far fa-copy"></i> نسخ
                  </button>
                </div>
                <pre class="sky-code-block"><code>${code.trim()}</code></pre>
              </div>`;
    });

    // تحويل الأسطر الجديدة
    return text.replace(/\n/g, '<br>');
  },

  // نسخ الكود
  copyCode(button) {
    const codeBlock = button.closest('.sky-code-container').querySelector('code');
    if (codeBlock) {
      navigator.clipboard.writeText(codeBlock.innerText).then(() => {
        const originalText = button.innerHTML;
        button.innerHTML = `<i class="fas fa-check"></i> تم النسخ`;
        setTimeout(() => {
          button.innerHTML = originalText;
        }, 2000);
      });
    }
  },

  showThinking() {
    if (!this.chatMessages) this.init();

    const thinking = document.createElement('div');
    thinking.id = 'thinking-indicator';
    thinking.className = 'message assistant';
    thinking.innerHTML = `
      <div class="message-content">
        <i class="fas fa-circle-notch fa-spin"></i> 
        <span style="margin-right:8px;">أفكر بعمق...</span>
      </div>
    `;
    this.chatMessages.appendChild(thinking);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  },

  hideThinking() {
    const thinking = document.getElementById('thinking-indicator');
    if (thinking) thinking.remove();
  },

  showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = message;
    container.appendChild(toast);

    setTimeout(() => toast.remove(), 3200);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  SkyUI.init();
});
