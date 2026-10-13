/** A single chart mark introduces its annotation and chart copy.
 *  점(마크)은 보통 앞 link가 이미 놓는다(skipNodes). 이 move는 리더선 → 주석 → 제목 순으로 약속(점 1개 = 값)을 세운다. */
import { colorOf } from '../_shared/color.js';
import { line, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';
import { draw } from './annotation-pin.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name) ? [] : ctx.beat.part(name).filter((node) => !ctx.skipNodes.includes(node));
const base = (nodes) => nodes.filter((node) => (node.dataset.state ?? 'base') === 'base');
export default {
  id: 'dot-seed',
  family: 'data',
  role: 'enter',
  accepts: ['chart'],
  sources: ['scale-pop', 'annotation-callout'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.5, max: 2.4, doc: '전체 길이(u)' },
    noteSide: { type: 'enum', default: 'right', values: ['left', 'right', 'top'], doc: '주석이 놓일 방향' },
    gap: { type: 'number', default: 44, min: 12, max: 160, doc: '점과 주석 사이(px, 1920 기준)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      mark = usable(ctx, 'mark')[0],
      note = base(usable(ctx, 'note'))[0];
    if (mark) {
      ctx.initial(mark, { autoAlpha: 0 });
      tl.to(mark, { autoAlpha: 1, duration: d * 0.25, ease: ctx.ease('settle') }, 0);
    }
    const title = base(usable(ctx, 'title')),
      dek = base(usable(ctx, 'dek')),
      rest = usable(ctx, 'source');
    [title, dek].forEach((nodes, i) => {
      if (!nodes.length) return;
      ctx.initial(nodes, { autoAlpha: 0, yPercent: 30 });
      tl.to(nodes, { autoAlpha: 1, yPercent: 0, duration: d * 0.35, ease: ctx.ease('settle') }, d * (0.05 + i * 0.12));
    });
    if (note) {
      // 주석은 점 옆 gap 자리로 옮겨 붙인다(렌더러 기본 자리는 마크 오른쪽 위 1%)
      const m = ctx.beat.anchor('mark').rect,
        b = ctx.beat.anchor('note', ctx.beat.part('note').indexOf(note)).rect,
        gap = px(ctx, params.gap),
        side = params.noteSide;
      const cx = m.x + m.w / 2,
        cy = m.y + m.h / 2;
      const want =
        side === 'left'
          ? { x: m.x - gap - b.w, y: cy - b.h / 2 }
          : side === 'top'
            ? { x: cx - b.w / 2, y: m.y - gap - b.h }
            : { x: m.x + m.w + gap, y: cy - b.h / 2 };
      const dx = want.x - b.x,
        dy = want.y - b.y;
      const a =
        side === 'left'
          ? [m.x - px(ctx, 8), cy, want.x + b.w + px(ctx, 10), cy]
          : side === 'top'
            ? [cx, m.y - px(ctx, 8), cx, want.y + b.h + px(ctx, 6)]
            : [m.x + m.w + px(ctx, 8), cy, want.x - px(ctx, 12), cy];
      const leader = line(svgLayer(ctx), ...a, { stroke: colorOf(ctx, 'fg'), 'stroke-width': px(ctx, 2) });
      draw(tl, ctx, leader, { at: d * 0.35, duration: d * 0.25, ease: ctx.ease('out') });
      const slide = px(ctx, side === 'left' ? -12 : 12);
      ctx.initial(note, { autoAlpha: 0, x: dx + (side === 'top' ? 0 : slide), y: dy + (side === 'top' ? px(ctx, 12) : 0) });
      tl.to(note, { autoAlpha: 1, x: dx, y: dy, duration: d * 0.35, ease: ctx.ease('settle') }, d * 0.5);
    }
    if (rest.length) {
      ctx.initial(rest, { autoAlpha: 0 });
      tl.to(rest, { autoAlpha: 1, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.6);
    }
  },
};
