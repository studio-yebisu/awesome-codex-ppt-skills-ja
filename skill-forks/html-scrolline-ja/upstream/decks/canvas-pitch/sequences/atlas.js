/** Atlas: the walked route lights up in route order over the whole map; place names readable at atlas scale. */
import { GROUND, dashable, frameOf, regionById, routePoints, spline } from './map.js';

const NS = 'http://www.w3.org/2000/svg';
const ACCENT = '#8fd3ff';
const FG = '#ede6d6';
const r1 = (n) => Math.round(n * 10) / 10;

function el(parent, name, attrs = {}) {
  const node = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  parent.append(node);
  return node;
}

export default {
  type: 'sequence',
  primary: 'route',
  fields: {
    use: { type: 'string', required: true, doc: '덱 전용 sequence 이름' },
    data: { type: 'any', required: true, doc: '여정 경로 데이터' },
  },
  timing: () => ({ duration: 3.2, stops: [] }),
  render(beat, rc) {
    const data = GROUND;
    const f = frameOf(rc.viewport, data);
    const { W, H, px } = f;
    const parts = { route: [], dot: [], name: [], head: [] };
    const root = document.createElement('section');
    root.className = 'sl-beat sl-beat--sequence sl-seq-atlas';
    root.style.cssText = `width:${W}px;height:${H}px;pointer-events:none;`;
    const svg = el(root, 'svg', { width: W, height: H, viewBox: `0 0 ${r1(W)} ${r1(H)}`, style: 'position:absolute;inset:0;overflow:visible' });
    const points = routePoints(f, data);
    const trail = spline(points);
    const route = el(svg, 'path', {
      d: trail.d,
      fill: 'none',
      stroke: ACCENT,
      'stroke-width': r1(12 * px),
      'stroke-linecap': 'round',
      'stroke-linejoin': 'round',
    });
    parts.route.push(route);
    const byId = regionById(data);
    data.route.forEach((id, i) => {
      const region = byId.get(id);
      if (!region) return;
      const [x, y] = points[i];
      const dot = el(svg, 'circle', { cx: r1(x), cy: r1(y), r: r1(30 * px), fill: ACCENT });
      dot.dataset.at = String(trail.at[i]);
      dot.style.transformOrigin = `${r1(x)}px ${r1(y)}px`;
      parts.dot.push(dot);
      const [tx, ty] = f.at(region.x, region.y);
      const name = document.createElement('div');
      name.textContent = region.name;
      name.dataset.at = String(trail.at[i]);
      name.style.cssText = `position:absolute;left:${r1(tx + 150 * px)}px;top:${r1(ty + 0.17 * f.vh)}px;font:600 ${r1(210 * px)}px/1 'Noto Serif KR',serif;letter-spacing:.04em;color:${FG};white-space:nowrap;text-shadow:0 0 ${r1(14 * px)}px #0f171d,0 0 ${r1(30 * px)}px #0f171d;`;
      root.append(name);
      parts.name.push(name);
    });
    const step = Math.max(1, Math.floor(trail.samples.length / 90));
    const head = el(svg, 'circle', { cx: r1(points[0][0]), cy: r1(points[0][1]), r: r1(44 * px), fill: FG });
    head.dataset.path = JSON.stringify(trail.samples.filter((_, k) => k % step === 0).concat([trail.samples.at(-1)]).map((p) => [r1(p[0]), r1(p[1])]));
    parts.head.push(head);
    return { root, parts };
  },
  build(tl, ctx) {
    const d = ctx.duration;
    const t0 = d * 0.12,
      span = d * 0.72;
    const route = ctx.beat.part('route');
    const [length] = dashable(route);
    ctx.initial(route, { strokeDashoffset: length });
    tl.to(route, { strokeDashoffset: 0, duration: span, ease: 'none' }, t0);
    const head = ctx.beat.part('head')[0];
    if (head) {
      const path = JSON.parse(head.dataset.path);
      ctx.initial(head, { autoAlpha: 0, attr: { cx: path[0][0], cy: path[0][1] } });
      tl.to(head, { autoAlpha: 1, duration: d * 0.04 }, t0);
      const legs = path.slice(1).map((p, k) => Math.hypot(p[0] - path[k][0], p[1] - path[k][1]));
      const total = legs.reduce((a, b) => a + b, 0) || 1;
      tl.to(
        head,
        { keyframes: path.slice(1).map(([cx, cy], k) => ({ attr: { cx, cy }, duration: (span * legs[k]) / total, ease: 'none' })) },
        t0,
      );
      tl.to(head, { autoAlpha: 0, duration: d * 0.08 }, t0 + span);
    }
    for (const dot of ctx.beat.part('dot')) {
      const at = t0 + Number(dot.dataset.at) * span;
      ctx.initial(dot, { autoAlpha: 0, scale: 0.2 });
      tl.to(dot, { autoAlpha: 1, scale: 1, duration: d * 0.05, ease: 'power3.out' }, Math.max(0, at - d * 0.01));
    }
    for (const name of ctx.beat.part('name')) {
      const at = t0 + Number(name.dataset.at) * span;
      ctx.initial(name, { autoAlpha: 0 });
      tl.to(name, { autoAlpha: 1, duration: d * 0.1, ease: 'power2.out' }, Math.max(0, at - d * 0.01));
    }
  },
};
