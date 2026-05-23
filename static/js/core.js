/* ============================================================
   SkyOS / Coogoo-AI
   core.js — HoloLiquid Neo-AI Chat Core (النظام الجديد)
   ============================================================ */

window.SkyCore = (() => {
  const CONFIG = window.SKY_CONFIG || { useMockAPI: true, version: "2.0" };

  /* ------------------------------------------------------------
     عناصر الواجهة الأساسية
  ------------------------------------------------------------ */
  const els = {};

  function cacheElements() {
    els.menuToggle        = document.getElementById("menu-toggle");
    els.sidebar           = document.getElementById("sidebar");
    els.newSessionBtn     = document.getElementById("new-session-btn");
    els.newSessionHeader  = document.getElementById("new-session-header");
    els.sessionList       = document.getElementById("session-list");
    els.themeToggle       = document.getElementById("theme-toggle");
    els.themeName         = document.getElementById("theme-name");

    els.messagesContainer = document.getElementById("messages-container");
    els.messagesList      = document.getElementById("messages-list");
    els.messageInput      = document.getElementById("message-input");
    els.sendBtn           = document.getElementById("send-btn");

    els.uploadBtn         = document.getElementById("upload-btn");
    els.voiceBtn          = document.getElementById("voice-btn");

    els.imagePreviewArea  = document.getElementById("image-preview-area");
    els.previewImg        = document.getElementById("preview-img");
    els.removePreview     = document.getElementById("remove-preview");

    els.toastContainer    = document.getElementById("toast-container");
  }

  /* ------------------------------------------------------------
     نظام التوست (إشعارات صغيرة)
  ------------------------------------------------------------ */
  function showToast(message, type = "info") {
    if (!els.toastContainer) return;

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    els.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.classList.add("visible");
    }, 10);

    setTimeout(() => {
      toast.classList.remove("visible");
      setTimeout(() => toast.remove(), 200);
    }, 3000);
  }

  /* ------------------------------------------------------------
     نظام الثيم (داكن / فاتح)
  ------------------------------------------------------------ */
  let currentTheme = 'dark';

  function initTheme() {
    const saved = localStorage.getItem('sky_theme');
    if (saved === 'light') {
      currentTheme = 'light';
      document.body.classList.add('light-theme');
      if (els.themeName) els.themeName.textContent = 'فاتح';
    }
  }

  function toggleTheme() {
    if (currentTheme === 'dark') {
      currentTheme = 'light';
      document.body.classList.add('light-theme');
      if (els.themeName) els.themeName.textContent = 'فاتح';
      localStorage.setItem('sky_theme', 'light');
    } else {
      currentTheme = 'dark';
      document.body.classList.remove('light-theme');
      if (els.themeName) els.themeName.textContent = 'داكن';
      localStorage.setItem('sky_theme', 'dark');
    }
    showToast(`الثيم: ${currentTheme === 'dark' ? 'داكن' : 'فاتح'}`, 'info');
  }

  /* ------------------------------------------------------------
     نظام الجلسات
  ------------------------------------------------------------ */
  let sessions = [];
  let currentSessionId = null;

  function loadSessions() {
    const saved = localStorage.getItem('sky_sessions');
    if (saved) {
      try {
        sessions = JSON.parse(saved);
        // تحويل تواريخ الجلسات من string إلى Date
        sessions.forEach(s => {
          s.createdAt = new Date(s.createdAt);
          s.messages.forEach(m => {
            m.timestamp = m.timestamp || Date.now();
          });
        });
      } catch (e) {
        sessions = [];
      }
    }
  }

  function saveSessions() {
    localStorage.setItem('sky_sessions', JSON.stringify(sessions));
  }

  function createSession() {
    const id = Date.now().toString();
    const session = {
      id,
      title: "محادثة جديدة",
      createdAt: new Date(),
      messages: []
    };
    sessions.unshift(session);
    currentSessionId = id;
    saveSessions();
    renderSessions();
    SkyChat.clearAndWelcome();
    SkyChat.resetArchiveToggle();
    showToast("تم إنشاء محادثة جديدة", "info");
  }

  function deleteSession(id, event) {
    if (event) event.stopPropagation();
    sessions = sessions.filter(s => s.id !== id);
    if (currentSessionId === id) {
      currentSessionId = sessions[0]?.id || null;
    }
    saveSessions();
    renderSessions();
    if (currentSessionId) {
      const session = sessions.find(s => s.id === currentSessionId);
      SkyChat.loadMessages(session ? session.messages : []);
    } else {
      createSession();
    }
    showToast('تم حذف المحادثة', 'info');
  }

  function switchSession(id) {
    currentSessionId = id;
    saveSessions();
    renderSessions();
    const session = sessions.find(s => s.id === id);
    SkyChat.loadMessages(session ? session.messages : []);
    
    // إغلاق القائمة الجانبية في الموبايل
    if (els.sidebar) els.sidebar.classList.remove('mobile-open');
  }

  function renderSessions() {
    if (!els.sessionList) return;
    els.sessionList.innerHTML = "";

    sessions.forEach(session => {
      const item = document.createElement("div");
      item.className = "session-item";
      if (session.id === currentSessionId) item.classList.add("active");

      item.innerHTML = `
        <i class="far fa-comment"></i>
        <span>${session.title}</span>
        <button class="delete-session" data-id="${session.id}"><i class="fas fa-trash"></i></button>
      `;

      item.addEventListener('click', (e) => {
        if (!e.target.closest('.delete-session')) {
          switchSession(session.id);
        }
      });

      const delBtn = item.querySelector('.delete-session');
      if (delBtn) {
        delBtn.addEventListener('click', (e) => deleteSession(session.id, e));
      }

      els.sessionList.appendChild(item);
    });
  }

  function getCurrentSession() {
    if (!currentSessionId && sessions.length === 0) {
      createSession();
    }
    return sessions.find(s => s.id === currentSessionId) || sessions[0];
  }

  function addMessageToSession(msg) {
    const session = getCurrentSession();
    if (!session) return;
    
    const messageObj = {
      role: msg.role,
      content: msg.text || msg.content,
      timestamp: msg.timestamp || Date.now()
    };
    
    session.messages.push(messageObj);

    // تحديث عنوان الجلسة بأول رسالة من المستخدم
    if (msg.role === "user" && session.title === "محادثة جديدة") {
      const text = msg.text || msg.content || '';
      session.title = text.slice(0, 24) + (text.length > 24 ? "…" : "");
      renderSessions();
    }
    
    saveSessions();
  }

  /* ------------------------------------------------------------
     نظام المحادثة HoloLiquid Neo-AI
  ------------------------------------------------------------ */
  const SkyChat = (() => {
    let archive = [];          // جميع الرسائل
    let maxVisible = 20;       // عدد الرسائل الظاهرة
    let showArchive = false;   // هل نعرض القديم؟
    let arrowBtn = null;

    function createArchiveButton() {
      if (arrowBtn) {
        const parent = arrowBtn.parentElement;
        if (parent) parent.removeChild(arrowBtn);
      }

      arrowBtn = document.createElement("button");
      arrowBtn.id = 'archive-toggle-btn';
      arrowBtn.className = "icon-btn neo-glow";
      arrowBtn.style.cssText = "margin: 10px auto; display: none;";
      arrowBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
      arrowBtn.title = 'عرض كل الرسائل';
      arrowBtn.onclick = () => toggleArchive();

      if (els.messagesContainer) {
        els.messagesContainer.insertBefore(arrowBtn, els.messagesContainer.firstChild);
      }
    }

    function resetArchiveToggle() {
      showArchive = false;
      if (arrowBtn) {
        arrowBtn.style.display = 'none';
        arrowBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
      }
    }

    function updateArchiveButton(totalMessages) {
      if (!arrowBtn) createArchiveButton();
      if (!arrowBtn) return;
      
      if (totalMessages <= maxVisible) {
        arrowBtn.style.display = 'none';
      } else {
        arrowBtn.style.display = 'block';
        arrowBtn.innerHTML = showArchive
          ? '<i class="fas fa-chevron-up"></i>'
          : '<i class="fas fa-chevron-down"></i>';
        arrowBtn.title = showArchive ? 'إخفاء الأرشيف' : 'عرض كل الرسائل';
      }
    }

    function toggleArchive() {
      showArchive = !showArchive;
      renderMessages();
    }

    function renderMessages() {
      if (!els.messagesList) return;
      els.messagesList.innerHTML = "";

      const visible = showArchive ? archive : archive.slice(-maxVisible);

      visible.forEach((msg, index) => {
        const row = document.createElement("div");
        row.className = `message ${msg.role}`;

        const time = msg.timestamp 
          ? new Date(msg.timestamp).toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" }) 
          : (msg.time || 'الآن');

        const avatarIcon = msg.role === "assistant" 
          ? '<i class="fas fa-sparkles"></i>' 
          : '<i class="fas fa-user"></i>';

        const content = msg.text || msg.content || '';

        row.innerHTML = `
          <div class="message-avatar">${avatarIcon}</div>
          <div class="message-bubble">
            <div class="message-text">${escapeHtml(content)}</div>
            <div class="message-time">${time}</div>
            <div class="message-actions">
              <button class="msg-action copy-msg"><i class="far fa-copy"></i> نسخ</button>
              <button class="msg-action share-msg"><i class="fas fa-share-alt"></i> مشاركة</button>
              ${msg.role === 'assistant' && index === visible.length - 1 ? '<button class="msg-action regenerate-msg"><i class="fas fa-undo-alt"></i> إعادة</button>' : ''}
            </div>
          </div>
        `;

        // ربط أزرار الإجراءات
        row.querySelector('.copy-msg')?.addEventListener('click', (e) => {
          e.stopPropagation();
          copyText(content);
        });
        
        row.querySelector('.share-msg')?.addEventListener('click', (e) => {
          e.stopPropagation();
          shareText(content);
        });
        
        row.querySelector('.regenerate-msg')?.addEventListener('click', (e) => {
          e.stopPropagation();
          regenerateLastMessage();
        });

        els.messagesList.appendChild(row);
      });

      // تمرير للأسفل
      setTimeout(() => {
        if (els.messagesList) {
          els.messagesList.scrollTop = els.messagesList.scrollHeight;
        }
      }, 50);

      updateArchiveButton(archive.length);
    }

    function sendUserMessage(text) {
      const msg = {
        role: "user",
        text,
        time: new Date().toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" }),
        timestamp: Date.now()
      };
      archive.push(msg);
      addMessageToSession(msg);
      renderMessages();
    }

    function sendAIMessage(text) {
      const msg = {
        role: "assistant",
        text,
        time: new Date().toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" }),
        timestamp: Date.now()
      };
      archive.push(msg);
      addMessageToSession(msg);
      renderMessages();
    }

    function showTyping() {
      if (!els.messagesList) return;
      
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
      els.messagesList.appendChild(typingDiv);
      els.messagesList.scrollTop = els.messagesList.scrollHeight;
    }

    function hideTyping() {
      const typing = document.getElementById('typing-indicator');
      if (typing) typing.remove();
    }

    function getSmartReply(message) {
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
        return `لديك ${sessions.length} جلسة محفوظة في الذاكرة. يمكنك التبديل بينها من القائمة الجانبية.`;
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
    }

    async function handleSend() {
      const input = els.messageInput;
      if (!input) return;
      
      const text = input.value.trim();
      if (!text) return;

      sendUserMessage(text);
      input.value = "";

      // محاكاة التفكير
      showTyping();
      
      setTimeout(() => {
        hideTyping();
        const reply = getSmartReply(text);
        sendAIMessage(reply);
      }, 800 + Math.random() * 500);
    }

    function clearAndWelcome() {
      archive = [];
      
      const welcome = {
        role: "assistant",
        text: "مرحباً بك في سماء — واجهة HoloLiquid Neo-AI. اكتب ما تريد وسأساعدك خطوة بخطوة.",
        time: new Date().toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" }),
        timestamp: Date.now()
      };
      archive.push(welcome);
      
      // حفظ رسالة الترحيب في الجلسة
      const session = getCurrentSession();
      if (session) {
        session.messages.push({
          role: 'assistant',
          content: welcome.text,
          timestamp: welcome.timestamp
        });
        saveSessions();
      }
      
      renderMessages();
    }

    function loadMessages(msgs) {
      archive = msgs.map(m => ({
        role: m.role,
        text: m.content || m.text,
        time: m.timestamp 
          ? new Date(m.timestamp).toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" }) 
          : (m.time || 'الآن'),
        timestamp: m.timestamp || Date.now()
      }));
      renderMessages();
    }

    // ربط زر الإرسال
    if (els.sendBtn && els.messageInput) {
      els.sendBtn.addEventListener('click', handleSend);
      els.messageInput.addEventListener('keydown', (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          handleSend();
        }
      });
    }

    return {
      sendUserMessage,
      sendAIMessage,
      renderMessages,
      clearAndWelcome,
      loadMessages,
      resetArchiveToggle,
      showTyping,
      hideTyping
    };
  })();

  window.SkyChat = SkyChat;

  /* ------------------------------------------------------------
     إجراءات مساعدة
  ------------------------------------------------------------ */
  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
      if (m === '&') return '&amp;';
      if (m === '<') return '&lt;';
      if (m === '>') return '&gt;';
      return m;
    }).replace(/\n/g, '<br>');
  }

  function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
      showToast('تم النسخ', 'success');
    }).catch(() => {
      showToast('فشل النسخ', 'error');
    });
  }

  function shareText(text) {
    if (navigator.share) {
      navigator.share({ text: text }).catch(() => {});
    } else {
      copyText(text);
      showToast('تم النسخ (المشاركة غير مدعومة)', 'info');
    }
  }

  function regenerateLastMessage() {
    const session = getCurrentSession();
    if (!session || session.messages.length < 2) return;
    
    const lastUserMsg = [...session.messages].reverse().find(m => m.role === 'user');
    if (!lastUserMsg) return;
    
    // حذف آخر رد من الجلسة
    const lastAssistantIndex = session.messages.map(m => m.role).lastIndexOf('assistant');
    if (lastAssistantIndex !== -1) {
      session.messages.splice(lastAssistantIndex, 1);
      saveSessions();
    }
    
    // إعادة تحميل الرسائل وعرض مؤشر التفكير
    SkyChat.loadMessages(session.messages);
    SkyChat.showTyping();
    
    setTimeout(() => {
      SkyChat.hideTyping();
      const reply = "تم إعادة توليد الرد. هذا رد جديد بناءً على طلبك.";
      SkyChat.sendAIMessage(reply);
    }, 600);
  }

  /* ------------------------------------------------------------
     رفع صورة (معاينة فقط)
  ------------------------------------------------------------ */
  function initImageUpload() {
    if (!els.uploadBtn || !els.imagePreviewArea || !els.previewImg || !els.removePreview) return;

    let imagePreview = null;
    let imageFile = null;

    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.style.display = "none";
    document.body.appendChild(fileInput);

    els.uploadBtn.onclick = () => {
      fileInput.click();
    };

    fileInput.onchange = () => {
      const file = fileInput.files[0];
      if (!file) return;

      imageFile = file;
      const reader = new FileReader();
      reader.onload = e => {
        imagePreview = e.target.result;
        els.previewImg.src = e.target.result;
        els.imagePreviewArea.style.display = "block";
      };
      reader.readAsDataURL(file);
    };

    els.removePreview.onclick = () => {
      imagePreview = null;
      imageFile = null;
      els.previewImg.src = "";
      els.imagePreviewArea.style.display = "none";
      fileInput.value = "";
    };
  }

  /* ------------------------------------------------------------
     إدخال صوتي
  ------------------------------------------------------------ */
  function initVoiceInput() {
    if (!els.voiceBtn) return;

    els.voiceBtn.addEventListener('click', () => {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        showToast('المتصفح لا يدعم الإدخال الصوتي', 'error');
        return;
      }
      
      const recognition = new SpeechRecognition();
      recognition.lang = 'ar-SA';
      recognition.interimResults = false;
      
      recognition.onstart = () => {
        showToast('جاري الاستماع...', 'info');
      };
      
      recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        if (els.messageInput) {
          els.messageInput.value = text;
        }
        // إرسال تلقائي بعد التعرف على الصوت
        if (els.sendBtn) {
          els.sendBtn.click();
        }
      };
      
      recognition.onerror = () => {
        showToast('حدث خطأ في الاستماع', 'error');
      };
      
      recognition.start();
    });
  }

  /* ------------------------------------------------------------
     القائمة الجانبية (إظهار/إخفاء)
  ------------------------------------------------------------ */
  function initSidebarToggle() {
    if (!els.menuToggle || !els.sidebar) return;
    
    els.menuToggle.addEventListener('click', () => {
      els.sidebar.classList.toggle('mobile-open');
    });
    
    // إغلاق القائمة عند النقر خارجها
    document.addEventListener('click', (e) => {
      if (els.sidebar && els.menuToggle) {
        if (!els.sidebar.contains(e.target) && !els.menuToggle.contains(e.target)) {
          els.sidebar.classList.remove('mobile-open');
        }
      }
    });
  }

  /* ------------------------------------------------------------
     أزرار الجلسات والثيم
  ------------------------------------------------------------ */
  function initButtons() {
    if (els.newSessionBtn) {
      els.newSessionBtn.addEventListener('click', () => createSession());
    }
    if (els.newSessionHeader) {
      els.newSessionHeader.addEventListener('click', () => createSession());
    }
    if (els.themeToggle) {
      els.themeToggle.addEventListener('click', () => toggleTheme());
    }
  }

  /* ------------------------------------------------------------
     تهيئة النظام
  ------------------------------------------------------------ */
  function init() {
    cacheElements();
    loadSessions();
    initTheme();
    initSidebarToggle();
    initImageUpload();
    initVoiceInput();
    initButtons();

    // إنشاء أول جلسة + رسالة ترحيب إذا لم تكن هناك جلسات
    if (sessions.length === 0) {
      createSession();
    } else {
      currentSessionId = sessions[0].id;
      renderSessions();
      const session = sessions[0];
      SkyChat.loadMessages(session.messages);
    }

    console.log("✅ SkyCore initialized — version:", CONFIG.version);
  }

  return {
    init,
    showToast,
    createSession,
    getCurrentSession
  };
})();

/* ============================================================
   تهيئة عند تحميل الصفحة
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  if (window.SkyCore && typeof SkyCore.init === "function") {
    SkyCore.init();
  }
});
