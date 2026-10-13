import { afterEach, describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './depth-ladder.js';
const scenario = {
  beats: [{ id: 'a', type: 'text', data: {} }],
  run: {
    role: 'ambient',
    beat: 'a',
    params: { rungs: ['전체', '앱', '결제'], level: 1, maxLevel: 2, appearAfter: 0.4 },
  },
  concept: { tokens: { ladderX: 72, ladderTop: 100, ladderStep: 30 } },
};
const hs = [];
afterEach(() => hs.splice(0).forEach((h) => h.destroy()));
describe('depth-ladder', () => {
  it('meets the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('waits for appearAfter and keeps deeper rungs faint', () => {
    const h = createHarness(scenario);
    hs.push(h);
    const r = h.runMove(move, scenario.run);
    const ladder = r.ctx.overlay.querySelector('.sl-depth-ladder');
    h.seek(0.2);
    expect(Number(r.ctx.gsap.getProperty(ladder, 'opacity'))).toBe(0);
    h.seek(1);
    expect(Number(r.ctx.gsap.getProperty(ladder, 'opacity'))).toBe(1);
    expect(r.ctx.overlay.querySelectorAll('.sl-depth-ladder__rung')[2].style.opacity).toBe('0.35');
  });
  it('draws only the rungs reached so far', () => {
    const h = createHarness(scenario);
    hs.push(h);
    const r = h.runMove(move, { ...scenario.run, params: { ...scenario.run.params, level: 1, maxLevel: 1 } });
    expect(r.ctx.overlay.querySelectorAll('.sl-depth-ladder__rung').length).toBe(2);
  });
});
