/** Fold a primary block flat, then extend it as a rail. */
import { transferVars } from '../../engine/index.js';
import { colorOf } from '../_shared/color.js';
import { finishLink, ghost } from '../_shared/link.js';

export default {
  id: 'fold-to-rail',
  family: 'rail',
  role: 'link',
  accepts: ['chronology'],
  sources: ['split-panel-handoff', 'line-draw', 'scale-swap', 'push-transition'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.8, max: 2.4, doc: '전체 길이(u)' },
    lineWidth: { type: 'number', default: 2, min: 1, max: 4, doc: 'lineWidth(안무 설명의 같은 이름)' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  handoff() {
    return { from: { part: '' }, to: { part: 'track' } };
  },
  build(tl, ctx, p) {
    const d = p.duration,
      { from, to } = ctx.handoff;
    if (ctx.reduce) return finishLink(tl, ctx, { at: d, cross: 0.12 });
    const carry = ghost(ctx, from.node, from.rect);
    carry.style.background = colorOf(ctx, 'accent');
    ctx.initial(carry, {
      autoAlpha: 1,
      x: 0,
      y: 0,
      scaleX: 1,
      scaleY: 1,
      borderRadius: 0,
      transformOrigin: '0 0',
    });
    ctx.initial(to.node, { autoAlpha: 0 });
    ctx.initial(from.node, { autoAlpha: 1 });
    ctx.initial(to.node, { scaleX: 0, transformOrigin: '50% 50%' });
    tl.to(carry, { scaleY: 0.02, autoAlpha: 0, duration: d * 0.35, ease: ctx.ease('in') }, 0);
    tl.to(
      carry,
      {
        ...transferVars(from.rect, to.rect),
        height: p.lineWidth,
        autoAlpha: 1,
        duration: d * 0.15,
        ease: ctx.ease('out'),
      },
      d * 0.25,
    );
    tl.to(to.node, { scaleX: 1, duration: d * 0.45, ease: ctx.ease('out') }, d * 0.35);
    const stem = ctx.beat.part('stem')[0];
    if (stem) {
      ctx.initial(stem, { scaleY: 0 });
      tl.to(stem, { scaleY: 1, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.8);
    }
    finishLink(tl, ctx, { at: d, cross: 0.12, from: [from.node, carry] });
  },
};
