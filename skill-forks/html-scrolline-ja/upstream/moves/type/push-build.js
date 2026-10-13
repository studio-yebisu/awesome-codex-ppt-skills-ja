/** Words enter from the right while their completed phrase remains centered. */
import { colorOf } from '../_shared/color.js';
import { px } from '../_shared/timeline.js';
export default {
  id: 'push-build',
  family: 'type',
  role: 'enter',
  accepts: ['text'],
  sources: ['phrase-push-build', 'word-relay'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.8, max: 3.2, doc: '전체 길이(u)' },
    accentWords: { type: 'array', default: [], doc: 'accent로 칠할 어절 index 목록' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const words = ctx.skipParts.includes('word') ? [] : ctx.beat.part('word');
    const d = p.duration,
      count = words.length,
      block = ctx.beat.anchor('block').rect;
    const rects = words.map((_, i) => ctx.beat.anchor('word', i).rect);
    // Lines are centred on their own, so the half-built phrase is re-centred within its line only.
    const lineOf = rects.map((r) => Math.round(r.y));
    const center = block.x + block.w / 2;
    const groupShift = (last) => {
      const used = rects.filter((_, i) => i <= last && lineOf[i] === lineOf[last]);
      const lo = Math.min(...used.map((r) => r.x)),
        hi = Math.max(...used.map((r) => r.x + r.w));
      return used.length ? center - (lo + hi) / 2 : 0;
    };
    const sameLine = (i) => words.filter((_, j) => j < i && lineOf[j] === lineOf[i]);
    const incoming = Math.min(d * 0.18, 0.18),
      interval = count > 1 ? (d * 0.85 - incoming) / (count - 1) : 0;
    words.forEach((node, i) => {
      const at = i * interval,
        centeredX = groupShift(i);
      ctx.initial(node, { x: centeredX + px(ctx, 80), autoAlpha: 0 });
      tl.to(node, { x: centeredX, autoAlpha: 1, duration: incoming, ease: ctx.ease('out') }, at);
      // All already placed words receive the same group translation at this beat.
      if (sameLine(i).length)
        tl.to(sameLine(i), { x: centeredX, duration: incoming, ease: ctx.ease('inout') }, at);
      if (p.accentWords.includes(i)) {
        ctx.initial(node, { color: colorOf(ctx, 'fg') });
        tl.to(
          node,
          { color: colorOf(ctx, 'accent'), duration: Math.min(0.12, incoming), ease: ctx.ease('out') },
          at + incoming,
        );
      }
    });
    // The final authored phrase is centered, so every temporary correction settles to zero.
    if (count) tl.to(words, { x: 0, duration: Math.min(d * 0.15, 0.2), ease: ctx.ease('inout') }, d * 0.85);
  },
};
