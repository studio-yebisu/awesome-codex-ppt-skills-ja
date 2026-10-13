/** Carries a media frame into the next metric or text figure. */
import { toInset, transferVars } from '../../engine/index.js';
import { finishLink } from '../_shared/link.js';
import { seg } from '../_shared/timeline.js';

export default {
  id: 'frame-to-figure',
  family: 'morph',
  role: 'link',
  accepts: ['number', 'text'],
  sources: ['scale-swap', 'match-cut', 'clip-reveal'],
  reduce: 'fade',
  params: { duration: { type: 'number', default: 1.4, min: 0.8, max: 2.4, doc: '전체 길이(u)' } },
  handoff() {
    return { from: { part: 'frame' }, to: { part: 'value' } };
  },
  timing: (p) => ({ duration: p.duration ?? 1.4, stops: [] }),
  build(tl, ctx, p) {
    const { from, to } = ctx.handoff,
      d = p.duration,
      part = (a, b) => ({ duration: d * (b - a) });
    const caption = ctx.from.part('caption');
    const later = ['label', 'source'].flatMap((name) => ctx.beat.part(name));
    ctx.initial(from.node, { clipPath: 'inset(0% 0% 0% 0%)', transformOrigin: '0 0', autoAlpha: 1 });
    ctx.initial(to.node, { autoAlpha: 0 });
    if (caption.length) ctx.initial(caption, { autoAlpha: 1 });
    if (later.length) ctx.initial(later, { autoAlpha: 0 });
    if (caption.length) tl.to(caption, { autoAlpha: 0, ...part(0, 0.15), ease: ctx.ease('in') }, 0);
    tl.to(
      from.node,
      {
        ...transferVars(from.rect, to.rect),
        clipPath: toInset(to.rect, ctx.viewport),
        ...part(0.1, 0.75),
        ease: ctx.ease('inout'),
      },
      d * 0.1,
    );
    finishLink(tl, ctx, { at: d * 0.85, cross: Math.min(0.15, d * 0.15) });
  },
};
