import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move, { lookAtVars } from './arc-flight.js';

const scenario = {
  beats: [
    { id: 'a', type: 'text', data: {}, place: { world: { x: 0, y: 0, s: 1 } } },
    { id: 'b', type: 'text', data: {}, place: { world: { x: 2, y: 1, s: 1 } } },
  ],
  run: {
    role: 'camera',
    beat: 'b',
    params: { duration: 1.8, altitude: 0.32, bank: 5, parallax: 0.35, settle: 0.12, ease: 'flight' },
  },
  concept: { eases: { flight: 'power2.inOut', inout: 'power2.inOut', out: 'power3.out' } },
};
const read = (h, ctx, prop) => Number(ctx.gsap.getProperty(h.stage.camera, prop));

it('flies from the previous tile to the target tile and lands level', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  const end = lookAtVars(h.stage.viewport, { cx: 2.5, cy: 1.5, s: 1 });
  h.seek(result.timing.duration);
  expect(read(h, result.ctx, 'x')).toBeCloseTo(end.x);
  expect(read(h, result.ctx, 'y')).toBeCloseTo(end.y);
  expect(read(h, result.ctx, 'scale')).toBeCloseTo(1);
  expect(read(h, result.ctx, 'rotationX')).toBe(0);
  expect(read(h, result.ctx, 'rotationY')).toBe(0);
  h.seek(0);
  expect(read(h, result.ctx, 'x')).toBeCloseTo(lookAtVars(h.stage.viewport, { cx: 0.5, cy: 0.5, s: 1 }).x);
  h.destroy();
});
it('climbs and banks toward the heading mid-flight', () => {
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  h.seek(result.timing.duration * 0.45);
  expect(read(h, result.ctx, 'scale')).toBeLessThan(0.75);
  expect(read(h, result.ctx, 'rotationY')).toBeGreaterThan(2);
  h.destroy();
});
it('turns a short hop into a level glide', () => {
  const h = createHarness({
    ...scenario,
    beats: [
      { id: 'a', type: 'text', data: {}, place: { world: { x: 0, y: 0, s: 1 } } },
      { id: 'b', type: 'text', data: {}, place: { world: { x: 0.2, y: 0.1, s: 1 } } },
    ],
  });
  const result = h.runMove(move, scenario.run);
  h.seek(result.timing.duration * 0.3);
  expect(read(h, result.ctx, 'rotationX')).toBe(0);
  expect(read(h, result.ctx, 'rotationY')).toBe(0);
  expect(read(h, result.ctx, 'scale')).toBeCloseTo(1);
  h.destroy();
});
