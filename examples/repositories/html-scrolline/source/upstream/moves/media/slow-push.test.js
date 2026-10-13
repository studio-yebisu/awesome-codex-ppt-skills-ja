import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './slow-push.js';

const scenario = {
  beats: [{ id: 'v', type: 'video', data: { parts: { media: true } } }],
  run: { role: 'ambient', beat: 'v', params: { pushScale: 1.08, focusX: 0.2, focusY: 0.7 } },
};
describe('slow-push', () => {
  it('meets the move contract with fill timing', () =>
    expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('uses the fill harness duration and lands on its linear scale', () => {
    const h = createHarness({ beats: scenario.beats }),
      r = h.runMove(move, scenario.run);
    expect(move.timing({}).duration).toBe('fill');
    expect(r.tl.duration()).toBeLessThanOrEqual(1);
    h.seek(1);
    expect(Number(r.ctx.gsap.getProperty(r.ctx.beat.part('media')[0], 'scaleX'))).toBeCloseTo(1.08);
    h.destroy();
  });
});
