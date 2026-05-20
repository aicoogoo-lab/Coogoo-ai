/* ============================================================
   سماء - الواجهة الذكية الحية العالمية
   نظام التشغيل الكامل والذكاء الاصطناعي v3.0
   ~1800 سطر من الكود الاحترافي المنظم
   شامل: أرشفة، ذكاء، وعي بالاتصال، تفاعلات حية، وكل التفاصيل
============================================================ */

// وضع الحماية (Strict Mode)
'use strict';

/* --------------------------------------------
   انتظار تحميل DOM بالكامل
-------------------------------------------- */
document.addEventListener('DOMContentLoaded', async () => {
  
  /* --------------------------------------------
     المتغيرات العامة والنظام الأساسي
  -------------------------------------------- */
  const App = {
    // حالة التطبيق
    state: {
      isOnline: navigator.onLine,
      isThinking: false,
      focusMode: false,
      currentConversationId: null,
      conversations: [],
      currentMessages: [],
      typingTimeout: null,
      scrollTimeout: null,
      connectionRetryCount: 0,
      unreadMessages: 0,
      lastScrollTop: 0,
      searchResults: [],
      currentSearchIndex: 0,
      suggestedResponses: [],
      emotion: 'neutral',
      latency: 0,
      lastPing: null
    },
    
    // إعدادات التطبيق
    config: {
      apiEndpoint: '/ask',
      uploadEndpoint: '/upload',
      healthEndpoint: '/health',
      maxRetries: 3,
      retryDelay: 2000,
      typingDelay: 800,
      pingInterval: 30000,
      maxFileSize: 10 * 1024 * 1024, // 10MB
      allowedFileTypes: ['image/*', 'application/pdf', 'text/*', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
      autoSaveInterval: 5000,
      maxConversations: 100,
      maxMessageLength: 4000
    },
    
    // عناصر DOM
    elements: {
      // رئيسية
      app: null,
      bgCanvas: null,
      messagesContainer: null,
      messagesWrapper: null,
      messageInput: null,
      sendBtn: null,
      
      // أزرار
      menuBtn: null,
      searchBtn: null,
      focusModeBtn: null,
      themeToggle: null,
      attachBtn: null,
      fileInput: null,
      scrollUpBtn: null,
      scrollDownBtn: null,
      
      // الأرشيف
      sidebar: null,
      conversationsList: null,
      archiveSearch: null,
      newConversationBtn: null,
      clearAllBtn: null,
      exportAllBtn: null,
      closeSidebarBtn: null,
      
      // حالة
      connectionStatus: null,
      statusText: null,
      latencyDisplay: null,
      
      // مؤشرات
      typingContainer: null,
      typingEmotion: null,
      charCount: null,
      wordCount: null,
      newMessagesBadge: null,
      
      // نافذة البحث
      searchModal: null,
      searchInChat: null,
      searchResultsContainer: null,
      searchPrevBtn: null,
      searchNextBtn: null,
      
      // نافذة الإعدادات
      settingsModal: null,
      convNameInput: null,
      renameConvBtn: null,
      deleteCurrentConvBtn: null,
      exportTxtBtn: null,
      exportJsonBtn: null,
      exportHtmlBtn: null,
      
      // الأفاتار
      avatarCore: null,
      avatarMouth: null,
      
      // معاينة الملفات
      filePreviewArea: null,
      
      // Toast
      toastContainer: null
    }
  };
  
  /* --------------------------------------------
     تهيئة العناصر
  -------------------------------------------- */
  function initElements() {
    App.elements.app = document.getElementById('app');
    App.elements.bgCanvas = document.getElementById('bg-canvas');
    App.elements.messagesContainer = document.getElementById('messagesContainer');
    App.elements.messagesWrapper = document.getElementById('messagesWrapper');
    App.elements.messageInput = document.getElementById('messageInput');
    App.elements.sendBtn = document.getElementById('sendMessageBtn');
    
    App.elements.menuBtn = document.getElementById('menuBtn');
    App.elements.searchBtn = document.getElementById('searchBtn');
    App.elements.focusModeBtn = document.getElementById('focusModeBtn');
    App.elements.themeToggle = document.getElementById('themeToggle');
    App.elements.attachBtn = document.getElementById('attachFileBtn');
    App.elements.fileInput = document.getElementById('fileInput');
    App.elements.scrollUpBtn = document.getElementById('scrollToTopBtn');
    App.elements.scrollDownBtn = document.getElementById('scrollToBottomBtn');
    
    App.elements.sidebar = document.getElementById('sidebar');
    App.elements.conversationsList = document.getElementById('conversationsList');
    App.elements.archiveSearch = document.getElementById('archiveSearch');
    App.elements.newConversationBtn = document.getElementById('newConversationBtn');
    App.elements.clearAllBtn = document.getElementById('clearAllConversationsBtn');
    App.elements.exportAllBtn = document.getElementById('exportAllBtn');
    App.elements.closeSidebarBtn = document.getElementById('closeSidebarBtn');
    
    App.elements.connectionStatus = document.getElementById('connectionStatus');
    App.elements.statusText = document.getElementById('statusText');
    App.elements.latencyDisplay = document.getElementById('latencyDisplay');
    
    App.elements.typingContainer = document.getElementById('typingContainer');
    App.elements.typingEmotion = document.getElementById('typingEmotion');
    App.elements.charCount = document.getElementById('charCount');
    App.elements.wordCount = document.getElementById('wordCount');
    App.elements.newMessagesBadge = document.getElementById('newMessagesBadge');
    
    App.elements.searchModal = document.getElementById('searchModal');
    App.elements.searchInChat = document.getElementById('searchInChat');
    App.elements.searchResultsContainer = document.getElementById('searchResults');
    App.elements.searchPrevBtn = document.getElementById('searchPrev');
    App.elements.searchNextBtn = document.getElementById('searchNext');
    
    App.elements.settingsModal = document.getElementById('settingsModal');
    App.elements.convNameInput = document.getElementById('convNameInput');
    App.elements.renameConvBtn = document.getElementById('renameConvBtn');
    App.elements.deleteCurrentConvBtn = document.getElementById('deleteCurrentConvBtn');
    App.elements.exportTxtBtn = document.getElementById('exportTxtBtn');
    App.elements.exportJsonBtn = document.getElementById('exportJsonBtn');
    App.elements.exportHtmlBtn = document.getElementById('exportHtmlBtn');
    
    App.elements.avatarCore = document.querySelector('.avatar-core');
    App.elements.avatarMouth = document.getElementById('avatarMouth');
    App.elements.filePreviewArea = document.getElementById('filePreviewArea');
    App.elements.toastContainer = document.getElementById('toastContainer');
  }
  
  /* --------------------------------------------
     نظام الإشعارات (Toast)
  -------------------------------------------- */
  function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const iconMap = {
      success: 'fa-check-circle',
      error: 'fa-exclamation-circle',
      warning: 'fa-exclamation-triangle',
      info: 'fa-info-circle'
    };
    toast.innerHTML = `
      <i class="fas ${iconMap[type] || 'fa-info-circle'}"></i>
      <span>${message}</span>
    `;
    App.elements.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, duration);
  }
  
  /* --------------------------------------------
     نظام الأرشفة - حفظ واسترجاع المحادثات
  -------------------------------------------- */
  const ArchiveSystem = {
    // حفظ المحادثات
    saveConversations() {
      try {
        localStorage.setItem('sky_conversations_v3', JSON.stringify(App.state.conversations));
        localStorage.setItem('sky_current_conv_v3', App.state.currentConversationId);
      } catch (e) {
        console.error('فشل حفظ المحادثات:', e);
        showToast('فشل حفظ المحادثات', 'error');
      }
    },
    
    // تحميل المحادثات
    loadConversations() {
      try {
        const saved = localStorage.getItem('sky_conversations_v3');
        if (saved) {
          App.state.conversations = JSON.parse(saved);
        }
        const currentId = localStorage.getItem('sky_current_conv_v3');
        if (currentId && App.state.conversations.find(c => c.id === currentId)) {
          App.state.currentConversationId = currentId;
        }
      } catch (e) {
        console.error('فشل تحميل المحادثات:', e);
        App.state.conversations = [];
      }
      
      if (App.state.conversations.length === 0) {
        this.newConversation();
      }
    },
    
    // إنشاء محادثة جديدة
    newConversation() {
      const newId = 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 8);
      const newConversation = {
        id: newId,
        title: 'محادثة جديدة',
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now(),
        pinned: false,
        archived: false,
        tags: []
      };
      App.state.conversations.unshift(newConversation);
      App.state.currentConversationId = newId;
      App.state.currentMessages = [];
      this.saveConversations();
      this.renderConversationsList();
      this.renderMessages();
      
      // رسالة ترحيب
      setTimeout(() => {
        this.addMessage('assistant', 'مرحباً بك في سماء 🌙\n\nأنا هنا لمساعدتك. اسألني عن أي شيء! ✨');
      }, 300);
      
      showToast('محادثة جديدة تم إنشاؤها', 'success');
    },
    
    // تحميل محادثة
    loadConversation(convId) {
      const conversation = App.state.conversations.find(c => c.id === convId);
      if (!conversation) return;
      
      App.state.currentConversationId = convId;
      App.state.currentMessages = [...conversation.messages];
      this.saveConversations();
      this.renderMessages();
      this.renderConversationsList();
      this.scrollToBottom();
      
      showToast(`تم فتح: ${conversation.title}`, 'info');
    },
    
    // إضافة رسالة
    addMessage(sender, content, timestamp = Date.now()) {
      const message = {
        id: 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
        sender: sender,
        content: content,
        timestamp: timestamp,
        edited: false,
        reactions: []
      };
      App.state.currentMessages.push(message);
      
      // تحديث المحادثة في الأرشيف
      const convIndex = App.state.conversations.findIndex(c => c.id === App.state.currentConversationId);
      if (convIndex !== -1) {
        App.state.conversations[convIndex].messages = [...App.state.currentMessages];
        App.state.conversations[convIndex].updatedAt = Date.now();
        
        // تحديث العنوان تلقائياً
        if (App.state.conversations[convIndex].title === 'محادثة جديدة' && sender === 'user') {
          const shortTitle = content.length > 30 ? content.substring(0, 30) + '...' : content;
          App.state.conversations[convIndex].title = shortTitle;
        }
      }
      
      this.saveConversations();
      this.renderMessages();
      this.renderConversationsList();
      
      return message;
    },
    
    // حذف محادثة
    deleteConversation(convId) {
      if (App.state.conversations.length === 1) {
        showToast('لا يمكن حذف آخر محادثة', 'warning');
        return;
      }
      
      const index = App.state.conversations.findIndex(c => c.id === convId);
      if (index !== -1) {
        App.state.conversations.splice(index, 1);
        
        if (App.state.currentConversationId === convId) {
          App.state.currentConversationId = App.state.conversations[0].id;
          App.state.currentMessages = [...App.state.conversations[0].messages];
        }
        
        this.saveConversations();
        this.renderConversationsList();
        this.renderMessages();
        showToast('تم حذف المحادثة', 'success');
      }
    },
    
    // حذف كل المحادثات
    deleteAllConversations() {
      if (confirm('⚠️ تحذير: سيتم حذف جميع المحادثات نهائياً. هل أنت متأكد؟')) {
        const firstId = App.state.conversations[0].id;
        App.state.conversations = [App.state.conversations[0]];
        App.state.currentConversationId = firstId;
        App.state.currentMessages = [...App.state.conversations[0].messages];
        this.saveConversations();
        this.renderConversationsList();
        this.renderMessages();
        showToast('تم حذف جميع المحادثات', 'success');
      }
    },
    
    // إعادة تسمية محادثة
    renameConversation(convId, newTitle) {
      const conv = App.state.conversations.find(c => c.id === convId);
      if (conv && newTitle.trim()) {
        conv.title = newTitle.trim().substring(0, 50);
        this.saveConversations();
        this.renderConversationsList();
        showToast('تم تغيير الاسم', 'success');
      }
    },
    
    // تصدير المحادثة الحالية
    exportCurrentConversation(format) {
      const conv = App.state.conversations.find(c => c.id === App.state.currentConversationId);
      if (!conv) return;
      
      let content = '';
      const filename = `سماء_${conv.title}_${new Date().toISOString().slice(0, 19)}`;
      
      switch(format) {
        case 'txt':
          content = `محادثة: ${conv.title}\nالتاريخ: ${new Date(conv.createdAt).toLocaleString('ar')}\n${'='.repeat(50)}\n\n`;
          conv.messages.forEach(msg => {
            const sender = msg.sender === 'user' ? '👤 أنت' : '🌙 سماء';
            content += `[${new Date(msg.timestamp).toLocaleTimeString('ar')}] ${sender}:\n${msg.content}\n\n`;
          });
          this.downloadFile(content, `${filename}.txt`, 'text/plain');
          break;
          
        case 'json':
          content = JSON.stringify(conv, null, 2);
          this.downloadFile(content, `${filename}.json`, 'application/json');
          break;
          
        case 'html':
          content = this.generateHtmlExport(conv);
          this.downloadFile(content, `${filename}.html`, 'text/html');
          break;
      }
      
      showToast(`تم تصدير المحادثة كـ ${format.toUpperCase()}`, 'success');
    },
    
    generateHtmlExport(conv) {
      let messagesHtml = '';
      conv.messages.forEach(msg => {
        const align = msg.sender === 'user' ? 'right' : 'left';
        const bg = msg.sender === 'user' ? 'linear-gradient(135deg, #6366f1, #c026d3)' : '#1e1e3e';
        const color = msg.sender === 'user' ? 'white' : '#f1f5f9';
        messagesHtml += `
          <div style="text-align: ${align}; margin: 16px 0;">
            <div style="display: inline-block; max-width: 80%; background: ${bg}; color: ${color}; padding: 12px 18px; border-radius: 20px; ${msg.sender === 'user' ? 'border-bottom-right-radius: 4px;' : 'border-bottom-left-radius: 4px;'}">
              ${msg.content.replace(/\n/g, '<br>')}
            </div>
            <div style="font-size: 11px; color: #666; margin-top: 4px;">${new Date(msg.timestamp).toLocaleString('ar')}</div>
          </div>
        `;
      });
      
      return `<!DOCTYPE html>
      <html dir="rtl" lang="ar">
      <head><meta charset="UTF-8"><title>سماء - ${conv.title}</title>
      <style>body{font-family:'Cairo',sans-serif;background:#0a0a1a;color:#f1f5f9;padding:20px;margin:0;}</style>
      </head><body><h1>🌙 سماء</h1><h3>${conv.title}</h3><p>التاريخ: ${new Date(conv.createdAt).toLocaleString('ar')}</p><hr>${messagesHtml}</body></html>`;
    },
    
    downloadFile(content, filename, mimeType) {
      const blob = new Blob([content], { type: mimeType });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      link.click();
      URL.revokeObjectURL(link.href);
    },
    
    // عرض قائمة المحادثات
    renderConversationsList() {
      if (!App.elements.conversationsList) return;
      
      const searchTerm = App.elements.archiveSearch?.value.toLowerCase() || '';
      let filtered = [...App.state.conversations];
      
      if (searchTerm) {
        filtered = filtered.filter(c => 
          c.title.toLowerCase().includes(searchTerm) ||
          c.messages.some(m => m.content.toLowerCase().includes(searchTerm))
        );
      }
      
      filtered.sort((a, b) => {
        if (a.pinned !== b.pinned) return a.pinned ? -1 : 1;
        return b.updatedAt - a.updatedAt;
      });
      
      App.elements.conversationsList.innerHTML = filtered.map(conv => `
        <div class="conversation-item ${conv.id === App.state.currentConversationId ? 'active' : ''}" data-id="${conv.id}">
          <div class="conv-title">
            ${conv.pinned ? '<i class="fas fa-thumbtack" style="color:#f59e0b; margin-left:6px;"></i>' : ''}
            ${this.escapeHtml(conv.title)}
          </div>
          <div class="conv-meta">
            <span class="conv-date"><i class="far fa-clock"></i> ${this.formatDate(conv.updatedAt)}</span>
            <div class="conv-actions">
              <button class="conv-action-btn pin-btn" data-id="${conv.id}" title="${conv.pinned ? 'إلغاء التثبيت' : 'تثبيت'}"><i class="fas ${conv.pinned ? 'fa-thumbtack' : 'fa-thumbtack'}" style="transform: ${conv.pinned ? 'rotate(45deg)' : 'none'}"></i></button>
              <button class="conv-action-btn rename-btn" data-id="${conv.id}" title="إعادة تسمية"><i class="fas fa-edit"></i></button>
              <button class="conv-action-btn delete-btn" data-id="${conv.id}" title="حذف"><i class="fas fa-trash"></i></button>
            </div>
          </div>
        </div>
      `).join('');
      
      // إضافة المستمعين
      document.querySelectorAll('.conversation-item').forEach(el => {
        el.addEventListener('click', (e) => {
          if (!e.target.closest('.conv-actions')) {
            this.loadConversation(el.dataset.id);
            App.elements.sidebar?.classList.remove('open');
          }
        });
      });
      
      document.querySelectorAll('.pin-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const conv = App.state.conversations.find(c => c.id === btn.dataset.id);
          if (conv) {
            conv.pinned = !conv.pinned;
            this.saveConversations();
            this.renderConversationsList();
          }
        });
      });
      
      document.querySelectorAll('.rename-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const newTitle = prompt('الاسم الجديد للمحادثة:');
          if (newTitle) this.renameConversation(btn.dataset.id, newTitle);
        });
      });
      
      document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.deleteConversation(btn.dataset.id);
        });
      });
    },
    
    // عرض الرسائل
    renderMessages() {
      if (!App.elements.messagesWrapper) return;
      
      if (App.state.currentMessages.length === 0) {
        App.elements.messagesWrapper.innerHTML = `
          <div style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">
            <i class="fas fa-comment-dots" style="font-size: 48px; opacity: 0.5; margin-bottom: 16px; display: block;"></i>
            <p>لا توجد رسائل بعد</p>
            <p style="font-size: 0.85rem;">اكتب رسالتك الأولى لتبدأ المحادثة</p>
          </div>
        `;
        return;
      }
      
      App.elements.messagesWrapper.innerHTML = App.state.currentMessages.map(msg => `
        <div class="message ${msg.sender}" data-message-id="${msg.id}">
          <div class="message-bubble">
            ${this.formatMessageContent(msg.content)}
          </div>
          <div class="message-footer">
            <span class="message-time"><i class="far fa-clock"></i> ${new Date(msg.timestamp).toLocaleTimeString('ar', { hour: '2-digit', minute: '2-digit' })}</span>
            <div class="message-actions">
              <button class="message-action-btn copy-msg-btn" data-content="${this.escapeHtmlAttr(msg.content)}" title="نسخ"><i class="fas fa-copy"></i></button>
              ${msg.sender === 'assistant' ? `<button class="message-action-btn regenerate-btn" title="إعادة توليد"><i class="fas fa-rotate-right"></i></button>` : ''}
              <button class="message-action-btn delete-msg-btn" data-id="${msg.id}" title="حذف"><i class="fas fa-trash"></i></button>
            </div>
          </div>
        </div>
      `).join('');
      
      // إضافة مستمعي النسخ
      document.querySelectorAll('.copy-msg-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          navigator.clipboard.writeText(btn.dataset.content);
          showToast('تم نسخ الرسالة', 'success');
        });
      });
      
      // إضافة مستمعي إعادة التوليد
      document.querySelectorAll('.regenerate-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const lastUserMsg = [...App.state.currentMessages].reverse().find(m => m.sender === 'user');
          if (lastUserMsg) {
            this.regenerateResponse(lastUserMsg.content);
          }
        });
      });
      
      // إضافة مستمعي حذف الرسائل
      document.querySelectorAll('.delete-msg-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const msgId = btn.dataset.id;
          const index = App.state.currentMessages.findIndex(m => m.id === msgId);
          if (index !== -1) {
            App.state.currentMessages.splice(index, 1);
            const convIndex = App.state.conversations.findIndex(c => c.id === App.state.currentConversationId);
            if (convIndex !== -1) {
              App.state.conversations[convIndex].messages = [...App.state.currentMessages];
            }
            ArchiveSystem.saveConversations();
            ArchiveSystem.renderMessages();
            showToast('تم حذف الرسالة', 'info');
          }
        });
      });
    },
    
    formatMessageContent(content) {
      // تحويل Markdown بسيط
      let formatted = this.escapeHtml(content);
      formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
      formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
      formatted = formatted.replace(/\n/g, '<br>');
      formatted = formatted.replace(/https?:\/\/[^\s]+/g, '<a href="$&" target="_blank">$&</a>');
      return formatted;
    },
    
    escapeHtml(str) {
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    },
    
    escapeHtmlAttr(str) {
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    },
    
    formatDate(timestamp) {
      const date = new Date(timestamp);
      const now = new Date();
      const diff = now - date;
      
      if (diff < 60000) return 'الآن';
      if (diff < 3600000) return `${Math.floor(diff / 60000)} دقيقة`;
      if (diff < 86400000) return `${Math.floor(diff / 3600000)} ساعة`;
      if (diff < 604800000) return `${Math.floor(diff / 86400000)} يوم`;
      return date.toLocaleDateString('ar');
    },
    
    scrollToBottom() {
      if (App.elements.messagesContainer) {
        App.elements.messagesContainer.scrollTop = App.elements.messagesContainer.scrollHeight;
      }
    },
    
    async regenerateResponse(userMessage) {
      showToast('جاري إعادة التوليد...', 'info');
      await AIEngine.sendMessage(userMessage, true);
    }
  };
  
  /* --------------------------------------------
     محرك الذكاء الاصطناعي والاتصال
  -------------------------------------------- */
  const AIEngine = {
    // التحقق من حالة الاتصال
    async checkConnection() {
      try {
        const startTime = performance.now();
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        
        const response = await fetch(App.config.healthEndpoint, {
          method: 'HEAD',
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        const latency = Math.round(performance.now() - startTime);
        App.state.latency = latency;
        App.state.isOnline = response.ok;
        
        this.updateConnectionUI(response.ok, latency);
        return response.ok;
      } catch (error) {
        App.state.isOnline = false;
        this.updateConnectionUI(false, null);
        return false;
      }
    },
    
    updateConnectionUI(isOnline, latency) {
      if (!App.elements.connectionStatus) return;
      
      const statusDot = App.elements.connectionStatus.querySelector('.status-dot');
      if (statusDot) {
        statusDot.className = `status-dot ${isOnline ? 'online' : 'offline'}`;
      }
      
      if (App.elements.statusText) {
        App.elements.statusText.textContent = isOnline ? 'متصل' : 'غير متصل';
      }
      
      if (App.elements.latencyDisplay && latency) {
        App.elements.latencyDisplay.textContent = `${latency}ms`;
        App.elements.latencyDisplay.style.opacity = latency < 100 ? '0.5' : latency < 300 ? '0.8' : '1';
        App.elements.latencyDisplay.style.color = latency < 100 ? '#10b981' : latency < 300 ? '#f59e0b' : '#ef4444';
      }
      
      if (!isOnline) {
        showToast('انقطع الاتصال بالخادم. جاري إعادة المحاولة...', 'warning');
        this.startReconnection();
      }
    },
    
    startReconnection() {
      if (App.state.connectionRetryCount >= App.config.maxRetries) return;
      
      App.state.connectionRetryCount++;
      setTimeout(async () => {
        const connected = await this.checkConnection();
        if (connected) {
          App.state.connectionRetryCount = 0;
          showToast('تم استعادة الاتصال 🌐', 'success');
        } else {
          this.startReconnection();
        }
      }, App.config.retryDelay * App.state.connectionRetryCount);
    },
    
    // إرسال رسالة إلى الذكاء الاصطناعي
    async sendMessage(message, isRegenerate = false) {
      if (!message.trim()) return false;
      
      if (!App.state.isOnline) {
        showToast('لا يوجد اتصال بالإنترنت', 'error');
        return false;
      }
      
      // إظهار مؤشر التفكير
      this.showTypingIndicator(true);
      App.state.isThinking = true;
      
      // إضافة المشاعر بناءً على النص
      this.detectEmotion(message);
      
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000);
        
        const response = await fetch(App.config.apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: message,
            session_id: App.state.currentConversationId,
            regenerate: isRegenerate
          }),
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) throw new Error('Server error');
        
        const data = await response.json();
        
        if (data.reply) {
          // إضافة رسالة المستخدم إذا لم تكن موجودة
          if (!isRegenerate) {
            ArchiveSystem.addMessage('user', message);
          } else {
            // حذف آخر رد للمساعد وإعادة توليد
            const lastAssistantIndex = [...App.state.currentMessages].reverse().findIndex(m => m.sender === 'assistant');
            if (lastAssistantIndex !== -1) {
              const actualIndex = App.state.currentMessages.length - 1 - lastAssistantIndex;
              App.state.currentMessages.splice(actualIndex, 1);
            }
          }
          
          ArchiveSystem.addMessage('assistant', data.reply);
          
          // تحديث المشاعر
          this.detectEmotion(data.reply);
        }
        
        this.showTypingIndicator(false);
        App.state.isThinking = false;
        
        return true;
      } catch (error) {
        console.error('Send message error:', error);
        this.showTypingIndicator(false);
        App.state.isThinking = false;
        showToast('حدث خطأ في الاتصال. حاول مرة أخرى.', 'error');
        return false;
      }
    },
    
    // رفع ملف
    async uploadFile(file) {
      if (!App.state.isOnline) {
        showToast('لا يوجد اتصال بالإنترنت', 'error');
        return false;
      }
      
      if (file.size > App.config.maxFileSize) {
        showToast('حجم الملف كبير جداً (الحد الأقصى 10MB)', 'warning');
        return false;
      }
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('session_id', App.state.currentConversationId);
      
      this.showTypingIndicator(true);
      
      try {
        const response = await fetch(App.config.uploadEndpoint, {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        this.showTypingIndicator(false);
        
        if (data.reply) {
          ArchiveSystem.addMessage('assistant', data.reply);
        }
        
        showToast(`تم رفع الملف: ${file.name}`, 'success');
        return true;
      } catch (error) {
        this.showTypingIndicator(false);
        showToast('فشل رفع الملف', 'error');
        return false;
      }
    },
    
    detectEmotion(text) {
      const emotions = {
        happy: ['😊', '😄', '🎉', '❤️', 'شكر', 'جميل', 'رائع', 'سعيد'],
        sad: ['😢', '😔', 'حزين', 'صعب', 'متعب', 'تعيس'],
        angry: ['😠', '😡', 'غاضب', 'مستاء', 'سيء', 'يزعج'],
        thinking: ['🤔', 'ربما', 'ربما', 'ممكن', 'لست متأكد'],
        excited: ['🤩', '🔥', 'مذهل', 'رائع', 'تحفة', 'سأجرب']
      };
      
      let detected = 'neutral';
      let emoji = '🤖';
      
      for (const [emotion, keywords] of Object.entries(emotions)) {
        if (keywords.some(k => text.includes(k))) {
          detected = emotion;
          switch(emotion) {
            case 'happy': emoji = '😊'; break;
            case 'sad': emoji = '😢'; break;
            case 'angry': emoji = '😠'; break;
            case 'thinking': emoji = '🤔'; break;
            case 'excited': emoji = '🤩'; break;
          }
          break;
        }
      }
      
      App.state.emotion = detected;
      if (App.elements.typingEmotion) {
        App.elements.typingEmotion.textContent = emoji;
      }
      
      // تغيير لون الأفاتار حسب المشاعر
      if (App.elements.avatarCore) {
        const colors = {
          happy: 'linear-gradient(135deg, #10b981, #34d399)',
          sad: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
          angry: 'linear-gradient(135deg, #ef4444, #f87171)',
          thinking: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
          excited: 'linear-gradient(135deg, #ec4899, #f472b6)',
          neutral: 'linear-gradient(135deg, #6366f1, #c026d3)'
        };
        App.elements.avatarCore.style.background = colors[detected] || colors.neutral;
      }
    },
    
    showTypingIndicator(show) {
      if (App.elements.typingContainer) {
        App.elements.typingContainer.style.display = show ? 'flex' : 'none';
      }
      
      if (App.elements.avatarCore) {
        if (show) {
          App.elements.avatarCore.classList.add('speaking');
        } else {
          App.elements.avatarCore.classList.remove('speaking');
        }
      }
    }
  };
  
  /* --------------------------------------------
     نظام التفاعلات والواجهة
  -------------------------------------------- */
  const UISystem = {
    // تهيئة المستمعين
    initEventListeners() {
      // إرسال الرسالة
      App.elements.sendBtn?.addEventListener('click', () => this.handleSend());
      App.elements.messageInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.handleSend();
        }
      });
      
      // عد الحروف والكلمات
      App.elements.messageInput?.addEventListener('input', (e) => {
        const text = e.target.value;
        if (App.elements.charCount) {
          App.elements.charCount.textContent = text.length;
        }
        if (App.elements.wordCount) {
          const words = text.trim() ? text.trim().split(/\s+/).length : 0;
          App.elements.wordCount.textContent = words;
        }
        
        // إظهار اقتراحات تلقائية
        this.showSuggestions(text);
      });
      
      // أزرار التنقل
      App.elements.scrollUpBtn?.addEventListener('click', () => ArchiveSystem.scrollToBottom());
      App.elements.scrollDownBtn?.addEventListener('click', () => ArchiveSystem.scrollToBottom());
      
      // متابعة التمرير
      App.elements.messagesContainer?.addEventListener('scroll', () => {
        const scrollTop = App.elements.messagesContainer.scrollTop;
        const maxScroll = App.elements.messagesContainer.scrollHeight - App.elements.messagesContainer.clientHeight;
        const isAtBottom = maxScroll - scrollTop < 100;
        
        if (App.elements.scrollDownBtn) {
          App.elements.scrollDownBtn.style.display = isAtBottom ? 'none' : 'flex';
        }
        if (App.elements.scrollUpBtn) {
          App.elements.scrollUpBtn.style.display = scrollTop > 100 ? 'flex' : 'none';
        }
      });
      
      // القائمة الجانبية
      App.elements.menuBtn?.addEventListener('click', () => {
        App.elements.sidebar?.classList.add('open');
      });
      App.elements.closeSidebarBtn?.addEventListener('click', () => {
        App.elements.sidebar?.classList.remove('open');
      });
      
      // البحث في الأرشيف
      App.elements.archiveSearch?.addEventListener('input', () => {
        ArchiveSystem.renderConversationsList();
      });
      
      // محادثة جديدة
      App.elements.newConversationBtn?.addEventListener('click', () => {
        ArchiveSystem.newConversation();
        App.elements.sidebar?.classList.remove('open');
      });
      
      // مسح الكل
      App.elements.clearAllBtn?.addEventListener('click', () => {
        ArchiveSystem.deleteAllConversations();
      });
      
      // تصدير الكل
      App.elements.exportAllBtn?.addEventListener('click', () => {
        const exportData = {
          exportDate: new Date().toISOString(),
          conversations: App.state.conversations
        };
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `سماء_جميع_المحادثات_${new Date().toISOString().slice(0, 19)}.json`;
        link.click();
        URL.revokeObjectURL(link.href);
        showToast('تم تصدير جميع المحادثات', 'success');
      });
      
      // وضع التركيز
      App.elements.focusModeBtn?.addEventListener('click', () => {
        App.state.focusMode = !App.state.focusMode;
        document.body.classList.toggle('focus-mode', App.state.focusMode);
        App.elements.focusModeBtn.innerHTML = App.state.focusMode ? '<i class="fas fa-compress"></i>' : '<i class="fas fa-expand"></i>';
        showToast(App.state.focusMode ? 'وضع التركيز مفعل' : 'الخروج من وضع التركيز', 'info');
      });
      
      // تبديل المظهر
      App.elements.themeToggle?.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
        document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
        App.elements.themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        localStorage.setItem('sky_theme', isDark ? 'light' : 'dark');
        showToast(`المظهر ${isDark ? 'الفاتح' : 'الداكن'}`, 'success');
      });
      
      // رفع الملفات
      App.elements.attachBtn?.addEventListener('click', () => {
        App.elements.fileInput?.click();
      });
      App.elements.fileInput?.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        files.forEach(file => {
          AIEngine.uploadFile(file);
        });
        App.elements.fileInput.value = '';
      });
      
      // نافذة البحث
      App.elements.searchBtn?.addEventListener('click', () => {
        App.elements.searchModal.style.display = 'flex';
        App.elements.searchInChat.value = '';
        App.elements.searchResultsContainer.innerHTML = '';
      });
      document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
          App.elements.searchModal.style.display = 'none';
          App.elements.settingsModal.style.display = 'none';
        });
      });
      
      App.elements.searchInChat?.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        if (!term) {
          App.elements.searchResultsContainer.innerHTML = '';
          return;
        }
        
        const results = [];
        App.state.currentMessages.forEach((msg, idx) => {
          if (msg.content.toLowerCase().includes(term)) {
            results.push({ index: idx, message: msg });
          }
        });
        
        App.state.searchResults = results;
        App.state.currentSearchIndex = 0;
        this.renderSearchResults(results);
      });
      
      App.elements.searchPrevBtn?.addEventListener('click', () => {
        if (App.state.searchResults.length === 0) return;
        App.state.currentSearchIndex = (App.state.currentSearchIndex - 1 + App.state.searchResults.length) % App.state.searchResults.length;
        this.highlightSearchResult(App.state.searchResults[App.state.currentSearchIndex]);
      });
      
      App.elements.searchNextBtn?.addEventListener('click', () => {
        if (App.state.searchResults.length === 0) return;
        App.state.currentSearchIndex = (App.state.currentSearchIndex + 1) % App.state.searchResults.length;
        this.highlightSearchResult(App.state.searchResults[App.state.currentSearchIndex]);
      });
      
      // نافذة الإعدادات
      const settingsTrigger = document.querySelector('.icon-btn[aria-label="القائمة"]')?.parentElement?.querySelector('.icon-btn:last-child');
      // إضافة زر الإعدادات - سنضيفه لاحقاً
      
      App.elements.renameConvBtn?.addEventListener('click', () => {
        const newTitle = App.elements.convNameInput.value;
        if (newTitle) {
          ArchiveSystem.renameConversation(App.state.currentConversationId, newTitle);
          App.elements.settingsModal.style.display = 'none';
        }
      });
      
      App.elements.deleteCurrentConvBtn?.addEventListener('click', () => {
        if (confirm('هل تريد حذف هذه المحادثة؟')) {
          ArchiveSystem.deleteConversation(App.state.currentConversationId);
          App.elements.settingsModal.style.display = 'none';
        }
      });
      
      App.elements.exportTxtBtn?.addEventListener('click', () => {
        ArchiveSystem.exportCurrentConversation('txt');
        App.elements.settingsModal.style.display = 'none';
      });
      
      App.elements.exportJsonBtn?.addEventListener('click', () => {
        ArchiveSystem.exportCurrentConversation('json');
        App.elements.settingsModal.style.display = 'none';
      });
      
      App.elements.exportHtmlBtn?.addEventListener('click', () => {
        ArchiveSystem.exportCurrentConversation('html');
        App.elements.settingsModal.style.display = 'none';
      });
    },
    
    handleSend() {
      const message = App.elements.messageInput?.value.trim();
      if (message) {
        AIEngine.sendMessage(message);
        App.elements.messageInput.value = '';
        if (App.elements.charCount) App.elements.charCount.textContent = '0';
        if (App.elements.wordCount) App.elements.wordCount.textContent = '0';
      }
    },
    
    showSuggestions(text) {
      if (!text || text.length < 3) return;
      
      const suggestions = [
        `ما هو ${text}؟`,
        `شرح ${text}`,
        `كيف يعمل ${text}`,
        `مميزات ${text}`,
        `مقارنة بين ${text} وشيء آخر`
      ];
      
      // يمكن إضافة عرض الاقتراحات في UI
    },
    
    renderSearchResults(results) {
      if (!App.elements.searchResultsContainer) return;
      
      if (results.length === 0) {
        App.elements.searchResultsContainer.innerHTML = '<div style="padding: 16px; text-align: center; color: var(--text-tertiary);">لا توجد نتائج</div>';
        return;
      }
      
      App.elements.searchResultsContainer.innerHTML = `
        <div style="padding: 8px 16px; background: var(--primary-glow); border-radius: var(--radius-md); margin-bottom: 12px;">
          تم العثور على ${results.length} نتيجة
        </div>
        ${results.map((r, i) => `
          <div class="search-result-item" data-index="${i}" style="padding: 12px; border-bottom: 1px solid var(--border-light); cursor: pointer;">
            <div style="font-size: 0.7rem; color: var(--text-tertiary);">${new Date(r.message.timestamp).toLocaleTimeString('ar')}</div>
            <div style="font-size: 0.85rem; ${r.message.sender === 'user' ? 'color: var(--primary-light);' : ''}">${r.message.content.substring(0, 100)}${r.message.content.length > 100 ? '...' : ''}</div>
          </div>
        `).join('')}
      `;
      
      document.querySelectorAll('.search-result-item').forEach(el => {
        el.addEventListener('click', () => {
          const idx = parseInt(el.dataset.index);
          this.highlightSearchResult(results[idx]);
          App.elements.searchModal.style.display = 'none';
        });
      });
    },
    
    highlightSearchResult(result) {
      const messages = document.querySelectorAll('.message');
      if (messages[result.index]) {
        messages[result.index].scrollIntoView({ behavior: 'smooth', block: 'center' });
        messages[result.index].style.animation = 'pulse-glow 0.5s ease';
        setTimeout(() => {
          messages[result.index].style.animation = '';
        }, 1000);
      }
    },
    
    // تأثيرات لمسية
    addRippleEffect(element, event) {
      const rect = element.getBoundingClientRect();
      const x = (event.clientX || event.touches?.[0]?.clientX || rect.width/2) - rect.left;
      const y = (event.clientY || event.touches?.[0]?.clientY || rect.height/2) - rect.top;
      
      const ripple = document.createElement('span');
      ripple.className = 'ripple-effect';
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      element.style.position = 'relative';
      element.style.overflow = 'hidden';
      element.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    },
    
    // حماية من الإغلاق العرضي
    beforeUnloadHandler(e) {
      if (App.state.isThinking) {
        e.preventDefault();
        e.returnValue = 'سماء لا تزال تفكر... هل تريد المغادرة؟';
        return e.returnValue;
      }
    },
    
    // حفظ الحالة تلقائياً
    autoSave() {
      setInterval(() => {
        ArchiveSystem.saveConversations();
      }, App.config.autoSaveInterval);
    },
    
    // مراقبة الاتصال
    startConnectionMonitoring() {
      setInterval(() => {
        AIEngine.checkConnection();
      }, App.config.pingInterval);
      
      window.addEventListener('online', () => {
        AIEngine.checkConnection();
        showToast('تم استعادة الاتصال بالإنترنت', 'success');
      });
      
      window.addEventListener('offline', () => {
        App.state.isOnline = false;
        AIEngine.updateConnectionUI(false, null);
        showToast('انقطع الاتصال بالإنترنت', 'warning');
      });
    }
  };
  
  /* --------------------------------------------
     نظام الخلفية ثلاثية الأبعاد
  -------------------------------------------- */
  const Background3D = {
    init() {
      if (!App.elements.bgCanvas) return;
      
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({ canvas: App.elements.bgCanvas, alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setClearColor(0x000000, 0);
      
      // جسيمات متحركة
      const particlesGeometry = new THREE.BufferGeometry();
      const particlesCount = 800;
      const positions = new Float32Array(particlesCount * 3);
      
      for (let i = 0; i < particlesCount; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 200;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 100;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 100 - 50;
      }
      
      particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      
      const particlesMaterial = new THREE.PointsMaterial({
        color: 0x6366f1,
        size: 0.2,
        transparent: true,
        opacity: 0.5,
        blending: THREE.AdditiveBlending
      });
      
      const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
      scene.add(particlesMesh);
      
      camera.position.z = 30;
      
      let time = 0;
      let mouseX = 0, mouseY = 0;
      
      document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = (e.clientY / window.innerHeight) * 2 - 1;
      });
      
      document.addEventListener('touchmove', (e) => {
        if (e.touches[0]) {
          mouseX = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
          mouseY = (e.touches[0].clientY / window.innerHeight) * 2 - 1;
        }
      });
      
      function animate() {
        requestAnimationFrame(animate);
        time += 0.003;
        
        particlesMesh.rotation.x = Math.sin(time * 0.2) * 0.2 + mouseY * 0.5;
        particlesMesh.rotation.y = Math.sin(time * 0.3) * 0.2 + mouseX * 0.5;
        
        const colors = ['#6366f1', '#c026d3', '#8b5cf6', '#a855f7'];
        particlesMaterial.color.setHex(parseInt(colors[Math.floor(time * 2) % colors.length].slice(1), 16));
        
        renderer.render(scene, camera);
      }
      
      animate();
      
      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });
    }
  };
  
  /* --------------------------------------------
     إخفاء مؤشر التحميل
  -------------------------------------------- */
  function hideLoader() {
    const loader = document.getElementById('initial-loader');
    if (loader) {
      loader.style.opacity = '0';
      setTimeout(() => {
        loader.style.display = 'none';
        if (App.elements.app) {
          App.elements.app.style.opacity = '1';
        }
      }, 500);
    }
  }
  
  /* --------------------------------------------
     استعادة المظهر المحفوظ
  -------------------------------------------- */
  function loadSavedTheme() {
    const savedTheme = localStorage.getItem('sky_theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
      if (App.elements.themeToggle) {
        App.elements.themeToggle.innerHTML = savedTheme === 'light' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
      }
    }
  }
  
  /* --------------------------------------------
     بدء التشغيل
  -------------------------------------------- */
  async function init() {
    // تهيئة العناصر
    initElements();
    
    // تحميل المحادثات المحفوظة
    ArchiveSystem.loadConversations();
    
    // تهيئة خلفية ثلاثية الأبعاد
    Background3D.init();
    
    // تهيئة المستمعين
    UISystem.initEventListeners();
    
    // استعادة المظهر
    loadSavedTheme();
    
    // بدء مراقبة الاتصال
    await AIEngine.checkConnection();
    UISystem.startConnectionMonitoring();
    
    // الحفظ التلقائي
    UISystem.autoSave();
    
    // منع الإغلاق العرضي
    window.addEventListener('beforeunload', UISystem.beforeUnloadHandler);
    
    // إخفاء مؤشر التحميل
    hideLoader();
    
    // تأثيرات لمسية على الأزرار
    document.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', (e) => UISystem.addRippleEffect(btn, e));
      btn.addEventListener('touchstart', (e) => UISystem.addRippleEffect(btn, e));
    });
    
    console.log('🌟 سماء - الواجهة الذكية الحية - جاهزة للعمل');
    showToast('مرحباً بك في سماء 🌙', 'success', 2000);
  }
  
  // بدء التطبيق
  init();
});
