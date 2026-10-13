/** Media primitives for deterministic image-sequence and live-video beats (C13). */
import { FRAMES } from './constants.js';

/** @param {import('./types.js').FramesManifest} manifest @param {{ w: number, dpr: number }} viewport */
export function pickTier(manifest, viewport) {
  const available = Object.keys(manifest.tiers ?? {})
    .map(Number)
    .filter(Number.isFinite)
    .sort((a, b) => a - b);
  if (!available.length) throw new Error('frames manifest has no tiers');
  if (viewport.w * viewport.dpr >= FRAMES.bigTierMinPx) return available.at(-1);
  return available.includes(FRAMES.smallTier) ? FRAMES.smallTier : available[0];
}

/** @param {number} count @param {number} current */
export function loadOrder(count, current) {
  if (!Number.isInteger(count) || count < 1) return [];
  const at = Math.max(0, Math.min(count - 1, Math.round(current)));
  const seen = new Set();
  const add = (i) => {
    if (i >= 0 && i < count) seen.add(i);
  };
  for (let i = 0; i < count; i += FRAMES.coarseStep) add(i);
  for (let i = at - FRAMES.window; i <= at + FRAMES.window; i += 1) add(i);
  for (let i = 0; i < count; i += 1) add(i);
  return [...seen];
}
function directory(url) {
  const slash = url.lastIndexOf('/');
  return slash < 0 ? '' : url.slice(0, slash + 1);
}
function formatPattern(pattern, frame) {
  return pattern.replace(/%(0?)(\d*)d/, (_all, zero, width) =>
    String(frame).padStart(Number(width) || 0, zero ? '0' : ' '),
  );
}
function imageLoad(url) {
  return new Promise((resolve) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => resolve(null);
    image.src = url;
  });
}

/** @param {{ progress?: number, index?: number }} want @param {number} count */
function frameFor(want, count) {
  const raw = want.index ?? (want.progress ?? 0) * (count - 1);
  return Math.max(0, Math.min(count - 1, Math.round(Number.isFinite(raw) ? raw : 0)));
}

/** @param {HTMLElement} host @param {import('./types.js').FramesManifest | string} source @param {{ fit?: 'cover'|'contain', tier?: number, viewport?: import('./types.js').Viewport }} [opts] */
export function frameSequence(host, source, opts = {}) {
  const canvas = document.createElement('canvas');
  canvas.className = 'sl-frame-sequence';
  canvas.style.objectFit = opts.fit ?? 'cover';
  host.append(canvas);
  let destroyed = false;
  let manifest;
  let base = '';
  let current = 0;
  // manifest 전에 온 setProgress·setFrame(부팅 직후 정지점 seek·발표 키 점프)은 버리지 않고 도착 뒤 적용한다.
  let pending = null;
  let posterImage;
  const loaded = new Map();
  let started;
  // canvas.dataset.frame = 원하는 프레임, dataset.drawn = 실제로 그린 프레임(-1 = poster). 캡처 도구가 둘이 같아질 때까지 기다린다.
  const draw = (wanted) => {
    canvas.dataset.frame = String(wanted);
    if (!manifest || destroyed) return;
    let image;
    let drawn = -1;
    for (let i = Math.min(wanted, manifest.count - 1); i >= 0; i -= 1)
      if (loaded.has(i)) {
        image = loaded.get(i);
        drawn = i;
        break;
      }
    image ??= posterImage;
    const context = canvas.getContext?.('2d');
    if (!context || !image) return;
    context.clearRect(0, 0, canvas.width, canvas.height);
    const scale =
      (opts.fit ?? 'cover') === 'contain'
        ? Math.min(canvas.width / image.width, canvas.height / image.height)
        : Math.max(canvas.width / image.width, canvas.height / image.height);
    const w = image.width * scale;
    const h = image.height * scale;
    context.drawImage(image, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h);
    canvas.dataset.drawn = String(drawn);
  };
  const start = async () => {
    if (typeof source === 'string') {
      const response = await fetch(source);
      if ('ok' in response && !response.ok) throw new Error(`could not load frames manifest: ${source}`);
      manifest = await response.json();
      base = directory(source);
    } else manifest = source;
    canvas.width = manifest.width;
    canvas.height = manifest.height;
    if (pending) current = frameFor(pending, manifest.count);
    pending = null;
    const viewport = opts.viewport ?? {
      w: window.innerWidth || manifest.width,
      dpr: window.devicePixelRatio || 1,
    };
    const tier = opts.tier ?? pickTier(manifest, viewport);
    const prefix = `${base}${manifest.tiers[String(tier)] ?? manifest.tiers[tier] ?? ''}`;
    posterImage = await imageLoad(`${base}${manifest.poster}`);
    draw(current);
    for (const index of loadOrder(manifest.count, current)) {
      if (destroyed) return;
      const image = await imageLoad(`${prefix}${formatPattern(manifest.pattern, index + 1)}`);
      if (image) {
        loaded.set(index, image);
        draw(current);
      }
    }
  };
  const ready = () => (started ??= start());
  void ready();
  return {
    canvas,
    get count() {
      return manifest?.count ?? (typeof source === 'string' ? 0 : source.count);
    },
    setProgress(progress) {
      const count = manifest?.count ?? (typeof source === 'string' ? 0 : source.count);
      if (!count) return void (pending = { progress: Number(progress) });
      current = frameFor({ progress: Number(progress) }, count);
      draw(current);
    },
    setFrame(index) {
      const count = manifest?.count ?? (typeof source === 'string' ? 0 : source.count);
      if (!count) return void (pending = { index: Number(index) });
      current = frameFor({ index: Number(index) }, count);
      draw(current);
    },
    ready,
    preloadAll: ready,
    destroy() {
      destroyed = true;
      canvas.remove();
      loaded.clear();
    },
  };
}

/** @param {HTMLElement} host @param {{ src: string, poster?: string, loop?: boolean, mode: 'play'|'loop' }} spec @param {{ exportMode: boolean }} opts */
export function videoClip(host, spec, opts) {
  const el = document.createElement('video');
  el.src = spec.src;
  if (spec.poster) el.poster = spec.poster;
  el.muted = true;
  el.playsInline = true;
  el.preload = 'metadata';
  el.loop = Boolean(spec.loop ?? spec.mode === 'loop');
  host.append(el);
  const activate = () => {
    if (!opts.exportMode) void el.play().catch(() => {});
  };
  const deactivate = () => el.pause();
  // C13 v2: activate/deactivate는 boot가 window `scrolline:active`에 맞춰 부른다(host 리스너 없음).
  return {
    el,
    activate,
    deactivate,
    bindExport({ start, duration }) {
      el.dataset.start = String(start);
      el.dataset.duration = String(duration);
    },
    destroy() {
      deactivate();
      el.remove();
    },
  };
}
const xmlEscape = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[c],
  );
/**
 * mask-image용 SVG data URL. 배경 투명·글자 흰색(불투명) — mask는 alpha로 읽으므로 글자 모양만 보인다.
 * @param {string} text @param {{ font: string, width: number, height: number, align?: 'center'|'left' }} opts
 */
export function textMask(text, opts) {
  const center = (opts.align ?? 'center') === 'center';
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${opts.width}" height="${opts.height}" viewBox="0 0 ${opts.width} ${opts.height}"><text x="${center ? '50%' : '0'}" y="50%" fill="white" text-anchor="${center ? 'middle' : 'start'}" dominant-baseline="middle" style="font:${xmlEscape(opts.font)}">${xmlEscape(text)}</text></svg>`;
  return `data:image/svg+xml,${encodeURIComponent(svg)}`;
}
/** @param {string[]} urls */
export async function preloadImages(urls) {
  await Promise.all(
    urls.map(
      (url) =>
        new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = async () => {
            try {
              if (image.decode) await image.decode();
              resolve();
            } catch (error) {
              reject(error);
            }
          };
          image.onerror = () => reject(new Error(`could not load image: ${url}`));
          image.src = url;
        }),
    ),
  );
}
