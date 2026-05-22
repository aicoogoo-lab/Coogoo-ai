// ======================================================
// SkyOS v10 — WebXR AR Controller (النسخة الثورية)
// ======================================================

let arSession = null;
let arRenderer = null;
let arScene = null;
let arCamera = null;

async function enterARMode() {
  if (!navigator.xr) {
    SkyUI.showToast("المتصفح لا يدعم الواقع المعزز");
    return;
  }

  try {
    const supported = await navigator.xr.isSessionSupported('immersive-ar');
    if (!supported) {
      SkyUI.showToast("الواقع المعزز غير مدعوم على هذا الجهاز");
      return;
    }

    arSession = await navigator.xr.requestSession('immersive-ar', {
      requiredFeatures: ['local-floor', 'hit-test']
    });

    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl', { xrCompatible: true });

    arRenderer = new THREE.WebGLRenderer({
      canvas: canvas,
      context: gl,
      alpha: true,
      preserveDrawingBuffer: true
    });
    arRenderer.xr.enabled = true;

    arScene = new THREE.Scene();
    arCamera = new THREE.PerspectiveCamera();

    // إضافة نموذج بسيط في الواقع المعزز
    const geometry = new THREE.IcosahedronGeometry(0.3, 1);
    const material = new THREE.MeshPhongMaterial({
      color: 0x6366f1,
      emissive: 0x1e1b4b,
      transparent: true,
      opacity: 0.9
    });
    const arMind = new THREE.Mesh(geometry, material);
    arMind.position.set(0, 1, -1);
    arScene.add(arMind);

    const light = new THREE.HemisphereLight(0xffffff, 0x444444);
    arScene.add(light);

    arRenderer.setAnimationLoop(() => {
      arRenderer.render(arScene, arCamera);
    });

    await arSession.updateRenderState({
      baseLayer: new XRWebGLLayer(arSession, gl)
    });

    const referenceSpace = await arSession.requestReferenceSpace('local-floor');
    arRenderer.xr.setReferenceSpace(referenceSpace);

    SkyUI.showToast("تم تفعيل الواقع المعزز");

    arSession.addEventListener('end', () => {
      exitARMode();
    });

  } catch (error) {
    console.error(error);
    SkyUI.showToast("فشل تفعيل الواقع المعزز");
  }
}

function exitARMode() {
  if (arSession) {
    arSession.end();
    arSession = null;
  }
  if (arRenderer) {
    arRenderer.setAnimationLoop(null);
    arRenderer = null;
  }
  SkyUI.showToast("تم إنهاء الواقع المعزز");
}

// ربط الزر
window.addEventListener('load', () => {
  const arButton = document.getElementById('ar-button');
  if (arButton) {
    arButton.addEventListener('click', enterARMode);
  }
});
