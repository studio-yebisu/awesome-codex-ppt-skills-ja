import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './rail-settle.js';

const scenario = {
  beats: [{ id: 'rail', type: 'chronology', data: {}, place: { world: { x: 0, y: 0, s: 1 } } }],
  run: { role: 'camera', beat: 'rail', params: { duration: 2.2, tilt: 9, startScale: 1.15 } },
  concept: { eases: { inout: 'power2.inOut' } },
};
it('settles the rail camera into a flat view', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  h.seek(0);
  expect(Math.abs(Number(result.ctx.gsap.getProperty(h.stage.camera, 'ry')))).toBeLessThanOrEqual(12);
  h.seek(result.timing.duration);
  expect(Number(result.ctx.gsap.getProperty(h.stage.camera, 'rx'))).toBe(0);
  expect(Number(result.ctx.gsap.getProperty(h.stage.camera, 'ry'))).toBe(0);
  h.destroy();
});
it('omits rotation in reduced motion', () => {
  const h = createHarness({ ...scenario, reduce: true }),
    result = h.runMove(move, scenario.run);
  h.seek(result.timing.duration / 2);
  expect(h.stage.camera.getAttribute('style') ?? '').not.toMatch(/rotation|rotate/i);
  h.destroy();
});
