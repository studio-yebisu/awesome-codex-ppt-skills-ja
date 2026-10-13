import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './count-roll.js';

const scenario = {
  beats: [
    {
      id: 'n',
      type: 'number',
      data: {
        value: 105.6,
        from: 120,
        label: '전환율',
        format: { decimals: 1, unit: '%' },
        parts: { digits: true, unit: true, label: true, source: true },
      },
    },
  ],
  run: { role: 'enter', beat: 'n', params: { duration: 1.4, ease: 'out', unitSlide: 8 } },
  concept: { tokens: { stagger: 0.04 } },
  nodes: () => [],
};
it('passes the move contract and rolls a decreasing formatted number', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness({ beats: scenario.beats, concept: scenario.concept });
  const r = h.runMove(move, scenario.run);
  expect(h.beats.get('n').part('digits')[0].textContent).toBe('120.0');
  h.seek(r.timing.duration);
  expect(h.beats.get('n').part('digits')[0].textContent).toBe('105.6');
  h.destroy();
});
