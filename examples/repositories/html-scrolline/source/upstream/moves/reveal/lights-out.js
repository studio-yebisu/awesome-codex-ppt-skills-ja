/** Removes caption, then dims a media frame to a black-stage exit. */
export default {
  id: 'lights-out',
  family: 'reveal',
  role: 'exit',
  accepts: ['video', 'photo'],
  sources: ['dip-to-color', 'spotlight'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1, min: 0.4, max: 2, doc: '전체 길이(u)' },
    darkFloor: { type: 'number', default: 0.04, min: 0, max: 0.3, doc: 'darkFloor(안무 설명의 같은 이름)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const frame = ctx.skipParts.includes('frame')
      ? []
      : ctx.beat.part('frame').filter((n) => !ctx.skipNodes?.includes(n));
    const captions = ctx.skipParts.includes('caption')
      ? []
      : ctx.beat.part('caption').filter((n) => !ctx.skipNodes?.includes(n));
    if (ctx.reduce) {
      tl.to(frame, { autoAlpha: 0, duration: d, ease: ctx.ease('in') }, 0);
      return;
    }
    // exit는 처음 상태를 정하지 않는다(enter·step의 initial을 덮으면 caption이 처음부터 보임): fromTo로만 내린다
    const late = (vars) => ({ ...vars, immediateRender: false, lazy: false });
    tl.fromTo(
      captions,
      { autoAlpha: 1, y: 0 },
      late({ autoAlpha: 0, y: -8, duration: d * 0.3, ease: ctx.ease('in') }),
      0,
    );
    // filter를 직접 tween(onUpdate는 timeline.seek에서 불리지 않아 점프·export 때 밝기가 남는다)
    tl.fromTo(
      frame,
      { filter: 'brightness(1) saturate(1)' },
      late({
        filter: `brightness(${params.darkFloor}) saturate(0.6)`,
        duration: d * 0.6,
        ease: ctx.ease('in'),
      }),
      d * 0.1,
    );
    // 마지막은 투명 대신 완전 암전(brightness 0): autoAlpha를 exit 중간에 걸면 되감기 때 inline 상태가 갈린다
    tl.fromTo(
      frame,
      { filter: `brightness(${params.darkFloor}) saturate(0.6)` },
      late({ filter: 'brightness(0) saturate(0.6)', duration: d * 0.3, ease: ctx.ease('in') }),
      d * 0.7,
    );
  },
};
