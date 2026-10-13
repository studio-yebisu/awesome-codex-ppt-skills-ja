/**
 * beat 'compare'(CONTRACTS C4). parts: item, label, value, text, divider, verdict. primary: item.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--compare" data-beat="<id>">는 build가 id를 채운다.
 */

import { add, asset, node, root, sourceText } from './helpers.js';
/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'compare',
  primary: 'item',
  fields: {
    items: {
      type: 'array',
      required: true,
      doc: '비교 항목 2~4개',
      of: {
        type: 'object',
        doc: '항목',
        fields: {
          label: {
            type: 'string',
            required: true,
            doc: '이름',
          },
          value: {
            type: 'number',
            doc: '수치',
          },
          text: {
            type: 'string',
            doc: '한 줄',
          },
          media: {
            type: 'asset',
            doc: '이미지',
          },
        },
      },
    },
    verdict: {
      type: 'string',
      doc: '결론 한 줄',
    },
    source: {
      type: 'any',
      doc: '출처 id 또는 id 배열',
    },
  },
  render(data, rc) {
    const parts = {};
    const view = root('compare', rc);
    const list = node(rc, 'div', 'sl-compare', view);
    data.items.forEach((item, index) => {
      if (index) add(parts, 'divider', node(rc, 'span', 'sl-compare__divider', list, 'vs'));
      const card = add(parts, 'item', node(rc, 'article', 'sl-compare__item', list));
      add(parts, 'label', node(rc, 'h3', 'sl-compare__label', card, item.label));
      if (item.value != null)
        add(
          parts,
          'value',
          node(
            rc,
            'strong',
            'sl-compare__value',
            card,
            new Intl.NumberFormat(rc.lang ?? 'ko').format(item.value),
          ),
        );
      if (item.text) add(parts, 'text', node(rc, 'p', 'sl-compare__text', card, item.text));
      if (item.media) {
        const img = node(rc, 'img', 'sl-compare__media', card);
        img.src = asset(rc, item.media);
        img.alt = item.label;
      }
    });
    if (data.verdict) add(parts, 'verdict', node(rc, 'p', 'sl-compare__verdict', view, data.verdict));
    if (data.source)
      add(parts, 'source', node(rc, 'small', 'sl-compare__source', view, sourceText(rc, data.source)));
    return { root: view, parts };
  },
};
