import { afterEach, expect, it, vi } from 'vitest';
import { maskUrl } from './timeline.js';

const beat = (rect) => ({ root: document.createElement('section'), anchor: () => ({ rect }) });
afterEach(() => vi.restoreAllMocks());

// 회귀(kinetic·launch 통합): 폭만 맞춰 「AI」가 프레임 높이를 넘었고, SVG mask는 웹폰트를 못 봤다.
it('caps the glyph at 80% of the rect height and draws on canvas when the browser has one', () => {
  const calls = [];
  const fake = {
    font: '',
    measureText(text) {
      const px = Number(/(\d+(?:\.\d+)?)px/.exec(this.font)[1]);
      return { width: text.length * px * 0.6, actualBoundingBoxAscent: px * 0.7, actualBoundingBoxDescent: px * 0.05 };
    },
    fillText: (...args) => calls.push(['fillText', ...args]),
    clearRect() {},
    setTransform() {},
  };
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(fake);
  vi.spyOn(HTMLCanvasElement.prototype, 'toDataURL').mockReturnValue('data:image/png;base64,AAAA');
  const url = maskUrl(beat({ x: 0, y: 0, w: 1600, h: 400 }), 'AI');
  expect(url).toBe('data:image/png;base64,AAAA');
  const px = Number(/(\d+(?:\.\d+)?)px/.exec(fake.font)[1]);
  expect(px * 0.75).toBeCloseTo(400 * 0.8, 3); // 높이가 먼저 걸림(폭 기준이면 1226px)
  expect(calls[0][2]).toBe(800); // 가운데
});

it('falls back to the C13 SVG mask without a canvas', () => {
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(null);
  expect(maskUrl(beat({ x: 0, y: 0, w: 400, h: 200 }), 'AI')).toMatch(/^data:image\/svg\+xml,/);
});
