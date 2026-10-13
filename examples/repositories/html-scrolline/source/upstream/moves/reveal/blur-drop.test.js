import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './blur-drop.js';

const wordScenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'A B', parts: { block: true, word: true } } }],
  run: { role: 'exit', beat: 'b', params: { duration: 0.8, unit: 'word' } },
};

it('satisfies the move contract for word exits', () =>
  expect(checkMove(move, wordScenario, createHarness)).toEqual([]));

it('uses the block exit for the zoom preset and video', () => {
  const scenario = {
    beats: [{ id: 'v', type: 'video', data: { src: 'v.mp4', parts: { frame: true } } }],
    run: {
      role: 'exit',
      beat: 'v',
      params: { duration: 1, unit: 'block', blur: 8, drop: 0, scaleTo: 0.97, emLast: 0.1 },
    },
  };
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
  const h = createHarness(scenario);
  const { timing } = h.runMove(move, scenario.run);
  const frame = h.beats.get('v').part('frame')[0];
  h.seek(0);
  expect(frame.style.opacity).toBe('');
  h.seek(timing.duration);
  expect(Number(frame.style.opacity)).toBe(0);
  h.destroy();
});
