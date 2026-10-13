/** Lift one rail event into a beat's primary subject. */
import { transferVars } from '../../engine/index.js';
import { eventPart } from '../_shared/event-part.js';
import { RAIL_DETAIL } from '../_shared/rail-focus.js';
import { finishLink, ghost } from '../_shared/link.js';

export default {
  id: 'rail-lift',
  family: 'rail',
  role: 'link',
  accepts: ['quote', 'video', 'photo', 'number'],
  sources: ['match-cut', 'morph-match-cut', 'scale-swap', 'clip-reveal'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.6, min: 0.8, max: 2.8, doc: '전체 길이(u)' },
    fromEvent: { type: 'integer', default: -1, doc: '-1 = 마지막 사건' },
    fromPart: {
      type: 'enum',
      default: 'media',
      values: ['dot', 'media', 'title'],
      doc: 'dot | media | title',
    },
    toPart: { type: 'part', default: '', doc: '빈 값 = B primary' },
    toIndex: { type: 'integer', default: 0, doc: 'B toPart 요소 순번(anchor index, 계약 요청)' },
    liftRise: { type: 'number', default: 0.12, min: 0.04, max: 0.3, doc: 'liftRise(안무 설명의 같은 이름)' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  handoff(p, { from } = {}) {
    return { from: eventPart(from?.events, p.fromPart, p.fromEvent), to: { part: p.toPart, index: p.toIndex } };
  },
  build(tl, ctx, p) {
    const d = p.duration,
      { from, to } = ctx.handoff;
    if (ctx.reduce) return finishLink(tl, ctx, { at: d, cross: 0.12 });
    const carry = ghost(ctx, from.node, from.rect);
    // 점에서 떠오르면 끝까지 둥근 잉크 방울로 간다(따옴표·이름표 자리에서 겹쳐 바뀐다)
    const radius = from.part === 'dot' ? '50%' : 0;
    const stem = ctx.from.part('stem').at(p.fromEvent) ?? ctx.from.part('stem').at(-1);
    const sinking = ['track', 'event', 'counter', 'label'].flatMap((name) => ctx.from.part(name));
    ctx.initial(carry, {
      autoAlpha: 1,
      x: 0,
      y: 0,
      scaleX: 1,
      scaleY: 1,
      borderRadius: radius,
      transformOrigin: '0 0',
    });
    ctx.initial(to.node, { autoAlpha: 0 });
    // 레일 초점 상세(제목·썸네일)는 step이 드러낼 때까지 숨어 있다 — 처음부터 보이게 두면 초점이 깨진다.
    const focused = RAIL_DETAIL.includes(from.part) && ctx.from.part('now').length > 0;
    ctx.initial(from.node, { autoAlpha: focused ? 0 : 1 });
    if (stem) tl.to(stem, { scaleY: 1.6, duration: d * 0.3, ease: ctx.ease('in') }, 0);
    tl.to(sinking, { y: 32, autoAlpha: 0.08, duration: d * 0.35, ease: ctx.ease('in') }, d * 0.1);
    tl.to(carry, { y: -p.liftRise * ctx.viewport.h, duration: d * 0.3, ease: ctx.ease('in') }, 0);
    tl.to(
      carry,
      { ...transferVars(from.rect, to.rect), borderRadius: radius, duration: d * 0.55, ease: ctx.ease('inout') },
      d * 0.3,
    );
    finishLink(tl, ctx, { at: d, cross: 0.12, from: [from.node, carry] });
  },
};
