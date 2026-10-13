import { describe, expect, it } from 'vitest';
import beat from './text.js';
const rc = { lang: 'ko', asset: (x) => x };
describe('text beat', () => {
  it('has required fields and renders real line/word text', () => {
    expect(beat.fields.text.required).toBe(true);
    expect(beat.fields.text.type).toBe('string');
    const view = beat.render(
      { text: '함께 만드는 이야기', lines: ['함께 만드는', '이야기'], emphasis: ['이야기'] },
      rc,
    );
    expect(view.root.matches('[data-beat], section')).toBe(true);
    expect(view.root.className).toContain('sl-beat--text');
    expect(view.parts.block).toHaveLength(1);
    expect(view.parts.line).toHaveLength(2);
    expect(view.parts.word.map((n) => n.textContent).join(' ')).toContain('이야기');
    expect(view.parts.em).toHaveLength(1);
  });
  it('reject schema fixture through required definition', () => expect(beat.fields.text.required).toBe(true));
});
