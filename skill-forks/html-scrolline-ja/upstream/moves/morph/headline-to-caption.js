/** Shrinks an outgoing headline into an incoming media caption. */
import { transferVars } from '../../engine/index.js';
import { finishLink } from '../_shared/link.js';
import { seg } from '../_shared/timeline.js';

export default {
  id: 'headline-to-caption',
  family: 'morph',
  role: 'link',
  accepts: ['video', 'photo'],
  sources: ['match-cut', 'inline-image-expand'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.6, max: 2.4, doc: '전체 길이(u)' },
    fromPart: { type: 'part', default: 'block', doc: 'fromPart(안무 설명의 같은 이름)' },
    toPart: { type: 'part', default: 'caption', doc: 'toPart(안무 설명의 같은 이름)' },
  },
  handoff(p) {
    return { from: { part: p.fromPart }, to: { part: p.toPart } };
  },
  timing: (p) => ({ duration: p.duration ?? 1.4, stops: [] }),
  build(tl, ctx, p) {
    const { from, to } = ctx.handoff,
      d = p.duration,
      part = (a, b) => ({ duration: d * (b - a) });
    const frame = ctx.beat.part('frame');
    const vars = transferVars(from.rect, to.rect);
    const uniform = Math.min(vars.scaleX, vars.scaleY);
    ctx.initial(from.node, { transformOrigin: '0 0', autoAlpha: 1 });
    ctx.initial(to.node, { autoAlpha: 0 });
    if (frame.length) ctx.initial(frame, { clipPath: 'inset(50% 50% 50% 50%)' });
    tl.to(
      from.node,
      {
        x: vars.x,
        y: vars.y,
        scaleX: uniform,
        scaleY: uniform,
        transformOrigin: '0 0',
        ...part(0, 0.55),
        ease: ctx.ease('inout'),
      },
      0,
    );
    tl.to(from.node, { ...vars, ...part(0.85, 1), ease: ctx.ease('inout') }, d * 0.85);
    if (frame.length)
      tl.to(frame, { clipPath: 'inset(0% 0% 0% 0%)', ...part(0.2, 0.8), ease: ctx.ease('inout') }, d * 0.2);
    finishLink(tl, ctx, { at: d, cross: Math.min(0.1, d * 0.15) });
  },
};
