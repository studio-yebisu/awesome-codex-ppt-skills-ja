/** Pins chart notes to their marks with leader geometry. Signature(data).
 *  shape: pin(짧은 리더선) · stairs(앞 막대 꼭대기에서 이 막대까지 계단, 오르막 옆 주석) · gap(두 계열 사이 괄호, 오른쪽 주석).
 *  주석 글자는 렌더러가 그린 상태 층 note 요소를 그대로 옮겨 쓴다(정지점 DOM = 보이는 글자). */
import { colorOf } from '../_shared/color.js';
import { line, path, svgLayer, drawOn } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';

/* ── data family 공용 도구(같은 family move만 import) ─────────────────── */
export const DISPLAY_FONT = '"Noto Serif KR", "Nanum Myeongjo", serif';
export const TEXT_FONT = '"Pretendard Variable", Pretendard, system-ui, sans-serif';

/** 렌더러 BOX(viewBox 1600×900 안 160..1460 × 160..760)를 화면 좌표로. */
export function plotBox(beat) {
  const r = beat.anchor('plot').rect,
    s = r.w / 1600;
  return { x: r.x + 160 * s, y: r.y + 160 * s, w: 1300 * s, h: 600 * s, s, rect: r };
}
/** 렌더러와 같은 값 범위. */
export function rangeOf(seriesList) {
  const values = seriesList.flatMap((item) => item.values);
  const min = Math.min(0, ...values),
    max = Math.max(0, ...values);
  return max === min ? { min: 0, max: 1 } : { min, max };
}
/** 세로 차트의 범주 i·값 v 화면 점. */
export function pointAt(beat, i, v, seriesList = beat.data.series) {
  const box = plotBox(beat),
    range = rangeOf(seriesList),
    n = beat.data.categories.length;
  return {
    x: box.x + (n > 1 ? (i * box.w) / (n - 1) : 0),
    y: box.y + box.h - ((v - range.min) / (range.max - range.min)) * box.h,
  };
}
/** 상태 층 글자: ctx.step 이름 층과 그 밖 층. */
export function layers(ctx, names = ['title', 'dek', 'unit', 'note'], beat = ctx.beat) {
  const all = names.flatMap((name) => beat.part(name));
  const now = ctx.step?.name;
  return {
    fresh: all.filter((node) => node.dataset.state === now),
    stale: all.filter((node) => node.dataset.state !== now),
  };
}
/** 상태 층 교대: 지난 층이 위로 빠진 다음 새 층이 아래서 올라온다(두 제목이 겹쳐 보이는 순간 없음). [at, at + duration] 안. */
export function swapLayers(tl, ctx, at, duration, names) {
  const { fresh, stale } = layers(ctx, names);
  if (!fresh.length) return;
  ctx.initial(fresh, { autoAlpha: 0, yPercent: 30 });
  tl.to(stale, { autoAlpha: 0, yPercent: -30, duration: duration * 0.4, ease: ctx.ease('in') }, at);
  tl.to(fresh, { autoAlpha: 1, yPercent: 0, duration: duration * 0.55, ease: ctx.ease('settle') }, at + duration * 0.45);
}
/** overlay 글자표(값·이름표). align = 'left'|'center'|'right', valign = 'top'|'middle'|'bottom'.
 *  바깥 span(위치·GSAP 대상) 안에 정렬용 span을 둔다: GSAP가 transform을 쓰면 바깥 요소의 CSS translate를 지우기 때문. */
export function tag(ctx, text, { x, y, align = 'left', valign = 'middle', size = 26, weight = 600, color = 'fg', font = TEXT_FONT } = {}) {
  const node = document.createElement('span');
  node.className = 'sl-data-tag';
  const inner = document.createElement('span');
  inner.textContent = text;
  const tx = align === 'center' ? '-50%' : align === 'right' ? '-100%' : '0';
  const ty = valign === 'middle' ? '-50%' : valign === 'bottom' ? '-100%' : '0';
  Object.assign(inner.style, { position: 'absolute', left: '0', top: '0', translate: `${tx} ${ty}`, whiteSpace: 'nowrap' });
  node.append(inner);
  Object.assign(node.style, {
    position: 'absolute',
    left: `${x}px`,
    top: `${y}px`,
    width: '0',
    height: '0',
    fontFamily: font,
    fontWeight: String(weight),
    fontSize: `${px(ctx, size)}px`,
    lineHeight: '1.1',
    fontVariantNumeric: 'tabular-nums',
    color: colorOf(ctx, color),
  });
  ctx.overlay.append(node);
  return node;
}
/** 글자표 안 글자를 바꿀 때 쓰는 안쪽 span. */
export const tagText = (node) => node.firstElementChild ?? node;
/** SVG 막대를 기준선에서 자라게(속성 tween: GSAP transform은 CSS scale·translate를 지우므로 쓰지 않음). */
export function growBar(tl, ctx, m, { at, duration, ease, horizontal = false }) {
  const a = (k) => Number(m.getAttribute(k));
  const x = a('x'),
    y = a('y'),
    w = a('width'),
    h = a('height'),
    neg = m.dataset.sign === 'neg';
  const start = horizontal ? (neg ? { x: x + w, width: 0 } : { width: 0 }) : neg ? { height: 0 } : { y: y + h, height: 0 };
  ctx.initial(m, { attr: start });
  tl.to(m, { attr: horizontal ? { x, width: w } : { y, height: h }, duration, ease }, at);
}
/** 앞 move들이 이 beat(또는 from beat)에 남긴 overlay 내용. */
export function overlaysOf(ctx, beatId, filter = () => true) {
  return [...(ctx.stage.overlay?.children ?? [])].filter(
    (node) => node !== ctx.overlay && node.dataset.overlayKey?.startsWith(`${beatId}:`) && filter(node.dataset.overlayKey),
  ).flatMap((node) => [...node.children]);
}
/** drawOn + 시작값 선언(되감기 때 시작값이 인라인으로 새로 써지지 않게). */
export function draw(tl, ctx, node, opts) {
  ctx.initial(node, { strokeDashoffset: 1 - (opts.from ?? 0) });
  drawOn(tl, node, opts);
}
export const fmt = (v, digits = 0) =>
  new Intl.NumberFormat('ko', { minimumFractionDigits: digits, maximumFractionDigits: digits }).format(v);

/* ── move ───────────────────────────────────────────────────────────── */
const notesFor = (ctx) => {
  const name = ctx.step?.name;
  const state = name ? ctx.beat.data.states?.find((s) => s.name === name) : null;
  return state?.notes ?? ctx.beat.data.notes ?? [];
};
const seriesIndex = (data, s) =>
  typeof s === 'number' ? s : Math.max(0, (data.series ?? []).findIndex((item) => item.name === s));

export default {
  id: 'annotation-pin',
  family: 'data',
  role: 'step',
  accepts: ['chart'],
  sources: ['annotation-callout', 'annotation-tracking', 'underline-draw'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.4, max: 3, doc: '전체 길이(u)' },
    shape: { type: 'enum', default: 'pin', values: ['pin', 'stairs', 'gap'], doc: '리더 모양' },
    offset: { type: 'number', default: 28, min: 12, max: 80, doc: '주석 거리(px)' },
    stagger: { type: 'number', default: 0.08, min: 0, max: 0.4, doc: '항목 간 시차(u, 넘치면 줄임)' },
    against: { type: 'integer', default: 1, min: 0, max: 8, doc: 'gap: 비교 계열 index' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      data = ctx.beat.data,
      notes = [...notesFor(ctx)].sort((a, b) => a.index - b.index),
      nodes = ctx.beat.part('note').filter((n) => n.dataset.state === (ctx.step?.name ?? 'base')),
      svg = svgLayer(ctx),
      ink = colorOf(ctx, 'accent'),
      sw = px(ctx, 3),
      n = Math.max(1, notes.length),
      each = Math.min(params.stagger, (d * 0.45) / n),
      span = d * 0.4;
    // 앞 상태 주석은 회색으로 물러남
    ctx.beat.part('note').filter((node) => !nodes.includes(node)).forEach((node) =>
      tl.to(node, { color: colorOf(ctx, 'fg-muted'), opacity: 0.35, duration: d * 0.2 }, 0),
    );
    swapLayers(tl, ctx, 0, d * 0.4, ['title', 'dek', 'unit']);
    const marks = ctx.beat.part('mark');
    const markOf = (note) =>
      marks.find(
        (m) =>
          m.tagName.toLowerCase() !== 'path' &&
          Number(m.dataset.index) === note.index &&
          Number(m.dataset.series) === seriesIndex(data, note.series ?? 0),
      );
    const rectOf = (m) => ctx.beat.anchor('mark', marks.indexOf(m)).rect;
    if (params.shape === 'stairs') {
      const first = Math.min(...notes.map((note) => note.index));
      marks.forEach((m) => {
        const i = Number(m.dataset.index);
        ctx.initial(m, { fill: globalThis.getComputedStyle?.(m).fill || colorOf(ctx, 'fg') });
        if (i < first - 1)
          tl.to(m, { fill: colorOf(ctx, 'rule'), duration: d * 0.3, ease: ctx.ease('out') }, 0);
      });
    }
    notes.forEach((note, k) => {
      const mark = markOf(note),
        node = nodes.find((x) => Number(x.dataset.index) === note.index);
      if (!mark) return;
      const r = rectOf(mark),
        at = d * 0.1 + k * each;
      let want; // 주석 왼쪽 위 목표점과 정렬
      if (params.shape === 'stairs') {
        const prev = marks.find(
          (m) => Number(m.dataset.index) === note.index - 1 && m.dataset.series === mark.dataset.series,
        );
        const p = prev ? rectOf(prev) : r;
        const g = path(
          svg,
          `M ${p.x + p.w / 2} ${p.y} L ${r.x} ${p.y} L ${r.x} ${r.y} L ${r.x + r.w / 2} ${r.y}`,
          { stroke: ink, 'stroke-width': sw, 'stroke-linejoin': 'miter' },
        );
        ctx.reduce
          ? tl.set(g, { strokeDashoffset: 0 }, at)
          : draw(tl, ctx, g, { at, duration: span, ease: ctx.ease('inout') });
        want = { x: r.x - px(ctx, 10), y: (p.y + r.y) / 2, align: 'right' };
      } else if (params.shape === 'gap') {
        const other = marks.find(
          (m) =>
            m.tagName.toLowerCase() !== 'path' &&
            Number(m.dataset.index) === note.index &&
            Number(m.dataset.series) === params.against,
        );
        const o = other ? rectOf(other) : r;
        // 괄호는 두 점 왼쪽(선 끝 이름표 자리를 비움), 주석은 괄호 왼쪽에 오른쪽 맞춤
        const x = Math.min(r.x, o.x) - px(ctx, params.offset);
        const y1 = r.y + r.h / 2,
          y2 = o.y + o.h / 2,
          tick = px(ctx, 14);
        const g = path(svg, `M ${x + tick} ${y1} L ${x} ${y1} L ${x} ${y2} L ${x + tick} ${y2}`, {
          stroke: ink,
          'stroke-width': sw,
        });
        ctx.reduce
          ? tl.set(g, { strokeDashoffset: 0 }, at)
          : draw(tl, ctx, g, { at, duration: span, ease: ctx.ease('inout') });
        want = { x: x - px(ctx, 18), y: (y1 + y2) / 2, align: 'right' };
      } else {
        const x1 = r.x + r.w / 2,
          y1 = r.y,
          x2 = x1 + px(ctx, params.offset),
          y2 = y1 - px(ctx, params.offset);
        const g = line(svg, x1, y1, x2, y2, { stroke: ink, 'stroke-width': px(ctx, 2) });
        ctx.reduce
          ? tl.set(g, { strokeDashoffset: 0 }, at)
          : draw(tl, ctx, g, { at, duration: span * 0.6, ease: ctx.ease('out') });
        want = { x: x2 + px(ctx, 8), y: y2, align: 'left' };
      }
      if (node) {
        const nr = ctx.beat.anchor('note', ctx.beat.part('note').indexOf(node)).rect;
        const left = want.align === 'right' ? want.x - nr.w : want.x;
        const dx = left - nr.x,
          dy = want.y - nr.h / 2 - nr.y;
        ctx.initial(node, { autoAlpha: 0, x: dx + (want.align === 'right' ? -px(ctx, 10) : px(ctx, 10)), y: dy, color: ink });
        tl.to(node, { autoAlpha: 1, x: dx, duration: span * 0.6, ease: ctx.ease("settle") }, at + span * 0.3);
      }
      const hi = data.highlight?.index === note.index;
      if (params.shape !== 'stairs') ctx.initial(mark, { fill: globalThis.getComputedStyle?.(mark).fill || colorOf(ctx, 'fg') });
      if (params.shape !== 'gap' && !hi)
        tl.to(mark, { fill: params.shape === 'stairs' ? colorOf(ctx, 'fg') : ink, duration: d * 0.3, ease: ctx.ease('out') }, at);
    });
  },
};
