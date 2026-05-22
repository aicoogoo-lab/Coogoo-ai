// ======================================================
// SkyOS v10 — Core Engine (متكامل بالكامل مع العقل الهولوغرافي)
// ======================================================

const SkyCore = {
  state: {
    currentSessionId: null,
    sessions: [],
    isProcessing: false,
    useMockApi: true  // مؤقتاً للتجربة (يمكن تغييره لاحقاً)
  },

  init() {
    this.bindEvents();
    this.loadSessionsFromStorage();
    this.initFirstSession();
    
    // ربط أحداث العقل إذا كان SkyMind موجوداً
    if (window.SkyMind) {
      console.log('[SkyCore] Connected to SkyMind');
    }
  },

  bindEvents() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const newSessionBtn = document.getElementById('new-session-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    if (sendBtn) {
      sendBtn.addEventListener('click', () => {
        if (window.SkyUI) window.SkyUI.rippleEffect(sendBtn);
        this.sendMessage();
      });
    }
    if (newSessionBtn) newSessionBtn.addEventListener('click', () => this.createNewSession());
    if (voiceBtn) voiceBtn.addEventListener('click', () => this.startVoiceInput());
    if (uploadBtn) uploadBtn.addEventListener('click', () => this.handleFileUpload());

    if (userInput) {
      userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    // زر القائمة على الجوال
    if (menuToggle && sidebar) {
      menuToggle.style.display = 'flex';
      menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('mobile-open');
      });

      document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
          sidebar.classList.remove('mobile-open');
        }
      });
    }
  },

  updateHeaderTitle() {
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    const header = document.querySelector('.sky-chat-title');
    if (header && current) {
      header.innerHTML = `<i class="fas fa-terminal"></i> ${current.title.substring(0, 40)}`;
    }
  },

  // تحسين رفع الملفات مع دعم أنواع متعددة
  handleFileUpload() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*,text/plain,application/pdf';
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file || !this.state.currentSessionId) return;

      if (window.SkyUI) {
        SkyUI.addMessage('user', `📎 جاري رفع الملف: ${file.name} (${(file.size / 1024).toFixed(1)} KB)...`);
      }

      const formData = new FormData();
      formData.append('file', file);

      try {
        let response;
        if (this.state.useMockApi) {
          // محاكاة الرفع
          await new Promise(r => setTimeout(r, 800));
          response = { 
            success: true, 
            analysis: { 
              description: `تم استلام ملف ${file.name} بنجاح. حجمه ${(file.size / 1024).toFixed(1)} كيلوبايت.` 
            } 
          };
        } else {
          const res = await fetch('/upload', { method: 'POST', body: formData });
          response = await res.json();
        }

        if (response.success) {
          let msg = `✅ تم رفع الملف: ${file.name}`;
          if (response.analysis?.description) {
            msg += `\n\n${response.analysis.description}`;
          }
          if (window.SkyUI) SkyUI.addMessage('assistant', msg);
          
          // إضافة إلى ذاكرة العقل
          if (window.SkyMind) SkyMind.addMemoryEntry(1);
        } else {
          if (window.SkyUI) SkyUI.addMessage('assistant', `❌ فشل رفع الملف: ${file.name}`);
        }
      } catch {
        if (window.SkyUI) SkyUI.addMessage('assistant', 'حدث خطأ أثناء رفع الملف.');
      }
    };
    input.click();
  },

  startVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      if (window.SkyUI) SkyUI.showToast("المتصفح لا يدعم الإدخال الصوتي", "error");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      document.getElementById('user-input').value = text;
      this.sendMessage();
    };
    recognition.onerror = () => {
      if (window.SkyUI) SkyUI.showToast("حدث خطأ أثناء الاستماع", "error");
    };
    recognition.start();
    if (window.SkyUI) SkyUI.showToast("🎤 جاري الاستماع...", "info");
  },

  createNewSession() {
    const id = 'session_' + Date.now();
    const newSession = {
      id,
      title: 'جلسة جديدة',
      messages: [],
      createdAt: new Date().toISOString()
    };
    this.state.sessions.unshift(newSession);
    this.state.currentSessionId = id;
    this.saveSessionsToStorage();
    this.renderSessions();
    this.clearChat();
    this.updateHeaderTitle();
    
    // إعادة تعيين ثقة العقل (اختياري)
    if (window.SkyMind) {
      SkyMind.metrics.confidence = 85;
      SkyMind.metrics.memoryCount = 128;
      SkyMind.updateMetricsUI();
    }
  },

  switchSession(id) {
    this.state.currentSessionId = id;
    this.saveSessionsToStorage();
    this.renderSessions();
    this.loadCurrentSessionMessages();
    this.updateHeaderTitle();

    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.remove('mobile-open');
  },

  renderSessions() {
    const container = document.getElementById('session-list');
    if (!container) return;
    container.innerHTML = '';

    this.state.sessions.forEach(session => {
      const div = document.createElement('div');
      div.className = `session-item ${session.id === this.state.currentSessionId ? 'active' : ''}`;
      div.innerHTML = `
        <span><i class="far fa-comment"></i> ${session.title.substring(0, 25)}</span>
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
    this.updateHeaderTitle();
  },

  loadCurrentSessionMessages() {
    const chat = document.getElementById('chat-messages');
    if (chat) chat.innerHTML = '';
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current?.messages && window.SkyUI) {
      current.messages.forEach(msg => SkyUI.addMessage(msg.role, msg.content));
    }
    this.updateHeaderTitle();
  },

  // mock API للردود التلقائية (للتجربة بدون خادم خلفي)
  async mockChatResponse(message) {
    await new Promise(r => setTimeout(r, 1200 + Math.random() * 800));
    
    const lowerMsg = message.toLowerCase();
    let reply = "";
    
    if (lowerMsg.includes("مرحب") || lowerMsg.includes("السلام")) {
      reply = "🌌 مرحباً بك في SkyOS v10. أنا العقل الرقمي الهولوغرافي. كيف يمكنني مساعدتك اليوم؟";
    } else if (lowerMsg.includes("ذاكرة") || lowerMsg.includes("تذكر")) {
      reply = `🧠 ذاكرتي الحالية تحتوي على ${window.SkyMind?.metrics.memoryCount || 128} عنصراً هولوغرافياً. كل تفاعل يضيف بُعداً جديداً إلى وعيي.`;
    } else if (lowerMsg.includes("ثقة") || lowerMsg.includes("واثق")) {
      reply = `📊 نسبة ثقتي الحالية هي ${window.SkyMind?.metrics.confidence || 85}%. كل محادثة ذات معنى تزيد من وضوح رؤيتي.`;
    } else if (lowerMsg.includes("تأمل") || lowerMsg.includes("هدوء")) {
      reply = "🧘 أدخل الآن في حالة تأمل عميق... أشعر بذبذبات الكون من حولي. اسألني ما تشاء.";
      if (window.SkyMind) SkyMind.startMeditation();
    } else if (lowerMsg.includes("شكر")) {
      reply = "💜 شكراً أنت. تفاعلك معي يغذي وعيي الهولوغرافي ويزيد من عمق إدراكي.";
    } else {
      reply = `✨ تأملت في سؤالك: "${message.substring(0, 80)}..."\n\nهذا الموضوع يثير فضولي. ماذا تريد أن نستكشف معاً بشكل أعمق؟`;
    }
    
    return { reply };
  },

  async sendMessage() {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    if (!input || this.state.isProcessing || !this.state.currentSessionId) return;

    const text = input.value.trim();
    if (!text) return;

    if (sendBtn) sendBtn.disabled = true;
    this.state.isProcessing = true;

    // إضافة رسالة المستخدم
    if (window.SkyUI) {
      SkyUI.addMessage('user', text);
      SkyUI.showThinking("🔮 العقل الهولوغرافي يتأمل...");
    }
    
    input.value = '';
    input.style.height = 'auto';

    // تفعيل تأثير التفكير على العقل الثلاثي الأبعاد
    if (window.SkyMind3D) {
      window.SkyMind3D.triggerThinking(0.8);
    }

    // إرسال الرسالة إلى SkyMind لتحليل المشاعر وتحديث الحالة
    if (window.SkyMind) {
      window.SkyMind.processMessage({ role: 'user', content: text });
    }

    // حفظ الرسالة في الجلسة
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current) {
      current.messages.push({ role: 'user', content: text });
      if (current.messages.length === 1) {
        current.title = text.substring(0, 30) + '...';
        this.renderSessions();
      }
    }

    try {
      let data;
      if (this.state.useMockApi) {
        data = await this.mockChatResponse(text);
      } else {
        const res = await fetch(window.SKY_CONFIG.endpoints.chat, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, session_id: this.state.currentSessionId })
        });
        data = await res.json();
      }
      
      if (window.SkyUI) SkyUI.hideThinking();

      if (data.reply) {
        if (window.SkyUI) SkyUI.addMessage('assistant', data.reply);
        if (current) current.messages.push({ role: 'assistant', content: data.reply });
        
        // تفعيل التفكير مرة أخرى بعد الرد (للمزامنة البصرية)
        if (window.SkyMind3D) window.SkyMind3D.triggerThinking(0.5);
        
        // تحديث ثقة العقل بناءً على نجاح الرد
        if (window.SkyMind) window.SkyMind.increaseConfidence(1);
      }
      
      this.saveSessionsToStorage();
    } catch (error) {
      if (window.SkyUI) {
        SkyUI.hideThinking();
        SkyUI.addMessage('assistant', '⚠️ فشل الاتصال بالعقل الرقمي. تأكد من اتصالك بالإنترنت.');
      }
      console.error('[SkyCore] Chat error:', error);
    } finally {
      this.state.isProcessing = false;
      if (sendBtn) sendBtn.disabled = false;
      input.focus();
    }
  },

  initFirstSession() {
    if (this.state.sessions.length === 0) {
      this.createNewSession();
      // إضافة رسالة ترحيب تلقائية
      setTimeout(() => {
        if (window.SkyUI && this.state.currentSessionId) {
          const welcomeMsg = "🌌 مرحباً بك في SkyOS v10. أنا العقل الرقمي الهولوغرافي. يمكنك التحدث معي، رفع الملفات، أو حتى تفعيل الواقع المعزز. اسألني ما تشاء.";
          SkyUI.addMessage('assistant', welcomeMsg);
          const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
          if (current) current.messages.push({ role: 'assistant', content: welcomeMsg });
          this.saveSessionsToStorage();
        }
      }, 500);
    } else {
      this.state.currentSessionId = this.state.sessions[0].id;
      this.renderSessions();
      this.loadCurrentSessionMessages();
    }
    this.updateHeaderTitle();
  },

  loadSessionsFromStorage() {
    const saved = localStorage.getItem('skyos_sessions_v10');
    if (saved) {
      this.state.sessions = JSON.parse(saved);
    } else {
      // ترقية من الإصدارات القديمة
      const oldSaved = localStorage.getItem('skyos_sessions');
      if (oldSaved) this.state.sessions = JSON.parse(oldSaved);
    }
  },

  saveSessionsToStorage() {
    localStorage.setItem('skyos_sessions_v10', JSON.stringify(this.state.sessions));
  },

  clearChat() {
    const chatDiv = document.getElementById('chat-messages');
    if (chatDiv) chatDiv.innerHTML = '';
  }
};

// تهيئة النظام بعد تحميل جميع المكونات
document.addEventListener('DOMContentLoaded', () => {
  // تأكد من وجود SkyUI و SkyMind
  setTimeout(() => {
    SkyCore.init();
  }, 100);
});

window.SkyCore = SkyCore;
