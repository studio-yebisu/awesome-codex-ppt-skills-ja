/** Map-to-map camera flight: take off (altitude), bank toward the heading, descend level onto the tile. */

/**
 * Canvas camera = a look-at point on the world plane (cx, cy in screen units), a scale and two tilts.
 * The pivot (transform-origin) is the look-at point, so the point stays centred while the scale and
 * the tilts change — a pan/zoom path that never swings, and a bank that turns about the screen centre.
 */
export function lookAtVars(viewport, { cx, cy, s, rx = 0, ry = 0 }) {
  const ox = cx * viewport.w,
    oy = cy * viewport.h;
  return {
    x: viewport.w / 2 - ox,
    y: viewport.h / 2 - oy,
    scale: s,
    rotationX: rx,
    rotationY: ry,
    transformOrigin: `${ox}px ${oy}px`,
  };
}

/** Camera target of a world place: tile centre, scale 1/s (engine cameraTarget convention). */
export function tileTarget(place, fallback = { cx: 0.5, cy: 0.5, s: 1 }) {
  const world = place?.world;
  if (!world) return fallback;
  const s = world.s ?? 1;
  return { cx: world.x + 0.5 * s, cy: world.y + 0.5 * s, s: 1 / s };
}

/** Near layers (data-depth ≥ 0.9, the haze) that only camera moves may push. */
export const nearLayers = (ctx) =>
  [...ctx.stage.root.querySelectorAll('[data-depth]')].filter((node) => Number(node.dataset.depth) >= 0.9);

/**
 * The camera path is sampled from state(p) into short linear fromTo segments on the camera (and the near
 * layers). Every segment carries both ends, so any seek order lands on the same frame, and nothing relies
 * on callbacks (seek suppresses them).
 */
export function driveCamera(tl, ctx, duration, state, steps = 24) {
  const camera = ctx.stage.camera,
    near = nearLayers(ctx),
    d = duration / steps;
  for (let k = 0; k < steps; k += 1) {
    const a = state(k / steps),
      b = state((k + 1) / steps);
    tl.fromTo(
      camera,
      lookAtVars(ctx.viewport, a),
      { ...lookAtVars(ctx.viewport, b), duration: d, ease: 'none', immediateRender: false },
      k * d,
    );
    if (near.length)
      tl.fromTo(
        near,
        { x: a.hazeX ?? 0, y: a.hazeY ?? 0 },
        { x: b.hazeX ?? 0, y: b.hazeY ?? 0, duration: d, ease: 'none', immediateRender: false },
        k * d,
      );
  }
}

export const lerp = (a, b, t) => a + (b - a) * t;
/** Scale interpolated in log space so a zoom reads at a constant rate. */
export const lerpScale = (a, b, t) => a * (b / a) ** t;

export default {
  id: 'arc-flight',
  family: 'camera',
  role: 'camera',
  accepts: ['*'],
  sources: ['camera-flight', 'parallax', 'deep-parallax', 'atmospheric-depth'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.6, max: 4, doc: '전체 길이(u)' },
    altitude: { type: 'number', default: 0.32, min: 0, max: 0.6, doc: '거리 1화면당 고도(배율 감소 비율)' },
    bank: { type: 'number', default: 5, min: 0, max: 8, doc: '진행 방향 기울기 최대(°, 정지점에서는 0)' },
    parallax: { type: 'number', default: 0.35, min: 0, max: 1, doc: 'haze 층이 비행 중 밀리는 양(화면 폭 비율)' },
    settle: { type: 'number', default: 0.12, min: 0, max: 0.3, doc: '끝에서 기울기가 먼저 풀리는 구간 비율' },
    ease: { type: 'ease', default: 'flight', doc: '컨셉 ease alias' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const to = tileTarget(ctx.beat.place, tileTarget(ctx.prev?.place));
    const from = tileTarget(ctx.prev?.place, to);
    const dx = to.cx - from.cx,
      dy = to.cy - from.cy,
      distance = Math.hypot(dx, dy);
    const glide = distance < (ctx.tokens.glideBelow ?? 0.6) || ctx.reduce;
    const ease = ctx.gsap.parseEase(ctx.ease(params.ease)) ?? ((t) => t);
    const lift = glide ? 0 : Math.min(0.62, params.altitude * distance);
    const bank = glide ? 0 : Math.min(params.bank, ctx.tokens.bankMax ?? 8);
    const level = 1 - params.settle;
    const shift = glide ? 0 : params.parallax * (ctx.tokens.hazeShift ?? 0.35) * ctx.viewport.w;
    driveCamera(tl, ctx, params.duration, (p) => {
      const e = ease(p);
      // altitude: a smooth hump, highest a little before the middle (take-off is quicker than landing)
      const hump = Math.sin(Math.PI * p ** 0.85);
      // bank only while cruising; level before the landing settle so the stop is always face-on
      const tilt = p >= level ? 0 : Math.sin(Math.PI * (p / level));
      return {
        cx: lerp(from.cx, to.cx, e),
        cy: lerp(from.cy, to.cy, e),
        s: lerpScale(from.s, to.s, e) * (1 - lift * hump),
        rx: distance ? (-dy / distance) * bank * 0.55 * tilt : 0,
        ry: distance ? (dx / distance) * bank * tilt : 0,
        hazeX: distance ? (-dx / distance) * shift * hump : 0,
        hazeY: distance ? (-dy / distance) * shift * hump : 0,
      };
    });
  },
};
