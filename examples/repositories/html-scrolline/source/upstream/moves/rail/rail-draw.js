/** Draw an initial chronology rail. Used when a rail chapter first enters. */
import { railFocus } from '../_shared/rail-focus.js';
import { reelFrom } from '../_shared/reel.js';
import { px } from '../_shared/timeline.js';

const visible = (ctx, name) =>
  ctx.skipParts.includes(name)
    ? []
    : ctx.beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));
const byDistance = (ctx, name) =>
  visible(ctx, name)
    .map((node, index) => ({
      node,
      index,
      distance: Math.abs(
        ctx.beat.anchor(name, index).rect.x -
          (ctx.beat.part('now')[0] ? ctx.beat.anchor('now').rect.x : ctx.viewport.w / 2),
      ),
    }))
    .sort((a, b) => a.distance - b.distance);
export default {
  id: 'rail-draw',
  family: 'rail',
  role: 'enter',
  accepts: ['chronology'],
  sources: ['line-draw', 'stagger', 'tracking-reveal'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.8, max: 2.4, doc: 'Overall duration.' },
    stagger: { type: 'number', default: 0.06, min: 0, max: 0.15, doc: 'Delay between rail items.' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = ctx.duration,
      track = visible(ctx, 'track'),
      now = ctx.beat.part('now')[0],
      origin = now ? `${ctx.beat.anchor('now').rect.x - ctx.beat.anchor('track').rect.x}px center` : 'center';
    railFocus(ctx, ctx.beat, 0);
    ctx.initial(track, { scaleX: 0, transformOrigin: origin });
    tl.to(track, { scaleX: 1, duration: d * 0.45, ease: ctx.ease('out') }, 0);
    [...byDistance(ctx, 'tick'), ...byDistance(ctx, 'dot')].forEach(({ node }, i) => {
      ctx.initial(node, { autoAlpha: 0, scale: 0 });
      tl.to(
        node,
        { autoAlpha: 1, scale: 1, duration: d * 0.18, ease: ctx.ease('out') },
        d * 0.15 + Math.min(d * 0.27, i * params.stagger),
      );
    });
    const stem = visible(ctx, 'stem').slice(0, 1),
      title = visible(ctx, 'title').slice(0, 1),
      note = visible(ctx, 'note').slice(0, 1);
    ctx.initial(stem, { scaleY: 0, transformOrigin: 'bottom' });
    ctx.initial(title, { y: px(ctx, 18), autoAlpha: 0 });
    ctx.initial(note, { autoAlpha: 0 });
    tl.to(stem, { scaleY: 1, duration: d * 0.25, ease: ctx.ease('arrive') }, d * 0.45);
    tl.to(title, { y: 0, autoAlpha: 1, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.57);
    tl.to(note, { autoAlpha: 1, duration: d * 0.16, ease: ctx.ease('out') }, d * 0.69);
    const label = visible(ctx, 'label'),
      counter = visible(ctx, 'counter');
    ctx.initial(label, { autoAlpha: 0, letterSpacing: '0.12em' });
    ctx.initial(counter, { autoAlpha: 0 });
    tl.to(label, { autoAlpha: 1, letterSpacing: '0em', duration: d * 0.45, ease: ctx.ease('out') }, d * 0.55);
    tl.to(counter, { autoAlpha: 1, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.7);
    const reel = counter[0] && reelFrom(counter[0]);
    reel?.cols.forEach((col) => {
      ctx.initial(col, { y: 0, yPercent: -Number(col.dataset.digit ?? 0) * 10 });
      tl.set(col, { yPercent: -Number(col.dataset.digit ?? 0) * 10 }, 0);
    });
  },
};
