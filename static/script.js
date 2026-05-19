class SkyChat {
  constructor() {
    this.messagesEl = document.getElementById('messages');
    this.input = document.getElementById('message-input');
    this.sendBtn = document.getElementById('send-btn');
    this.typing = document.getElementById('typing-indicator');
    this.clearBtn = document.getElementById('clear-chat');
    this.attachBtn = document.getElementById('attach-btn');
    this.fileInput = document.getElementById('file-input');
    this.filePreviewContainer = document.getElementById('file-preview-container');

    this.sessionId = localStorage.getItem('sky_session') || this.generateSessionId();
    this.selectedFiles = [];

    this.init();
  }

  generateSessionId() {
    const id = 'sky-' + Date.now();
    localStorage.setItem('sky_session', id);
    return id;
  }

  init() {
    this.sendBtn.addEventListener('click', () => this.sendMessage());
    this.input.addEventListener('keypress', e => {
      if (e.key === 'Enter') this.sendMessage();
    });
    this.clearBtn.addEventListener('click', () => this.clearChat());
    this.attachBtn.addEventListener('click', () => this.fileInput.click());
    this.fileInput.addEventListener('change', () => this.handleFileSelect());

    this.restoreMessages();
    this.showWelcomeIfEmpty();
  }

  async sendMessage() {
    const text = this.input.value.trim();
    if (!text && this.selectedFiles.length === 0) return;

    if (text) this.addMessage(text, 'user');
    this.input.value = '';

    // إرسال الملفات أولاً إن وجدت
    for (let file of this.selectedFiles) {
      await this.uploadFile(file);
    }
    this.selectedFiles = [];
    this.filePreviewContainer.innerHTML = '';

    if (!text) return;

    this.showTyping(true);

    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: this.sessionId })
      });
      const data = await res.json();
      this.showTyping(false);
      if (data.reply) this.addMessage(data.reply, 'assistant');
    } catch {
      this.showTyping(false);
      this.addMessage('حدث خطأ. حاول مرة أخرى.', 'assistant');
    }
  }

  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', this.sessionId);

    try {
      const res = await fetch('/upload', { method: 'POST', body: formData });
      const data = await res.json();
      if (data.reply) this.addMessage(data.reply, 'assistant');
    } catch {
      this.addMessage('فشل رفع الملف.', 'assistant');
    }
  }

  handleFileSelect() {
    const files = Array.from(this.fileInput.files);
    this.selectedFiles = [...this.selectedFiles, ...files];
    this.renderFilePreviews();
    this.fileInput.value = '';
  }

  renderFilePreviews() {
    this.filePreviewContainer.innerHTML = '';
    this.selectedFiles.forEach((file, index) => {
      const div = document.createElement('div');
      div.className = 'file-preview';
      div.innerHTML = `
        <span>${file.name}</span>
        <button onclick="window.SkyChat.removeFile(${index})">×</button>
      `;
      this.filePreviewContainer.appendChild(div);
    });
  }

  removeFile(index) {
    this.selectedFiles.splice(index, 1);
    this.renderFilePreviews();
  }

  addMessage(content, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.innerHTML = content.replace(/\n/g, '<br>');
    this.messagesEl.appendChild(div);
    this.scrollToBottom();
  }

  showTyping(show) {
    this.typing.classList.toggle('hidden', !show);
  }

  scrollToBottom() {
    document.getElementById('chat-area').scrollTop = document.getElementById('chat-area').scrollHeight;
  }

  showWelcomeIfEmpty() {
    if (this.messagesEl.children.length === 0) {
      this.addMessage('مرحباً بك... أنا سماء. كيف حالك اليوم؟', 'assistant');
    }
  }

  clearChat() {
    if (!confirm('مسح المحادثة؟')) return;
    this.messagesEl.innerHTML = '';
    localStorage.removeItem('sky_session');
    this.sessionId = this.generateSessionId();
    this.showWelcomeIfEmpty();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.SkyChat = new SkyChat();
});
