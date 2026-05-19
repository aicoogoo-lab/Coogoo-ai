// static/script.js - النسخة الجبارة
let currentSessionId = localStorage.getItem('sky_session_id') || null;
let messageCount = 0;

// تهيئة المتغيرات
const messagesEl = document.getElementById("messages");
const chatContainer = document.getElementById("chat-container");
const typingEl = document.getElementById("typing");
const inputEl = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const groqBtn = document.getElementById("groq-btn");
const geminiBtn = document.getElementById("gemini-btn");
const clearBtn = document.getElementById("clear-btn");
const settingsBtn = document.getElementById("settings-btn");
const settingsPanel = document.getElementById("settings-panel");
const closeSettingsBtn = document.getElementById("close-settings");
const defaultModelSelect = document.getElementById("default-model");
const fileUpload = document.getElementById("file-upload");
const urlBtn = document.getElementById("url-btn");
const msgCountSpan = document.getElementById("msg-count");

let selectedModel = localStorage.getItem('sky_selected_model') || "groq";

// تحديث عدد الرسائل
function updateMsgCount() {
    const count = document.querySelectorAll('#messages .message').length;
    if (msgCountSpan) msgCountSpan.innerText = `${count} رسالة`;
}

// إضافة رسالة مع نسخ
function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.textContent = text;
    
    if (sender === "assistant") {
        const copyBtn = document.createElement("button");
        copyBtn.className = "copy-btn";
        copyBtn.textContent = "📋";
        copyBtn.title = "نسخ";
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(text);
            copyBtn.textContent = "✅";
            setTimeout(() => copyBtn.textContent = "📋", 2000);
        };
        div.appendChild(copyBtn);
    }
    
    messagesEl.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    updateMsgCount();
    saveMessagesToLocal();
}

// حفظ واستعادة الرسائل
function saveMessagesToLocal() {
    const msgs = [];
    document.querySelectorAll('#messages .message').forEach(el => {
        let text = el.childNodes[0]?.nodeValue || el.innerText;
        text = text.replace(/[📋✅]|نسخ/gi, '').trim();
        const sender = el.classList.contains('user') ? 'user' : 'assistant';
        msgs.push({ text, sender });
    });
    localStorage.setItem('sky_messages_v3', JSON.stringify(msgs));
    localStorage.setItem('sky_session_id', currentSessionId || '');
}

function restoreMessages() {
    const saved = localStorage.getItem('sky_messages_v3');
    const savedSession = localStorage.getItem('sky_session_id');
    
    if (savedSession) currentSessionId = savedSession;
    
    if (saved) {
        try {
            const msgs = JSON.parse(saved);
            messagesEl.innerHTML = '';
            msgs.forEach(m => {
                const div = document.createElement("div");
                div.className = `message ${m.sender}`;
                div.textContent = m.text;
                if (m.sender === "assistant") {
                    const copyBtn = document.createElement("button");
                    copyBtn.className = "copy-btn";
                    copyBtn.textContent = "📋";
                    copyBtn.onclick = () => {
                        navigator.clipboard.writeText(m.text);
                        copyBtn.textContent = "✅";
                        setTimeout(() => copyBtn.textContent = "📋", 2000);
                    };
                    div.appendChild(copyBtn);
                }
                messagesEl.appendChild(div);
            });
        } catch(e) {}
    } else {
        // رسالة ترحيب
        addMessage("✨ مرحباً بك في سماء! أنا مساعدك الذكي. أسألني أي شيء، وسأتذكر كل تفاصيل محادثتنا. ✨", "assistant");
    }
    updateMsgCount();
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// إرسال رسالة مع ذاكرة كاملة
async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;
    
    addMessage(text, "user");
    inputEl.value = "";
    typingEl.classList.remove("hidden");
    
    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "X-Session-Id": currentSessionId || ''
            },
            body: JSON.stringify({ 
                message: text, 
                ai_type: selectedModel,
                session_id: currentSessionId
            })
        });
        const data = await res.json();
        
        if (data.session_id && !currentSessionId) {
            currentSessionId = data.session_id;
            localStorage.setItem('sky_session_id', currentSessionId);
        }
        
        typingEl.classList.add("hidden");
        
        // عرض معلومات الذاكرة
        let replyText = data.reply;
        if (data.context_used && data.context_used > 0) {
            replyText += `\n\n📌 (أتذكر ${data.context_used} رسالة سابقة)`;
        }
        if (data.provider && data.provider !== 'none') {
            // لا نعرض معلومات المزود للمستخدم العادي
        }
        
        addMessage(replyText, "assistant");
    } catch (e) {
        typingEl.classList.add("hidden");
        addMessage("⚠️ تعذر الاتصال بسماء. تأكد من اتصال الإنترنت.", "assistant");
    }
}

// تبديل النموذج
function setModel(model) {
    selectedModel = model;
    localStorage.setItem('sky_selected_model', model);
    if (groqBtn && geminiBtn) {
        groqBtn.classList.toggle("active", model === "groq");
        geminiBtn.classList.toggle("active", model === "gemini");
    }
}

// مسح المحادثة
async function clearConversation() {
    if (confirm("هل تريد مسح كل المحادثة؟ سيتم حذف الذاكرة بالكامل.")) {
        messagesEl.innerHTML = "";
        localStorage.removeItem("sky_messages_v3");
        
        if (currentSessionId) {
            try {
                await fetch("/clear", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ session_id: currentSessionId })
                });
            } catch(e) {}
        }
        
        currentSessionId = null;
        localStorage.removeItem('sky_session_id');
        addMessage("✨ تم مسح المحادثة والذاكرة بالكامل. يمكنك البدء من جديد. ✨", "assistant");
    }
}

// رفع ملف
async function uploadFile(file) {
    if (!file) return;
    addMessage(`📎 جاري رفع وتحليل: ${file.name}`, "user");
    typingEl.classList.remove("hidden");
    
    const formData = new FormData();
    formData.append("file", file);
    if (currentSessionId) formData.append("session_id", currentSessionId);
    
    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData,
            headers: { "X-Session-Id": currentSessionId || '' }
        });
        const data = await res.json();
        typingEl.classList.add("hidden");
        
        if (data.session_id && !currentSessionId) {
            currentSessionId = data.session_id;
            localStorage.setItem('sky_session_id', currentSessionId);
        }
        
        addMessage(data.reply, "assistant");
    } catch(e) {
        typingEl.classList.add("hidden");
        addMessage("⚠️ فشل رفع الملف.", "assistant");
    }
}

// رابط
function sendUrl() {
    const url = prompt("ألصق الرابط هنا:");
    if (url && url.startsWith('http')) {
        inputEl.value = url;
        sendMessage();
    } else if(url) {
        alert("الرجاء إدخال رابط صحيح يبدأ بـ http:// أو https://");
    }
}

// ============================================================================
// ربط الأحداث
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    if (sendBtn) sendBtn.addEventListener("click", sendMessage);
    if (inputEl) inputEl.addEventListener("keypress", (e) => { if (e.key === "Enter") sendMessage(); });
    if (groqBtn) groqBtn.addEventListener("click", () => setModel("groq"));
    if (geminiBtn) geminiBtn.addEventListener("click", () => setModel("gemini"));
    if (clearBtn) clearBtn.addEventListener("click", clearConversation);
    if (urlBtn) urlBtn.addEventListener("click", sendUrl);
    if (fileUpload) fileUpload.addEventListener("change", (e) => {
        if (e.target.files[0]) uploadFile(e.target.files[0]);
        fileUpload.value = '';
    });
    
    // إعدادات
    if (settingsBtn) {
        settingsBtn.addEventListener("click", () => {
            if (settingsPanel) settingsPanel.classList.toggle("hidden");
        });
    }
    if (closeSettingsBtn) {
        closeSettingsBtn.addEventListener("click", () => {
            if (settingsPanel) settingsPanel.classList.add("hidden");
        });
    }
    if (defaultModelSelect) {
        defaultModelSelect.value = selectedModel;
        defaultModelSelect.addEventListener("change", (e) => setModel(e.target.value));
    }
    
    // استعادة الرسائل
    restoreMessages();
    setModel(selectedModel);
    if (inputEl) inputEl.focus();
});
