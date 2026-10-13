import { describe, expect, it } from 'vitest';
import beat from './prompt.js';
describe('prompt beat', () => {
  it('splits every unicode character into a real DOM char', () => {
    const text = '안녕 A!';
    const view = beat.render({ text, label: '요청', result: { type: 'text', text: '완료' } }, {});
    expect(beat.fields.text.required).toBe(true);
    expect(view.parts.field).toHaveLength(1);
    expect(view.parts.char).toHaveLength(Array.from(text).length);
    expect(view.parts.char.map((n) => n.textContent).join('')).toBe(text);
    expect(view.parts.caret).toHaveLength(1);
    expect(view.parts.label[0].textContent).toBe('요청');
    expect(view.parts.result[0].textContent).toBe('완료');
    expect(view.parts.word).toHaveLength(1);
  });
  it('makes one result word part per whitespace-delimited word', () => {
    const view = beat.render({ text: '질문', result: { type: 'text', text: 'one two three' } }, {});
    expect(view.parts.word.map((word) => word.textContent)).toEqual(['one', 'two', 'three']);
  });
  it('requires text', () => expect(beat.fields.text.required).toBe(true));
});
