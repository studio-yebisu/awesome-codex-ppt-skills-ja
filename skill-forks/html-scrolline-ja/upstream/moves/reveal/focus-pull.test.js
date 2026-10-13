import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './focus-pull.js';

const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'A B', parts: { block: true, word: true, em: true } } }],
  concept: { tokens: { blurMax: 6 } },
  run: { role: 'enter', beat: 'b', params: { duration: 1, scaleFrom: 1.06, rise: 0, tracking: 0 } },
};

it('satisfies the move contract and canvas preset', () =>
  expect(checkMove(move, scenario, createHarness)).toEqual([]));

it('lands sharp and without a transform', () => {
  const h = createHarness(scenario);
  const { timing, ctx } = h.runMove(move, scenario.run);
  const word = h.beats.get('b').part('word')[0];
  h.seek(0);
  expect(Number(word.style.opacity)).toBe(0);
  h.seek(timing.duration);
  expect(word.style.filter).toBe('none');
  expect(Number(ctx.gsap.getProperty(word, 'x'))).toBe(0);
  expect(Number(ctx.gsap.getProperty(word, 'y'))).toBe(0);
  h.destroy();
});
