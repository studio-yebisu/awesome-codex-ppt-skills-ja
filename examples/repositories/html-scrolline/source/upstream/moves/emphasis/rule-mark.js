/** Draw a labeled comparison rule across a measured part. Used by zoom decks. */
import { colorOf } from '../_shared/color.js';
import { drawOn, line, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';

export default {
  id: 'rule-mark',
  family: 'emphasis',
  role: 'step',
  accepts: ['compare', 'photo', 'video', 'chart'],
  sources: ['line-draw', 'underline-draw', 'annotation-callout'],
  reduce: 'self',
  params: {
    part: { type: 'part', default: 'item', doc: '기준 part' },
    y: { type: 'number', default: 0.5, min: 0, max: 1, doc: 'part rect 높이 비율' },
    label: { type: 'string', default: '', doc: '선 끝 주석' },
    below: { type: 'boolean', default: true, doc: '선 아래 scrim 여부' },
    duration: { type: 'number', default: 1.2, min: 0.6, max: 2, doc: 'u' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      parts = ctx.beat.part(params.part),
      rects = parts.map((_, i) => ctx.beat.anchor(params.part, i).rect);
    if (!rects.length) return;
    const left = Math.min(...rects.map((r) => r.x)),
      right = Math.max(...rects.map((r) => r.x + r.w)),
      base = rects[0],
      y = base.y + params.y * base.h,
      accent = colorOf(ctx, 'accent');
    const svg = svgLayer(ctx),
      rule = line(svg, left, y, right, y, {
        stroke: accent,
        'stroke-width': px(ctx, 1.5),
        'stroke-dasharray': '6 6',
      });
    drawOn(tl, rule, { at: 0, duration: d * 0.55, ease: 'none' });
    if (params.label) {
      const label = document.createElement('div');
      label.className = 'sl-rule-mark__label';
      label.textContent = params.label;
      Object.assign(label.style, {
        position: 'absolute',
        left: `${right}px`,
        top: `${y}px`,
        color: accent,
        fontFamily: 'monospace',
      });
      ctx.overlay.append(label);
      ctx.initial(label, { autoAlpha: 0, x: -px(ctx, 8) });
      tl.to(label, { autoAlpha: 1, x: 0, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.4);
    }
    if (params.below) {
      const scrim = document.createElement('div');
      scrim.className = 'sl-rule-mark__scrim';
      Object.assign(scrim.style, {
        position: 'absolute',
        left: `${left}px`,
        top: `${y}px`,
        width: `${right - left}px`,
        height: `${Math.max(0, ctx.viewport.h - y)}px`,
        background: colorOf(ctx, 'scrim'),
        pointerEvents: 'none',
      });
      ctx.overlay.append(scrim);
      ctx.initial(scrim, { opacity: 0 });
      tl.to(scrim, { opacity: 0.35, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.8);
    }
  },
};
