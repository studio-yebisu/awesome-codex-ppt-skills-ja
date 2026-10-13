/** Condenses a media iris around one light into the first mark of a chart.
 *  영상 끝 프레임의 불빛 한 점(focusX·focusY)을 원형 조리개로 조이고, 그 원을 그대로 옮겨 B의 첫 마크(점)로 바꾼다.
 *  확대·축소 없이 이동만 해서 불빛이 끝까지 원 한가운데 남는다. */
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { frameSeqOf, scrubTo } from '../_shared/media.js';

const circle = (r, x, y) => `circle(${r}px at ${x}px ${y}px)`;
export default {
  id: 'iris-to-dot',
  family: 'morph',
  role: 'link',
  accepts: ['chart'],
  sources: ['morph-match-cut', 'scale-swap', 'shape-morph', 'text-cutout-zoom'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.8, max: 2.4, doc: '전체 길이(u)' },
    focusX: { type: 'number', default: 0.52, min: 0, max: 1, doc: '불빛 x(영상 폭 비율)' },
    focusY: { type: 'number', default: 0.46, min: 0, max: 1, doc: '불빛 y(영상 높이 비율)' },
    hold: {
      type: 'number',
      default: 56,
      min: 20,
      max: 200,
      doc: '조리개가 잠깐 머무는 반지름(px, 1920 기준)',
    },
    desaturate: { type: 'number', default: 1, min: 0, max: 1, doc: '끝에서 채도 빼기' },
  },
  handoff() {
    return { from: { part: 'frame' }, to: { part: 'mark', index: 0 } };
  },
  timing: (p) => ({ duration: p.duration ?? 1.8, stops: [] }),
  build(tl, ctx, p) {
    const { from, to } = ctx.handoff,
      d = p.duration;
    const carry = from.node,
      fr = from.rect;
    const fx = fr.w * p.focusX,
      fy = fr.h * p.focusY; // 불빛(요소 안 좌표)
    const end = { x: to.rect.x + to.rect.w / 2, y: to.rect.y + to.rect.h / 2 };
    const r0 = Math.hypot(fr.w, fr.h),
      r1 = p.hold * ctx.viewport.px,
      r2 = Math.max(to.rect.w, to.rect.h) / 2;
    const dot = document.createElement('i');
    ctx.overlay.append(dot);
    Object.assign(dot.style, {
      position: 'absolute',
      left: `${end.x - r2}px`,
      top: `${end.y - r2}px`,
      width: `${r2 * 2}px`,
      height: `${r2 * 2}px`,
      borderRadius: '50%',
      backgroundColor: colorOf(ctx, 'accent'),
    });
    const caption = ctx.from.part('caption');
    ctx.initial(carry, {
      clipPath: circle(r0, fx, fy),
      x: 0,
      y: 0,
      autoAlpha: 1,
      filter: 'brightness(1) saturate(1)',
    });
    ctx.initial(dot, { autoAlpha: 0, scale: 1 });
    if (ctx.reduce) {
      tl.to(caption, { autoAlpha: 0, duration: d * 0.3 }, 0);
      tl.set(carry, { clipPath: circle(r2, fx, fy), x: end.x - fr.x - fx, y: end.y - fr.y - fy }, d * 0.3);
      tl.to(dot, { autoAlpha: 1, duration: d * 0.3 }, d * 0.5);
      finishLink(tl, ctx, { at: d, cross: 0.12, from: [carry], to: [to.node] });
      return;
    }
    const seq = frameSeqOf(ctx.from);
    if (seq) scrubTo(tl, seq, { from: 1, to: 1, at: 0, duration: d * 0.05 });
    tl.to(caption, { autoAlpha: 0, y: -12 * ctx.viewport.px, duration: d * 0.2, ease: ctx.ease('in') }, 0);
    // 1) 조리개: 화면 → 불빛 둘레
    tl.fromTo(
      carry,
      { clipPath: circle(r0, fx, fy) },
      { clipPath: circle(r1, fx, fy), duration: d * 0.4, ease: 'power3.inOut', immediateRender: false },
      0,
    );
    // 2) 원이 마크 자리로 이동하며 마크 크기로 조여짐, 빛은 주홍 잉크로 식는다
    tl.to(
      carry,
      { x: end.x - fr.x - fx, y: end.y - fr.y - fy, duration: d * 0.4, ease: ctx.ease('inout') },
      d * 0.42,
    );
    tl.fromTo(
      carry,
      { clipPath: circle(r1, fx, fy) },
      { clipPath: circle(r2, fx, fy), duration: d * 0.4, ease: ctx.ease('inout'), immediateRender: false },
      d * 0.42,
    );
    tl.to(
      carry,
      { filter: `brightness(1.8) saturate(${1 - p.desaturate})`, duration: d * 0.3, ease: ctx.ease('inout') },
      d * 0.5,
    );
    tl.to(dot, { autoAlpha: 1, duration: d * 0.14, ease: ctx.ease('out') }, d * 0.74);
    tl.to(carry, { autoAlpha: 0, duration: d * 0.1, ease: ctx.ease('in') }, d * 0.8);
    finishLink(tl, ctx, { at: d, cross: 0.1, from: [carry], to: [to.node] });
    tl.to(dot, { autoAlpha: 0, duration: 0.001 }, d - 0.001);
  },
};
