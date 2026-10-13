/** Opening crane: low and tilted over a piece of the map, the camera rises and stands up on the title. */
import { driveCamera, lerp, lerpScale, lookAtVars, nearLayers, tileTarget } from './arc-flight.js';

export default {
  id: 'establish-crane',
  family: 'camera',
  role: 'camera',
  accepts: ['*'],
  sources: ['crane-tilt', 'perspective-tilt', 'atmospheric-depth'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 1, max: 4, doc: '전체 길이(u)' },
    tilt: { type: 'number', default: 10, min: 0, max: 12, doc: '시작 tilt 각도(°, ≤12)' },
    startScale: { type: 'number', default: 1.6, min: 1, max: 2.5, doc: '시작 배율(지형에 붙은 낮은 고도)' },
    lift: { type: 'number', default: 0.35, min: 0, max: 1, doc: '시작 시선이 목표보다 아래(화면 높이 비율)' },
    haze: { type: 'number', default: 0.5, min: 0, max: 1, doc: '시작 haze 층 아래 밀림(화면 높이 비율)' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const to = tileTarget(ctx.beat.place);
    const tilt = ctx.reduce ? 0 : params.tilt;
    const from = { cx: to.cx, cy: to.cy + params.lift, s: to.s * params.startScale };
    const rise = ctx.gsap.parseEase(ctx.ease('out')) ?? ((t) => t);
    const stand = ctx.gsap.parseEase(ctx.ease('inout')) ?? ((t) => t);
    const hazeY = ctx.reduce ? 0 : params.haze * ctx.viewport.h;
    const state = (p) => {
      const e = rise(p);
      // tilt holds through the first third (the oblique map piece), then the camera stands up
      const level = p < 0.3 ? 0 : stand(Math.min(1, (p - 0.3) / 0.6));
      return {
        cx: to.cx,
        cy: lerp(from.cy, to.cy, e),
        s: lerpScale(from.s, to.s, e),
        rx: tilt * (1 - level),
        ry: 0,
        hazeY: hazeY * (1 - e),
      };
    };
    const start = state(0);
    ctx.initial(ctx.stage.camera, lookAtVars(ctx.viewport, start));
    const near = nearLayers(ctx);
    if (near.length) ctx.initial(near, { x: 0, y: start.hazeY });
    driveCamera(tl, ctx, params.duration, state);
  },
};
