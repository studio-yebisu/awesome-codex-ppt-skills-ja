import { afterEach, expect, it, vi } from 'vitest';
import { frameSequence } from './media.js';

const manifest = {
  version: 1,
  fps: 24,
  count: 30,
  width: 1920,
  height: 1080,
  pattern: 'f_%04d.webp',
  tiers: { 960: '960/' },
  poster: 'poster.webp',
};
afterEach(() => vi.restoreAllMocks());

// 회귀(launch 통합): manifest 로드 전 setProgress를 버려 부팅 직후 정지점 seek가 프레임 0에 고정됐다.
it('keeps a progress set before the manifest arrives and draws that frame once loaded', async () => {
  const requested = [];
  const original = globalThis.Image;
  globalThis.Image = class {
    width = 100;
    height = 50;
    set src(value) {
      this.url = value;
      requested.push(value);
      queueMicrotask(() => this.onload());
    }
  };
  const drawn = [];
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue({
    clearRect() {},
    drawImage: (image) => drawn.push(image),
  });
  let resolve;
  vi.stubGlobal('fetch', () => new Promise((r) => (resolve = r)));
  const seq = frameSequence(document.body, '/frames/manifest.json', { viewport: { w: 400, dpr: 1 } });
  expect(seq.count).toBe(0);
  seq.setProgress(0.42); // round(0.42 × 29) = 12
  resolve({ ok: true, json: async () => manifest });
  await seq.ready();
  expect(drawn.at(-1).url).toBe('/frames/960/f_0013.webp');
  // 캡처 도구용: 원하는 프레임과 실제 그린 프레임
  expect(seq.canvas.dataset).toMatchObject({ frame: '12', drawn: '12' });
  expect(requested[0]).toBe('/frames/poster.webp');
  seq.destroy();
  globalThis.Image = original;
  vi.unstubAllGlobals();
});
