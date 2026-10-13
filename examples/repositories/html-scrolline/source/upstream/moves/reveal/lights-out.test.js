import { expect, it } from 'vitest';
import { checkMove } from '../_shared/contract-check.js';
import { createHarness } from '../../engine/testing.js';
import move from './lights-out.js';

const scenario = {
  beats: [{ id: 'p', type: 'photo', data: { src: 'p.jpg', parts: { frame: true, caption: true } } }],
  run: { role: 'exit', beat: 'p', params: { duration: 1, darkFloor: 0.04 } },
};

it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));

it('ends on a fully dark frame', () => {
  const h = createHarness(scenario);
  const { timing } = h.runMove(move, scenario.run);
  const frame = h.beats.get('p').part('frame')[0];
  h.seek(timing.duration);
  expect(frame.style.filter).toContain('brightness(0)');
  h.destroy();
});
