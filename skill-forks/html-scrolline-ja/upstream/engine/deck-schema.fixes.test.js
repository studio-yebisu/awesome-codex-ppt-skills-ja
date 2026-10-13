// 계약 v2 수리(CONTRACT-REQUESTS #15·#21·#22·#23·#26) 회귀 테스트. 기존 deck-schema.test.js는 그대로 둔다(Hat: refactor).
import { describe, expect, it } from 'vitest';
import { createRegistry } from './registry.js';
import { validateDeck } from './deck-schema.js';

const move = (id, role, accepts = ['*']) => ({
  id,
  family: 'reveal',
  role,
  accepts,
  sources: ['test'],
  reduce: 'self',
  params: {},
  timing: () => ({ duration: 1 }),
  build: () => {},
});
const registry = createRegistry([
  move('rise', 'enter'),
  move('leave', 'exit'),
  move('to-text', 'link', ['text']),
]);
const type = { fields: {}, primary: 'block', render: () => {} };
const env = {
  registry,
  concept: {
    id: 'test',
    beats: { allow: ['text', 'photo'] },
    moves: { allow: ['rise', 'leave', 'to-text'] },
    defaults: { enter: 'rise', exit: 'leave' },
  },
  beatTypes: { text: type, photo: type },
};
const deck = (beats, id = 'fixes') => ({
  id,
  title: 'Fixes',
  lang: 'en',
  concept: 'test',
  sample: true,
  beats,
});
const messages = (d) => validateDeck(d, env).errors.map((x) => `${x.path} ${x.message}`);

describe('validateDeck v2 수리', () => {
  it('#21 link accepts는 받는 beat(다음 beat) type으로 검사한다', () => {
    const ok = deck([
      { id: 'a', type: 'photo', link: { move: 'to-text' }, enter: { move: 'rise' } },
      { id: 'b', type: 'text', enter: { move: 'engine:none' } },
    ]);
    expect(messages(ok)).toEqual([]);
    const bad = deck([
      { id: 'a', type: 'text', link: { move: 'to-text' }, enter: { move: 'rise' } },
      { id: 'b', type: 'photo', enter: { move: 'engine:none' } },
    ]);
    expect(messages(bad)).toEqual(['deck.beats[0].link.move does not accept beat type']);
  });

  it('#22 engine:none은 enter·exit·link·step·camera 어디에나 쓸 수 있고 반복 검사도 면제', () => {
    const d = deck([
      { id: 'a', type: 'text', enter: { move: 'engine:none' }, exit: { move: 'engine:none' } },
      {
        id: 'b',
        type: 'text',
        enter: { move: 'engine:none' },
        steps: [{ move: 'engine:none' }],
        camera: { move: 'engine:none' },
        link: { move: 'engine:none' },
      },
      { id: 'c', type: 'text', enter: { move: 'engine:none' }, exit: { move: 'engine:none' } },
    ]);
    expect(messages(d)).toEqual([]);
  });

  it('#15·#23 반복 검사가 콜론 든 move id를 자르지 않는다', () => {
    const d = deck([
      { id: 'a', type: 'text', exit: { move: 'engine:fade-out' } },
      { id: 'b', type: 'text', enter: { move: 'engine:fade-in' }, exit: { move: 'engine:fade-out' } },
    ]);
    const errs = messages(d).filter((m) => m.includes('repeats'));
    expect(errs).toEqual(['deck.beats engine:fade-out repeats as exit without repeat: intended']);
    d.beats[1].repeat = 'intended';
    expect(messages(d).filter((m) => m.includes('repeats'))).toEqual([]);
  });

  it('#26 `_`로 시작하는 내부 덱 id는 통과, 형식 밖 id는 오류', () => {
    const one = [{ id: 'a', type: 'text' }];
    expect(messages(deck(one, '_smoke'))).toEqual([]);
    expect(messages(deck(one, '_Smoke'))).toEqual(['deck.id invalid id']);
    expect(messages(deck(one, '__smoke'))).toEqual(['deck.id invalid id']);
    expect(messages(deck([{ id: '_a', type: 'text' }]))).toEqual([
      'deck.beats[0].id must be a unique valid id',
    ]);
  });
});
