import { expect, it } from 'vitest';
import move from './rail-drop.js';

// 회귀: toEvent는 사건 순번이고 media part는 media가 있는 사건에만 생긴다.
it('turns toEvent into the index inside the sparse media part', () => {
  const events = [{ title: 'a', media: 'a.jpg' }, { title: 'b' }, { title: 'c', media: 'c.jpg' }];
  expect(move.handoff({ toEvent: 2 }, { from: {}, to: { events } }).to).toEqual({ part: 'media', index: 1 });
});
