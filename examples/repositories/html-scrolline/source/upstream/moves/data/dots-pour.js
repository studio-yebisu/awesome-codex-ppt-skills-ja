/** Pours a unit-dot grid into one bar of the next chart, then grows the rest of that chart.
 *  A의 점 N개가 B의 대상 막대(toIndex) 안으로 쏟아져 아래부터 쌓이고, 다 차면 막대가 굳는다.
 *  그다음 나머지 막대가 기준선에서 차례로 자라 「그 점들이 2025년 한 해」였음을 보여 준다. */
import { colorOf } from '../_shared/color.js';
import { canvasLayer } from '../_shared/grid.js';
import { finishLink } from '../_shared/link.js';
import { driveValue } from '../_shared/drive.js';
import { clamp, lerp, px } from '../_shared/timeline.js';
import { fmt, growBar, overlaysOf, tag } from './annotation-pin.js';
import { dotCount, unitGrid } from './dot-multiply.js';

const base = (nodes) => nodes.filter((node) => (node.dataset.state ?? 'base') === 'base');
export default {
  id: 'dots-pour',
  family: 'data',
  role: 'link',
  accepts: ['chart'],
  sources: ['dot-regroup', 'unit-aggregate-transition', 'beeswarm-settling'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 1, max: 4, doc: '전체 길이(u)' },
    toIndex: { type: 'integer', default: -1, min: -1, max: 40, doc: 'B 쪽 대상 막대 index(-1 = 마지막)' },
    cols: { type: 'integer', default: 18, min: 6, max: 60, doc: 'A 격자 열 수(dot-multiply와 같게)' },
    pitch: { type: 'number', default: 54, min: 8, max: 120, doc: 'A 격자 칸 간격(px)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  handoff(params) {
    return { from: { part: 'mark', index: 0 }, to: { part: 'mark', index: params.toIndex } };
  },
  build(tl, ctx, params) {
    const d = params.duration,
      A = ctx.from,
      B = ctx.beat,
      to = ctx.handoff.to,
      bar = to.rect;
    const lastState = A.data.states?.at(-1) ?? A.data;
    const n = dotCount(A.data, lastState),
      m = A.anchor('mark').rect,
      seed = { x: m.x + m.w / 2, y: m.y + m.h / 2 },
      r0 = px(ctx, params.pitch) * 0.37;
    const from = unitGrid(seed, n, { cols: params.cols, pitch: px(ctx, params.pitch) });
    // 막대 안 칸: 막대 비율에 맞춘 열 수, 아래 줄부터
    const cell = Math.sqrt((bar.w * bar.h) / n),
      cols = Math.max(1, Math.round(bar.w / cell)),
      rows = Math.ceil(n / cols),
      cw = bar.w / cols,
      ch = bar.h / rows,
      r1 = Math.min(cw, ch) * 0.42;
    const slots = Array.apply(null, { length: n }).map((_, k) => ({
      x: bar.x + cw * ((k % cols) + 0.5),
      y: bar.y + bar.h - ch * (Math.floor(k / cols) + 0.5),
    }));
    // 막대에 가까운 점부터 출발(오른쪽 아래 → 왼쪽 위)
    const order = [...from].sort((a, b) => Math.hypot(a.x - bar.x, a.y - bar.y - bar.h) - Math.hypot(b.x - bar.x, b.y - bar.y - bar.h));
    const layer = canvasLayer(ctx),
      accent = colorOf(ctx, 'accent'),
      dpr = ctx.viewport.dpr ?? 1,
      proxy = { p: 0 };
    const paint = () => {
      const g = layer.g;
      if (!g) return;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.clearRect(0, 0, ctx.viewport.w, ctx.viewport.h);
      g.fillStyle = accent;
      order.forEach((c, k) => {
        const t = clamp((proxy.p - (k / n) * 0.5) / 0.4, 0, 1);
        const e = t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2;
        const s = slots[k];
        // 살짝 위로 떠올랐다 떨어지는 포물선(붓는 느낌), 끝값은 정확히 칸
        const lift = Math.sin(Math.PI * e) * px(ctx, 80);
        g.beginPath();
        g.arc(lerp(c.x, s.x, e), lerp(c.y, s.y, e) - lift, lerp(r0, r1, e), 0, Math.PI * 2);
        g.fill();
      });
    };
    paint();
    driveValue(tl, (v) => ((proxy.p = v), paint()), { from: 0, to: 1, at: 0, duration: ctx.reduce ? 0.001 : d * 0.55, ease: 'none' });
    // A: 점 격자·카운터·글자는 출발과 함께 정리
    const aOverlay = overlaysOf(ctx, A.id, (key) => !key.includes(':link:'));
    tl.set(aOverlay.filter((node) => node.tagName === 'CANVAS'), { autoAlpha: 0 }, 0);
    const aText = Object.values(A.parts).flat().filter((node) => !A.part('plot').includes(node));
    tl.to([...aText, ...aOverlay.filter((node) => node.tagName !== 'CANVAS')], { autoAlpha: 0, duration: d * 0.12, ease: ctx.ease('in') }, 0);
    tl.set(A.part('mark'), { autoAlpha: 0 }, 0);
    // B: 대상 막대가 굳고 점은 녹는다
    ctx.initial(to.node, { autoAlpha: 0 });
    tl.to(to.node, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.58);
    ctx.initial(layer.canvas, { autoAlpha: 1 });
    tl.to(layer.canvas, { autoAlpha: 0, duration: d * 0.1, ease: ctx.ease('in') }, d * 0.64);
    // 축·이름표 → 나머지 막대가 기준선에서 자람(오래된 해부터)
    const support = [...B.part('axis'), ...B.part('label'), ...B.part('baseline')];
    ctx.initial(support, { autoAlpha: 0 });
    tl.to(support, { autoAlpha: 1, duration: d * 0.12, ease: ctx.ease('out') }, d * 0.5);
    const others = B.part('mark').filter((node) => node !== to.node);
    others.forEach((node, k) =>
      growBar(tl, ctx, node, {
        at: d * (0.64 + (0.14 * k) / Math.max(1, others.length - 1)),
        duration: d * 0.18,
        ease: ctx.ease('settle'),
        horizontal: B.data.orient === 'h',
      }),
    );
    const copy = [...base(B.part('title')), ...base(B.part('dek')), ...base(B.part('unit')), ...B.part('source')];
    ctx.initial(copy, { autoAlpha: 0, yPercent: 30 });
    tl.to(copy, { autoAlpha: 1, yPercent: 0, duration: d * 0.16, ease: ctx.ease('settle') }, d * 0.45);
    const v = B.data.series?.[0]?.values?.at(to.index);
    if (Number.isFinite(v)) {
      const label = tag(ctx, `${fmt(v)}${B.data.unit ?? ''}`, { x: bar.x + bar.w / 2, y: bar.y - px(ctx, 14), align: 'center', valign: 'bottom', size: 30, weight: 700, color: 'accent' });
      ctx.initial(label, { autoAlpha: 0 });
      tl.to(label, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.62);
    }
    finishLink(tl, ctx, { at: d, cross: 0, from: [ctx.handoff.from.node], to: [to.node] });
  },
};
