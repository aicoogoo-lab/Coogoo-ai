// ======================================================
// سماء • المحرك الأساسي (النسخة المتكاملة الكاملة)
// ======================================================

const SkyCore = {
  state: {
    currentSessionId: null,
    sessions: [],
    isProcessing: false,
    useMockApi: true,
    currentTheme: 'galaxy', // galaxy, dark, focus
    archivedSessionsOffset: 0,
    sessionsPerPage: 10,
    imagePreview: null,
    lastTap: null,
    tapTime: 0
  },

  init() {
    this.bindEvents();
    this.loadSessionsFromStorage();
    this.initFirstSession();
    this.initTheme();
    this.initGalaxyBackground();
    if (window.SkyCharacters) console.log('✅ الشخصيات الحية متصلة');
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
        const moodText = { happy: 'سعيد', sad: 'حزين', shy: 'خجول', annoyed: 'منزعج', surprised: 'مندهش', idle: 'محايد' };
        moodSpan.textContent = moodText[e.detail.mood] || 'محايد';
      }
    });
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
      btn.style.cursor = 'pointer';
      btn.style.marginRight = '10px';
      btn.style.padding = '4px 8px';
      btn.style.borderRadius = '20px';
      btn.style.background = 'rgba(255,255,255,0.1)';
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
    if (window.SkyUI) SkyUI.showToast(`الثيم: ${this.state.currentTheme === 'galaxy' ? 'المجرة' : this.state.currentTheme === 'dark' ? 'الليلي' : 'التركيز'}`, 'info');
  },

  applyTheme() {
    const body = document.body;
    body.classList.remove('theme-galaxy', 'theme-dark', 'theme-focus');
    body.classList.add(`theme-${this.state.currentTheme}`);
    
    // تطبيق ألوان الخلفية
    if (this.state.currentTheme === 'galaxy') {
      this.startGalaxyAnimation();
      document.body.style.background = '#050507';
    } else if (this.state.currentTheme === 'dark') {
      this.stopGalaxyAnimation();
      document.body.style.background = '#0a0a0f';
    } else if (this.state.currentTheme === 'focus') {
      this.stopGalaxyAnimation();
      document.body.style.background = '#f5f5f7';
      document.body.style.color = '#1a1a2e';
    }
  },

  initGalaxyBackground() {
    if (this.state.currentTheme === 'galaxy') this.startGalaxyAnimation();
  },

  startGalaxyAnimation() {
    if (window.galaxyInterval) return;
    const canvas = document.createElement('canvas');
    canvas.id = 'galaxy-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-2';
    canvas.style.pointerEvents = 'none';
    document.body.prepend(canvas);
    
    const ctx = canvas.getContext('2d');
    let width, height;
    const stars = [];
    let animationId;

    function resize() {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;
      initStars();
    }

    function initStars() {
      stars.length = 0;
      for (let i = 0; i < 400; i++) {
        stars.push({
          x: Math.random() * width,
          y: Math.random() * height,
          radius: Math.random() * 1.5 + 0.5,
          alpha: Math.random() * 0.5 + 0.2,
          speedX: (Math.random() - 0.5) * 0.2,
          speedY: (Math.random() - 0.5) * 0.1,
          twinkle: Math.random() * Math.PI * 2
        });
      }
    }

    function draw() {
      if (!ctx || !canvas.parentNode) return;
      ctx.clearRect(0, 0, width, height);
      
      // سدم دوارة
      const time = Date.now() * 0.0003;
      for (let i = 0; i < 8; i++) {
        const gradient = ctx.createLinearGradient(
          width/2 + Math.sin(time + i) * 80,
          height/2 + Math.cos(time * 0.7 + i) * 80,
          width/2 + Math.cos(time * 0.3 + i) * 150,
          height/2 + Math.sin(time * 0.5 + i) * 150
        );
        gradient.addColorStop(0, `rgba(99, 102, 241, ${0.04 + Math.sin(time + i) * 0.02})`);
        gradient.addColorStop(0.5, `rgba(167, 139, 250, ${0.02 + Math.cos(time * 0.8 + i) * 0.01})`);
        gradient.addColorStop(1, `rgba(236, 72, 153, 0.01)`);
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
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
      previewDiv.style.cssText = 'display:flex; align-items:center; gap:8px; padding:8px; background:rgba(0,0,0,0.5); border-radius:12px; margin-bottom:8px;';
      previewDiv.innerHTML = `
        <img src="${ev.target.result}" style="height:50px; width:50px; object-fit:cover; border-radius:8px;">
        <span style="flex:1; font-size:12px;">${file.name}</span>
        <button class="remove-image" style="background:none; border:none; color:#f87171; cursor:pointer;"><i class="fas fa-times-circle"></i></button>
      `;
      const inputArea = document.querySelector('.input-area');
      const existingPreview = document.querySelector('.image-preview');
      if (existingPreview) existingPreview.remove();
      inputArea.insertBefore(previewDiv, inputArea.firstChild);
      previewDiv.querySelector('.remove-image').onclick = () => previewDiv.remove();
      this.state.imagePreview = ev.target.result;
    };
    reader.readAsDataURL(file);
  },

  // ==================== جلسات وأرشفة ====================
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
    
    // رسالة ترحيب
    setTimeout(() => {
      if (window.SkyUI) {
        const welcome = "🌌 مرحباً بك في سماء! أنا تراس، وهذه حكيم ولطيفة. نحن هنا لنستمع ونتفاعل معك. كيف تشعر اليوم؟";
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
                       <button class="delete-btn"><i class="fas fa-trash"></i></button>`;
      div.addEventListener('click', (e) => { if (!e.target.closest('.delete-btn')) this.switchSession(session.id); });
      const delBtn = div.querySelector('.delete-btn');
      delBtn.addEventListener('click', (e) => { e.stopPropagation(); this.deleteSession(session.id); });
      container.appendChild(div);
    });
    
    if (this.state.sessions.length > this.state.sessionsPerPage + this.state.archivedSessionsOffset) {
      const loadMore = document.createElement('div');
      loadMore.className = 'load-more-sessions';
      loadMore.style.cssText = 'text-align:center; padding:10px; color:#a78bfa; cursor:pointer; font-size:0.8rem; margin-top:10px;';
      loadMore.innerHTML = '<i class="fas fa-chevron-down"></i> تحميل المزيد';
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
    const header = document.querySelector('.mind-status div:first-child div');
    if (header && current) {
      const titleSpan = header.querySelector('span:last-child');
      if (titleSpan) titleSpan.textContent = current.title.substring(0, 30);
    }
  },

  clearChat() {
    const chatDiv = document.getElementById('chat-messages');
    if (chatDiv) chatDiv.innerHTML = '';
  },

  // ==================== رسائل مع أزرار إضافية ====================
  addMessageWithActions(role, content, timestamp = null) {
    if (!window.SkyUI) return;
    
    const msgId = timestamp || Date.now();
    const escapedContent = content.replace(/"/g, '&quot;').replace(/\n/g, '<br>');
    
    const actionsHtml = role === 'assistant' ? `
      <div class="message-actions" style="display:flex; gap:8px; margin-top:8px; justify-content:flex-end;">
        <button class="msg-action copy-msg" data-msg="${escapedContent}" style="background:none; border:none; color:#64748b; cursor:pointer;"><i class="far fa-copy"></i></button>
        <button class="msg-action share-msg" data-msg="${escapedContent}" style="background:none; border:none; color:#64748b; cursor:pointer;"><i class="fas fa-share-alt"></i></button>
        <button class="msg-action regenerate-msg" data-id="${msgId}" style="background:none; border:none; color:#64748b; cursor:pointer;"><i class="fas fa-undo-alt"></i></button>
        <button class="msg-action export-msg" data-msg="${escapedContent}" style="background:none; border:none; color:#64748b; cursor:pointer;"><i class="fas fa-download"></i></button>
      </div>
    ` : '';
    
    SkyUI.addMessage(role, content, { actions: actionsHtml, msgId });
    
    // ربط الأحداث بعد الإضافة
    setTimeout(() => {
      document.querySelectorAll(`.copy-msg[data-msg="${escapedContent}"]`).forEach(btn => {
        btn.onclick = () => { 
          navigator.clipboard.writeText(content); 
          if (window.SkyUI) SkyUI.showToast('تم نسخ الرد', 'success');
        };
      });
      document.querySelectorAll('.share-msg').forEach(btn => {
        btn.onclick = () => { 
          if (navigator.share) navigator.share({ text: btn.dataset.msg }); 
          else if (window.SkyUI) SkyUI.showToast('المشاركة غير مدعومة', 'error');
        };
      });
      document.querySelectorAll('.regenerate-msg').forEach(btn => {
        btn.onclick = () => this.regenerateLastMessage();
      });
      document.querySelectorAll('.export-msg').forEach(btn => {
        btn.onclick = () => this.exportChat();
      });
    }, 50);
  },

  async regenerateLastMessage() {
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (!current || current.messages.length < 2) return;
    
    const lastUserMsg = [...current.messages].reverse().find(m => m.role === 'user');
    if (!lastUserMsg) return;
    
    // حذف آخر رد
    const lastAssistantIndex = current.messages.map(m => m.role).lastIndexOf('assistant');
    if (lastAssistantIndex !== -1) current.messages.splice(lastAssistantIndex, 1);
    
    // حذف آخر رسالة من الواجهة
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages && chatMessages.lastElementChild) {
      if (chatMessages.lastElementChild.classList.contains('message', 'assistant')) {
        chatMessages.lastElementChild.remove();
      }
    }
    
    await this.sendMessage(lastUserMsg.content, true);
  },

  async exportChat() {
    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (!current) return;
    
    const date = new Date().toLocaleString();
    const text = `سماء - محادثة: ${current.title}\nالتاريخ: ${date}\n\n` + 
      current.messages.map(m => `${m.role === 'user' ? '👤 المستخدم' : '🤖 سماء'} (${new Date(m.timestamp || Date.now()).toLocaleTimeString()}):\n${m.content}\n`).join('\n');
    
    const blob = new Blob([text], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `سماء_محادثة_${current.title.replace(/[^a-z0-9]/gi, '_')}.txt`;
    a.click();
    URL.revokeObjectURL(a.href);
    if (window.SkyUI) SkyUI.showToast('تم تصدير المحادثة', 'success');
  },

  // ==================== إدخال صوتي ====================
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
      text = text || '📷 أرسل صورة';
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
    
    if (window.SkyCharacters) SkyCharacters.onSend();
    if (window.SkyCharacters) SkyCharacters.analyzeAndReact(text);

    const current = this.state.sessions.find(s => s.id === this.state.currentSessionId);
    if (current) {
      current.messages.push({ role: 'user', content: text || 'صورة', timestamp: Date.now(), image: imageData });
      if (current.messages.length === 1) {
        current.title = (text || 'صورة').substring(0, 30);
        this.renderSessions();
      }
    }

    if (window.SkyUI) SkyUI.showThinking('🔮 الشخصيات تتأمل...');
    if (window.SkyMind3D) window.SkyMind3D?.triggerThinking?.(0.7);
    if (window.SkyMind) SkyMind.processMessage?.({ role: 'user', content: text });

    try {
      let reply;
      if (this.state.useMockApi) {
        await new Promise(r => setTimeout(r, 1000 + Math.random() * 500));
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
    if (lower.includes('مرحب') || lower.includes('السلام')) {
      return '🌌 أهلاً بك في سماء! تراس، حكيم، ولطيفة هنا ينتظرونك. كيف تشعر اليوم؟';
    }
    if (lower.includes('شكر')) {
      return '💜 الشكر لك! تفاعلك يجعل الشخصيات أكثر حيوية. هل تحب أن نستكشف شيئاً جديداً معاً؟';
    }
    if (lower.includes('حزين') || lower.includes('بكي')) {
      return '😢 لطيفة تشعر بحزنك... تريد أن تشاركها ما يمر بك؟ أنا هنا لأستمع وأدعمك.';
    }
    if (lower.includes('خجل') || lower.includes('خجولة')) {
      return '😊 تراس خجول قليلاً الآن! هذا لطيف جداً. ماذا تريد أن تسأل حكيماً؟';
    }
    if (lower.includes('غضب') || lower.includes('مزعج')) {
      return '😤 حكيم منزعج قليلاً... لكنه يتنفس بعمق. هل هناك شيء يزعجك؟ دعنا نتحدث بهدوء.';
    }
    if (lower.includes('فضول') || lower.includes('كيف') || lower.includes('لماذا')) {
      return '🤔 حكيم ينظر إليك بفضول! سؤال جميل. دعني أفكر معك في هذا الموضوع...';
    }
    return '✨ الشخصيات تتابعك بفضول. تراس يريد أن يعرف: هل هناك شيء محدد تريد مناقشته اليوم؟';
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
    const saved = localStorage.getItem('skyos_sessions_v11');
    if (saved) {
      this.state.sessions = JSON.parse(saved);
    } else {
      const oldSaved = localStorage.getItem('skyos_sessions');
      if (oldSaved) this.state.sessions = JSON.parse(oldSaved);
    }
  },

  saveSessionsToStorage() {
    localStorage.setItem('skyos_sessions_v11', JSON.stringify(this.state.sessions));
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
  }, 100);
});

window.SkyCore = SkyCore;
