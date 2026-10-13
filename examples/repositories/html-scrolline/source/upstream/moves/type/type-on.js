/** Type a prompt field deterministically, either by character or word groups. */
import { colorOf } from '../_shared/color.js';
import { line, svgLayer, drawOn } from '../_shared/stroke.js';

const units = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name));
const textOf = (data) => String(data?.text ?? '');
const wordCount = (data) =>
  String(data?.text ?? '')
    .trim()
    .split(/\s+/)
    .filter(Boolean).length;

export default {
  id: 'type-on',
  family: 'type',
  role: 'enter',
  accepts: ['prompt'],
  sources: ['typewriter', 'context-caret', 'karaoke-caption'],
  reduce: 'self',
  params: {
    speed: { type: 'number', default: 30, min: 8, max: 120, doc: 'u당 글자 수' },
    labelFirst: { type: 'boolean', default: true, doc: '라벨을 먼저 표시' },
    chunk: { type: 'enum', default: 'char', values: ['char', 'word'], doc: '표시 단위' },
    chunkMax: { type: 'integer', default: 3, min: 1, max: 6, doc: '어절 묶음 최대 크기' },
    pause: { type: 'number', default: 0.35, min: 0, max: 0.8, doc: '묶음 사이 정지(u)' },
    speakerFirst: { type: 'boolean', default: false, doc: '첫 어절 즉시 표시' },
    rule: { type: 'boolean', default: false, doc: 'field 테두리 선을 그림' },
  },
  timing(p, data) {
    return {
      duration:
        0.4 +
        textOf(data).length / p.speed +
        (p.chunk === 'word' ? p.pause * Math.ceil(wordCount(data) / p.chunkMax) : 0),
      stops: [],
    };
  },
  build(tl, ctx, p) {
    const d = ctx.duration,
      chars = units(ctx, 'char'),
      words = units(ctx, 'word');
    const field = ctx.beat.anchor('field').rect,
      caret = units(ctx, 'caret');
    // caret은 글 끝에 inline으로 놓여 있다: 무대 좌표 rect를 caret 자기 자리(rest) 기준 translate로 바꾼다.
    const rest = caret.length ? ctx.beat.anchor('caret').rect : { x: 0, y: 0 },
      caretAt = (r, end = true) => ({ x: r.x + (end ? r.w : 0) - rest.x, y: r.y - rest.y }),
      start = chars.length ? caretAt(ctx.beat.anchor('char', 0).rect, false) : { x: field.x - rest.x, y: 0 };
    const label = units(ctx, 'label'),
      result = units(ctx, 'result');
    ctx.initial(result, { autoAlpha: 0 });
    ctx.initial(caret, { ...start, autoAlpha: 1, color: colorOf(ctx, 'accent') });
    if (p.labelFirst) {
      ctx.initial(label, { autoAlpha: 0 });
      tl.to(label, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, 0);
    }
    if (p.rule) {
      const svg = svgLayer(ctx),
        border = line(svg, field.x, field.y, field.x + field.w, field.y, {
          stroke: colorOf(ctx, 'rule'),
          'stroke-width': 1,
        });
      drawOn(tl, border, { at: 0, duration: d * 0.1, ease: ctx.ease('out') });
    }
    if (ctx.reduce) {
      const shown = words.length ? words : chars;
      ctx.initial(shown, { autoAlpha: 0 });
      tl.to(shown, { autoAlpha: 1, duration: d * 0.82, ease: ctx.ease('out') }, d * 0.1);
      return;
    }
    if (p.chunk === 'char' || !words.length) {
      ctx.initial(chars, { autoAlpha: 0 });
      chars.forEach((node, i) => {
        const at = d * (0.1 + (i / Math.max(1, chars.length)) * 0.82),
          rect = ctx.beat.anchor('char', i).rect;
        tl.set(node, { autoAlpha: 1 }, at);
        tl.set(caret, caretAt(rect), at);
      });
    } else {
      ctx.initial(words, { autoAlpha: 0 });
      let index = 0,
        at = d * 0.1;
      if (p.speakerFirst && words.length) {
        tl.set(words[0], { autoAlpha: 1 }, at);
        index = 1;
      }
      // Keep the RNG-selected boundaries within the same group count used by timing().
      const remaining = words.length - index,
        groups = Math.ceil(remaining / p.chunkMax);
      let groupIndex = 0;
      while (index < words.length) {
        const left = words.length - index,
          groupsLeft = groups - groupIndex;
        const minimum = Math.max(1, left - (groupsLeft - 1) * p.chunkMax);
        const maximum = Math.min(p.chunkMax, left - (groupsLeft - 1));
        const size = minimum + Math.floor(ctx.rng() * (maximum - minimum + 1));
        const group = words.slice(index, index + size),
          last = index + size - 1;
        tl.set(group, { autoAlpha: 1 }, at);
        tl.set(caret, caretAt(ctx.beat.anchor('word', last).rect), at);
        at += p.pause;
        index += size;
        groupIndex += 1;
      }
    }
  },
};
