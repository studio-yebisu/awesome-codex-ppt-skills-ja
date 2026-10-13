/** Cool and recede completed content. Used by canvas and data decks. */
import { colorOf } from '../_shared/color.js';

export default {
  id: 'recede',
  family: 'emphasis',
  role: 'exit',
  accepts: ['*'],
  sources: ['chart-filter-fade', 'fade-slide', 'fade', 'atmospheric-depth'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.9, min: 0.3, max: 2, doc: '전체 길이(u)' },
    to: { type: 'number', default: 0, min: 0, max: 0.6, doc: '끝 opacity(다녀온 곳)' },
    drift: { type: 'number', default: 0, min: 0, max: 0.2, doc: '위로 빠지는 양(화면 높이 비율)' },
    scaleTo: { type: 'number', default: 1, min: 0.95, max: 1, doc: '끝 scale' },
    cool: { type: 'boolean', default: true, doc: '색을 rule·fg-muted로 식힘' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      all = Object.values(ctx.beat.parts)
        .flat()
        .filter(
          (node) => !ctx.skipParts.includes(node.dataset.part) && !(ctx.skipNodes ?? []).includes(node),
        );
    if (params.cool)
      tl.to(all, { color: colorOf(ctx, 'fg-muted'), duration: d * 0.4, ease: ctx.ease('out') }, 0);
    tl.to(all, { scale: params.scaleTo, duration: d * 0.6, ease: ctx.ease('inout') }, 0);
    const primary = ctx.beat.part(ctx.beat.primary),
      title = ctx.beat.part('title'),
      lead = [...new Set([...primary, ...title])];
    // 결론(primary·title)은 위로 빠지며 흐려지고, 나머지 part(dek·note·source·unit)와 이 beat의 move overlay
    // (주석·값 라벨)도 같은 끝 opacity로. 겹친 part는 바깥 것만(opacity가 곱해지지 않게).
    const rest = [...all.filter((node) => !lead.includes(node)), ...(ctx.overlaysOf?.(ctx.beat) ?? [])],
      outer = rest.filter(
        (node) =>
          !rest.some((other) => other !== node && other.contains(node)) && !lead.some((l) => l.contains(node)),
      );
    tl.to(
      lead,
      { y: -params.drift * ctx.viewport.h, opacity: params.to, duration: d * 0.8, ease: ctx.ease('in') },
      d * 0.2,
    );
    if (outer.length) tl.to(outer, { opacity: params.to, duration: d * 0.8, ease: ctx.ease('in') }, d * 0.2);
  },
};
