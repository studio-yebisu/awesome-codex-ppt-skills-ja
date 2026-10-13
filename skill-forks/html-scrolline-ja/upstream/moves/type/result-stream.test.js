import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './result-stream.js';
const scenario = {
  beats: [
    {
      id: 'p',
      type: 'prompt',
      data: {
        text: 'ask',
        result: { type: 'text', text: 'one two three' },
        parts: { result: true, word: true },
      },
    },
  ],
  rects: {
    'p.result': { x: 20, y: 50, w: 200, h: 30 },
    'p.word#0': { x: 20, y: 50, w: 30, h: 20 },
    'p.word#1': { x: 55, y: 50, w: 30, h: 20 },
    'p.word#2': { x: 90, y: 50, w: 40, h: 20 },
  },
  run: { role: 'step', beat: 'p', params: { duration: 2, compress: 0.85 } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('uses the declared duration', () => expect(move.timing(scenario.run.params).duration).toBe(2));
