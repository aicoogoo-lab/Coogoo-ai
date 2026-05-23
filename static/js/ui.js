// ============================================================
// SkyOS v10 - Sovereign Liquid Holographic UI Controller
// الجبارة • التاج في المشروع • GodMode + Ultra + فخم
// النسخة النهائية المطلقة - لا تعديل عليها مستقبلاً
// ============================================================

// --------------------------------------------
// تهيئة النظام عند تحميل الصفحة
// --------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    console.log(
        "%c[SkyOS v10] ⚡ Sovereign Holographic UI Initialized • GodMode Active • Ultra Mode Engaged",
        "color:#00E5FF; font-weight:bold; font-size:14px; background:#000; padding:4px 12px; border-radius:20px;"
    );

    initCommandCenter();
    initAICorePulse();
    initQuickChips();
    initAutoScroll();
    initEnergyMatrixUpdater();
    initGodModeToggle();
    initUltraMode();
    initSystemNotifications();
    loadSovereignPreferences();
    initVoiceRecognitionSupport();
});

// --------------------------------------------
// متغيرات الحالة السيادية
// --------------------------------------------
let godModeActive = true;
let ultraModeActive = true;
let currentCognitiveState = "Hyper Analysis";
let currentNeuralLoad = 62;
let currentSecurityLevel = "Zero-Trust Active";
let energyUpdateInterval = null;
let activityLogs = [];

// --------------------------------------------
// مركز الأوامر - مع دعم GodMode
// --------------------------------------------
function initCommandCenter() {
    const input = document.getElementById("commandInput");
    if (!input) {
        console.warn("[SkyOS] commandInput not found");
        return;
    }

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendCommand();
        }
    });
}

// إرسال الأمر مع تحليل سياقي متقدم
function sendCommand() {
    const input = document.getElementById("commandInput");
    if (!input) return;

    const command = input.value.trim();
    if (!command) {
        showSystemNotification("⚠️ يرجى كتابة أمر سيادي أولاً.", "warning");
        return;
    }

    displayUserMessage(command);
    input.value = "";

    animateAICoreThinking();
    updateCognitiveState("Executing Command");
    updateNeuralLoad(currentNeuralLoad + 5); // زيادة مؤقتة

    // محاكاة زمن المعالجة حسب تعقيد الأمر و GodMode
    const processingTime = godModeActive ? (command.length > 50 ? 600 : 400) : (command.length > 50 ? 1200 : 800);
    setTimeout(() => {
        const response = generateAIResponse(command);
        displayAIResponse(response);
        animateAICoreIdle();
        updateCognitiveState(currentCognitiveState);
        logActivity(command, response);
        updateNeuralLoad(currentNeuralLoad - 5);
        if (godModeActive) {
            showSystemNotification("🧠 تم تنفيذ الأمر باستخدام GodMode • سرعة فائقة", "success");
        }
    }, processingTime);
}

// --------------------------------------------
// توليد الرد السيادي بذكاء وتفوق
// --------------------------------------------
function generateAIResponse(command) {
    const lower = command.toLowerCase();
    
    // قاعدة ذكية للكلمات المفتاحية
    if (lower.includes("ذاكرة") || lower.includes("memory") || lower.includes("هولوغرافية")) {
        return `
            <span class="response-icon">🧠</span> <strong>تحليل الذاكرة الهولوغرافية:</strong><br>
            • مستوى التماسك: <span style="color:#00E5FF">94.7%</span> (مستقر)<br>
            • الروابط الكمية النشطة: <span style="color:#00E5FF">12,438</span><br>
            • العقد الهولوغرافية: <span style="color:#00E5FF">847,291</span><br>
            • حالة التخزين: <span style="color:#22c55e">مستقرة وآمنة</span>
        `;
    }
    else if (lower.includes("حالة") || lower.includes("status") || lower.includes("النظام")) {
        return `
            <span class="response-icon">📊</span> <strong>حالة النظام السيادي:</strong><br>
            • Core Engine: <span style="color:#22c55e">Operational</span><br>
            • Quantum Memory: <span style="color:#22c55e">Stable</span><br>
            • Self-Evolution: <span style="color:#fbbf24">Active</span><br>
            • Neural Load: <span style="color:#00E5FF">${currentNeuralLoad}%</span><br>
            • Security: ${currentSecurityLevel}<br>
            • GodMode: ${godModeActive ? "<span style='color:#00E5FF'>✅ مفعل</span>" : "❌ غير مفعل"}
        `;
    }
    else if (lower.includes("أمان") || lower.includes("security") || lower.includes("حماية")) {
        return `
            <span class="response-icon">🛡️</span> <strong>مركز الأمان السيادي:</strong><br>
            • لا توجد تهديدات حالية.<br>
            • جدار الحماية الصفري: نشط.<br>
            • جميع الصلاحيات ضمن النطاق المسموح.<br>
            • آخر فحص: قبل 12 ثانية.
        `;
    }
    else if (lower.includes("تحليل") || lower.includes("analysis") || lower.includes("تقرير")) {
        return `
            <span class="response-icon">📈</span> <strong>محرك التحليل السيادي:</strong><br>
            • تحليل سياقي متعدد الطبقات: مكتمل.<br>
            • استخراج النقاط الحرجة: <span style="color:#00E5FF">تم</span><br>
            • إنشاء تقرير تنفيذي فوري.<br>
            • تصنيف المخاطر: منخفض (95% ثقة).
        `;
    }
    else if (lower.includes("أتمتة") || lower.includes("automation") || lower.includes("عصبية")) {
        return `
            <span class="response-icon">⚙️</span> <strong>الأتمتة العصبية:</strong><br>
            • تم تفعيل 3 سيناريوهات آلية.<br>
            • مراقبة الأحداث مستمرة.<br>
            • آخر إجراء تلقائي: مزامنة الذاكرة قبل 2 دقيقة.
        `;
    }
    else if (lower.includes("قدرة") || lower.includes("godmode") || lower.includes("god")) {
        if (!godModeActive) {
            activateGodMode();
            return `<span class="response-icon">👑</span> <strong>تم تفعيل GodMode</strong><br>جميع القدرات السيادية متاحة الآن.`;
        }
        return `<span class="response-icon">👑</span> <strong>وضع GodMode مفعل بالفعل.</strong><br>• التحليل العميق: نشط.<br>• رؤية النظام الكاملة: ممنوحة.`;
    }
    else {
        return `
            <span class="response-icon">✨</span> <strong>تم استلام الأمر السيادي:</strong><br>
            "${command.substring(0, 100)}"<br><br>
            جاري معالجته بواسطة المحرك السيادي. استخدم أوامر مثل:<br>
            • تحليل الذاكرة<br>
            • حالة النظام<br>
            • تقرير أمني<br>
            • تفعيل الأتمتة العصبية
        `;
    }
}

// --------------------------------------------
// عرض رسائل المستخدم والردود في الواجهة
// --------------------------------------------
function displayUserMessage(command) {
    const container = document.querySelector(".main-container");
    if (!container) return;

    const messageDiv = document.createElement("div");
    messageDiv.className = "glass-card user-message";
    messageDiv.style.borderRight = "4px solid #00E5FF";
    messageDiv.style.marginTop = "20px";
    messageDiv.style.animation = "fadeInUp 0.3s ease";

    messageDiv.innerHTML = `
        <div class="msg-header" style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <i class="fas fa-user-shield" style="color:#00E5FF; font-size:1.2rem;"></i>
            <strong style="color:#00E5FF;">Sovereign Master</strong>
        </div>
        <p class="msg-text" style="font-size:0.9rem; line-height:1.5;">${escapeHtml(command)}</p>
    `;

    container.appendChild(messageDiv);
    messageDiv.scrollIntoView({ behavior: "smooth", block: "center" });
}

function displayAIResponse(responseHtml) {
    const container = document.querySelector(".main-container");
    if (!container) return;

    const messageDiv = document.createElement("div");
    messageDiv.className = "glass-card ai-message";
    messageDiv.style.borderRight = "4px solid #7C3AED";
    messageDiv.style.marginTop = "14px";
    messageDiv.style.animation = "fadeInUp 0.3s ease";

    messageDiv.innerHTML = `
        <div class="msg-header" style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <i class="fas fa-robot" style="color:#7C3AED; font-size:1.2rem;"></i>
            <strong style="color:#7C3AED;">SkyOS Core</strong>
        </div>
        <div class="msg-text" style="font-size:0.9rem; line-height:1.6;">${responseHtml}</div>
    `;

    container.appendChild(messageDiv);
    messageDiv.scrollIntoView({ behavior: "smooth", block: "center" });
}

function escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
        if (m === "&") return "&amp;";
        if (m === "<") return "&lt;";
        if (m === ">") return "&gt;";
        return m;
    });
}

// --------------------------------------------
// تحديث حالة العقل السيادي وعناصر الواجهة
// --------------------------------------------
function updateCognitiveState(state) {
    currentCognitiveState = state;
    const stateElement = document.querySelector(".ai-state-item:first-child .ai-state-value");
    if (stateElement) stateElement.innerText = state;
}

function updateNeuralLoad(load) {
    currentNeuralLoad = Math.min(100, Math.max(0, load));
    const loadElement = document.querySelector(".ai-state-item:nth-child(3) .ai-state-value");
    if (loadElement) loadElement.innerText = `${currentNeuralLoad}%`;
    
    // تحديث شريط الطاقة
    const fillBar = document.querySelector(".energy-matrix-grid .metric-fill.mid");
    if (fillBar) fillBar.style.width = `${currentNeuralLoad}%`;
    
    const energyFill = document.querySelector(".energy-fill");
    if (energyFill) energyFill.style.width = `${currentNeuralLoad}%`;
}

function updateSecurityStatus(status) {
    currentSecurityLevel = status;
    const secElement = document.querySelector(".ai-state-item:last-child .ai-state-value");
    if (secElement) secElement.innerText = status;
}

// --------------------------------------------
// تحديث مصفوفة الطاقة ديناميكيًا
// --------------------------------------------
function initEnergyMatrixUpdater() {
    if (energyUpdateInterval) clearInterval(energyUpdateInterval);
    energyUpdateInterval = setInterval(() => {
        let newLoad = currentNeuralLoad + (Math.random() * 6 - 3);
        newLoad = Math.min(95, Math.max(45, newLoad));
        updateNeuralLoad(Math.round(newLoad));
    }, 8000);
}

// --------------------------------------------
// تحريك العقل السيادي
// --------------------------------------------
function initAICorePulse() {
    const core = document.querySelector(".ai-core-node");
    if (!core) return;

    setInterval(() => {
        if (godModeActive) {
            core.classList.add("pulse-animate");
            setTimeout(() => core.classList.remove("pulse-animate"), 1200);
        }
    }, 2600);
}

function animateAICoreThinking() {
    const core = document.querySelector(".ai-core-node");
    if (!core) return;
    core.style.transition = "all 0.2s ease";
    core.style.boxShadow = "0 0 45px rgba(0,229,255,1), 0 0 90px rgba(124,58,237,1)";
    core.style.transform = "scale(1.15)";
}

function animateAICoreIdle() {
    const core = document.querySelector(".ai-core-node");
    if (!core) return;
    core.style.boxShadow = "0 0 24px rgba(0,229,255,0.7), 0 0 50px rgba(124,58,237,0.6)";
    core.style.transform = "scale(1)";
}

// --------------------------------------------
// تفعيل GodMode و Ultra Mode
// --------------------------------------------
function initGodModeToggle() {
    const godButton = document.querySelector(".quick-action-btn i.fa-microchip")?.parentElement;
    if (godButton) {
        godButton.addEventListener("click", () => {
            if (!godModeActive) activateGodMode();
            else showSystemNotification("وضع GodMode مفعل بالفعل.", "info");
        });
    }
    if (godModeActive) activateGodMode();
}

function activateGodMode() {
    godModeActive = true;
    showSystemNotification("👑 تم تفعيل وضع GodMode: تحليل عميق، أوامر متعددة، رؤية كاملة.", "success");
    document.body.classList.add("godmode-active");
    updateCognitiveState("GodMode Active");
    if (energyUpdateInterval) clearInterval(energyUpdateInterval);
    initEnergyMatrixUpdater();
    localStorage.setItem("skyos_godmode", "true");
}

function initUltraMode() {
    ultraModeActive = true;
    document.body.classList.add("ultra-active");
    const style = document.createElement("style");
    style.textContent = `
        .ultra-active .glass-card { transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1); }
        .ultra-active .glass-card:hover { transform: translateY(-4px); }
    `;
    document.head.appendChild(style);
    showSystemNotification("💎 تم تفعيل Ultra Mode: فخامة سينمائية وتأثيرات هولوغرافية متقدمة.", "success");
    localStorage.setItem("skyos_ultra", "true");
}

// --------------------------------------------
// الأوامر السريعة (Quick Chips)
// --------------------------------------------
function initQuickChips() {
    const chips = document.querySelectorAll(".quick-chip");
    chips.forEach((chip) => {
        chip.addEventListener("click", () => {
            const text = chip.innerText.trim();
            displayUserMessage(text);
            animateAICoreThinking();
            setTimeout(() => {
                const response = generateAIResponse(text);
                displayAIResponse(response);
                animateAICoreIdle();
            }, 600);
        });
    });
}

// --------------------------------------------
// التمرير التلقائي
// --------------------------------------------
function initAutoScroll() {
    const container = document.querySelector(".main-container");
    if (!container) return;
    const observer = new MutationObserver(() => {
        container.lastElementChild?.scrollIntoView({ behavior: "smooth" });
    });
    observer.observe(container, { childList: true });
}

// --------------------------------------------
// الأوامر الصوتية الحقيقية (Web Speech API)
// --------------------------------------------
let voiceRecognitionSupported = false;
function initVoiceRecognitionSupport() {
    voiceRecognitionSupported = !!(window.SpeechRecognition || window.webkitSpeechRecognition);
}

function toggleVoiceCommand() {
    if (!voiceRecognitionSupported) {
        showSystemNotification("المتصفح لا يدعم الأوامر الصوتية. استخدم Chrome أو Edge.", "error");
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = "ar-SA";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    showSystemNotification("🎤 استمع الآن... تحدث بأمرك السيادي.", "info");
    recognition.start();

    recognition.onresult = (event) => {
        const spokenCommand = event.results[0][0].transcript;
        showSystemNotification(`✅ تم التعرف على: "${spokenCommand}"`, "success");
        const input = document.getElementById("commandInput");
        if (input) input.value = spokenCommand;
        sendCommand();
    };
    recognition.onerror = () => {
        showSystemNotification("خطأ في التعرف على الصوت. حاول مرة أخرى.", "error");
    };
}

// --------------------------------------------
// قوالب الأوامر السيادية المتقدمة
// --------------------------------------------
function openCommandTemplates() {
    const templates = [
        "تحليل شامل للذاكرة الهولوغرافية",
        "تقرير حالة النظام الكامل",
        "تفعيل الحماية القصوى",
        "تشغيل الأتمتة العصبية للمهام الحرجة",
        "إنشاء تقرير سيادي تنفيذي",
        "مسح شامل للثغرات الأمنية",
        "إظهار سجل العمليات لآخر ساعة",
        "تفعيل وضع GodMode",
        "تحديث جميع النماذج المحلية"
    ];
    
    let message = "📋 قوالب الأوامر السيادية المتاحة:\n\n";
    templates.forEach((t, idx) => {
        message += `${idx+1}. ${t}\n`;
    });
    message += "\nأدخل رقم القالب أو اكتب الأمر المطلوب:";
    
    const choice = prompt(message);
    if (choice && !isNaN(choice) && choice >= 1 && choice <= templates.length) {
        const selected = templates[parseInt(choice)-1];
        const input = document.getElementById("commandInput");
        if (input) input.value = selected;
        sendCommand();
    } else if (choice && choice.trim()) {
        const input = document.getElementById("commandInput");
        if (input) input.value = choice;
        sendCommand();
    }
}

// --------------------------------------------
// تسجيل النشاط السيادي
// --------------------------------------------
function logActivity(command, response) {
    const logEntry = {
        timestamp: new Date().toISOString(),
        command: command.substring(0, 200),
        responsePreview: response.substring(0, 100)
    };
    activityLogs.unshift(logEntry);
    if (activityLogs.length > 50) activityLogs.pop();
    localStorage.setItem("skyos_activity_logs", JSON.stringify(activityLogs));
    console.log("[SkyOS Activity]", logEntry);
}

// --------------------------------------------
// تفضيلات المستخدم السيادي
// --------------------------------------------
function loadSovereignPreferences() {
    const savedGodMode = localStorage.getItem("skyos_godmode");
    if (savedGodMode === "false") {
        godModeActive = false;
        showSystemNotification("وضع GodMode معطل. يمكنك تفعيله من الأوامر.", "info");
    } else {
        godModeActive = true;
        activateGodMode();
    }
    
    const savedUltra = localStorage.getItem("skyos_ultra");
    if (savedUltra === "false") {
        ultraModeActive = false;
        document.body.classList.remove("ultra-active");
    } else {
        ultraModeActive = true;
        initUltraMode();
    }
}

// --------------------------------------------
// إشعارات النظام (Toast Notifications)
// --------------------------------------------
function initSystemNotifications() {
    const style = document.createElement("style");
    style.textContent = `
        .system-notification {
            position: fixed; bottom: 20px; right: 20px; z-index: 1000;
            background: rgba(0,0,0,0.85); backdrop-filter: blur(12px);
            border-right: 3px solid #00e5ff; padding: 12px 20px;
            border-radius: 12px; color: white; font-size: 0.85rem;
            animation: slideIn 0.3s ease; max-width: 320px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            font-family: 'Inter', sans-serif; direction: rtl;
        }
        .system-notification.success { border-right-color: #22c55e; }
        .system-notification.error { border-right-color: #ef4444; }
        .system-notification.warning { border-right-color: #fbbf24; }
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

function showSystemNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `system-notification ${type}`;
    notification.innerText = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = "fadeOut 0.3s ease";
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// --------------------------------------------
// وظائف إضافية للأزرار السريعة (Overclock, Stealth)
// --------------------------------------------
function activateOverclock() {
    if (!godModeActive) {
        showSystemNotification("⚠️ يجب تفعيل GodMode أولاً لاستخدام وضع Overclock.", "warning");
        return;
    }
    showSystemNotification("⚡ تفعيل وضع Overclock: سرعة المعالجة العصبية +200%، استهلاك الطاقة مرتفع.", "success");
    updateNeuralLoad(98);
    updateCognitiveState("Overclock Mode");
    animateAICoreThinking();
    setTimeout(() => {
        updateNeuralLoad(72);
        updateCognitiveState("Hyper Analysis");
        animateAICoreIdle();
        showSystemNotification("انتهى وضع Overclock. العودة إلى الوضع الطبيعي.", "info");
    }, 10000);
}

function activateStealth() {
    showSystemNotification("🕶️ تفعيل وضع Stealth: إخفاء البصمة الرقمية، تقليل الإشعاع الهولوغرافي.", "success");
    updateSecurityStatus("Stealth Active");
    const hologramCanvas = document.getElementById("hologram-canvas");
    if (hologramCanvas) hologramCanvas.style.opacity = "0.5";
    setTimeout(() => {
        if (hologramCanvas) hologramCanvas.style.opacity = "1";
        updateSecurityStatus("Zero-Trust Active");
        showSystemNotification("وضع Stealth تم إلغاؤه تلقائيًا.", "info");
    }, 8000);
}

// --------------------------------------------
// ربط الوظائف بالكائن العام لضمان التوافق مع onclick
// --------------------------------------------
window.sendCommand = sendCommand;
window.toggleVoiceCommand = toggleVoiceCommand;
window.openCommandTemplates = openCommandTemplates;
window.quickCommand = function(cmd) {
    displayUserMessage(cmd);
    animateAICoreThinking();
    setTimeout(() => {
        const response = generateAIResponse(cmd);
        displayAIResponse(response);
        animateAICoreIdle();
    }, 600);
};
window.activateOverclock = activateOverclock;
window.activateStealth = activateStealth;

// تهيئة إضافية لمراقبة أزرار لوحة التحكم
document.addEventListener("click", (e) => {
    const btn = e.target.closest(".btn-secondary");
    if (btn && btn.closest(".dashboard-card")) {
        const card = btn.closest(".dashboard-card");
        const title = card?.querySelector("h3")?.innerText || "الوحدة";
        showSystemNotification(`🔓 فتح ${title} - سيتم التوجيه في الإصدارات القادمة.`, "info");
    }
});

console.log("%c[SkyOS v10] ✅ Sovereign UI fully loaded. GodMode + Ultra active. Ready for commands.", "color:#7C3AED; font-weight:bold;");

// ============================================================
// نهاية الملف - التاج في المشروع
// ============================================================
