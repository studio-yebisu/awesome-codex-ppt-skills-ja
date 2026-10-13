import { expect, it } from 'vitest';
import { applyTextMask } from './mask.js';
it('installs an SVG data-url mask', () => {
  const node = document.createElement('div');
  let vars;
  applyTextMask(
    {
      initial(_n, value) {
        vars = value;
      },
    },
    node,
    'MASK',
    { rect: { w: 100, h: 20 }, align: 'center' },
  );
  expect(vars.maskImage).toContain('url("data:image/svg+xml');
});
