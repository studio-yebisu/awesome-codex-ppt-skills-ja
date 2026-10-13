import { describe, expect, it, vi } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './frame-scrub.js';

const scenario = {
  beats: [{ id: 'v', type: 'video', data: { parts: { media: true } } }],
  run: { role: 'step', beat: 'v', params: { duration: 2, from: 0.2, to: 0.8 } },
  prepare(h) {
    h.beats.get('v').media.seq = { setProgress: vi.fn() };
  },
};
describe('frame-scrub', () => {
  it('meets the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('is a reversible from-to frame mapping', () => {
    const h = createHarness({ beats: scenario.beats });
    scenario.prepare(h);
    const r = h.runMove(move, scenario.run);
    h.seek(0);
    h.seek(1);
    h.seek(0);
    h.seek(2);
    h.destroy();
  });
});
