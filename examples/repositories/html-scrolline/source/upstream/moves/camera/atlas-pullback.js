/** Final atlas pullback: rise off the last tile, tilt once to show the terrain's depth, settle flat on the whole map. */
import { driveCamera, lerp, lerpScale, tileTarget } from './arc-flight.js';

export default {
  id: 'atlas-pullback',
  family: 'camera',
  role: 'camera',
  accepts: ['*'],
  sources: ['zoom-to-detail', 'perspective-tilt', 'atmospheric-depth'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 3.2, min: 1.5, max: 5, doc: '전체 길이(u)' },
    bounds: {
      type: 'object',
      default: { x0: -0.6, y0: -0.6, x1: 6, y1: 4.6 },
      doc: '끝에 한 화면에 들어올 world 범위',
    },
    margin: { type: 'number', default: 0.06, min: 0, max: 0.2, doc: '범위 바깥 여백 비율' },
    tilt: { type: 'number', default: 6, min: 0, max: 10, doc: '물러나는 중 한 번 기울이는 각도(°)' },
    offsetY: { type: 'number', default: 0, min: -0.3, max: 0.3, doc: '끝 화면에서 지도를 위로 올리는 양(화면 높이 비율)' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const from = tileTarget(ctx.prev?.place, tileTarget(ctx.beat.place));
    const b = params.bounds;
    const fit = Math.min(1 / (b.x1 - b.x0), 1 / (b.y1 - b.y0)) * (1 - params.margin);
    // offsetY > 0 lifts the map up on screen (look-at moves down in world units)
    const to = { cx: (b.x0 + b.x1) / 2, cy: (b.y0 + b.y1) / 2 + params.offsetY / fit, s: fit };
    const out = ctx.gsap.parseEase(ctx.ease('inout')) ?? ((t) => t);
    const tilt = ctx.reduce ? 0 : params.tilt;
    driveCamera(tl, ctx, params.duration, (p) => {
      const e = out(p);
      // tilt rises with the pullback and is gone by 85%: the full map always lands face-on
      const lean = p >= 0.85 ? 0 : Math.sin(Math.PI * (p / 0.85)) ** 2;
      return {
        cx: lerp(from.cx, to.cx, e),
        cy: lerp(from.cy, to.cy, e),
        s: lerpScale(from.s, to.s, e),
        rx: tilt * lean,
        ry: 0,
      };
    });
  },
};
