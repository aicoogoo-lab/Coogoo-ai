// ============================================================
// SkyOS v10 - Sovereign Liquid Holographic UI Controller (الكامل النهائي)
// GodMode + Ultra + فخم | Sovereign Edition
// تم التطوير وفق رؤية العقل السيادي
// ============================================================

// --------------------------------------------
// تهيئة النظام عند تحميل الصفحة
// --------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    console.log('%c[SkyOS v10] Sovereign UI Initialized | GodMode Ready', 'color:#00E5FF; font-weight:bold; font-size:14px;');
    initCommandCenter();
    initAICorePulse();
    initQuickChips();
    initAutoScroll();
    initEnergyMatrixUpdater();
    initGodModeToggle();
    initUltraMode();
    initSystemListeners();
    loadSovereignPreferences();
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

// --------------------------------------------
// مركز الأوامر - تحسين الإدخال
// --------------------------------------------
function initCommandCenter() {
    const input = document.getElementById('commandInput');
    if (!input) {
        console.warn('[SkyOS] commandInput not found');
        return;
    }

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendCommand();
        }
    });
}

// إرسال الأمر مع تحليل سياقي
function sendCommand() {
    const input = document.getElementById('commandInput');
    if (!input) return;

    const command = input.value.trim();
    if (!command) {
        showSystemNotification('⚠️ يرجى كتابة أمر سيادي أولاً.', 'warning');
        return;
    }

    displayUserMessage(command);
    input.value = '';

    animateAICoreThinking();
    updateCognitiveState('Executing Command');

    // محاكاة زمن المعالجة حسب تعقيد الأمر
    const processingTime = command.length > 50 ? 1500 : 800;
    setTimeout(() => {
        const response = generateAIResponse(command);
        displayAIResponse(response);
        animateAICoreIdle();
        updateCognitiveState(currentCognitiveState); // العودة للحالة السابقة
        logActivity(command, response);
    }, processingTime);
}

// --------------------------------------------
// توليد الرد السيادي بذكاء
// --------------------------------------------
function generateAIResponse(command) {
    const lower = command.toLowerCase();
    
    // تحليل الكلمات المفتاحية
    if (lower.includes('ذاكرة') || lower.includes('memory') || lower.includes('هولوغرافية')) {
        return `
            <span class="response-icon">🧠</span> <strong>تحليل الذاكرة الهولوغرافية:</strong><br>
            • مستوى التماسك: <span style="color:#00E5FF">94.7%</span> (مستقر)<br>
            • الروابط الكمية النشطة: <span style="color:#00E5FF">12,438</span><br>
            • العقد الهولوغرافية: <span style="color:#00E5FF">847,291</span><br>
            • حالة التخزين: <span style="color:#22c55e">مستقرة وآمنة</span>
        `;
    }
    else if (lower.includes('حالة') || lower.includes('status') || lower.includes('النظام')) {
        return `
            <span class="response-icon">📊</span> <strong>حالة النظام السيادي:</strong><br>
            • Core Engine: <span style="color:#22c55e">Operational</span><br>
            • Quantum Memory: <span style="color:#22c55e">Stable</span><br>
            • Self-Evolution: <span style="color:#fbbf24">Active</span><br>
            • Neural Load: <span style="color:#00E5FF">${currentNeuralLoad}%</span><br>
            • Security: ${currentSecurityLevel}
        `;
    }
    else if (lower.includes('أمان') || lower.includes('security') || lower.includes('حماية')) {
        return `
            <span class="response-icon">🛡️</span> <strong>مركز الأمان السيادي:</strong><br>
            • لا توجد تهديدات حالية.<br>
            • جدار الحماية الصفري: نشط.<br>
      • جميع الصلاحيات ضمن النطاق المسموح.<br>
            • آخر فحص: قبل 12 ثانية.
        `;
    }
    else if (lower.includes('تحليل') || lower.includes('analysis') || lower.includes('تقرير')) {
        return `
            <span class="response-icon">📈</span> <strong>محرك التحليل السيادي:</strong><br>
            • تحليل سياقي متعدد الطبقات: مكتمل.<br>
            • استخراج النقاط الحرجة: <span style="color:#00E5FF">تم</span><br>
            • إنشاء تقرير تنفيذي فوري.<br>
            • تصنيف المخاطر: منخفض (95% ثقة).
        `;
    }
    else if (lower.includes('أتمتة') || lower.includes('automation') || lower.includes('عصبية')) {
        return `
            <span class="response-icon">⚙️</span> <strong>الأتمتة العصبية:</strong><br>
            • تم تفعيل 3 سيناريوهات آلية.<br>
            • مراقبة الأحداث مستمرة.<br>
            • آخر إجراء تلقائي: مزامنة الذاكرة قبل 2 دقيقة.
        `;
    }
    else if (lower.includes('قدرة') || lower.includes('godmode') || lower.includes('god')) {
        return `
            <span class="response-icon">👑</span> <strong>وضع GodMode مفعل بالفعل.</strong><br>
            • جميع القدرات السيادية متاحة.<br>
            • التحليل العميق: نشط.<br>
            • رؤية النظام الكاملة: ممنوحة.<br>
            • يمكنك استخدام أوامر مثل "تحليل شامل"، "تقرير سيادي".
        `;
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
    const container = document.querySelector('.main-container');
    if (!container) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'glass-card user-message';
    messageDiv.style.borderRight = '4px solid #00E5FF';
    messageDiv.style.marginTop = '20px';
    messageDiv.style.animation = 'fadeInUp 0.3s ease';

    messageDiv.innerHTML = `
        <div class="msg-header" style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <i class="fas fa-user-shield" style="color:#00E5FF; font-size:1.2rem;"></i>
            <strong style="color:#00E5FF;">Sovereign Master</strong>
        </div>
        <p class="msg-text" style="font-size:0.9rem; line-height:1.5;">${escapeHtml(command)}</p>
    `;

    container.appendChild(messageDiv);
    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function displayAIResponse(responseHtml) {
    const container = document.querySelector('.main-container');
    if (!container) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'glass-card ai-message';
    messageDiv.style.borderRight = '4px solid #7C3AED';
    messageDiv.style.marginTop = '14px';
    messageDiv.style.animation = 'fadeInUp 0.3s ease';

    messageDiv.innerHTML = `
        <div class="msg-header" style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <i class="fas fa-robot" style="color:#7C3AED; font-size:1.2rem;"></i>
            <strong style="color:#7C3AED;">SkyOS Core</strong>
        </div>
        <div class="msg-text" style="font-size:0.9rem; line-height:1.6;">${responseHtml}</div>
    `;

    container.appendChild(messageDiv);
    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// أداة لمنع حقن HTML ضار
function escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    }).replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, function(c) {
        return c;
    });
}

// --------------------------------------------
// تحديث حالة العقل السيادي وعناصر الواجهة
// --------------------------------------------
function updateCognitiveState(state) {
    currentCognitiveState = state;
    const stateElement = document.querySelector('.ai-state-item:first-child .ai-state-value');
    if (stateElement) stateElement.innerText = state;
}

function updateNeuralLoad(load) {
    currentNeuralLoad = Math.min(100, Math.max(0, load));
    const loadElement = document.querySelector('.ai-state-item:nth-child(3) .ai-state-value');
    if (loadElement) loadElement.innerText = `${currentNeuralLoad}%`;
    
    // تحديث شريط الطاقة
    const fillBar = document.querySelector('.energy-matrix-grid .metric-fill.mid');
    if (fillBar) fillBar.style.width = `${currentNeuralLoad}%`;
}

function updateSecurityStatus(status) {
    currentSecurityLevel = status;
    const secElement = document.querySelector('.ai-state-item:last-child .ai-state-value');
    if (secElement) secElement.innerText = status;
}

// --------------------------------------------
// تحديث مصفوفة الطاقة ديناميكيًا (محاكاة حيوية)
// --------------------------------------------
function initEnergyMatrixUpdater() {
    if (energyUpdateInterval) clearInterval(energyUpdateInterval);
    energyUpdateInterval = setInterval(() => {
        // تغيير طفيف في الحمل العصبي لإحساس الحياة
        let newLoad = currentNeuralLoad + (Math.random() * 4 - 2);
        newLoad = Math.min(95, Math.max(45, newLoad));
        updateNeuralLoad(Math.round(newLoad));
        
        // تحديث مؤشرات الطاقة المصغرة في الهيدر
        const energyFill = document.querySelector('.energy-fill');
        if (energyFill) {
            const widthPercent = currentNeuralLoad;
            energyFill.style.width = `${widthPercent}%`;
        }
    }, 8000);
}

// --------------------------------------------
// Animations AI Core (GodMode Enhancements)
// --------------------------------------------
function initAICorePulse() {
    const core = document.querySelector('.ai-core-node');
    if (!core) return;

    setInterval(() => {
        if (godModeActive) {
            core.classList.add('pulse-animate');
            setTimeout(() => core.classList.remove('pulse-animate'), 1200);
        }
    }, 2600);
}

function animateAICoreThinking() {
    const core = document.querySelector('.ai-core-node');
    if (!core) return;
    core.style.transition = 'all 0.2s ease';
    core.style.boxShadow = '0 0 45px rgba(0,229,255,1), 0 0 90px rgba(124,58,237,1)';
    core.style.transform = 'scale(1.15)';
}

function animateAICoreIdle() {
    const core = document.querySelector('.ai-core-node');
    if (!core) return;
    core.style.boxShadow = '0 0 24px rgba(0,229,255,0.7), 0 0 50px rgba(124,58,237,0.6)';
    core.style.transform = 'scale(1)';
}

// --------------------------------------------
// تفعيل GodMode و Ultra Mode
// --------------------------------------------
function initGodModeToggle() {
    // البحث عن أزرار أو إعدادات GodMode في الواجهة (مثال: زر في شريط الإجراءات السريعة)
    // نفترض وجود زر "وضع Overclock" أو "GodMode" لكننا سنضيف وظيفة عامة
    const godButton = document.querySelector('.quick-action-btn i.fa-microchip')?.parentElement;
    if (godButton) {
        godButton.addEventListener('click', () => {
            if (!godModeActive) {
                activateGodMode();
            } else {
                showSystemNotification('وضع GodMode مفعل بالفعل.', 'info');
            }
        });
    }
    
    // تفعيل GodMode افتراضيًا
    activateGodMode();
}

function activateGodMode() {
    godModeActive = true;
    showSystemNotification('👑 تم تفعيل وضع GodMode: تحليل عميق، أوامر متعددة، رؤية كاملة.', 'success');
    document.body.classList.add('godmode-active');
    updateCognitiveState('GodMode Active');
    // زيادة سرعة الاستجابة
    if (energyUpdateInterval) clearInterval(energyUpdateInterval);
    initEnergyMatrixUpdater(); // إعادة تشغيل محدث الطاقة
}

function initUltraMode() {
    // Ultra Mode يضيف فخامة إضافية (تأثيرات بصرية، صوتيات خفيفة)
    ultraModeActive = true;
    document.body.classList.add('ultra-active');
    // إضافة تأثيرات بصرية إضافية (مثلاً وميض ناعم للزجاج)
    const style = document.createElement('style');
    style.textContent = `
        .ultra-active .glass-card {
            transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
        }
        .ultra-active .glass-card:hover {
            transform: translateY(-2px);
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
    showSystemNotification('💎 تم تفعيل Ultra Mode: فخامة سينمائية وتأثيرات هولوغرافية متقدمة.', 'success');
}

// --------------------------------------------
// وظائف شريط الإجراءات السريعة
// --------------------------------------------
function initQuickChips() {
    const chips = document.querySelectorAll('.quick-chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
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
// التمرير التلقائي للرسائل الجديدة
// --------------------------------------------
function initAutoScroll() {
    const container = document.querySelector('.main-container');
    if (!container) return;

    const observer = new MutationObserver(() => {
        const lastMsg = container.lastElementChild;
        if (lastMsg) lastMsg.scrollIntoView({ behavior: 'smooth', block: 'end' });
    });
    observer.observe(container, { childList: true });
}

// --------------------------------------------
// أوامر الصوت (Web Speech API)
// --------------------------------------------
function toggleVoiceCommand() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showSystemNotification('المتصفح لا يدعم الأوامر الصوتية.', 'error');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'ar-SA';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    
    showSystemNotification('🎤 استمع الآن... تحدث بأمرك السيادي.', 'info');
    
    recognition.start();
    
    recognition.onresult = (event) => {
        const spokenCommand = event.results[0][0].transcript;
        showSystemNotification(`✅ تم التعرف على: "${spokenCommand}"`, 'success');
        const input = document.getElementById('commandInput');
        if (input) input.value = spokenCommand;
        sendCommand();
    };
    
    recognition.onerror = (event) => {
        showSystemNotification('خطأ في التعرف على الصوت. حاول مرة أخرى.', 'error');
    };
}

// --------------------------------------------
// قوالب الأوامر السيادية
// --------------------------------------------
function openCommandTemplates() {
    const templates = [
        "تحليل شامل للذاكرة الهولوغرافية",
        "تقرير حالة النظام الكامل",
        "تفعيل الحماية القصوى",
        "تشغيل الأتمتة العصبية للمهام الحرجة",
        "إنشاء تقرير سيادي تنفيذي",
        "مسح شامل للثغرات الأمنية",
        "إظهار سجل العمليات لآخر ساعة"
    ];
    
    let message = "📋 قوالب الأوامر السيادية المتاحة:\n\n";
    templates.forEach((t, idx) => {
        message += `${idx+1}. ${t}\n`;
    });
    message += "\nاضغط موافق لنسخ قالب، أو انسخ يدويًا.";
    
    const choice = prompt(message);
    if (choice && !isNaN(choice) && choice >= 1 && choice <= templates.length) {
        const selected = templates[parseInt(choice)-1];
        const input = document.getElementById('commandInput');
        if (input) input.value = selected;
        sendCommand();
    } else if (choice && choice.trim()) {
        // إذا أدخل نصًا غير رقمي، نعتبره أمرًا مباشرًا
        const input = document.getElementById('commandInput');
        if (input) input.value = choice;
        sendCommand();
    }
}

// --------------------------------------------
// تسجيل النشاط (محاكاة)
// --------------------------------------------
function logActivity(command, response) {
    const logEntry = {
        timestamp: new Date().toISOString(),
        command: command.substring(0, 200),
        responsePreview: response.substring(0, 100)
    };
    console.log('[SkyOS Activity]', logEntry);
    // يمكن تخزينها في localStorage أو إرسالها للخادم لاحقًا
    let logs = JSON.parse(localStorage.getItem('skyos_activity_logs') || '[]');
    logs.unshift(logEntry);
    if (logs.length > 50) logs.pop();
    localStorage.setItem('skyos_activity_logs', JSON.stringify(logs));
}

// --------------------------------------------
// تفضيلات المستخدم السيادي
// --------------------------------------------
function loadSovereignPreferences() {
    const savedGodMode = localStorage.getItem('skyos_godmode');
    if (savedGodMode === 'false') {
        godModeActive = false;
        showSystemNotification('وضع GodMode معطل. يمكنك تفعيله من الإعدادات.', 'info');
    } else {
        activateGodMode();
    }
    
    const savedUltra = localStorage.getItem('skyos_ultra');
    if (savedUltra === 'false') {
        ultraModeActive = false;
        document.body.classList.remove('ultra-active');
    } else {
        initUltraMode();
    }
}

function saveSovereignPreferences() {
    localStorage.setItem('skyos_godmode', godModeActive);
    localStorage.setItem('skyos_ultra', ultraModeActive);
}

// --------------------------------------------
// إظهار إشعارات النظام داخل الواجهة (Toasts)
// --------------------------------------------
function showSystemNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `system-notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(0,0,0,0.85);
        backdrop-filter: blur(12px);
        border-right: 3px solid ${type === 'success' ? '#22c55e' : (type === 'error' ? '#ef4444' : '#00e5ff')};
        padding: 12px 20px;
        border-radius: 12px;
        color: white;
        font-size: 0.85rem;
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 300px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    `;
    notification.innerText = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// إضافة أنماط للإشعارات إذا لم تكن موجودة
const styleNotify = document.createElement('style');
styleNotify.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    .system-notification {
        font-family: 'Inter', sans-serif;
        direction: rtl;
    }
`;
document.head.appendChild(styleNotify);

// --------------------------------------------
// وظائف إضافية للأزرار السريعة في واجهة المستخدم (Overclock, Stealth)
// --------------------------------------------
function activateOverclock() {
    if (!godModeActive) {
        showSystemNotification('⚠️ يجب تفعيل GodMode أولاً لاستخدام وضع Overclock.', 'warning');
        return;
    }
    showSystemNotification('⚡ تفعيل وضع Overclock: سرعة المعالجة العصبية +200%، استهلاك الطاقة مرتفع.', 'success');
    updateNeuralLoad(98);
    updateCognitiveState('Overclock Mode');
    animateAICoreThinking();
    setTimeout(() => {
        updateNeuralLoad(72);
        updateCognitiveState('Hyper Analysis');
        animateAICoreIdle();
        showSystemNotification('انتهى وضع Overclock. العودة إلى الوضع الطبيعي.', 'info');
    }, 10000);
}

function activateStealth() {
    showSystemNotification('🕶️ تفعيل وضع Stealth: إخفاء البصمة الرقمية، تقليل الإشعاع الهولوغرافي.', 'success');
    updateSecurityStatus('Stealth Active');
    // تأثير بصري: خفض شفافية الهولوغرام؟
    const hologramCanvas = document.getElementById('hologram-canvas');
    if (hologramCanvas) hologramCanvas.style.opacity = '0.5';
    setTimeout(() => {
        if (hologramCanvas) hologramCanvas.style.opacity = '1';
        updateSecurityStatus('Zero-Trust Active');
        showSystemNotification('وضع Stealth تم إلغاؤه تلقائيًا.', 'info');
    }, 8000);
}

// ربط الوظائف بالكائن العام لضمان توفرها من onclick في HTML
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

// تهيئة إضافية لمراقبة حالة النظام
function initSystemListeners() {
    // يمكن إضافة مستمعين للأزرار الموجودة في لوحة التحكم (مثل "فتح محرك التحليل")
    const btns = document.querySelectorAll('.btn-secondary');
    btns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const parentCard = btn.closest('.dashboard-card');
            const title = parentCard?.querySelector('h3')?.innerText || 'الوحدة';
            showSystemNotification(`🔓 فتح ${title} - سيتم التوجيه قريبًا في الإصدارات القادمة.`, 'info');
        });
    });
}

// التأكد من أن الإشعارات تعمل حتى إذا لم يكن هناك عناصر معينة
console.log('%c[SkyOS v10] Sovereign UI fully loaded. GodMode + Ultra active.', 'color:#7C3AED; font-weight:bold;');
