/** Drops comparison or chronology entries into their final layout positions. */
import { colorOf } from '../_shared/color.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name)
    ? []
    : ctx.beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));

export default {
  id: 'pin-drop',
  family: 'assemble',
  role: 'enter',
  accepts: ['compare', 'chronology'],
  sources: ['map-event-accumulation', 'fade-slide'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.5, min: 0.6, max: 2.4, doc: '전체 길이(u)' },
    drop: { type: 'number', default: 28, min: 0, max: 80, doc: '낙하 거리(px)' },
    stagger: { type: 'number', default: 0.18, min: 0.05, max: 0.4, doc: '항목 간 시차(u)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const itemPart = ctx.beat.type === 'chronology' ? 'event' : 'item';
    const labelPart = ctx.beat.type === 'chronology' ? 'title' : 'label';
    const items = usable(ctx, itemPart);
    const labels = usable(ctx, labelPart);
    const stagger =
      items.length > 1 ? Math.min(params.stagger, (d * 0.75 - d * 0.32) / (items.length - 1)) : 0;
    const landing = d * 0.32;
    items.forEach((node, index) => {
      const at = index * stagger;
      ctx.initial(node, { autoAlpha: 0, y: -px(ctx, params.drop), scale: 1.04 });
      tl.to(node, { autoAlpha: 1, y: 0, scale: 1, duration: landing, ease: ctx.ease('out') }, at);
      const label = labels[index];
      if (label) {
        ctx.initial(label, { color: colorOf(ctx, 'fg') });
        tl.to(label, { color: colorOf(ctx, 'accent'), duration: 0.05, ease: ctx.ease('out') }, at + landing);
        tl.to(
          label,
          { color: colorOf(ctx, 'fg'), duration: 0.05, ease: ctx.ease('out') },
          at + landing + 0.05,
        );
      }
    });
    const verdict = usable(ctx, 'verdict');
    ctx.initial(verdict, { autoAlpha: 0 });
    tl.to(verdict, { autoAlpha: 1, duration: d * 0.25, ease: ctx.ease('out') }, d * 0.75);
  },
};
