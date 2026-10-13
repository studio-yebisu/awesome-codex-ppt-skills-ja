import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './establish-crane.js';

const scenario = {
  beats: [{ id: 'b', type: 'text', data: {}, place: { world: { x: 1, y: 2, s: 1 } } }],
  run: {
    role: 'camera',
    beat: 'b',
    params: { duration: 2.4, tilt: 10, startScale: 1.6, lift: 0.35, haze: 0.5 },
  },
  concept: { eases: { inout: 'power2.inOut', out: 'power3.out' } },
};
const read = (h, ctx, prop) => Number(ctx.gsap.getProperty(h.stage.camera, prop));

it('cranes from its low tilted start to a level target', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  h.seek(0);
  expect(read(h, result.ctx, 'rotationX')).toBe(10);
  expect(read(h, result.ctx, 'scale')).toBeCloseTo(1.6);
  h.seek(result.timing.duration);
  expect(read(h, result.ctx, 'rotationX')).toBe(0);
  expect(read(h, result.ctx, 'scale')).toBe(1);
  expect(read(h, result.ctx, 'x')).toBeCloseTo(960 - 1.5 * 1920);
  h.destroy();
});
it('reduced motion rises without tilting', () => {
  const h = createHarness({ ...scenario, reduce: true }),
    result = h.runMove(move, scenario.run);
  h.seek(result.timing.duration * 0.2);
  expect(read(h, result.ctx, 'rotationX')).toBe(0);
  h.destroy();
});
