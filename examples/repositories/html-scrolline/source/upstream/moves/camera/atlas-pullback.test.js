import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './atlas-pullback.js';

const scenario = {
  beats: [
    { id: 'a', type: 'text', data: {}, place: { world: { x: 0, y: 2.2, s: 1 } } },
    { id: 'b', type: 'text', data: {}, place: { world: { x: -0.6, y: -0.6, s: 1 } } },
  ],
  run: {
    role: 'camera',
    beat: 'b',
    params: { duration: 3.2, bounds: { x0: -0.6, y0: -0.6, x1: 6, y1: 4.6 }, margin: 0.06, tilt: 6 },
  },
  concept: { eases: { inout: 'power2.inOut', out: 'power3.out' } },
};
const read = (h, ctx, prop) => Number(ctx.gsap.getProperty(h.stage.camera, prop));

it('starts on the previous tile, tilts once, fits the bounds level', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  h.seek(0);
  expect(read(h, result.ctx, 'scale')).toBeCloseTo(1);
  expect(read(h, result.ctx, 'x')).toBeCloseTo(960 - 0.5 * 1920);
  h.seek(result.timing.duration * 0.42);
  expect(read(h, result.ctx, 'rotationX')).toBeGreaterThan(4);
  h.seek(result.timing.duration);
  expect(read(h, result.ctx, 'scale')).toBeCloseTo((1 / 6.6) * 0.94);
  expect(read(h, result.ctx, 'rotationX')).toBe(0);
  expect(read(h, result.ctx, 'rotationY')).toBe(0);
  h.destroy();
});
