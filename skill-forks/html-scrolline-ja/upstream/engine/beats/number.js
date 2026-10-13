/**
 * beat 'number'(CONTRACTS C4). parts: value, digits, unit, label, source. primary: value.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--number" data-beat="<id>">는 build가 id를 채운다.
 */

import { add, node, root, sourceText } from './helpers.js';
/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'number',
  primary: 'value',
  fields: {
    value: {
      type: 'number',
      required: true,
      doc: '최종 값',
    },
    label: {
      type: 'string',
      required: true,
      doc: '숫자 뜻 한 줄',
    },
    format: {
      type: 'object',
      fields: {
        prefix: {
          type: 'string',
          doc: '앞 기호',
        },
        suffix: {
          type: 'string',
          doc: '뒤 기호',
        },
        decimals: {
          type: 'integer',
          min: 0,
          max: 4,
          default: 0,
          doc: '소수 자리',
        },
        unit: {
          type: 'string',
          doc: '단위',
        },
      },
      doc: 'Intl.NumberFormat(lang) 기반 표기',
    },
    from: {
      type: 'number',
      default: 0,
      doc: 'count-up 시작 값',
    },
    source: {
      type: 'any',
      doc: '출처 id(deck.sources[].id). sample 덱이 아니면 수치·인용·실사에 필수',
    },
  },
  render(data, rc) {
    const parts = {};
    const view = root('number', rc);
    const format = data.format ?? {};
    const value = add(parts, 'value', node(rc, 'div', 'sl-number__value', view));
    if (format.prefix) value.append(node(rc, 'span', 'sl-number__prefix', null, format.prefix));
    const digits = add(
      parts,
      'digits',
      node(
        rc,
        'span',
        'sl-number__digits',
        value,
        new Intl.NumberFormat(rc.lang ?? 'ko', {
          minimumFractionDigits: format.decimals ?? 0,
          maximumFractionDigits: format.decimals ?? 0,
        }).format(data.value),
      ),
    );
    if (format.suffix) value.append(node(rc, 'span', 'sl-number__suffix', null, format.suffix));
    if (format.unit) add(parts, 'unit', node(rc, 'span', 'sl-number__unit', value, format.unit));
    add(parts, 'label', node(rc, 'p', 'sl-number__label', view, data.label));
    if (data.source)
      add(parts, 'source', node(rc, 'small', 'sl-number__source', view, sourceText(rc, data.source)));
    return { root: view, parts };
  },
};
