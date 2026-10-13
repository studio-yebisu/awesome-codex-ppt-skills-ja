import { readFileSync } from 'node:fs';
import { expect, it } from 'vitest';

// 실제 브라우저(tools/smoke.mjs rail-ai-decade)에서 드러난 배치 회귀. engine-css.rail.test.js에서 이관(#49).
const css = readFileSync('concepts/rail/layout.css', 'utf8');
const rule = (selector) => {
  const at = css.indexOf(`${selector} {`);
  return at < 0 ? '' : css.slice(at, css.indexOf('}', at));
};

it('lays the time rail out from the now line with a month-proportional length', () => {
  expect(rule('.sl-concept-rail [data-now] > .sl-chronology__track')).toMatch(/left:\s*var\(--sl-now\)/);
  expect(rule('.sl-concept-rail [data-now] > .sl-chronology__track')).toMatch(/var\(--sl-span\)/);
  expect(rule('.sl-concept-rail .sl-chronology__event')).toMatch(/left:\s*calc\(var\(--sl-position-x\)/);
});

it('lays era paper behind toned non-chronology beats and lifts their video caption to L2', () => {
  expect(rule('.sl-concept-rail .sl-beat[data-tone]:not(.sl-beat--chronology)')).toMatch(/background:\s*var\(--sl-bg\)/);
  expect(rule('.sl-concept-rail .sl-beat[data-tone] .sl-video__caption')).toMatch(/var\(--sl-size-m\)/);
});
