/** Splits a bar chart around zero: the 0 line draws, negative bars fall first, positive bars rise after.
 *  음수 막대는 주홍으로 떨어지고(in), 양수 막대는 잉크로 오른다(settle). 값 표는 막대 끝에. */
import { colorOf } from '../_shared/color.js';
import { line, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';
import { draw, growBar, plotBox, rangeOf } from './annotation-pin.js';
import { valueTags } from './aggregate-split.js';

const part = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name).filter((n) => !ctx.skipNodes.includes(n)));
const base = (nodes) => nodes.filter((node) => (node.dataset.state ?? 'base') === 'base');

export default {
  id: 'diverge-grow',
  family: 'data',
  role: 'enter',
  accepts: ['chart'],
  sources: ['bar-grow', 'change-arrows'],
  reduce: 'fade',
  params: { duration: { type: 'number', default: 2, min: 0.6, max: 3, doc: '전체 길이(u)' } },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      beat = ctx.beat,
      marks = part(ctx, 'mark').filter((m) => m.tagName.toLowerCase() !== 'path'),
      horizontal = beat.data.orient === 'h';
    const text = ['title', 'dek', 'unit', 'source'].flatMap((name) => base(part(ctx, name)));
    ctx.initial(text, { autoAlpha: 0, yPercent: 30 });
    tl.to(text, { autoAlpha: 1, yPercent: 0, duration: d * 0.2, ease: ctx.ease('settle') }, 0);
    // 0선: 렌더러 baseline이 있으면 그것을, 없으면 overlay에
    let zero = part(ctx, 'baseline')[0];
    if (zero) {
      zero.setAttribute('pathLength', '1');
      zero.style.strokeDasharray = '1 1';
      ctx.initial(zero, { strokeDashoffset: 1 });
      tl.to(zero, { strokeDashoffset: 0, duration: d * 0.2, ease: ctx.ease('inout') }, d * 0.1);
    } else {
      const box = plotBox(beat),
        range = rangeOf(beat.data.series),
        y = box.y + box.h - ((0 - range.min) / (range.max - range.min)) * box.h;
      zero = line(svgLayer(ctx), box.x - px(ctx, 40), y, box.x + box.w + px(ctx, 40), y, { stroke: colorOf(ctx, 'fg'), 'stroke-width': px(ctx, 2) });
      draw(tl, ctx, zero, { at: d * 0.1, duration: d * 0.2, ease: ctx.ease('inout') });
    }
    ctx.initial(part(ctx, 'axis'), { autoAlpha: 0 });
    const neg = marks.filter((m) => m.dataset.sign === 'neg'),
      pos = marks.filter((m) => m.dataset.sign !== 'neg');
    neg.forEach((m, i) => growBar(tl, ctx, m, { at: d * (0.3 + i * 0.04), duration: d * 0.25, ease: ctx.ease('in'), horizontal }));
    pos.forEach((m, i) =>
      growBar(tl, ctx, m, { at: d * (0.5 + (0.12 * i) / Math.max(1, pos.length)), duration: d * 0.25, ease: ctx.ease('settle'), horizontal }),
    );
    // 음수 막대는 막대 아래 값 표가 이름도 함께 단다(아래 이름표 자리를 막대가 차지하므로)
    const values = beat.data.series[0].values;
    const labels = part(ctx, 'label');
    ctx.initial(labels, { autoAlpha: 0 });
    tl.to(labels.filter((_, i) => !(values[i] < 0) || horizontal), { autoAlpha: 1, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.3);
    const tags = valueTags(ctx, beat, { named: !horizontal });
    ctx.initial(tags, { autoAlpha: 0 });
    tags.forEach((t, i) => {
      const isNeg = beat.data.series[0].values[i] < 0;
      tl.to(t, { autoAlpha: 1, duration: d * 0.12, ease: ctx.ease('out') }, d * (isNeg ? 0.52 : 0.72));
    });
    const notes = base(part(ctx, 'note'));
    notes.forEach((node) => {
      const i = Number(node.dataset.index),
        m = marks.find((x) => Number(x.dataset.index) === i);
      if (!m) return;
      const r = beat.anchor('mark', beat.part('mark').indexOf(m)).rect,
        nr = beat.anchor('note', beat.part('note').indexOf(node)).rect;
      // 음수 막대는 값 표 아래, 양수 막대는 값 표 위(막대 왼쪽 끝에 맞춤)
      const negative = m.dataset.sign === 'neg';
      const dx = r.x - nr.x,
        dy = negative ? r.y + r.h + px(ctx, 62) - nr.y : r.y - px(ctx, 62) - nr.h - nr.y;
      ctx.initial(node, { autoAlpha: 0, x: dx, y: dy });
      tl.to(node, { autoAlpha: 1, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.6);
    });
  },
};
