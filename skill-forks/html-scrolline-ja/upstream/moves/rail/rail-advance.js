/** Advance a chronology rail to its next dated event. Used by rail step beats; signature rail move. */
import { gridLayout } from '../_shared/grid.js';
import { eventDetail } from '../_shared/rail-focus.js';
import { reelFrom, rollReel } from '../_shared/reel.js';
import { clamp, px } from '../_shared/timeline.js';

const monthAt = (date) => {
  const match = String(date).match(/^(\d{4})(?:-(\d{1,2}))?/);
  return match ? Number(match[1]) * 12 + (Number(match[2] ?? 1) - 1) : 0;
};
const digits = (date, counter) =>
  String(date)
    .replace(/\D/g, '')
    .slice(0, counter === 'month' ? 6 : 4)
    .padEnd(counter === 'month' ? 6 : 4, '0');
const nodes = (ctx, name) =>
  ctx.skipParts.includes(name)
    ? []
    : ctx.beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));
const eventIndex = (params, events) =>
  clamp(params.from < 0 ? params.to - 1 : params.from, 0, events.length - 1);
// 사건 위치 = 점 중심(사건 상자는 설명 폭만큼 넓어 중심이 점에서 멀다)
const eventX = (ctx, index) => ctx.beat.anchor('dot', index).point.x;
const nowX = (ctx) => {
  const now = ctx.beat.part('now')[0];
  return now ? ctx.beat.anchor('now').rect.x + ctx.beat.anchor('now').rect.w / 2 : ctx.viewport.w / 2;
};

export default {
  id: 'rail-advance',
  family: 'rail',
  role: 'step',
  accepts: ['chronology'],
  sources: [
    'pan',
    'infinite-pan',
    'parallax',
    'rolling-digits',
    'glyph-roll',
    'motion-blur',
    'timeline-scrub',
    'focus-handoff',
  ],
  reduce: 'self',
  params: {
    from: { type: 'integer', default: -1, doc: '-1 = to-1, 0..events-1' },
    to: { type: 'integer', default: 1, doc: '0..events-1' },
    base: { type: 'number', default: 0.6, min: 0.3, max: 1.2, doc: 'Base travel duration.' },
    perMonth: { type: 'number', default: 0.05, min: 0, max: 0.15, doc: 'Extra duration per month.' },
    max: { type: 'number', default: 2.6, min: 0.8, max: 4, doc: 'Maximum travel duration.' },
    ghostParallax: { type: 'number', default: 1, min: 0, max: 1, doc: 'Year-marker travel ratio (1 = rides the rail).' },
    blurMax: { type: 'number', default: 4, min: 0, max: 8, doc: 'Maximum motion blur in px.' },
    trailOpacity: { type: 'number', default: 0.32, min: 0.15, max: 0.6, doc: 'Passed-event opacity.' },
  },
  timing(params, data) {
    const events = data.events ?? [],
      from = eventIndex(params, events),
      to = clamp(params.to, 0, Math.max(0, events.length - 1));
    return {
      duration: Math.min(
        params.max,
        params.base + params.perMonth * Math.abs(monthAt(events[to]?.date) - monthAt(events[from]?.date)),
      ),
      stops: [],
    };
  },
  build(tl, ctx, params) {
    const events = ctx.beat.data.events ?? [],
      from = eventIndex(params, events),
      to = clamp(params.to, 0, events.length - 1),
      d = ctx.duration;
    if (!events.length) return;
    gridLayout({ n: events.length, cols: events.length || 1, cell: 1 });
    const track = nodes(ctx, 'track'),
      start = nowX(ctx) - eventX(ctx, from),
      end = nowX(ctx) - eventX(ctx, to),
      travel = d * 0.7;
    // fromTo: 같은 track을 여러 step이 움직이므로 시작 x를 직접 적는다(initial은 마지막 step 값만 남음).
    ctx.initial(track, { filter: 'none' });
    tl.fromTo(
      track,
      { x: start },
      { x: end, duration: travel, ease: ctx.reduce ? 'none' : ctx.ease('travel'), immediateRender: false },
      0,
    );
    if (!ctx.reduce && params.blurMax) {
      const blur = Math.min(params.blurMax, ctx.tokens.blurMax ?? 12);
      tl.to(track, { filter: `blur(${blur}px)`, duration: d * 0.15, ease: ctx.ease('out') }, 0);
      tl.to(track, { filter: `blur(${blur}px)`, duration: d * 0.25, ease: 'none' }, d * 0.15);
      tl.to(track, { filter: 'none', duration: d * 0.15, ease: ctx.ease('in') }, d * 0.4);
    }
    // 연도 표석은 레일과 같이 달린다(종이 ground 자체는 화면에 고정)
    const ghosts = nodes(ctx, 'ghost');
    tl.fromTo(
      ghosts,
      { x: start * params.ghostParallax },
      {
        x: end * params.ghostParallax,
        duration: travel,
        ease: ctx.reduce ? 'none' : ctx.ease('travel'),
        immediateRender: false,
      },
      0,
    );
    // 지나온 사건: 상세는 접고 줄기만 흐린 자취로. 사이에 낀 사건은 점만 스친다.
    // skipNodes는 「들여오기」에서만 뺀다: link가 놓은 썸네일도 지나가면 접는다(C5 v2 skip 규칙 명시).
    const skip = ctx.skipNodes ?? [];
    const passed = eventDetail(ctx.beat, from);
    const passedStem = passed.filter((node) => node.dataset.part === 'stem');
    const passedText = passed.filter((node) => node.dataset.part !== 'stem');
    tl.to(passedText, { autoAlpha: 0, duration: d * 0.3, ease: ctx.ease('in') }, d * 0.05);
    tl.to(passedStem, { autoAlpha: params.trailOpacity, duration: d * 0.5, ease: ctx.ease('in') }, d * 0.1);
    const detail = eventDetail(ctx.beat, to).filter((node) => !skip.includes(node)),
      stem = detail.filter((node) => node.dataset.part === 'stem'),
      title = detail.filter((node) => node.dataset.part === 'title'),
      note = detail.filter((node) => node.dataset.part === 'note'),
      media = detail.filter((node) => node.dataset.part === 'media'),
      source = detail.filter((node) => ['source', 'date'].includes(node.dataset.part));
    ctx.initial(stem, { scaleY: 0, transformOrigin: 'bottom' });
    ctx.initial(title, { y: px(ctx, 18), autoAlpha: 0 });
    ctx.initial([...note, ...source], { autoAlpha: 0 });
    tl.to(stem, { scaleY: 1, autoAlpha: 1, duration: d * 0.4, ease: ctx.ease('arrive') }, d * 0.6);
    tl.to(title, { y: 0, autoAlpha: 1, duration: d * 0.24, ease: ctx.ease('out') }, d * 0.68);
    tl.to([...note, ...source], { autoAlpha: 1, duration: d * 0.22, ease: ctx.ease('out') }, d * 0.78);
    if (media.length) {
      ctx.initial(media, { clipPath: 'inset(100% 0 0 0)', autoAlpha: 0 });
      tl.to(media, { clipPath: 'inset(0% 0 0 0)', autoAlpha: 1, duration: d * 0.22, ease: ctx.ease('out') }, d * 0.76);
    }
    // 카운터는 counter-handoff가 놓고 간 뒤에도 사건마다 구른다(skip은 들여오기만, #48).
    const counter = ctx.beat.part('counter')[0];
    if (counter) {
      const reel = reelFrom(counter),
        kind = ctx.beat.data.counter,
        fromText = digits(events[from].date, kind),
        toText = digits(events[to].date, kind);
      // y: 0 — 렌더러의 inline translateY(%)를 GSAP이 px y로 읽어 yPercent에 겹치지 않게(C4 counter).
      reel.cols.forEach((col, i) => {
        ctx.initial(col, { y: 0, yPercent: -Number(col.dataset.digit ?? 0) * 10 });
        tl.set(col, { yPercent: -Number(fromText[i] ?? 0) * 10 }, 0);
      });
      if (ctx.reduce)
        reel.cols.forEach((col, i) => {
          if (fromText[i] !== toText[i]) tl.set(col, { yPercent: -Number(toText[i]) * 10 }, d * 0.7);
        });
      else
        rollReel(tl, reel, fromText, toText, {
          at: d * 0.05,
          duration: d * 0.65,
          ease: ctx.ease('travel'),
          steps: kind === 'month',
        });
    }
  },
};
