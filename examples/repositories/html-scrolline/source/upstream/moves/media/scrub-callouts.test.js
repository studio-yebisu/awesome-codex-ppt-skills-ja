import { describe, expect, it, vi } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './scrub-callouts.js';

const scenario = {
  beats: [{ id: 'v', type: 'video', data: {} }],
  rects: { 'v.frame': { x: 100, y: 80, w: 600, h: 340 } },
  run: { role: 'step', beat: 'v', params: { duration: 1, from: 0, to: 0.9 } },
  prepare(h) {
    h.beats.get('v').media.seq = { setProgress: vi.fn() };
  },
  nodes: (h) => [h.beats.get('v').part('frame')[0]],
};
describe('scrub-callouts', () => {
  it('meets the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('draws normalized stroke and omits scrim when requested', () => {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
    scenario.prepare(h);
    const r = h.runMove(move, { ...scenario.run, params: { ...scenario.run.params, dimOthers: false } });
    const path = r.ctx.overlay.querySelector('path');
    expect(path.getAttribute('pathLength')).toBe('1');
    h.seek(r.timing.duration);
    expect(path.style.strokeDashoffset).toBe('0');
    expect(r.ctx.overlay.querySelector('.sl-scrub-callouts__scrim')).toBeNull();
    h.destroy();
  });
});
