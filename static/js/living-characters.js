// ======================================================
// سماء • الشخصيات الحية (النسخة التفاعلية)
// ======================================================

const SkyCharacters = {
  chars: {
    pink: { name: 'تراس', mood: 'idle', hidden: false, hideUntil: 0 },
    green: { name: 'حكيم', mood: 'idle', hidden: false, hideUntil: 0 },
    white: { name: 'لطيفة', mood: 'idle', hidden: false, hideUntil: 0 }
  },
  audioEnabled: true,
  audioContext: null,
  
  init() {
    this.createCharactersUI();
    this.bindEvents();
    this.initAudio();
    this.startIdleAnimation();
    console.log('🌟 الشخصيات الحية جاهزة');
  },
  
  createCharactersUI() {
    const container = document.createElement('div');
    container.id = 'living-chars';
    container.innerHTML = `
      <div class="char-spot" data-char="pink">
        <div class="char-avatar char-pink">
          <div class="char-face">
            <div class="eyes">
              <div class="eye left-eye"></div>
              <div class="eye right-eye"></div>
            </div>
            <div class="mouth"></div>
            <div class="blush"></div>
          </div>
        </div>
        <div class="char-name">تراس</div>
      </div>
      <div class="char-spot" data-char="green">
        <div class="char-avatar char-green">
          <div class="char-face">
            <div class="eyes">
              <div class="eye left-eye"></div>
              <div class="eye right-eye"></div>
            </div>
            <div class="mouth"></div>
            <div class="blush"></div>
          </div>
        </div>
        <div class="char-name">حكيم</div>
      </div>
      <div class="char-spot" data-char="white">
        <div class="char-avatar char-white">
          <div class="char-face">
            <div class="eyes">
              <div class="eye left-eye"></div>
              <div class="eye right-eye"></div>
            </div>
            <div class="mouth"></div>
            <div class="blush"></div>
          </div>
        </div>
        <div class="char-name">لطيفة</div>
      </div>
    `;
    
    const target = document.querySelector('.mind-status') || document.body;
    target.insertBefore(container, target.firstChild);
    
    // أنماط الشخصيات
    this.injectStyles();
    
    // إضافة مستمعي اللمس
    document.querySelectorAll('.char-spot').forEach(spot => {
      spot.addEventListener('click', (e) => {
        e.stopPropagation();
        const charId = spot.dataset.char;
        this.handleCharacterTap(charId);
      });
    });
  },
  
  injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
      #living-chars {
        display: flex;
        gap: 12px;
        background: rgba(10,10,15,0.6);
        backdrop-filter: blur(8px);
        padding: 6px 16px;
        border-radius: 60px;
        position: absolute;
        top: 8px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 100;
        border: 1px solid rgba(255,255,255,0.1);
      }
      
      .char-spot {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        transition: transform 0.1s ease;
      }
      .char-spot:active { transform: scale(0.95); }
      
      .char-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
      }
      .char-pink { background: radial-gradient(circle at 30% 30%, #ff99cc, #ff66aa); }
      .char-green { background: radial-gradient(circle at 30% 30%, #88ff88, #44cc44); }
      .char-white { background: radial-gradient(circle at 30% 30%, #ffffff, #ccccdd); }
      
      .char-face {
        position: relative;
        width: 32px;
        height: 32px;
      }
      .eyes {
        display: flex;
        gap: 8px;
        justify-content: center;
        position: absolute;
        top: 8px;
        left: 4px;
      }
      .eye {
        width: 6px;
        height: 6px;
        background: #1a1a2e;
        border-radius: 50%;
        transition: all 0.15s ease;
      }
      .mouth {
        width: 12px;
        height: 6px;
        background: #3d2a1f;
        border-radius: 0 0 8px 8px;
        position: absolute;
        bottom: 6px;
        left: 10px;
        transition: all 0.15s ease;
      }
      .blush {
        width: 8px;
        height: 4px;
        background: #ffaaaa;
        border-radius: 50%;
        position: absolute;
        bottom: 10px;
        opacity: 0;
        transition: opacity 0.2s;
      }
      .char-spot[data-char="pink"] .blush { left: 2px; background: #ff8888; }
      .char-spot[data-char="green"] .blush { right: 2px; background: #ffaaaa; }
      .char-spot[data-char="white"] .blush { left: 22px; background: #ffcccc; }
      
      /* حالات الوجه */
      .char-spot[data-mood="happy"] .mouth { border-radius: 50%; transform: scaleY(-1); height: 8px; }
      .char-spot[data-mood="sad"] .mouth { border-radius: 50%; background: #8866aa; transform: scaleY(0.6); }
      .char-spot[data-mood="surprised"] .mouth { width: 8px; height: 8px; border-radius: 50%; background: #553322; }
      .char-spot[data-mood="annoyed"] .eye { transform: scaleX(0.7); }
      .char-spot[data-mood="shy"] .blush { opacity: 1; }
      .char-spot[data-mood="shy"] .eye { transform: translateX(2px); }
      
      .char-name {
        font-size: 10px;
        color: #aaa;
        font-weight: 500;
      }
      
      /* شخصية مخفية */
      .char-spot[data-hidden="true"] {
        opacity: 0;
        pointer-events: none;
        transform: scale(0);
        transition: all 0.3s;
      }
    `;
    document.head.appendChild(style);
  },
  
  setMood(charId, mood) {
    if (!this.chars[charId] || this.chars[charId].hidden) return;
    this.chars[charId].mood = mood;
    const spot = document.querySelector(`.char-spot[data-char="${charId}"]`);
    if (spot) {
      spot.setAttribute('data-mood', mood);
      // تحديث شكل الفم والعينين حسب المود
      const mouth = spot.querySelector('.mouth');
      const eyes = spot.querySelectorAll('.eye');
      switch(mood) {
        case 'happy':
          mouth.style.borderRadius = '50%';
          mouth.style.transform = 'scaleY(-1)';
          break;
        case 'sad':
          mouth.style.borderRadius = '50%';
          mouth.style.transform = 'scaleY(0.6)';
          break;
        case 'surprised':
          mouth.style.width = '8px';
          mouth.style.height = '8px';
          mouth.style.borderRadius = '50%';
          break;
        case 'annoyed':
          eyes.forEach(e => e.style.transform = 'scaleX(0.7)');
          break;
        default:
          mouth.style.cssText = '';
          eyes.forEach(e => e.style.cssText = '');
      }
    }
  },
  
  setAllMoods(mood) {
    Object.keys(this.chars).forEach(c => this.setMood(c, mood));
  },
  
  async handleCharacterTap(charId) {
    const char = this.chars[charId];
    if (char.hidden) return;
    
    this.playSound('tap');
    
    // انزعاج الشخصية المقروصة
    this.setMood(charId, 'annoyed');
    setTimeout(() => this.setMood(charId, char.mood === 'annoyed' ? 'idle' : char.mood), 800);
    
    // الآخرون يضحكون
    const others = Object.keys(this.chars).filter(c => c !== charId);
    others.forEach(c => {
      this.setMood(c, 'happy');
      setTimeout(() => this.setMood(c, this.chars[c].mood), 1200);
    });
    
    // إذا تكرر اللمس (نقرتان سريعتان)
    if (this.lastTap === charId && Date.now() - this.tapTime < 500) {
      this.hideCharacter(charId, 8000);
      this.playSound('hide');
    }
    this.lastTap = charId;
    this.tapTime = Date.now();
  },
  
  hideCharacter(charId, durationMs) {
    const char = this.chars[charId];
    if (char.hidden) return;
    char.hidden = true;
    char.hideUntil = Date.now() + durationMs;
    const spot = document.querySelector(`.char-spot[data-char="${charId}"]`);
    if (spot) spot.setAttribute('data-hidden', 'true');
    
    setTimeout(() => {
      if (Date.now() >= char.hideUntil) {
        char.hidden = false;
        if (spot) spot.removeAttribute('data-hidden');
      }
    }, durationMs);
  },
  
  // التفاعل مع الكتابة
  onTyping(isTyping) {
    if (isTyping) {
      Object.keys(this.chars).forEach(c => {
        if (!this.chars[c].hidden) {
          // النظر إلى الأسفل
          const spot = document.querySelector(`.char-spot[data-char="${c}"]`);
          if (spot) {
            spot.querySelectorAll('.eye').forEach(eye => eye.style.transform = 'translateY(2px)');
          }
        }
      });
    } else {
      Object.keys(this.chars).forEach(c => {
        const spot = document.querySelector(`.char-spot[data-char="${c}"]`);
        if (spot) {
          spot.querySelectorAll('.eye').forEach(eye => eye.style.transform = '');
        }
      });
    }
  },
  
  // التفاعل مع الإرسال
  onSend() {
    Object.keys(this.chars).forEach(c => {
      if (!this.chars[c].hidden) {
        this.setMood(c, 'surprised');
        setTimeout(() => this.setMood(c, 'happy'), 600);
      }
    });
    this.playSound('send');
  },
  
  // تحليل المشاعر من النص وتغيير تعابير الشخصيات
  analyzeAndReact(text) {
    const lower = text.toLowerCase();
    if (lower.includes('خجل') || lower.includes('خجولة')) {
      this.setAllMoods('shy');
      this.playSound('shy');
      setTimeout(() => this.setAllMoods('idle'), 2000);
    } else if (lower.includes('حزين') || lower.includes('بكي')) {
      this.setAllMoods('sad');
      this.playSound('sad');
    } else if (lower.includes('سعيد') || lower.includes('فرح')) {
      this.setAllMoods('happy');
      this.playSound('happy');
    } else if (lower.includes('غضب') || lower.includes('مزعج')) {
      this.setAllMoods('annoyed');
      this.playSound('annoyed');
    }
    // بعد 3 ثوانٍ ارجع إلى idle
    setTimeout(() => this.setAllMoods('idle'), 3000);
  },
  
  // المؤثرات الصوتية (ناعمة)
  initAudio() {
    if (!window.AudioContext && !window.webkitAudioContext) return;
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
  },
  
  playSound(type) {
    if (!this.audioEnabled || !this.audioContext) return;
    // نستخدم Oscillator لنبضات خفيفة
    const osc = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();
    osc.connect(gain);
    gain.connect(this.audioContext.destination);
    gain.gain.value = 0.1;
    
    switch(type) {
      case 'tap': osc.frequency.value = 800; gain.gain.exponentialRampToValueAtTime(0.00001, 0.3); break;
      case 'send': osc.frequency.value = 1200; gain.gain.exponentialRampToValueAtTime(0.00001, 0.4); break;
      case 'shy': osc.frequency.value = 600; gain.gain.exponentialRampToValueAtTime(0.00001, 0.5); break;
      default: osc.frequency.value = 440;
    }
    osc.start();
    osc.stop(0.3);
  },
  
  startIdleAnimation() {
    setInterval(() => {
      Object.keys(this.chars).forEach(c => {
        if (!this.chars[c].hidden && this.chars[c].mood === 'idle') {
          // رمش العينين كل 3 ثوانٍ
          const spot = document.querySelector(`.char-spot[data-char="${c}"]`);
          if (spot) {
            const eyes = spot.querySelectorAll('.eye');
            eyes.forEach(e => e.style.transform = 'scaleY(0.1)');
            setTimeout(() => eyes.forEach(e => e.style.transform = ''), 150);
          }
        }
      });
    }, 3000);
  }
};

// ربط الأحداث مع التطبيق الرئيسي
document.addEventListener('DOMContentLoaded', () => {
  SkyCharacters.init();
  
  // ربط بالكتابة
  const textarea = document.getElementById('user-input');
  if (textarea) {
    textarea.addEventListener('focus', () => SkyCharacters.onTyping(true));
    textarea.addEventListener('blur', () => SkyCharacters.onTyping(false));
    textarea.addEventListener('input', () => SkyCharacters.onTyping(true));
  }
  
  // ربط بالإرسال
  const sendBtn = document.getElementById('send-btn');
  if (sendBtn) sendBtn.addEventListener('click', () => SkyCharacters.onSend());
  
  // استماع لأحداث الرسائل لتحليل المشاعر
  window.addEventListener('new-message', (e) => {
    if (e.detail.role === 'user') SkyCharacters.analyzeAndReact(e.detail.content);
  });
});

window.SkyCharacters = SkyCharacters;
