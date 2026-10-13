/**
 * Next-token pick: under the empty slot, candidate words rise with probability bars (stop `cands`),
 * the top one turns accent, the rest drop away, and the pick flies up into the slot and lands.
 * Probabilities are illustrative; the note stays on screen with them.
 */
import { colorOf } from '../_shared/color.js';

export default {
  id: 'slot-pick',
  family: 'type',
  role: 'enter',
  accepts: ['text'],
  sources: ['next-token', 'word-slot-cycle', 'phrase-push-build', 'word-rise-fade'],
  reduce: 'self',
  params: {
    word: { type: 'integer', default: 0, doc: '채울 어절 index' },
    candidates: { type: 'array', default: [], doc: '[{word, p, other?}] 후보 목록(첫 항목 = 고르는 단어)' },
    note: { type: 'string', default: '확률은 설명용 예시', doc: 'L3 확률 안내 문구' },
    duration: { type: 'number', default: 2.8, min: 1.2, max: 4.5, doc: '전체 길이(u)' },
    candsAt: { type: 'number', default: 0.42, min: 0.3, max: 0.6, doc: '후보 정지점 비율' },
    speed: { type: 'number', default: 1, min: 0.4, max: 1.5, doc: '빠르기 배율(길이 = duration / speed)' },
  },
  timing(p) {
    const duration = p.duration / p.speed;
    return { duration, stops: [{ name: 'cands', at: p.candsAt * duration }] };
  },
  build(tl, ctx, p) {
    const words = ctx.skipParts.includes('word') ? [] : ctx.beat.part('word');
    if (!words.length) return;
    const index = Math.min(words.length - 1, Math.max(0, p.word)),
      target = ctx.beat.anchor('word', index).rect,
      d = ctx.duration,
      u = ctx.viewport.px || 1;
    const fg = colorOf(ctx, 'fg'),
      muted = colorOf(ctx, 'fg-muted'),
      accent = colorOf(ctx, 'accent'),
      track = colorOf(ctx, 'accent-2');
    const prev = index > 0 ? ctx.beat.anchor('word', index - 1).rect : null;
    const later = words.slice(index),
      candidates = p.candidates.length ? p.candidates : [{ word: words[index].textContent || '…', p: 100 }];
    // Column under the slot's left edge: word | bar | percent
    const rowH = 84 * u,
      wordSize = 60 * u,
      barX = 400 * u,
      barMax = Math.max(160 * u, Math.min(560 * u, ctx.viewport.w - 96 * u - target.x - 400 * u - 130 * u)),
      top = target.y + target.h + 36 * u;
    const style = globalThis.getComputedStyle?.(ctx.stage.root);
    const display = style?.getPropertyValue('--sl-font-display').trim() || 'sans-serif';
    const mono = style?.getPropertyValue('--sl-font-mono').trim() || 'monospace';
    const make = (tag, css, text) => {
      const node = document.createElement(tag);
      if (text != null) node.textContent = text;
      Object.assign(node.style, { position: 'absolute', margin: '0', whiteSpace: 'nowrap', ...css });
      ctx.overlay.append(node);
      return node;
    };
    const rows = candidates.map((candidate, i) => {
      const y = top + i * rowH;
      const row = make('div', { left: '0px', top: '0px', width: '1px', height: '1px' });
      row.className = 'sl-slot-pick__candidate';
      const word = make(
        'span',
        {
          left: `${target.x}px`,
          top: `${y}px`,
          font: `${candidate.other ? 500 : 700} ${wordSize}px/1 ${display}`,
          letterSpacing: '-0.02em',
          color: candidate.other ? muted : fg,
        },
        candidate.word,
      );
      const rail = make('i', {
        left: `${target.x + barX}px`,
        top: `${y + wordSize * 0.36}px`,
        width: `${barMax}px`,
        height: `${12 * u}px`,
        background: track,
      });
      const bar = make('i', {
        left: `${target.x + barX}px`,
        top: `${y + wordSize * 0.36}px`,
        width: `${barMax}px`,
        height: `${12 * u}px`,
        background: i === 0 ? fg : muted,
        transformOrigin: '0 50%',
      });
      const pct = make(
        'span',
        {
          left: `${target.x + barX + barMax + 28 * u}px`,
          top: `${y + wordSize * 0.08}px`,
          font: `500 ${36 * u}px/1 ${mono}`,
          color: i === 0 ? fg : muted,
        },
        `${candidate.p}%`,
      );
      row.append(word, rail, bar, pct);
      return { row, word, bar, pct, rail, candidate, y };
    });
    const note = make(
      'small',
      {
        left: `${target.x}px`,
        top: `${top + candidates.length * rowH + 12 * u}px`,
        font: `400 ${24 * u}px/1 ${mono}`,
        color: muted,
      },
      p.note,
    );
    note.className = 'sl-slot-pick__note';
    // The pick that flies: same face as the sentence, starts as the first candidate's word
    const sentence = globalThis.getComputedStyle?.(words[index]);
    const carrier = make(
      'span',
      {
        left: `${target.x}px`,
        top: `${target.y}px`,
        font: sentence?.font || `800 ${target.h}px ${display}`,
        letterSpacing: sentence?.letterSpacing || 'normal',
        lineHeight: sentence?.lineHeight || 'normal',
        color: accent,
        transformOrigin: '0 0',
      },
      words[index].textContent,
    );
    carrier.className = 'sl-slot-pick__carrier';
    const caret = make('i', {
      left: '0px',
      top: '0px',
      width: `${Math.max(3, target.h * 0.04)}px`,
      height: `${target.h * 0.78}px`,
      background: accent,
    });
    caret.className = 'sl-slot-pick__caret';
    const after = (r) => ({ x: r.x + r.w + r.h * 0.08, y: r.y + r.h * 0.13 });
    const fromScale = wordSize / Math.max(1, target.h * 0.86);
    const first = rows[0];
    ctx.initial(later, { autoAlpha: 0, color: fg });
    ctx.initial(caret, {
      autoAlpha: 1,
      ...(prev ? after(prev) : { x: target.x, y: target.y + target.h * 0.13 }),
    });
    ctx.initial(note, { autoAlpha: 0 });
    ctx.initial(carrier, {
      autoAlpha: 0,
      x: 0,
      y: first.y - target.y - target.h * 0.06,
      scale: fromScale,
    });
    rows.forEach(({ word, bar, pct, rail, candidate }, i) => {
      const at = i * Math.min(0.06, d * 0.03);
      ctx.initial([word, pct, rail], { autoAlpha: 0, y: 24 * u, filter: 'blur(0px)' });
      ctx.initial(bar, { autoAlpha: 0, y: 24 * u, scaleX: 0, filter: 'blur(0px)' });
      tl.to([word, pct, rail, bar], { autoAlpha: 1, y: 0, duration: d * 0.12, ease: ctx.ease('out') }, at);
      tl.to(
        bar,
        { scaleX: Math.max(0.004, candidate.p / 100), duration: d * 0.24, ease: ctx.ease('out') },
        at + d * 0.04,
      );
    });
    tl.to(note, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.12);
    const pickAt = d * 0.5,
      flyAt = d * 0.6;
    tl.to([first.word, first.pct], { color: accent, duration: d * 0.06, ease: ctx.ease('out') }, pickAt);
    tl.to(first.bar, { backgroundColor: accent, duration: d * 0.06, ease: ctx.ease('out') }, pickAt);
    const losers = rows.slice(1).flatMap(({ word, bar, pct, rail }) => [word, bar, pct, rail]);
    if (losers.length) {
      tl.to(losers, { autoAlpha: 0.3, duration: d * 0.06, ease: ctx.ease('out') }, pickAt);
      tl.to(
        losers,
        {
          y: 40 * u,
          autoAlpha: 0,
          filter: ctx.reduce ? 'blur(0px)' : 'blur(4px)',
          duration: d * 0.16,
          ease: ctx.ease('in'),
        },
        flyAt,
      );
      tl.set(losers, { filter: 'blur(0px)' }, d);
    }
    // the chosen word leaves its row and flies into the slot
    tl.set(first.word, { autoAlpha: 0 }, flyAt);
    tl.set(carrier, { autoAlpha: 1 }, flyAt);
    tl.to(carrier, { y: 0, scale: 1, duration: d * 0.24, ease: ctx.ease('land') }, flyAt);
    tl.to(
      [first.bar, first.pct, first.rail, note],
      { autoAlpha: 0, duration: d * 0.14, ease: ctx.ease('in') },
      flyAt + d * 0.08,
    );
    tl.set(caret, { autoAlpha: 0 }, flyAt);
    tl.set(carrier, { autoAlpha: 0 }, flyAt + d * 0.24);
    tl.set(words[index], { autoAlpha: 1, color: accent }, flyAt + d * 0.24);
    tl.set(caret, { autoAlpha: 1, ...after(target) }, flyAt + d * 0.24);
  },
};
