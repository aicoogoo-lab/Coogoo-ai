const messagesEl = document.getElementById("messages");
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
const toneSelect = document.getElementById("tone-select");

let selectedModel = "groq";

function setModel(model) {
  selectedModel = model;
  groqBtn.classList.toggle("active", model === "groq");
  geminiBtn.classList.toggle("active", model === "gemini");
}

groqBtn.addEventListener("click", () => setModel("groq"));
geminiBtn.addEventListener("click", () => setModel("gemini"));

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;
  addMessage(text, "user");
  inputEl.value = "";
  typingEl.classList.remove("hidden");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, ai_type: selectedModel })
    });
    const data = await res.json();
    typingEl.classList.add("hidden");
    addMessage(data.reply || "لم يصل رد.", "assistant");
  } catch (e) {
    typingEl.classList.add("hidden");
    addMessage("حدث خطأ في الاتصال.", "assistant");
  }
}

sendBtn.addEventListener("click", sendMessage);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

// مسح المحادثة
clearBtn.addEventListener("click", async () => {
  messagesEl.innerHTML = "";
  try {
    await fetch("/clear", { method: "POST" });
  } catch (e) { /* نتجاهل */ }
});

// الإعدادات
settingsBtn.addEventListener("click", () => settingsPanel.classList.remove("hidden"));
closeSettingsBtn.addEventListener("click", () => settingsPanel.classList.add("hidden"));
defaultModelSelect.addEventListener("change", (e) => setModel(e.target.value));
toneSelect.addEventListener("change", () => {
  // مستقبلاً سيُربط بتعديل الشخصية
});
