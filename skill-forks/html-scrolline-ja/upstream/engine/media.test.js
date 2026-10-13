import { afterEach, describe, expect, it, vi } from 'vitest';
import { frameSequence, loadOrder, pickTier, textMask, videoClip } from './media.js';

const manifest = {
  version: 1,
  fps: 24,
  count: 30,
  width: 1920,
  height: 1080,
  pattern: 'f_%04d.webp',
  tiers: { 1920: '1920/', 960: '960/' },
  poster: 'poster.webp',
};
afterEach(() => {
  vi.restoreAllMocks();
  document.body.replaceChildren();
});
describe('media', () => {
  it('chooses the specified resolution boundary and prioritises coarse frames', () => {
    expect(pickTier(manifest, { w: 699, dpr: 2 })).toBe(960);
    expect(pickTier(manifest, { w: 701, dpr: 2 })).toBe(1920);
    expect(loadOrder(30, 15).slice(0, 4)).toEqual([0, 8, 16, 24]);
    expect(new Set(loadOrder(30, 15)).size).toBe(30);
  });
  it('rounds progress to the closest frame and draws the closest loaded preceding frame', async () => {
    const requested = [];
    const original = globalThis.Image;
    class FakeImage {
      constructor() {
        this.width = 100;
        this.height = 50;
      }
      set src(value) {
        requested.push(value);
        queueMicrotask(() => this.onload());
      }
    }
    globalThis.Image = FakeImage;
    const context = { clearRect: vi.fn(), drawImage: vi.fn() };
    vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(context);
    const seq = frameSequence(document.body, manifest, { viewport: { w: 400, dpr: 1 } });
    seq.setProgress(0.51);
    await seq.ready();
    expect(requested[0]).toBe('poster.webp');
    expect(requested[1]).toBe('960/f_0001.webp');
    expect(context.drawImage).toHaveBeenCalled();
    seq.destroy();
    globalThis.Image = original;
  });
  it('creates export-safe live clips and valid SVG masks', () => {
    const clip = videoClip(
      document.body,
      { src: 'movie.mp4', poster: 'p.webp', mode: 'loop' },
      { exportMode: true },
    );
    clip.bindExport({ start: 1.25, duration: 3 });
    expect(clip.el.outerHTML).toContain('data-start="1.25"');
    expect(clip.el.hasAttribute('crossorigin')).toBe(false);
    expect(
      decodeURIComponent(textMask('A&B', { font: '700 80px sans-serif', width: 300, height: 100 })),
    ).toContain('<svg');
    clip.destroy();
  });
});
