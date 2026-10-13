import { describe, expect, it, vi } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './sticky-scrub-link.js';

const scenario = {
  beats: [
    { id: 'a', type: 'video', data: { parts: { caption: true } } },
    { id: 'b', type: 'video', data: { parts: { caption: true } } },
  ],
  rects: { 'a.frame': { x: 0, y: 0, w: 400, h: 220 }, 'b.frame': { x: 40, y: 20, w: 400, h: 220 } },
  run: { role: 'link', from: 'a', beat: 'b', params: { duration: 1.2, from: 0.2, to: 0.8, bAt: -1 } },
  prepare(h) {
    h.beats.get('a').media.seq = { setProgress: vi.fn() };
    h.beats.get('b').media.seq = { setProgress: vi.fn() };
  },
  carry: null, // 두 beat가 같은 자리(full)라 유령 복제 없음
  nodes: () => [],
};
describe('sticky-scrub-link', () => {
  it('meets the link contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('sets B at its handoff frame and finishes B visible', () => {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
    scenario.prepare(h);
    const r = h.runMove(move, scenario.run);
    h.seek(r.timing.duration);
    r.tl.seek(r.timing.duration);
    expect(h.beats.get('b').media.seq.setProgress).toHaveBeenCalledWith(0.8);
    expect(Number(r.ctx.gsap.getProperty(r.ctx.handoff.to.node, 'opacity'))).toBe(1);
    expect(Number(r.ctx.gsap.getProperty(r.ctx.handoff.from.node, 'opacity'))).toBe(0);
    h.destroy();
  });
  it('keeps B media hidden until the swap so A carries the turn', () => {
    const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
    scenario.prepare(h);
    const r = h.runMove(move, scenario.run);
    const media = h.beats.get('b').part('media')[0];
    h.seek(0.7 * r.timing.duration);
    if (media) expect(Number(r.ctx.gsap.getProperty(media, 'opacity'))).toBe(0);
    expect(Number(r.ctx.gsap.getProperty(r.ctx.handoff.from.node, 'opacity'))).toBe(1);
    h.seek(r.timing.duration);
    if (media) expect(Number(r.ctx.gsap.getProperty(media, 'opacity'))).toBe(1);
    h.destroy();
  });
});
