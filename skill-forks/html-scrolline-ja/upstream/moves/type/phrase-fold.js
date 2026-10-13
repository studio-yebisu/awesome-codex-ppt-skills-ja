/** Fold unneeded words away, then carry each retained word onto its twin in the next text beat. */
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { clamp } from '../_shared/timeline.js';
import { ghostWords } from '../_shared/words.js';
import { transferVars } from '../../engine/index.js';

// transferVars without transformOrigin (set once in initial so rewinds restore it exactly)
const carry = (a, b) => {
  const { transformOrigin, ...vars } = transferVars(a, b);
  return vars;
};

export default {
  id: 'phrase-fold',
  family: 'type',
  role: 'link',
  accepts: ['text'],
  sources: ['letter-anagram-shift', 'origami-fold', 'phrase-push-build', 'text-half-split'],
  reduce: 'fade',
  params: {
    fromPart: { type: 'part', default: 'word', doc: 'A의 어절 part' },
    toPart: {
      type: 'part',
      default: 'word',
      doc: 'B의 도착 part(word면 남긴 어절이 B의 같은 순번 어절 자리로)',
    },
    keepFrom: { type: 'integer', default: 0, doc: '남길 첫 어절 index' },
    keepTo: { type: 'integer', default: -1, doc: '남길 끝 어절 index(−1 = 끝)' },
    fold: {
      type: 'enum',
      default: 'right',
      values: ['right', 'both'],
      doc: 'right(뒤부터 접힘, 되감기) | both(양옆에서 가운데로)',
    },
    caret: { type: 'boolean', default: false, doc: '접히는 끝을 따라 커서가 되감김' },
    appendIn: { type: 'boolean', default: false, doc: 'B의 나머지 어절이 따라 붙음' },
    duration: { type: 'number', default: 1.6, min: 0.8, max: 3, doc: '전체 길이(u)' },
  },
  handoff(p) {
    return { from: { part: p.fromPart, index: p.keepFrom }, to: { part: p.toPart } };
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const d = p.duration,
      fromWords = p.fromPart === 'word' ? ctx.from.part('word') : [];
    const words = fromWords.length
      ? fromWords
      : ghostWords(ctx, ctx.handoff.from.node, ctx.handoff.from.rect);
    const rectOf = (node, i) => (fromWords.length ? ctx.from.anchor('word', i).rect : ctx.handoff.from.rect);
    const rects = words.map(rectOf);
    const end = p.keepTo < 0 ? words.length - 1 : clamp(p.keepTo, 0, words.length - 1);
    const begin = clamp(p.keepFrom, 0, Math.max(0, end));
    const kept = words.slice(begin, end + 1);
    const center = (begin + end) / 2;
    const discarded = words
      .map((node, i) => ({ node, i }))
      .filter(({ i }) => i < begin || i > end)
      .sort((a, b) => (p.fold === 'both' ? Math.abs(b.i - center) - Math.abs(a.i - center) : b.i - a.i));
    const targets = ctx.beat.part('word');
    const block = ctx.beat.part(p.toPart === 'word' ? 'block' : p.toPart);
    const to = block.length ? block : [ctx.handoff.to.node];
    words.forEach((node, i) =>
      ctx.initial(node, {
        autoAlpha: 1,
        scaleX: 1,
        x: 0,
        y: 0,
        scaleY: 1,
        transformOrigin: i < begin ? '100% 50%' : i > end ? '0% 50%' : '0 0',
      }),
    );
    // A's other furniture (prompt label, field, caret) steps out first
    const furniture = ['label', 'field', 'caret'].flatMap((name) => ctx.from.part(name));
    if (furniture.length) {
      ctx.initial(furniture, { autoAlpha: 1 });
      tl.to(furniture, { autoAlpha: 0, duration: d * 0.2, ease: ctx.ease('in') }, 0);
    }
    // 1) fold: discarded words collapse toward the kept phrase, one after another
    const foldEnd = d * 0.42,
      each = discarded.length ? Math.min(d * 0.12, foldEnd / discarded.length) : 0;
    discarded.forEach(({ node }, k) =>
      tl.to(
        node,
        {
          scaleX: 0,
          autoAlpha: 0,
          duration: each * 1.4,
          ease: ctx.ease('in'),
        },
        Math.min(foldEnd - each, k * each),
      ),
    );
    // 2) carry: each kept word flies onto its twin in B (same order), or the whole phrase onto B's part
    const landing = (k) => {
      if (p.toPart === 'word' && targets[k]) return ctx.beat.anchor('word', k).rect;
      const target = ctx.handoff.to.rect,
        first = rects[begin],
        last = rects[end],
        w = Math.max(1, last.x + last.w - first.x),
        s = target.w / w,
        r = rects[begin + k];
      return { x: target.x + (r.x - first.x) * s, y: target.y + (r.y - first.y) * s, w: r.w * s, h: r.h * s };
    };
    kept.forEach((node, k) =>
      tl.to(
        node,
        { ...carry(rects[begin + k], landing(k)), duration: d * 0.42, ease: ctx.ease('inout') },
        d * 0.46 + k * Math.min(0.03, d * 0.02),
      ),
    );
    if (p.caret) {
      const caret = document.createElement('i');
      caret.className = 'sl-phrase-fold__caret';
      const h0 = rects[end].h;
      Object.assign(caret.style, {
        position: 'absolute',
        left: '0px',
        top: '0px',
        width: `${Math.max(2, h0 * 0.05)}px`,
        height: `${h0 * 0.8}px`,
        background: colorOf(ctx, 'accent'),
        transformOrigin: '0 0',
      });
      ctx.overlay.append(caret);
      const after = (r) => ({ x: r.x + r.w + r.h * 0.1, y: r.y + r.h * 0.12 });
      const lastShown = words.length - 1;
      ctx.initial(caret, { autoAlpha: 0, ...after(rects[lastShown]), scaleY: 1 });
      tl.set(caret, { autoAlpha: 1 }, 0);
      if (p.fold === 'right')
        discarded.forEach(({ i }, k) => {
          const prev = rects[Math.max(0, i - 1)];
          tl.set(caret, after(prev), Math.min(foldEnd - each, k * each) + each);
        });
      else tl.set(caret, after(rects[end]), foldEnd);
      const land = landing(kept.length - 1);
      tl.to(
        caret,
        { ...after(land), scaleY: land.h / h0, duration: d * 0.42, ease: ctx.ease('inout') },
        d * 0.46,
      );
      tl.set(caret, { autoAlpha: 0 }, d);
    }
    // B: block shown, its words hidden; twins swap in at the end, the rest append (or appear with them)
    const twins = targets.slice(0, kept.length),
      rest = targets.slice(kept.length);
    if (targets.length) ctx.initial(block, { autoAlpha: 1 });
    if (p.appendIn)
      rest.forEach((node, k) => {
        ctx.initial(node, { x: '0.5em', autoAlpha: 0 });
        tl.to(node, { x: 0, autoAlpha: 1, duration: d * 0.16, ease: ctx.ease('out') }, d * 0.78 + k * 0.04);
      });
    // land a hair before the end so the stop at the link's end never shows both copies
    finishLink(tl, ctx, {
      at: d - Math.min(0.02, d * 0.01),
      cross: Math.min(0.06, d * 0.04),
      from: [...new Set([...words, ctx.handoff.from.node])],
      to: targets.length ? [...new Set([...twins, ...(p.appendIn ? [] : rest), ctx.handoff.to.node])] : to,
    });
  },
};
