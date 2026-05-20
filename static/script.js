/* ============================================================
   script.js — SkyOS v5.2 Pro (Ultra)
   - جلسات ذكية
   - Workspace
   - Settings
   - أوامر سريعة
   - صوت + رؤية + ملفات
   - Toasts + Status + Theme
   ============================================================ */

(() => {
  "use strict";

  /* ============================
     Helpers & Config
     ============================ */

  const ENDPOINTS = (window.SKY_CONFIG && window.SKY_CONFIG.endpoints) || {
    ask: "/ask",
    upload: "/upload",
    voice: "/voice",
    vision: "/vision",
    feedback: "/feedback",
    clear: "/clear",
    status: "/api/v1/status",
  };

  const LS_SESSION_KEY = "sky_session_id_v52";
  const LS_SESSIONS_LIST = "sky_sessions_list_v52";
  const LS_THEME_KEY = "sky_theme_v52";

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  /* ============================
     State
     ============================ */

  let sessionId = loadOrCreateSessionId();
  let sessions = loadSessions();
  let isDark = loadTheme();
  let isSending = false;

  // UI elements
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

  /* ============================
     Utilities
     ============================ */

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
      document.body.classList.add("dark");
      return true;
    }
    if (saved === "light") {
      document.body.classList.remove("dark");
      return false;
    }
    return document.body.classList.contains("dark");
  }

  function setTheme(dark) {
    isDark = dark;
    document.body.classList.toggle("dark", dark);
    localStorage.setItem(LS_THEME_KEY, dark ? "dark" : "light");
  }

  function setSession(id) {
    sessionId = id;
    localStorage.setItem(LS_SESSION_KEY, id);
    sessionIndicator.textContent = `جلسة: ${id.slice(0, 8)}`;
    addSessionRecord(id, `جلسة ${id.slice(2, 10)}`);
  }

  function addSessionRecord(id, title = "جلسة جديدة") {
    sessions = sessions.filter((s) => s.id !== id);
    sessions.unshift({ id, title, updated: Date.now() });
    saveSessions();
    renderSessionList();
  }

  function showToast(text, timeout = 4200) {
    const t = document.createElement("div");
    t.className = "toast";
    t.textContent = text;
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
      (m) => `<a href="${m}" target="_blank" rel="noopener noreferrer">${m}</a>`
    );
    safe = safe.replace(/\n{2,}/g, "</p><p>").replace(/\n/g, "<br/>");
    return `<p>${safe}</p>`;
  }

  function createMessageElement({ role = "assistant", text = "", time = null }) {
    const row = document.createElement("div");
    row.className = `message-row ${role === "user" ? "user" : "assistant"}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar " + (role === "user" ? "user-avatar" : "assistant-avatar");
    avatar.textContent = role === "user" ? "أنت" : "س";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const header = document.createElement("div");
    header.className = "message-header";
    const author = document.createElement("span");
    author.className = "message-author";
    author.textContent = role === "user" ? "أنت" : "سماء";
    const timeEl = document.createElement("span");
    timeEl.className = "message-time";
    timeEl.style.marginLeft = "8px";
    timeEl.textContent = time || formatTime();

    header.appendChild(author);
    header.appendChild(timeEl);

    const content = document.createElement("div");
    content.className = "message-content";
    content.innerHTML = sanitizeAndFormat(text);

    bubble.appendChild(header);
    bubble.appendChild(content);

    row.appendChild(avatar);
    row.appendChild(bubble);

    return row;
  }

  function appendMessage(role, text) {
    const el = createMessageElement({ role, text });
    chatWindow.appendChild(el);
    scrollToBottom();
  }

  function showTypingIndicator() {
    if ($("#typing-indicator")) return;
    const row = document.createElement("div");
    row.id = "typing-indicator";
    row.className = "message-row assistant";
    row.style.opacity = "0.9";

    const avatar = document.createElement("div");
    avatar.className = "avatar assistant-avatar";
    avatar.textContent = "س";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.style.maxWidth = "40%";
    bubble.innerHTML = `<div class="message-header">
        <span class="message-author">سماء</span>
        <span class="message-time">${formatTime()}</span>
      </div>
      <div class="message-content"><em>يكتب...</em></div>`;

    row.appendChild(avatar);
    row.appendChild(bubble);
    chatWindow.appendChild(row);
    scrollToBottom();
  }

  function hideTypingIndicator() {
    const el = $("#typing-indicator");
    if (el) el.remove();
  }

  /* ============================
     Local history mirror
     ============================ */

  function addToHistoryLocal(role, content) {
    try {
      const key = "sky_local_history_v52_" + sessionId;
      const raw = localStorage.getItem(key);
      const arr = raw ? JSON.parse(raw) : [];
      arr.push({ role, content, t: Date.now() });
      const trimmed = arr.slice(-150);
      localStorage.setItem(key, JSON.stringify(trimmed));
    } catch {}
  }

  function loadLocalHistory() {
    try {
      const key = "sky_local_history_v52_" + sessionId;
      const raw = localStorage.getItem(key);
      const arr = raw ? JSON.parse(raw) : [];
      arr.forEach((m) => appendMessage(m.role, m.content));
    } catch {}
  }

  /* ============================
     Rendering
     ============================ */

  function renderSessionList() {
    if (!sessionListEl) return;
    sessionListEl.innerHTML = "";
    if (!sessions.length) {
      const empty = document.createElement("div");
      empty.className = "sky-session-empty";
      empty.textContent = "لا يوجد أرشيف بعد";
      sessionListEl.appendChild(empty);
      return;
    }
    sessions.forEach((s) => {
      const item = document.createElement("div");
      item.className = "session-item";
      item.textContent = `${s.title} • ${new Date(s.updated).toLocaleString("ar-SA")}`;
      item.dataset.id = s.id;
      item.addEventListener("click", () => {
        if (s.id === sessionId) return;
        sessionId = s.id;
        localStorage.setItem(LS_SESSION_KEY, sessionId);
        sessionIndicator.textContent = `جلسة: ${sessionId.slice(0, 8)}`;
        chatWindow.innerHTML = "";
        loadLocalHistory();
        showToast("تم تبديل الجلسة");
      });
      sessionListEl.appendChild(item);
    });
  }

  /* ============================
     Network: ask / upload / voice / vision
     ============================ */

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
    userInput.value = "";
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
        showToast("خطأ في الاتصال بالمزود");
        isSending = false;
        return;
      }

      if (typeof resp.reply === "string" && resp.reply.startsWith("REFUSE:")) {
        appendMessage("assistant", resp.reply.replace(/^REFUSE:\s*/i, ""));
        isSending = false;
        return;
      }

      const reply = resp.reply || resp;
      appendMessage("assistant", reply);
      addSessionRecord(sessionId, `جلسة ${sessionId.slice(2, 10)}`);
      addToHistoryLocal("assistant", reply);

      if (resp.provider) {
        modelIndicator.textContent = `النموذج: ${resp.provider}`;
      }
    } catch (err) {
      hideTypingIndicator();
      appendMessage("assistant", "عذراً، حدث خطأ أثناء معالجة الطلب.");
      console.error("sendMessage error:", err);
      showToast("فشل إرسال الرسالة");
    } finally {
      isSending = false;
    }
  }

  async function uploadFile(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ رفع الملف وتحليله...");
    try {
      const res = await fetch(ENDPOINTS.upload, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم تحليل الملف");
      } else {
        showToast("لم يتم تحليل الملف بنجاح");
      }
    } catch (e) {
      console.error("uploadFile error:", e);
      showToast("فشل رفع الملف");
    }
  }

  async function uploadAudio(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("audio", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ رفع الصوت وتحويله إلى نص...");
    try {
      const res = await fetch(ENDPOINTS.voice, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم تحويل الصوت والرد");
      } else {
        showToast("لم يتم تحويل الصوت بنجاح");
      }
    } catch (e) {
      console.error("uploadAudio error:", e);
      showToast("فشل رفع الصوت");
    }
  }

  async function uploadImage(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("image", file);
    fd.append("session_id", sessionId);

    showToast("جارٍ رفع الصورة وتحليلها...");
    try {
      const res = await fetch(ENDPOINTS.vision, { method: "POST", body: fd });
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
        showToast("تم تحليل الصورة");
      } else {
        showToast("لم يتم تحليل الصورة بنجاح");
      }
    } catch (e) {
      console.error("uploadImage error:", e);
      showToast("فشل رفع الصورة");
    }
  }

  /* ============================
     Quick Commands
     ============================ */

  function handleQuickCommand(text) {
    const cmd = text.trim().split(/\s+/)[0].toLowerCase();
    switch (cmd) {
      case "/new":
       ===========
     Quick Commands
     ============================ */

  function handleQuickCommand(text) {
    const cmd = text.trim().split(/\s+/)[0].toLowerCase();
    switch (cmd) {
      case "/new":
        createNewSession();
        return true;
      case "/clear":
        clearCurrentSession();
        return true;
      case "/workspace":
        toggleWorkspace();
        return true;
      case "/settings":
        toggleSettings();
        return true;
      default:
        return false;
    }
  }

  function createNewSession() {
    const id = "s-" + Math.random().toString(36).slice(2, 12);
    setSession(id);
    chatWindow.innerHTML = "";
    appendMessage("assistant", "تم إنشاء جلسة جديدة. مرحباً بك يا سيدي.");
    showToast("جلسة جديدة جاهزة");
  }

  function clearCurrentSession() {
    chatWindow.innerHTML = "";
    localStorage.removeItem("sky_local_history_v52_" + sessionId);
    appendMessage("assistant", "تم مسح محتوى الجلسة الحالية محلياً.");
    showToast("تم مسح الجلسة محلياً");
  }

  /* ============================
     Settings Panel
     ============================ */

  function buildSettingsPanel() {
    if (!settingsPanel) return;
    settingsPanel.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
        <div style="font-weight:700;font-size:0.95rem;">الإعدادات</div>
        <button class="sky-icon-btn" id="close-settings-btn">✕</button>
      </div>
      <div style="font-size:0.85rem;color:var(--text-muted);margin-bottom:10px;">
        تحكم في مظهر النظام وبعض السلوكيات العامة.
      </div>

      <div style="margin-bottom:14px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:4px;">المظهر</div>
        <div style="display:flex;gap:8px;">
          <button class="sky-btn-secondary" data-theme="light">وضع فاتح</button>
          <button class="sky-btn-secondary" data-theme="dark">وضع داكن</button>
        </div>
      </div>

      <div style="margin-bottom:14px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:4px;">جلسة العمل</div>
        <button class="sky-btn-secondary full" id="settings-new-session">جلسة جديدة</button>
        <button class="sky-btn-secondary full" id="settings-clear-session" style="margin-top:6px;">مسح محتوى الجلسة الحالية</button>
      </div>

      <div style="margin-top:auto;font-size:0.75rem;color:var(--text-muted);">
        SkyOS v5.2 • واجهة تجريبية متقدمة
      </div>
    `;

    const closeBtn = $("#close-settings-btn");
    if (closeBtn) closeBtn.addEventListener("click", () => toggleSettings(false));

    $$("#settings-panel [data-theme]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const theme = btn.getAttribute("data-theme");
        setTheme(theme === "dark");
        showToast(theme === "dark" ? "تم تفعيل الوضع الداكن" : "تم تفعيل الوضع الفاتح");
      });
    });

    const newSessionSettingsBtn = $("#settings-new-session");
    const clearSessionSettingsBtn = $("#settings-clear-session");
    if (newSessionSettingsBtn) newSessionSettingsBtn.addEventListener("click", createNewSession);
    if (clearSessionSettingsBtn) clearSessionSettingsBtn.addEventListener("click", clearCurrentSession);
  }

  function toggleSettings(force) {
    if (!settingsPanel) return;
    const visible = typeof force === "boolean" ? force : !settingsPanel.classList.contains("visible");
    settingsPanel.classList.toggle("visible", visible);
    settingsPanel.classList.toggle("hidden", !visible);
  }

  /* ============================
     Workspace Panel
     ============================ */

  function buildWorkspacePanel() {
    if (!workspacePanel) return;
    workspacePanel.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
        <div style="font-weight:700;font-size:0.95rem;">مساحة العمل</div>
        <button class="sky-icon-btn" id="close-workspace-btn">✕</button>
      </div>
      <div style="font-size:0.85rem;color:var(--text-muted);margin-bottom:10px;">
        نظرة سريعة على الجلسات الأخيرة وبعض المعلومات المحلية.
      </div>

      <div style="margin-bottom:12px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:4px;">الجلسات الأخيرة</div>
        <div id="workspace-sessions" style="max-height:180px;overflow:auto;border-radius:12px;border:1px solid var(--border);padding:6px 8px;"></div>
      </div>

      <div style="margin-bottom:12px;">
        <div style="font-size:0.85rem;font-weight:600;margin-bottom:4px;">ملاحظات</div>
        <textarea id="workspace-notes" style="width:100%;min-height:80px;border-radius:12px;border:1px solid var(--border);padding:8px;font-size:0.85rem;background:var(--bg);color:var(--text);"></textarea>
      </div>

      <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:6px;">
        <button class="sky-btn-secondary" id="workspace-save-notes">حفظ الملاحظات</button>
      </div>
    `;

    const closeBtn = $("#close-workspace-btn");
    if (closeBtn) closeBtn.addEventListener("click", () => toggleWorkspace(false));

    renderWorkspaceSessions();
    loadWorkspaceNotes();

    const saveNotesBtn = $("#workspace-save-notes");
    if (saveNotesBtn) {
      saveNotesBtn.addEventListener("click", () => {
        const notes = $("#workspace-notes").value || "";
        localStorage.setItem("sky_workspace_notes_v52", notes);
        showToast("تم حفظ الملاحظات");
      });
    }
  }

  function renderWorkspaceSessions() {
    const container = $("#workspace-sessions");
    if (!container) return;
    container.innerHTML = "";
    if (!sessions.length) {
      container.innerHTML = `<div style="font-size:0.8rem;color:var(--text-muted);">لا توجد جلسات محفوظة بعد.</div>`;
      return;
    }
    sessions.slice(0, 10).forEach((s) => {
      const div = document.createElement("div");
      div.style.fontSize = "0.8rem";
      div.style.padding = "4px 6px";
      div.style.borderRadius = "8px";
      div.style.cursor = "pointer";
      div.style.marginBottom = "4px";
      div.style.transition = "background 0.18s";
      div.textContent = `${s.title} • ${new Date(s.updated).toLocaleString("ar-SA")}`;
      div.addEventListener("click", () => {
        sessionId = s.id;
        localStorage.setItem(LS_SESSION_KEY, sessionId);
        sessionIndicator.textContent = `جلسة: ${sessionId.slice(0, 8)}`;
        chatWindow.innerHTML = "";
        loadLocalHistory();
        showToast("تم فتح الجلسة من مساحة العمل");
      });
      div.addEventListener("mouseover", () => {
        div.style.background = "var(--primary-soft)";
      });
      div.addEventListener("mouseout", () => {
        div.style.background = "transparent";
      });
      container.appendChild(div);
    });
  }

  function loadWorkspaceNotes() {
    const notesEl = $("#workspace-notes");
    if (!notesEl) return;
    const saved = localStorage.getItem("sky_workspace_notes_v52");
    if (saved) notesEl.value = saved;
  }

  function toggleWorkspace(force) {
    if (!workspacePanel) return;
    const visible = typeof force === "boolean" ? force : !workspacePanel.classList.contains("visible");
    workspacePanel.classList.toggle("visible", visible);
    workspacePanel.classList.toggle("hidden", !visible);
    if (visible) renderWorkspaceSessions();
  }

  /* ============================
     Status Polling
     ============================ */

  async function pollStatus() {
    try {
      const res = await fetch(ENDPOINTS.status);
      const data = await res.json();
      if (data) {
        const online = data.groq || data.gemini || data.openai;
        const dot = connectionStatus.querySelector(".sky-status-dot");
        const text = connectionStatus.querySelector(".sky-status-text");
        if (online) {
          dot.classList.remove("offline");
          dot.classList.add("online");
          text.textContent = "متصل • جاهز";
        } else {
          dot.classList.remove("online");
          dot.classList.add("offline");
          text.textContent = "غير متصل • في وضع الانتظار";
        }
      }
    } catch (e) {
      // silent
    } finally {
      setTimeout(pollStatus, 8000);
    }
  }

  /* ============================
     Event Listeners
     ============================ */

  sendBtn.addEventListener("click", () => {
    const text = userInput.value.trim();
    if (!text) return;
    if (text.startsWith("/")) {
      if (handleQuickCommand(text)) {
        userInput.value = "";
        return;
      }
    }
    sendMessage(text);
  });

  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const text = userInput.value.trim();
      if (!text) return;
      if (text.startsWith("/")) {
        if (handleQuickCommand(text)) {
          userInput.value = "";
          return;
        }
      }
      sendMessage(text);
    }
  });

  userInput.addEventListener("input", () => {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(220, userInput.scrollHeight) + "px";
  });

  newSessionBtn.addEventListener("click", createNewSession);

  fileInput.addEventListener("change", (e) => {
    const f = e.target.files && e.target.files[0];
    if (f) uploadFile(f);
    fileInput.value = "";
  });

  miniUploadBtn.addEventListener("click", () => fileInput.click());
  miniVoiceBtn.addEventListener("click", () => hiddenAudioInput.click());
  miniVisionBtn.addEventListener("click", () => hiddenImageInput.click());

  hiddenAudioInput.addEventListener("change", (e) => {
    const f = e.target.files && e.target.files[0];
    if (f) uploadAudio(f);
    hiddenAudioInput.value = "";
  });

  hiddenImageInput.addEventListener("change", (e) => {
    const f = e.target.files && e.target.files[0];
    if (f) uploadImage(f);
    hiddenImageInput.value = "";
  });

  voiceBtn.addEventListener("click", () => hiddenAudioInput.click());
  visionBtn.addEventListener("click", () => hiddenImageInput.click());

  toggleThemeBtn.addEventListener("click", () => {
    setTheme(!isDark);
    showToast(isDark ? "الوضع الداكن مفعل" : "الوضع الفاتح مفعل");
  });

  openSettingsBtn.addEventListener("click", () => toggleSettings());
  openWorkspaceBtn.addEventListener("click", () => toggleWorkspace());

  chatWindow.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
  });
  chatWindow.addEventListener("drop", (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) {
      if (f.type.startsWith("image/")) uploadImage(f);
      else if (f.type.startsWith("audio/")) uploadAudio(f);
      else uploadFile(f);
    }
  });

  /* ============================
     Initialization
     ============================ */

  function init() {
    setSession(sessionId);
    renderSessionList();
    loadLocalHistory();

    if (!chatWindow.children.length) {
      appendMessage(
        "assistant",
        "مرحباً سيدي، هنا سماء — جاهزة للعمل. اكتب ما تريد، أو استخدم الأوامر السريعة مثل /new أو /clear أو /workspace."
      );
    }

    buildSettingsPanel();
    buildWorkspacePanel();
    pollStatus();
    userInput.focus();
    scrollToBottom(false);
  }

  window.SkyUI = {
    setSession,
    appendMessage,
    showToast,
    getSessionId: () => sessionId,
  };

  init();
})();
