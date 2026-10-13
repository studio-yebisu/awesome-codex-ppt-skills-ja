import { readFileSync } from 'node:fs';
import { expect, it } from 'vitest';

// 실제 브라우저(tools/smoke.mjs zoom-root-cause)에서 드러난 배치 회귀.
const css = readFileSync('concepts/zoom/layout.css', 'utf8');
const rule = (selector) => {
  const at = css.indexOf(`${selector} {`);
  return at < 0 ? '' : css.slice(at, css.indexOf('}', at));
};

it('puts every plot and phone screen in the same field so dives land on one rect', () => {
  for (const selector of ['.sl-concept-zoom .sl-chart__plot', '.sl-concept-zoom .sl-compare__item', '.sl-concept-zoom .sl-video'])
    expect(rule(selector)).toMatch(/top:\s*var\(--zoom-field-y\)/);
  expect(rule('.sl-concept-zoom .sl-chart__plot')).toMatch(/height:\s*var\(--zoom-field-h\)/);
});

it('widens bars with the scale property, never transform (the port rect is measured with transform off)', () => {
  expect(rule('.sl-concept-zoom .sl-chart__mark--bar')).toMatch(/scale:\s*3\.6 1/);
  expect(css).not.toMatch(/transform:\s*scale/);
});
