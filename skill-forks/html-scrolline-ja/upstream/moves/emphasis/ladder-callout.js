/** Connect closing text lines to depth-ladder rungs. Used by zoom decks. */
import { colorOf } from '../_shared/color.js';
import { polyline, drawOn, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';

export default {
  id: 'ladder-callout',
  family: 'emphasis',
  role: 'enter',
  accepts: ['text'],
  sources: ['annotation-callout', 'line-draw', 'sequence-message-draw'],
  reduce: 'fade',
  params: {
    rungs: { type: 'array', default: [0], doc: '각 줄이 연결될 사다리 칸 번호' },
    stagger: { type: 'number', default: 0.18, min: 0.08, max: 0.4, doc: '줄 사이 시차(u)' },
    duration: { type: 'number', default: 1.8, min: 1, max: 3, doc: '전체 길이(u)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      lines = ctx.beat.part('line');
    const targets = lines.length ? lines : ctx.beat.part('block');
    const x = px(ctx, ctx.tokens.ladderX ?? 72),
      top = px(ctx, ctx.tokens.ladderTop ?? 180),
      step = px(ctx, ctx.tokens.ladderStep ?? 32),
      accent = colorOf(ctx, 'accent');
    const svg = svgLayer(ctx),
      spread = Math.min(d * 0.45, Math.max(0, targets.length - 1) * params.stagger);
    ctx.initial(targets, { autoAlpha: 0, y: px(ctx, 14) });
    targets.forEach((node, i) => {
      const rect = ctx.beat.anchor(lines.length ? 'line' : 'block', i).rect;
      const rung = params.rungs[Math.min(i, params.rungs.length - 1)] ?? 0,
        y = top + rung * step,
        at = d * 0.1 + (targets.length < 2 ? 0 : (i / (targets.length - 1)) * spread);
      const end = { x: rect.x, y: rect.y + rect.h / 2 },
        bend = Math.max(x + px(ctx, 28), end.x - px(ctx, 28));
      const leader = polyline(svg, [{ x, y }, { x: bend, y }, { x: bend, y: end.y }, end], {
        stroke: accent,
        'stroke-width': px(ctx, 1.5),
      });
      ctx.initial(leader, { strokeDashoffset: 1, opacity: 1 });
      drawOn(tl, leader, { at, duration: d * 0.32, ease: 'none' });
      tl.to(node, { autoAlpha: 1, y: 0, duration: d * 0.26, ease: ctx.ease('out') }, at + d * 0.15);
      tl.to(leader, { opacity: 0.5, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.85);
    });
    if (params.rungs.length !== targets.length && import.meta.env?.DEV)
      console.warn('ladder-callout: rungs length differs from line count; reusing last rung');
  },
};
