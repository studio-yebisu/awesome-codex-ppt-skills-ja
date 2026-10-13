import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './scramble-out.js';

const scenario = {
  beats: [{ id: 'b', type: 'text', data: { parts: { word: true } } }],
  rects: { 'b.block': { x: 100, y: 100, w: 400, h: 80 }, 'b.word#0': { x: 100, y: 100, w: 120, h: 40 } },
  run: { role: 'exit', beat: 'b', params: { duration: 0.9, glyphs: '#%&' } },
};
it('meets the exit contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('restores the original hidden text at the end', () => {
  const h = createHarness(scenario),
    word = h.beats.get('b').part('word')[0];
  word.textContent = '원문';
  const result = h.runMove(move, scenario.run);
  h.seek(result.timing.duration);
  expect(word.textContent).toBe('원문');
  expect(Number(result.ctx.gsap.getProperty(h.beats.get('b').part('block')[0], 'opacity'))).toBe(0);
  h.destroy();
});
