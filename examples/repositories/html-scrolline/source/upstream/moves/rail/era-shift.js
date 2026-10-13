/** Link two chronology eras with a travelling boundary. Used by rail chapter transitions; signature rail move. */
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { eventDetail, railFocus } from '../_shared/rail-focus.js';
import { reelFrom, rollReel } from '../_shared/reel.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, beat, name) =>
  ctx.skipParts.includes(name) && beat === ctx.beat
    ? []
    : beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));
const monthAt = (date) => {
  const match = String(date).match(/^(\d{4})(?:-(\d{1,2}))?/);
  return match ? Number(match[1]) * 12 + (Number(match[2] ?? 1) - 1) : 0;
};
const nowX = (ctx, beat) => (beat.part('now')[0] ? beat.anchor('now').point.x : ctx.viewport.w / 2);
const dotX = (beat, index) => (beat.part('dot')[index] ? beat.anchor('dot', index).point.x : 0);
const digits = (date, kind) =>
  String(date)
    .replace(/\D/g, '')
    .slice(0, kind === 'month' ? 6 : 4)
    .padEnd(kind === 'month' ? 6 : 4, '0');
export default {
  id: 'era-shift',
  family: 'rail',
  role: 'link',
  accepts: ['chronology'],
  sources: ['wipe', 'luma-wipe', 'pan', 'tracking-reveal', 'rolling-digits', 'match-on-action'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2, min: 1, max: 3.6, doc: 'Overall duration.' },
    boundaryWidth: { type: 'number', default: 2, min: 1, max: 6, doc: 'Boundary width in px.' },
    labelTracking: { type: 'number', default: 0.12, min: 0, max: 0.3, doc: 'Incoming label tracking in em.' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  // 넘겨주는 것은 카운터(같은 자리에서 계속 구른다). 트랙은 둘 다 달리므로 착지 대상이 아님.
  handoff(params, { from, to }) {
    const counted = (data) => data?.counter && data.counter !== 'none';
    return counted(from) && counted(to)
      ? { from: { part: 'counter' }, to: { part: 'counter' } }
      : { from: { part: 'track' }, to: { part: 'track' } };
  },
  build(tl, ctx, params) {
    const d = ctx.duration,
      a = ctx.from,
      b = ctx.beat,
      aTrack = a.part('track'),
      bTrack = b.part('track'), // link 자신이 넘기는 트랙이라 skip 대상 아님
      aGround = usable(ctx, a, 'ground'),
      bGround = usable(ctx, b, 'ground');
    // 레일은 끊기지 않는다: A의 마지막 사건에서 B의 첫 사건까지 개월 수만큼 두 트랙이 함께 왼쪽으로 달린다.
    const aEvents = a.data.events ?? [],
      bEvents = b.data.events ?? [];
    const months = Math.max(1, monthAt(bEvents[0]?.date) - monthAt(aEvents.at(-1)?.date));
    const gap = months * (ctx.tokens.monthPx ?? 64) * ctx.viewport.px;
    const aStart = nowX(ctx, a) - dotX(a, aEvents.length - 1),
      bEnd = nowX(ctx, b) - dotX(b, 0);
    railFocus(ctx, b, 0);
    ctx.initial(bGround, { clipPath: 'inset(0% 0% 0% 100%)', autoAlpha: 1 });
    // 앞 시대 종이는 경계선 왼쪽에만 남는다(뒤 beat가 아래 깔려도 넘김이 보이게)
    ctx.initial(aGround, { clipPath: 'inset(0% 0% 0% 0%)' });
    if (!ctx.reduce) {
      const travel = { duration: d * 0.75, ease: ctx.ease('travel'), immediateRender: false };
      tl.fromTo(aTrack, { x: aStart }, { x: aStart - gap, ...travel }, 0);
      tl.fromTo(bTrack, { x: bEnd + gap }, { x: bEnd, ...travel }, 0);
      // 연도 표석은 자기 레일과 같이 달린다
      const aGhosts = a.part('ghost'),
        bGhosts = usable(ctx, b, 'ghost');
      if (aGhosts.length) tl.fromTo(aGhosts, { x: aStart }, { x: aStart - gap, ...travel }, 0);
      if (bGhosts.length) tl.fromTo(bGhosts, { x: bEnd + gap }, { x: bEnd, ...travel }, 0);
      // 떠나는 시대의 초점 사건(제목·설명·날짜)은 출발과 함께 접는다 — 새 시대 사건과 겹치지 않게
      const aDetail = eventDetail(a, aEvents.length - 1).filter((node) => node.dataset.part !== 'stem');
      tl.to(aDetail, { autoAlpha: 0, duration: d * 0.15, ease: ctx.ease('in') }, 0);
      tl.to(bTrack, { autoAlpha: 1, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.15);
    } else {
      tl.to(aTrack, { autoAlpha: 0, duration: d * 0.12 }, d * 0.68);
    }
    tl.to(
      bGround,
      {
        clipPath: 'inset(0% 0% 0% 0%)', // 단위를 맞춰야 GSAP이 보간한다
        duration: d * 0.6,
        ease: ctx.ease('inout'),
      },
      d * 0.2,
    );
    if (!ctx.reduce)
      tl.to(aGround, { clipPath: 'inset(0% 100% 0% 0%)', duration: d * 0.6, ease: ctx.ease('inout') }, d * 0.2);
    const boundary = document.createElement('div');
    Object.assign(boundary.style, {
      position: 'absolute',
      top: '0',
      bottom: '0',
      width: `${px(ctx, params.boundaryWidth)}px`,
      backgroundColor: colorOf(ctx, 'accent'),
    });
    ctx.overlay.append(boundary);
    ctx.initial(boundary, { x: ctx.viewport.w });
    tl.to(boundary, { x: 0, duration: d * 0.6, ease: ctx.ease('inout') }, d * 0.2);
    // 왼쪽 끝에 닿은 경계선은 정지 화면에 남기지 않는다.
    ctx.initial(boundary, { autoAlpha: 1 });
    tl.to(boundary, { autoAlpha: 0, duration: d * 0.12, ease: ctx.ease('in') }, d * 0.8);
    const aLabel = usable(ctx, a, 'label'),
      bLabel = usable(ctx, b, 'label');
    ctx.initial(bLabel, { autoAlpha: 0, letterSpacing: `${params.labelTracking}em` });
    tl.to(aLabel, { x: -px(ctx, 24), autoAlpha: 0, duration: d * 0.2, ease: ctx.ease('in') }, d * 0.55);
    tl.to(
      bLabel,
      { autoAlpha: 1, letterSpacing: '0em', duration: d * 0.24, ease: ctx.ease('out') },
      d * 0.56,
    );
    const aCounter = usable(ctx, a, 'counter')[0],
      bCounter = usable(ctx, b, 'counter')[0];
    if (aCounter) {
      const reel = reelFrom(aCounter),
        fromText = digits(a.data.events.at(-1)?.date, a.data.counter),
        toText = digits(b.data.events[0]?.date, b.data.counter);
      reel.cols.forEach((col, i) => {
        ctx.initial(col, { y: 0, yPercent: -Number(col.dataset.digit ?? 0) * 10 });
        tl.set(col, { yPercent: -Number(fromText[i] ?? 0) * 10 }, 0);
      });
      if (ctx.reduce)
        reel.cols.forEach((col, i) => tl.set(col, { yPercent: -Number(toText[i] ?? 0) * 10 }, d * 0.75));
      else
        rollReel(tl, reel, fromText, toText, { at: d * 0.1, duration: d * 0.65, ease: ctx.ease('travel') });
    }
    if (bCounter) ctx.initial(bCounter, { autoAlpha: 0 });
    const first = eventDetail(b, 0).filter((node) => !(ctx.skipNodes ?? []).includes(node)),
      stem = first.filter((node) => node.dataset.part === 'stem'),
      title = first.filter((node) => node.dataset.part === 'title'),
      rest = first.filter((node) => !['stem', 'title'].includes(node.dataset.part));
    ctx.initial(stem, { scaleY: 0, transformOrigin: 'bottom' });
    ctx.initial(title, { y: px(ctx, 18), autoAlpha: 0 });
    ctx.initial(rest, { autoAlpha: 0 });
    tl.to(stem, { scaleY: 1, duration: d * 0.18, ease: ctx.ease('arrive') }, d * 0.75);
    tl.to(title, { y: 0, autoAlpha: 1, duration: d * 0.18, ease: ctx.ease('out') }, d * 0.8);
    tl.to(rest, { autoAlpha: 1, duration: d * 0.14, ease: ctx.ease('out') }, d * 0.86);
    finishLink(tl, ctx, {
      at: d,
      cross: 0.1,
      from: [...new Set([ctx.handoff.from.node, ...aTrack, ...(aCounter ? [aCounter] : [])])],
      to: [...new Set([ctx.handoff.to.node, ...bTrack, ...(bCounter ? [bCounter] : [])])],
    });
  },
};
