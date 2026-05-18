const chatWindow = document.getElementById("chatWindow");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const modelSelect = document.getElementById("modelSelect");
const settingsToggle = document.getElementById("settingsToggle");
const settingsPanel = document.getElementById("settingsPanel");
const closeSettings = document.getElementById("closeSettings");
const clearChatBtn = document.getElementById("clearChat");
const clearLocalBtn = document.getElementById("clearLocal");
const scrollDownBtn = document.getElementById("scrollDown");

const STORAGE_KEY = "samaa_chat_history_v1";

// تحميل المحادثة من التخزين المحلي
function loadChatFromStorage() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;
    try {
        const messages = JSON.parse(saved);
        messages.forEach(msg => {
            addMessage(msg.text, msg.sender, false);
        });
        scrollToBottom();
    } catch (e) {
        console.error("خطأ في قراءة المحادثة من التخزين:", e);
    }
}

// حفظ المحادثة في التخزين المحلي
function saveChatToStorage() {
    const bubbles = chatWindow.querySelectorAll(".message-bubble");
    const data = [];
    bubbles.forEach(bubble => {
        const sender = bubble.dataset.sender || "assistant";
        const text = bubble.querySelector(".text")?.innerText || bubble.innerText;
        data.push({ sender, text });
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

// إضافة رسالة للواجهة
function addMessage(text, sender = "assistant", save = true) {
    const row = document.createElement("div");
    row.classList.add("message-row", sender);

    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");
    bubble.dataset.sender = sender;

    const span = document.createElement("div");
    span.classList.add("text");
    span.innerText = text;

    bubble.appendChild(span);

    if (sender === "assistant") {
        const copyBtn = document.createElement("button");
        copyBtn.classList.add("copy-btn");
        copyBtn.innerText = "نسخ";
        copyBtn.addEventListener("click", () => {
            navigator.clipboard.writeText(text).then(() => {
                copyBtn.innerText = "✓";
                setTimeout(() => (copyBtn.innerText = "نسخ"), 1000);
            });
        });
        bubble.appendChild(copyBtn);
    }

    row.appendChild(bubble);
    chatWindow.appendChild(row);

    if (save) saveChatToStorage();
    scrollToBottom();
}

// تمرير لأسفل
function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// إظهار/إخفاء زر النزول
chatWindow.addEventListener("scroll", () => {
    const nearBottom =
        chatWindow.scrollHeight - chatWindow.scrollTop - chatWindow.clientHeight < 80;
    if (nearBottom) {
        scrollDownBtn.classList.add("hidden");
    } else {
        scrollDownBtn.classList.remove("hidden");
    }
});

scrollDownBtn.addEventListener("click", scrollToBottom);

// إرسال الرسالة
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    const model = modelSelect.value || "groq";

    addMessage(text, "user");
    userInput.value = "";
    userInput.style.height = "auto";

    const thinkingId = "thinking-" + Date.now();
    addMessage("… سماء تفكر في رد مناسب لك", "assistant");
    const thinkingBubble = chatWindow.querySelector(
        `.message-bubble:last-child .text`
    );
    thinkingBubble.dataset.thinkingId = thinkingId;

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text, model })
        });

        const data = await res.json();
        const reply = data.reply || "لم يصل رد من سماء.";

        // إزالة رسالة التفكير الأخيرة
        const lastRow = chatWindow.querySelector(".message-row.assistant:last-child");
        if (lastRow) lastRow.remove();

        addMessage(reply, "assistant");
    } catch (e) {
        const lastRow = chatWindow.querySelector(".message-row.assistant:last-child");
        if (lastRow) lastRow.remove();

        addMessage("حدث خطأ أثناء الاتصال بسماء. حاول مرة أخرى.", "assistant");
    }
}

// تكبير/تصغير حقل الإدخال تلقائيًا
userInput.addEventListener("input", () => {
    userInput.style.height = "auto";
    userInput.style.height = userInput.scrollHeight + "px";
});

// إرسال بالزر
sendBtn.addEventListener("click", sendMessage);

// إرسال بزر Enter (مع Shift للسطر الجديد)
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// فتح/إغلاق الإعدادات
settingsToggle.addEventListener("click", () => {
    settingsPanel.classList.toggle("hidden");
});

closeSettings.addEventListener("click", () => {
    settingsPanel.classList.add("hidden");
});

// مسح المحادثة من الباك إند + التخزين
clearChatBtn.addEventListener("click", async () => {
    if (!confirm("هل أنت متأكد من مسح المحادثة بالكامل؟")) return;

    try {
        await fetch("/clear", { method: "POST" });
    } catch (e) {
        console.warn("تعذر الاتصال بالخادم لمسح الذاكرة، سيتم المسح محليًا فقط.");
    }

    chatWindow.innerHTML = "";
    localStorage.removeItem(STORAGE_KEY);
});

// تنظيف الشاشة فقط (بدون لمس ذاكرة الباك إند)
clearLocalBtn.addEventListener("click", () => {
    chatWindow.innerHTML = "";
    localStorage.removeItem(STORAGE_KEY);
});

// تحميل المحادثة عند فتح الصفحة
window.addEventListener("load", () => {
    loadChatFromStorage();
});
