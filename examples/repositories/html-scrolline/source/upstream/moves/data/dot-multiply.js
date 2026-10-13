/** Expands one unit dot into N same-size dots (N = state value ÷ base value). Signature data move.
 *  점 하나가 제자리에서 복제돼 격자를 채운다. 새 점은 씨앗에서 출발해 가까운 칸부터 자리를 잡고(파문),
 *  오른쪽 카운터가 내려앉은 점 수를 센다. 격자 칸 집합은 행 우선 앞 N칸이라 끝 줄만 비어 「센 수」로 읽힌다. */
import { colorOf } from '../_shared/color.js';
import { canvasLayer } from '../_shared/grid.js';
import { driveValue } from '../_shared/drive.js';
import { clamp, lerp, px } from '../_shared/timeline.js';
import { DISPLAY_FONT, fmt, layers, overlaysOf, swapLayers, tag, tagText } from './annotation-pin.js';

const stateOf = (ctx) =>
  ctx.beat.data.states?.find((s) => s.name === ctx.step?.name) ?? ctx.beat.data.states?.[0] ?? ctx.beat.data;
const valueOf = (data) => data.series?.[0]?.values?.[0] ?? 1;
/** 점 개수 = 상태 값 ÷ 기준 값(beat 기본 값 = 점 하나). */
export const dotCount = (beatData, stateData, max = 2400) =>
  Math.min(max, Math.max(1, Math.round(valueOf(stateData) / (valueOf(beatData) || 1))));
/** 씨앗 점을 가운데 근처 칸에 두는 행 우선 격자(앞 n칸). 순수. */
export function unitGrid(seed, n, { cols, pitch }) {
  const rows = Math.ceil(n / cols),
    cs = Math.floor((cols - 1) / 2),
    rs = Math.floor((rows - 1) / 2);
  return Array.apply(null, { length: n }).map((_, i) => {
    const c = i % cols,
      r = Math.floor(i / cols);
    return { x: seed.x + (c - cs) * pitch, y: seed.y + (r - rs) * pitch, i, d: Math.hypot(c - cs, r - rs) };
  });
}
export const gridBounds = (cells) => ({
  x0: Math.min(...cells.map((c) => c.x)),
  x1: Math.max(...cells.map((c) => c.x)),
  y0: Math.min(...cells.map((c) => c.y)),
  y1: Math.max(...cells.map((c) => c.y)),
});

export default {
  id: 'dot-multiply',
  family: 'data',
  role: 'step',
  accepts: ['chart'],
  sources: ['unit-grid', 'particle-assemble', 'aggregate-split-merge', 'dot-regroup'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 1, max: 4, doc: '전체 길이(u)' },
    cols: { type: 'integer', default: 18, min: 6, max: 60, doc: '격자 열 수' },
    pitch: { type: 'number', default: 54, min: 8, max: 120, doc: '칸 간격(px, 1920 기준)' },
    maxDots: { type: 'integer', default: 2400, min: 50, max: 6000, doc: '점 개수 상한' },
    counter: { type: 'boolean', default: true, doc: '오른쪽 카운터' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      n = dotCount(ctx.beat.data, stateOf(ctx), params.maxDots),
      m = ctx.beat.anchor('mark').rect,
      seed = { x: m.x + m.w / 2, y: m.y + m.h / 2 },
      pitch = px(ctx, params.pitch),
      r = pitch * 0.37,
      R0 = m.w / 2;
    const cells = unitGrid(seed, n, { cols: params.cols, pitch });
    const order = [...cells].sort((a, b) => a.d - b.d || a.i - b.i);
    const rank = new Map(order.map((c, k) => [c.i, k]));
    const layer = canvasLayer(ctx),
      accent = colorOf(ctx, 'accent'),
      proxy = { p: 0 },
      dpr = ctx.viewport.dpr ?? 1;
    const startOf = (k) => 0.04 + 0.66 * (k / n) ** 0.85;
    const q = (k) => clamp((proxy.p - startOf(k)) / 0.16, 0, 1);
    const paint = () => {
      const g = layer.g;
      if (!g) return;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.clearRect(0, 0, ctx.viewport.w, ctx.viewport.h);
      g.fillStyle = accent;
      for (const c of cells) {
        const t = q(rank.get(c.i));
        if (t <= 0) continue;
        const e = 1 - (1 - t) ** 4; // settle: 감속만, 넘침 없음
        g.beginPath();
        g.arc(lerp(seed.x, c.x, e), lerp(seed.y, c.y, e), r * (0.55 + 0.45 * e), 0, Math.PI * 2);
        g.fill();
      }
    };
    let write = () => {};
    const step = (v) => {
      proxy.p = v;
      paint();
      write();
    };
    paint();
    // 진행은 접근자 tween(driveValue)으로: seek이 onUpdate를 건너뛰어도 그려진다
    driveValue(tl, step, { from: 0, to: 1, at: 0, duration: ctx.reduce ? 0.001 : d * 0.8, ease: 'none' });
    // 씨앗 점(실제 마크)은 격자 한 칸 크기로 줄어든다: r은 CSS 속성이라 style로 쓴다
    const seedMark = ctx.beat.part('mark')[0];
    if (seedMark && R0 > r + 0.5)
      driveValue(tl, (v) => seedMark.style.setProperty('r', `${v}px`), { from: R0, to: r, at: 0, duration: ctx.reduce ? 0.001 : d * 0.18, ease: ctx.ease('inout') });
    // 씨앗 주석·리더선은 격자에 덮이기 전에 물러남
    const { stale } = layers(ctx, ['note']);
    const enterMarks = overlaysOf(ctx, ctx.beat.id, (key) => key.includes(':enter:'));
    tl.to([...stale, ...enterMarks], { autoAlpha: 0, duration: d * 0.12, ease: ctx.ease('in') }, 0);
    swapLayers(tl, ctx, d * 0.05, d * 0.3, ['title', 'dek', 'unit']);
    if (params.counter) {
      const b = { x1: Math.max(...cells.map((c) => c.x)), y0: Math.min(...cells.map((c) => c.y)), y1: Math.max(...cells.map((c) => c.y)) };
      const count = tag(ctx, '1', {
        x: b.x1 + r + px(ctx, 96),
        y: (b.y0 + b.y1) / 2,
        size: 220,
        weight: 900,
        color: 'accent',
        font: DISPLAY_FONT,
      });
      const unit = document.createElement('small');
      unit.textContent = '개';
      Object.assign(unit.style, { fontSize: '0.32em', fontWeight: '700', marginLeft: '0.08em' });
      const digits = document.createElement('span');
      digits.textContent = '1';
      tagText(count).replaceChildren(digits, unit);
      ctx.initial(count, { autoAlpha: 0 });
      tl.to(count, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.04);
      write = () => {
        let k = 0;
        for (let i = 0; i < n; i += 1) if (q(i) >= 0.5) k += 1;
        digits.textContent = fmt(Math.max(1, k));
      };
    }
  },
};
