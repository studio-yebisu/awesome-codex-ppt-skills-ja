/** Rail-opening camera yaw which settles into a flat chronology. */
const flat = (vars) =>
  Object.fromEntries(
    Object.entries(vars).filter(([key]) => !['rotationX', 'rotationY', 'rx', 'ry'].includes(key)),
  );
const cameraVars = (ctx, target) => {
  const vars = ctx.stage.cameraVars(target);
  if (!Object.hasOwn(vars, 's')) return vars;
  const { s, ...rest } = vars;
  return { ...rest, scale: s };
};
export default {
  id: 'rail-settle',
  family: 'camera',
  role: 'camera',
  accepts: ['chronology'],
  sources: ['perspective-tilt', 'crane-tilt', 'parallax', 'atmospheric-depth'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.2, min: 1, max: 3.6, doc: '전체 길이(u)' },
    tilt: { type: 'number', default: 9, min: 0, max: 12, doc: 'tilt 각도(°, ≤12)' },
    startScale: { type: 'number', default: 1.15, min: 1, max: 1.4, doc: '시작 scale' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const target = ctx.camera ?? { x: 0.5, y: 0.5, s: 1, rx: 0, ry: 0 },
      end = cameraVars(ctx, target);
    const scaleKey = Object.hasOwn(end, 'scale') ? 'scale' : 's',
      rxKey = Object.hasOwn(end, 'rotationX') ? 'rotationX' : 'rx',
      ryKey = Object.hasOwn(end, 'rotationY') ? 'rotationY' : 'ry';
    const start = {
      ...end,
      x: end.x - ctx.viewport.w * 0.08,
      [scaleKey]: end[scaleKey] * params.startScale,
      [rxKey]: params.tilt * 0.35,
      [ryKey]: -params.tilt,
    };
    const d = params.duration;
    if (ctx.reduce) {
      const reduced = { ...flat(end), [scaleKey]: end[scaleKey] * 1.04, autoAlpha: 0.92 };
      ctx.initial(ctx.stage.camera, reduced);
      tl.to(ctx.stage.camera, { ...flat(end), autoAlpha: 1, duration: d, ease: 'none' }, 0);
      return;
    }
    ctx.initial(ctx.stage.camera, start);
    tl.to(ctx.stage.camera, { ...end, duration: d * 0.8, ease: ctx.ease('inout') }, 0);
    tl.to(ctx.stage.camera, { ...end, duration: d * 0.2, ease: 'power3.out' }, d * 0.8);
    for (const layer of ctx.stage.root.querySelectorAll('[data-depth="0"]')) {
      ctx.initial(layer, { x: ctx.viewport.w * 0.06 });
      tl.to(layer, { x: 0, duration: d * 0.8 * (ctx.tokens.depthFar ?? 0.35), ease: ctx.ease('inout') }, 0);
    }
  },
};
