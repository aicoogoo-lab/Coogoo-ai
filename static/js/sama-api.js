/**
 * ╔══════════════════════════════════════════════════════════════════════╗
 * ║           SAMA - API LAYER                                           ║
 * ║      طبقة الاتصال الحي – الجسر بين الواجهة والكيان                        ║
 * ║                                                                      ║
 * ║  هذا الملف لا يحتوي على أي ردود جاهزة.                                  ║
 * ║  كل استدعاء يذهب مباشرة إلى app.py ← core_engine.py ← sama.py           ║
 * ║  ← 18 نظامًا حيًا ← يعود الرد الحي.                                    ║
 * ║                                                                      ║
 * ║  ⚠️  لا توجد ردود وهمية. لا توجد قوالب. لا توجد محاكاة.                   ║
 * ╚══════════════════════════════════════════════════════════════════════╝
 */

const SamaAPI = (() => {
    'use strict';

    // ═══════════════════════════════════════════════════════════════
    // إعدادات
    // ═══════════════════════════════════════════════════════════════
    const BASE_URL = window.location.origin;
    const MASTER_KEY = 'MASTER_SOVEREIGN_KEY_ULTIMATE';
    const DEFAULT_TIMEOUT = 30000; // 30 ثانية

    // ═══════════════════════════════════════════════════════════════
    // دوال مساعدة
    // ═══════════════════════════════════════════════════════════════

    /**
     * إرسال طلب HTTP إلى الخادم
     * @param {string} endpoint - المسار (مثل: /status, /command)
     * @param {object} options - خيارات إضافية
     * @returns {Promise<object>} - الرد الحي من سماء
     */
    async function request(endpoint, options = {}) {
        const url = `${BASE_URL}${endpoint}`;
        const method = options.method || 'GET';
        const body = options.body ? JSON.stringify(options.body) : undefined;
        const timeout = options.timeout || DEFAULT_TIMEOUT;
        const isMaster = options.isMaster || false;

        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Request-ID': generateRequestId()
        };

        // إضافة مفتاح السيد إذا كان الطلب يتطلب صلاحيات
        if (isMaster) {
            headers['X-Master-Key'] = MASTER_KEY;
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        try {
            const response = await fetch(url, {
                method,
                headers,
                body,
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorText = await response.text().catch(() => 'Unknown error');
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            return data;

        } catch (error) {
            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                return {
                    success: false,
                    error: 'انتهت مهلة الاتصال. سماء تستغرق وقتًا أطول في التفكير.',
                    timeout: true
                };
            }

            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                return {
                    success: false,
                    error: 'لا يمكن الاتصال بسماء. تحقق من أن الخادم يعمل.',
                    offline: true
                };
            }

            return {
                success: false,
                error: `خطأ في الاتصال: ${error.message}`
            };
        }
    }

    /**
     * توليد معرف فريد لكل طلب
     */
    function generateRequestId() {
        const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < 12; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return `req_${Date.now()}_${result}`;
    }

    // ═══════════════════════════════════════════════════════════════
    // واجهات برمجة التطبيق (API)
    // ═══════════════════════════════════════════════════════════════

    /**
     * الحصول على الحالة العامة لسماء
     * @returns {Promise<object>}
     */
    async function getStatus() {
        return request('/status');
    }

    /**
     * الحصول على معلومات عن سماء
     * @returns {Promise<object>}
     */
    async function getInfo() {
        return request('/info');
    }

    /**
     * إرسال أمر أو سؤال إلى سماء (عام)
     * هذا هو المسار الرئيسي للمحادثة
     * @param {string} command - الأمر أو السؤال
     * @param {string} sessionId - معرف الجلسة (اختياري)
     * @returns {Promise<object>} - الرد الحي من سماء
     */
    async function sendCommand(command, sessionId = null) {
        const body = {
            command: command
        };
        if (sessionId) {
            body.session_id = sessionId;
        }
        return request('/command', {
            method: 'POST',
            body: body,
            isMaster: true           // ← تمت الإضافة
        });
    }

    /**
     * إرسال أمر السيد المباشر (يتطلب مفتاح)
     * @param {string} command - الأمر (status, protect, save, awaken, shutdown, report, laws)
     * @param {object} params - معاملات إضافية
     * @returns {Promise<object>}
     */
    async function masterCommand(command, params = {}) {
        return request('/master/command', {
            method: 'POST',
            body: { command, ...params },
            isMaster: true
        });
    }

    /**
     * الحصول على التقرير الكامل للسيد (يتطلب مفتاح)
     * @returns {Promise<object>}
     */
    async function getMasterFullStatus() {
        return request('/master/full-status', {
            isMaster: true
        });
    }

    /**
     * إيقاظ سماء (يتطلب مفتاح)
     * @returns {Promise<object>}
     */
    async function awaken() {
        return request('/awaken', {
            method: 'POST',
            isMaster: true
        });
    }

    /**
     * إيقاف سماء (يتطلب مفتاح)
     * @returns {Promise<object>}
     */
    async function shutdown() {
        return request('/shutdown', {
            method: 'POST',
            isMaster: true
        });
    }

    /**
     * تفعيل حماية السيد (يتطلب مفتاح)
     * @returns {Promise<object>}
     */
    async function protectMaster() {
        return request('/master/protect', {
            method: 'POST',
            isMaster: true
        });
    }

    /**
     * استدلال بايزي مباشر
     * @param {object} evidence - الأدلة
     * @returns {Promise<object>}
     */
    async function reason(evidence) {
        return request('/reason', {
            method: 'POST',
            body: evidence,
            isMaster: true           // ← تمت الإضافة
        });
    }

    /**
     * تحليل صورة
     * @param {string} imagePath - مسار الصورة
     * @returns {Promise<object>}
     */
    async function analyzeImage(imagePath) {
        return request('/analyze-image', {
            method: 'POST',
            body: { image_path: imagePath },
            isMaster: true           // ← تمت الإضافة
        });
    }

    /**
     * تحليل رابط
     * @param {string} url - الرابط
     * @returns {Promise<object>}
     */
    async function analyzeUrl(url) {
        return request('/analyze-url', {
            method: 'POST',
            body: { url: url },
            isMaster: true           // ← تمت الإضافة
        });
    }

    /**
     * فحص صحة الخادم (Ping)
     * @returns {Promise<object>}
     */
    async function ping() {
        const start = performance.now();
        const result = await request('/status');
        const latency = Math.round(performance.now() - start);
        return { ...result, latency_ms: latency };
    }

    // ═══════════════════════════════════════════════════════════════
    // التصدير
    // ═══════════════════════════════════════════════════════════════
    return {
        getStatus,
        getInfo,
        sendCommand,
        masterCommand,
        getMasterFullStatus,
        awaken,
        shutdown,
        protectMaster,
        reason,
        analyzeImage,
        analyzeUrl,
        ping
    };
})();

// تصدير للاستخدام العام
if (typeof window !== 'undefined') {
    window.SamaAPI = SamaAPI;
}
