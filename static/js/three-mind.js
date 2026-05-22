// ======================================================
// SkyOS v10 — Three.js Holographic Mind (النسخة الثورية)
// ======================================================

let scene, camera, renderer;
let mindMesh;
let animationFrame;

function initThreeMind() {
  const container = document.getElementById('mind-container');
  if (!container) return;

  // إنشاء المشهد
  scene = new THREE.Scene();

  // الكاميرا
  camera = new THREE.PerspectiveCamera(
    75,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.z = 5;

  // الرندر
  renderer = new THREE.WebGLRenderer({ 
    antialias: true, 
    alpha: true,
    powerPreference: "high-performance"
  });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // إضاءة
  const ambientLight = new THREE.AmbientLight(0x6366f1, 0.6);
  scene.add(ambientLight);

  const pointLight = new THREE.PointLight(0xa78bfa, 1.2, 100);
  pointLight.position.set(5, 5, 5);
  scene.add(pointLight);

  // إنشاء العقل الهولوغرافي (كرة مع تأثير)
  const geometry = new THREE.IcosahedronGeometry(1.8, 1);
  const material = new THREE.MeshPhongMaterial({
    color: 0x6366f1,
    emissive: 0x1e1b4b,
    shininess: 80,
    wireframe: false,
    transparent: true,
    opacity: 0.85
  });

  mindMesh = new THREE.Mesh(geometry, material);
  scene.add(mindMesh);

  // إضافة حلقة خارجية
  const ringGeometry = new THREE.TorusGeometry(2.6, 0.04, 16, 100);
  const ringMaterial = new THREE.MeshPhongMaterial({
    color: 0xa78bfa,
    emissive: 0x4c1d95,
    shininess: 100
  });
  const ring = new THREE.Mesh(ringGeometry, ringMaterial);
  ring.rotation.x = Math.PI / 2;
  scene.add(ring);

  // حدث تغيير الحجم
  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });

  // تشغيل الحركة
  animateMind();
}

function animateMind() {
  animationFrame = requestAnimationFrame(animateMind);

  if (mindMesh) {
    mindMesh.rotation.y += 0.003;
    mindMesh.rotation.x = Math.sin(Date.now() * 0.0005) * 0.1;
  }

  renderer.render(scene, camera);
}

// دالة لتفعيل تأثير "التفكير"
function triggerMindThinking() {
  if (!mindMesh) return;

  const originalColor = mindMesh.material.color.getHex();
  mindMesh.material.color.setHex(0xa78bfa);

  setTimeout(() => {
    if (mindMesh) {
      mindMesh.material.color.setHex(originalColor);
    }
  }, 1200);
}

// تصدير الدوال لاستخدامها من ملفات أخرى
window.SkyMind3D = {
  init: initThreeMind,
  triggerThinking: triggerMindThinking
};

// تشغيل تلقائي عند تحميل الصفحة
window.addEventListener('load', () => {
  if (document.getElementById('mind-container')) {
    initThreeMind();
  }
});
