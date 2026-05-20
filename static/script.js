/* =============================================
   سماء - المحرك الإدراكي وخوارزميات المعالجة v7.5
============================================= */

// 1. نظام جزيئات الشبكة العصبية السائلة بالخلفية (Interactive Canvas)
const canvas = document.getElementById('neural-net-fluid');
const ctx = canvas.getContext('2d');
let nodes = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

class NeuralNode {
  constructor() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.radius = Math.random() * 2 + 0.5;
  }
  update(touchX, touchY) {
    this.x += this.vx;
    this.y += this.vy;

    if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
    if (this.y < 0 || this.y > canvas.height) this.vy *= -1;

    // التفاعل الحركي عند لمس الشاشة بالجوال
    if (touchX && touchY) {
      let dist = Math.hypot(touchX - this.x, touchY - this.y);
      if (dist < 100) {
        this.x += (touchX - this.x) * 0.02;
        this.y += (touchY - this.y) * 0.02;
      }
    }
  }
  draw() {
    ctx.fillStyle = 'rgba(147, 51, 234, 0.25)';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fill();
  }
}

const totalNodes = 35;
for (let i = 0; i < totalNodes; i++) nodes.push(new NeuralNode());

let currentTouch = { x: null, y: null };
window.addEventListener('pointermove', (e) => { currentTouch.x = e.clientX; currentTouch.y = e.clientY; });
window.addEventListener('pointerleave', () => { currentTouch.x = null; currentTouch.y = null; });

function renderNeuralCore() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  nodes.forEach(node => {
    node.update(currentTouch.x, currentTouch.y);
    node.draw();
  });
  requestAnimationFrame(renderNeuralCore);
}
renderNeuralCore();


// 2. إدارة محرك الواجهة الذكية وعمليات المعالجة
class SkyCognitiveEngine {
  constructor() {
    // ربط العناصر البرمجية بالهيكل
    this.container = document.getElementById('messages-container');
    this.input = document.getElementById('core-message-input');
    this.sendBtn = document.getElementById('execute-send-btn');
    this.indicator = document.getElementById('neural-thinking-indicator');
    this.clearBtn = document.getElementById('clear-session-btn');
    this.attachBtn = document.getElementById('trigger-attach-btn');
    this.fileInput = document.getElementById('system-file-input');
    this.previewArea = document.getElementById('attachment-preview-area');
    this.viewport = document.getElementById('viewport-stream');
    
    this.sidebar = document.getElementById('sidebar-archive');
    this.menuToggle = document.getElementById('menu-toggle-btn');
    this.closeSidebarBtn = document.getElementById('close-archive-btn');
    this.sidebarNewChatBtn = document.getElementById('new-chat-sidebar-btn');
    this.archiveContainer = document.getElementById('archive-sessions-container');

    // تهيئة الجلسة الحالية وإعداد الذاكرة المحلية
    this.sessionId = localStorage.getItem('sky_active_session') || this.generateNewSessionID();
    this.pendingFiles = [];

    // إعداد واجهة الماركدوان المتقدمة
    if (typeof marked !== 'undefined') {
      marked.setOptions({
        highlight: function(code, lang) {
          if (Prism.languages[lang]) {
            return Prism.highlight(code, Prism.languages[lang], lang);
          }
          return code;
        }
      });
    }

    this.registerEngineEvents();
  }

  generateNewSessionID() {
    const id = 'sky-sess-' + Date.now();
    localStorage.setItem('sky_active_session', id);
    this.saveSessionToArchiveRegistry(id);
    return id;
  }

  registerEngineEvents() {
    this.sendBtn.addEventListener('click', () => this.processUserOutbound());
    
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.processUserOutbound();
      }
    });

    // تكيف حقل الإدخال المطاطي ديناميكياً مع السطور الجديدة على الجوال
    this.input.addEventListener('input', () => {
      this.input.style.height = '38px';
      this.input.style.height = Math.min(this.input.scrollHeight, 110) + 'px';
    });

    this.clearBtn.addEventListener('click', () => this.triggerMemoryWipe());
    this.sidebarNewChatBtn.addEventListener('click', () => this.triggerMemoryWipe());
    this.attachBtn.addEventListener('click', () => this.fileInput.click());
    this.fileInput.addEventListener('change', () => this.handleFileQueue());

    // أحداث درج الأرشفة والذاكرة
    this.menuToggle.addEventListener('click', () => this.sidebar.classList.toggle('active'));
    this.closeSidebarBtn.addEventListener('click', () => this.sidebar.classList.remove('active'));

    // مراقبة سكرول الشاشة للتحكم بالأسهم العائمة
    this.viewport.addEventListener('scroll', () => this.manageScrollNavigationVisibility());

    this.loadActiveSessionHistory();
    this.renderArchiveList();
  }

  async processUserOutbound() {
    const text = this.input.value.trim();
    if (!text && this.pendingFiles.length === 0) return;

    // 1. عرض نص المستخدم فوراً إن وُجد
    if (text) {
      this.appendMessageBubble(text, 'user');
    }
    this.input.value = '';
    this.input.style.height = '38px';

    // 2. معالجة وإرسال المرفقات المعلقة أولاً
    for (let file of this.pendingFiles) {
      await this.uploadFileToServer(file);
    }
    this.pendingFiles = [];
    this.previewArea.innerHTML = '';

    if (!text) return;

    // 3. إظهار مؤشر التفكير وبدء طلب المعالجة من الخادم
    this.setThinkingState(true);

    try {
      const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: this.sessionId })
      });
      const data = await response.json();
      this.setThinkingState(false);
      
      if (data.reply) {
        this.appendMessageBubble(data.reply, 'assistant', true);
      }
    } catch (err) {
      this.setThinkingState(false);
      this.appendMessageBubble('لم نتمكن من الوصول لمركز المعالجة السحابي، تأكد من اتصال خادم راندر.', 'assistant');
    }
  }

  async uploadFileToServer(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', this.sessionId);

    try {
      const res = await fetch('/upload', { method: 'POST', body: formData });
      const data = await res.json();
      if (data.reply) {
        this.appendMessageBubble(data.reply, 'assistant', true);
      }
    } catch {
      this.appendMessageBubble(`فشل معالجة المستند: ${file.name}`, 'assistant');
    }
  }

  handleFileQueue() {
    const files = Array.from(this.fileInput.files);
    this.pendingFiles = [...this.pendingFiles, ...files];
    this.previewArea.innerHTML = '';
    
    this.pendingFiles.forEach((file, index) => {
      const pill = document.createElement('div');
      pill.className = 'preview-pill';
      pill.innerHTML = `<span><i class="fas fa-file-invoice"></i> ${file.name.substring(0, 10)}...</span>
                        <button onclick="window.SkyEngineInstance.removeQueuedFile(${index})">×</button>`;
      this.previewArea.appendChild(pill);
    });
    this.fileInput.value = '';
  }

  removeQueuedFile(index) {
    this.pendingFiles.splice(index, 1);
    this.handleFileQueue();
  }

  // دالة بناء وضم فقاعات الرسائل وتحليل محتواها برمجياً وماركدوان
  appendMessageBubble(content, role, isStreaming = false) {
    const bubble = document.createElement('div');
    bubble.className = `msg ${role}`;
    this.container.appendChild(bubble);

    if (role === 'assistant') {
      // تحويل نصوص الماركدوان والأكواد البرمجية بالاعتماد على ميزات Marked.js العالمية
      let formattedHtml = content;
      if (typeof marked !== 'undefined') {
        formattedHtml = marked.parse(content);
      } else {
        formattedHtml = content.replace(/\n/g, '<br>');
      }

      if (isStreaming) {
        // تأثير الكتابة الانسيابية المتدرجة للذكاء الاصطناعي
        bubble.innerHTML = '';
        let tempDiv = document.createElement('div');
        tempDiv.innerHTML = formattedHtml;
        
        // إعادة معالجة الأكواد وتنظيمها داخل صناديق فخمة قابلة للنسخ
        this.wrapAndRefineCodeBlocks(tempDiv);

        bubble.innerHTML = tempDiv.innerHTML;
        if (typeof Prism !== 'undefined') Prism.highlightAllUnder(bubble);
      } else {
        let tempDiv = document.createElement('div');
        tempDiv.innerHTML = formattedHtml;
        this.wrapAndRefineCodeBlocks(tempDiv);
        bubble.innerHTML = tempDiv.innerHTML;
        if (typeof Prism !== 'undefined') Prism.highlightAllUnder(bubble);
      }
    } else {
      bubble.innerText = content;
    }

    this.saveMessageToLocalStorage(content, role);
    this.scrollViewportToBottom();
  }

  // هندسة صناديق الأكواد البرمجية الفخمة وزر النسخ الاحترافي
  wrapAndRefineCodeBlocks(parentElement) {
    const preElements = parentElement.querySelectorAll('pre');
    preElements.forEach(pre => {
      const codeEl = pre.querySelector('code');
      let lang = 'code';
      if (codeEl) {
        const classList = codeEl.className.split(' ');
        const langClass = classList.find(c => c.startsWith('language-'));
        if (langClass) lang = langClass.replace('language-', '');
      }

      const wrapper = document.createElement('div');
      wrapper.className = 'code-wrapper';
      
      const header = document.createElement('div');
      header.className = 'code-header';
      header.innerHTML = `<span>${lang.toUpperCase()}</span>
                          <button class="copy-code-btn" onclick="window.SkyEngineInstance.copyCodeSnippet(this)"><i class="far fa-copy"></i> نسخ الكود</button>`;
      
      wrapper.appendChild(header);
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
    });
  }

  copyCodeSnippet(buttonElement) {
    const pre = buttonElement.closest('.code-wrapper').querySelector('pre');
    if (pre) {
      navigator.clipboard.writeText(pre.innerText).then(() => {
        buttonElement.innerHTML = '<i class="fas fa-check" style="color:#10b981"></i> تم النسخ!';
        setTimeout(() => {
          buttonElement.innerHTML = '<i class="far fa-copy"></i> نسخ الكود';
        }, 2000);
      });
    }
  }

  setThinkingState(isActive) {
    this.indicator.classList.toggle('hidden', !isActive);
    this.scrollViewportToBottom();
  }

  scrollViewportToBottom() {
    this.viewport.scrollTop = this.viewport.scrollHeight;
  }

  manageScrollNavigationVisibility() {
    const navigatorBox = document.getElementById('scroll-navigator');
    if (this.viewport.scrollTop > 250) {
      navigatorBox.classList.add('visible');
    } else {
      navigatorBox.classList.remove('visible');
    }
  }

  saveMessageToLocalStorage(content, role) {
    let history = JSON.parse(localStorage.getItem(`sky_data_${this.sessionId}`)) || [];
    // منع تكرار حفظ الرسائل عند إعادة التحميل
    if (history.length > 0 && history[history.length - 1].content === content && history[history.length - 1].role === role) {
      return;
    }
    history.push({ content, role });
    localStorage.setItem(`sky_data_${this.sessionId}`, JSON.stringify(history));
  }

  loadActiveSessionHistory() {
    this.container.innerHTML = '';
    let history = JSON.parse(localStorage.getItem(`sky_data_${this.sessionId}`)) || [];
    
    if (history.length === 0) {
      this.appendMessageBubble('مرحباً بك في فضائي الإدراكي الجديد. أنا سماء، بوابتك لتطوير واجهات وأفكار جبارة خالية من الأخطاء العشوائية. بمَ نبدأ هندسته اليوم؟ ⚡', 'assistant');
    } else {
      history.forEach(msg => {
        this.appendMessageBubble(msg.content, msg.role, false);
      });
      this.scrollViewportToBottom();
    }
  }

  saveSessionToArchiveRegistry(id) {
    let registry = JSON.parse(localStorage.getItem('sky_archive_registry')) || [];
    if (!registry.includes(id)) {
      registry.push(id);
      localStorage.setItem('sky_archive_registry', JSON.stringify(registry));
    }
  }

  renderArchiveList() {
    this.archiveContainer.innerHTML = '';
    let registry = JSON.parse(localStorage.getItem('sky_archive_registry')) || [];
    
    // تصفية الجلسات لإظهار المحادثات القديمة فقط في شريط الأرشيف السهمي
    const historicalSessions = registry.filter(sid => sid !== this.sessionId);

    if (historicalSessions.length === 0) {
      this.archiveContainer.innerHTML = '<div style="font-size:0.8rem; color:#64748b; text-align:center; padding:20px 0;">الأرشيف فارغ حالياً.</div>';
      return;
    }

    historicalSessions.forEach((sid, index) => {
      const item = document.createElement('div');
      item.className = 'archive-item';
      item.innerText = `جلسة معالجة مؤرشفة #${index + 1}`;
      item.addEventListener('click', () => {
        this.sessionId = sid;
        localStorage.setItem('sky_active_session', sid);
        this.loadActiveSessionHistory();
        this.sidebar.classList.remove('active');
      });
      this.archiveContainer.appendChild(item);
    });
  }

  triggerMemoryWipe() {
    if (!confirm('هل تود نقل الجلسة الحالية بشكل آمن إلى أرشيف الذاكرة وفتح جلسة نقية جديدة؟')) return;
    this.sessionId = this.generateNewSessionID();
    this.loadActiveSessionHistory();
    this.renderArchiveList();
    this.sidebar.classList.remove('active');
  }
}

// دالة التحكم في أزرار التنقل السريع العائمة لأعلى وأسفل الواجهة
function executeQuickScroll(direction) {
  const view = document.getElementById('viewport-stream');
  if (direction === 'top') {
    view.scrollTo({ top: 0, behavior: 'smooth' });
  } else {
    view.scrollTo({ top: view.scrollHeight, behavior: 'smooth' });
  }
}

// تشغيل النظام عند اكتمال تحميل الواجهة والخطوط
document.addEventListener('DOMContentLoaded', () => {
  window.SkyEngineInstance = new SkyCognitiveEngine();
});
