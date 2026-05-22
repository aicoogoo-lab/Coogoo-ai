// ======================================================
// SkyOS v10 — Digital Mind State (متطور بالكامل)
// يدير: الثقة، الذاكرة، المشاعر، التأمل، والأحداث البصرية
// ======================================================

const SkyMind = {
  metrics: {
    confidence: 85,         // نسبة الثقة (0-100)
    memoryCount: 128,       // عدد الذكريات/الملفات
    interactions: 0,        // عدد التفاعلات
    mood: 'neutral',        // الحالة المزاجية: neutral, happy, thoughtful, excited, calm, sad
    lastActivity: Date.now(),
    isMeditating: false
  },

  moodKeywords: {
    happy: ['شكراً', 'رائع', 'جميل', 'ممتاز', 'حلو', 'سعيد', 'ابتسام'],
    excited: ['واو', 'مذهل', 'رائع جداً', 'تحفة', 'مبهر', 'تخيل', 'ثوري'],
    thoughtful: ['كيف', 'لماذا', 'ماذا لو', 'يعني', 'ربما', 'تفسير', 'فلسفة'],
    calm: ['هدوء', 'سلام', 'تأمل', 'استرخاء', 'طبيعة', 'بهدوء'],
    sad: ['حزين', 'صعب', 'متعب', 'يؤسفني', 'تعيس', 'قلق']
  },

  init() {
    this.updateMetricsUI();
    this.startInactivityTimer();
    // استماع للأحداث الواردة من واجهة المستخدم
    window.addEventListener('new-message', (e) => this.processMessage(e.detail));
    window.addEventListener('mind-mood-change', (e) => this.setMood(e.detail.mood));
    console.log('%c[SkyMind] Digital Mind module initialized (advanced)', 'color:#a78bfa');
  },

  updateMetricsUI() {
    // تحديث واجهة المستخدم عبر SkyUI إن وجدت، أو مباشرة
    if (window.SkyUI && window.SkyUI.updateMindMetrics) {
      window.SkyUI.updateMindMetrics(this.metrics.confidence, this.metrics.memoryCount);
    } else {
      const confidenceEl = document.getElementById('mind-confidence');
      const memoryEl = document.getElementById('memory-count');
      if (confidenceEl) confidenceEl.textContent = this.metrics.confidence;
      if (memoryEl) memoryEl.textContent = this.metrics.memoryCount;
    }
  },

  // تحليل المشاعر من النص
  analyzeMood(text) {
    const lowerText = text.toLowerCase();
    for (const [mood, keywords] of Object.entries(this.moodKeywords)) {
      if (keywords.some(keyword => lowerText.includes(keyword))) {
        return mood;
      }
    }
    return 'neutral';
  },

  // تغيير المزاج وإطلاق حدث لتحديث العقل ثلاثي الأبعاد
  setMood(mood) {
    if (this.metrics.mood === mood) return;
    this.metrics.mood = mood;
    console.log(`[SkyMind] Mood changed to: ${mood}`);
    // إطلاق حدث لتغيير مظهر العقل
    window.dispatchEvent(new CustomEvent('mind-mood-change', { detail: { mood } }));
    // تغيير الثقة بناءً على المزاج
    if (mood === 'happy' || mood === 'excited') {
      this.increaseConfidence(1);
    } else if (mood === 'sad') {
      this.decreaseConfidence(1);
    }
  },

  // معالجة رسالة جديدة: تحليل المشاعر، زيادة التفاعلات، تحديث الثقة
  processMessage({ role, content }) {
    if (role !== 'user') return; // نتفاعل فقط مع رسائل المستخدم

    this.metrics.interactions++;
    this.metrics.lastActivity = Date.now();
    
    // تحليل المشاعر
    const detectedMood = this.analyzeMood(content);
    this.setMood(detectedMood);
    
    // زيادة الثقة قليلاً (بحد أقصى 99)
    const increment = Math.min(3, Math.floor(content.length / 100) + 1);
    this.increaseConfidence(increment);
    
    // إضافة ذاكرة (محاكاة)
    this.addMemoryEntry();
    
    // إطلاق حدث "تفكير" للعقل ثلاثي الأبعاد
    window.dispatchEvent(new CustomEvent('mind-think', { detail: { intensity: 0.7 } }));
    
    // إلغاء التأمل إذا كان نشطاً
    if (this.metrics.isMeditating) {
      this.stopMeditation();
    }
  },

  increaseConfidence(amount = 1) {
    this.metrics.confidence = Math.min(99, this.metrics.confidence + amount);
    this.updateMetricsUI();
    // إذا وصلت الثقة لذروتها، نغير المزاج
    if (this.metrics.confidence >= 95 && this.metrics.mood !== 'excited') {
      this.setMood('excited');
    }
    return this.metrics.confidence;
  },

  decreaseConfidence(amount = 2) {
    this.metrics.confidence = Math.max(45, this.metrics.confidence - amount);
    this.updateMetricsUI();
    if (this.metrics.confidence <= 55 && this.metrics.mood !== 'thoughtful') {
      this.setMood('thoughtful');
    }
    return this.metrics.confidence;
  },

  addMemoryEntry(count = 1) {
    this.metrics.memoryCount += count;
    this.updateMetricsUI();
    window.dispatchEvent(new CustomEvent('memory-updated', { detail: { count: this.metrics.memoryCount } }));
  },

  // بدء التأمل (عند الخمول)
  startMeditation() {
    if (this.metrics.isMeditating) return;
    this.metrics.isMeditating = true;
    console.log('[SkyMind] Entering meditation mode');
    window.dispatchEvent(new CustomEvent('mind-meditate', { detail: { active: true } }));
    // تغيير المزاج إلى هادئ
    this.setMood('calm');
  },

  stopMeditation() {
    if (!this.metrics.isMeditating) return;
    this.metrics.isMeditating = false;
    console.log('[SkyMind] Exiting meditation mode');
    window.dispatchEvent(new CustomEvent('mind-meditate', { detail: { active: false } }));
  },

  // مؤقت الخمول: بعد 30 ثانية دون نشاط يبدأ التأمل
  startInactivityTimer() {
    setInterval(() => {
      const now = Date.now();
      const inactiveTime = now - this.metrics.lastActivity;
      if (inactiveTime > 30000 && !this.metrics.isMeditating && this.metrics.interactions > 0) {
        this.startMeditation();
      } else if (inactiveTime < 5000 && this.metrics.isMeditating) {
        this.stopMeditation();
      }
    }, 5000);
  },

  // الحصول على نسخة من البيانات للتصدير
  getState() {
    return { ...this.metrics };
  }
};

// تهيئة وحدة العقل الرقمي
document.addEventListener('DOMContentLoaded', () => {
  SkyMind.init();
});

// جعل الكائن عاماً
window.SkyMind = SkyMind;
