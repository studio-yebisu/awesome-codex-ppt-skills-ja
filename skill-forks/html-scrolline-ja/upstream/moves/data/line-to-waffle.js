/** Unfolds the end point of a share line into a 100-cell waffle.
 *  A 선의 끝점(마지막 비중)이 B 격자의 첫 칸으로 날아가 네모가 되고, 그 칸에서 켜진 칸(값 %)이 번지고
 *  나머지 칸이 회색으로 깔린다. 오른쪽에는 범주 이름과 큰 값. 칸은 DOM(정지점 = 보이는 그대로). */
import { colorOf } from '../_shared/color.js';
import { px } from '../_shared/timeline.js';
import { DISPLAY_FONT, fmt, overlaysOf, plotBox, tag, tagText } from './annotation-pin.js';
import { morphPoints } from './mark-morph.js';

/** B 플롯 왼쪽에 놓는 cols×rows 격자(행 우선, 위에서 아래). */
export function waffleGeom(beat, { cols = 10, cells = 100 } = {}) {
  const box = plotBox(beat),
    rows = Math.ceil(cells / cols),
    pitch = box.h / rows,
    size = pitch * 0.86;
  const list = Array.apply(null, { length: cells }).map((_, i) => ({
    x: box.x + (i % cols) * pitch,
    y: box.y + Math.floor(i / cols) * pitch,
    i,
  }));
  return { box, pitch, size, list, right: box.x + cols * pitch, mid: box.y + (rows * pitch) / 2 };
}
/** 오른쪽 열: 범주 이름(L2) + 큰 값(숫자 히어로). */
export function waffleLegend(ctx, beat, g, index, value) {
  const x = g.right + px(ctx, 120);
  const label = tag(ctx, beat.data.categories?.[index] ?? '', { x, y: g.mid - px(ctx, 200), valign: 'bottom', size: 36, weight: 600, color: 'fg' });
  const big = tag(ctx, '', { x: x - px(ctx, 8), y: g.mid - px(ctx, 130), valign: 'top', size: 260, weight: 900, color: 'accent', font: DISPLAY_FONT });
  const digits = document.createElement('span');
  digits.textContent = fmt(value);
  const unit = document.createElement('small');
  unit.textContent = beat.data.unit ?? '';
  Object.assign(unit.style, { fontSize: '0.4em', marginLeft: '0.06em' });
  tagText(big).replaceChildren(digits, unit);
  label.classList.add('sl-data-waffle-label');
  big.classList.add('sl-data-waffle-value');
  return { label, big, digits };
}
export function cell(ctx, g, c, color) {
  const node = document.createElement('i');
  node.className = 'sl-data-cell';
  node.dataset.cell = String(c.i);
  Object.assign(node.style, {
    position: 'absolute',
    left: `${c.x}px`,
    top: `${c.y}px`,
    width: `${g.size}px`,
    height: `${g.size}px`,
    backgroundColor: color,
    boxSizing: 'border-box',
  });
  ctx.overlay.append(node);
  return node;
}

export default {
  id: 'line-to-waffle',
  family: 'data',
  role: 'link',
  accepts: ['chart'],
  sources: ['unit-grid', 'scale-swap', 'fractional-icon-fill'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2, min: 0.8, max: 3, doc: '전체 길이(u)' },
    cols: { type: 'integer', default: 10, min: 5, max: 20, doc: '격자 열 수' },
    cells: { type: 'integer', default: 100, min: 20, max: 400, doc: '격자 칸 수' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  handoff() {
    // B 플롯은 칸이 대신하므로 넘길 대상은 B 제목(끝에 보이게 함)
    return { from: { part: 'mark', index: -1 }, to: { part: 'title', index: 0 } };
  },
  build(tl, ctx, params) {
    const d = params.duration,
      R = ctx.reduce ? 0.001 : 1,
      A = ctx.from,
      B = ctx.beat;
    const aState = A.data.states?.at(-1) ?? A.data;
    const end = morphPoints(A, aState).at(-1);
    const value = (aState.series ?? A.data.series)[0].values.at(-1);
    const lit = Math.max(0, Math.min(params.cells, Math.round((value * params.cells) / 100)));
    const g = waffleGeom(B, params),
      accent = colorOf(ctx, 'accent'),
      rule = colorOf(ctx, 'rule');
    // A 정리: 끝점만 남기고 전부 퇴장
    const aLine = overlaysOf(ctx, A.id, (k) => k.includes(':step:'));
    const aAll = Object.values(A.parts).flat().filter((n) => !A.part('plot').includes(n));
    tl.to(aLine, { autoAlpha: 0, duration: d * 0.2 * R, ease: ctx.ease('in') }, d * 0.22);
    // 선은 끝점이 떠난 뒤에 물러난다(빈 화면에 점 하나만 남는 순간을 피함)
    tl.to(aAll, { autoAlpha: 0, duration: d * 0.15 * R, ease: ctx.ease('in') }, 0);
    tl.to(A.part('plot'), { autoAlpha: 0, duration: d * 0.2 * R, ease: ctx.ease('in') }, d * 0.22);
    // 끝점 대역: 원 → 첫 칸 네모
    const r0 = px(ctx, 15),
      first = g.list[0];
    const carrier = document.createElement('i');
    Object.assign(carrier.style, {
      position: 'absolute',
      left: `${first.x}px`,
      top: `${first.y}px`,
      width: `${g.size}px`,
      height: `${g.size}px`,
      backgroundColor: accent,
    });
    ctx.overlay.append(carrier);
    const s0 = (2 * r0) / g.size;
    ctx.initial(carrier, {
      x: end.x - first.x - g.size / 2,
      y: end.y - first.y - g.size / 2,
      scale: s0,
      borderRadius: '50%',
      transformOrigin: '50% 50%',
      autoAlpha: 1,
    });
    tl.to(carrier, { x: 0, y: 0, scale: 1, duration: d * 0.35 * R, ease: ctx.ease('inout') }, d * 0.1);
    tl.to(carrier, { borderRadius: '0%', duration: d * 0.15 * R, ease: ctx.ease('inout') }, d * 0.3);
    // 켜진 칸이 첫 칸에서 번지고, 나머지는 회색으로 깔림
    const cells = g.list.map((c) => cell(ctx, g, c, c.i < lit ? accent : rule));
    cells.forEach((node, i) => {
      const dist = Math.hypot(g.list[i].x - first.x, g.list[i].y - first.y) / (g.pitch * params.cols);
      ctx.initial(node, { autoAlpha: 0, scale: 0.3, transformOrigin: '50% 50%' });
      const at = i < lit ? d * (0.45 + 0.18 * (i / Math.max(1, lit))) : d * (0.62 + 0.18 * dist);
      tl.to(node, { autoAlpha: 1, scale: 1, duration: d * 0.12 * R, ease: ctx.ease('settle') }, at);
    });
    tl.set(carrier, { autoAlpha: 0 }, d * 0.47);
    const legend = waffleLegend(ctx, B, g, 0, lit);
    ctx.initial([legend.label, legend.big], { autoAlpha: 0, y: px(ctx, 16) });
    tl.to([legend.label, legend.big], { autoAlpha: 1, y: 0, duration: d * 0.16 * R, ease: ctx.ease('settle'), stagger: d * 0.04 * R }, d * 0.66);
    // B 글자(기본 층)
    const copy = ['title', 'dek', 'unit', 'source'].flatMap((name) => B.part(name)).filter((n) => (n.dataset.state ?? 'base') === 'base' && n !== ctx.handoff.to.node);
    ctx.initial(copy, { autoAlpha: 0, yPercent: 30 });
    tl.to(copy, { autoAlpha: 1, yPercent: 0, duration: d * 0.16 * R, ease: ctx.ease('settle') }, d * 0.45);
    ctx.initial(ctx.handoff.to.node, { autoAlpha: 0, yPercent: 30 });
    tl.to(ctx.handoff.to.node, { autoAlpha: 1, yPercent: 0, duration: d * 0.16 * R, ease: ctx.ease('settle') }, d * 0.4);
    ctx.overlay.dataset.litCells = String(lit);
  },
};
