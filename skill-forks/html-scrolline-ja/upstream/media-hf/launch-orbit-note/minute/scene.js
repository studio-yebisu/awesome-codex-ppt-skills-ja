// Shared, deterministic Minute product scene. MEDIA-L2 imports this module.
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
export const END_STATE = Object.freeze({ elev: 6, yaw: 300, halo: 1, haloArc: 1, explode: [0, 0, 0, 0, 0, 0] });

const DEG = Math.PI / 180;
const mm = (v) => v;

function annulus(THREE, outer, inner, material, segments = 128) {
  const shape = new THREE.Shape();
  shape.absarc(0, 0, outer, 0, Math.PI * 2, false);
  const hole = new THREE.Path();
  hole.absarc(0, 0, inner, 0, Math.PI * 2, true);
  shape.holes.push(hole);
  return new THREE.Mesh(new THREE.ShapeGeometry(shape, segments), material);
}

function roundedBox(THREE, w, h, d, r, material) {
  const g = new THREE.BoxGeometry(w, h, d, 5, 2, 2);
  g.computeVertexNormals();
  const mesh = new THREE.Mesh(g, material);
  // A small bevel is the visible cue; the geometry remains lightweight and deterministic.
  mesh.scale.set(1, 1, 1);
  return mesh;
}

function makeContactShadow(THREE) {
  const shadowCanvas = document.createElement('canvas');
  shadowCanvas.width = shadowCanvas.height = 256;
  const context = shadowCanvas.getContext('2d');
  const gradient = context.createRadialGradient(128, 128, 18, 128, 128, 128);
  gradient.addColorStop(0, 'rgba(0,0,0,0.30)');
  gradient.addColorStop(0.52, 'rgba(0,0,0,0.12)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  context.fillStyle = gradient;
  context.fillRect(0, 0, 256, 256);
  const texture = new THREE.CanvasTexture(shadowCanvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(
    new THREE.PlaneGeometry(118, 86),
    new THREE.MeshBasicMaterial({ map: texture, transparent: true, depthWrite: false }),
  );
}

export function createMinute({ THREE, canvas, width, height }) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, preserveDrawingBuffer: true });
  renderer.setSize(width, height, false);
  renderer.setPixelRatio(1);
  renderer.setClearColor(0x050506, 1);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  // Keep the black stage, but expose the product for material read rather than
  // treating it as a silhouette. ACES keeps the amber halo from clipping.
  renderer.toneMappingExposure = 1.25;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050506);
  // The studio environment only informs material reflections. The black stage
  // remains a deliberate background while the matte body gets a soft form read.
  const pmremGenerator = new THREE.PMREMGenerator(renderer);
  scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.28;
  pmremGenerator.dispose();
  const camera = new THREE.PerspectiveCamera(28, width / height, 1, 1000);
  const product = new THREE.Group();
  scene.add(product);

  const bodyMat = new THREE.MeshPhysicalMaterial({ color: 0x303136, metalness: 0.88, roughness: 0.62, clearcoat: 0.14, clearcoatRoughness: 0.58 });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x15161a, metalness: 0.25, roughness: 0.65 });
  const rubberMat = new THREE.MeshStandardMaterial({ color: 0x0b0b0c, roughness: 0.82 });
  const boardMat = new THREE.MeshStandardMaterial({ color: 0x183127, metalness: 0.25, roughness: 0.42 });
  const goldMat = new THREE.MeshStandardMaterial({ color: 0xb88935, metalness: 0.85, roughness: 0.28 });
  const chipMat = new THREE.MeshPhysicalMaterial({ color: 0x202126, metalness: 0.65, roughness: 0.3 });
  const batteryMat = new THREE.MeshStandardMaterial({ color: 0x3b3c40, metalness: 0.18, roughness: 0.45 });
  const haloMat = new THREE.MeshStandardMaterial({ color: 0x3a3a3f, metalness: 0.25, roughness: 0.42, emissive: 0xffb648, emissiveIntensity: 0.02 });
  const arcMat = haloMat.clone();

  const textureLoader = new THREE.TextureLoader();
  const fabric = textureLoader.load(new URL('./textures/fabric-tile.png', import.meta.url).href);
  fabric.colorSpace = THREE.SRGBColorSpace;
  fabric.wrapS = fabric.wrapT = THREE.RepeatWrapping;
  fabric.repeat.set(7, 7);
  const normal = textureLoader.load(new URL('./textures/fabric-normal.png', import.meta.url).href);
  normal.wrapS = normal.wrapT = THREE.RepeatWrapping;
  normal.repeat.set(7, 7);
  // The albedo is deliberately lifted: the tile carries the charcoal knit
  // detail while the normal map catches the top key light at every angle.
  const fabricMat = new THREE.MeshPhysicalMaterial({ color: 0x1f2125, map: fabric, normalMap: normal, normalScale: new THREE.Vector2(1.0, 1.0), roughness: 0.72, metalness: 0.0, sheen: 1, sheenColor: new THREE.Color(0xbcbcb8), sheenRoughness: 0.5 });

  // Six separated assemblies that read as one sealed product while explode=0.
  const layers = Array.from({ length: 6 }, () => new THREE.Group());
  layers.forEach((layer) => product.add(layer));

  const profile = [
    [45.4, -12], [47.2, -10.5], [48, -9], [48, 9], [47.2, 10.5], [45.4, 12],
  ].map(([r, y]) => new THREE.Vector2(mm(r), mm(y)));
  const body = new THREE.Mesh(new THREE.LatheGeometry(profile, 256), bodyMat);
  body.rotation.x = Math.PI / 2;
  layers[5].add(body);
  const pad = new THREE.Mesh(new THREE.CylinderGeometry(34, 34, 1.4, 96), rubberMat);
  pad.rotation.x = Math.PI / 2;
  pad.position.z = -12.25;
  layers[5].add(pad);

  // A nearly-black stage gives the product a quiet floor relationship without
  // turning the background into a lit set. The two discs are a bounded,
  // deterministic contact shadow and an intentionally faint reflected read.
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(700, 700), new THREE.MeshBasicMaterial({ color: 0x07080a }));
  floor.position.z = -13.05;
  scene.add(floor);
  const reflection = new THREE.Mesh(new THREE.CircleGeometry(43, 96), new THREE.MeshBasicMaterial({ color: 0x28313b, transparent: true, opacity: 0.16, depthWrite: false }));
  reflection.position.z = -13.0;
  scene.add(reflection);
  const contactShadow = makeContactShadow(THREE);
  contactShadow.position.z = -12.94;
  scene.add(contactShadow);

  const top = new THREE.Mesh(new THREE.CylinderGeometry(45.2, 45.2, 0.9, 192), fabricMat);
  top.rotation.x = Math.PI / 2;
  top.position.z = 12.15;
  layers[0].add(top);

  const halo = annulus(THREE, 44.0, 42.0, haloMat, 192);
  halo.position.z = 12.72;
  layers[1].add(halo);
  const arc = new THREE.Mesh(new THREE.TorusGeometry(43, 0.94, 10, 96, Math.PI / 3), arcMat);
  arc.rotation.z = 150 * DEG;
  arc.position.z = 12.78;
  layers[1].add(arc);

  const micBoard = new THREE.Mesh(new THREE.CylinderGeometry(39.5, 39.5, 0.8, 128), boardMat);
  micBoard.rotation.x = Math.PI / 2;
  micBoard.position.z = 11.25;
  layers[2].add(micBoard);
  for (let i = 0; i < 8; i += 1) {
    const a = i * 45 * DEG;
    const x = Math.cos(a) * 39.5;
    const y = Math.sin(a) * 39.5;
    const hole = new THREE.Mesh(new THREE.CircleGeometry(0.55, 20), new THREE.MeshBasicMaterial({ color: 0x030304 }));
    hole.position.set(x, y, 12.73);
    layers[0].add(hole);
    const mems = new THREE.Mesh(new THREE.BoxGeometry(3, 2.2, 0.7), chipMat);
    mems.position.set(x, y, 11.85);
    layers[2].add(mems);
    const gold = new THREE.Mesh(new THREE.CircleGeometry(1.15, 20), goldMat);
    gold.position.set(x * 0.9, y * 0.9, 11.7);
    layers[2].add(gold);
  }

  const main = new THREE.Mesh(new THREE.CylinderGeometry(37, 37, 1.2, 128), boardMat);
  main.rotation.x = Math.PI / 2;
  main.position.z = 8.7;
  layers[3].add(main);
  const heat = roundedBox(THREE, 24, 24, 2.2, 2, chipMat);
  heat.position.z = 9.65;
  layers[3].add(heat);
  const npuMark = new THREE.Mesh(new THREE.BoxGeometry(10, 10, 0.35), goldMat);
  npuMark.position.z = 10.9;
  layers[3].add(npuMark);

  const battery = roundedBox(THREE, 52, 38, 4.5, 3, batteryMat);
  battery.position.z = 4.8;
  layers[4].add(battery);
  const batteryCap = new THREE.Mesh(new THREE.BoxGeometry(42, 28, 0.35), darkMat);
  batteryCap.position.z = 7.15;
  layers[4].add(batteryCap);

  // USB-C is positioned toward the camera when yaw is 300°; the mute button is opposite.
  const port = new THREE.Mesh(new THREE.BoxGeometry(12, 3.5, 1.2), darkMat);
  port.position.set(0, -48.05, -1.2);
  port.rotation.x = Math.PI / 2;
  layers[5].add(port);
  const button = new THREE.Mesh(new THREE.CylinderGeometry(3.3, 3.3, 1, 32), darkMat);
  button.position.set(0, 47.9, -1.2);
  button.rotation.x = Math.PI / 2;
  layers[5].add(button);

  // Three-point studio lighting: warm 45° key, lifted rear rim and restrained
  // fill separate the graphite silhouette while retaining a black stage.
  const rim = new THREE.RectAreaLight(0xe8eef8, 19, 104, 62);
  rim.position.set(-112, 74, 128);
  rim.lookAt(0, 0, 0);
  scene.add(rim);
  const key = new THREE.RectAreaLight(0xfff3e2, 5.5, 142, 108);
  key.position.set(68, -118, 132);
  key.lookAt(0, 0, 3);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xb9c6d5, 2.8);
  fill.position.set(105, -145, 62);
  scene.add(fill);

  const closedZ = [0, 0, 0, 0, 0, 0];
  const explodeZ = [76, 61, 34, 7, -18, 0];
  function renderAt(state) {
    const s = { ...END_STATE, ...state };
    const ex = Array.isArray(s.explode) ? s.explode : closedZ;
    product.rotation.z = s.yaw * DEG;
    product.scale.setScalar(s.scale || 1);
    layers.forEach((layer, i) => { layer.position.z = THREE.MathUtils.lerp(closedZ[i], explodeZ[i], ex[i] || 0); });
    haloMat.emissiveIntensity = 0.02 + 1.15 * s.halo;
    arcMat.emissiveIntensity = 0.02 + 1.8 * s.halo * s.haloArc;
    arc.visible = s.haloArc > 0.001;

    const elev = s.elev * DEG;
    const distance = 232;
    camera.position.set(0, -Math.cos(elev) * distance, Math.sin(elev) * distance);
    camera.lookAt(0, 0, 0);
    const center = s.center || { x: 0.62, y: 0.52 };
    camera.setViewOffset(width, height, width * 0.5 - width * center.x, height * 0.5 - height * center.y, width, height);
    camera.updateProjectionMatrix();
    renderer.render(scene, camera);
  }

  return { renderAt };
}
