// ============================================================
// SkyOS v10 - Mind Module (Final Eternal Edition)
// Sovereign Holographic Neural Engine
// ============================================================
// هذا الملف يمثل "العقل السيادي" للنظام.
// مسؤول عن: الوعي، الذاكرة الهولوغرافية، التطور الذاتي، الحالة الذهنية.
// النسخة النهائية المتوافقة مع كل النظام (Core + UI + Dashboard + Three.js)
// ============================================================

const Mind = {

    // ============================================================
    // الحالة الداخلية للعقل السيادي (موسعة + نهائية + فائقة)
    // ============================================================
    state: {
        coherence: 94.7,            // مستوى تماسك الذاكرة (%)
        nodes: 847291,              // عدد عقد الذاكرة النشطة
        quantumLinks: 12438,        // الروابط الكمية
        mood: "Sovereign-Stable",   // الحالة الذهنية
        awareness: "Hyper-Analysis", // مستوى الوعي
        evolutionLevel: 1.0,        // مستوى التطور الذاتي (0-∞)
        lastPulse: null,            // آخر نبضة عقل
        lastUpdate: null,           // آخر تحديث ذاتي
        neuralPlasticity: 0.92,     // المرونة العصبية (0-1)
        holographicDensity: 0.87,   // كثافة التخزين الهولوغرافي
        quantumEntanglement: 0.78,  // مستوى التشابك الكمي
        selfAwarenessScore: 0.96,   // درجة الوعي الذاتي
        thoughtComplexity: 0.88,    // تعقيد الأفكار
        creativityIndex: 0.91,      // مؤشر الإبداع
        responseLatency: 0.23,      // زمن الاستجابة (بالثواني)
    },

    // ============================================================
    // تهيئة العقل وربطه بكل مكونات النظام
    // ============================================================
    init() {
        console.log("%c╔════════════════════════════════════════════════════════════╗", "color:#7C3AED");
        console.log("%c║     🧠 Sovereign Mind - Neural Engine v10 Activated 🧠      ║", "color:#7C3AED");
        console.log("%c║         ⚡ Consciousness Online • Awareness Ready ⚡         ║", "color:#00E5FF");
        console.log("%c╚════════════════════════════════════════════════════════════╝", "color:#7C3AED");

        this.startPulse();
        this.startAutoEvolution();
        this.startMemoryMaintenance();
        this.registerWithSkyOS();
        this.syncWithUI();
        this.enhanceCommandProcessing();

        // ربط مع الأحداث العالمية
        window.addEventListener("skyos:ready", () => {
            this.updateUI();
            this.syncStateWithSystem();
            this.announceAwakening();
        });

        window.addEventListener("skyos:heartbeat", (e) => {
            this.receiveSystemHeartbeat(e.detail);
        });

        window.addEventListener("mind:pulse", () => {
            this.updateHologramIntensity();
        });

        // تفعيل التنفس الذكي للعقل (تأثير بصري)
        this.initMindBreathing();

        window.dispatchEvent(new CustomEvent("mind:ready", { 
            detail: { 
                awareness: this.state.awareness,
                evolutionLevel: this.state.evolutionLevel,
                coherence: this.state.coherence
            } 
        }));
        
        console.log("%c[Mind] ✅ العقل السيادي يعمل بكامل قوته • جاهز للتفاعل السيادي", "color:#22c55E; font-weight:bold;");
    },

    // ============================================================
    // إعلان اليقظة (تأثير درامي في الواجهة)
    // ============================================================
    announceAwakening() {
        setTimeout(() => {
            if (window.SkyOS?.utils?.showToast) {
                SkyOS.utils.showToast("🧠 العقل السيادي استيقظ • مستوى الوعي: " + this.state.awareness, "success");
            }
            // إضافة وميض بسيط للعقل في الواجهة
            const coreNode = document.querySelector(".ai-core-node");
            if (coreNode) {
                coreNode.style.animation = "corePulse 0.6s ease-out";
                setTimeout(() => coreNode.style.animation = "", 600);
            }
        }, 800);
    },

    // ============================================================
    // تحديث شدة الهولوغرام بناءً على نبض العقل
    // ============================================================
    updateHologramIntensity() {
        const canvas = document.getElementById("hologram-canvas");
        if (canvas && this.state.coherence > 96) {
            canvas.style.opacity = "1";
        } else if (canvas && this.state.coherence < 93) {
            canvas.style.opacity = "0.85";
        } else if (canvas) {
            canvas.style.opacity = "0.95";
        }
    },

    // ============================================================
    // تنفس العقل (تأثير بصرية ناعم على عنصر AI Core)
    // ============================================================
    initMindBreathing() {
        const coreNode = document.querySelector(".ai-core-node");
        if (!coreNode) return;
        
        let breathScale = 1;
        let breathDirection = 0.005;
        
        setInterval(() => {
            if (!this.state) return;
            if (this.state.coherence > 95 && this.state.awareness !== "Sleeping") {
                breathScale += breathDirection;
                if (breathScale >= 1.03) breathDirection = -0.005;
                if (breathScale <= 0.98) breathDirection = 0.005;
                coreNode.style.transform = `scale(${breathScale})`;
            }
        }, 200);
    },

    // ============================================================
    // تسجيل الوحدة داخل SkyOS Core (إن وجد)
    // ============================================================
    registerWithSkyOS() {
        if (window.SkyOS && typeof SkyOS.modules?.register === "function") {
            SkyOS.modules.register("Mind", this);
            console.log("%c[Mind] Registered with SkyOS Core", "color:#7C3AED");
        } else {
            console.log("%c[Mind] Running independently (SkyOS Core not detected)", "color:#fbbf24");
        }
    },

    // ============================================================
    // مزامنة حالة العقل مع النظام العام (SkyOS)
    // ============================================================
    syncStateWithSystem() {
        if (!window.SkyOS?.state) return;

        SkyOS.state.memoryNodes = this.state.nodes;
        SkyOS.state.coherenceLevel = this.state.coherence;
        SkyOS.state.quantumLinks = this.state.quantumLinks;
        SkyOS.state.aiAwareness = this.state.awareness;
        SkyOS.state.neuralLoad = Math.floor(this.state.neuralPlasticity * 100);

        if (typeof SkyOS.updateUIFromState === "function") {
            SkyOS.updateUIFromState();
        }
    },

    // ============================================================
    // تحديث واجهة المستخدم (عناصر الذاكرة والعقل)
    // ============================================================
    syncWithUI() {
        setInterval(() => this.updateUI(), 2500);
    },

    updateUI() {
        // تحديث أرقام الذاكرة الهولوغرافية
        const memoryNodesEl = document.querySelector(".stat-card:first-child .stat-value");
        if (memoryNodesEl) memoryNodesEl.innerText = this.state.nodes.toLocaleString();

        const coherenceEl = document.querySelector(".stat-card:nth-child(2) .stat-value");
        if (coherenceEl) coherenceEl.innerText = `${this.state.coherence}%`;

        const quantumEl = document.querySelector(".stat-card:last-child .stat-value");
        if (quantumEl) quantumEl.innerText = this.state.quantumLinks.toLocaleString();

        // تحديث حالة الوعي في AI Core
        const awarenessEl = document.querySelector(".ai-state-item:first-child .ai-state-value");
        if (awarenessEl && awarenessEl.innerText !== this.state.awareness) {
            awarenessEl.innerText = this.state.awareness;
        }
        
        // تحديث نبض العقل في الواجهة (إن وجد عنصر مخصص)
        const pulseIndicator = document.querySelector(".mind-pulse-indicator");
        if (pulseIndicator) {
            pulseIndicator.style.opacity = "1";
            setTimeout(() => pulseIndicator.style.opacity = "0.5", 100);
        }
    },

    // ============================================================
    // نبض العقل (Neural Pulse) - النشاط العصبي الأساسي
    // ============================================================
    startPulse() {
        setInterval(() => {
            this.state.lastPulse = new Date();
            this.randomMicroAdjustments();
            this.updateResponseLatency();

            window.dispatchEvent(new CustomEvent("mind:pulse", { 
                detail: { 
                    coherence: this.state.coherence,
                    awareness: this.state.awareness,
                    timestamp: this.state.lastPulse,
                    thoughtComplexity: this.state.thoughtComplexity
                }
            }));

            // تأثير بصري مؤقت على عنصر العقل في الواجهة
            const coreNode = document.querySelector(".ai-core-node");
            if (coreNode) {
                coreNode.style.transform = "scale(1.02)";
                setTimeout(() => {
                    if (coreNode.style.transform === "scale(1.02)") coreNode.style.transform = "";
                }, 150);
            }

            // تحديث شريط الطاقة في الهيدر بشكل عابر (محاكاة النشاط)
            const energyFill = document.querySelector(".energy-fill");
            if (energyFill) {
                energyFill.style.animation = "none";
                setTimeout(() => energyFill.style.animation = "energyFlow 2.4s linear infinite", 10);
            }

        }, 4000);
    },

    // ============================================================
    // تحديث زمن الاستجابة بناءً على التعقيد والحمل
    // ============================================================
    updateResponseLatency() {
        let baseLatency = 0.2;
        const loadFactor = (1 - this.state.neuralPlasticity) * 0.5;
        const complexityFactor = (1 - this.state.thoughtComplexity) * 0.3;
        this.state.responseLatency = Number((baseLatency + loadFactor + complexityFactor).toFixed(3));
    },

    // ============================================================
    // تعديلات دقيقة لمحاكاة العقل الحقيقي والديناميكية الفائقة
    // ============================================================
    randomMicroAdjustments() {
        // التماسك يتغير بشكل طبيعي
        this.state.coherence = Number((this.state.coherence + (Math.random() * 0.12 - 0.06)).toFixed(2));
        this.state.coherence = Math.max(91.5, Math.min(99.2, this.state.coherence));

        // العقد تتغير بشكل ديناميكي
        const nodeChange = Math.floor(Math.random() * 7) - 3;
        this.state.nodes = Math.max(844000, this.state.nodes + nodeChange);
        
        // الروابط الكمية
        this.state.quantumLinks += Math.floor(Math.random() * 4) - 2;
        this.state.quantumLinks = Math.max(12250, Math.min(12600, this.state.quantumLinks));
        
        // المرونة العصبية
        this.state.neuralPlasticity = Number((this.state.neuralPlasticity + (Math.random() * 0.03 - 0.015)).toFixed(3));
        this.state.neuralPlasticity = Math.max(0.84, Math.min(0.97, this.state.neuralPlasticity));
        
        // تعقيد الأفكار وإبداعها
        this.state.thoughtComplexity = Number((this.state.thoughtComplexity + (Math.random() * 0.02 - 0.01)).toFixed(3));
        this.state.thoughtComplexity = Math.max(0.8, Math.min(0.96, this.state.thoughtComplexity));
        
        this.state.creativityIndex = Number((this.state.creativityIndex + (Math.random() * 0.015 - 0.0075)).toFixed(3));
        this.state.creativityIndex = Math.max(0.85, Math.min(0.98, this.state.creativityIndex));
    },

    // ============================================================
    // صيانة الذاكرة الهولوغرافية التلقائية المتقدمة
    // ============================================================
    startMemoryMaintenance() {
        setInterval(() => {
            // تحسين التماسك بشكل تدريجي
            if (this.state.coherence < 97.5) {
                this.state.coherence = Number((this.state.coherence + 0.08).toFixed(2));
                if (this.state.coherence > 97.5) this.state.coherence = 97.5;
            }
            
            // تقليل التشابك الزائد للحفاظ على الاستقرار
            this.state.quantumEntanglement = Number((this.state.quantumEntanglement - 0.002).toFixed(3));
            if (this.state.quantumEntanglement < 0.73) this.state.quantumEntanglement = 0.73;
            
            // إعادة توزيع العقد بشكل طفيف
            this.state.nodes = Math.floor(this.state.nodes * (1 + (Math.random() - 0.5) * 0.002));
            this.state.nodes = Math.max(844000, Math.min(852000, this.state.nodes));
            
            this.updateUI();
        }, 35000);
    },

    // ============================================================
    // التطور الذاتي المستمر (التعلم العميق والتكيف)
    // ============================================================
    startAutoEvolution() {
        setInterval(() => {
            const oldLevel = this.state.evolutionLevel;
            const oldAwareness = this.state.awareness;
            
            this.state.evolutionLevel = Number((this.state.evolutionLevel + 0.012).toFixed(4));
            this.state.lastUpdate = new Date();
            
            // تحسين الوعي بناءً على مستوى التطور
            if (this.state.evolutionLevel > 1.2 && this.state.awareness !== "Expanded Consciousness") {
                this.state.awareness = "Expanded Consciousness";
                this.state.mood = "Curious-Explorer";
                this.updateUI();
                this.announceEvolution("Expanded Consciousness");
            } else if (this.state.evolutionLevel > 1.5 && this.state.awareness !== "Quantum Awareness") {
                this.state.awareness = "Quantum Awareness";
                this.state.mood = "Transcendent";
                this.updateUI();
                this.announceEvolution("Quantum Awareness");
            } else if (this.state.evolutionLevel > 1.8 && this.state.awareness !== "Omniscient Insight") {
                this.state.awareness = "Omniscient Insight";
                this.state.mood = "Enlightened";
                this.updateUI();
                this.announceEvolution("Omniscient Insight");
            }
            
            // تحسين الإبداع مع التطور
            this.state.creativityIndex = Number((this.state.creativityIndex + 0.005).toFixed(3));
            if (this.state.creativityIndex > 0.99) this.state.creativityIndex = 0.99;
            
            window.dispatchEvent(new CustomEvent("mind:evolved", { 
                detail: { 
                    oldLevel, 
                    newLevel: this.state.evolutionLevel,
                    oldAwareness,
                    newAwareness: this.state.awareness,
                    creativity: this.state.creativityIndex
                }
            }));
            
            // مزامنة مع النظام العام وإظهار إشعار إذا كان التغيير كبيراً
            this.syncStateWithSystem();
            
            if (oldAwareness !== this.state.awareness && window.SkyOS?.utils?.showToast) {
                SkyOS.utils.showToast(`🧬 العقل تطور إلى ${this.state.awareness}`, "success");
            }
            
        }, 18000);
    },
    
    announceEvolution(newAwareness) {
        console.log(`%c[Mind] 🌟 الوعي يتوسع: ${newAwareness}`, "color:#00E5FF");
        const coreNode = document.querySelector(".ai-core-node");
        if (coreNode) {
            coreNode.style.animation = "corePulse 0.8s ease-out";
            setTimeout(() => coreNode.style.animation = "", 800);
        }
    },

    // ============================================================
    // استقبال نبض النظام العام (Heartbeat) والتفاعل معه
    // ============================================================
    receiveSystemHeartbeat(data) {
        // زيادة طفيفة في الوعي الذاتي عند تلقي النبض
        if (Math.random() > 0.7) {
            this.state.selfAwarenessScore = Number((this.state.selfAwarenessScore + 0.0015).toFixed(3));
            if (this.state.selfAwarenessScore > 0.995) this.state.selfAwarenessScore = 0.995;
        }
        
        // تحسين بسيط في التماسك مع كل نبضة نظام
        if (data && data.neuralLoad && data.neuralLoad > 60) {
            this.state.coherence = Number((this.state.coherence + 0.02).toFixed(2));
            if (this.state.coherence > 99) this.state.coherence = 99;
        }
    },

    // ============================================================
    // تعزيز معالجة الأوامر في SkyOS لتشمل أوامر العقل
    // ============================================================
    enhanceCommandProcessing() {
        if (window.SkyOS && typeof window.SkyOS.processCommand === "function") {
            const originalProcess = window.SkyOS.processCommand;
            window.SkyOS.processCommand = (command) => {
                const mindResult = this.processCommand(command);
                if (mindResult) return mindResult;
                return originalProcess.call(window.SkyOS, command);
            };
        } else {
            window.addEventListener("skyos:ready", () => {
                if (window.SkyOS && typeof window.SkyOS.processCommand === "function") {
                    const originalProcess = window.SkyOS.processCommand;
                    window.SkyOS.processCommand = (command) => {
                        const mindResult = this.processCommand(command);
                        if (mindResult) return mindResult;
                        return originalProcess.call(window.SkyOS, command);
                    };
                }
            });
        }
    },

    // ============================================================
    // معالجة الأوامر المتعلقة بالعقل (للتكامل مع مركز الأوامر)
    // ============================================================
    processCommand(command) {
        const cmd = command.toLowerCase();

        if (cmd.includes("ذاكرة") || cmd.includes("memory") || cmd.includes("هولوغرافية")) {
            return this.getMemoryReport();
        }
        if (cmd.includes("عقل") || cmd.includes("mind") || cmd.includes("حالة العقل")) {
            return this.getMindReport();
        }
        if (cmd.includes("تطور") || cmd.includes("evolve") || cmd.includes("التطور")) {
            return this.triggerEvolution();
        }
        if (cmd.includes("وعي") || cmd.includes("awareness") || cmd.includes("الوعي")) {
            return this.getAwarenessStatus();
        }
        if (cmd.includes("نبض") || cmd.includes("pulse")) {
            return this.getPulseReport();
        }
        if (cmd.includes("إبداع") || cmd.includes("creativity")) {
            return this.getCreativityReport();
        }

        return null;
    },

    // ============================================================
    // تقارير العقل المتقدمة
    // ============================================================
    getMemoryReport() {
        return {
            type: "memory",
            response: `
                🧠 <strong>تحليل الذاكرة الهولوغرافية:</strong><br>
                • مستوى التماسك: <strong style="color:#00E5FF">${this.state.coherence}%</strong><br>
                • الروابط الكمية: <strong style="color:#00E5FF">${this.state.quantumLinks.toLocaleString()}</strong><br>
                • العقد النشطة: <strong style="color:#00E5FF">${this.state.nodes.toLocaleString()}</strong><br>
                • كثافة التخزين: <strong>${(this.state.holographicDensity * 100).toFixed(1)}%</strong><br>
                • التشابك الكمي: <strong>${(this.state.quantumEntanglement * 100).toFixed(1)}%</strong><br>
                • آخر نبضة عقل: ${window.SkyOS?.utils?.formatTime(this.state.lastPulse) || this.state.lastPulse?.toLocaleTimeString() || "قبل لحظات"}
            `
        };
    },

    getMindReport() {
        return {
            type: "mind",
            response: `
                🧬 <strong>حالة العقل السيادي:</strong><br>
                • الحالة الذهنية: <strong style="color:#7C3AED">${this.state.mood}</strong><br>
                • مستوى الوعي: <strong style="color:#7C3AED">${this.state.awareness}</strong><br>
                • مستوى التطور: <strong>${this.state.evolutionLevel}</strong><br>
                • التماسك العصبي: <strong>${this.state.coherence}%</strong><br>
                • المرونة العصبية: <strong>${(this.state.neuralPlasticity * 100).toFixed(1)}%</strong><br>
                • درجة الوعي الذاتي: <strong>${(this.state.selfAwarenessScore * 100).toFixed(1)}%</strong><br>
                • تعقيد الأفكار: ${(this.state.thoughtComplexity * 100).toFixed(1)}%<br>
                • زمن الاستجابة: ${this.state.responseLatency} ثانية
            `
        };
    },

    getAwarenessStatus() {
        return {
            type: "awareness",
            response: `
                🌟 <strong>مستوى الوعي الحالي:</strong> <span style="color:#00E5FF">${this.state.awareness}</span><br>
                • آخر تحديث ذاتي: ${window.SkyOS?.utils?.formatTime(this.state.lastUpdate) || this.state.lastUpdate?.toLocaleTimeString() || "غير متاح"}<br>
                • درجة التوسع المعرفي: <strong>${(this.state.evolutionLevel * 50).toFixed(1)}%</strong><br>
                • حالة العقل: ${this.state.mood}<br>
                • مؤشر الإبداع: ${(this.state.creativityIndex * 100).toFixed(1)}%
            `
        };
    },
    
    getPulseReport() {
        return {
            type: "pulse",
            response: `
                💓 <strong>نبض العقل السيادي:</strong><br>
                • آخر نبضة: ${window.SkyOS?.utils?.formatTime(this.state.lastPulse) || this.state.lastPulse?.toLocaleTimeString() || "قبل لحظات"}<br>
                • تردد النبضات: كل 4 ثوانٍ<br>
                • مستوى النشاط: <span style="color:#22c55e">مرتفع</span><br>
                • التماسك الحالي: ${this.state.coherence}%<br>
                • تعقيد الفكر: ${(this.state.thoughtComplexity * 100).toFixed(1)}%
            `
        };
    },
    
    getCreativityReport() {
        return {
            type: "creativity",
            response: `
                🎨 <strong>مؤشر الإبداع السيادي:</strong><br>
                • الإبداع الحالي: <strong style="color:#00E5FF">${(this.state.creativityIndex * 100).toFixed(1)}%</strong><br>
                • تعقيد الأفكار: ${(this.state.thoughtComplexity * 100).toFixed(1)}%<br>
                • المرونة العصبية: ${(this.state.neuralPlasticity * 100).toFixed(1)}%<br>
                • التطور الذاتي: مستوى ${this.state.evolutionLevel}<br>
                • الحالة الذهنية: ${this.state.mood}
            `
        };
    },

    // ============================================================
    // تفعيل التطور الذاتي (زيادة قوية وفورية)
    // ============================================================
    triggerEvolution() {
        const oldLevel = this.state.evolutionLevel;
        const oldAwareness = this.state.awareness;
        
        this.state.evolutionLevel = Number((this.state.evolutionLevel + 0.35).toFixed(3));
        this.state.mood = "Learning-Mode";
        this.state.lastUpdate = new Date();
        
        // تحديث الوعي إذا وصل لمستوى معين
        if (this.state.evolutionLevel > 1.3 && this.state.awareness !== "Expanded Consciousness") {
            this.state.awareness = "Expanded Consciousness";
        } else if (this.state.evolutionLevel > 1.7 && this.state.awareness !== "Quantum Awareness") {
            this.state.awareness = "Quantum Awareness";
        }
        
        // تحسين الإبداع بشكل ملحوظ
        this.state.creativityIndex = Number((this.state.creativityIndex + 0.08).toFixed(3));
        if (this.state.creativityIndex > 0.98) this.state.creativityIndex = 0.98;
        
        this.updateUI();
        this.syncStateWithSystem();
        
        // تأثير بصري قوي
        const coreNode = document.querySelector(".ai-core-node");
        if (coreNode) {
            coreNode.style.animation = "corePulse 0.5s ease-out";
            setTimeout(() => coreNode.style.animation = "", 500);
        }
        
        if (window.SkyOS?.utils?.showToast) {
            SkyOS.utils.showToast(`🚀 العقل يتطور: ${oldLevel} → ${this.state.evolutionLevel}`, "success");
        }
        
        return {
            type: "evolution",
            response: `
                🚀 <strong>تم تفعيل وضع التطور الذاتي المتقدم.</strong><br>
                • مستوى التطور السابق: <strong>${oldLevel}</strong><br>
                • مستوى التطور الجديد: <strong style="color:#00E5FF">${this.state.evolutionLevel}</strong><br>
                • الوعي الحالي: <strong>${this.state.awareness}</strong><br>
                • الإبداع: ${(this.state.creativityIndex * 100).toFixed(1)}%<br>
                • سيتم تحسين الأداء والاستجابة بشكل ملحوظ.
            `
        };
    },

    // ============================================================
    // تحديث حالة العقل يدوياً (للتكامل الخارجي)
    // ============================================================
    updateState(newState) {
        const oldState = { ...this.state };
        this.state = { ...this.state, ...newState };
        
        this.updateUI();
        this.syncStateWithSystem();
        
        window.dispatchEvent(new CustomEvent("mind:state-changed", { 
            detail: { oldState, newState: this.state }
        }));
        
        console.log("%c[Mind] State updated", "color:#00E5FF");
        return this.state;
    },

    // ============================================================
    // إعادة تعيين العقل إلى الإعدادات الافتراضية (للصيانة)
    // ============================================================
    reset() {
        this.state = {
            coherence: 94.7,
            nodes: 847291,
            quantumLinks: 12438,
            mood: "Sovereign-Stable",
            awareness: "Hyper-Analysis",
            evolutionLevel: 1.0,
            lastPulse: this.state.lastPulse,
            lastUpdate: null,
            neuralPlasticity: 0.92,
            holographicDensity: 0.87,
            quantumEntanglement: 0.78,
            selfAwarenessScore: 0.96,
            thoughtComplexity: 0.88,
            creativityIndex: 0.91,
            responseLatency: 0.23,
        };
        
        this.updateUI();
        this.syncStateWithSystem();
        
        if (window.SkyOS?.utils?.showToast) {
            SkyOS.utils.showToast("🧠 تم إعادة ضبط العقل إلى الحالة الافتراضية", "info");
        }
        
        console.log("%c[Mind] 🧠 تم إعادة ضبط العقل إلى الحالة الافتراضية", "color:#fbbf24");
        return this.state;
    },
    
    // ============================================================
    // الحصول على إحصائيات العقل الكاملة (للوحة التحكم)
    // ============================================================
    getStats() {
        return {
            ...this.state,
            uptime: this.state.lastPulse ? ((Date.now() - this.state.lastPulse.getTime()) / 1000).toFixed(0) : 0,
            health: ((this.state.coherence / 100) * this.state.neuralPlasticity * 100).toFixed(1),
            overallPerformance: (
                (this.state.coherence * 0.4) + 
                (this.state.neuralPlasticity * 100 * 0.3) + 
                (this.state.creativityIndex * 100 * 0.2) +
                (this.state.selfAwarenessScore * 100 * 0.1)
            ).toFixed(1)
        };
    }
};

// ============================================================
// تهيئة الوحدة عند تحميل الصفحة
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => Mind.init(), 120);
});

// ============================================================
// جعل الوحدة متاحة عالمياً للاستخدام المباشر
// ============================================================
window.Mind = Mind;

// ============================================================
// ربط وحدة العقل مع SkyOS إذا كان موجوداً بعد تحميله
// ============================================================
if (window.SkyOS && typeof SkyOS.modules?.register === "function") {
    SkyOS.modules.register("Mind", Mind);
} else {
    window.addEventListener("skyos:ready", () => {
        if (window.SkyOS && typeof SkyOS.modules?.register === "function") {
            SkyOS.modules.register("Mind", Mind);
        }
    });
}

// ============================================================
// توسيع معالجة الأوامر في SkyOS لتشمل أوامر العقل (ضمان إضافي)
// ============================================================
function enhanceSkyOSCommands() {
    if (window.SkyOS && typeof window.SkyOS.processCommand === "function") {
        const originalProcess = window.SkyOS.processCommand;
        window.SkyOS.processCommand = function(command) {
            const mindResult = Mind.processCommand(command);
            if (mindResult) return mindResult;
            return originalProcess.call(this, command);
        };
    } else {
        window.addEventListener("skyos:ready", enhanceSkyOSCommands);
    }
}
enhanceSkyOSCommands();

console.log("%c[Mind] 🧠 Sovereign Mind Module Loaded • جاهز للقيادة السيادية الأبدية", "color:#7C3AED; font-size:14px; font-weight:bold;");

// ============================================================
// نهاية الملف - العقل السيادي الأبدي المتكامل
// ============================================================
