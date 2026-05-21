/* ============================================================
   SkyOS v10.0 — Holographic Edition (JavaScript Engine)
   - تعديلات متقدمة شاملة للجوال
   - تفعيل أزرار التفاعل (نسخ، تحميل ملف، تقييم)
   - تصفية فورية وشاملة وإصلاح أخطاء الرفع الصامتة
   ============================================================ */

(() => {
  "use strict";

  const ENDPOINTS = (window.SKY_CONFIG && window.SKY_CONFIG.endpoints) || {
    ask: "/api/chat",
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
    setTimeout(() => {
      chatWindow.scrollTo({
        top: chatWindow.scrollHeight + 500,
        behavior: smooth ? "smooth" : "auto",
      });
    }, 100);
  }

  // توسيع ذكي وحقيقي متوافق مع شاشات الجوال
  function autoResizeTextarea(el) {
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 130) + "px";
  }

  function sanitizeAndFormat(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    let safe = div.innerHTML;

    const codeBlocks = [];
    safe = safe.replace(/```([\s\S]*?)```/g, (match, code) => {
      const id = `__SKY_CODE_BLOCK_${codeBlocks.length}__`;
      codeBlocks.push(`<pre class="sky-code-block"><code>${code.trim()}</code></pre>`);
      return id;
    });

    safe = safe.replace(/`([^`]+)`/g, '<code class="sky-inline-code">$1</code>');

    safe = safe.replace(
      /(https?:\/\/[^\s]+)/g,
      (m) => `<a href="${m}" target="_blank" rel="noopener noreferrer" style="color: var(--primary-3); text-decoration: underline;">${m}</a>`
    );
    
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    safe = safe.replace(/\*(.*?)\*/g, "<em>$1</em>");
    safe = safe.replace(/\n{2,}/g, "</p><p>").replace(/\n/g, "<br/>");
    
    codeBlocks.forEach((block, index) => {
      safe = safe.replace(`__SKY_CODE_BLOCK_${index}__`, block);
    });

    return `<p>${safe}</p>`;
  }

  // بناء الرسالة متضمناً أزرار نسخ، تحميل ملف، وتفاعل حقيقي كامل
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

    // إضافة شريط الأدوات المطور لرسائل النظام
    if (role === "assistant") {
      const actionParam = document.createElement("div");
      actionParam.className = "msg-action-bar";
      actionParam.innerHTML = `
        <button class="msg-action-btn copy-msg-btn" title="نسخ النص كاملاً"><i class="fas fa-copy"></i> نسخ</button>
        <button class="msg-action-btn file-msg-btn" title="تحويل لملف نصي"><i class="fas fa-file-download"></i> تصدير لملف</button>
        <button class="msg-action-btn good feedback-btn" data-score="1" style="margin-right:auto;"><i class="fas fa-thumbs-up"></i> مفيد</button>
        <button class="msg-action-btn bad feedback-btn" data-score="-1"><i class="fas fa-thumbs-down"></i> غير مفيد</button>
      `;
      bubble.appendChild(actionParam);

      // ربط أحداث النسخ والتصدير والتقييم الحقيقي
      actionParam.querySelector(".copy-msg-btn").addEventListener("click", () => {
        navigator.clipboard.writeText(text);
        showToast("تم نسخ نص رسالة سماء بنجاح!", "success");
      });

      actionParam.querySelector(".file-msg-btn").addEventListener("click", () => {
        const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `SkyOS_Response_${Date.now().toString().slice(-6)}.txt`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
        showToast("تم تحويل وتحميل الرسالة كملف بنجاح", "success");
      });

      const goodBtn = actionParam.querySelector(".good");
      const badBtn = actionParam.querySelector(".bad");
      goodBtn.addEventListener("click", () => sendFeedback(1, sessionId, text, goodBtn, badBtn));
      badBtn.addEventListener("click", () => sendFeedback(0, sessionId, text, goodBtn, badBtn));
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
    // تفعيل لوني فوري لتوضيح عمل الأزرار حتى قبل استجابة السيرفر
    if (score === 1) {
      goodBtn.style.color = "#22c55e";
      badBtn.style.color = "#94a3b8";
      showToast("شكراً على تقييمك الإيجابي! 🤍", "success");
    } else {
      badBtn.style.color = "#ef4444";
      goodBtn.style.color = "#94a3b8";
      showToast("شكراً على ملاحظاتك، سأتحسن! 🌱", "info");
    }

    try {
      await fetch(ENDPOINTS.feedback, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ score, session_id: sessId, comment: comment.slice(0, 50) })
      });
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
          <span style="margin-right: 8px;">جاري التفكير والتحليل...</span>
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
        appendMessage("assistant", "مرحباً… 🌌\n\nأنا **SkyOS Holographic v10**، نظام ذكاء هجين واعٍ لخدمتك.\n\n✨ يمكنك الآن:\n• إرسال ومناقشة كود البرمجة دون أي مشاكل في العرض أو المحاذاة للجوال 📱\n• رفع صور وملفات وتحليلها ومسح البيانات فورياً بضغطة زر.\n\n**أنا متصل وبانتظار أوامرك...** 🚀");
      } else {
        arr.forEach(m => appendMessage(m.role, m.content));
      }
      scrollToBottom(false);
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
        if (sidebar) sidebar.classList.remove("mobile-show");
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
        ai_type: $("#setting-ai-engine") ? $("#setting-ai-engine").value : "holo"
      });

      hideTypingIndicator();

      if (!resp || (!resp.reply && typeof resp !== "string")) {
        appendMessage("assistant", "حدث خطأ: لم يتم استلام رد صحيح من الخادم.");
        return;
      }

      const reply = resp.reply || resp;
      appendMessage("assistant", reply);
      addToHistoryLocal("assistant", reply);
    } catch (err) {
      hideTypingIndicator();
      appendMessage("assistant", "عذراً، واجهت مشكلة أثناء الاتصال بـ SkyOS. تأكد من أن السيرفر يعمل.");
    } finally {
      isSending = false;
    }
  }

  // إلغاء تعليق شاشة الرفع والتحليل فوراً عند الفشل
  async function uploadFile(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    fd.append("session_id", sessionId);

    appendMessage("user", `📄 [طلب رفع مستند: ${file.name}]`);
    showTypingIndicator();

    try {
      const res = await fetch(ENDPOINTS.upload, { method: "POST", body: fd });
      hideTypingIndicator(); // مسح مؤشر التحليل فورا لمنع التعليق
      if (!res.ok) throw new Error("Backend Error");
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
        addToHistoryLocal("assistant", data.reply);
      }
    } catch (e) {
      hideTypingIndicator(); // إجبار الإغلاق عند الخطأ
      appendMessage("assistant", `❌ عذراً، فشلت عملية معالجة ورفع الملف. (تأكد من إعداد الـ Backend لـ /upload)`);
    }
  }

  async function uploadAudio(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("audio", file);
    fd.append("session_id", sessionId);

    appendMessage("user", `🎙️ [طلب معالجة ملف صوتي]`);
    showTypingIndicator();

    try {
      const res = await fetch(ENDPOINTS.voice, { method: "POST", body: fd });
      hideTypingIndicator();
      if (!res.ok) throw new Error("Backend Error");
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
      }
    } catch (e) {
      hideTypingIndicator();
      appendMessage("assistant", `❌ فشل معالجة الملف الصوتي على المسار الحالي.`);
    }
  }

  async function uploadImage(file) {
    if (!file) return;
    const fd = new FormData();
    fd.append("image", file);
    fd.append("session_id", sessionId);

    appendMessage("user", `🖼️ [طلب تحليل صورة: ${file.name}]`);
    showTypingIndicator();

    try {
      const res = await fetch(ENDPOINTS.vision, { method: "POST", body: fd });
      hideTypingIndicator();
      if (!res.ok) throw new Error("Backend Error");
      const data = await res.json();
      if (data && data.reply) {
        appendMessage("assistant", data.reply);
      }
    } catch (e) {
      hideTypingIndicator();
      appendMessage("assistant", `فشل تحليل أو رفع الصورة. تأكد من تهيئة استقبال الصور في الـ Backend.`);
    }
  }

  async function pingStatus() {
    try {
      const res = await fetch(ENDPOINTS.status);
      const data = await res.json();
      if (connectionStatus) {
        const dot = connectionStatus.querySelector(".sky-status-dot");
        if (dot) dot.style.background = "#22c55e";
      }
    } catch {
      if (connectionStatus) {
        const dot = connectionStatus.querySelector(".sky-status-dot");
        if (dot) dot.style.background = "#ef4444";
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
      case "/help": showHelp(); return true;
      default: return false;
    }
  }

  function showHelp() {
    appendMessage("assistant", "📖 **الأوامر السريعة:**\n\n`/new` — جلسة جديدة\n`/clear` — مسح الذاكرة الحالية\n`/help` — عرض المساعدة");
  }

  function createNewSession() {
    const id = "s-" + Math.random().toString(36).slice(2, 12);
    setSession(id);
    loadLocalHistory();
    if (sidebar) sidebar.classList.remove("mobile-show");
    showToast("تم فتح منفذ جلسة جديد", "success");
  }

  // تصفية النافذة والمحادثة فورياً وإعادة البناء الترحيبي دون تعليق واجهة المستخدم
  function clearCurrentSession() {
    if (confirm("هل تريد مسح ذاكرة هذه الجلسة والنافذة بالكامل؟")) {
      localStorage.removeItem(`sky_local_history_v10_${sessionId}`);
      if (chatWindow) chatWindow.innerHTML = "";
      loadLocalHistory(); 
      if (sidebar) sidebar.classList.remove("mobile-show");
      showToast("تم تصفية وبناء النافذة بنجاح", "success");
    }
  }

  // ========== Event Handlers & Mounting ==========

  if (sendBtn) {
    sendBtn.addEventListener("click", () => {
      if (userInput) sendMessage(userInput.value.trim());
    });
  }

  if (userInput) {
    userInput.addEventListener("input", () => autoResizeTextarea(userInput));
    userInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage(userInput.value.trim());
      }
    });
  }

  if (newSessionBtn) newSessionBtn.addEventListener("click", createNewSession);
  if (clearChatBtn) clearChatBtn.addEventListener("click", clearCurrentSession);

  if (toggleThemeBtn) {
    toggleThemeBtn.addEventListener("click", () => setTheme(!isDark));
  }

  if (menuToggleBtn && sidebar) {
    menuToggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      sidebar.classList.toggle("mobile-show");
    });
  }

  if (chatWindow) {
    chatWindow.addEventListener("click", () => {
      if (sidebar && sidebar.classList.contains("mobile-show")) {
        sidebar.classList.remove("mobile-show");
      }
    });
  }

  if (miniUploadBtn && fileInput) miniUploadBtn.addEventListener("click", () => fileInput.click());
  if (fileInput) {
    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) uploadFile(e.target.files[0]);
    });
  }

  if ((voiceBtn || miniVoiceBtn) && hiddenAudioInput) {
    const triggerVoice = () => hiddenAudioInput.click();
    if (voiceBtn) voiceBtn.addEventListener("click", triggerVoice);
    if (miniVoiceBtn) miniVoiceBtn.addEventListener("click", triggerVoice);
  }
  if (hiddenAudioInput) {
    hiddenAudioInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) uploadAudio(e.target.files[0]);
    });
  }

  if ((visionBtn || miniVisionBtn) && hiddenImageInput) {
    const triggerVision = () => hiddenImageInput.click();
    if (visionBtn) visionBtn.addEventListener("click", triggerVision);
    if (miniVisionBtn) miniVisionBtn.addEventListener("click", triggerVision);
  }
  if (hiddenImageInput) {
    hiddenImageInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) uploadImage(e.target.files[0]);
    });
  }

  if (openSettingsBtn && settingsPanel) {
    openSettingsBtn.addEventListener("click", () => settingsPanel.classList.toggle("hidden"));
  }
  if (openWorkspaceBtn && workspacePanel) {
    openWorkspaceBtn.addEventListener("click", () => workspacePanel.classList.toggle("hidden"));
  }

  // أحداث لوحة التحكم الفعالة لتعديل مقاس الخط فوراً
  if ($("#setting-font-size")) {
    $("#setting-font-size").addEventListener("change", (e) => {
      if (chatWindow) chatWindow.style.fontSize = e.target.value;
      showToast("تم تحديث أبعاد الخط", "info");
    });
  }

  // ========== Initialization ==========
  function init() {
    setSession(sessionId);
    loadLocalHistory();
    renderSessionList();
    pingStatus();
    setInterval(pingStatus, 30000);
  }

  init();

})();
