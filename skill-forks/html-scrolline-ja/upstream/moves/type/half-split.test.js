import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './half-split.js';

const scenario = {
  beats: [{ id: 'b', type: 'text', data: {} }],
  run: { role: 'exit', beat: 'b', params: { duration: 0.9, distance: 1 } },
};
it('meets the exit contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('creates two exact 50 percent clipped copies and hides the source', () => {
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run);
  h.seek(result.timing.duration);
  const copies = result.ctx.overlay.querySelectorAll('[class*="sl-half-split__"]');
  expect(copies).toHaveLength(2);
  expect(copies[0].style.clipPath + copies[1].style.clipPath).toContain('50%');
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('b').part('block')[0], 'opacity'))).toBe(0);
  h.destroy();
});
