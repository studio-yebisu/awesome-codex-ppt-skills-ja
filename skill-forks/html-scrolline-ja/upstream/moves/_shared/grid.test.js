import { expect, it } from 'vitest';
import { drawDots, gridLayout } from './grid.js';
it('lays out a grid and tolerates a missing canvas context', () => {
  expect(gridLayout({ n: 7, cols: 3, cell: 10, gap: 2, origin: { x: 0, y: 0 } })[3]).toEqual({
    x: 0,
    y: 12,
    i: 3,
  });
  expect(() => drawDots({ g: null }, [], { r: 1, color: '#fff' })).not.toThrow();
});
