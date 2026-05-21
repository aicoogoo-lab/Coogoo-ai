/* ============================================================
   SkyOS v10.0 — Holographic Edition (JavaScript Engine)
   - جلسات ذكية ومزامنة PWA كاملة
   - واجهة حية وتتبع الأنماط الرسومية (UI Modes)
   - ملفات / صوت / رؤية / إدارة الأخطاء الصامتة
   - Workspace + Settings + Safe DOM Mounting
   ============================================================ */

(() => {
  "use strict";

  const ENDPOINTS = (window.SKY_CONFIG && window.SKY_CONFIG.endpoints) || {
    ask: "/ask",
    upload: "/upload",
    voice: "/voice",
    vision: "/vision",
    feedback: "/feedback",
    clear: "/clear",
    status: "/api/v1/status",
  };

  const LS_SESSION_KEY = "sky_session_id_v10";
  const LS_SESSIONS_LIST = "sky_sessions_list_v10";
  const LS_THEME_KEY = "sky_theme_v10";

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  let sessionId = loadOrCreateSessionId();
  let sessions = loadSessions();
  let isDark = loadTheme();
  let isSending = false;

  // DOM Elements
  const chatWindow = $("#chat-window");
  const userInput = $("#user-input");
  const sendBtn = $("#send-btn");
  const fileInput = $("#file-input");
  const hiddenAudioInput = $("#hidden-audio-input");
  const hiddenImageInput = $("#hidden-image-input");
  const newSessionBtn = $("#new-session-btn");
  const sessionListEl = $("#session-list");
  const voiceBtn = $("#voice-btn");
  const visionBtn = $("#vision-btn");
  const miniUploadBtn = $("#mini-upload-btn");
  const miniVoiceBtn = $("#mini-voice-btn");
  const miniVisionBtn = $("#mini-vision-btn");
  const toggleThemeBtn = $("#toggle-theme-btn");
  const toastContainer = $("#toast-container");
  const modelIndicator = $("#model-indicator");
  const sessionIndicator = $("#session-indicator");
  const connectionStatus = $("#connection-status");
  const openSettingsBtn = $("#open-settings-btn");
  const openWorkspaceBtn = $("#open-workspace-btn");
  const settingsPanel = $("#settings-panel");
  const workspacePanel = $("#workspace-panel");
  const menuToggleBtn = $("#menu-toggle");
  const sidebar = $("#sidebar");
  const clearChatBtn = $("#clear-chat-btn");
  const exportChatBtn = $("#export-chat-btn");

  // ========== Utilities ==========

  function loadOrCreateSessionId() {
    let id = localStorage.getItem(LS_SESSION_KEY);
    if (!id) {
      id = "s-" + Math.random().toString(36).slice(2, 12);
      localStorage.setItem(LS_SESSION_KEY, id);
    }
    return id;
  }

  function loadSessions() {
    try {
      const raw = localStorage.getItem(LS_SESSIONS_LIST);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function saveSessions() {
    try {
      localStorage.setItem(LS_SESSIONS_LIST, JSON.stringify(sessions));
    } catch {}
  }

  function loadTheme() {
    const saved = localStorage.getItem(LS_THEME_KEY);
    if (saved === "dark") {
      document.body.classList.remove("light");
      document.body.classList.add("dark");
      return true;
    }
    if (saved === "light") {
      document.body.classList.add("light");
      document.body.classList.remove("dark");
      return false;
    }
    return !document.body.classList.contains("light");
  }

  function setTheme(dark) {
    isDark = dark;
    if (dark) {
      document.body.classList.remove("light");
      document.body.classList.add("dark");
    } else {
      document.body.classList.add("light");
      document.body.classList.remove("dark");
    }
    localStorage.setItem(LS_THEME_KEY, dark ? "dark" : "light");
  }

  function setSession(id) {
    sessionId = id;
    localStorage.setItem(LS_SESSION_KEY, id);
    if (sessionIndicator) {
      sessionIndicator.innerHTML = `<i class="fas fa-id-card"></i> جلسة: ${id.slice(0, 8)}`;
    }
    addSessionRecord(id, `جلسة ${id.slice(2, 10)}`);
  }

  function addSessionRecord(id, title = "جلسة جديدة") {
    sessions = sessions.filter((s) => s.id !== id);
    sessions.unshift({ id, title, updated: Date.now() });
    saveSessions();
    renderSessionList();
  }

  function showToast(text, type = "info", timeout = 4000) {
    if (!toastContainer) return;
    const t = document.createElement("div");
    t.className = `toast ${type}`;
    const icon = type === "error" ? "fa-exclamation-circle" : type === "success" ? "fa-check-circle" : "fa-info-circle";
    t.innerHTML = `<i class="fas ${icon}" style="margin-left: 8px;"></i> ${text}`;
    toastContainer.appendChild(t);
    setTimeout(() => {
      t.style.opacity = "0";
      t.style.transform = "translateY(4px)";
      setTimeout(() => t.remove(), 260);
    }, timeout);
  }

  function formatTime(date = new Date()) {
    return date.toLocaleTimeString("ar-SA", { hour: "2-digit", minute: "2-digit" });
  }

  function scrollToBottom(smooth = true) {
    if (!chatWindow) return;
    chatWindow.scrollTo({
      top: chatWindow.scrollHeight + 200,
      behavior: smooth ? "smooth" : "auto",
    });
  }

  function autoResizeTextarea(el) {
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 180) + "px";
  }

  // تم إصلاح الدالة لحماية الأسطر البرمجية والمسافات داخل قوالب الكود من التلف
  function sanitizeAndFormat(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    let safe = div.innerHTML;

    // مصفوفة مؤقتة لحفظ الأكواد ومنع تأثير الـ <br/> عليها
    const codeBlocks = [];
    safe = safe.replace(/```([\s\S]*?)```/g, (match, code) => {
      const id = `__SKY_CODE_BLOCK_${codeBlocks.length}__`;
      codeBlocks.push(`<pre class="sky-code-block"><code>${code}</code></pre>`);
      return id;
    });

    // معالجة الأكواد البرمجية السطرية (Inline Code)
    safe = safe.replace(/`([^`]+)`/g, '<code class="sky-inline-code">$1</code>');

    // الروابط
    safe = safe.replace(
      /(https?:\/\/[^\s]+)/g,
      (m) => `<a href="${m}" target="_blank" rel="noopener noreferrer" style="color: var(--primary-3); text-decoration: underline;">${m}</a>`
    );
    
    // التنسيقات العادية للمنصوص
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    safe = safe.replace(/\*(.*?)\*/g, "<em>$1</em>");
    safe = safe.replace(/\n{2,}/g, "</p><p>").replace(/\n/g, "<br/>");
    
    // إعادة قوالب الأكواد البرمجية الأصلية سليمة بدون وسم <br/>
    codeBlocks.forEach((block, index) => {
      safe = safe.replace(`__SKY_CODE_BLOCK_${index}__`, block);
    });

    return `<p>${safe}</p>`;
  }

  function createMessageElement({ role = "assistant", text = "", time = null, messageId = null }) {
    const row = document.createElement("div");
    row.className = `message-row ${role === "user" ? "user" : "assistant"}`;
    if (messageId) row.dataset.msgId = messageId;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${role === "user" ? "user-avatar" : "assistant-avatar"}`;
    avatar.innerHTML = role === "user" ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const header = document.createElement("div");
    header.className = "message-header";
    const author = document.createElement("span");
    author.className = "message-author";
    author.innerHTML = role === "user" ? '<i class="fas fa-user-circle"></i> أنت' : '<i class="fas fa-star-of-life"></i> SkyOS';
    const timeEl = document.createElement("span");
    timeEl.className = "message-time";
    timeEl.innerHTML = `<i class="far fa-clock"></i> ${time || formatTime()}`;

    header.appendChild(author);
    header.appendChild(timeEl);

    const content = document.createElement("div");
    content.className = "message-content";
    content.innerHTML = sanitizeAndFormat(text);

    bubble.appendChild(header);
    bubble.appendChild(content);

    if (role === "assistant") {
      const feedbackDiv = document.createElement("div");
      feedbackDiv.className = "message-feedback";
      feedbackDiv.style.display = "flex";
      feedbackDiv.style.gap = "12px";
      feedbackDiv.style.marginTop = "12px";
      feedbackDiv.style.paddingTop = "8px";
      feedbackDiv.style.borderTop = "1px solid var(--border)";
      feedbackDiv.innerHTML = `
        <button class="feedback-btn good" data-score="1" style="background: none; border: none; cursor: pointer; color: var(--text-muted); transition: all 0.2s;">
          <i class="fas fa-thumbs-up"></i> مفيد
        </button>
        <button class="feedback-btn bad" data-score="-1" style="background: none; border: none; cursor: pointer; color: var(--text-muted); transition: all 0.2s;">
          <i class="fas fa-thumbs-down"></i> غير مفيد
        </button>
      `;
      bubble.appendChild(feedbackDiv);
      
      const goodBtn = feedbackDiv.querySelector(".good");
      const badBtn = feedbackDiv.querySelector(".bad");
      if (goodBtn) goodBtn.addEventListener("click", () => sendFeedback(1, sessionId, text, goodBtn, badBtn));
      if (badBtn) badBtn.addEventListener("click", () => sendFeedback(0, sessionId, text, goodBtn, badBtn));
    }

    row.appendChild(avatar);
    row.appendChild(bubble);
    return row;
  }

  function appendMessage(role, text, messageId = null) {
    if (!chatWindow) return;
    const id = messageId || Date.now().toString();
    const el = createMessageElement({ role, text, messageId: id });
    chatWindow.appendChild(el);
    scrollToBottom();
    return id;
  }

  async function sendFeedback(score, sessId, comment, goodBtn, badBtn) {
    try {
      const response = await fetch(ENDPOINTS.feedback, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          score: score === 1 ? 1 : 0,
          session_id: sessId,
          comment: comment.slice(0, 100)
        })
      });
      
      if (response.ok && goodBtn && badBtn) {
        if (score === 1) {
          goodBtn.style.color = "#22c55e";
          badBtn.style.color = "var(--text-muted)";
          showToast("شكراً على تقييمك الإيجابي! 🤍", "success");
        } else {
          badBtn.style.color = "#ef4444";
          goodBtn.style.color = "var(--text-muted)";
          showToast("شكراً على ملاحظاتك، سأتحسن! 🌱", "info");
        }
      }
    } catch (e) {
      console.error("Feedback error:", e);
    }
  }

  function showTypingIndicator() {
    if (!chatWindow || $("#typing-indicator")) return;

    const row = document.createElement("div");
    row.id = "typing-indicator";
    row.className = "message-row assistant";

    const avatar = document.createElement("div");
    avatar.className = "avatar assistant-avatar";
    avatar.innerHTML = '<i class="fas fa-robot"></i>';

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = `
      <div class="message-header">
        <span class="message-author"><i class="fas fa-star-of-life"></i> SkyOS</span>
        <span class="message-time"><i class="far fa-clock"></i> ${formatTime()}</span>
      </div>
      <div class="message-content">
        <div class="typing-indicator">
          <span></span><span></span><span></span>
          <span style="margin-right: 8px;">جاري التفكير...</span>
        </div>
      </div>
    `;

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatWindow.appendChild(row);
    scrollToBottom();
  }

  function hideTypingIndicator() {
    const el = $("#typing-indicator");
    if (el) el.remove();
  }

  // ========== Local History ==========

  function addToHistoryLocal(role, content) {
    try {
      const key = `sky_local_history_v10_${sessionId}`;
      const raw = localStorage.getItem(key);
      const arr = raw ? JSON.parse(raw) : [];
      arr.push({ role, content, t: Date.now() });
      localStorage.setItem(key, JSON.stringify(arr.slice(-200)));
    } catch {}
  }

  function loadLocalHistory() {
    try {
      const key = `sky_local_history_v10_${sessionId}`;
      const raw = localStorage.getItem(key);
      const arr = raw ? JSON.parse(raw) : [];
      if (!chatWindow) return;
      chatWindow.innerHTML = "";
      if (arr.length === 0) {
        appendMessage("assistant", "مرحباً… 🌌\n\nأنا **SkyOS Holographic v10**، نظام ذكاء هجين واعٍ.\n\n✨ يمكنك:\n• الدردشة ومناقشة البرمجة والبيانات\n• رفع ملفات ومستندات 📄\n• إرسال صور 🖼️ أو صوتيات 🎙️\n\n**أنا جاهز ومقترن بالسيرفر بنجاح...** 🚀");
      } else {
        arr.forEach(m => appendMessage(m.role, m.content));
      }
    } catch {}
  }

  function renderSessionList() {
    if (!sessionListEl) return;
    sessionListEl.innerHTML = "";
    if (!sessions.length) {
      sessionListEl.innerHTML = `<div class="sky-session-empty"><i class="fas fa-inbox"></i><br>لا يوجد أرشيف</div>`;
      return;
    }
    sessions.forEach((s) => {
      const item = document.createElement("div");
      item.className = "session-item" + (s.id === sessionId ? " active" : "");
      item.innerHTML = `<i class="fas fa-comment"></i> ${s.title}<br><small>${new Date(s.updated).toLocaleString("ar-SA")}</small>`;
      item.addEventListener("click", () => {
        if (s.id === sessionId) return;
        setSession(s.id);
        loadLocalHistory();
        showToast("تم تبديل الجلسة بنجاح", "success");
      });
      sessionListEl.appendChild(item);
    });
  }

  // ========== Network Actions ==========

  async function postJSON(url, payload) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return res.json();
  }

  async function sendMessage(text) {
    if (!text || isSending) return;
    if (handleQuickCommand(text)) {
      if (userInput) {
        userInput.value = "";
        autoResizeTextarea(userInput);
      }
      return;
    }

    isSending = true;
    if (userInput) {
      userInput.value = "";
      autoResizeTextarea(userInput);
    }
    appendMessage("user", text);
    addToHistoryLocal("user", text);
    addSessionRecord(sessionId, text.slice(0, 20) + "...");
    showTypingIndicator();

    try {
      const resp = await postJSON(ENDPOINTS.ask, {
        message: text,
        session_id: sessionId,
        ai_type: window.SKY_CONFIG?.ui_mode || "holo"
      });

      hideTypingIndicator();

      if (!resp || (!resp.reply && typeof resp !== "string")) {
        appendMessage("assistant", "حدث خطأ: لم يتم استلام رد صحيح من الخادم.");
        showToast("خطأ في معالجة رد السيرفر", "error");
        return;
      }

      const reply = resp.reply || resp;
      appendMessage("assistant", reply);
      addToHistoryLocal("assistant", reply);

      if (resp.provider && modelIndicator) {
        modelIndicator.innerHTML = `<i class="fas fa-microchip"></i> النموذج: ${resp.provider}`;
      }
    } catch (err) {
      hideTypingIndicator();
      appendMessage("assistant", "عذراً، واجهت مشكلة أثناء الاتصال بـ SkyOS. تأكد من أن السيرفر يعمل.");
      console.error("sendMessage error:", err);
      showToast("فشل إرسال الرسالة", "error");
    } finally {
      isSending = false;
    }
  }

  async function uploadFile(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ رفع وتحليل الملف...", "info");
    try {
      const res = await fetch(ENDPOINTS.upload, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم تحليل المستند بنجاح", "success");
      }
    } catch (e) {
      console.error(e);
      showToast("فشل رفع الملف", "error");
    }
  }

  async function uploadAudio(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("audio", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ معالجة الصوت وتحويله لنص...", "info");
    try {
      const res = await fetch(ENDPOINTS.voice, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم معالجة الصوت", "success");
      }
    } catch (e) {
      console.error(e);
      showToast("فشل معالجة الملف الصوتي", "error");
    }
  }

  async function uploadImage(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("image", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ فحص وتحليل الصورة...", "info");
    try {
      const res = await fetch(ENDPOINTS.vision, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("اكتمل تحليل الرؤية", "success");
      }
    } catch (e) {
      console.error(e);
      showToast("فشل رفع الصورة", "error");
    }
  }

  async function pingStatus() {
    try {
      const res = await fetch(ENDPOINTS.status);
      const data = await res.json();
      if (connectionStatus) {
        const dot = connectionStatus.querySelector(".sky-status-dot");
        const text = connectionStatus.querySelector(".sky-status-text");
        if (data && !data.error) {
          if (dot) dot.style.background = "#22c55e";
          if (text) text.innerHTML = '<i class="fas fa-plug"></i> متصل • جاهز';
        } else {
          if (dot) dot.style.background = "#f97316";
          if (text) text.innerHTML = '<i class="fas fa-exclamation-triangle"></i> متصل جزئياً';
        }
      }
    } catch {
      if (connectionStatus) {
        const dot = connectionStatus.querySelector(".sky-status-dot");
        const text = connectionStatus.querySelector(".sky-status-text");
        if (dot) dot.style.background = "#ef4444";
        if (text) text.innerHTML = '<i class="fas fa-ban"></i> غير متصل';
      }
    }
  }

  // ========== Quick Commands ==========

  function handleQuickCommand(text) {
    const t = text.trim();
    if (!t.startsWith("/")) return false;
    const cmd = t.split(/\s+/)[0].toLowerCase();
    switch (cmd) {
      case "/new": createNewSession(); return true;
      case "/clear": clearCurrentSession(); return true;
      case "/export": exportConversation(); return true;
      case "/help": showHelp(); return true;
      default: return false;
    }
  }

  function showHelp() {
    appendMessage("assistant", "📖 **الأوامر السريعة المتوفرة:**\n\n`/new` — إنشاء جلسة ذكية جديدة\n`/clear` — مسح ذاكرة الجلسة الحالية\n`/export` — تصدير المحادثة لملف JSON\n`/help` — عرض المساعدة المتقدمة");
  }

  function createNewSession() {
    const id = "s-" + Math.random().toString(36).slice(2, 12);
    setSession(id);
    loadLocalHistory();
    showToast("تم فتح منفذ جلسة جديد", "success");
  }

  function clearCurrentSession() {
    if (confirm("هل تريد مسح ذاكرة هذه الجلسة بالكامل؟")) {
      if (chatWindow) chatWindow.innerHTML = "";
      localStorage.removeItem(`sky_local_history_v10_${sessionId}`);
      appendMessage("assistant", "✨ تم تهيئة الجلسة ومسح السجلات المحلية بنجاح.");
      showToast("تم تصفية البيانات", "success");
    }
  }

  function exportConversation() {
    try {
      const key = `sky_local_history_v10_${sessionId}`;
      const raw = localStorage.getItem(key);
      const data = raw || "[]";
      const blob = new Blob([data], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `skyos_export_${sessionId.slice(0, 8)}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      showToast("تم تصدير ملف الجلسة بنجاح", "success");
    } catch (e) {
      console.error(e);
      showToast("فشل تصدير المحادثة", "error");
    }
  }

  // ========== Event Handlers & Mounting ==========

  function initEvents() {
    if (sendBtn && userInput) {
      sendBtn.addEventListener("click", () => sendMessage(userInput.value));
      userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          sendMessage(userInput.value);
        }
      });
      userInput.addEventListener("input", () => autoResizeTextarea(userInput));
    }

    if (toggleThemeBtn) {
      toggleThemeBtn.addEventListener("click", () => {
        setTheme(!isDark);
        showToast(isDark ? "تم تفعيل الوضع المظلم" : "تم تفعيل الوضع المضيء", "info");
      });
    }

    if (menuToggleBtn && sidebar) {
      menuToggleBtn.addEventListener("click", () => sidebar.classList.toggle("open"));
    }

    if (fileInput) fileInput.addEventListener("change", (e) => uploadFile(e.target.files[0]));
    if (miniUploadBtn && fileInput) miniUploadBtn.addEventListener("click", () => fileInput.click());

    if (hiddenAudioInput) hiddenAudioInput.addEventListener("change", (e) => uploadAudio(e.target.files[0]));
    if (voiceBtn && hiddenAudioInput) voiceBtn.addEventListener("click", () => hiddenAudioInput.click());
    if (miniVoiceBtn && hiddenAudioInput) miniVoiceBtn.addEventListener("click", () => hiddenAudioInput.click());

    if (hiddenImageInput) hiddenImageInput.addEventListener("change", (e) => uploadImage(e.target.files[0]));
    if (visionBtn && hiddenImageInput) visionBtn.addEventListener("click", () => hiddenImageInput.click());
    if (miniVisionBtn && hiddenImageInput) miniVisionBtn.addEventListener("click", () => hiddenImageInput.click());

    if (newSessionBtn) newSessionBtn.addEventListener("click", createNewSession);
    if (clearChatBtn) clearChatBtn.addEventListener("click", clearCurrentSession);
    if (exportChatBtn) exportChatBtn.addEventListener("click", exportConversation);

    if (openSettingsBtn && settingsPanel) {
      openSettingsBtn.addEventListener("click", () => settingsPanel.classList.toggle("hidden"));
    }
    if (openWorkspaceBtn && workspacePanel) {
      openWorkspaceBtn.addEventListener("click", () => workspacePanel.classList.toggle("hidden"));
    }
  }

  // محرك تفعيل الـ PWA لضمان العمل أوفلاين
  function registerPWA() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/service-worker.js')
          .then(reg => console.log('SkyOS Core: تم ربط الـ Service Worker بنجاح!'))
          .catch(err => console.error('PWA Error: فشل تسجيل محرك الأوفلاين:', err));
      });
    }
  }

  // ========== System Boot ==========
  document.addEventListener("DOMContentLoaded", () => {
    setSession(sessionId);
    loadLocalHistory();
    renderSessionList();
    initEvents();
    registerPWA(); // حقن التسجيل أثناء إقلاع النظام
    if (userInput) autoResizeTextarea(userInput);
    pingStatus();
    setInterval(pingStatus, 30000);
  });

})();
