/**
 * Collapses a full-bleed frame into the receiving prompt caret: the footage narrows to a vertical
 * slit, the slit turns into an accent bar, and the bar shrinks onto the spot where typing starts.
 */
import { transferVars } from '../../engine/index.js';
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';

export default {
  id: 'caret-collapse',
  family: 'morph',
  role: 'link',
  accepts: ['prompt'],
  sources: ['origami-fold', 'split-slide', 'morph-match-cut', 'context-caret'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.8, max: 2.5, doc: '전체 길이(u)' },
    toPart: { type: 'part', default: 'caret', doc: 'B 도착 part' },
  },
  handoff(p) {
    return { from: { part: 'frame' }, to: { part: p.toPart } };
  },
  timing: (p) => ({ duration: p.duration ?? 1.4, stops: [] }),
  build(tl, ctx, p) {
    const { from, to } = ctx.handoff,
      d = p.duration,
      field = ctx.beat.part('field'),
      label = ctx.beat.part('label');
    // Where the caret waits before the first character is typed (falls back to the caret itself).
    const first = ctx.beat.part('char').length ? ctx.beat.anchor('char', 0).rect : null;
    const caretH = (first ?? to.rect).h * 0.86;
    const land = first
      ? { x: first.x, y: first.y + first.h * 0.07, w: Math.max(2, to.rect.w), h: caretH }
      : to.rect;
    const slit = Math.max(4, from.rect.w * 0.004);
    const bar = document.createElement('i');
    bar.className = 'sl-caret-collapse__bar';
    ctx.overlay.append(bar);
    Object.assign(bar.style, {
      position: 'absolute',
      left: '0px',
      top: '0px',
      width: '1px',
      height: '1px',
      backgroundColor: colorOf(ctx, 'accent'),
      transformOrigin: '0 0',
    });
    const barAt = (r) => ({ x: r.x, y: r.y, scaleX: r.w, scaleY: r.h });
    const slitRect = {
      x: from.rect.x + from.rect.w / 2 - slit / 2,
      y: from.rect.y,
      w: slit,
      h: from.rect.h,
    };
    ctx.initial(from.node, {
      clipPath: 'inset(0px 0px 0px 0px)',
      transformOrigin: '0 0',
      filter: 'brightness(1)',
      autoAlpha: 1,
    });
    ctx.initial(bar, { autoAlpha: 0, ...barAt(slitRect) });
    if (field.length) ctx.initial(field, { scaleX: 0, transformOrigin: '0 50%' });
    if (label.length) ctx.initial(label, { autoAlpha: 0 });
    const side = (from.rect.w - slit) / 2;
    tl.to(
      from.node,
      {
        clipPath: `inset(0px ${side}px 0px ${side}px)`,
        filter: 'brightness(0.7)',
        duration: d * 0.42,
        ease: ctx.ease('inout'),
      },
      0,
    );
    tl.to(bar, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.36);
    tl.set(from.node, { autoAlpha: 0 }, d * 0.46);
    tl.to(bar, { ...barAt(land), duration: d * 0.38, ease: ctx.ease('inout') }, d * 0.48);
    // The footage node itself is carried onto the caret (invisible by now) so the handoff closes.
    const { transformOrigin, ...carry } = transferVars(from.rect, to.rect);
    tl.set(from.node, { ...carry, clipPath: 'inset(0px 0px 0px 0px)' }, d * 0.47);
    if (field.length) tl.to(field, { scaleX: 1, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.6);
    if (label.length) tl.to(label, { autoAlpha: 1, duration: d * 0.14, ease: ctx.ease('out') }, d * 0.84);
    tl.set(bar, { autoAlpha: 0 }, d);
    finishLink(tl, ctx, { at: d, cross: Math.min(0.08, d * 0.06), from: [from.node] });
  },
};
