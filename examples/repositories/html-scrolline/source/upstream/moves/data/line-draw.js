/** Draws line series together from left to right, optionally carrying their names. */
import { colorOf } from '../_shared/color.js';
import { driveValue } from '../_shared/drive.js';
import { pointOnPolyline } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';

const part = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name));
const points = (node) =>
  (node.getAttribute('d')?.match(/-?\d*\.?\d+/g) ?? []).reduce((out, n, i, all) => {
    if (i % 2 === 0) out.push({ x: Number(n), y: Number(all[i + 1]) });
    return out;
  }, []);

export default {
  id: 'line-draw',
  family: 'data',
  role: 'enter',
  accepts: ['chart'],
  sources: ['line-draw', 'line-chart-race', 'annotation-tracking'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.6, max: 3.5, doc: '전체 길이(u)' },
    series: { type: 'integer', default: -1, min: -1, max: 8, doc: '그릴 series index(−1 = 전부)' },
    headLabels: { type: 'boolean', default: false, doc: '선 머리 이름표(범례 대체)' },
    labelOffset: { type: 'number', default: 16, min: 6, max: 40, doc: '이름표 간격(px)' },
    markPop: { type: 'boolean', default: true, doc: '머리가 지날 때 점 등장' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      marks = part(ctx, 'mark');
    const paths = marks.filter(
      (node) =>
        node.tagName?.toLowerCase() === 'path' &&
        (params.series < 0 || Number(node.dataset.series) === params.series),
    );
    const dots = marks.filter(
      (node) =>
        node.tagName?.toLowerCase() !== 'path' &&
        (params.series < 0 || Number(node.dataset.series) === params.series),
    );
    const axis = [...part(ctx, 'axis'), ...part(ctx, 'label')];
    ctx.initial(axis, { autoAlpha: 0 });
    tl.to(axis, { autoAlpha: 1, duration: d * 0.2, ease: ctx.ease('out') }, 0);
    paths.forEach((node) => {
      node.setAttribute('pathLength', '1');
      node.style.strokeDasharray = '1 1';
      ctx.initial(node, { strokeDashoffset: 1 });
      tl.to(node, { strokeDashoffset: 0, duration: d * 0.7, ease: 'none' }, d * 0.15);
    });
    dots.forEach((node) => {
      const ratio = Number(node.dataset.index) / Math.max(1, ctx.beat.data.categories?.length - 1);
      ctx.initial(node, { scale: params.markPop ? 0 : 1 });
      if (params.markPop)
        tl.to(node, { scale: 1, duration: d * 0.08, ease: ctx.ease('out') }, d * (0.15 + 0.7 * ratio));
    });
    if (params.headLabels)
      paths.forEach((node) => {
        const label = document.createElement('span'),
          pts = points(node),
          series = Number(node.dataset.series);
        label.textContent = ctx.beat.data.series?.[series]?.name ?? '';
        label.style.position = 'absolute';
        ctx.overlay.append(label);
        ctx.initial(label, { autoAlpha: 0 });
        driveValue(
          tl,
          (p) => {
            const q = pointOnPolyline(pts, p);
            label.style.left = `${Math.round(q.x * 1000) / 1000}px`;
            label.style.top = `${Math.round(q.y * 1000) / 1000}px`;
          },
          { from: 0, to: 1, at: d * 0.15, duration: d * 0.7, ease: 'none' },
        );
        tl.to(
          label,
          { autoAlpha: 1, x: px(ctx, params.labelOffset), duration: d * 0.2, ease: ctx.ease('out') },
          d * 0.8,
        );
      });
    const highlight = ctx.beat.data.highlight?.series;
    if (highlight !== undefined)
      paths
        .filter((n) => Number(n.dataset.series) === Number(highlight))
        .forEach((n) =>
          tl.to(n, { stroke: colorOf(ctx, 'accent'), duration: d * 0.2, ease: ctx.ease('out') }, d * 0.8),
        );
    const source = part(ctx, 'source');
    ctx.initial(source, { autoAlpha: 0 });
    tl.to(source, { autoAlpha: 1, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.8);
  },
};
