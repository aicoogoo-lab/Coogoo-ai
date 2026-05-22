// ======================================================
// SkyOS v10 — WebXR AR Controller (نسخة متكاملة)
// يدعم: hit-test، تتبع المكان، ربط حالة العقل، جسيمات، تفاعل
// ======================================================

let arSession = null;
let arRenderer = null;
let arScene = null;
let arCamera = null;
let arMind = null;
let arParticles = null;
let arRing = null;
let currentArMood = 'neutral';
let arFrameRequest = null;
let hitTestSource = null;
let referenceSpace = null;
let currentPosition = { x: 0, y: 0, z: -1.2 };

// ألوان المزاج للواقع المعزز (نفس الألوان المستخدمة في three-mind.js)
const arMoodColors = {
  neutral: 0x6366f1,
  happy: 0x4ade80,
  excited: 0xf59e0b,
  thoughtful: 0x8b5cf6,
  calm: 0x06b6d4,
  sad: 0xef4444
};

async function enterARMode() {
  if (!navigator.xr) {
    if (window.SkyUI) SkyUI.showToast("المتصفح لا يدعم الواقع المعزز", "error");
    else alert("المتصفح لا يدعم الواقع المعزز");
    return;
  }

  try {
    const supported = await navigator.xr.isSessionSupported('immersive-ar');
    if (!supported) {
      if (window.SkyUI) SkyUI.showToast("الواقع المعزز غير مدعوم على هذا الجهاز", "error");
      else alert("الواقع المعزز غير مدعوم على هذا الجهاز");
      return;
    }

    arSession = await navigator.xr.requestSession('immersive-ar', {
      requiredFeatures: ['local-floor', 'hit-test'],
      optionalFeatures: ['dom-overlay'],
      domOverlay: { root: document.body }
    });

    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl', { xrCompatible: true });

    arRenderer = new THREE.WebGLRenderer({
      canvas: canvas,
      context: gl,
      alpha: true,
      preserveDrawingBuffer: true
    });
    arRenderer.setSize(window.innerWidth, window.innerHeight);
    arRenderer.setPixelRatio(window.devicePixelRatio);
    arRenderer.xr.enabled = true;

    arScene = new THREE.Scene();
    arScene.background = null; // شفاف لرؤية الكاميرا الحقيقية

    // إضاءة مناسبة للواقع المعزز
    const ambientLight = new THREE.AmbientLight(0x404060, 0.6);
    arScene.add(ambientLight);
    
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(1, 2, 1);
    arScene.add(dirLight);
    
    const fillLight = new THREE.PointLight(0x6366f1, 0.4);
    fillLight.position.set(0, 1, 0);
    arScene.add(fillLight);

    // إنشاء العقل الهولوغرافي للواقع المعزز
    const geometry = new THREE.IcosahedronGeometry(0.22, 1);
    const material = new THREE.MeshStandardMaterial({
      color: arMoodColors.neutral,
      emissive: 0x1e1b4b,
      emissiveIntensity: 0.5,
      metalness: 0.7,
      roughness: 0.3,
      transparent: true,
      opacity: 0.92
    });
    arMind = new THREE.Mesh(geometry, material);
    
    // حلقة حول العقل
    const ringGeo = new THREE.TorusGeometry(0.32, 0.008, 32, 100);
    const ringMat = new THREE.MeshStandardMaterial({ color: 0xa78bfa, emissive: 0x4c1d95 });
    arRing = new THREE.Mesh(ringGeo, ringMat);
    arMind.add(arRing);
    
    // جسيمات صغيرة حول العقل
    const particleCount = 150;
    const particlesGeometry = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
      const radius = 0.45 + Math.random() * 0.2;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      particlePositions[i*3] = radius * Math.sin(phi) * Math.cos(theta);
      particlePositions[i*3+1] = radius * Math.sin(phi) * Math.sin(theta);
      particlePositions[i*3+2] = radius * Math.cos(phi);
    }
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    const particleMaterial = new THREE.PointsMaterial({ color: 0xa78bfa, size: 0.008, transparent: true });
    arParticles = new THREE.Points(particlesGeometry, particleMaterial);
    arMind.add(arParticles);
    
    arScene.add(arMind);

    // إعداد hit-test
    arSession.addEventListener('end', () => exitARMode());
    
    const xrRefSpace = await arSession.requestReferenceSpace('local');
    referenceSpace = xrRefSpace;
    
    hitTestSource = await arSession.requestHitTestSource({ space: referenceSpace });
    
    // بدء حلقة الرسم
    arRenderer.setAnimationLoop((time, frame) => {
      if (frame) {
        const hitTestResults = frame.getHitTestResults(hitTestSource);
        if (hitTestResults.length > 0 && !arMind.userPlaced) {
          const hit = hitTestResults[0];
          const pose = hit.getPose(referenceSpace);
          if (pose) {
            currentPosition.x = pose.transform.position.x;
            currentPosition.y = pose.transform.position.y + 0.15;
            currentPosition.z = pose.transform.position.z;
            arMind.position.set(currentPosition.x, currentPosition.y, currentPosition.z);
            arMind.userPlaced = true;
            if (window.SkyUI) SkyUI.showToast("تم وضع العقل على السطح", "success");
          }
        }
        
        // تحديث دوران الحلقة والجسيمات
        if (arMind) {
          arMind.rotation.y += 0.01;
          if (arRing) arRing.rotation.z += 0.02;
          if (arParticles) arParticles.rotation.y += 0.005;
        }
        
        // تحديث لون العقل حسب المزاج الحالي
        if (arMind && currentArMood) {
          const targetColor = arMoodColors[currentArMood] || arMoodColors.neutral;
          if (arMind.material.color.getHex() !== targetColor) {
            arMind.material.color.setHex(targetColor);
          }
        }
      }
      
      if (arRenderer && arScene && arCamera) {
        arRenderer.render(arScene, arCamera);
      }
    });
    
    await arSession.updateRenderState({
      baseLayer: new XRWebGLLayer(arSession, gl)
    });
    
    arCamera = arRenderer.xr.getCamera();
    
    if (window.SkyUI) SkyUI.showToast("✅ الواقع المعزز نشط - حرك الكاميرا لوضع العقل", "success");
    
  } catch (error) {
    console.error(error);
    if (window.SkyUI) SkyUI.showToast("فشل تفعيل الواقع المعزز: " + error.message, "error");
    else alert("فشل تفعيل الواقع المعزز");
  }
}

function exitARMode() {
  if (arSession) {
    arSession.end();
    arSession = null;
  }
  if (arRenderer) {
    arRenderer.setAnimationLoop(null);
    arRenderer.dispose();
    arRenderer = null;
  }
  if (hitTestSource) {
    hitTestSource.cancel();
    hitTestSource = null;
  }
  arMind = null;
  arParticles = null;
  arRing = null;
  arScene = null;
  arCamera = null;
  if (window.SkyUI) SkyUI.showToast("تم إنهاء الواقع المعزز", "info");
}

// تحديث حالة العقل في AR (يتم استدعاؤها من SkyMind)
function updateARMood(mood) {
  currentArMood = mood;
  if (arMind && arMind.material) {
    const targetColor = arMoodColors[mood] || arMoodColors.neutral;
    arMind.material.color.setHex(targetColor);
    // تأثير وميض
    arMind.material.emissiveIntensity = 0.9;
    setTimeout(() => {
      if (arMind) arMind.material.emissiveIntensity = 0.5;
    }, 300);
  }
}

// تفعيل تأثير التفكير في AR
function triggerARThinking() {
  if (!arMind) return;
  const originalColor = arMind.material.color.getHex();
  arMind.material.color.setHex(0xf59e0b);
  arMind.material.emissiveIntensity = 1.0;
  setTimeout(() => {
    if (arMind) {
      arMind.material.color.setHex(arMoodColors[currentArMood] || arMoodColors.neutral);
      arMind.material.emissiveIntensity = 0.5;
    }
  }, 800);
}

// الاستماع لأحداث العقل لتحديث AR
function bindAREvents() {
  window.addEventListener('mind-mood-change', (e) => {
    if (arSession) updateARMood(e.detail.mood);
  });
  window.addEventListener('mind-think', () => {
    if (arSession) triggerARThinking();
  });
}

// ربط الزر
window.addEventListener('load', () => {
  const arButton = document.getElementById('ar-button');
  if (arButton) {
    arButton.addEventListener('click', enterARMode);
  }
  bindAREvents();
});

// تصدير الواجهة للاستخدام الخارجي
window.ARController = {
  enter: enterARMode,
  exit: exitARMode,
  updateMood: updateARMood,
  triggerThinking: triggerARThinking
};
