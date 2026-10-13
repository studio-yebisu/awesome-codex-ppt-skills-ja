/** Keeps a product canvas fixed while its frame and captions hand over. Signature launch link. */
import { frameSeqOf, scrubTo } from '../_shared/media.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, beat, name) =>
  beat.part(name).filter((node) => !ctx.skipParts.includes(name) && !ctx.skipNodes?.includes(node));
export default {
  id: 'sticky-scrub-link',
  family: 'media',
  role: 'link',
  accepts: ['video'],
  sources: ['scroll-frame-scrub', 'frame-scrub', 'anchored-substitution'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.6, max: 3, doc: '전체 길이(u)' },
    from: { type: 'number', default: -1, min: -1, max: 1, doc: '시작 진행률(-1 = 0)' },
    to: { type: 'number', default: 1, min: 0, max: 1, doc: '끝 진행률' },
    captionOut: { type: 'number', default: 0.25, min: 0.1, max: 0.5, doc: 'A caption 퇴장 비율' },
    captionIn: { type: 'number', default: 0.6, min: 0.3, max: 0.9, doc: 'B caption 입장 비율' },
    swapAt: { type: 'number', default: 0.9, min: 0.5, max: 1, doc: 'frame 교체 비율' },
    bAt: { type: 'number', default: -1, min: -1, max: 1, doc: 'B frame 진행률(-1 = to)' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const d = params.duration,
      start = params.from < 0 ? 0 : params.from;
    const aCaption = usable(ctx, ctx.from, 'caption');
    const bCaption = usable(ctx, ctx.beat, 'caption');
    const bMedia = usable(ctx, ctx.beat, 'media');
    const aSeq = frameSeqOf(ctx.from),
      bSeq = frameSeqOf(ctx.beat);
    const { from, to } = ctx.handoff;
    const bProgress = params.bAt < 0 ? params.to : params.bAt;
    // 제품은 한 자리(두 beat 모두 full): 유령 복제 없이 A 캔버스가 돌고, swap 순간 같은 프레임의 B로 바뀐다.
    // B frame은 caption이 오를 때부터 보이되 B 캔버스는 swap까지 숨겨 A 캔버스가 비친다.
    ctx.initial(bCaption, { autoAlpha: 0, y: px(ctx, 24) });
    ctx.initial(to.node, { autoAlpha: 0 });
    ctx.initial(bMedia, { autoAlpha: 0 });
    // A caption의 처음 상태는 앞 move(enter·앞 link)가 정한다: initial로 덮지 않고 fromTo로 내린다
    tl.fromTo(
      aCaption,
      { autoAlpha: 1, y: 0 },
      {
        autoAlpha: 0,
        y: -px(ctx, 12),
        duration: d * params.captionOut,
        ease: ctx.ease('in'),
        immediateRender: false,
      },
      0,
    );
    scrubTo(tl, aSeq, { from: start, to: params.to, at: d * 0.05, duration: d * (params.swapAt - 0.05) });
    scrubTo(tl, bSeq, { from: bProgress, to: bProgress, at: 0, duration: d * 0.05 });
    tl.set(to.node, { autoAlpha: 1 }, d * params.captionIn);
    tl.to(
      bCaption,
      { autoAlpha: 1, y: 0, duration: d * (1 - params.captionIn), ease: ctx.ease('out') },
      d * params.captionIn,
    );
    tl.set(bMedia, { autoAlpha: 1 }, d * params.swapAt);
    tl.set(from.node, { autoAlpha: 0 }, d * params.swapAt);
    tl.set(to.node, { autoAlpha: 1 }, d);
    tl.set(from.node, { autoAlpha: 0 }, d);
  },
};
