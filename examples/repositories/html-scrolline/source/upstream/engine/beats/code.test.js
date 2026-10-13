import { describe, expect, it } from 'vitest';
import beat from './code.js';
describe('code beat', () => {
  it('renders source as DOM lines and tokens', () => {
    const view = beat.render({ code: 'const x = 1;\nreturn x;', lang: 'js', highlight: [[2, 2]] }, {});
    expect(beat.fields.code.required).toBe(true);
    expect(view.parts.block).toHaveLength(1);
    expect(view.parts.line).toHaveLength(2);
    expect(view.parts.token[1].textContent).toBe('return x;');
    expect(view.parts.line[1].dataset.highlight).toBe('true');
    expect(view.parts.caret).toHaveLength(1);
  });
  it('requires language', () => expect(beat.fields.lang.required).toBe(true));
});
