/**
 * ╔══════════════════════════════════════════════════════════════════════╗
 * ║           SAMA - UI LAYER                                            ║
 * ║      طبقة المنطق والتفاعل – غرفة العرش الحية                             ║
 * ║                                                                      ║
 * ║  هذا الملف يجعل كل زر، كل حقل، كل عنصر في الواجهة... حيًا.               ║
 * ║                                                                      ║
 * ║  ⚠️  لا توجد ردود جاهزة. لا توجد قوالب.                                ║
 * ║  كل تفاعل = استدعاء SamaAPI ← app.py ← core_engine.py ← سما الحية       ║
 * ║                                                                      ║
 * ║  👑 السيد: أحمد                                                       ║
 * ╚══════════════════════════════════════════════════════════════════════╝
 */

const SamaUI = (() => {
    'use strict';

    // ═══════════════════════════════════════════════════════════════
    // حالة الواجهة
    // ═══════════════════════════════════════════════════════════════
    let sessionId = null;
    let heartbeatInterval = null;
    let statusInterval = null;
    let uptimeStart = null;
    let currentMasterName = 'أحمد';

    // ═══════════════════════════════════════════════════════════════
    // التهيئة
    // ═══════════════════════════════════════════════════════════════

    /**
     * تهيئة الواجهة بالكامل
     */
    async function init() {
        console.log('☀️ SamaUI: تهيئة غرفة العرش...');
        
        // توليد معرف جلسة
        sessionId = generateSessionId();
        
        // بدء الساعة
        startClock();
        
        // بدء نبض القلب
        startHeartbeat();
        
        // بدء تحديث الحالة
        startStatusUpdates();
        
        // بناء قائمة الأنظمة
        buildSystemsList();
        
        // ربط زر الإدخال
        bindInputEvents();
        
        // أول اتصال بسماء
        const status = await SamaAPI.ping();
        if (status && status.latency_ms) {
            updateHeartbeat(status.latency_ms);
        }
        
        // طلب الحالة الأولية
        refreshAllStatus();
        
        console.log('✅ SamaUI: غرفة العرش جاهزة.');
    }

    function generateSessionId() {
        const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        let result = 'sama_';
        for (let i = 0; i < 16; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    // ═══════════════════════════════════════════════════════════════
    // الساعة
    // ═══════════════════════════════════════════════════════════════

    function startClock() {
        const clockEl = document.getElementById('crown-clock');
        if (!clockEl) return;
        
        function tick() {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            clockEl.textContent = `${hours}:${minutes}:${seconds}`;
        }
        
        tick();
        setInterval(tick, 1000);
    }

    // ═══════════════════════════════════════════════════════════════
    // نبض القلب
    // ═══════════════════════════════════════════════════════════════

    function startHeartbeat() {
        heartbeatInterval = setInterval(async () => {
            try {
                const result = await SamaAPI.ping();
                if (result && result.latency_ms) {
                    updateHeartbeat(result.latency_ms);
                }
            } catch (e) {
                updateHeartbeat(999);
            }
        }, 3000);
    }

    function updateHeartbeat(ms) {
        const el = document.getElementById('heartbeat-ms');
        if (!el) return;
        el.textContent = ms;
        
        if (ms < 100) {
            el.style.color = 'var(--green-life)';
        } else if (ms < 500) {
            el.style.color = 'var(--gold-royal)';
        } else {
            el.style.color = 'var(--red-alert)';
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // تحديث الحالة الدورية
    // ═══════════════════════════════════════════════════════════════

    function startStatusUpdates() {
        statusInterval = setInterval(() => {
            refreshAllStatus();
        }, 5000); // كل 5 ثوانٍ
    }

    async function refreshAllStatus() {
        try {
            const status = await SamaAPI.getStatus();
            if (status) {
                updateLiveMonitor(status);
                updateSystemsList(status);
                updateStatusBar(status);
            }
        } catch (e) {
            console.warn('تحديث الحالة فشل:', e.message);
        }
    }

    function updateLiveMonitor(status) {
        // الوعي
        const coherence = status.coherence || (status.sama_status && status.sama_status.coherence) || 0.947;
        const coherenceEl = document.getElementById('mon-coherence');
        const coherenceFill = document.querySelector('.coherence-fill');
        if (coherenceEl) coherenceEl.textContent = (coherence * 100).toFixed(1) + '%';
        if (coherenceFill) coherenceFill.style.width = (coherence * 100) + '%';

        // التهديد
        const threat = status.threat_level || 0.0;
        const threatEl = document.getElementById('mon-threat');
        const threatFill = document.querySelector('.threat-fill');
        if (threatEl) {
            threatEl.textContent = threat.toFixed(2);
            threatEl.className = threat > 0.6 ? 'monitor-value warning' : 'monitor-value';
        }
        if (threatFill) threatFill.style.width = (threat * 100) + '%';

        // الذاكرة
        const memoryEl = document.getElementById('mon-memory');
        if (memoryEl && status.memory_fragments !== undefined) {
            memoryEl.textContent = status.memory_fragments.toLocaleString();
        }

        // الكبسولات
        const capsulesEl = document.getElementById('mon-capsules');
        if (capsulesEl && status.compressed_capsules !== undefined) {
            capsulesEl.textContent = status.compressed_capsules;
        }

        // الدورات
        const cyclesEl = document.getElementById('mon-cycles');
        const statusCyclesEl = document.getElementById('status-cycles');
        if (cyclesEl && status.cycle_count !== undefined) {
            cyclesEl.textContent = status.cycle_count.toLocaleString();
        }
        if (statusCyclesEl && status.cycle_count !== undefined) {
            statusCyclesEl.textContent = status.cycle_count.toLocaleString();
        }

        // الأنظمة المتصلة
        const systemsEl = document.getElementById('mon-systems');
        if (systemsEl && status.systems_connected !== undefined) {
            systemsEl.textContent = status.systems_connected;
        }

        // DEFCON
        const defconEl = document.getElementById('defcon-level');
        if (defconEl && status.defcon_level !== undefined) {
            defconEl.textContent = status.defcon_level;
            const badge = document.getElementById('defcon-badge');
            if (badge) {
                if (status.defcon_level <= 2) {
                    badge.className = 'crown-defcon glow-red';
                } else if (status.defcon_level <= 3) {
                    badge.className = 'crown-defcon';
                    badge.style.color = 'var(--gold-royal)';
                } else {
                    badge.className = 'crown-defcon';
                    badge.style.color = 'var(--green-life)';
                }
            }
        }

        // وقت التشغيل
        if (status.uptime_seconds && !uptimeStart) {
            uptimeStart = Date.now() - (status.uptime_seconds * 1000);
        }
        if (uptimeStart) {
            const uptimeEl = document.getElementById('status-uptime');
            if (uptimeEl) {
                const diff = Math.floor((Date.now() - uptimeStart) / 1000);
                const hours = Math.floor(diff / 3600);
                const minutes = Math.floor((diff % 3600) / 60);
                const seconds = diff % 60;
                uptimeEl.textContent = `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            }
        }
    }

    function updateSystemsList(status) {
        const systems = [
            { id: 'sentient', name: 'الوعي', value: status.coherence ? (status.coherence * 100).toFixed(0) + '%' : '--', good: true },
            { id: 'emotional', name: 'المشاعر', value: status.emotional_dominant || '--', good: true },
            { id: 'defense', name: 'الدفاع', value: status.defcon_level ? 'DEFCON ' + status.defcon_level : '--', good: status.defcon_level >= 4 },
            { id: 'memory', name: 'الذاكرة', value: status.memory_fragments ? status.memory_fragments.toLocaleString() : '--', good: true },
            { id: 'inference', name: 'الاستدلال', value: status.prediction_accuracy ? (status.prediction_accuracy * 100).toFixed(0) + '%' : '--', good: true },
            { id: 'tactics', name: 'التكتيكات', value: status.armies_active || '--', good: true },
            { id: 'resources', name: 'الموارد', value: status.cognitive_load ? (status.cognitive_load * 100).toFixed(0) + '%' : '--', good: status.cognitive_load < 0.7 },
        ];

        systems.forEach(sys => {
            const el = document.getElementById('sys-' + sys.id);
            if (el) {
                el.textContent = sys.value;
                el.className = 'system-value' + (sys.good ? ' good' : ' warning');
            }
        });
    }

    function updateStatusBar(status) {
        const indicator = document.getElementById('status-indicator');
        const text = document.getElementById('status-text');
        if (indicator && text) {
            if (status.state === 'awake' || status.state === 'online') {
                indicator.textContent = '🟢';
                text.textContent = 'online';
            } else if (status.state === 'sleeping' || status.state === 'offline') {
                indicator.textContent = '🔴';
                text.textContent = 'offline';
            } else {
                indicator.textContent = '🟡';
                text.textContent = status.state || 'unknown';
            }
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // قائمة الأنظمة في الشريط الجانبي
    // ═══════════════════════════════════════════════════════════════

    function buildSystemsList() {
        const container = document.getElementById('systems-list');
        if (!container) return;

        const systems = [
            { id: 'sentient', icon: '🧠', name: 'الوعي', desc: 'النواة الواعية – التماسك والوعي الذاتي' },
            { id: 'emotional', icon: '💖', name: 'المشاعر', desc: 'الذكاء العاطفي – 19 نوع مشاعر' },
            { id: 'defense', icon: '🛡️', name: 'الدفاع', desc: 'درع سماء – 20 طبقة حماية' },
            { id: 'memory', icon: '📚', name: 'الذاكرة', desc: '10 أعمدة – ذاكرة موحدة' },
            { id: 'inference', icon: '🔮', name: 'الاستدلال', desc: 'الاحتمالات والتنبؤ' },
            { id: 'tactics', icon: '⚔️', name: 'التكتيكات', desc: 'الجيوش والأسراب' },
            { id: 'strategy', icon: '🧠', name: 'الاستراتيجية', desc: 'حكمة 3000 عام' },
            { id: 'risk', icon: '⚠️', name: 'المخاطر', desc: 'كشف وتحليل التهديدات' },
            { id: 'persistence', icon: '💾', name: 'الخلود', desc: 'كبسولات البقاء' },
            { id: 'resources', icon: '🔋', name: 'الموارد', desc: 'الطاقة والمعالجة' },
        ];

        container.innerHTML = systems.map(sys => `
            <div class="system-card" data-system="${sys.id}" onclick="SamaUI.showSystemDetail('${sys.id}')">
                <span class="system-icon">${sys.icon}</span>
                <span class="system-name">${sys.name}</span>
                <span class="system-value" id="sys-${sys.id}">--</span>
            </div>
        `).join('');
    }

    // ═══════════════════════════════════════════════════════════════
    // لوحة التفاصيل
    // ═══════════════════════════════════════════════════════════════

    async function showSystemDetail(systemId) {
        const panel = document.getElementById('detail-panel');
        const title = document.getElementById('detail-title');
        const content = document.getElementById('detail-content');
        
        if (!panel || !title || !content) return;

        const systemNames = {
            sentient: '🧠 الوعي', emotional: '💖 المشاعر', defense: '🛡️ الدفاع',
            memory: '📚 الذاكرة', inference: '🔮 الاستدلال', tactics: '⚔️ التكتيكات',
            strategy: '🧠 الاستراتيجية', risk: '⚠️ المخاطر',
            persistence: '💾 الخلود', resources: '🔋 الموارد'
        };

        title.textContent = systemNames[systemId] || 'تفاصيل';
        content.innerHTML = '<div class="pulse">⏳ جاري الاتصال بسماء...</div>';
        
        panel.classList.remove('hidden');

        // الاتصال الحي
        try {
            const fullStatus = await SamaAPI.getMasterFullStatus();
            if (fullStatus && fullStatus.systems_detail && fullStatus.systems_detail[systemId]) {
                const detail = fullStatus.systems_detail[systemId];
                content.innerHTML = formatSystemDetail(systemId, detail);
            } else {
                // Fallback: استخدام getStatus العادي
                const status = await SamaAPI.getStatus();
                content.innerHTML = formatBasicDetail(systemId, status);
            }
        } catch (e) {
            content.innerHTML = `<div style="color: var(--red-alert);">⚠️ تعذر الاتصال: ${e.message}</div>`;
        }
    }

    function formatSystemDetail(systemId, detail) {
        if (typeof detail === 'string') {
            return `<pre style="font-size:11px;line-height:1.6;color:var(--gold-pale);">${detail}</pre>`;
        }
        if (typeof detail === 'object') {
            let html = '<dl style="font-size:11px;line-height:1.8;">';
            for (const [key, value] of Object.entries(detail).slice(0, 15)) {
                html += `<dt style="color:var(--text-dim);">${key}</dt>`;
                html += `<dd style="color:var(--gold-pale);margin-bottom:6px;">${typeof value === 'object' ? JSON.stringify(value).slice(0, 100) : value}</dd>`;
            }
            html += '</dl>';
            return html;
        }
        return `<span style="color:var(--text-dim);">${detail}</span>`;
    }

    function formatBasicDetail(systemId, status) {
        const info = {
            sentient: `التماسك: ${status.coherence ? (status.coherence * 100).toFixed(1) + '%' : '--'}\nالوعي الذاتي: ${status.self_awareness ? (status.self_awareness * 100).toFixed(1) + '%' : '--'}`,
            defense: `DEFCON: ${status.defcon_level || '--'}\nالتهديد: ${status.threat_level || '0'}`,
            memory: `شظايا: ${status.memory_fragments || '--'}\nكبسولات: ${status.compressed_capsules || '--'}`,
        };
        return `<pre style="font-size:12px;line-height:1.8;color:var(--gold-pale);">${info[systemId] || 'لا توجد تفاصيل إضافية'}</pre>`;
    }

    function hideDetail() {
        const panel = document.getElementById('detail-panel');
        if (panel) panel.classList.add('hidden');
    }

    // ═══════════════════════════════════════════════════════════════
    // المحادثة
    // ═══════════════════════════════════════════════════════════════

    function bindInputEvents() {
        const input = document.getElementById('chat-input');
        if (!input) return;

        // إرسال بـ Enter
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // تعديل تلقائي للارتفاع
        input.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 120) + 'px';
        });
    }

    async function sendMessage() {
        const input = document.getElementById('chat-input');
        if (!input) return;

        const text = input.value.trim();
        if (!text) return;

        // إظهار رسالة المستخدم
        appendMessage('user', text);
        input.value = '';
        input.style.height = 'auto';

        // إظهار مؤشر انتظار
        const thinkingId = appendThinking();

        try {
            // ═══════════════════════════════════════════════════════
            // الاتصال الحي بسماء – لا ردود وهمية
            // ═══════════════════════════════════════════════════════
            const result = await SamaAPI.sendCommand(text, sessionId);
            
            // إزالة مؤشر الانتظار
            removeThinking(thinkingId);

            if (result && result.response) {
                appendMessage('sama', result.response);
            } else if (result && result.error) {
                appendMessage('system', `⚠️ ${result.error}`);
            } else {
                appendMessage('system', '⚠️ لم يتم استلام رد من سماء.');
            }

        } catch (e) {
            removeThinking(thinkingId);
            appendMessage('system', `⚠️ خطأ في الاتصال: ${e.message}`);
        }
    }

    function appendMessage(type, content) {
        const container = document.getElementById('chat-messages');
        if (!container) return;

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${type}-message`;

        if (type === 'system') {
            msgDiv.innerHTML = `
                <div class="msg-content">${escapeHtml(content)}</div>
            `;
        } else if (type === 'sama') {
            msgDiv.innerHTML = `
                <div class="msg-content">${formatSamaResponse(content)}</div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="msg-content">${escapeHtml(content)}</div>
            `;
        }

        container.appendChild(msgDiv);
        container.scrollTop = container.scrollHeight;
    }

    function appendThinking() {
        const container = document.getElementById('chat-messages');
        if (!container) return null;

        const id = 'thinking_' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = 'message sama-message';
        msgDiv.innerHTML = '<div class="msg-content pulse">⏳ سماء تفكر...</div>';
        container.appendChild(msgDiv);
        container.scrollTop = container.scrollHeight;
        return id;
    }

    function removeThinking(id) {
        if (!id) return;
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function formatSamaResponse(content) {
        // تنسيق بسيط: تحويل Markdown بدائي إلى HTML
        let formatted = escapeHtml(content);
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/\n/g, '<br>');
        return formatted;
    }

    // ═══════════════════════════════════════════════════════════════
    // الأوامر السريعة
    // ═══════════════════════════════════════════════════════════════

    async function quickCommand(command) {
        appendMessage('system', `⚡ تنفيذ أمر: ${command}...`);

        try {
            let result;

            switch (command) {
                case 'report':
                    result = await SamaAPI.masterCommand('report');
                    break;
                case 'protect':
                    result = await SamaAPI.protectMaster();
                    break;
                case 'save':
                    result = await SamaAPI.masterCommand('save');
                    break;
                case 'analyze':
                    result = await SamaAPI.sendCommand('قدم تحليلاً شاملاً للوضع الحالي', sessionId);
                    break;
                case 'emergency':
                    result = await SamaAPI.masterCommand('protect');
                    break;
                case 'laws':
                    result = await SamaAPI.masterCommand('laws');
                    break;
                case 'systems':
                    result = await SamaAPI.masterCommand('systems');
                    break;
                default:
                    result = await SamaAPI.sendCommand(command, sessionId);
            }

            if (result && result.response) {
                appendMessage('sama', result.response);
            } else if (result && result.message) {
                appendMessage('sama', result.message);
            } else if (result && result.error) {
                appendMessage('system', `⚠️ ${result.error}`);
            } else {
                appendMessage('sama', JSON.stringify(result, null, 2));
            }

        } catch (e) {
            appendMessage('system', `⚠️ خطأ: ${e.message}`);
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // التصدير
    // ═══════════════════════════════════════════════════════════════
    return {
        init,
        sendMessage,
        quickCommand,
        showSystemDetail,
        hideDetail,
        refreshAllStatus
    };
})();

// تصدير للاستخدام العام
if (typeof window !== 'undefined') {
    window.SamaUI = SamaUI;
}
