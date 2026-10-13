/** A full frame arcs down into an event thumbnail. */
import { transferVars } from '../../engine/index.js';
import { eventPart } from '../_shared/event-part.js';
import { finishLink, ghost, takeoff } from '../_shared/link.js';

export default {
  id: 'rail-drop',
  family: 'rail',
  role: 'link',
  accepts: ['chronology'],
  sources: ['scale-swap', 'match-cut', 'match-on-action'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.6, min: 0.8, max: 2.6, doc: '전체 길이(u)' },
    toEvent: { type: 'integer', default: 0, doc: '0..events-1' },
    arc: { type: 'number', default: 0.06, min: 0, max: 0.2, doc: 'arc(안무 설명의 같은 이름)' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  handoff(p, { to } = {}) {
    return { from: { part: 'frame' }, to: eventPart(to?.events, 'media', p.toEvent) };
  },
  build(tl, ctx, p) {
    const d = p.duration,
      { from, to } = ctx.handoff;
    if (ctx.reduce) return finishLink(tl, ctx, { at: d, cross: 0.12 });
    const carry = ghost(ctx, from.node, from.rect);
    const caption = ctx.from.part('caption');
    const stem = ctx.beat.part('stem').at(p.toEvent);
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
    takeoff(tl, ctx);
    tl.to(caption, { autoAlpha: 0, duration: d * 0.2, ease: ctx.ease('in') }, 0);
    tl.to(
      carry,
      { borderRadius: 12, y: -p.arc * ctx.viewport.h, duration: d * 0.15, ease: ctx.ease('out') },
      0,
    );
    const landing = transferVars(from.rect, to.rect);
    tl.to(carry, { ...landing, duration: d * 0.65, ease: ctx.ease('in') }, d * 0.15);
    if (stem) {
      ctx.initial(stem, { scaleY: 0 });
      tl.to(stem, { scaleY: 1, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.7);
    }
    finishLink(tl, ctx, { at: d, cross: 0.12, from: [from.node, carry] });
  },
};
