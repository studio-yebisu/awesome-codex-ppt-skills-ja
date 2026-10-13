/** Re-encodes a bar chart as a line of a new state on the same stage. Signature data move.
 *  단계 분리(staged-chart-transition): ① 앞 주석 퇴장 ② 막대가 꼭대기 점으로 접힘 ③ 단위 교체
 *  ④ 점이 새 축 값으로 이동 ⑤ 선이 점을 이음 ⑥ 제목 교체·끝점 강조. 축과 값이 동시에 움직이는 순간은 없다. */
import { colorOf } from '../_shared/color.js';
import { polyline, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';
import { draw, layers, overlaysOf, pointAt, swapLayers } from './annotation-pin.js';

const NS = 'http://www.w3.org/2000/svg';
const stateFor = (ctx) =>
  ctx.beat.data.states?.find((state) => state.name === ctx.step?.name) ?? ctx.beat.data.states?.[0] ?? {};

/** 상태의 선 점(화면 좌표). link가 같은 점을 다시 계산할 때도 쓴다. */
export function morphPoints(beat, state) {
  const series = state.series ?? beat.data.series;
  return series[0].values.map((v, i) => pointAt(beat, i, v, series));
}

export default {
  id: 'mark-morph',
  family: 'data',
  role: 'step',
  accepts: ['chart'],
  sources: ['chart-path-morph', 'axis-rescale', 'staged-chart-transition', 'line-draw'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 1, max: 4, doc: '전체 길이(u)' },
    dot: { type: 'number', default: 9, min: 3, max: 24, doc: '선 위 점 반지름(px, 1920 기준)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      R = ctx.reduce ? 0.001 : 1,
      state = stateFor(ctx),
      points = morphPoints(ctx.beat, state),
      marks = ctx.beat.part('mark').filter((m) => m.tagName.toLowerCase() !== 'path' && m.dataset.series === '0'),
      ink = colorOf(ctx, 'fg'),
      accent = colorOf(ctx, 'accent'),
      r = px(ctx, params.dot);
    // ① 앞 단계의 주석·값 표·계단은 먼저 퇴장
    const old = overlaysOf(ctx, ctx.beat.id, (key) => !key.includes(`:step:${ctx.step?.index}:`));
    const oldNotes = layers(ctx, ['note']).stale;
    tl.to([...old, ...oldNotes], { autoAlpha: 0, duration: d * 0.12 * R, ease: ctx.ease('in') }, 0);
    // ② 막대 → 꼭대기 점
    const svg = svgLayer(ctx);
    const dots = marks.map((m, i) => {
      const a = ctx.beat.anchor('mark', ctx.beat.part('mark').indexOf(m)).rect;
      const c = document.createElementNS(NS, 'circle');
      c.setAttribute('cx', String(points[i]?.x ?? a.x + a.w / 2));
      c.setAttribute('cy', String(a.y));
      c.setAttribute('r', String(r));
      c.setAttribute('fill', i === marks.length - 1 ? accent : ink);
      svg.append(c);
      return { c, top: a.y, to: points[i] };
    });
    ctx.initial(dots.map((x) => x.c), { autoAlpha: 0 });
    marks.forEach((m, i) => {
      const h = Number(m.getAttribute('height'));
      // fromTo: 앞 move(link의 막대 자라기)가 선언한 시작 상태를 덮지 않게 initial 대신 명시 시작값
      tl.fromTo(m, { attr: { height: h } }, { attr: { height: Math.min(h, 2) }, duration: d * 0.2 * R, ease: ctx.ease('in'), immediateRender: false }, d * (0.1 + (0.06 * i) / Math.max(1, marks.length)));
    });
    tl.to(dots.map((x) => x.c), { autoAlpha: 1, duration: d * 0.06 * R }, d * 0.22);
    tl.set(marks, { autoAlpha: 0 }, d * 0.32);
    // ③ 단위·축 교체(값은 아직 그대로)
    swapLayers(tl, ctx, d * 0.3, d * 0.16 * R, ['unit']);
    // ④ 점이 새 값으로(왼쪽부터 조금씩 늦게)
    dots.forEach((x, i) => {
      if (!x.to) return;
      tl.fromTo(
        x.c,
        { attr: { cy: x.top } },
        { attr: { cy: x.to.y }, duration: d * 0.24 * R, ease: ctx.ease('inout'), immediateRender: false },
        d * (0.4 + (0.1 * i) / Math.max(1, dots.length - 1)),
      );
    });
    // ⑤ 선
    const path = polyline(svg, points, {
      stroke: ink,
      'stroke-width': px(ctx, 5),
      'stroke-linejoin': 'round',
      'stroke-linecap': 'round',
    });
    svg.insertBefore(path, svg.firstChild);
    ctx.reduce
      ? tl.set(path, { strokeDashoffset: 0 }, 0)
      : draw(tl, ctx, path, { at: d * 0.66, duration: d * 0.22, ease: 'none' });
    // ⑥ 제목 교체, 끝점 강조, 끝점 주석은 점 오른쪽
    swapLayers(tl, ctx, d * 0.62, d * 0.2 * R, ['title', 'dek']);
    const end = dots.at(-1);
    if (end?.to)
      tl.to(end.c, { attr: { r: r * 1.7 }, duration: d * 0.1 * R, ease: ctx.ease('settle') }, d * 0.86);
    const { fresh } = layers(ctx, ['note']);
    fresh.forEach((node) => {
      const i = Number(node.dataset.index),
        p = points[i];
      if (!p) return;
      const nr = ctx.beat.anchor('note', ctx.beat.part('note').indexOf(node)).rect;
      const dx = p.x + r * 2 + px(ctx, 14) - nr.x,
        dy = p.y - nr.h / 2 - nr.y;
      ctx.initial(node, { autoAlpha: 0, x: dx - px(ctx, 10), y: dy, color: accent });
      tl.to(node, { autoAlpha: 1, x: dx, duration: d * 0.12 * R, ease: ctx.ease('settle') }, d * 0.86);
    });
  },
};
