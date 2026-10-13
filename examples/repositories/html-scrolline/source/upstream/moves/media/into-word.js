/**
 * Carries a video frame into a word of the following text beat: the full frame clips down to the
 * word's box, the footage then shows only through the word's glyphs, and the word fills in with
 * the accent ink while the rest of the sentence arrives. Works for canvas frame sequences too
 * (the real frame is clipped in place, nothing is cloned).
 */
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { applyTextMask } from '../_shared/mask.js';
import { glyphMask } from '../_shared/glyph-mask.js';

export default {
  id: 'into-word',
  family: 'media',
  role: 'link',
  accepts: ['text'],
  sources: ['inline-image-expand', 'text-window-fill', 'clip-reveal'],
  reduce: 'fade',
  params: {
    word: { type: 'integer', default: 0, doc: 'B 쪽 도착 어절 index' },
    duration: { type: 'number', default: 1.6, min: 0.8, max: 3, doc: '전체 길이(u)' },
  },
  handoff(params) {
    return { from: { part: 'frame' }, to: { part: 'word', index: params.word } };
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const { from, to } = ctx.handoff,
      d = params.duration;
    const words = ctx.beat.part('word');
    const rest = words.filter((node) => node !== to.node && !ctx.skipNodes?.includes(node));
    const others = ['caption', 'credit', 'source'].flatMap((name) => ctx.from.part(name));
    const r = to.rect,
      f = from.rect;
    const inset = `inset(${r.y - f.y}px ${f.x + f.w - r.x - r.w}px ${f.y + f.h - r.y - r.h}px ${r.x - f.x}px)`;
    // fill = accent block behind the glyph window, so the word "fills with ink" as the footage fades
    const fill = document.createElement('div');
    fill.className = 'sl-into-word__fill';
    ctx.overlay.append(fill);
    Object.assign(fill.style, {
      position: 'absolute',
      left: `${r.x}px`,
      top: `${r.y}px`,
      width: `${r.w}px`,
      height: `${r.h}px`,
    });
    const glyph = glyphMask(ctx, to.node.textContent || 'WORD', r, { scale: 0.8 });
    if (glyph) {
      const url = `url("${glyph.url}")`;
      Object.assign(fill.style, {
        maskImage: url,
        webkitMaskImage: url,
        maskSize: '100% 100%',
        webkitMaskSize: '100% 100%',
      });
    } else applyTextMask(ctx, fill, to.node.textContent || 'WORD', { rect: r });
    ctx.initial(from.node, { autoAlpha: 1, clipPath: 'inset(0px 0px 0px 0px)', filter: 'brightness(1)' });
    ctx.initial(fill, { autoAlpha: 0, backgroundColor: colorOf(ctx, 'accent') });
    ctx.initial(to.node, { color: colorOf(ctx, 'accent') });
    if (others.length) ctx.initial(others, { autoAlpha: 1 });
    if (rest.length) ctx.initial(rest, { autoAlpha: 0, x: 12 });
    if (others.length) tl.to(others, { autoAlpha: 0, duration: d * 0.15, ease: ctx.ease('in') }, 0);
    tl.to(
      from.node,
      { clipPath: inset, filter: 'brightness(1.15)', duration: d * 0.45, ease: ctx.ease('inout') },
      0,
    );
    if (glyph) {
      const url = `url("${glyph.url}")`,
        size = `${r.w}px ${r.h}px`,
        pos = `${r.x - f.x}px ${r.y - f.y}px`;
      tl.set(
        from.node,
        {
          maskImage: url,
          webkitMaskImage: url,
          maskSize: size,
          webkitMaskSize: size,
          maskPosition: pos,
          webkitMaskPosition: pos,
          maskRepeat: 'no-repeat',
          webkitMaskRepeat: 'no-repeat',
        },
        d * 0.47,
      );
    }
    tl.to(fill, { autoAlpha: 1, duration: d * 0.23, ease: ctx.ease('out') }, d * 0.55);
    tl.to(from.node, { autoAlpha: 0, duration: d * 0.2, ease: ctx.ease('in') }, d * 0.6);
    tl.to(fill, { autoAlpha: 0, duration: d * 0.16, ease: ctx.ease('out') }, d * 0.84);
    if (rest.length) tl.to(rest, { autoAlpha: 1, x: 0, duration: d * 0.25, ease: ctx.ease('out') }, d * 0.55);
    finishLink(tl, ctx, { at: d, cross: 0.12, from: [from.node], to: [to.node] });
  },
};
