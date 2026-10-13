/**
 * beat 'text'(CONTRACTS C4). parts: block, line, word, em. primary: block.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--text" data-beat="<id>">는 build가 id를 채운다.
 */

import { add, root, node, textWords } from './helpers.js';

/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'text',
  primary: 'block',
  fields: {
    text: {
      type: 'string',
      required: true,
      doc: '한 문장. 어절 단위로 쪼갠다',
    },
    emphasis: {
      type: 'array',
      of: {
        type: 'string',
        doc: '강조할 부분 문자열',
      },
      doc: '강조 부분 문자열 목록(part em)',
    },
    size: {
      type: 'enum',
      values: ['xl', 'l', 'm'],
      default: 'l',
      doc: '글자 크기 단계',
    },
    lines: {
      type: 'array',
      of: {
        type: 'string',
        doc: '한 줄',
      },
      doc: '명시 줄 나눔(있으면 text 대신 사용, 합치면 text와 같아야 함)',
    },
  },
  render(data, rc) {
    const parts = {};
    const view = root('text', rc);
    const block = add(parts, 'block', node(rc, 'div', `sl-text sl-text--${data.size ?? 'l'}`, view));
    const lines = data.lines?.length ? data.lines : String(data.text).split('\n');
    const words = lines.flatMap((line) => {
      const lineEl = add(parts, 'line', node(rc, 'div', 'sl-text__line', block));
      return textWords(rc, lineEl, line, parts);
    });
    // 강조 구절은 여러 어절·줄에 걸칠 수 있다: 어절을 공백 하나로 이은 글에서 구절 위치를 찾아 겹치는 어절을 모두 감싼다.
    const marked = new Set();
    let at = 0;
    const spans = words.map((word) => {
      const span = [at, at + word.textContent.length];
      at = span[1] + 1;
      return span;
    });
    const joined = words.map((word) => word.textContent).join(' ');
    for (const raw of data.emphasis ?? []) {
      const phrase = String(raw ?? '').trim().split(/\s+/).join(' ');
      if (!phrase) continue;
      for (let from = joined.indexOf(phrase); from >= 0; from = joined.indexOf(phrase, from + 1)) {
        const to = from + phrase.length;
        spans.forEach(([start, end], index) => {
          if (start < to && from < end) marked.add(index);
        });
      }
    }
    words.forEach((word, index) => {
      if (!marked.has(index)) return;
      const em = add(parts, 'em', node(rc, 'mark', 'sl-text__em', null, word.textContent));
      word.replaceChildren(em);
    });
    return { root: view, parts };
  },
};
