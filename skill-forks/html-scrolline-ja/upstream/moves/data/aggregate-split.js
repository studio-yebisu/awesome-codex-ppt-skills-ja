/** Grows one stacked total bar, then splits its segments into the chart's own bars.
 *  합계 막대(조각마다 범주, 강조 범주가 맨 아래)가 가운데에서 자라고 합계 값이 붙는다.
 *  조각이 제 범주 자리로 미끄러져 기준선에 내려앉으며 차트 축척으로 늘고, 실제 막대·값 표가 넘겨받는다. */
import { colorOf } from '../_shared/color.js';
import { px } from '../_shared/timeline.js';
import { fmt, plotBox, tag } from './annotation-pin.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name) ? [] : ctx.beat.part(name).filter((node) => !ctx.skipNodes.includes(node));
const base = (nodes) => nodes.filter((node) => (node.dataset.state ?? 'base') === 'base');

/** 막대마다 값 표(강조는 크게·주홍). */
export function valueTags(ctx, beat, { unit = beat.data.unit ?? '', hi = beat.data.highlight?.index, named = false } = {}) {
  const values = beat.data.series[0].values,
    marks = beat.part('mark').filter((m) => m.dataset.series === '0');
  const horizontal = beat.data.orient === 'h';
  return marks.map((m, i) => {
    const r = beat.anchor('mark', beat.part('mark').indexOf(m)).rect,
      v = values[i],
      neg = v < 0,
      strong = i === hi;
    const value = `${v < 0 ? '−' : ''}${fmt(Math.abs(v), Number.isInteger(v) ? 0 : 1)}${unit}`;
    const text = named && neg ? `${beat.data.categories[i]} ${value}` : value;
    const top = plotBox(beat).y;
    // 플롯 맨 위에 닿은 세로 막대는 값 표를 막대 안쪽 위에(위 dek와 겹치지 않게)
    if (!horizontal && !neg && r.y - top < px(ctx, 44))
      return tag(ctx, text, { x: r.x + r.w / 2, y: r.y + px(ctx, 14), align: 'center', valign: 'top', size: strong ? 34 : 26, weight: strong ? 800 : 600, color: 'bg' });
    const at = horizontal
      ? { x: neg ? r.x - px(ctx, 12) : r.x + r.w + px(ctx, 12), y: r.y + r.h / 2, align: neg ? 'right' : 'left', valign: 'middle' }
      : { x: r.x + r.w / 2, y: neg ? r.y + r.h + px(ctx, 10) : r.y - px(ctx, 10), align: 'center', valign: neg ? 'top' : 'bottom' };
    return tag(ctx, text, { ...at, size: strong ? 34 : 26, weight: strong ? 800 : 600, color: strong ? 'accent' : 'fg' });
  });
}

export default {
  id: 'aggregate-split',
  family: 'data',
  role: 'enter',
  accepts: ['chart'],
  sources: ['aggregate-split-merge', 'stacked-grouped-transition'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 2.4, min: 0.8, max: 4, doc: '전체 길이(u)' },
    totalLabel: { type: 'boolean', default: true, doc: '합계 값 표' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      beat = ctx.beat,
      box = plotBox(beat),
      marks = usable(ctx, 'mark').filter((m) => m.dataset.series === '0'),
      values = beat.data.series[0].values,
      total = values.reduce((s, v) => s + Math.max(0, v), 0) || 1,
      hi = beat.data.highlight?.index ?? 0;
    const rects = marks.map((m) => beat.anchor('mark', beat.part('mark').indexOf(m)).rect);
    const w = rects[0]?.w ?? px(ctx, 120),
      cx = box.x + box.w / 2;
    // 쌓는 순서: 강조 범주가 맨 아래, 나머지는 원래 순서
    const order = [hi, ...values.map((_, i) => i).filter((i) => i !== hi)];
    let y = box.y + box.h;
    const pieces = order.map((i) => {
      const h = (values[i] / total) * box.h;
      y -= h;
      const node = document.createElement('i');
      Object.assign(node.style, {
        position: 'absolute',
        left: `${cx - w / 2}px`,
        top: `${y}px`,
        width: `${w}px`,
        height: `${h}px`,
        backgroundColor: colorOf(ctx, i === hi ? 'accent' : 'fg'),
        boxShadow: `inset 0 ${px(ctx, 3)}px 0 ${colorOf(ctx, 'bg')}`,
      });
      ctx.overlay.append(node);
      return { i, node, y, h };
    });
    const stackTop = pieces.at(-1).y;
    ctx.initial(pieces.map((p) => p.node), { clipPath: 'inset(100% 0% 0% 0%)', autoAlpha: 1 });
    tl.to(pieces.map((p) => p.node), { clipPath: 'inset(0% 0% 0% 0%)', duration: d * 0.12, ease: ctx.ease('settle'), stagger: d * 0.05 }, d * 0.02);
    const axis = [...usable(ctx, 'axis'), ...usable(ctx, 'baseline')];
    ctx.initial(axis, { autoAlpha: 0 });
    tl.to(axis, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, 0);
    if (params.totalLabel) {
      const label = tag(ctx, `${fmt(total)}${beat.data.unit ?? ''}`, { x: cx, y: stackTop - px(ctx, 14), align: 'center', valign: 'bottom', size: 40, weight: 800, color: 'fg' });
      ctx.initial(label, { autoAlpha: 0 });
      tl.to(label, { autoAlpha: 1, duration: d * 0.08, ease: ctx.ease('out') }, d * 0.2);
      tl.to(label, { autoAlpha: 0, duration: d * 0.08, ease: ctx.ease('in') }, d * 0.4);
    }
    // 조각 → 제 자리 막대(축척도 차트 것으로)
    pieces.forEach((p, k) => {
      const r = rects[p.i];
      if (!r) return;
      tl.to(
        p.node,
        { left: r.x, top: r.y, width: r.w, height: r.h, duration: d * 0.3, ease: ctx.ease('inout') },
        d * (0.42 + 0.06 * k),
      );
    });
    ctx.initial(marks, { autoAlpha: 0 });
    tl.set(marks, { autoAlpha: 1 }, d * 0.9);
    tl.set(pieces.map((p) => p.node), { autoAlpha: 0 }, d * 0.9);
    const labels = usable(ctx, 'label');
    ctx.initial(labels, { autoAlpha: 0 });
    tl.to(labels, { autoAlpha: 1, duration: d * 0.12, ease: ctx.ease('out') }, d * 0.7);
    const tags = valueTags(ctx, beat);
    ctx.initial(tags, { autoAlpha: 0, y: px(ctx, 8) });
    tl.to(tags, { autoAlpha: 1, y: 0, duration: d * 0.1, ease: ctx.ease('settle'), stagger: d * 0.02 }, d * 0.82);
    const text = ['title', 'dek', 'unit', 'note', 'source'].flatMap((name) => base(usable(ctx, name)));
    ctx.initial(text, { autoAlpha: 0, yPercent: 30 });
    tl.to(text, { autoAlpha: 1, yPercent: 0, duration: d * 0.16, ease: ctx.ease('settle') }, d * 0.05);
  },
};
