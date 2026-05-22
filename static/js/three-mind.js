// ======================================================
// SkyOS v10 — Three.js Holographic Mind (نسخة ثورية متكاملة)
// يدعم: جسيمات، تفاعل باللمس/الفارة، تأثيرات المزاج، أحداث العقل
// ======================================================

let scene, camera, renderer, controls;
let mindMesh, ring1, ring2, particleSystem;
let animationFrame;
let isUserInteracting = false;
let targetRotation = { y: 0, x: 0 };
let currentColor = 0x6366f1;
let pulseIntensity = 0;

// تكوين الألوان حسب المزاج
const moodColors = {
  neutral: 0x6366f1,    // أزرق بنفسجي
  happy: 0x4ade80,      // أخضر زاهي
  excited: 0xf59e0b,    // برتقالي
  thoughtful: 0x8b5cf6, // بنفسجي غامق
  calm: 0x06b6d4,       // أزرق سماوي
  sad: 0xef4444         // أحمر ناعم
};

function initThreeMind() {
  const container = document.getElementById('mind-container');
  if (!container) return;

  // المشهد
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050507);
  scene.fog = new THREE.FogExp2(0x050507, 0.008);

  // الكاميرا
  camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.set(0, 1, 6);
  camera.lookAt(0, 0, 0);

  // الرندر
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x050507, 1);
  container.appendChild(renderer.domElement);

  // الإضاءة المتقدمة
  const ambientLight = new THREE.AmbientLight(0x1a1a2e, 0.5);
  scene.add(ambientLight);
  
  const mainLight = new THREE.DirectionalLight(0xffffff, 1);
  mainLight.position.set(2, 5, 3);
  scene.add(mainLight);
  
  const backLight = new THREE.PointLight(0x6366f1, 0.5);
  backLight.position.set(-2, 1, -3);
  scene.add(backLight);
  
  const fillLight = new THREE.PointLight(0xa78bfa, 0.4);
  fillLight.position.set(2, 2, 2);
  scene.add(fillLight);
  
  const pulseLight = new THREE.PointLight(0xa78bfa, 0.8);
  pulseLight.position.set(0, 0, 2);
  scene.add(pulseLight);

  // إنشاء العقل الهولوغرافي (IcosahedronGeometry بمستوى تفصيل أعلى)
  const geometry = new THREE.IcosahedronGeometry(1.4, 1);
  const material = new THREE.MeshStandardMaterial({
    color: currentColor,
    emissive: 0x1e1b4b,
    emissiveIntensity: 0.4,
    metalness: 0.7,
    roughness: 0.3,
    transparent: true,
    opacity: 0.92
  });
  mindMesh = new THREE.Mesh(geometry, material);
  scene.add(mindMesh);

  // إضافة شبكة سلكية خارجية شفافة
  const wireframeMat = new THREE.MeshBasicMaterial({ color: 0xa78bfa, wireframe: true, transparent: true, opacity: 0.15 });
  const wireframeMesh = new THREE.Mesh(geometry, wireframeMat);
  wireframeMesh.scale.setScalar(1.05);
  scene.add(wireframeMesh);

  // الحلقة الداخلية (دوران سريع)
  const ringGeo1 = new THREE.TorusGeometry(1.9, 0.035, 64, 200);
  const ringMat1 = new THREE.MeshStandardMaterial({ color: 0x8b5cf6, emissive: 0x4c1d95, emissiveIntensity: 0.5 });
  ring1 = new THREE.Mesh(ringGeo1, ringMat1);
  ring1.rotation.x = Math.PI / 2;
  scene.add(ring1);

  // الحلقة الخارجية (دوران بطيء مع إمالة)
  const ringGeo2 = new THREE.TorusGeometry(2.3, 0.025, 64, 200);
  const ringMat2 = new THREE.MeshStandardMaterial({ color: 0xa78bfa, emissive: 0x6d28d9, emissiveIntensity: 0.3 });
  ring2 = new THREE.Mesh(ringGeo2, ringMat2);
  ring2.rotation.z = Math.PI / 3;
  scene.add(ring2);

  // نظام الجسيمات (نجوم هولوغرافية)
  const particleCount = 800;
  const particlesGeometry = new THREE.BufferGeometry();
  const particlePositions = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount; i++) {
    // توزيع كروي عشوائي
    const radius = 2.8 + Math.random() * 1.2;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    particlePositions[i*3] = radius * Math.sin(phi) * Math.cos(theta);
    particlePositions[i*3+1] = radius * Math.sin(phi) * Math.sin(theta);
    particlePositions[i*3+2] = radius * Math.cos(phi);
  }
  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  const particleMaterial = new THREE.PointsMaterial({ color: 0xa78bfa, size: 0.03, transparent: true, opacity: 0.6 });
  particleSystem = new THREE.Points(particlesGeometry, particleMaterial);
  scene.add(particleSystem);

  // تفاعل المستخدم (سحب للتدوير)
  let mouseX = 0, mouseY = 0;
  let targetRotationX = 0, targetRotationY = 0;
  
  container.style.cursor = 'grab';
  container.addEventListener('mousedown', () => { isUserInteracting = true; container.style.cursor = 'grabbing'; });
  window.addEventListener('mouseup', () => { isUserInteracting = false; container.style.cursor = 'grab'; });
  container.addEventListener('mousemove', (e) => {
    if (!isUserInteracting) return;
    const rect = container.getBoundingClientRect();
    const deltaX = (e.clientX - rect.left) / rect.width - 0.5;
    const deltaY = (e.clientY - rect.top) / rect.height - 0.5;
    targetRotationY = deltaX * Math.PI;
    targetRotationX = deltaY * Math.PI * 0.5;
  });
  
  // تكبير باللمس (بسيط)
  container.addEventListener('wheel', (e) => {
    camera.position.z += e.deltaY * 0.005;
    camera.position.z = Math.min(8, Math.max(3, camera.position.z));
  });

  // ربط أحداث العقل
  window.addEventListener('mind-think', (e) => triggerMindThinking(e.detail?.intensity || 0.7));
  window.addEventListener('mind-mood-change', (e) => changeMoodColor(e.detail.mood));
  window.addEventListener('mind-meditate', (e) => handleMeditation(e.detail.active));
  window.addEventListener('memory-updated', () => flashMemoryPulse());

  // حدث تغيير الحجم
  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });

  // بدء الحلقة
  animateMind();
}

function animateMind() {
  animationFrame = requestAnimationFrame(animateMind);
  
  const time = Date.now() * 0.001;
  
  // دوران العقل (تفاعل المستخدم + دوران تلقائي خفيف)
  if (mindMesh) {
    if (isUserInteracting) {
      mindMesh.rotation.y = targetRotationY;
      mindMesh.rotation.x = targetRotationX;
    } else {
      mindMesh.rotation.y += 0.002;
      mindMesh.rotation.x = Math.sin(time * 0.3) * 0.1;
    }
  }
  
  // دوران الحلقات
  if (ring1) {
    ring1.rotation.z += 0.008;
    ring1.rotation.y += 0.003;
  }
  if (ring2) {
    ring2.rotation.x += 0.004;
    ring2.rotation.z += 0.002;
  }
  
  // دوران الجسيمات
  if (particleSystem) {
    particleSystem.rotation.y += 0.0005;
    particleSystem.rotation.x += 0.0003;
  }
  
  // تأثير النبض الضوئي
  const pulse = 0.6 + Math.sin(time * 8) * 0.15;
  const pulseLightObj = scene.children.find(c => c instanceof THREE.PointLight && c.position.z === 2);
  if (pulseLightObj) pulseLightObj.intensity = 0.5 + pulseIntensity * 0.8;
  
  renderer.render(scene, camera);
}

// تأثير التفكير المتقدم
function triggerMindThinking(intensity = 0.7) {
  if (!mindMesh) return;
  
  // تغيير اللون مؤقتاً
  const originalColor = mindMesh.material.color.getHex();
  mindMesh.material.color.setHex(0xf59e0b);
  mindMesh.material.emissiveIntensity = 0.8;
  pulseIntensity = 0.9;
  
  // اهتزاز بسيط للكاميرا
  const originalCamZ = camera.position.z;
  let shakeCount = 0;
  const shakeInterval = setInterval(() => {
    if (shakeCount >= 6) {
      camera.position.z = originalCamZ;
      clearInterval(shakeInterval);
      return;
    }
    camera.position.z = originalCamZ + (Math.random() - 0.5) * 0.05;
    shakeCount++;
  }, 30);
  
  setTimeout(() => {
    if (mindMesh) {
      mindMesh.material.color.setHex(currentColor);
      mindMesh.material.emissiveIntensity = 0.4;
      pulseIntensity = 0;
    }
  }, intensity * 1000);
}

// تغيير لون العقل حسب المزاج
function changeMoodColor(mood) {
  const newColor = moodColors[mood] || moodColors.neutral;
  currentColor = newColor;
  if (mindMesh) {
    mindMesh.material.color.setHex(newColor);
    // تأثير وميض عند تغيير المزاج
    mindMesh.material.emissiveIntensity = 0.9;
    setTimeout(() => {
      if (mindMesh) mindMesh.material.emissiveIntensity = 0.4;
    }, 300);
  }
}

// تأثير التأمل (تخفيف الألوان، بطء الدوران)
let originalRingSpeed = { r1z: 0.008, r1y: 0.003, r2x: 0.004, r2z: 0.002 };
function handleMeditation(active) {
  if (active) {
    // دخول التأمل: تخفيف الإضاءة وتبطؤ الحلقات
    if (mindMesh) mindMesh.material.opacity = 0.7;
    if (particleSystem) particleSystem.material.opacity = 0.3;
  } else {
    if (mindMesh) mindMesh.material.opacity = 0.92;
    if (particleSystem) particleSystem.material.opacity = 0.6;
  }
}

// وميض سريع عند إضافة ذاكرة
function flashMemoryPulse() {
  if (!mindMesh) return;
  const originalEmissive = mindMesh.material.emissiveIntensity;
  mindMesh.material.emissiveIntensity = 1.2;
  setTimeout(() => {
    if (mindMesh) mindMesh.material.emissiveIntensity = originalEmissive;
  }, 200);
}

// تصدير الواجهة العامة
window.SkyMind3D = {
  init: initThreeMind,
  triggerThinking: triggerMindThinking,
  changeMood: changeMoodColor,
  setMeditationMode: handleMeditation
};

// التشغيل التلقائي
window.addEventListener('load', () => {
  if (document.getElementById('mind-container')) {
    initThreeMind();
  }
});
