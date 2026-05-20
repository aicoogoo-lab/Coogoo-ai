/* ============================================================
   SkyOS v7.2 — Crown Edition (JavaScript Engine)
   - جلسات ذكية
   - واجهة حية متحركة
   - ملفات / صوت / رؤية
   - Workspace + Settings
   - Toasts + Status + Theme
   - تم تصحيح جميع الأخطاء
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

  const LS_SESSION_KEY = "sky_session_id_v72";
  const LS_SESSIONS_LIST = "sky_sessions_list_v72";
  const LS_THEME_KEY = "sky_theme_v72";
  const LS_NOTES_KEY = "sky_workspace_notes_v72";

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
    renderWorkspaceSessions();
  }

  function showToast(text, type = "info", timeout = 4000) {
    if (!toastContainer) return;
    const t = document.createElement("div");
    t.className = "toast";
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

  function sanitizeAndFormat(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    let safe = div.innerHTML;
    safe = safe.replace(
      /(https?:\/\/[^\s]+)/g,
      (m) => `<a href="${m}" target="_blank" rel="noopener noreferrer" style="color: var(--primary-3);">${m}</a>`
    );
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    safe = safe.replace(/\*(.*?)\*/g, "<em>$1</em>");
    safe = safe.replace(/\n{2,}/g, "</p><p>").replace(/\n/g, "<br/>");
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

    // Feedback buttons for assistant messages only
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
    if (!chatWindow) return;
    if ($("#typing-indicator")) return;

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
          <span style="margin-right: 8px;">يكتب</span>
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

  function autoResizeTextarea(el) {
    if (!el) return;
    const resize = () => {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 180) + "px";
    };
    el.addEventListener("input", resize);
    resize();
  }

  // ========== Local History ==========

  function addToHistoryLocal(role, content) {
    try {
      const key = `sky_local_history_v72_${sessionId}`;
      const raw = localStorage.getItem(key);
      const arr = raw ? JSON.parse(raw) : [];
      arr.push({ role, content, t: Date.now() });
      const trimmed = arr.slice(-200);
      localStorage.setItem(key, JSON.stringify(trimmed));
    } catch {}
  }

  function loadLocalHistory() {
    try {
      const key = `sky_local_history_v72_${sessionId}`;
      const raw = localStorage.getItem(key);
      const arr = raw ? JSON.parse(raw) : [];
      if (!chatWindow) return;
      chatWindow.innerHTML = "";
      if (arr.length === 0) {
        appendMessage("assistant", "مرحباً… 🌌\n\nأنا **SkyOS Crown Edition v7.2**، نظام ذكاء هجين واعٍ.\n\n✨ يمكنك:\n• الدردشة معي بأي موضوع\n• رفع ملفات 📄\n• إرسال صور 🖼️ للتحليل\n• إرسال صوت 🎙️\n• استخدام الأوامر السريعة: /new, /clear, /export, /help\n\n**أنا جاهز. اكتب ما تريد…** 🚀");
      } else {
        arr.forEach(m => appendMessage(m.role, m.content));
      }
    } catch {}
  }

  // ========== Rendering ==========

  function renderSessionList() {
    if (!sessionListEl) return;
    sessionListEl.innerHTML = "";
    if (!sessions.length) {
      sessionListEl.innerHTML = `<div class="sky-session-empty" style="text-align:center; opacity:0.6;"><i class="fas fa-inbox"></i><br>لا يوجد أرشيف</div>`;
      return;
    }
    sessions.forEach((s) => {
      const item = document.createElement("div");
      item.className = "session-item";
      item.innerHTML = `<i class="fas fa-comment"></i> ${s.title}<br><small>${new Date(s.updated).toLocaleString("ar-SA")}</small>`;
      item.dataset.id = s.id;
      item.addEventListener("click", () => {
        if (s.id === sessionId) return;
        sessionId = s.id;
        localStorage.setItem(LS_SESSION_KEY, sessionId);
        if (sessionIndicator) {
          sessionIndicator.innerHTML = `<i class="fas fa-id-card"></i> جلسة: ${sessionId.slice(0, 8)}`;
        }
        loadLocalHistory();
        showToast("تم تبديل الجلسة", "success");
      });
      sessionListEl.appendChild(item);
    });
  }

  // ========== Network ==========

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
    isSending = true;
    if (userInput) userInput.value = "";
    appendMessage("user", text);
    addSessionRecord(sessionId, `جلسة ${sessionId.slice(2, 10)}`);
    addToHistoryLocal("user", text);

    showTypingIndicator();

    try {
      const resp = await postJSON(ENDPOINTS.ask, {
        message: text,
        session_id: sessionId,
        ai_type: "groq",
      });

      hideTypingIndicator();

      if (!resp) {
        appendMessage("assistant", "حدث خطأ: لم يتم استلام رد من الخادم.");
        showToast("خطأ في الاتصال بالمزود", "error");
        isSending = false;
        return;
      }

      if (typeof resp.reply === "string" && resp.reply.startsWith("REFUSE:")) {
        const msg = resp.reply.replace(/^REFUSE:\s*/i, "");
        appendMessage("assistant", msg);
        addToHistoryLocal("assistant", msg);
        isSending = false;
        return;
      }

      const reply = resp.reply || resp;
      appendMessage("assistant", reply);
      addSessionRecord(sessionId, `جلسة ${sessionId.slice(2, 10)}`);
      addToHistoryLocal("assistant", reply);

      if (resp.provider && modelIndicator) {
        modelIndicator.innerHTML = `<i class="fas fa-microchip"></i> النموذج: ${resp.provider}`;
      }
    } catch (err) {
      hideTypingIndicator();
      appendMessage("assistant", "عذراً، حدث خطأ أثناء معالجة الطلب.");
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

    showToast("جارٍ رفع الملف وتحليله...", "info");
    try {
      const res = await fetch(ENDPOINTS.upload, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم تحليل الملف", "success");
      } else {
        showToast("لم يتم تحليل الملف بنجاح", "error");
      }
    } catch (e) {
      console.error("uploadFile error:", e);
      showToast("فشل رفع الملف", "error");
    }
  }

  async function uploadAudio(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("audio", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ رفع الصوت وتحويله إلى نص...", "info");
    try {
      const res = await fetch(ENDPOINTS.voice, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم تحويل الصوت والرد", "success");
      } else {
        showToast("لم يتم تحويل الصوت بنجاح", "error");
      }
    } catch (e) {
      console.error("uploadAudio error:", e);
      showToast("فشل رفع الصوت", "error");
    }
  }

  async function uploadImage(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("image", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ رفع الصورة وتحليلها...", "info");
    try {
      const res = await fetch(ENDPOINTS.vision, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم تحليل الصورة", "success");
      } else {
        showToast("لم يتم تحليل الصورة بنجاح", "error");
      }
    } catch (e) {
      console.error("uploadImage error:", e);
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
    const cmd = text.trim().split(/\s+/)[0].toLowerCase();
    switch (cmd) {
      case "/new":
        createNewSession();
        return true;
      case "/clear":
        clearCurrentSession();
        return true;
      case "/export":
        exportConversation();
        return true;
      case "/workspace":
        toggleWorkspace();
        return true;
      case "/settings":
        toggleSettings();
        return true;
      case "/help":
        showHelp();
        return true;
      default:
        return false;
    }
  }

  function showHelp() {
    appendMessage("assistant", "📖 **الأوامر السريعة المتاحة:**\n\n/new — جلسة جديدة\n/clear — مسح المحادثة\n/export — تصدير المحادثة\n/workspace — فتح مساحة العمل\n/settings — فتح الإعدادات\n/help — عرض هذه المساعدة\n\n✨ يمكنك أيضاً رفع ملفات، صور، أو صوت.");
  }

  function createNewSession() {
    const id = "s-" + Math.random().toString(36).slice(2, 12);
    setSession(id);
    loadLocalHistory();
    showToast("جلسة جديدة جاهزة", "success");
  }

  function clearCurrentSession() {
    if (confirm("هل أنت متأكد من مسح جميع الرسائل؟")) {
      if (chatWindow) chatWindow.innerHTML = "";
      localStorage.removeItem(`sky_local_history_v72_${sessionId}`);
      appendMessage("assistant", "✨ تم مسح المحادثة. كيف يمكنني مساعدتك الآن؟");
      showToast("تم مسح المحادثة", "success");
    }
  }

  function exportConversation() {
    try {
      const key = `sky_local_history_v72_${sessionId}`;
      const raw = localStorage.getItem(key);
      const data = raw || "[]";
      const blob = new Blob([data], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `skyos_conversation_${sessionId.slice(0, 8)}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      showToast("تم تصدير المحادثة", "success");
    } catch (e) {
      console.error("exportConversation error:", e);
      showToast("فشل تصدير المحادثة", "error");
    }
  }

  // ========== Settings Panel ==========

  function buildSettingsPanel() {
    if (!settingsPanel) return;
    settingsPanel.classList.add("glass-layer");
    settingsPanel.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:15px;">
        <div style="font-weight:700;font-size:1rem;"><i class="fas fa-cog"></i> الإعدادات</div>
        <button class="sky-icon-btn" id="close-settings-btn"><i class="fas fa-times"></i></button>
      </div>
      <div style="font-size:0.85rem;color:var(--text-muted);margin-bottom:15px;">
        تحكم في مظهر النظام وبعض السلوكيات العامة.
      </div>

      <div style="margin-bottom:15px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:8px;"><i class="fas fa-palette"></i> المظهر</div>
        <div style="display:flex;gap:8px;">
          <button class="sky-btn-secondary" data-theme="light"><i class="fas fa-sun"></i> فاتح</button>
          <button class="sky-btn-secondary" data-theme="dark"><i class="fas fa-moon"></i> داكن</button>
        </div>
      </div>

      <div style="margin-bottom:15px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:8px;"><i class="fas fa-comments"></i> جلسة العمل</div>
        <button class="sky-btn-secondary full" id="settings-new-session"><i class="fas fa-plus"></i> جلسة جديدة</button>
        <button class="sky-btn-secondary full" id="settings-clear-session" style="margin-top:6px;"><i class="fas fa-trash-alt"></i> مسح المحادثة</button>
        <button class="sky-btn-secondary full" id="settings-export-chat" style="margin-top:6px;"><i class="fas fa-download"></i> تصدير المحادثة</button>
      </div>

      <div style="margin-top:15px;font-size:0.75rem;color:var(--text-muted);text-align:center;">
        <i class="fas fa-crown"></i> SkyOS Crown Edition v7.2
      </div>
    `;

    const closeBtn = $("#close-settings-btn");
    if (closeBtn) closeBtn.addEventListener("click", () => toggleSettings(false));

    $$("#settings-panel [data-theme]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const theme = btn.getAttribute("data-theme");
        setTheme(theme === "dark");
        showToast(theme === "dark" ? "تم تفعيل الوضع الداكن 🌙" : "تم تفعيل الوضع الفاتح ☀️", "success");
      });
    });

    const newSessionSettingsBtn = $("#settings-new-session");
    const clearSessionSettingsBtn = $("#settings-clear-session");
    const exportChatBtn = $("#settings-export-chat");
    
    if (newSessionSettingsBtn) newSessionSettingsBtn.addEventListener("click", createNewSession);
    if (clearSessionSettingsBtn) clearSessionSettingsBtn.addEventListener("click", clearCurrentSession);
    if (exportChatBtn) exportChatBtn.addEventListener("click", exportConversation);
  }

  function toggleSettings(force) {
    if (!settingsPanel) return;
    const visible = typeof force === "boolean" ? force : !settingsPanel.classList.contains("visible");
    settingsPanel.classList.toggle("visible", visible);
    settingsPanel.classList.toggle("hidden", !visible);
  }

  // ========== Workspace Panel ==========

  function buildWorkspacePanel() {
    if (!workspacePanel) return;
    workspacePanel.classList.add("glass-layer");
    workspacePanel.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:15px;">
        <div style="font-weight:700;font-size:1rem;"><i class="fas fa-folder-open"></i> مساحة العمل</div>
        <button class="sky-icon-btn" id="close-workspace-btn"><i class="fas fa-times"></i></button>
      </div>
      <div style="font-size:0.85rem;color:var(--text-muted);margin-bottom:15px;">
        نظرة سريعة على الجلسات الأخيرة والملاحظات الشخصية.
      </div>

      <div style="margin-bottom:15px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:8px;"><i class="fas fa-history"></i> الجلسات الأخيرة</div>
        <div id="workspace-sessions" style="max-height:200px;overflow:auto;border-radius:12px;border:1px solid rgba(255,255,255,0.1);padding:6px 8px;"></div>
      </div>

      <div style="margin-bottom:15px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:8px;"><i class="fas fa-pen"></i> ملاحظات سريعة</div>
        <textarea id="workspace-notes" placeholder="اكتب ملاحظاتك هنا..." style="width:100%;min-height:100px;border-radius:12px;border:1px solid rgba(255,255,255,0.15);padding:8px;font-size:0.85rem;background:rgba(0,0,0,0.4);color:#fff;"></textarea>
      </div>

      <div style="display:flex;justify-content:flex-end;gap:8px;">
        <button class="sky-btn-secondary" id="workspace-save-notes"><i class="fas fa-save"></i> حفظ الملاحظات</button>
        <button class="sky-btn-secondary" id="workspace-export-notes"><i class="fas fa-download"></i> تصدير</button>
      </div>
    `;

    const closeBtn = $("#close-workspace-btn");
    if (closeBtn) closeBtn.addEventListener("click", () => toggleWorkspace(false));

    renderWorkspaceSessions();
    
    const savedNotes = localStorage.getItem(LS_NOTES_KEY);
    const notesArea = $("#workspace-notes");
    if (notesArea && savedNotes) notesArea.value = savedNotes;
    
    const saveNotesBtn = $("#workspace-save-notes");
    if (saveNotesBtn) {
      saveNotesBtn.addEventListener("click", () => {
        const notes = $("#workspace-notes")?.value || "";
        localStorage.setItem(LS_NOTES_KEY, notes);
        showToast("تم حفظ الملاحظات", "success");
      });
    }

    const exportNotesBtn = $("#workspace-export-notes");
    if (exportNotesBtn) {
      exportNotesBtn.addEventListener("click", () => {
        const notes = $("#workspace-notes")?.value || "";
        const blob = new Blob([notes], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `skyos_notes_${new Date().toISOString().slice(0, 10)}.txt`;
        a.click();
        URL.revokeObjectURL(url);
        showToast("تم تصدير الملاحظات", "success");
      });
    }
  }

  function renderWorkspaceSessions() {
    const container = $("#workspace-sessions");
    if (!container) return;
    container.innerHTML = "";
    if (!sessions.length) {
      container.innerHTML = `<div style="text-align:center;opacity:0.6;"><i class="fas fa-inbox"></i><br>لا توجد جلسات</div>`;
      return;
    }
    sessions.slice(0, 8).forEach((s) => {
      const div = document.createElement("div");
      div.style.cssText = "padding:8px;border-radius:12px;cursor:pointer;margin-bottom:6px;transition:all0.2s";
      div.innerHTML = `<i class="fas fa-comment"></i> ${s.title}<br><small>${new Date(s.updated).toLocaleString("ar-SA")}</small>`;
      div.addEventListener("click", () => {
        sessionId = s.id;
        localStorage.setItem(LS_SESSION_KEY, sessionId);
        if (sessionIndicator) {
          sessionIndicator.innerHTML = `<i class="fas fa-id-card"></i> جلسة: ${sessionId.slice(0, 8)}`;
        }
        loadLocalHistory();
        showToast("تم فتح الجلسة", "success");
      });
      div.addEventListener("mouseenter", () => div.style.background = "var(--glass)");
      div.addEventListener("mouseleave", () => div.style.background = "transparent");
      container.appendChild(div);
    });
  }

  function loadWorkspaceNotes() {
    const notesEl = $("#workspace-notes");
    if (!notesEl) return;
    const saved = localStorage.getItem(LS_NOTES_KEY);
    if (saved) notesEl.value = saved;
  }

  function toggleWorkspace(force) {
    if (!workspacePanel) return;
    const visible = typeof force === "boolean" ? force : !workspacePanel.classList.contains("visible");
    workspacePanel.classList.toggle("visible", visible);
    workspacePanel.classList.toggle("hidden", !visible);
  }

  // ========== Particles Effect ==========

  function initParticles() {
    try {
      const canvas = document.getElementById("sky-particles");
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      let w = canvas.width = window.innerWidth;
      let h = canvas.height = window.innerHeight;
      const particles = [];
      const count = Math.max(12, Math.floor((w * h) / 120000));

      for (let i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * w,
          y: Math.random() * h,
          r: 20 + Math.random() * 60,
          vx: (Math.random() - 0.5) * 0.2,
          vy: (Math.random() - 0.5) * 0.2,
          hue: 260 + Math.random() * 120
        });
      }

      function draw() {
        if (!ctx) return;
        ctx.clearRect(0, 0, w, h);
        particles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < -200) p.x = w + 200;
          if (p.x > w + 200) p.x = -200;
          if (p.y < -200) p.y = h + 200;
          if (p.y > h + 200) p.y = -200;
          const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
          g.addColorStop(0, `hsla(${p.hue}, 90%, 60%, 0.12)`);
          g.addColorStop(0.6, `hsla(${p.hue}, 80%, 50%, 0.04)`);
          g.addColorStop(1, "rgba(0,0,0,0)");
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fill();
        });
        requestAnimationFrame(draw);
      }

      window.addEventListener("resize", () => {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
      });

      draw();
    } catch (e) {
      console.warn("Particles init failed", e);
    }
  }

  // ========== Event Setup ==========

  function setupEvents() {
    if (sendBtn && userInput) {
      sendBtn.addEventListener("click", () => {
        const text = userInput.value.trim();
        if (!text) return;
        if (handleQuickCommand(text)) {
          userInput.value = "";
          return;
        }
        sendMessage(text);
      });

      userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          const text = userInput.value.trim();
          if (!text) return;
          if (handleQuickCommand(text)) {
            userInput.value = "";
            return;
          }
          sendMessage(text);
        }
      });
    }

    if (fileInput) {
      fileInput.addEventListener("change", (e) => {
        if (e.target.files[0]) uploadFile(e.target.files[0]);
        fileInput.value = "";
      });
    }

    if (hiddenAudioInput) {
      hiddenAudioInput.addEventListener("change", (e) => {
        if (e.target.files[0]) uploadAudio(e.target.files[0]);
        hiddenAudioInput.value = "";
      });
    }

    if (hiddenImageInput) {
      hiddenImageInput.addEventListener("change", (e) => {
        if (e.target.files[0]) uploadImage(e.target.files[0]);
        hiddenImageInput.value = "";
      });
    }

    if (voiceBtn && hiddenAudioInput) voiceBtn.addEventListener("click", () => hiddenAudioInput.click());
    if (visionBtn && hiddenImageInput) visionBtn.addEventListener("click", () => hiddenImageInput.click());
    if (miniUploadBtn && fileInput) miniUploadBtn.addEventListener("click", () => fileInput.click());
    if (miniVoiceBtn && hiddenAudioInput) miniVoiceBtn.addEventListener("click", () => hiddenAudioInput.click());
    if (miniVisionBtn && hiddenImageInput) miniVisionBtn.addEventListener("click", () => hiddenImageInput.click());

    if (newSessionBtn) newSessionBtn.addEventListener("click", createNewSession);
    if (clearChatBtn) clearChatBtn.addEventListener("click", clearCurrentSession);
    if (exportChatBtn) exportChatBtn.addEventListener("click", exportConversation);

    if (toggleThemeBtn) {
      toggleThemeBtn.addEventListener("click", () => {
        setTheme(!isDark);
        showToast(isDark ? "تم تفعيل الوضع الفاتح ☀️" : "تم تفعيل الوضع الداكن 🌙", "success");
      });
    }

    if (openSettingsBtn) openSettingsBtn.addEventListener("click", () => toggleSettings());
    if (openWorkspaceBtn) openWorkspaceBtn.addEventListener("click", () => toggleWorkspace());

    if (menuToggleBtn && sidebar) {
      menuToggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open");
      });
    }

    // Drag & Drop
    if (chatWindow) {
      ["dragenter", "dragover"].forEach((ev) => {
        chatWindow.addEventListener(ev, (e) => {
          e.preventDefault();
          e.stopPropagation();
          chatWindow.classList.add("drag-over");
        });
      });
      ["dragleave", "drop"].forEach((ev) => {
        chatWindow.addEventListener(ev, (e) => {
          e.preventDefault();
          e.stopPropagation();
          chatWindow.classList.remove("drag-over");
        });
      });
      chatWindow.addEventListener("drop", (e) => {
        const files = e.dataTransfer.files;
        if (!files || !files.length) return;
        const file = files[0];
        if (file.type.startsWith("image/")) {
          uploadImage(file);
        } else if (file.type.startsWith("audio/")) {
          uploadAudio(file);
        } else {
          uploadFile(file);
        }
      });
    }

    // Parallax effect for background
    const grad = document.querySelector(".sky-gradient");
    if (grad) {
      window.addEventListener("mousemove", (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        grad.style.transform = `translate(${x}px, ${y}px)`;
      });
    }

    setInterval(pingStatus, 30000);
  }

  // ========== Initialization ==========

  setSession(sessionId);
  renderSessionList();
  buildSettingsPanel();
  buildWorkspacePanel();
  loadWorkspaceNotes();
  loadLocalHistory();
  pingStatus();
  setupEvents();
  autoResizeTextarea(userInput);
  initParticles();
})();
