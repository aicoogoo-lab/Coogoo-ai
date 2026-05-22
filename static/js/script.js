document.addEventListener("DOMContentLoaded", () => {
  
  // دالة محاكاة تسلسل الإقلاع الأساسي (Boot Sequence)
  setTimeout(() => {
    const bootScreen = document.getElementById("sky-boot-screen");
    if (bootScreen) {
      bootScreen.classList.add("fade-out");
    }
  }, 1400);

  // مستودع الحالة المعزول للنظام
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
  // محرك معالجة النصوص والأكواد
  // ------------------------------
  function parseMarkdown(text) {
    if (!text) return "";
    let escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

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

    escaped = escaped.replace(/`([^`]+)`/g, '<span class="sky-inline-code">$1</span>');
    return escaped.replace(/\n/g, "<br>");
  }

  function showToast(message) {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `<i class="fas fa-info-circle" style="color:#6366f1; margin-left:8px;"></i> ${message}`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
  }

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
  // محرك إدارة الجلسات
  // ------------------------------
  function initEngine() {
    document.body.className = SkyState.theme;
    fontSizeSelect.value = SkyState.fontSize;
    renderSessions();

    // === الإصلاح الرئيسي: إنشاء جلسة تلقائياً إذا لم توجد ===
    if (!SkyState.currentSessionId) {
      createNewSession();
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
  // تدفق الإرسال
  // ------------------------------
  async function handleSendMessage() {
    const text = userInput.value.trim();
    if (!text || !SkyState.currentSessionId) return;

    appendMessage("user", text);
    userInput.value = "";
    userInput.style.height = "auto";

    const current = SkyState.sessions.find(s => s.id === SkyState.currentSessionId);
    if (current) {
      current.messages.push({ role: "user", content: text });
      if (current.messages.length === 1) {
        current.title = text.substring(0, 24) + "...";
        renderSessions();
      }
      saveState();
    }

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
      appendMessage("assistant", "خطأ: فشل الاتصال بخادم المحرك الذكي.");
    }
  }

  // ------------------------------
  // الإصلاحات الجديدة: الصوت + رفع الملفات
  // ------------------------------
  function startVoiceRecognition() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      showToast("المتصفح لا يدعم الإدخال الصوتي. استخدم Chrome أو Edge.");
      return;
    }
    const recognition = new SpeechRec();
    recognition.lang = 'ar-SA';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript.trim();
      if (transcript) {
        userInput.value = transcript;
        showToast("تم التعرف على الصوت ✓");
        handleSendMessage();
      }
    };
    recognition.onerror = (e) => showToast("خطأ صوتي: " + e.error);
    try {
      recognition.start();
      showToast("🎤 جاري الاستماع... تحدث الآن");
    } catch (_) {
      showToast("تعذر تشغيل الميكروفون");
    }
  }

  function handleFileSelection() {
    const fileInput = document.getElementById("file-input");
    if (!fileInput) return;

    fileInput.onchange = (e) => {
      const file = e.target.files[0];
      if (!file || !SkyState.currentSessionId) return;

      showToast(`جاري معالجة ${file.name}...`);

      const reader = new FileReader();
      reader.onload = (ev) => {
        let content = `📎 ملف مرفوع: ${file.name} (${(file.size / 1024).toFixed(1)} كيلوبايت)`;
        if (file.type.startsWith("text/") || /\.(md|py|js|txt|json|csv)$/i.test(file.name)) {
          content += `\n\n${ev.target.result.substring(0, 2500)}`;
        } else if (file.type.startsWith("image/")) {
          content += "\n\n[صورة — جاهزة للتحليل البصري]";
        }
        appendMessage("user", content);
        showToast("تم إضافة الملف إلى السياق");
      };

      if (file.type.startsWith("text/") || /\.(md|py|js|txt)$/i.test(file.name)) {
        reader.readAsText(file);
      } else {
        reader.readAsDataURL(file);
        setTimeout(() => {
          appendMessage("user", `📎 ${file.name} — جاهز للتحليل`);
        }, 400);
      }
      fileInput.value = "";
    };
    fileInput.click();
  }

  // ------------------------------
  // روابط الأحداث
  // ------------------------------
  sendBtn.addEventListener("click", handleSendMessage);
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 768) {
      e.preventDefault();
      handleSendMessage();
    }
  });

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

  // === ربط أزرار الصوت ورفع الملفات (الإصلاح الرئيسي) ===
  const voiceBtn = document.getElementById("voice-btn");
  if (voiceBtn) voiceBtn.addEventListener("click", startVoiceRecognition);

  const miniVoiceBtn = document.getElementById("mini-voice-btn");
  if (miniVoiceBtn) miniVoiceBtn.addEventListener("click", startVoiceRecognition);

  const miniUploadBtn = document.getElementById("mini-upload-btn");
  if (miniUploadBtn) miniUploadBtn.addEventListener("click", handleFileSelection);

  const visionBtn = document.getElementById("vision-btn");
  if (visionBtn) visionBtn.addEventListener("click", () => {
    showToast("وضع الرؤية مفعّل");
    handleFileSelection();
  });

  // تشغيل المحرك
  initEngine();
});
