/**
 * beat 'quote'(CONTRACTS C4). parts: block, mark, word, by. primary: block.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--quote" data-beat="<id>">는 build가 id를 채운다.
 */

import { add, node, root, sourceText, textWords } from './helpers.js';
/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'quote',
  primary: 'block',
  fields: {
    text: {
      type: 'string',
      required: true,
      doc: '인용문',
    },
    by: {
      type: 'string',
      required: true,
      doc: '말한 사람',
    },
    role: {
      type: 'string',
      doc: '직함',
    },
    source: {
      type: 'any',
      doc: '출처 id(deck.sources[].id). sample 덱이 아니면 수치·인용·실사에 필수',
    },
  },
  render(data, rc) {
    const parts = {};
    const view = root('quote', rc);
    const block = add(parts, 'block', node(rc, 'blockquote', 'sl-quote', view));
    add(parts, 'mark', node(rc, 'span', 'sl-quote__mark', block, '“'));
    const body = node(rc, 'span', 'sl-quote__text', block);
    textWords(rc, body, data.text, parts);
    const cite = add(parts, 'by', node(rc, 'cite', 'sl-quote__by', view, data.by));
    if (data.role) cite.append(document.createTextNode(`, ${data.role}`));
    if (data.source)
      add(parts, 'source', node(rc, 'small', 'sl-quote__source', view, sourceText(rc, data.source)));
    return { root: view, parts };
  },
};
