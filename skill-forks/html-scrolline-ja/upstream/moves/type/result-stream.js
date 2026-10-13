/** Stream the prompt's answer word by word in place; the prompt recedes, a caret rides the last word. */
import { colorOf } from '../_shared/color.js';
import { slots } from '../_shared/timeline.js';

export default {
  id: 'result-stream',
  family: 'type',
  role: 'step',
  accepts: ['prompt'],
  sources: ['word-pop-caption', 'karaoke-caption', 'typewriter'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 2.2, min: 1, max: 4, doc: '전체 길이(u)' },
    compress: { type: 'number', default: 0.85, min: 0.5, max: 1, doc: '어절 간격 감소 배율' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const result = ctx.skipParts.includes('result') ? [] : ctx.beat.part('result');
    if (!result.length) return;
    const words = ctx.skipParts.includes('word') ? [] : ctx.beat.part('word');
    const d = p.duration,
      fg = colorOf(ctx, 'fg'),
      accent = colorOf(ctx, 'accent');
    const prompt = ['char', 'label'].flatMap((name) =>
      ctx.skipParts.includes(name) ? [] : ctx.beat.part(name),
    );
    // The question steps back so the answer is the only thing moving.
    tl.to(prompt, { color: colorOf(ctx, 'fg-muted'), duration: d * 0.12, ease: ctx.ease('out') }, 0);
    tl.to(ctx.beat.part('caret'), { autoAlpha: 0, duration: d * 0.06 }, 0);
    if (!words.length) {
      tl.fromTo(
        result,
        { autoAlpha: 0 },
        { autoAlpha: 1, duration: d * 0.9, ease: ctx.ease('out'), immediateRender: false },
        0,
      );
      return;
    }
    const rects = words.map((_, i) => ctx.beat.anchor('word', i).rect);
    const caret = document.createElement('i');
    caret.className = 'sl-result-stream__caret';
    Object.assign(caret.style, {
      position: 'absolute',
      left: '0px',
      top: '0px',
      width: `${Math.max(2, rects[0].h * 0.05)}px`,
      height: `${rects[0].h * 0.8}px`,
      background: accent,
    });
    ctx.overlay.append(caret);
    const caretAt = (r) => ({ x: r.x + r.w + r.h * 0.1, y: r.y + r.h * 0.12 });
    // type-on keeps the result hidden until this step; the step only reveals the box, words come one by one
    // (words are hidden by a set, not an initial: a following link may own their resting state)
    tl.set(result, { autoAlpha: 1 }, 0);
    tl.set(words, { autoAlpha: 0, y: rects[0].h * 0.12, color: fg }, 0);
    ctx.initial(caret, { autoAlpha: 0, x: rects[0].x, y: rects[0].y + rects[0].h * 0.12 });
    tl.set(caret, { autoAlpha: 1 }, d * 0.04);
    const times = slots(words.length, {
      start: d * 0.06,
      span: d * 0.74,
      compress: p.compress,
      minRatio: 0.4,
    });
    const pop = Math.min(0.12, d * 0.06);
    words.forEach((node, i) => {
      const at = times[i].at;
      tl.to(node, { autoAlpha: 1, y: 0, color: accent, duration: pop, ease: ctx.ease('out') }, at);
      if (i) tl.to(words[i - 1], { color: fg, duration: pop, ease: ctx.ease('out') }, at);
      tl.set(caret, caretAt(rects[i]), at);
    });
    // Only the last word keeps the accent; the caret blinks off before the fold.
    tl.to(caret, { autoAlpha: 0, duration: d * 0.04 }, d * 0.9);
  },
};
