/** Replace outgoing text with seeded glyphs before the authored text fades away. */
import { driveValue } from '../_shared/drive.js';
import { scrambleAt, scrambleTable } from '../_shared/scramble.js';

export default {
  id: 'scramble-out',
  family: 'type',
  role: 'exit',
  accepts: ['text'],
  sources: ['text-scramble', 'text-particle-dissolve'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.9, min: 0.4, max: 1.6, doc: '전체 길이(u)' },
    glyphs: { type: 'string', default: '#%&@*+=/<>', doc: '기호 집합' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const block = ctx.beat.part('block')[0];
    if (!block || ctx.skipParts.includes('block') || (ctx.skipNodes ?? []).includes(block)) return;
    const d = p.duration,
      words = ctx.skipParts.includes('word') ? [] : ctx.beat.part('word');
    const nodes = words.length ? words : [block];
    const originals = nodes.map((node) => node.dataset?.slText ?? node.textContent ?? '');
    const tables = originals.map((text) =>
      scrambleTable(ctx.rng, text.length, Math.max(2, Math.ceil((d * 0.75) / 0.05)), p.glyphs),
    );
    const proxy = { p: 0 };
    const paint = () =>
      nodes.forEach((node, index) => {
        node.textContent = scrambleAt(originals[index], '', proxy.p, tables[index]);
      });
    ctx.initial(block, { autoAlpha: 1 });
    // no paint at build: an earlier step (scramble-swap) may own the text before this exit starts
    tl.to(block, { autoAlpha: 0, duration: d * 0.4, ease: ctx.ease('in') }, d * 0.6);
    // driveValue, not onUpdate/call: seek()/pause(t) suppress callbacks (C5 v2.2).
    // v runs over the whole exit: glyphs boil for the first 75%, the hidden text is restored at the end.
    const restore = () =>
      nodes.forEach((node, index) => {
        node.textContent = originals[index];
      });
    driveValue(
      tl,
      (v) => {
        if (v >= 1) return restore();
        proxy.p = ctx.reduce ? 0 : Math.min(0.999, v / 0.75);
        paint();
      },
      { from: 0, to: 1, at: 0, duration: d, ease: 'none' },
    );
  },
};
