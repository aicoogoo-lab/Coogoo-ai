// ======================================================
// SkyOS v10 — Digital Mind State (النسخة الثورية)
// ======================================================

const SkyMind = {
  metrics: {
    confidence: 94,
    memoryCount: 128,
    interactions: 0,
  },

  init() {
    this.updateMetricsUI();
    console.log('%c[SkyMind] Digital Mind module initialized', 'color:#a78bfa');
  },

  updateMetricsUI() {
    const confidenceEl = document.getElementById('mind-confidence');
    const memoryEl = document.getElementById('memory-count');

    if (confidenceEl) confidenceEl.textContent = this.metrics.confidence;
    if (memoryEl) memoryEl.textContent = this.metrics.memoryCount;
  },

  increaseConfidence(amount = 1) {
    this.metrics.confidence = Math.min(99, this.metrics.confidence + amount);
    this.updateMetricsUI();

    // تفعيل تأثير بصري على العقل الثلاثي الأبعاد
    if (window.SkyMind3D) {
      window.SkyMind3D.triggerThinking();
    }
  },

  decreaseConfidence(amount = 2) {
    this.metrics.confidence = Math.max(60, this.metrics.confidence - amount);
    this.updateMetricsUI();
  },

  addMemoryEntry() {
    this.metrics.memoryCount++;
    this.updateMetricsUI();
  }
};

// تهيئة وحدة العقل الرقمي
document.addEventListener('DOMContentLoaded', () => {
  SkyMind.init();
});
