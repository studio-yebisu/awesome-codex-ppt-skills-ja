/**
 * beat 'photo'(CONTRACTS C4). parts: frame, media, caption. primary: frame.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--photo" data-beat="<id>">는 build가 id를 채운다.
 */

import { add, asset, node, root, sourceText } from './helpers.js';
/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'photo',
  primary: 'frame',
  fields: {
    src: {
      type: 'asset',
      required: true,
      doc: '이미지 경로(assets/…)',
    },
    alt: {
      type: 'string',
      required: true,
      doc: '대체 텍스트',
    },
    focus: {
      type: 'object',
      fields: {
        x: {
          type: 'number',
          min: 0,
          max: 1,
          default: 0.5,
          doc: '초점 x',
        },
        y: {
          type: 'number',
          min: 0,
          max: 1,
          default: 0.5,
          doc: '초점 y',
        },
      },
      doc: '초점(0..1), background-position·transform-origin',
    },
    caption: {
      type: 'string',
      doc: '캡션',
    },
    credit: {
      type: 'string',
      doc: '저작자 표기',
    },
    source: {
      type: 'any',
      doc: '출처 id(deck.sources[].id). sample 덱이 아니면 수치·인용·실사에 필수',
    },
  },
  render(data, rc) {
    const parts = {};
    const view = root('photo', rc);
    const frame = add(parts, 'frame', node(rc, 'figure', 'sl-photo', view));
    const media = add(parts, 'media', node(rc, 'img', 'sl-photo__media', frame));
    media.src = asset(rc, data.src);
    media.alt = data.alt;
    const focus = data.focus ?? { x: 0.5, y: 0.5 };
    media.style.objectPosition = `${focus.x * 100}% ${focus.y * 100}%`;
    if (data.caption || data.credit)
      add(
        parts,
        'caption',
        node(
          rc,
          'figcaption',
          'sl-photo__caption',
          frame,
          [data.caption, data.credit].filter(Boolean).join(' — '),
        ),
      );
    if (data.source)
      add(parts, 'source', node(rc, 'small', 'sl-photo__source', frame, sourceText(rc, data.source)));
    return { root: view, parts };
  },
};
