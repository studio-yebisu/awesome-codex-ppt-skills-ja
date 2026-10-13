import { expect, it } from 'vitest';
import move from './rail-lift.js';

// 회귀: b-r3는 다섯 사건 중 마지막에만 media가 있어 media part가 한 개뿐 — fromEvent 4를 그대로 넘기면 media[4]가 없다.
it('turns fromEvent into the index inside the sparse media part', () => {
  const events = [{ title: 'a' }, { title: 'b' }, { title: 'c' }, { title: 'd' }, { title: 'e', media: 'e.jpg' }];
  const picked = move.handoff({ fromEvent: 4, fromPart: 'media', toPart: '', toIndex: 0 }, { from: { events }, to: {} });
  expect(picked.from).toEqual({ part: 'media', index: 0 });
  const title = move.handoff({ fromEvent: 3, fromPart: 'title', toPart: 'label', toIndex: 0 }, { from: { events }, to: {} });
  expect(title.from).toEqual({ part: 'title', index: 3 });
});
