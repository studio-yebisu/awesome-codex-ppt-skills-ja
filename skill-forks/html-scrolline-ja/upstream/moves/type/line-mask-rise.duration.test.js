import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './line-mask-rise.js';

// 회귀: 어절 9개 인용에 stagger 0.12 × 8 + 0.7d가 duration 1을 넘어 build가 throw했다(rail b-q-gpt2).
it('fits a many-word quote inside its planned duration', () => {
  const text = '기술이 악용될 우려 때문에, 학습한 모델은 공개하지 않습니다. 하나 둘';
  const scenario = {
    beats: [{ id: 'q', type: 'quote', data: { text, by: 'OpenAI' } }],
    run: { role: 'enter', beat: 'q', params: { duration: 1 } },
  };
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
});
