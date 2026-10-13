/** Strike one word, scramble it deterministically, and settle on its replacement. */
import { colorOf } from '../_shared/color.js';
import { driveValue } from '../_shared/drive.js';
import { scrambleAt, scrambleTable } from '../_shared/scramble.js';
import { line, svgLayer } from '../_shared/stroke.js';

export default {
  id: 'scramble-swap',
  family: 'type',
  role: 'step',
  accepts: ['text'],
  sources: ['text-scramble', 'strikethrough-replace', 'word-slot-cycle'],
  reduce: 'self',
  params: {
    word: { type: 'integer', default: 0, doc: '대상 어절 index' },
    from: { type: 'string', default: '이전', doc: '처음 보여 줄 단어' },
    duration: { type: 'number', default: 1.6, min: 0.8, max: 3, doc: '전체 길이(u)' },
    glyphs: { type: 'string', default: '#%&@*+=/<>', doc: '들끓는 기호 집합' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const node = ctx.beat.part('word')[p.word];
    if (!node || ctx.skipParts.includes('word') || (ctx.skipNodes ?? []).includes(node)) return;
    const d = p.duration,
      to = node.textContent ?? '',
      rect = ctx.beat.anchor('word', p.word).rect;
    const table = scrambleTable(
      ctx.rng,
      Math.max(p.from.length, to.length),
      Math.max(2, Math.ceil((d * 0.5) / 0.05)),
      p.glyphs,
    );
    // The wrong word is shorter or longer than the right one: close the line up around it so the
    // first stop reads naturally, then let the line breathe back to its authored layout during the swap.
    const original = node.textContent;
    node.dataset.slText = to;
    node.textContent = p.from;
    const fromW = node.getBoundingClientRect?.().width || rect.w;
    node.textContent = original;
    const delta = rect.w - fromW;
    const words = ctx.beat.part('word'),
      sameLine = (i) => Math.abs(ctx.beat.anchor('word', i).rect.y - rect.y) < rect.h * 0.5;
    const block = ctx.beat.part('block')[0];
    const centred = block && globalThis.getComputedStyle?.(block).textAlign === 'center';
    const shiftOf = (i) =>
      i < p.word || i === p.word ? (centred ? delta / 2 : 0) : centred ? -delta / 2 : -delta;
    const moved = words.map((w, i) => ({ w, i })).filter(({ w, i }) => w && sameLine(i) && shiftOf(i));
    const x0 = rect.x + shiftOf(p.word);
    const svg = svgLayer(ctx),
      stroke = line(svg, x0, rect.y + rect.h * 0.55, x0 + fromW, rect.y + rect.h * 0.55, {
        stroke: colorOf(ctx, 'accent'),
        'stroke-width': Math.max(3, rect.h * 0.05),
      });
    const proxy = { p: 0 };
    const paint = () => {
      node.textContent = ctx.reduce ? (proxy.p < 0.5 ? p.from : to) : scrambleAt(p.from, to, proxy.p, table);
    };
    ctx.initial(node, {
      autoAlpha: 1,
      color: colorOf(ctx, 'fg'),
      display: 'inline-block',
      whiteSpace: 'nowrap',
      // box + margin always = the right word's width, so the line never reflows while the text changes
      width: fromW,
      marginRight: rect.w - fromW,
    });
    moved.forEach(({ w, i }) => ctx.initial(w, { x: shiftOf(i) }));
    ctx.initial(stroke, { scaleX: 0, transformOrigin: 'left center' });
    paint();
    if (moved.length)
      tl.to(
        moved.map(({ w }) => w),
        { x: 0, duration: d * 0.5, ease: ctx.ease('inout') },
        d * 0.35,
      );
    tl.to(node, { width: rect.w, marginRight: 0, duration: d * 0.5, ease: ctx.ease('inout') }, d * 0.35);
    tl.to(stroke, { scaleX: 1, duration: d * 0.25, ease: ctx.ease('inout') }, 0);
    tl.to(node, { autoAlpha: 0.45, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.25);
    // driveValue, not onUpdate: seek()/pause(t) suppress callbacks (C5 v2.2)
    driveValue(tl, (v) => ((proxy.p = v), paint()), {
      from: 0,
      to: 1,
      at: d * 0.35,
      duration: d * 0.5,
      ease: 'none',
    });
    tl.to(stroke, { autoAlpha: 0, duration: d * 0.5, ease: ctx.ease('out') }, d * 0.35);
    tl.to(
      node,
      { autoAlpha: 1, color: colorOf(ctx, 'accent'), duration: d * 0.15, ease: ctx.ease('out') },
      d * 0.85,
    );
  },
};
