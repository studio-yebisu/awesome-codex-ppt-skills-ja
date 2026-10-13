import { readFileSync } from 'node:fs';
import { expect, it } from 'vitest';

// 실제 브라우저(tools/smoke.mjs canvas-pitch)에서 드러난 배치 회귀.
const css = readFileSync('concepts/canvas/layout.css', 'utf8');
const rule = (selector) => {
  const at = css.indexOf(`${selector} {`);
  return at < 0 ? '' : css.slice(at, css.indexOf('}', at));
};

it('sizes every world tile to one screen so content can sit under its place name', () => {
  const tile = rule('.sl-concept-canvas .sl-place-world:not(.sl-beat--sequence)');
  expect(tile).toMatch(/width:\s*var\(--vw-px\)/);
  expect(tile).toMatch(/height:\s*var\(--vh-px\)/);
});

it('drops the user-agent highlight behind emphasis marks', () => {
  expect(rule('.sl-concept-canvas mark')).toMatch(/background:\s*transparent/);
});

it('draws the compare divider as a hairline, not the word "vs"', () => {
  const divider = rule('.sl-concept-canvas .sl-compare__divider');
  expect(divider).toMatch(/font-size:\s*0/);
  expect(divider).toMatch(/border-inline-start:\s*1px solid/);
});
