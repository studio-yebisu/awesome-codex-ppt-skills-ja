import { expect, it, vi } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './word-slam.js';
const scenario = {
  beats: [{ id: 'b', type: 'text', data: { text: 'Slam', parts: { word: true, line: true } } }],
  run: { role: 'enter', beat: 'b', params: { duration: 1.4, scaleFrom: 1.4 } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('warns once for five words', () => {
  const warn = vi.spyOn(console, 'warn').mockImplementation(() => {});
  const h = createHarness({
    beats: [{ id: 'b', type: 'text', data: { text: 'a b c d e', parts: { word: true } } }],
  });
  const beat = h.beats.get('b');
  for (let i = 0; i < 4; i += 1) {
    const node = document.createElement('span');
    beat.root.append(node);
    beat.parts.word.push(node);
  }
  h.runMove(move, { role: 'enter', beat: 'b' });
  expect(warn).toHaveBeenCalledTimes(1);
  warn.mockRestore();
  h.destroy();
});
