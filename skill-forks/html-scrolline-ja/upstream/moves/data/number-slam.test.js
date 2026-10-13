import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './number-slam.js';

const scenario = {
  beats: [
    {
      id: 'n',
      type: 'number',
      data: { value: 42, label: '답', parts: { digits: true, unit: true, label: true } },
    },
  ],
  run: {
    role: 'enter',
    beat: 'n',
    params: { duration: 1, slamScale: 1.6, slamBlur: 18, sweep: true, sweepWidth: 0.35 },
  },
};
it('passes contract and has resolved digits at the slam landing', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats });
  const r = h.runMove(move, scenario.run);
  const digits = h.beats.get('n').part('digits')[0];
  h.seek(0.35);
  expect(Number(r.ctx.gsap.getProperty(digits, 'scale'))).toBe(1);
  expect(r.ctx.gsap.getProperty(digits, 'filter')).toBe('none');
  h.destroy();
});
it('removes blur in reduced motion', () => {
  const h = createHarness({ beats: scenario.beats, reduce: true });
  const r = h.runMove(move, scenario.run);
  h.seek(0);
  expect(r.ctx.gsap.getProperty(h.beats.get('n').part('digits')[0], 'filter')).not.toContain('18px');
  h.destroy();
});
