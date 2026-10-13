/** Scrubs an exploded video frame, then draws one anchored annotation. */
import { colorOf } from '../_shared/color.js';
import { frameSeqOf, scrubTo } from '../_shared/media.js';
import { drawOn, line, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';

const TAG = 'calloutOf';

export default {
  id: 'scrub-callouts',
  family: 'media',
  role: 'step',
  accepts: ['video'],
  sources: ['frame-scrub', 'annotation-tracking', 'annotation-callout', 'exploded-assembly'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1, min: 0.5, max: 2.5, doc: '전체 길이(u)' },
    from: {
      type: 'number',
      default: -1,
      min: -1,
      max: 1,
      doc: '시작 진행률(-1 = 앞 step의 to, 첫 step은 0)',
    },
    to: { type: 'number', default: 1, min: 0, max: 1, doc: '끝 진행률' },
    anchor: { type: 'object', default: { x: 0.62, y: 0.4 }, doc: 'frame 정규화 anchor' },
    label: { type: 'string', default: '부품', doc: '콜아웃 라벨' },
    note: { type: 'string', default: '부품 설명', doc: '콜아웃 설명' },
    side: { type: 'enum', default: 'left', values: ['left', 'right'], doc: '라벨 방향' },
    reach: { type: 'number', default: 0.34, min: 0, max: 1, doc: '지시선 끝(라벨 쪽) x, frame 정규화' },
    dimOthers: { type: 'boolean', default: true, doc: 'anchor 밖 영역 dim 여부' },
    captionOut: { type: 'boolean', default: true, doc: '첫 step에서 beat caption을 내림(라벨과 칼럼 공유)' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    // anchor는 그려진 프레임(media 캔버스) 기준: 세로 화면에선 캔버스가 frame보다 작게 위쪽에 앉는다
    const d = params.duration,
      rect = (ctx.beat.part('media').length ? ctx.beat.anchor('media') : ctx.beat.anchor('frame')).rect;
    const x = rect.x + rect.w * params.anchor.x,
      y = rect.y + rect.h * params.anchor.y;
    const left = params.side === 'left';
    const end =
      rect.x +
      rect.w * (left ? Math.min(params.reach, params.anchor.x) : Math.max(params.reach, params.anchor.x));
    const gap = px(ctx, 18);
    const accent = colorOf(ctx, 'accent');
    // 앞 step이 남긴 콜아웃(같은 beat)은 이 step이 시작하면 물러난다: 라벨은 그 프레임 구간에서만 산다.
    const previous = [...(ctx.stage.overlay?.querySelectorAll?.(`[data-callout-of="${ctx.beat.id}"]`) ?? [])];
    const index = ctx.step?.index ?? 0;
    const from = params.from >= 0 ? params.from : (ctx.beat.data.steps?.[index - 1]?.params?.to ?? 0);
    // 세로 화면: 옆에 라벨 둘 폭이 없어 지시선은 아래로 내려 프레임 밑 왼쪽 정렬 라벨에 닿는다
    const below = ctx.viewport.portrait;
    const labelTop = rect.y + rect.h + px(ctx, 40);
    const svg = svgLayer(ctx),
      stroke = below
        ? line(svg, x, labelTop - px(ctx, 16), x, y, {
            stroke: accent,
            'stroke-width': Math.max(1.5, px(ctx, 2)),
          })
        : line(svg, end, y, x, y, { stroke: accent, 'stroke-width': Math.max(1.5, px(ctx, 2)) });
    const dot = document.createElement('i'),
      label = document.createElement('div'),
      note = document.createElement('div');
    dot.className = 'sl-scrub-callouts__dot';
    label.className = 'sl-scrub-callouts__label';
    note.className = 'sl-scrub-callouts__note';
    label.textContent = params.label;
    note.textContent = params.note;
    const side = below
      ? { left: `${px(ctx, 48)}px`, textAlign: 'left' }
      : left
        ? { right: `${ctx.viewport.w - (end - gap)}px`, textAlign: 'right' }
        : { left: `${end + gap}px`, textAlign: 'left' };
    Object.assign(dot.style, { position: 'absolute', left: `${x}px`, top: `${y}px`, display: 'block' });
    Object.assign(
      label.style,
      below
        ? { position: 'absolute', top: `${labelTop}px`, ...side }
        : { position: 'absolute', bottom: `${ctx.viewport.h - y + px(ctx, 4)}px`, ...side },
    );
    Object.assign(note.style, {
      position: 'absolute',
      top: `${below ? labelTop + px(ctx, 52) : y + px(ctx, 10)}px`,
      ...side,
    });
    const group = [svg, dot, label, note];
    if (params.dimOthers) {
      const scrim = document.createElement('div');
      scrim.className = 'sl-scrub-callouts__scrim';
      Object.assign(scrim.style, {
        position: 'absolute',
        inset: '0',
        pointerEvents: 'none',
        background: `radial-gradient(ellipse 34% 26% at ${(x / ctx.viewport.w) * 100}% ${(y / ctx.viewport.h) * 100}%, transparent 0%, rgba(0,0,0,.45) 100%)`,
      });
      ctx.overlay.prepend(scrim);
      group.unshift(scrim);
    }
    group.forEach((node) => (node.dataset[TAG] = ctx.beat.id));
    ctx.overlay.append(dot, label, note);
    ctx.initial(
      group.filter((n) => n !== svg),
      { autoAlpha: 0 },
    );
    ctx.initial(label, { y: px(ctx, 12) });
    ctx.initial(note, { y: px(ctx, 8) });
    if (previous.length) {
      // fromTo + immediateRender false: 앞 step의 initial(숨김)을 덮지 않는다
      tl.fromTo(
        previous,
        { autoAlpha: 1 },
        { autoAlpha: 0, duration: d * 0.2, ease: ctx.ease('in'), immediateRender: false },
        0,
      );
    } else if (params.captionOut) {
      const caption = ctx.beat.part('caption').filter((n) => !ctx.skipParts.includes('caption'));
      tl.fromTo(
        caption,
        { autoAlpha: 1 },
        { autoAlpha: 0, duration: d * 0.25, ease: ctx.ease('in'), immediateRender: false },
        0,
      );
    }
    scrubTo(tl, frameSeqOf(ctx.beat), { from, to: params.to, at: 0, duration: d * 0.7 });
    drawOn(tl, stroke, { at: d * 0.55, duration: d * 0.25, ease: 'none' });
    tl.to(dot, { autoAlpha: 1, duration: d * 0.08, ease: ctx.ease('out') }, d * 0.72);
    tl.to(label, { autoAlpha: 1, y: 0, duration: d * 0.25, ease: ctx.ease('out') }, d * 0.65);
    tl.to(note, { autoAlpha: 1, y: 0, duration: d * 0.25, ease: ctx.ease('out') }, d * 0.72);
    if (params.dimOthers)
      tl.to(group[0], { autoAlpha: 1, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.6);
  },
};
