/* ============================================================
   SkyOS v10.0 — Unified Autonomous Architecture Engine
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  
  // دالة محاكاة تسلسل الإقلاع الأساسي (Boot Sequence) طبقاً للبند 4
  setTimeout(() => {
    const bootScreen = document.getElementById("sky-boot-screen");
    if (bootScreen) {
      bootScreen.classList.add("fade-out");
    }
  }, 1400);

  // مستودع الحالة المعزول للنظام (Isolated Memory State)
  const SkyState = {
    theme: localStorage.getItem("sky-theme") || "dark",
    sessions: JSON.parse(localStorage.getItem("sky-sessions")) || [],
    currentSessionId: localStorage.getItem("sky-current-session") || null,
    fontSize: localStorage.getItem("sky-font-size") || "16px"
  };

  // مراجع عناصر الواجهة
  const chatWindow = document.getElementById("chat-window");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const sessionList = document.getElementById("session-list");
  const newSessionBtn = document.getElementById("new-session-btn");
  const toggleThemeBtn = document.getElementById("toggle-theme-btn");
  const menuToggle = document.getElementById("menu-toggle");
  const sidebar = document.getElementById("sidebar");
  const clearActiveChatBtn = document.getElementById("clear-active-chat");
  
  const openSettingsBtn = document.getElementById("open-settings-btn");
  const settingsPanel = document.getElementById("settings-panel");
  const openWorkspaceBtn = document.getElementById("open-workspace-btn");
  const workspacePanel = document.getElementById("workspace-panel");
  const fontSizeSelect = document.getElementById("setting-font-size");

  // ------------------------------
  // محرك معالجة النصوص والأكواد (Markdown Parser)
  // ------------------------------
  function parseMarkdown(text) {
    if (!text) return "";
    let escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // الكتل البرمجية الكبيرة الثلاثية ```
    const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
    escaped = escaped.replace(codeBlockRegex, (match, lang, code) => {
      const language = lang || "code";
      return `<div class="sky-code-container">
                <div class="sky-code-header">
                  <span><i class="fas fa-code"></i> ${language}</span>
                  <button class="sky-code-copy-btn" onclick="SkyEngine.copyCode(this)"><i class="far fa-copy"></i> نسخ الكود</button>
                </div>
                <pre class="sky-code-block"><code>${code.trim()}</code></pre>
              </div>`;
    });

    // الأكواد المضمنة السريعة `
    escaped = escaped.replace(/`([^`]+)`/g, '<span class="sky-inline-code">$1</span>');
    
    // الأسطر الجديدة
    return escaped.replace(/\n/g, "<br>");
  }

  // ------------------------------
  // نظام الإشعارات الداخلي (Toast Center)
  // ------------------------------
  function showToast(message) {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `<i class="fas fa-info-circle" style="color:#6366f1; margin-left:8px;"></i> ${message}`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
  }

  // ------------------------------
  // محرك إدارة النوافذ والرسائل والنسخ
  // ------------------------------
  window.SkyEngine = {
    copyCode(button) {
      const container = button.closest(".sky-code-container");
      const codeElement = container.querySelector(".sky-code-block code");
      if (codeElement) {
        navigator.clipboard.writeText(codeElement.innerText).then(() => {
          button.innerHTML = `<i class="fas fa-check" style="color:#10b981;"></i> تم النسخ`;
          showToast("تم نسخ الكود البرمجي للذاكرة");
          setTimeout(() => {
            button.innerHTML = `<i class="far fa-copy"></i> نسخ الكود`;
          }, 2000);
        });
      }
    },

    copyMessage(button) {
      const bubble = button.closest(".message-bubble");
      // استنساخ لتجنب نسخ كود شريط الأدوات السفلي
      const clone = bubble.cloneNode(true);
      const actionBar = clone.querySelector(".msg-action-bar");
      if (actionBar) actionBar.remove();
      const codeContainers = clone.querySelectorAll(".sky-code-container");
      codeContainers.forEach(c => {
        const codeText = c.querySelector(".sky-code-block code")?.innerText || "";
        c.replaceWith(codeText);
      });

      const cleanText = clone.innerText.trim();
      navigator.clipboard.writeText(cleanText).then(() => {
        showToast("تم نسخ الرسالة بالكامل");
      });
    }
  };

  function appendMessage(sender, text) {
    const row = document.createElement("div");
    row.className = `message-row ${sender}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${sender}-avatar`;
    avatar.innerHTML = sender === "user" ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.style.fontSize = SkyState.fontSize;

    const content = document.createElement("div");
    content.className = "message-content";
    content.innerHTML = parseMarkdown(text);
    bubble.appendChild(content);

    // بناء شريط أدوات الرسالة أسفل المحتوى طبقاً للطلب
    const actionBar = document.createElement("div");
    actionBar.className = "msg-action-bar";
    actionBar.innerHTML = `
      <button class="msg-action-btn" onclick="SkyEngine.copyMessage(this)"><i class="far fa-copy"></i> نسخ النص</button>
      <span style="font-size:0.7rem; color:var(--text-muted); margin-right:auto;">${new Date().toLocaleTimeString('ar-EG', {hour:'2-digit', minute:'2-digit'})}</span>
    `;
    bubble.appendChild(actionBar);

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatWindow.appendChild(row);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // ------------------------------
  // محرك مسح وإدارة الجلسات الحية والمؤرشفة
  // ------------------------------
  function initEngine() {
    document.body.className = SkyState.theme;
    fontSizeSelect.value = SkyState.fontSize;
    renderSessions();

    if (!SkyState.currentSessionId && SkyState.sessions.length > 0) {
      SkyState.currentSessionId = SkyState.sessions[0].id;
    }
    loadCurrentSession();
  }

  function renderSessions() {
    sessionList.innerHTML = "";
    if (SkyState.sessions.length === 0) {
      sessionList.innerHTML = '<div class="sky-session-empty">لا توجد جلسات مؤرشفة حالياً</div>';
      return;
    }

    SkyState.sessions.forEach(session => {
      const item = document.createElement("div");
      item.className = `session-item ${session.id === SkyState.currentSessionId ? 'active' : ''}`;
      item.dataset.id = session.id;

      const titleSpan = document.createElement("span");
      titleSpan.className = "session-title-text";
      titleSpan.innerHTML = `<i class="far fa-comments"></i> ${session.title}`;
      titleSpan.addEventListener("click", () => switchSession(session.id));

      // زر الحذف المنفصل لكل جلسة مؤرشفة في القائمة الجانبية
      const deleteBtn = document.createElement("button");
      deleteBtn.className = "delete-session-btn";
      deleteBtn.innerHTML = '<i class="far fa-trash-alt"></i>';
      deleteBtn.title = "مسح هذه الجلسة نهائياً";
      deleteBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        deleteArchivedSession(session.id);
      });

      item.appendChild(titleSpan);
      item.appendChild(deleteBtn);
      sessionList.appendChild(item);
    });
  }

  function createNewSession() {
    const id = "session_" + Date.now();
    const newSession = {
      id: id,
      title: `جلسة معالجة #${SkyState.sessions.length + 1}`,
      messages: []
    };
    SkyState.sessions.unshift(newSession);
    SkyState.currentSessionId = id;
    saveState();
    renderSessions();
    loadCurrentSession();
    showToast("تم إنشاء مسار ذاكرة جديد");
  }

  function switchSession(id) {
    SkyState.currentSessionId = id;
    saveState();
    renderSessions();
    loadCurrentSession();
    if (window.innerWidth <= 768) {
      sidebar.classList.remove("mobile-show");
    }
  }

  // دالة مسح المحادثة المؤرشفة المحددة من الشريط الجانبي
  function deleteArchivedSession(id) {
    SkyState.sessions = SkyState.sessions.filter(s => s.id !== id);
    if (SkyState.currentSessionId === id) {
      SkyState.currentSessionId = SkyState.sessions.length > 0 ? SkyState.sessions[0].id : null;
    }
    saveState();
    renderSessions();
    loadCurrentSession();
    showToast("تم مسح الجلسة المؤرشفة بنجاح");
  }

  function loadCurrentSession() {
    chatWindow.innerHTML = "";
    if (!SkyState.currentSessionId) {
      chatWindow.innerHTML = '<div style="text-align:center; margin-top:40px; color:var(--text-muted); font-size:0.9rem;"><i class="fas fa-brain" style="font-size:2rem; margin-bottom:10px; color:var(--primary);"></i><br>قم بإنشاء أو اختيار جلسة لبدء تشغيل النواة الذكية</div>';
      return;
    }
    const current = SkyState.sessions.find(s => s.id === SkyState.currentSessionId);
    if (current && current.messages) {
      current.messages.forEach(msg => appendMessage(msg.role, msg.content));
    }
  }

  // مسح محتوى محادثة النافذة النشطة الحالية بالكامل
  clearActiveChatBtn.addEventListener("click", () => {
    if (!SkyState.currentSessionId) return;
    const current = SkyState.sessions.find(s => s.id === SkyState.currentSessionId);
    if (current) {
      current.messages = [];
      saveState();
      loadCurrentSession();
      showToast("تم تفريغ محتوى النافذة النشطة");
    }
  });

  function saveState() {
    localStorage.setItem("sky-theme", SkyState.theme);
    localStorage.setItem("sky-sessions", JSON.stringify(SkyState.sessions));
    localStorage.setItem("sky-current-session", SkyState.currentSessionId);
    localStorage.setItem("sky-font-size", SkyState.fontSize);
  }

  // ------------------------------
  // تدفق الإرسال والاتصال بالسيرفر
  // ------------------------------
  async function handleSendMessage() {
    const text = userInput.value.trim();
    if (!text || !SkyState.currentSessionId) return;

    appendMessage("user", text);
    userInput.value = "";
    userInput.style.height = "auto";

    // حفظ رسالة المستخدم
    const current = SkyState.sessions.find(s => s.id === SkyState.currentSessionId);
    if (current) {
      current.messages.push({ role: "user", content: text });
      // تحديث تلقائي لعنوان الجلسة بناء على أول سؤال
      if (current.messages.length === 1) {
        current.title = text.substring(0, 24) + "...";
        renderSessions();
      }
      saveState();
    }

    // إرسال الطلب للسيرفر الفعلي
    try {
      const response = await fetch(SKY_CONFIG.endpoints.ask, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, session_id: SkyState.currentSessionId })
      });
      const data = await response.json();
      const reply = data.reply || "لم يتم استقبال استجابة صحيحة من النواة المركزية.";
      
      appendMessage("assistant", reply);
      if (current) {
        current.messages.push({ role: "assistant", content: reply });
        saveState();
      }
    } catch (error) {
      console.error(error);
      appendMessage("assistant", "خطأ: فشل الاتصال بخادم المحرك المحرك الذكي. يرجى مراجعة حالة الربط.");
    }
  }

  // ------------------------------
  // روابط أحداث الواجهة التفاعلية
  // ------------------------------
  sendBtn.addEventListener("click", handleSendMessage);
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 768) {
      e.preventDefault();
      handleSendMessage();
    }
  });

  // تكبير تلقائي مرن لحقل الإدخال السفلي
  userInput.addEventListener("input", () => {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(userInput.scrollHeight, 100) + "px";
  });

  newSessionBtn.addEventListener("click", createNewSession);

  toggleThemeBtn.addEventListener("click", () => {
    SkyState.theme = SkyState.theme === "dark" ? "light" : "dark";
    document.body.className = SkyState.theme;
    toggleThemeBtn.innerHTML = SkyState.theme === "dark" ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
    saveState();
    showToast(`تم التبديل إلى الوضع ${SkyState.theme === "dark" ? "الليل" : "النهار"}`);
  });

  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("mobile-show");
  });

  openSettingsBtn.addEventListener("click", () => {
    settingsPanel.classList.toggle("hidden");
    workspacePanel.classList.add("hidden");
  });

  openWorkspaceBtn.addEventListener("click", () => {
    workspacePanel.classList.toggle("hidden");
    settingsPanel.classList.add("hidden");
  });

  fontSizeSelect.addEventListener("change", (e) => {
    SkyState.fontSize = e.target.value;
    saveState();
    loadCurrentSession();
  });

  // تشغيل المحرك لأول مرة
  initEngine();
});
