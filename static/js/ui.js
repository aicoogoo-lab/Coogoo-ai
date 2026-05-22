// ======================================================
// SkyOS v10 — UI Controller (محسّن)
// ======================================================

const SkyUI = {
  chatMessages: null,

  init() {
    this.chatMessages = document.getElementById('chat-messages');
  },

  addMessage(role, content) {
    if (!this.chatMessages) this.init();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = this.parseMarkdown(content);

    const time = document.createElement('div');
    time.style.fontSize = '0.7rem';
    time.style.color = '#64748b';
    time.style.marginTop = '6px';
    time.textContent = new Date().toLocaleTimeString('ar-EG', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(time);
    this.chatMessages.appendChild(messageDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  },

  parseMarkdown(text) {
    if (!text) return '';
    text = text.replace(/```([\s\S]*?)```/g, (match, code) => {
      return `<div class="sky-code-container">
                <div class="sky-code-header">
                  <span><i class="fas fa-code"></i> كود</span>
                  <button onclick="SkyUI.copyCode(this)" class="sky-code-copy-btn">
                    <i class="far fa-copy"></i>
                  </button>
                </div>
                <pre class="sky-code-block"><code>${code.trim()}</code></pre>
              </div>`;
    });
    return text.replace(/\n/g, '<br>');
  },

  copyCode(button) {
    const code = button.closest('.sky-code-container').querySelector('code');
    if (code) {
      navigator.clipboard.writeText(code.innerText).then(() => {
        const original = button.innerHTML;
        button.innerHTML = 'تم النسخ';
        setTimeout(() => button.innerHTML = original, 2000);
      });
    }
  },

  showThinking() {
    if (!this.chatMessages) this.init();

    const thinking = document.createElement('div');
    thinking.id = 'thinking-indicator';
    thinking.className = 'message assistant thinking';
    thinking.innerHTML = `
      <div class="message-content" style="display:flex; align-items:center; gap:10px;">
        <i class="fas fa-brain fa-pulse" style="color:#a78bfa;"></i>
        <span>أفكر بعمق في سياقك...</span>
      </div>
    `;
    this.chatMessages.appendChild(thinking);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  },

  hideThinking() {
    const el = document.getElementById('thinking-indicator');
    if (el) el.remove();
  },

  showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3200);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  SkyUI.init();
});
