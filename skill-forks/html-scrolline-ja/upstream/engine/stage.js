import { MAX_TILT, SLOT_DEFAULTS, SLOTS } from './constants.js';

/**
 * C2 뷰포트 식. portrait = w/h <= 1, px = portrait ? w/760 : min(w, h*16/9)/1920, dpr = min(dpr, 2)
 * @param {number} w
 * @param {number} h
 * @param {number} [dpr]
 * @returns {import('./types.js').Viewport}
 */
export function computeViewport(w, h, dpr = 1) {
  const portrait = w / h <= 1;
  return {
    w,
    h,
    portrait,
    px: portrait ? w / 760 : Math.min(w, h * (16 / 9)) / 1920,
    dpr: Math.min(dpr || 1, 2),
  };
}

/**
 * 무대를 host 안에 만든다. stage 루트에 --px, --vw-px, --vh-px, --sl-portrait와 class sl-concept-<id> 설정.
 * mode 'export'면 1920×1080 고정 크기.
 * @param {HTMLElement} host
 * @param {{ viewport: import('./types.js').Viewport, concept: import('./types.js').ConceptPack, mode?: 'live'|'export' }} opts
 * @returns {import('./types.js').Stage}
 */
export function createStage(host, opts) {
  const { viewport, concept, mode = 'live' } = opts;
  const root = document.createElement('div');
  root.className = `sl-stage sl-concept-${concept.id}`;
  root.dataset.mode = mode;
  root.style.setProperty('--px', String(viewport.px));
  root.style.setProperty('--vw-px', `${viewport.w}px`);
  root.style.setProperty('--vh-px', `${viewport.h}px`);
  root.style.setProperty('--sl-portrait', viewport.portrait ? '1' : '0');
  if (mode === 'export') {
    root.style.width = '1920px';
    root.style.height = '1080px';
  }
  const viewportEl = document.createElement('div');
  viewportEl.className = 'sl-viewport';
  const camera = document.createElement('div');
  camera.className = 'sl-camera';
  const world = document.createElement('div');
  world.className = 'sl-world';
  const screen = document.createElement('div');
  screen.className = 'sl-screen';
  const overlay = document.createElement('div');
  overlay.className = 'sl-overlay';
  camera.append(world);
  viewportEl.append(camera);
  root.append(viewportEl, screen, overlay);
  host.append(root);
  const slotClasses = SLOTS.map((slot) => `sl-slot-${slot}`);
  const clamp = (n) => Math.max(-MAX_TILT, Math.min(MAX_TILT, Number(n) || 0));
  return {
    root,
    viewportEl,
    camera,
    world,
    screen,
    overlay,
    viewport,
    placeBeat(beatRoot, place = { slot: 'center' }) {
      beatRoot.classList.remove(...slotClasses, 'sl-place-world');
      beatRoot.style.removeProperty('inset');
      beatRoot.style.removeProperty('max-width');
      beatRoot.style.removeProperty('translate');
      beatRoot.style.removeProperty('scale');
      if ('world' in place) {
        const { x, y, z = 0, s = 1 } = place.world;
        beatRoot.classList.add('sl-place-world');
        beatRoot.style.left = `${x * viewport.w}px`;
        beatRoot.style.top = `${y * viewport.h}px`;
        beatRoot.style.translate = `0 0 ${z}px`;
        beatRoot.style.scale = String(s);
        beatRoot.style.transformOrigin = '0 0';
        world.append(beatRoot);
        return;
      }
      const slot = place.slot || 'center';
      if (!SLOTS.includes(slot)) throw new Error(`Unknown stage slot: ${slot}`);
      beatRoot.classList.add(`sl-slot-${slot}`);
      if (slot === 'full') {
        beatRoot.style.inset = '0';
      } else {
        const override = concept.slots?.[slot] ?? {};
        const spec = { ...SLOT_DEFAULTS[slot], ...override };
        beatRoot.style.left = `${spec.x * 100}%`;
        beatRoot.style.top = `${spec.y * 100}%`;
        beatRoot.style.translate = `${-spec.ax * 100}% ${-spec.ay * 100}%`;
        if (spec.w != null) beatRoot.style.maxWidth = `${spec.w * 100}%`;
      }
      screen.append(beatRoot);
    },
    cameraVars({ x, y, s, rx = 0, ry = 0 }) {
      const rotationX = clamp(rx),
        rotationY = clamp(ry);
      if ((Number(rx) || 0) !== rotationX || (Number(ry) || 0) !== rotationY)
        console.warn(`Scrolline camera tilt was clamped to ±${MAX_TILT}°`);
      const scale = Number(s) || 1;
      return {
        x: viewport.w / 2 - (Number(x) || 0) * viewport.w * scale,
        y: viewport.h / 2 - (Number(y) || 0) * viewport.h * scale,
        scale,
        rotationX,
        rotationY,
        transformOrigin: '0 0',
      };
    },
    overlayFor(key) {
      let node = [...overlay.children].find((child) => child.dataset.overlayKey === key);
      if (!node) {
        node = document.createElement('div');
        node.className = 'sl-move-overlay';
        node.dataset.overlayKey = key;
        overlay.append(node);
      }
      return node;
    },
    clear() {
      world.replaceChildren();
      screen.replaceChildren();
      overlay.replaceChildren();
    },
  };
}
