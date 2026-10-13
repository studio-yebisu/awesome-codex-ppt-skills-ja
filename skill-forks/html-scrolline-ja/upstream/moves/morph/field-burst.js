/** Opens an outgoing prompt field into an incoming media frame. */
import { toInset, transferVars } from '../../engine/index.js';
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { seg, slots } from '../_shared/timeline.js';

export default {
  id: 'field-burst',
  family: 'morph',
  role: 'link',
  accepts: ['video', 'photo'],
  sources: ['clip-reveal', 'split-panel-handoff', 'text-particle-dissolve'],
  reduce: 'fade',
  params: { duration: { type: 'number', default: 1.3, min: 0.6, max: 2.4, doc: '전체 길이(u)' } },
  handoff() {
    return { from: { part: 'field' }, to: { part: 'frame' } };
  },
  timing: (p) => ({ duration: p.duration ?? 1.3, stops: [] }),
  build(tl, ctx, p) {
    const { from, to } = ctx.handoff,
      d = p.duration,
      part = (a, b) => ({ duration: d * (b - a) });
    const caret = ctx.from.part('caret'),
      chars = ctx.from.part('char');
    ctx.initial(from.node, { autoAlpha: 1, transformOrigin: '0 0' });
    ctx.initial(to.node, { clipPath: toInset(from.rect, ctx.viewport), autoAlpha: 0 });
    if (caret.length) ctx.initial(caret, { scaleX: 1, backgroundColor: colorOf(ctx, 'accent') });
    // (chars keep the alpha type-on gave them; only the transform/filter rest state is ours)
    if (chars.length) ctx.initial(chars, { y: 0, filter: 'blur(0px)' });
    if (caret.length) tl.to(caret, { scaleX: 1.08, ...part(0, 0.075), ease: ctx.ease('out') }, 0);
    if (caret.length) tl.to(caret, { scaleX: 1, ...part(0.075, 0.15), ease: ctx.ease('in') }, d * 0.075);
    if (!ctx.reduce)
      slots(chars.length, {
        start: d * 0.1,
        each: chars.length > 1 ? Math.min(d * 0.02, (d * 0.2) / (chars.length - 1)) : 0,
      }).forEach((slot, i) =>
        tl.to(
          chars[i],
          {
            y: -24 * ctx.viewport.px,
            filter: 'blur(3px)',
            duration: d * 0.25,
            ease: ctx.ease('in'),
          },
          slot.at,
        ),
      );
    tl.to(
      to.node,
      { clipPath: 'inset(0% 0% 0% 0%)', autoAlpha: 1, ...part(0.25, 0.8), ease: ctx.ease('inout') },
      d * 0.25,
    );
    tl.to(
      from.node,
      { ...transferVars(from.rect, to.rect), ...part(0.25, 0.8), ease: ctx.ease('inout') },
      d * 0.25,
    );
    // the typed text bursts and is gone before the frame is fully open; the label leaves with it
    tl.to(from.node, { autoAlpha: 0, duration: d * 0.25, ease: ctx.ease('in') }, d * 0.3);
    const label = ctx.from.part('label');
    if (label.length) {
      ctx.initial(label, { autoAlpha: 1 });
      tl.to(label, { autoAlpha: 0, duration: d * 0.15, ease: ctx.ease('in') }, d * 0.1);
    }
    finishLink(tl, ctx, { at: d, cross: Math.min(0.15, d * 0.2) });
  },
};
