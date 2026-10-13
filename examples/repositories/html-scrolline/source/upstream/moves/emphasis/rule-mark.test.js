import { afterEach, describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './rule-mark.js';
const scenario = {
  beats: [{ id: 'c', type: 'compare', data: {} }],
  rects: { 'c.item': { x: 100, y: 120, w: 300, h: 400 } },
  run: { role: 'step', beat: 'c', params: { y: 0.25, label: '첫 화면 끝', duration: 1.2 } },
};
const hs = [];
afterEach(() => hs.splice(0).forEach((h) => h.destroy()));
describe('rule-mark', () => {
  it('meets the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('places the rule at rect.y + y × rect.h', () => {
    const h = createHarness(scenario);
    hs.push(h);
    const r = h.runMove(move, scenario.run);
    expect(r.ctx.overlay.querySelector('path').getAttribute('d')).toContain('220');
  });
});
