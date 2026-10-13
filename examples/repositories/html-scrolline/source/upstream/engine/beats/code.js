/**
 * beat 'code'(CONTRACTS C4). parts: block, line, token, caret. primary: block.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--code" data-beat="<id>">는 build가 id를 채운다.
 */

import { add, node, root } from './helpers.js';
/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'code',
  primary: 'block',
  fields: {
    code: {
      type: 'string',
      required: true,
      doc: '코드 원문',
    },
    lang: {
      type: 'string',
      required: true,
      doc: '언어 이름',
    },
    highlight: {
      type: 'array',
      doc: '강조 줄 범위',
      of: {
        type: 'array',
        of: {
          type: 'integer',
          min: 1,
          doc: '줄 번호(1-base)',
        },
        doc: '[from, to]',
      },
    },
    caption: {
      type: 'string',
      doc: '캡션',
    },
  },
  render(data, rc) {
    const parts = {};
    const view = root('code', rc);
    const block = add(parts, 'block', node(rc, 'pre', `sl-code language-${data.lang}`, view));
    const ranges = data.highlight ?? [];
    String(data.code)
      .split('\n')
      .forEach((source, i) => {
        const line = add(parts, 'line', node(rc, 'code', 'sl-code__line', block));
        line.dataset.line = String(i + 1);
        if (ranges.some(([from, to]) => i + 1 >= from && i + 1 <= to)) line.dataset.highlight = 'true';
        add(parts, 'token', node(rc, 'span', 'sl-code__token', line, source || ' '));
      });
    add(parts, 'caret', node(rc, 'span', 'sl-code__caret', block, '▍'));
    if (data.caption) node(rc, 'p', 'sl-code__caption', view, data.caption);
    return { root: view, parts };
  },
};
