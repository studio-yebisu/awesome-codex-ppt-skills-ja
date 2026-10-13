import { expect, it } from 'vitest';
import text from './text.js';

const ems = (view) => view.parts.em.map((em) => em.textContent);

// 회귀(data 통합): 어절마다 `includes(phrase)`로 봐서 여러 어절 구절은 끝내 강조되지 않았다.
it('marks every word a multi-word phrase covers, across lines, and keeps single-word matches', () => {
  const view = text.render(
    { text: '결국 도로 위 차가 바뀌는 속도가 관건이다', emphasis: ['도로 위 차가 바뀌는 속도'] },
    {},
  );
  expect(ems(view)).toEqual(['도로', '위', '차가', '바뀌는', '속도가']);
  const lines = text.render({ text: 'a b c d', lines: ['a b', 'c d'], emphasis: ['b c', 'd'] }, {});
  expect(ems(lines)).toEqual(['b', 'c', 'd']);
  expect(ems(text.render({ text: '함께 만드는 이야기', emphasis: ['이야'] }, {}))).toEqual(['이야기']);
});
