import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './strike-swap.js';

const scenario = {
  beats: [
    {
      id: 'n',
      type: 'number',
      data: {
        value: 120,
        label: '이전',
        format: { decimals: 1 },
        parts: { value: true, digits: true, label: true },
      },
    },
  ],
  run: {
    role: 'step',
    beat: 'n',
    params: { to: 105.6, decimals: 1, suffix: '', label: '수정', duration: 1.6 },
  },
  nodes: () => [],
};
it('passes contract and leaves the old value struck back', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats });
  const r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration);
  expect(r.ctx.overlay.querySelector('.sl-strike-swap__digits').textContent).toBe('105.6');
  expect(Number(r.ctx.gsap.getProperty(h.beats.get('n').part('value')[0], 'opacity'))).toBeCloseTo(0.35);
  h.destroy();
});
