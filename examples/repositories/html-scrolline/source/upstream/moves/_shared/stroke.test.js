import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { drawOn, path, pointOnPolyline, svgLayer } from './stroke.js';
it('uses normalized paths and interpolates polyline points', () => {
  const h = createHarness({ beats: [{ id: 'a', type: 'text', data: {} }] });
  const svg = svgLayer({ overlay: h.stage.overlay, viewport: h.stage.viewport });
  const p = path(svg, 'M 0 0 L 1 1');
  expect(p.getAttribute('pathLength')).toBe('1');
  const tl = h.runMove(
    {
      id: 'stroke-test',
      family: 'data',
      role: 'enter',
      accepts: ['*'],
      sources: ['x'],
      reduce: 'self',
      params: {},
      timing: () => ({ duration: 1 }),
      build(t) {
        drawOn(t, p, { at: 0, duration: 1 });
      },
    },
    { role: 'enter', beat: 'a' },
  );
  h.seek(0.5);
  expect(Number(p.style.strokeDashoffset)).toBeCloseTo(0.5);
  expect(
    pointOnPolyline(
      [
        { x: 0, y: 0 },
        { x: 10, y: 0 },
        { x: 10, y: 10 },
      ],
      0.75,
    ),
  ).toEqual({ x: 10, y: 5 });
  h.destroy();
});
