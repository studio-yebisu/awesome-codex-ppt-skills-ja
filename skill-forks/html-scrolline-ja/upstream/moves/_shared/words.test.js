import { expect, it } from 'vitest';
import { wordsIn } from './words.js';
it('finds nested word parts', () => {
  const root = document.createElement('div'),
    word = document.createElement('span');
  word.dataset.part = 'word';
  root.append(word);
  expect(wordsIn({ part: (name) => (name === 'block' ? [root] : []) }, 'block')).toEqual([word]);
});
