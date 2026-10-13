/**
 * Splits a giant word-mask into two doors, leaving full-bleed video. Kinetic signature.
 * The footage keeps one mask with three layers: the left glyphs, the right glyphs and the gap
 * between them. The doors slide apart (each still showing the footage inside its strokes) and the
 * gap widens until it is the whole frame.
 */
import { driveValue } from '../_shared/drive.js';
import { applyTextMask } from '../_shared/mask.js';
import { glyphMask } from '../_shared/glyph-mask.js';

export default {
  id: 'word-door',
  family: 'media',
  role: 'step',
  accepts: ['video'],
  sources: ['text-window-fill', 'text-cutout-zoom', 'split-slide', 'inline-image-expand'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 1.2, max: 4, doc: '전체 길이(u)' },
    split: { type: 'integer', default: -1, doc: '갈라질 글자 index(−1 = 가운데)' },
    gap: { type: 'number', default: 0.06, min: 0, max: 0.2, doc: '처음 벌어지는 틈(프레임 폭 비율)' },
    mediaScaleFrom: {
      type: 'number',
      default: 1.08,
      min: 1,
      max: 1.3,
      doc: 'mediaScaleFrom(안무 설명의 같은 이름)',
    },
    maskScale: {
      type: 'number',
      default: 0.78,
      min: 0.4,
      max: 0.95,
      doc: '마스크 글자 높이(glyph-rise와 같게)',
    },
    maskY: {
      type: 'number',
      default: 0.5,
      min: 0.3,
      max: 0.7,
      doc: '마스크 글자 세로 중심(glyph-rise와 같게)',
    },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const media = ctx.beat.part('media').filter((n) => !ctx.skipNodes?.includes(n));
    if (!media.length) return;
    const source = ctx.beat.data.mask?.text ?? media[0]?.dataset.maskText ?? 'WORD';
    const chars = [...source];
    const split =
      params.split < 0 ? Math.ceil(chars.length / 2) : Math.max(1, Math.min(chars.length - 1, params.split));
    const rect = ctx.beat.anchor('media').rect,
      d = params.duration;
    const opts = { scale: params.maskScale, cy: params.maskY };
    const left = glyphMask(ctx, source, rect, { ...opts, from: 0, to: split, split });
    const right = glyphMask(ctx, source, rect, { ...opts, from: split });
    const W = rect.w;
    if (!left || !right) {
      // No canvas text (tests): fall back to two plain text masks and a fading word.
      for (const node of media) applyTextMask(ctx, node, source, { rect });
      tl.to(media, { maskSize: '400% 400%', duration: d * 0.9, ease: ctx.ease('inout') }, 0);
      tl.set(media, { maskImage: 'none', webkitMaskImage: 'none' }, d);
      return;
    }
    const cut = left.splitX;
    const layers = `url("${left.url}"), url("${right.url}"), linear-gradient(#fff, #fff)`;
    // o = how far each door has slid out (left door −o, right door +o); the gap between them is 2o
    const paint = (o) => {
      const gapX = cut - o,
        gapW = Math.max(0, 2 * o);
      const pos = `${-o}px 0px, ${o}px 0px, ${gapX}px 0px`;
      const size = `${W}px 100%, ${W}px 100%, ${gapW}px 100%`;
      for (const node of media)
        Object.assign(node.style, {
          maskPosition: pos,
          webkitMaskPosition: pos,
          maskSize: size,
          webkitMaskSize: size,
        });
    };
    // Swap the single rise mask for the three-layer door at the start of the step.
    tl.set(
      media,
      {
        maskImage: layers,
        webkitMaskImage: layers,
        maskRepeat: 'no-repeat',
        webkitMaskRepeat: 'no-repeat',
      },
      0,
    );
    ctx.initial(media, { scale: params.mediaScaleFrom, filter: 'brightness(0.92)' });
    const crack = W * params.gap * 0.5;
    // driveValue, not onUpdate: seek()/pause(t) suppress callbacks (C5 v2.2)
    if (ctx.reduce)
      driveValue(tl, paint, { from: 0, to: W, at: 0, duration: d * 0.9, ease: ctx.ease('inout') });
    else {
      // crack open (0–0.22), hold a beat, then the doors run off-frame (0.3–0.85)
      driveValue(tl, paint, { from: 0, to: crack, at: 0, duration: d * 0.22, ease: ctx.ease('out') });
      driveValue(tl, paint, { from: crack, to: W, at: d * 0.3, duration: d * 0.55, ease: ctx.ease('inout') });
    }
    tl.to(media, { scale: 1, filter: 'brightness(1)', duration: d * 0.6, ease: ctx.ease('inout') }, d * 0.3);
    tl.set(media, { maskImage: 'none', webkitMaskImage: 'none' }, d);
  },
};
