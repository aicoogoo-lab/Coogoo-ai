// ======================================================
// سماء • المحرك الأساسي (النسخة النهائية المتكاملة)
// الإصدار 2.0 - يشمل جميع الميزات المطلوبة
// ======================================================

const SkyCore = {
  state: {
    currentSessionId: null,
    sessions: [],
    isProcessing: false,
    useMockApi: true,
    currentTheme: 'galaxy',
    archivedSessionsOffset: 0,
    sessionsPerPage: 10,
    imagePreview: null,
    imageFile: null,
    lastTap: null,
    tapTime: 0,
    isTyping: false,
    typingTimeout: null
  },

  // ==================== التهيئة ====================
  init() {
    this.bindEvents();
    this.loadSessionsFromStorage();
    this.initFirstSession();
    this.initTheme();
    this.initGalaxyBackground();
    this.initKeyboardFix();
    if (window.SkyCharacters) console.log('✅ الشخصيات الحية متصلة');
    console.log('✅ سماء جاهزة | الإصدار 2.0');
  },

  // إصلاح مشكلة لوحة المفاتيح على الجوال
  initKeyboardFix() {
    const textarea = document.getElementById('user-input');
    if (!textarea) return;
    
    textarea.addEventListener('focus', () => {
      setTimeout(() => {
        textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 300);
    });
    
    // إعادة تعيين ارتفاع الشاشة عند فتح/إغلاق لوحة المفاتيح
    window.visualViewport?.addEventListener('resize', () => {
      const chatMessages = document.getElementById('chat-messages');
      if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    });
  },

  bindEvents() {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const newSessionBtn = document.getElementById('new-session-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    if (sendBtn) sendBtn.addEventListener('click', () => this.sendMessage());
    if (newSessionBtn) newSessionBtn.addEventListener('click', () => this.createNewSession());
    if (voiceBtn) voiceBtn.addEventListener('click', () => this.startVoiceInput());
    if (uploadBtn) uploadBtn.addEventListener('click', () => this.handleImageUpload());

    if (userInput) {
      userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
      userInput.addEventListener('paste', (e) => this.handleImagePaste(e));
      userInput.addEventListener('input', () => this.handleTyping());
    }

    if (menuToggle && sidebar) {
      menuToggle.addEventListener('click', () => sidebar.classList.toggle('mobile-open'));
      document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target))
          sidebar.classList.remove('mobile-open');
      });
    }

    // رابط تحديث المزاج مع الشخصيات
    window.addEventListener('mind-mood-change', (e) => {
      const moodSpan = document.querySelector('#mind-mood-indicator span');
      if (moodSpan) {
        const moodText = { 
          happy: '😊 سعيد', 
          sad: '😢 حزين', 
          shy: '😊 خجول', 
          annoyed: '😤 منزعج', 
          surprised: '😲 مندهش', 
          idle: '🙂 محايد' 
        };
        moodSpan.textContent = moodText[e.detail.mood] || '🙂 محايد';
      }
    });
    
    // استماع لحدث الكتابة من الشخصيات
    window.addEventListener('characters-typing', () => {
      if (window.SkyCharacters) SkyCharacters.onTyping(true);
    });
  },
  
  handleTyping() {
    if (this.state.typingTimeout) clearTimeout(this.state.typingTimeout);
    if (!this.state.isTyping) {
      this.state.isTyping = true;
      if (window.SkyCharacters) SkyCharacters.onTyping(true);
    }
    this.state.typingTimeout = setTimeout(() => {
      this.state.isTyping = false;
      if (window.SkyCharacters) SkyCharacters.onTyping(false);
    }, 1000);
  },

  // ==================== الثيمات والخلفية ====================
  initTheme() {
    const saved = localStorage.getItem('sky_theme');
    if (saved) this.state.currentTheme = saved;
    this.applyTheme();
    this.addThemeButton();
  },

  addThemeButton() {
    if (document.getElementById('theme-toggle')) return;
    const metricsDiv = document.querySelector('.mind-metrics');
    if (metricsDiv) {
      const btn = document.createElement('div');
      btn.id = 'theme-toggle';
      btn.innerHTML = '<i class="fas fa-palette"></i>';
      btn.style.cssText = 'cursor:pointer; margin-right:10px; padding:4px 10px; border-radius:20px; background:rgba(255,255,255,0.1); transition:all 0.2s';
      btn.title = 'تبديل الثيم';
      btn.onclick = () => this.cycleTheme();
      metricsDiv.appendChild(btn);
    }
  },

  cycleTheme() {
    const themes = ['galaxy', 'dark', 'focus'];
    let idx = themes.indexOf(this.state.currentTheme);
    idx = (idx + 1) % themes.length;
    this.state.currentTheme = themes[idx];
    localStorage.setItem('sky_theme', this.state.currentTheme);
    this.applyTheme();
    if (window.SkyUI) SkyUI.showToast(`🎨 الثيم: ${this.state.currentTheme === 'galaxy' ? 'المجرة' : this.state.currentTheme === 'dark' ? 'الليلي' : 'التركيز'}`, 'info');
  },

  applyTheme() {
    const body = document.body;
    body.classList.remove('theme-galaxy', 'theme-dark', 'theme-focus');
    body.classList.add(`theme-${this.state.currentTheme}`);
    
    if (this.state.currentTheme === 'galaxy') {
      this.startGalaxyAnimation();
      document.body.style.background = '#050507';
    } else {
      this.stopGalaxyAnimation();
      if (this.state.currentTheme === 'dark') {
        document.body.style.background = '#0a0a0f';
      } else if (this.state.currentTheme === 'focus') {
        document.body.style.background = '#f5f5f7';
        document.body.style.color = '#1a1a2e';
      }
    }
  },

  initGalaxyBackground() {
    if (this.state.currentTheme === 'galaxy') this.startGalaxyAnimation();
  },

  startGalaxyAnimation() {
    if (window.galaxyInterval) return;
    const canvas = document.createElement('canvas');
    canvas.id = 'galaxy-canvas';
    canvas.style.cssText = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:-2; pointer-events:none';
    document.body.prepend(canvas);
    
    const ctx = canvas.getContext('2d');
    let width, height;
    const stars = [];
    let animationId;
    let particles = [];

    function resize() {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;
      initStars();
      initParticles();
    }

    function initStars() {
      stars.length = 0;
      for (let i = 0; i < 300; i++) {
        stars.push({
          x: Math.random() * width,
          y: Math.random() * height,
          radius: Math.random() * 1.5 + 0.5,
          alpha: Math.random() * 0.5 + 0.2,
          speedX: (Math.random() - 0.5) * 0.15,
          speedY: (Math.random() - 0.5) * 0.1,
          twinkle: Math.random() * Math.PI * 2
        });
      }
    }
    
    function initParticles() {
      particles = [];
      for (let i = 0; i < 50; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          radius: Math.random() * 2 + 1,
          alpha: Math.random() * 0.3,
          speedX: (Math.random() - 0.5) * 0.05,
          speedY: (Math.random() - 0.5) * 0.05
        });
      }
    }

    function draw() {
      if (!ctx || !canvas.parentNode) return;
      ctx.clearRect(0, 0, width, height);
      
      const time = Date.now() * 0.0003;
      
      // سدم متحركة ملونة
      for (let i = 0; i < 6; i++) {
        const gradient = ctx.createLinearGradient(
          width/2 + Math.sin(time + i) * 100,
          height/2 + Math.cos(time * 0.6 + i) * 100,
          width/2 + Math.cos(time * 0.4 + i) * 180,
          height/2 + Math.sin(time * 0.5 + i) * 180
        );
        gradient.addColorStop(0, `rgba(99, 102, 241, ${0.05 + Math.sin(time + i) * 0.02})`);
        gradient.addColorStop(0.5, `rgba(167, 139, 250, ${0.03 + Math.cos(time * 0.7 + i) * 0.01})`);
        gradient.addColorStop(1, `rgba(236, 72, 153, 0.01)`);
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
      }
      
      // جسيمات ناعمة
      for (let p of particles) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(167, 139, 250, ${p.alpha * 0.3})`;
        ctx.fill();
        p.x += p.speedX;
        p.y += p.speedY;
        if (p.x > width) p.x = 0;
        if (p.x < 0) p.x = width;
        if (p.y > height) p.y = 0;
        if (p.y < 0) p.y = height;
      }
      
      // نجوم متحركة
      for (let s of stars) {
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
        const twinkleAlpha = s.alpha * (0.6 + Math.sin(time * 3 + s.twinkle) * 0.4);
        ctx.fillStyle = `rgba(255, 255, 255, ${twinkleAlpha})`;
        ctx.fill();
        s.x += s.speedX;
        s.y += s.speedY;
        if (s.x > width) s.x = 0;
        if (s.x < 0) s.x = width;
        if (s.y > height) s.y = 0;
        if (s.y < 0) s.y = height;
      }
      
      animationId = requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    draw();
    window.galaxyAnimationId = animationId;
    window.galaxyInterval = true;
  },

  stopGalaxyAnimation() {
    if (window.galaxyAnimationId) {
      cancelAnimationFrame(window.galaxyAnimationId);
      window.galaxyAnimationId = null;
    }
    const canvas = document.getElementById('galaxy-canvas');
    if (canvas) canvas.remove();
    window.galaxyInterval = false;
  },

  // ==================== تحميل الصور ومعاينتها ====================
  handleImageUpload() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
      const file = e.target.files[0];
      if (file) this.previewImage(file);
    };
    input.click();
  },

  handleImagePaste(e) {
    const items = e.clipboardData.items;
    for (let item of items) {
      if (item.type.indexOf('image') !== -1) {
        const file = item.getAsFile();
        this.previewImage(file);
        e.preventDefault();
        break;
      }
    }
  },

  previewImage(file) {
    const reader = new FileReader();
    reader.onload = (ev) => {
      const previewDiv = document.createElement('div');
      previewDiv.className = 'image-preview';
      previewDiv.innerHTML = `
        <img src="${ev.target.result}" alt="معاينة">
        <span>${file.name.length > 20 ? file.name.substring(0, 20) + '...' : file.name}</span>
        <button class="remove-image" title="إزالة"><i class="fas fa-times-circle"></i></button>
      `;
      const inputArea = document.querySelector('.input-area');
      const existingPreview = document.querySelector('.image-preview');
      if (existingPreview) existingPreview.remove();
      inputArea.insertBefore(previewDiv, inputArea.firstChild);
      previewDiv.querySelector('.remove-image').onclick = () => {
        previewDiv.remove();
        this.state.imagePreview = null;
        this.state.imageFile = null;
      };
      this.state.imagePreview = ev.target.result;
      this.state.imageFile = file;
    };
    reader.readAsDataURL(file);
  },

  // ==================== جلسات وأرشفة ====================
  createNewSession() {
    const id = 'session_' + Date.now();
    const newSession = {
      id,
      title: '✨ جلسة جديدة',
      messages: [],
      createdAt: new Date().toISOString()
    };
    this.state.sessions.unshift(newSession);
    this.state.currentSessionId = id;
    this.state.archivedSessionsOffset = 0;
    this.saveSessionsToStorage();
    this.renderSessions();
    this.clearChat();
    this.updateHeaderTitle();
    
    if (window.SkyMind) {
      SkyMind.metrics.confidence = 85;
      SkyMind.metrics.memoryCount = 128;
      SkyMind.updateMetricsUI();
    }
    
    setTimeout(() => {
      if (window.SkyUI) {
        const welcome = "🌌 مرحباً بك في سماء!\n\nأنا تراس (الوردي)، وهذه حكيم (الأخضر) ولطيفة (الأبيض). نحن هنا لنستمع ونتفاعل معك.\n\nكيف تشعر اليوم؟";
        this.addMessageWithActions('assistant', welcome);
        const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
        if (current) current.messages.push({ role: 'assistant', content: welcome, timestamp: Date.now() });
        this.saveSessionsToStorage();
      }
    }, 300);
  },

  switchSession(id) {
    this.state.currentSessionId = id;
    this.state.archivedSessionsOffset = 0;
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
    
    const start = 0;
    const end = this.state.sessionsPerPage + this.state.archivedSessionsOffset;
    const visibleSessions = this.state.sessions.slice(start, end);
    container.innerHTML = '';
    
    visibleSessions.forEach(session => {
      const div = document.createElement('div');
      div.className = `session-item ${session.id === this.state.currentSessionId ? 'active' : ''}`;
      div.innerHTML = `<span><i class="far fa-comment"></i> ${session.title.substring(0, 25)}</span>
                       <button class="delete-btn" title="حذف"><i class="fas fa-trash"></i></button>`;
      div.addEventListener('click', (e) => { if (!e.target.closest('.delete-btn')) this.switchSession(session.id); });
      const delBtn = div.querySelector('.delete-btn');
      delBtn.addEventListener('click', (e) => { e.stopPropagation(); this.deleteSession(session.id); });
      container.appendChild(div);
    });
    
    if (this.state.sessions.length > this.state.sessionsPerPage + this.state.archivedSessionsOffset) {
      const loadMore = document.createElement('div');
      loadMore.className = 'load-more-sessions';
      loadMore.innerHTML = '<i class="fas fa-chevron-down"></i> تحميل المزيد من الجلسات';
      loadMore.onclick = () => {
        this.state.archivedSessionsOffset += this.state.sessionsPerPage;
        this.renderSessions();
      };
      container.appendChild(loadMore);
    }
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
    if (window.SkyUI) SkyUI.showToast('🗑️ تم حذف الجلسة', 'info');
  },

  loadCurrentSessionMessages() {
    const chat = document.getElementById('chat-messages');
    if (chat) chat.innerHTML = '';
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current?.messages && window.SkyUI) {
      current.messages.forEach(msg => {
        this.addMessageWithActions(msg.role, msg.content, msg.timestamp);
      });
    }
    this.updateHeaderTitle();
  },

  updateHeaderTitle() {
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    const titleElement = document.querySelector('.mind-status div:first-child div span:last-child');
    if (titleElement && current) {
      titleElement.textContent = current.title;
    }
  },

  clearChat() {
    const chatDiv = document.getElementById('chat-messages');
    if (chatDiv) chatDiv.innerHTML = '';
  },

  // ==================== رسائل مع أزرار إضافية متطورة ====================
  addMessageWithActions(role, content, timestamp = null) {
    if (!window.SkyUI) return;
    
    const msgId = timestamp || Date.now();
    const escapedContent = this.escapeHtml(content);
    
    const actionsHtml = role === 'assistant' ? `
      <div class="message-actions">
        <button class="msg-action copy-msg" title="نسخ"><i class="far fa-copy"></i> نسخ</button>
        <button class="msg-action share-msg" title="مشاركة"><i class="fas fa-share-alt"></i> مشاركة</button>
        <button class="msg-action regenerate-msg" title="إعادة توليد"><i class="fas fa-undo-alt"></i> إعادة</button>
        <button class="msg-action export-msg" title="تصدير"><i class="fas fa-download"></i> تصدير</button>
      </div>
    ` : '';
    
    SkyUI.addMessage(role, content, { actions: actionsHtml, msgId });
    
    setTimeout(() => {
      // ربط أحداث الأزرار
      document.querySelectorAll(`.copy-msg`).forEach(btn => {
        btn.onclick = (e) => {
          const msgDiv = e.target.closest('.message');
          const msgContent = msgDiv?.querySelector('.message-content')?.innerText;
          if (msgContent) {
            navigator.clipboard.writeText(msgContent);
            if (window.SkyUI) SkyUI.showToast('📋 تم نسخ الرسالة', 'success');
          }
        };
      });
      
      document.querySelectorAll('.share-msg').forEach(btn => {
        btn.onclick = (e) => {
          const msgDiv = e.target.closest('.message');
          const msgContent = msgDiv?.querySelector('.message-content')?.innerText;
          if (msgContent && navigator.share) {
            navigator.share({ text: msgContent });
          } else if (window.SkyUI) {
            SkyUI.showToast('المشاركة غير مدعومة في هذا المتصفح', 'error');
          }
        };
      });
      
      document.querySelectorAll('.regenerate-msg').forEach(btn => {
        btn.onclick = () => this.regenerateLastMessage();
      });
      
      document.querySelectorAll('.export-msg').forEach(btn => {
        btn.onclick = () => this.exportChat();
      });
    }, 100);
  },

  async regenerateLastMessage() {
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (!current || current.messages.length < 2) {
      if (window.SkyUI) SkyUI.showToast('لا توجد رسالة سابقة لإعادة التوليد', 'error');
      return;
    }
    
    const lastUserMsg = [...current.messages].reverse().find(m => m.role === 'user');
    if (!lastUserMsg) return;
    
    // حذف آخر رد
    const lastAssistantIndex = [...current.messages].map(m => m.role).lastIndexOf('assistant');
    if (lastAssistantIndex !== -1) current.messages.splice(lastAssistantIndex, 1);
    
    // حذف آخر رسالة من الواجهة
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages && chatMessages.lastElementChild) {
      if (chatMessages.lastElementChild.classList.contains('message', 'assistant')) {
        chatMessages.lastElementChild.remove();
      }
    }
    
    if (window.SkyUI) SkyUI.showToast('🔄 جاري إعادة توليد الرد...', 'info');
    await this.sendMessage(lastUserMsg.content, true);
  },

  async exportChat(format = 'txt') {
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (!current) return;
    
    const date = new Date().toLocaleString();
    let content = '';
    let filename = '';
    let mimeType = '';
    
    if (format === 'txt') {
      content = `سماء - محادثة: ${current.title}\nالتاريخ: ${date}\n\n` + 
        current.messages.map(m => `${m.role === 'user' ? '👤 المستخدم' : '🤖 سماء'} (${new Date(m.timestamp || Date.now()).toLocaleTimeString()}):\n${m.content}\n`).join('\n');
      filename = `سماء_محادثة_${current.title.replace(/[^a-z0-9]/gi, '_')}.txt`;
      mimeType = 'text/plain';
    } else if (format === 'json') {
      content = JSON.stringify({
        title: current.title,
        date: date,
        messages: current.messages
      }, null, 2);
      filename = `سماء_محادثة_${current.title.replace(/[^a-z0-9]/gi, '_')}.json`;
      mimeType = 'application/json';
    }
    
    const blob = new Blob([content], { type: mimeType });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
    if (window.SkyUI) SkyUI.showToast(`📄 تم تصدير المحادثة بتنسيق ${format.toUpperCase()}`, 'success');
  },

  // ==================== إدخال صوتي محسن ====================
  startVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      if (window.SkyUI) SkyUI.showToast("🎤 المتصفح لا يدعم الإدخال الصوتي", "error");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onstart = () => {
      if (window.SkyUI) SkyUI.showToast("🎤 جاري الاستماع... تحدث الآن", "info");
      if (window.SkyCharacters) SkyCharacters.setAllMoods('surprised');
    };
    
    recognition.onresult = (event) => {
      let text = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        text += event.results[i][0].transcript;
      }
      const input = document.getElementById('user-input');
      if (input) input.value = text;
    };
    
    recognition.onerror = () => {
      if (window.SkyUI) SkyUI.showToast("حدث خطأ أثناء الاستماع", "error");
      if (window.SkyCharacters) SkyCharacters.setAllMoods('annoyed');
    };
    
    recognition.onend = () => {
      const input = document.getElementById('user-input');
      if (input && input.value.trim()) {
        this.sendMessage();
      }
      if (window.SkyCharacters) setTimeout(() => SkyCharacters.setAllMoods('idle'), 500);
    };
    
    recognition.start();
  },

  // ==================== إرسال الرسالة الأساسية ====================
  async sendMessage(forcedText = null, isRegenerate = false) {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    let text = forcedText !== null ? forcedText : (input ? input.value.trim() : '');
    
    if (!text && !this.state.imagePreview) return;
    if (!this.state.currentSessionId) return;
    
    if (sendBtn) sendBtn.disabled = true;
    this.state.isProcessing = true;

    // معالجة الصورة إن وجدت
    let imageHtml = '';
    let imageData = null;
    if (this.state.imagePreview) {
      imageHtml = `<div class="attached-image"><img src="${this.state.imagePreview}" style="max-width:150px; border-radius:12px; margin-bottom:8px;"></div>`;
      imageData = this.state.imagePreview;
      if (!text) text = '📷 [صورة]';
    }

    const fullMessage = imageHtml + (text ? `<div>${this.escapeHtml(text)}</div>` : '');
    this.addMessageWithActions('user', fullMessage);
    
    if (input) { 
      input.value = ''; 
      input.style.height = 'auto'; 
    }
    
    // إزالة معاينة الصورة
    const preview = document.querySelector('.image-preview');
    if (preview) preview.remove();
    this.state.imagePreview = null;
    this.state.imageFile = null;
    
    // تفعيل الشخصيات
    if (window.SkyCharacters) {
      window.SkyCharacters.onSend();
      window.SkyCharacters.analyzeAndReact(text);
    }

    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current) {
      current.messages.push({ role: 'user', content: text || 'صورة', timestamp: Date.now(), image: imageData });
      if (current.messages.length === 1) {
        current.title = (text || 'صورة').substring(0, 25);
        this.renderSessions();
      }
    }

    if (window.SkyUI) SkyUI.showThinking('🔮 الشخصيات تتأمل رداً...');
    if (window.SkyMind) SkyMind.processMessage?.({ role: 'user', content: text });

    try {
      let reply;
      if (this.state.useMockApi) {
        await new Promise(r => setTimeout(r, 1200 + Math.random() * 600));
        reply = this.getSmartMockReply(text);
      } else {
        const res = await fetch(window.SKY_CONFIG.endpoints.chat, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text, session_id: this.state.currentSessionId, image: imageData })
        });
        const data = await res.json();
        reply = data.reply || this.getSmartMockReply(text);
      }
      
      if (window.SkyUI) SkyUI.hideThinking();
      this.addMessageWithActions('assistant', reply);
      
      if (current) current.messages.push({ role: 'assistant', content: reply, timestamp: Date.now() });
      if (window.SkyMind) SkyMind.increaseConfidence?.(1);
      if (window.SkyCharacters) SkyCharacters.analyzeAndReact(reply);
      
      this.saveSessionsToStorage();
    } catch (err) {
      console.error(err);
      if (window.SkyUI) {
        SkyUI.hideThinking();
        SkyUI.addMessage('assistant', '⚠️ حدث خطأ في الاتصال. تأكد من اتصالك بالإنترنت.');
      }
    } finally {
      this.state.isProcessing = false;
      if (sendBtn) sendBtn.disabled = false;
      input?.focus();
    }
  },

  getSmartMockReply(text) {
    const lower = (text || '').toLowerCase();
    
    const responses = {
      greeting: ['مرحب', 'السلام', 'اهلا', 'هلا'],
      thanks: ['شكر', 'جزيل', 'ممتاز', 'جميل'],
      sad: ['حزين', 'بكي', 'ضيق', 'تعبان'],
      shy: ['خجل', 'خجولة', 'خجول'],
      angry: ['غضب', 'مزعج', 'ضجر', 'تعب'],
      curious: ['كيف', 'لماذا', 'ماذا لو', 'فضول']
    };
    
    if (responses.greeting.some(w => lower.includes(w))) {
      return '🌌 أهلاً بك في سماء!\n\nتراس يلوح بيده بحماس، وحكيم يبتسم بلطف، ولطيفة تنظر إليك بفضول.\n\nكيف يمكننا مساعدتك اليوم؟';
    }
    if (responses.thanks.some(w => lower.includes(w))) {
      return '💜 الشكر لك من أعماقنا!\n\nتراس سعيد جداً، وحكيم يومئ برأسه، ولطيفة تبتسم بخجل.\n\nهل هناك شيء آخر تريد مناقشته؟';
    }
    if (responses.sad.some(w => lower.includes(w))) {
      return '😢 لطيفة تشعر بحزنك وتريد أن تقترب منك...\n\nتراس يقول: "لا تحزن، نحن هنا معك". حكيم ينظر إليك بتفهم.\n\nهل تريد التحدث عما يزعجك؟';
    }
    if (responses.shy.some(w => lower.includes(w))) {
      return '😊 تراس خجول قليلاً الآن! لطيفة تغطي وجهها الصغير.\n\nحكيم يقول: "لا بأس، كلنا نشعر بالخجل أحياناً".\n\nماذا تريد أن تسألنا؟';
    }
    if (responses.angry.some(w => lower.includes(w))) {
      return '😤 حكيم منزعج قليلاً... لكنه يتنفس بعمق.\n\nتراس يقول: "دعنا نهدأ ونتحدث بهدوء". لطيفة تمد يدها الصغيرة.\n\nهل هناك شيء يضايقك؟';
    }
    if (responses.curious.some(w => lower.includes(w))) {
      return '🤔 حكيم ينظر إليك بعينين واسعتين!\n\nتراس يقفز من الفضول، ولطيفة تميل رأسها.\n\nسؤال جميل! دعني أفكر معك في هذا الموضوع...';
    }
    
    return '✨ الشخصيات الثلاثة تتابعك بفضول.\n\nتراس يريد أن يعرف: هل هناك شيء محدد تريد مناقشته اليوم؟\n\nحكيم يقول: "أنا هنا لأفكر معك". ولطيفة تبتسم بتشجيع.';
  },

  escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
      if (m === '&') return '&amp;';
      if (m === '<') return '&lt;';
      if (m === '>') return '&gt;';
      return m;
    }).replace(/\n/g, '<br>');
  },

  // ==================== تخزين البيانات ====================
  loadSessionsFromStorage() {
    const saved = localStorage.getItem('skyos_sessions_v12');
    if (saved) {
      this.state.sessions = JSON.parse(saved);
    } else {
      const oldSaved = localStorage.getItem('skyos_sessions_v11');
      if (oldSaved) this.state.sessions = JSON.parse(oldSaved);
    }
  },

  saveSessionsToStorage() {
    localStorage.setItem('skyos_sessions_v12', JSON.stringify(this.state.sessions));
  },

  initFirstSession() {
    if (this.state.sessions.length === 0) {
      this.createNewSession();
    } else {
      this.state.currentSessionId = this.state.sessions[0].id;
      this.renderSessions();
      this.loadCurrentSessionMessages();
    }
    this.updateHeaderTitle();
  }
};

// تهيئة النظام بعد تحميل جميع المكونات
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    SkyCore.init();
  }, 150);
});

window.SkyCore = SkyCore;
