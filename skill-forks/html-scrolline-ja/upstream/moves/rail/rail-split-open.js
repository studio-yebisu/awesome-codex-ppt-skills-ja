/** Split a rail at now and reveal the next frame. */
import { colorOf } from '../_shared/color.js';
import { finishLink, ghost } from '../_shared/link.js';

export default {
  id: 'rail-split-open',
  family: 'rail',
  role: 'link',
  accepts: ['video', 'photo'],
  sources: ['split-slide', 'symmetric-panel-open', 'counter-moving-matte', 'clip-reveal'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.5, min: 0.8, max: 2.6, doc: '전체 길이(u)' },
    lineHold: { type: 'number', default: 0.25, min: 0, max: 0.4, doc: 'lineHold(안무 설명의 같은 이름)' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  handoff() {
    return { from: { part: 'track' }, to: { part: 'frame' } };
  },
  build(tl, ctx, p) {
    const d = p.duration,
      { from, to } = ctx.handoff;
    if (ctx.reduce) return finishLink(tl, ctx, { at: d, cross: 0.12 });
    const left = ghost(ctx, from.node, from.rect),
      right = ghost(ctx, from.node, from.rect);
    const now = ctx.from.part('now')[0];
    const nowX = now ? ctx.from.anchor('now').point.x : ctx.viewport.w / 2;
    const line = document.createElement('div');
    Object.assign(line.style, {
      position: 'absolute',
      left: `${nowX}px`,
      top: '0',
      width: '2px',
      height: '100%',
      background: colorOf(ctx, 'accent'),
    });
    ctx.overlay.append(line);
    left.style.clipPath = `inset(0 ${Math.max(0, ctx.viewport.w - nowX)}px 0 0)`;
    right.style.clipPath = `inset(0 0 0 ${Math.max(0, nowX)}px)`;
    ctx.initial([left, right], { x: 0 });
    ctx.initial([to.node], { autoAlpha: 0, clipPath: 'inset(0 50% 0 50%)' });
    tl.set(from.node, { autoAlpha: 0 }, 0);
    tl.to(line, { autoAlpha: 1, duration: d * p.lineHold, ease: ctx.ease('out') }, 0);
    tl.to(left, { x: -nowX, duration: d * 0.55, ease: ctx.ease('inout') }, d * 0.2);
    tl.to(right, { x: ctx.viewport.w - nowX, duration: d * 0.55, ease: ctx.ease('inout') }, d * 0.2);
    tl.to(
      to.node,
      { autoAlpha: 1, clipPath: 'inset(0 0% 0 0%)', duration: d * 0.55, ease: ctx.ease('inout') },
      d * 0.2,
    );
    const caption = ctx.beat.part('caption');
    if (caption.length) {
      ctx.initial(caption, { y: 12, autoAlpha: 0 });
      tl.to(caption, { y: 0, autoAlpha: 1, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.7);
    }
    tl.to(line, { autoAlpha: 0, duration: d * 0.3, ease: ctx.ease('in') }, d * 0.7);
    finishLink(tl, ctx, { at: d, cross: 0.12 });
  },
};
