/** A display-word mask brings photo or video into view. Shared by data, launch and rail. */
import { applyTextMask } from '../_shared/mask.js';
import { seg } from '../_shared/timeline.js';

const mediaParts = (ctx) => ctx.beat.part('media').filter((node) => !ctx.skipNodes?.includes(node));
const captionParts = (ctx) => ctx.beat.part('caption').filter((node) => !ctx.skipParts.includes('caption'));

export default {
  id: 'mask-word-in',
  family: 'media',
  role: 'enter',
  accepts: ['video', 'photo'],
  sources: ['text-window-fill', 'tracking-reveal'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.6, max: 2.5, doc: '전체 길이(u)' },
    brightFrom: { type: 'number', default: 0.3, min: 0, max: 1, doc: '시작 밝기' },
    brightTo: { type: 'number', default: 1.3, min: 1, max: 1.6, doc: '끝 밝기(마스크 안 대비)' },
    scaleFrom: { type: 'number', default: 0.94, min: 0.8, max: 1, doc: '시작 scale' },
    trackFrom: { type: 'number', default: 1.12, min: 1, max: 1.3, doc: '시작 maskSize 가로 배율' },
    riseFrom: { type: 'number', default: 0, min: 0, max: 100, doc: '시작 maskPosition y(%)' },
    captionIn: { type: 'boolean', default: false, doc: 'caption을 0.80–1.00에 함께 올림' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const media = mediaParts(ctx);
    const caption = captionParts(ctx);
    const text = ctx.beat.data.mask?.text ?? media[0]?.dataset.maskText ?? ctx.beat.data.maskText ?? 'MASK';
    const rect = ctx.beat.anchor('media').rect;
    for (const node of media) {
      applyTextMask(ctx, node, text, { rect });
      ctx.initial(node, {
        autoAlpha: 0,
        scale: params.scaleFrom,
        filter: `brightness(${params.brightFrom})`,
        maskSize: `${params.trackFrom * 100}% 100%`,
        maskPosition: `50% ${params.riseFrom}%`,
      });
      tl.to(
        node,
        {
          autoAlpha: 1,
          scale: 1,
          filter: `brightness(${params.brightTo})`,
          maskPosition: '50% 0%',
          ...seg(params.duration, 0, 0.6),
          ease: ctx.ease(params.riseFrom > 0 ? 'land' : 'out'),
        },
        0,
      );
      tl.to(node, { maskSize: '100% 100%', ...seg(params.duration, 0.2, 0.8), ease: ctx.ease('inout') }, 0);
    }
    ctx.initial(caption, { autoAlpha: 0, yPercent: 40 });
    if (params.captionIn)
      tl.to(
        caption,
        { autoAlpha: 1, yPercent: 0, ...seg(params.duration, 0.8, 1), ease: ctx.ease('out') },
        0,
      );
  },
};
