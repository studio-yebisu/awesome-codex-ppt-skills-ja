import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './lit-from-dark.js';

const scenario = {
  beats: [{ id: 'v', type: 'video', data: { mode: 'scrub', parts: { frame: true, caption: true } } }],
  run: { role: 'enter', beat: 'v', params: { duration: 1.6, scrubTo: 0.8 } },
  prepare(h) {
    h.beats.get('v').media = { seq: { setProgress() {} } };
  },
};

it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));

it('starts dark and clears the rim mask at rest', () => {
  const h = createHarness(scenario);
  scenario.prepare(h);
  const { timing } = h.runMove(move, scenario.run);
  const frame = h.beats.get('v').part('frame')[0];
  h.seek(0);
  expect(frame.style.filter).toContain('brightness(0.04)');
  h.seek(timing.duration);
  expect(frame.style.maskImage).toBe('none');
  expect(frame.style.filter).toBe('none');
  h.destroy();
});
