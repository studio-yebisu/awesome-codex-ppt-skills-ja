/** Compress a close rail view into an all-history chronology. Used by the final rail link. */
import { transferVars } from '../../engine/index.js';
import { finishLink } from '../_shared/link.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name)
    ? []
    : ctx.beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));
export default {
  id: 'rail-compress',
  family: 'rail',
  role: 'link',
  accepts: ['chronology'],
  sources: ['axis-rescale', 'scale-swap', 'zoom-to-detail', 'time-compression'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 2.4, min: 1.2, max: 4, doc: 'Overall duration.' },
    startZoom: { type: 'number', default: 8, min: 2, max: 16, doc: 'Initial horizontal zoom.' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  handoff(params, { to }) {
    return { to: { part: 'dot', index: Math.max(0, (to.events?.length ?? 1) - 1) } };
  },
  build(tl, ctx, params) {
    const d = ctx.duration,
      track = usable(ctx, 'track'),
      label = usable(ctx, 'label'),
      dots = usable(ctx, 'dot'),
      stems = usable(ctx, 'stem'),
      titles = usable(ctx, 'title');
    ctx.initial(track, {
      scaleX: ctx.reduce ? 1 : params.startZoom,
      transformOrigin: '100% center',
      autoAlpha: 1,
    });
    ctx.initial(label, { autoAlpha: 0 });
    const minor =
      ctx.beat.data.events
        ?.map((event, index) => (event.weight === 'minor' ? index : -1))
        .filter((index) => index >= 0) ?? [];
    minor.forEach((index) => ctx.initial(titles[index], { autoAlpha: 0 }));
    ctx.initial(ctx.handoff.to.node, { autoAlpha: 0 });
    tl.to(
      ctx.handoff.from.node,
      {
        ...transferVars(ctx.handoff.from.rect, ctx.handoff.to.rect),
        duration: d * 0.3,
        ease: ctx.ease('inout'),
      },
      0,
    );
    tl.to(
      Object.values(ctx.from.parts)
        .flat()
        .filter((node) => node !== ctx.handoff.from.node),
      { autoAlpha: 0, duration: d * 0.24, ease: ctx.ease('in') },
      d * 0.06,
    );
    if (!ctx.reduce) {
      tl.to(track, { scaleX: 1, duration: d * 0.65, ease: ctx.ease('inout') }, d * 0.2);
      [...dots, ...stems].forEach((node) => {
        ctx.initial(node, { scaleX: 1 / params.startZoom });
        tl.to(node, { scaleX: 1, duration: d * 0.65, ease: ctx.ease('inout') }, d * 0.2);
      });
    }
    // 압축되는 동안 사건 점이 레일 위에 촘촘히 보인다(오른쪽 끝 = 지금). 제목·날짜는 배율이 거의 풀린 뒤에.
    const events = usable(ctx, 'event'),
      labels = [...titles.filter((_, index) => !minor.includes(index)), ...usable(ctx, 'date')];
    ctx.initial(events, { autoAlpha: 0 });
    ctx.initial(labels, { autoAlpha: 0 });
    tl.to(events, { autoAlpha: 1, y: 0, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.18);
    tl.to(labels, { autoAlpha: 1, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.78);
    const counter = usable(ctx, 'counter');
    if (counter.length) tl.set(counter, { autoAlpha: 1 }, d * 0.3);
    ctx.initial(label, { y: px(ctx, 16), autoAlpha: 0 });
    tl.to(label, { y: 0, autoAlpha: 1, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.8);
    finishLink(tl, ctx, { at: d, cross: 0.12 });
  },
};
