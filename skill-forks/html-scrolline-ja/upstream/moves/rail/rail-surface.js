/** Surface the remaining rail events after a handoff. Used by fast chronology enters. */
import { railFocus } from '../_shared/rail-focus.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name)
    ? []
    : ctx.beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));
export default {
  id: 'rail-surface',
  family: 'rail',
  role: 'enter',
  accepts: ['chronology'],
  sources: ['fade-slide', 'stagger', 'overlapping-action'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.7, min: 0.3, max: 1.4, doc: 'Overall duration.' },
    stagger: { type: 'number', default: 0.04, min: 0, max: 0.1, doc: 'Delay between events.' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = ctx.duration,
      now = ctx.beat.part('now')[0] ? ctx.beat.anchor('now').rect.x : ctx.viewport.w / 2;
    const events = usable(ctx, 'event')
      .map((node, index) => ({
        node,
        index,
        distance: Math.abs(ctx.beat.anchor('event', index).rect.x - now),
      }))
      .sort((a, b) => a.distance - b.distance);
    if (events.length) railFocus(ctx, ctx.beat, ctx.beat.part('event').indexOf(events[0].node));
    events.forEach(({ node }, index) => {
      ctx.initial(node, { y: px(ctx, 14), autoAlpha: 0 });
      tl.to(
        node,
        { y: 0, autoAlpha: 1, duration: d * 0.35, ease: ctx.ease('out') },
        Math.min(d * 0.35, index * params.stagger),
      );
    });
    const label = usable(ctx, 'label'),
      counter = usable(ctx, 'counter');
    ctx.initial(label, { autoAlpha: 0 });
    ctx.initial(counter, { autoAlpha: 0 });
    tl.to(label, { autoAlpha: 1, duration: d * 0.7, ease: ctx.ease('out') }, d * 0.3);
    tl.to(counter, { autoAlpha: 1, duration: d * 0.7, ease: ctx.ease('out') }, d * 0.3);
  },
};
