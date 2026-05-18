const messagesEl = document.getElementById("messages");
const typingEl = document.getElementById("typing");
const inputEl = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const groqBtn = document.getElementById("groq-btn");
const geminiBtn = document.getElementById("gemini-btn");

let selectedModel = "groq";

function setModel(model) {
  selectedModel = model;
  if (model === "groq") {
    groqBtn.classList.add("active");
    geminiBtn.classList.remove("active");
  } else {
    geminiBtn.classList.add("active");
    groqBtn.classList.remove("active");
  }
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
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: text,
        ai_type: selectedModel,
      }),
    });

    const data = await res.json();
    typingEl.classList.add("hidden");
    addMessage(data.reply || "لم يصل رد من المساعد.", "assistant");
  } catch (e) {
    typingEl.classList.add("hidden");
    addMessage("حدث خطأ في الاتصال بالخادم.", "assistant");
  }
}

sendBtn.addEventListener("click", sendMessage);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
