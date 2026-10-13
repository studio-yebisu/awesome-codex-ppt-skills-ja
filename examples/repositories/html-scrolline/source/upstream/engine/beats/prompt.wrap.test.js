import { expect, it } from 'vitest';
import prompt from './prompt.js';

// 회귀(kinetic·launch 통합): inline-block 글자가 공백을 0폭으로 접고 어절 중간에서 줄이 갈렸다.
it('groups non-space characters into runs and keeps every char part in text order', () => {
  const view = prompt.render({ text: '신입 사원  환영' }, {});
  const field = view.parts.field[0];
  expect(view.parts.char.map((c) => c.textContent).join('')).toBe('신입 사원  환영');
  expect([...field.querySelectorAll('.sl-prompt__run')].map((r) => r.textContent)).toEqual(['신입', '사원', '환영']);
  expect(view.parts.char.filter((c) => c.textContent === ' ').every((c) => c.parentElement === field)).toBe(true);
  expect(field.lastElementChild).toBe(view.parts.caret[0]);
});
