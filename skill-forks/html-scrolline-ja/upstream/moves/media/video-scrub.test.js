import { describe, expect, it, vi } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './video-scrub.js';

const scenario = {
  beats: [{ id: 'v', type: 'video', data: { parts: { media: true, caption: true } } }],
  run: { role: 'enter', beat: 'v', params: { duration: 3.2, stops: [{ name: 'pause', at: 0.5 }] } },
  prepare(h) {
    h.beats.get('v').media.seq = { setProgress: vi.fn() };
  },
};
describe('video-scrub', () => {
  it('meets the move contract and records scaled stops', () => {
    expect(checkMove(move, scenario, createHarness)).toEqual([]);
    expect(move.timing(scenario.run.params).stops).toEqual([{ name: 'pause', at: 1.6 }]);
  });
  it('maps every seek to the same sequence progress, including reduce', () => {
    const h = createHarness({ beats: scenario.beats, reduce: true });
    scenario.prepare(h);
    const r = h.runMove(move, scenario.run);
    h.seek(0);
    h.seek(0.8);
    h.seek(r.timing.duration);
    expect(r.tl.duration()).toBe(r.timing.duration);
    expect(Number(r.ctx.gsap.getProperty(r.ctx.beat.part('caption')[0], 'opacity'))).toBe(1);
    h.destroy();
  });
});
