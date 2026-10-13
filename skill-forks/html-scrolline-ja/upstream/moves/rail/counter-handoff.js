/** Counter reels become the next metric. Rail signature link. */
import { finishLink } from '../_shared/link.js';

const numberText = (data) => String(data.value ?? '0');
const dateText = (data) =>
  String(data.events?.[0]?.date ?? '000000')
    .replace(/\D/g, '')
    .slice(0, 6);
const CYCLES = 3;
const css = (node, name) => globalThis.getComputedStyle?.(node)?.getPropertyValue(name) ?? '';

/**
 * 숫자 글꼴로 된 릴 줄. 칸 = 숫자 글자 하나(0–9 × CYCLES 세로 띠) 또는 고정 글자(쉼표·단위·날짜 점).
 * 날짜 상태에선 앞 6자리와 점만, 숫자 상태에선 점 빼고 전부 열린다. 닫힌 칸은 폭 0.
 */
function buildCarry(ctx, rect, number, date, fontPx, font) {
  const carry = document.createElement('div');
  carry.className = 'sl-counter-carry';
  Object.assign(carry.style, {
    position: 'absolute',
    left: `${rect.x}px`,
    top: `${rect.y}px`,
    width: `${rect.w}px`,
    height: `${rect.h}px`,
    margin: '0',
    display: 'flex',
    alignItems: 'flex-start',
    whiteSpace: 'nowrap',
    fontFamily: font.family,
    fontWeight: font.weight,
    fontSize: `${fontPx}px`,
    lineHeight: '1.08',
    letterSpacing: font.tracking,
  });
  carry.dataset.slRect = JSON.stringify(rect);
  ctx.overlay.append(carry);
  const cells = [];
  let digitIndex = 0;
  const cell = (char, kind) => {
    const box = document.createElement('span');
    Object.assign(box.style, {
      display: 'inline-block',
      height: '1.08em',
      overflow: 'hidden',
      textAlign: 'center',
      flex: '0 0 auto',
    });
    const strip = document.createElement('span');
    strip.style.display = 'block';
    if (kind === 'digit')
      for (let i = 0; i < 10 * CYCLES; i += 1) {
        const d = document.createElement('span');
        Object.assign(d.style, { display: 'block', height: '1.08em' });
        d.textContent = String(i % 10);
        strip.append(d);
      }
    else strip.textContent = char;
    box.append(strip);
    carry.append(box);
    cells.push({ box, strip, kind, char });
    return cells.at(-1);
  };
  [...number].forEach((char) => {
    if (/\d/.test(char)) {
      const c = cell(char, 'digit');
      c.numberDigit = Number(char);
      c.dateDigit = digitIndex < date.length ? Number(date[digitIndex]) : null;
      digitIndex += 1;
      // 날짜 「2020.05」의 점: 넷째 숫자 뒤에 날짜 전용 칸
      if (digitIndex === 4 && date.length > 4) cell('.', 'dot');
    } else cell(char, 'fixed');
  });
  // 폭은 그 상태에서 보이는 글자 폭(비례 숫자라 칸마다 다름)
  const probe = document.createElement('span');
  probe.style.display = 'inline-block';
  carry.append(probe);
  const widthOf = (char) => {
    probe.textContent = char;
    return probe.getBoundingClientRect().width;
  };
  cells.forEach((c) => {
    const open = (state) =>
      c.kind === 'dot' ? state === 'date' : c.kind === 'fixed' ? state === 'number' : state === 'number' || c.dateDigit !== null;
    c.width = {
      number: open('number') ? widthOf(c.kind === 'digit' ? String(c.numberDigit) : c.char) : 0,
      date: open('date') ? widthOf(c.kind === 'digit' ? String(c.dateDigit) : c.char) : 0,
    };
    c.digit = { number: c.numberDigit, date: c.dateDigit ?? 0 };
  });
  probe.remove();
  return { carry, cells };
}

export default {
  id: 'counter-handoff',
  family: 'rail',
  role: 'link',
  accepts: ['number', 'chronology'],
  sources: ['rolling-digits', 'count-up', 'match-cut', 'scale-swap', 'glyph-roll'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.8, max: 3, doc: '전체 길이(u)' },
    stagger: { type: 'number', default: 0.04, min: 0, max: 0.12, doc: '항목 간 시차(u)' },
    dim: { type: 'number', default: 0.12, min: 0, max: 0.4, doc: '물린 대상 opacity' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  handoff(p, { from, to }) {
    return {
      from: { part: from.type === 'chronology' ? 'counter' : 'value' },
      to: { part: to.type === 'chronology' ? 'counter' : 'value' },
    };
  },
  build(tl, ctx, p) {
    const d = p.duration,
      from = ctx.handoff.from,
      to = ctx.handoff.to;
    if (ctx.reduce) return finishLink(tl, ctx, { at: d, cross: 0.12 });
    const outgoing = ctx.from.type === 'chronology';
    const numberNode = outgoing ? to.node : from.node,
      numberRect = outgoing ? to.rect : from.rect;
    const number = (numberNode.textContent ?? '').trim() || numberText(outgoing ? ctx.beat.data : ctx.from.data);
    const date = dateText(outgoing ? ctx.from.data : ctx.beat.data);
    // 운반체는 도착 자리(to.rect)에 도착 크기로 놓고, 출발 자리 크기로 줄였다 펴서 끝 프레임이 선명하게.
    const numberFont = parseFloat(css(numberNode, 'font-size')) || numberRect.h / 1.08 || 16;
    const fontPx = numberRect.h ? (numberFont * to.rect.h) / numberRect.h : numberFont;
    // 글꼴은 숫자 beat의 계산값을 그대로(운반체는 overlay에 있어 beat 범위 CSS를 못 받는다)
    const font = {
      family: css(numberNode, 'font-family') || 'serif',
      weight: css(numberNode, 'font-weight') || '800',
      tracking: css(numberNode, 'letter-spacing') || 'normal',
    };
    const { carry, cells } = buildCarry(ctx, to.rect, number, date, fontPx, font);
    const start = outgoing ? 'date' : 'number',
      end = outgoing ? 'number' : 'date';
    const scale = to.rect.h ? from.rect.h / to.rect.h : 1;
    const fromColor = css(from.node, 'color'),
      toColor = css(to.node, 'color');
    ctx.initial(carry, {
      autoAlpha: 0,
      x: from.rect.x - to.rect.x,
      y: from.rect.y - to.rect.y,
      scaleX: scale,
      scaleY: scale,
      transformOrigin: '0 0',
      ...(fromColor ? { color: fromColor } : {}),
    });
    // from.node의 처음 상태는 앞 move가 정한다(여기서 initial로 켜면 같은 노드를 받는 앞 link의 숨김을 덮어쓴다).
    ctx.initial(to.node, { autoAlpha: 0 });
    // 출발: 진짜 카운터/숫자와 운반체가 겹친 자리에서 바뀐다
    tl.to(carry, { autoAlpha: 1, duration: d * 0.08, ease: 'none' }, 0);
    tl.to(from.node, { autoAlpha: 0, duration: d * 0.08, ease: 'none' }, d * 0.04);
    const rail = ['track', 'event', 'ghost', 'now'].flatMap((name) => (outgoing ? ctx.from : ctx.beat).part(name));
    if (outgoing) tl.to(rail, { y: 24, autoAlpha: p.dim, duration: d * 0.2, ease: ctx.ease('in') }, 0);
    else {
      ctx.initial(rail, { y: 24, autoAlpha: p.dim });
      tl.to(rail, { y: 0, autoAlpha: 1, duration: d * 0.4, ease: ctx.ease('out') }, d * 0.6);
    }
    // 비행: 작은 날짜 ↔ 큰 숫자
    tl.to(
      carry,
      { x: 0, y: 0, scaleX: 1, scaleY: 1, duration: d * 0.62, ease: ctx.ease('inout') },
      d * 0.08,
    );
    if (toColor) tl.to(carry, { color: toColor, duration: d * 0.5, ease: 'none' }, d * 0.2);
    // 칸 열고 닫기(새 자리는 폭 0에서 열린다)
    cells.forEach((c) => {
      ctx.initial(c.box, { width: c.width[start], autoAlpha: c.width[start] ? 1 : 0 });
      if (c.width[start] !== c.width[end])
        tl.to(
          c.box,
          { width: c.width[end], autoAlpha: c.width[end] ? 1 : 0, duration: d * 0.42, ease: ctx.ease('inout') },
          d * 0.14,
        );
    });
    // 릴: 모두 함께 돌기 시작해 왼쪽부터 차례로 멈춘다(마지막 칸이 가장 늦게)
    const digits = cells.filter((c) => c.kind === 'digit');
    const step = 100 / (10 * CYCLES);
    digits.forEach((c, i) => {
      const a = c.digit[start],
        b = c.digit[end] + 10 * (CYCLES - 1);
      const land = d * (0.62 + 0.24 * (digits.length > 1 ? i / (digits.length - 1) : 1));
      ctx.initial(c.strip, { yPercent: -a * step });
      tl.to(c.strip, { yPercent: -b * step, duration: land - d * 0.1, ease: ctx.ease('settle') }, d * 0.1);
    });
    finishLink(tl, ctx, { at: d, cross: 0.12, from: [from.node, carry] });
  },
};
