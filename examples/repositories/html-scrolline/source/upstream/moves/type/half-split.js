/** Send exact clipped top and bottom copies of a title in opposite directions. */
export default {
  id: 'half-split',
  family: 'type',
  role: 'exit',
  accepts: ['text', 'number'],
  sources: ['text-half-split', 'split-slide'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.9, min: 0.4, max: 1.6, doc: '전체 길이(u)' },
    distance: { type: 'number', default: 1, min: 0.4, max: 1.5, doc: '이동 거리 배율' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const node = ctx.beat.part('block')[0] ?? ctx.beat.part('value')[0];
    if (!node || ctx.skipParts.includes('block') || (ctx.skipNodes ?? []).includes(node)) return;
    if (ctx.reduce) {
      ctx.initial(node, { autoAlpha: 1 });
      tl.to(node, { autoAlpha: 0, duration: p.duration, ease: ctx.ease('in') }, 0);
      return;
    }
    const rect = ctx.beat.anchor().rect,
      make = (name, clip) => {
        const copy = node.cloneNode(true);
        copy.removeAttribute('data-part');
        copy.classList.add(`sl-half-split__${name}`);
        Object.assign(copy.style, {
          position: 'absolute',
          left: `${rect.x}px`,
          top: `${rect.y}px`,
          width: `${rect.w}px`,
          height: `${rect.h}px`,
          margin: '0',
          clipPath: clip,
        });
        ctx.overlay.append(copy);
        return copy;
      };
    const top = make('top', 'inset(0 0 50% 0)'),
      bottom = make('bottom', 'inset(50% 0 0 0)'),
      d = p.duration;
    ctx.initial(node, { autoAlpha: 1 });
    ctx.initial([top, bottom], { autoAlpha: 1 });
    tl.to(top, { yPercent: -100 * p.distance, autoAlpha: 0, duration: d * 0.8, ease: ctx.ease('inout') }, 0);
    tl.to(
      bottom,
      { yPercent: 100 * p.distance, autoAlpha: 0, duration: d * 0.8, ease: ctx.ease('inout') },
      0,
    );
    tl.to(node, { autoAlpha: 0, duration: d * 0.01, ease: ctx.ease('in') }, 0);
  },
};
