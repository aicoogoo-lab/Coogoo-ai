// ======================================================
// SkyOS v10 — UI Controller (متطور بالكامل)
// + HoloLiquid Fluid Motion Effect مدمج
// ======================================================

const SkyUI = {
  chatMessages: null,
  thinkingIndicatorId: 'thinking-indicator',

  init() {
    this.chatMessages = document.getElementById('chat-messages');
    this.toastContainer = document.getElementById('toast-container');
    if (!this.toastContainer) {
      this.toastContainer = document.createElement('div');
      this.toastContainer.id = 'toast-container';
      document.body.appendChild(this.toastContainer);
    }
  },

  // عرض رسالة مع تأثير دخول سلس
  addMessage(role, content, options = {}) {
    if (!this.chatMessages) this.init();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(20px)';
    messageDiv.style.transition = 'all 0.3s ease';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = this.parseMarkdown(content);

    const footer = document.createElement('div');
    footer.className = 'message-footer';
    footer.innerHTML = `
      <span class="message-time">${new Date().toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' })}</span>
      ${role === 'assistant' ? '<i class="fas fa-robot" style="font-size:0.7rem;"></i>' : '<i class="fas fa-user" style="font-size:0.7rem;"></i>'}
    `;

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(footer);
    this.chatMessages.appendChild(messageDiv);

    // تأثير الظهور
    requestAnimationFrame(() => {
      messageDiv.style.opacity = '1';
      messageDiv.style.transform = 'translateY(0)';
    });

    this.chatMessages.scrollTo({
      top: this.chatMessages.scrollHeight,
      behavior: 'smooth'
    });

    // إطلاق حدث مخصص للرسالة الجديدة (يمكن للـ mind.js الاستماع له)
    window.dispatchEvent(new CustomEvent('new-message', { detail: { role, content } }));
  },

  // تحليل Markdown متقدم
  parseMarkdown(text) {
    if (!text) return '';

    // معالجة كتل الأكواد
    text = text.replace(/```(\w*)?\n([\s\S]*?)```/g, (match, lang, code) => {
      const language = lang || 'code';
      return `<div class="sky-code-container">
                <div class="sky-code-header">
                  <span><i class="fas fa-code"></i> ${language}</span>
                  <button class="sky-code-copy-btn" onclick="SkyUI.copyCode(this)">
                    <i class="far fa-copy"></i> نسخ
                  </button>
                </div>
                <pre class="sky-code-block"><code>${this.escapeHtml(code.trim())}</code></pre>
              </div>`;
    });

    // معالجة الروابط
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color:#a78bfa;">$1</a>');

    // معالجة الاقتباسات
    text = text.replace(/^> (.+)$/gm, '<blockquote style="border-right:3px solid #6366f1; padding-right:12px; margin:8px 0; color:#94a3b8;">$1</blockquote>');

    // معالجة القوائم غير المرتبة
    text = text.replace(/^[\*\-] (.+)$/gm, '<li style="margin-right:20px;">$1</li>');
    text = text.replace(/(<li.*<\/li>)/s, '<ul style="margin:8px 0;">$1</ul>');

    // معالجة النصوص الغامقة والمائلة
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // الأسطر الجديدة
    text = text.replace(/\n/g, '<br>');

    return text;
  },

  escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
      if (m === '&') return '&amp;';
      if (m === '<') return '&lt;';
      if (m === '>') return '&gt;';
      return m;
    });
  },

  copyCode(button) {
    const container = button.closest('.sky-code-container');
    if (!container) return;
    const codeBlock = container.querySelector('code');
    if (codeBlock) {
      navigator.clipboard.writeText(codeBlock.innerText).then(() => {
        const original = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> تم النسخ';
        setTimeout(() => button.innerHTML = original, 2000);
      }).catch(() => {
        this.showToast('فشل النسخ', 'error');
      });
    }
  },

  // مؤشر التفكير المتقدم
  showThinking(customText = 'أفكر بعمق في سياقك...') {
    if (!this.chatMessages) this.init();
    this.hideThinking(); // إزالة أي مؤشر قديم

    const thinking = document.createElement('div');
    thinking.id = this.thinkingIndicatorId;
    thinking.className = 'message assistant thinking';
    thinking.innerHTML = `
      <div class="message-content" style="display:flex; align-items:center; gap:12px;">
        <div class="thinking-dots">
          <span></span><span></span><span></span>
        </div>
        <span>${customText}</span>
        <i class="fas fa-brain" style="color:#a78bfa; animation: pulse 1.5s infinite;"></i>
      </div>
    `;
    this.chatMessages.appendChild(thinking);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  },

  hideThinking() {
    const el = document.getElementById(this.thinkingIndicatorId);
    if (el) el.remove();
  },

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<i class="fas ${type === 'error' ? 'fa-exclamation-triangle' : type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i> ${message}`;
    this.toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  },

  // تحديث مؤشرات العقل (الثقة، الذاكرة)
  updateMindMetrics(confidence, memoryCount) {
    const confidenceSpan = document.getElementById('mind-confidence');
    const memorySpan = document.getElementById('memory-count');
    if (confidenceSpan) confidenceSpan.textContent = Math.min(100, Math.max(0, confidence));
    if (memorySpan) memorySpan.textContent = memoryCount;

    // تغيير لون نسبة الثقة بناءً على القيمة
    if (confidenceSpan) {
      if (confidence > 80) confidenceSpan.style.color = '#4ade80';
      else if (confidence > 50) confidenceSpan.style.color = '#fbbf24';
      else confidenceSpan.style.color = '#f87171';
    }
  },

  // تغيير مزاج العقل (يؤثر على لون النموذج ثلاثي الأبعاد)
  setMindMood(mood) {
    const event = new CustomEvent('mind-mood-change', { detail: { mood } });
    window.dispatchEvent(event);
  },

  // إضافة تأثير تموج عند إرسال الرسالة
  rippleEffect(element) {
    if (!element) return;
    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    element.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  }
};

/* ============================================================
   HOLOLIQUID FLUID MOTION EFFECT (مدمج)
   ============================================================ */
const HoloLiquidFluid = {
  fluidLayer: null,
  x: 0,
  y: 0,
  tx: 0,
  ty: 0,
  animationId: null,

  init() {
    // إنشاء طبقة السائل الهولوغرافي
    this.fluidLayer = document.createElement("div");
    this.fluidLayer.className = "holo-fluid-layer";
    document.body.appendChild(this.fluidLayer);

    // بدء حلقة الحركة
    this.animate();

    // تتبع حركة الماوس
    document.addEventListener("mousemove", (e) => {
      this.tx = (e.clientX - window.innerWidth / 2) * 0.02;
      this.ty = (e.clientY - window.innerHeight / 2) * 0.02;
    });

    // إيقاف الحركة عند الخروج من النافذة (اختياري)
    document.addEventListener("mouseleave", () => {
      this.tx = 0;
      this.ty = 0;
    });

    console.log('🌊 HoloLiquid Fluid Motion مفعّل');
  },

  animate() {
    this.x += (this.tx - this.x) * 0.05;
    this.y += (this.ty - this.y) * 0.05;

    if (this.fluidLayer) {
      this.fluidLayer.style.transform = `translate(${this.x}px, ${this.y}px)`;
    }

    this.animationId = requestAnimationFrame(() => this.animate());
  },

  // إيقاف الحركة (لتوفير الأداء عند الحاجة)
  stop() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  },

  // استئناف الحركة
  resume() {
    if (!this.animationId) {
      this.animate();
    }
  }
};

// ======================================================
// إضافة الأنماط الديناميكية للتأثيرات
// ======================================================
const addDynamicStyles = () => {
  if (document.getElementById('skyui-dynamic-styles')) return;
  
  const style = document.createElement('style');
  style.id = 'skyui-dynamic-styles';
  style.textContent = `
    /* ==================== */
    /* أنماط SkyUI الأساسية */
    /* ==================== */
    .thinking-dots {
      display: flex;
      gap: 4px;
    }
    .thinking-dots span {
      width: 6px;
      height: 6px;
      background: #a78bfa;
      border-radius: 50%;
      animation: dot-bounce 1.4s infinite ease-in-out both;
    }
    .thinking-dots span:nth-child(1) { animation-delay: -0.32s; }
    .thinking-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes dot-bounce {
      0%, 80%, 100% { transform: scale(0); opacity: 0.3; }
      40% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }
    
    .message {
      transition: opacity 0.3s ease, transform 0.3s ease;
    }
    
    .toast {
      background: #1e1e2f;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 10px 18px;
      margin-bottom: 8px;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 10px;
      backdrop-filter: blur(8px);
    }
    .toast-error { border-right: 3px solid #ef4444; }
    .toast-success { border-right: 3px solid #22c55e; }
    
    .ripple {
      position: absolute;
      border-radius: 50%;
      background: rgba(99, 102, 241, 0.3);
      transform: scale(0);
      animation: ripple-anim 0.6s linear;
      pointer-events: none;
    }
    
    @keyframes ripple-anim {
      to { transform: scale(4); opacity: 0; }
    }

    /* ============================ */
    /* أنماط HoloLiquid Fluid Layer */
    /* ============================ */
    .holo-fluid-layer {
      position: fixed;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      pointer-events: none;
      z-index: -1;
      background:
        radial-gradient(circle at 30% 30%, rgba(79, 210, 255, 0.08), transparent 50%),
        radial-gradient(circle at 70% 60%, rgba(179, 107, 255, 0.08), transparent 50%),
        radial-gradient(circle at 50% 80%, rgba(255, 79, 123, 0.05), transparent 50%);
      filter: blur(60px);
      transition: transform 0.1s ease-out;
      will-change: transform;
    }
    
    /* كود بلوك */
    .sky-code-container {
      background: rgba(15, 20, 35, 0.9);
      border: 1px solid rgba(79, 210, 255, 0.2);
      border-radius: 12px;
      margin: 10px 0;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .sky-code-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 14px;
      background: rgba(10, 15, 30, 0.8);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      font-size: 0.78rem;
      color: #a4b0d0;
    }
    
    .sky-code-copy-btn {
      background: rgba(79, 210, 255, 0.1);
      border: 1px solid rgba(79, 210, 255, 0.3);
      color: #a4b0d0;
      padding: 4px 10px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.72rem;
      transition: all 0.2s ease;
    }
    
    .sky-code-copy-btn:hover {
      background: rgba(79, 210, 255, 0.2);
      color: #e8eeff;
    }
    
    .sky-code-block {
      padding: 14px;
      margin: 0;
      overflow-x: auto;
      font-family: 'Fira Code', 'Cascadia Code', monospace;
      font-size: 0.82rem;
      line-height: 1.6;
      color: #e2e8f0;
    }
    
    .sky-code-block code {
      font-family: inherit;
    }
    
    /* تنسيق الرسائل */
    .message-content {
      font-size: 0.9rem;
      line-height: 1.6;
    }
    
    .message-content blockquote {
      border-right: 3px solid #6366f1;
      padding-right: 12px;
      margin: 8px 0;
      color: #94a3b8;
      background: rgba(99, 102, 241, 0.05);
      padding: 8px 12px;
      border-radius: 0 8px 8px 0;
    }
    
    .message-content ul {
      margin: 8px 0;
      padding-right: 20px;
    }
    
    .message-content li {
      margin-bottom: 4px;
    }
    
    .message-footer {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 6px;
      font-size: 0.7rem;
      color: rgba(255, 255, 255, 0.4);
    }
    
    .message.user .message-footer {
      justify-content: flex-end;
    }
  `;
  
  document.head.appendChild(style);
};

// ======================================================
// تهيئة كل شيء عند تحميل الصفحة
// ======================================================
document.addEventListener('DOMContentLoaded', () => {
  // تهيئة SkyUI
  SkyUI.init();
  
  // إضافة الأنماط الديناميكية
  addDynamicStyles();
  
  // تفعيل تأثير HoloLiquid Fluid Motion
  HoloLiquidFluid.init();
  
  console.log('✅ SkyUI + HoloLiquid Fluid Motion جاهزان');
});

// ======================================================
// جعل الدوال عامة للاستخدام من HTML
// ======================================================
window.SkyUI = SkyUI;
window.HoloLiquidFluid = HoloLiquidFluid;
