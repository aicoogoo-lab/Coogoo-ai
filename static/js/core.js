// ======================================================
// سماء • المحرك الأساسي + نظام محادثة HoloLiquid Neo-AI
// ======================================================

const SkyCore = {
  state: {
    currentSessionId: null,
    sessions: [],
    isProcessing: false,
    currentTheme: 'dark',
    imagePreview: null,
    imageFile: null,
    archive: [],
    maxVisible: 20,
    showArchive: false
  },

  init() {
    this.loadSessions();
    this.initFirstSession();
    this.bindEvents();
    this.initTheme();
    this.renderSessions();
    this.initArchiveToggle();
    this.renderMessages();
    console.log('✅ سماء + HoloLiquid Neo-AI جاهزة');
  },

  // ==================== زر أرشيف HoloLiquid ====================
  initArchiveToggle() {
    const messagesContainer = document.getElementById('messages-list');
    if (!messagesContainer) return;
    
    // إزالة الزر القديم إن وجد
    const existingBtn = document.getElementById('archive-toggle-btn');
    if (existingBtn) existingBtn.remove();
    
    // إنشاء زر الأرشيف الجديد
    const arrowBtn = document.createElement("button");
    arrowBtn.id = 'archive-toggle-btn';
    arrowBtn.className = "icon-btn neo-glow";
    arrowBtn.style.cssText = "margin: 10px auto; display: block;";
    arrowBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
    arrowBtn.title = 'عرض كل الرسائل';
    arrowBtn.onclick = () => this.toggleArchive();
    
    // إدراج الزر قبل قائمة الرسائل
    const parent = messagesList.parentElement;
    if (parent) {
      parent.insertBefore(arrowBtn, messagesList);
    }
  },

  toggleArchive() {
    this.state.showArchive = !this.state.showArchive;
    this.renderMessages();
    
    const arrowBtn = document.getElementById('archive-toggle-btn');
    if (arrowBtn) {
      arrowBtn.innerHTML = this.state.showArchive
        ? '<i class="fas fa-chevron-up"></i>'
        : '<i class="fas fa-chevron-down"></i>';
      arrowBtn.title = this.state.showArchive ? 'إخفاء الأرشيف' : 'عرض كل الرسائل';
    }
  },

  // ==================== عرض الرسائل (HoloLiquid) ====================
  renderMessages() {
    const container = document.getElementById('messages-list');
    if (!container) return;

    container.innerHTML = '';

    const session = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    const archive = session ? session.messages : [];
    
    let visible = this.state.showArchive 
      ? archive 
      : archive.slice(-this.state.maxVisible);

    if (visible.length === 0) {
      // رسالة ترحيب
      const welcomeDiv = document.createElement('div');
      welcomeDiv.className = 'message assistant';
      welcomeDiv.innerHTML = `
        <div class="message-avatar"><i class="fas fa-sparkles"></i></div>
        <div class="message-bubble">
          <div class="message-text">مرحباً بك في سماء. كيف يمكنني مساعدتك اليوم؟</div>
          <div class="message-time">الآن</div>
          <div class="message-actions">
            <button class="msg-action copy-msg"><i class="far fa-copy"></i> نسخ</button>
            <button class="msg-action share-msg"><i class="fas fa-share-alt"></i> مشاركة</button>
            <button class="msg-action export-all"><i class="fas fa-download"></i> تصدير</button>
          </div>
        </div>
      `;
      container.appendChild(welcomeDiv);
      this.bindMessageActions(welcomeDiv, 'مرحباً بك في سماء. كيف يمكنني مساعدتك اليوم؟');
    } else {
      visible.forEach((msg, index) => {
        const div = document.createElement('div');
        div.className = `message ${msg.role}`;
        div.dataset.index = index;
        
        const time = msg.timestamp 
          ? new Date(msg.timestamp).toLocaleTimeString('ar', { hour: '2-digit', minute: '2-digit' }) 
          : 'الآن';
        
        const avatarIcon = msg.role === 'user' 
          ? '<i class="fas fa-user"></i>' 
          : '<i class="fas fa-sparkles"></i>';
        
        div.innerHTML = `
          <div class="message-avatar">${avatarIcon}</div>
          <div class="message-bubble">
            <div class="message-text">${this.escapeHtml(msg.content)}</div>
            <div class="message-time">${time}</div>
            <div class="message-actions">
              <button class="msg-action copy-msg"><i class="far fa-copy"></i> نسخ</button>
              <button class="msg-action share-msg"><i class="fas fa-share-alt"></i> مشاركة</button>
              ${msg.role === 'assistant' && index === visible.length - 1 ? '<button class="msg-action regenerate-msg"><i class="fas fa-undo-alt"></i> إعادة</button>' : ''}
              <button class="msg-action export-all"><i class="fas fa-download"></i> تصدير</button>
            </div>
          </div>
        `;
        
        container.appendChild(div);
        this.bindMessageActions(div, msg.content);
      });
    }

    // تحديث زر الأرشيف
    this.updateArchiveButton(archive.length);

    // تمرير للأسفل
    setTimeout(() => {
      container.scrollTop = container.scrollHeight;
    }, 50);
  },

  updateArchiveButton(totalMessages) {
    const arrowBtn = document.getElementById('archive-toggle-btn');
    if (!arrowBtn) return;
    
    if (totalMessages <= this.state.maxVisible) {
      arrowBtn.style.display = 'none';
    } else {
      arrowBtn.style.display = 'block';
      arrowBtn.innerHTML = this.state.showArchive
        ? '<i class="fas fa-chevron-up"></i>'
        : '<i class="fas fa-chevron-down"></i>';
    }
  },

  bindMessageActions(messageDiv, content) {
    const copyBtn = messageDiv.querySelector('.copy-msg');
    const shareBtn = messageDiv.querySelector('.share-msg');
    const regenerateBtn = messageDiv.querySelector('.regenerate-msg');
    const exportBtn = messageDiv.querySelector('.export-all');
    
    if (copyBtn) {
      copyBtn.onclick = (e) => {
        e.stopPropagation();
        this.copyText(content);
      };
    }
    if (shareBtn) {
      shareBtn.onclick = (e) => {
        e.stopPropagation();
        this.shareText(content);
      };
    }
    if (regenerateBtn) {
      regenerateBtn.onclick = (e) => {
        e.stopPropagation();
        this.regenerateLastMessage();
      };
    }
    if (exportBtn) {
      exportBtn.onclick = (e) => {
        e.stopPropagation();
        this.exportChat();
      };
    }
  },

  bindEvents() {
    const sendBtn = document.getElementById('send-btn');
    const input = document.getElementById('message-input');
    const newSessionBtn = document.getElementById('new-session-btn');
    const newSessionHeader = document.getElementById('new-session-header');
    const voiceBtn = document.getElementById('voice-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const themeToggle = document.getElementById('theme-toggle');
    const removePreview = document.getElementById('remove-preview');

    if (sendBtn) sendBtn.addEventListener('click', () => this.sendMessage());
    if (newSessionBtn) newSessionBtn.addEventListener('click', () => this.newSession());
    if (newSessionHeader) newSessionHeader.addEventListener('click', () => this.newSession());
    if (voiceBtn) voiceBtn.addEventListener('click', () => this.startVoice());
    if (uploadBtn) uploadBtn.addEventListener('click', () => this.uploadImage());
    if (removePreview) removePreview.addEventListener('click', () => this.clearImagePreview());
    if (themeToggle) themeToggle.addEventListener('click', () => this.toggleTheme());

    if (input) {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    if (menuToggle && sidebar) {
      menuToggle.addEventListener('click', () => sidebar.classList.toggle('mobile-open'));
      document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
          sidebar.classList.remove('mobile-open');
        }
      });
    }
  },

  // ==================== الثيم ====================
  initTheme() {
    const saved = localStorage.getItem('sky_theme');
    if (saved === 'light') {
      this.state.currentTheme = 'light';
      document.body.classList.add('light-theme');
      const themeName = document.getElementById('theme-name');
      if (themeName) themeName.textContent = 'فاتح';
    }
  },

  toggleTheme() {
    const themeName = document.getElementById('theme-name');
    if (this.state.currentTheme === 'dark') {
      this.state.currentTheme = 'light';
      document.body.classList.add('light-theme');
      if (themeName) themeName.textContent = 'فاتح';
      localStorage.setItem('sky_theme', 'light');
    } else {
      this.state.currentTheme = 'dark';
      document.body.classList.remove('light-theme');
      if (themeName) themeName.textContent = 'داكن';
      localStorage.setItem('sky_theme', 'dark');
    }
    this.showToast(`الثيم: ${this.state.currentTheme === 'dark' ? 'داكن' : 'فاتح'}`, 'info');
  },

  // ==================== الصور ====================
  uploadImage() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
      const file = e.target.files[0];
      if (file) this.previewImage(file);
    };
    input.click();
  },

  previewImage(file) {
    const reader = new FileReader();
    reader.onload = (ev) => {
      this.state.imagePreview = ev.target.result;
      this.state.imageFile = file;
      const previewArea = document.getElementById('image-preview-area');
      const previewImg = document.getElementById('preview-img');
      if (previewArea && previewImg) {
        previewImg.src = ev.target.result;
        previewArea.style.display = 'block';
      }
    };
    reader.readAsDataURL(file);
  },

  clearImagePreview() {
    this.state.imagePreview = null;
    this.state.imageFile = null;
    const previewArea = document.getElementById('image-preview-area');
    if (previewArea) previewArea.style.display = 'none';
  },

  // ==================== الجلسات ====================
  newSession() {
    const id = Date.now().toString();
    const newSession = {
      id: id,
      title: 'محادثة جديدة',
      messages: [],
      createdAt: new Date().toISOString()
    };
    this.state.sessions.unshift(newSession);
    this.state.currentSessionId = id;
    this.state.showArchive = false;
    this.saveSessions();
    this.renderSessions();
    this.renderMessages();
    this.initArchiveToggle();
    this.showToast('محادثة جديدة', 'success');
  },

  switchSession(id) {
    this.state.currentSessionId = id;
    this.state.showArchive = false;
    this.saveSessions();
    this.renderSessions();
    this.renderMessages();
    this.initArchiveToggle();
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.remove('mobile-open');
  },

  deleteSession(id, event) {
    if (event) event.stopPropagation();
    this.state.sessions = this.state.sessions.filter(s => s.id !== id);
    if (this.state.currentSessionId === id) {
      this.state.currentSessionId = this.state.sessions[0]?.id || null;
    }
    this.saveSessions();
    this.renderSessions();
    if (this.state.currentSessionId) {
      this.renderMessages();
    } else {
      this.newSession();
    }
    this.showToast('تم حذف المحادثة', 'info');
  },

  renderSessions() {
    const container = document.getElementById('session-list');
    if (!container) return;
    container.innerHTML = '';
    this.state.sessions.forEach(session => {
      const div = document.createElement('div');
      div.className = `session-item ${session.id === this.state.currentSessionId ? 'active' : ''}`;
      div.innerHTML = `
        <i class="far fa-comment"></i>
        <span>${session.title}</span>
        <button class="delete-session" data-id="${session.id}"><i class="fas fa-trash"></i></button>
      `;
      div.addEventListener('click', (e) => {
        if (!e.target.closest('.delete-session')) this.switchSession(session.id);
      });
      const delBtn = div.querySelector('.delete-session');
      delBtn.addEventListener('click', (e) => this.deleteSession(session.id, e));
      container.appendChild(div);
    });
  },

  // ==================== الإجراءات ====================
  copyText(text) {
    navigator.clipboard.writeText(text);
    this.showToast('تم النسخ', 'success');
  },

  shareText(text) {
    if (navigator.share) {
      navigator.share({ text: text });
    } else {
      this.copyText(text);
      this.showToast('تم النسخ (المشاركة غير مدعومة)', 'info');
    }
  },

  exportChat() {
    const session = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (!session) return;
    const content = session.messages.map(m => `${m.role === 'user' ? '👤' : '🤖'}: ${m.content}`).join('\n\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `سماء_${session.title}.txt`;
    a.click();
    URL.revokeObjectURL(a.href);
    this.showToast('تم تصدير المحادثة', 'success');
  },

  async regenerateLastMessage() {
    const session = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (!session || session.messages.length < 2) return;
    
    const lastUserMsg = [...session.messages].reverse().find(m => m.role === 'user');
    if (!lastUserMsg) return;
    
    // حذف آخر رد
    const lastAssistantIndex = session.messages.map(m => m.role).lastIndexOf('assistant');
    if (lastAssistantIndex !== -1) session.messages.splice(lastAssistantIndex, 1);
    this.saveSessions();
    this.renderMessages();
    
    await this.getAIResponse(lastUserMsg.content);
  },

  // ==================== الإدخال الصوتي ====================
  startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      this.showToast('المتصفح لا يدعم الإدخال الصوتي', 'error');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      const input = document.getElementById('message-input');
      if (input) input.value = text;
      this.sendMessage();
    };
    recognition.onerror = () => this.showToast('حدث خطأ في الاستماع', 'error');
    recognition.start();
    this.showToast('جاري الاستماع...', 'info');
  },

  // ==================== إرسال الرسالة (HoloLiquid) ====================
  async sendMessage() {
    const input = document.getElementById('message-input');
    const text = input?.value.trim();
    
    if (!text && !this.state.imagePreview) return;
    if (this.state.isProcessing) return;
    
    let messageText = text || '';
    
    if (this.state.imagePreview) {
      const imageInfo = `[صورة: ${this.state.imageFile?.name || 'صورة'}]`;
      messageText = messageText ? `${imageInfo}\n${messageText}` : imageInfo;
    }
    
    // إضافة رسالة المستخدم
    const session = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (session) {
      session.messages.push({ role: 'user', content: messageText || 'صورة', timestamp: Date.now() });
      if (session.messages.length === 1 && text) {
        session.title = text.substring(0, 25);
        this.renderSessions();
      }
      this.saveSessions();
    }
    
    // تحديث الواجهة
    this.renderMessages();
    this.clearImagePreview();
    if (input) input.value = '';
    
    await this.getAIResponse(messageText);
  },

  async getAIResponse(userMessage) {
    this.state.isProcessing = true;
    this.showTyping();
    
    try {
      const reply = this.getSmartReply(userMessage);
      await new Promise(r => setTimeout(r, 800 + Math.random() * 500));
      
      this.hideTyping();
      
      const session = this.state.sessions.find(s => s.id === this.state.currentSessionId);
      if (session) {
        session.messages.push({ role: 'assistant', content: reply, timestamp: Date.now() });
        this.saveSessions();
      }
      
      this.renderMessages();
    } catch (err) {
      this.hideTyping();
      
      const session = this.state.sessions.find(s => s.id === this.state.currentSessionId);
      if (session) {
        session.messages.push({ role: 'assistant', content: 'عذراً، حدث خطأ. حاول مرة أخرى.', timestamp: Date.now() });
        this.saveSessions();
      }
      
      this.renderMessages();
    } finally {
      this.state.isProcessing = false;
    }
  },

  showTyping() {
    const container = document.getElementById('messages-list');
    if (!container) return;
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
      <div class="message-avatar"><i class="fas fa-sparkles"></i></div>
      <div class="message-bubble">
        <div class="thinking-indicator">
          <div class="thinking-dots"><span></span><span></span><span></span></div>
          <span>يكتب...</span>
        </div>
      </div>
    `;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
  },

  hideTyping() {
    const typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
  },

  getSmartReply(message) {
    const lower = message.toLowerCase();
    
    if (lower.includes('مرحب') || lower.includes('السلام')) {
      return 'أهلاً بك! كيف يمكنني مساعدتك اليوم؟';
    }
    if (lower.includes('شكر')) {
      return 'العفو! أنا سعيد بمساعدتك. هل هناك شيء آخر تحتاجه؟';
    }
    if (lower.includes('كيف حال')) {
      return 'أنا بخير، شكراً لسؤالك. كيف يمكنني مساعدتك؟';
    }
    if (lower.includes('صور') || lower.includes('صورة')) {
      return 'يمكنك رفع الصور بالضغط على أيقونة الصورة 📷 أو لصقها مباشرة.';
    }
    if (lower.includes('صوت') || lower.includes('تكلم')) {
      return 'يمكنك استخدام الإدخال الصوتي بالضغط على أيقونة الميكروفون 🎤';
    }
    if (lower.includes('ذاكرة') || lower.includes('تذكر')) {
      return `لديك ${this.state.sessions.length} جلسة محفوظة في الذاكرة. يمكنك التبديل بينها من القائمة الجانبية.`;
    }
    if (lower.includes('وداع')) {
      return 'وداعاً! أتمنى لك يوماً جميلاً. عد متى شئت.';
    }
    
    const responses = [
      'هذا مثير للاهتمام! هل تريد التعمق أكثر في هذا الموضوع؟',
      'فهمت وجهة نظرك. ماذا تقترح كخطوة تالية؟',
      'شكراً لمشاركتك. هل هناك تفاصيل إضافية تود إضافتها؟',
      'أرى. دعني أفكر في ذلك قليلاً... ماذا تتوقع أن يحدث بعد ذلك؟',
      'جميل! هل لديك أي سؤال محدد حول هذا؟',
      'تم استلام رسالتك. هذا رد تجريبي ويمكن ربطه بـ API خارجي للحصول على ردود ذكية.'
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  },

  // ==================== مساعدة ====================
  escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
      if (m === '&') return '&amp;';
      if (m === '<') return '&lt;';
      if (m === '>') return '&gt;';
      return m;
    }).replace(/\n/g, '<br>');
  },

  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
  },

  loadSessions() {
    const saved = localStorage.getItem('sky_sessions');
    if (saved) {
      this.state.sessions = JSON.parse(saved);
    } else {
      this.state.sessions = [];
    }
  },

  saveSessions() {
    localStorage.setItem('sky_sessions', JSON.stringify(this.state.sessions));
  },

  initFirstSession() {
    if (this.state.sessions.length === 0) {
      const id = Date.now().toString();
      const newSession = {
        id: id,
        title: 'محادثة جديدة',
        messages: [],
        createdAt: new Date().toISOString()
      };
      this.state.sessions.unshift(newSession);
      this.state.currentSessionId = id;
      this.saveSessions();
    } else {
      this.state.currentSessionId = this.state.sessions[0].id;
    }
  }
};

window.SkyCore = SkyCore;
