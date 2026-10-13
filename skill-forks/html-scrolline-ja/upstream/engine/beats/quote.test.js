import { describe, expect, it } from 'vitest';
import beat from './quote.js';
describe('quote beat', () => {
  it('renders actual quote words and attribution', () => {
    const view = beat.render({ text: '변화는 작은 선택에서 시작됩니다', by: '홍길동', role: '대표' }, {});
    expect(beat.fields.text.required).toBe(true);
    expect(view.parts.block).toHaveLength(1);
    expect(view.parts.mark[0].textContent).toBe('“');
    expect(view.parts.word.map((n) => n.textContent).join(' ')).toContain('선택에서');
    expect(view.parts.by[0].textContent).toContain('대표');
  });
  it('declares by required', () => expect(beat.fields.by.required).toBe(true));
  it('renders one source part for an array source', () => {
    const view = beat.render(
      { text: '인용', by: '사람', source: ['s1', 's2'] },
      { sources: { s1: { short: '신문' }, s2: { title: '기록원' } } },
    );
    expect(beat.fields.source.type).toBe('any');
    expect(view.parts.source[0].textContent).toBe('신문 · 기록원');
  });
});
