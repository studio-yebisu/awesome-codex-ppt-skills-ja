/**
 * beat 'video'(CONTRACTS C4). parts: frame, media, caption. primary: frame.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--video" data-beat="<id>">는 build가 id를 채운다.
 */

import { add, asset, node, root, sourceText } from './helpers.js';
/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'video',
  primary: 'frame',
  fields: {
    src: {
      type: 'asset',
      required: true,
      doc: 'mp4 경로',
    },
    poster: {
      type: 'asset',
      required: true,
      doc: '포스터 이미지',
    },
    alt: {
      type: 'string',
      required: true,
      doc: '대체 텍스트',
    },
    mode: {
      type: 'enum',
      values: ['scrub', 'play', 'loop'],
      required: true,
      doc: 'scrub = 스크롤로 프레임, play/loop = 장면 안 재생',
    },
    frames: {
      type: 'asset',
      doc: 'frames.json 경로(scrub 필수)',
    },
    caption: {
      type: 'string',
      doc: '캡션',
    },
    mask: {
      type: 'object',
      fields: {
        type: {
          type: 'enum',
          values: ['text', 'shape'],
          required: true,
          doc: '마스크 종류',
        },
        text: {
          type: 'string',
          doc: 'text 마스크 글자',
        },
        shape: {
          type: 'string',
          doc: 'clip-path 값',
        },
      },
      doc: '영상 마스크',
    },
    source: {
      type: 'any',
      doc: '출처 id(deck.sources[].id). sample 덱이 아니면 수치·인용·실사에 필수',
    },
    credit: {
      type: 'string',
      doc: '스톡 영상 라이선스 표기',
    },
  },
  render(data, rc) {
    const parts = {};
    const view = root('video', rc);
    const frame = add(parts, 'frame', node(rc, 'figure', 'sl-video', view));
    let media;
    let mediaHandle;
    if (data.mode === 'scrub' && rc.media?.frameSequence) {
      const host = node(rc, 'div', 'sl-video__media', frame);
      const sequence = rc.media.frameSequence(host, asset(rc, data.frames));
      media = sequence.canvas;
      add(parts, 'media', media);
      mediaHandle = { seq: sequence };
    } else if ((data.mode === 'play' || data.mode === 'loop') && rc.media?.videoClip) {
      const host = node(rc, 'div', 'sl-video__media-host', frame);
      const clip = rc.media.videoClip(
        host,
        {
          src: asset(rc, data.src),
          poster: asset(rc, data.poster),
          loop: data.mode === 'loop',
          mode: data.mode,
        },
        { exportMode: rc.mode === 'export' },
      );
      media = clip.el;
      add(parts, 'media', media);
      mediaHandle = { clip };
    } else {
      media = add(parts, 'media', node(rc, 'video', 'sl-video__media', frame));
      media.src = asset(rc, data.src);
      media.poster = asset(rc, data.poster);
      media.muted = true;
      media.playsInline = true;
      media.loop = data.mode === 'loop';
      media.setAttribute('aria-label', data.alt);
    }
    if (data.mask) {
      media.classList.add('sl-mask');
      if (data.mask.type === 'shape' && data.mask.shape) media.style.clipPath = data.mask.shape;
      if (data.mask.type === 'text' && data.mask.text) media.dataset.maskText = data.mask.text;
    }
    if (data.caption) add(parts, 'caption', node(rc, 'figcaption', 'sl-video__caption', frame, data.caption));
    if (data.credit) add(parts, 'credit', node(rc, 'small', 'sl-video__credit', frame, data.credit));
    if (data.source)
      add(parts, 'source', node(rc, 'small', 'sl-video__source', frame, sourceText(rc, data.source)));
    return { root: view, parts, media: mediaHandle };
  },
};
