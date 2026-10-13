/** The persistent night survey map: contours, sheet grid, place names, the walked route, cartouche. */
import { GROUND, cellName, dashable, contours, frameOf, labelAt, routePoints, spline, waypoint } from './map.js';

const NS = 'http://www.w3.org/2000/svg';
const C = {
  plate: '#0f171d',
  rule: '#24343e',
  contour: '#2a3e4a',
  index: '#35505e',
  line: '#3a5260',
  muted: '#7d8a91',
  ink: '#a9a698',
};

function el(parent, name, attrs = {}, text) {
  const node = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  if (text != null) node.textContent = text;
  parent.append(node);
  return node;
}
function div(parent, css, text) {
  const node = document.createElement('div');
  node.style.cssText = css;
  if (text != null) node.textContent = text;
  parent.append(node);
  return node;
}
function layer(root, depth) {
  const node = div(root, 'position:absolute;inset:0;pointer-events:none;');
  node.dataset.depth = String(depth);
  return node;
}
const r1 = (n) => Math.round(n * 10) / 10;
/** Cartographic label halo: knocks contours and the route out behind type. */
const halo = (px) => [3, 7, 12].map((b) => `0 0 ${r1(b * px)}px ${C.plate}`).join(',');

export default {
  type: 'sequence',
  primary: 'contour',
  fields: {
    use: { type: 'string', required: true, doc: '덱 전용 sequence 이름' },
    data: { type: 'any', required: true, doc: '지도 지형 데이터' },
  },
  timing: () => ({ duration: 1.2, stops: [] }),
  render(beat, rc) {
    const data = beat.data ?? GROUND;
    const f = frameOf(rc.viewport, data);
    const { W, H, px } = f;
    const parts = { contour: [], grid: [], name: [], route: [], cartouche: [], haze: [] };
    const root = document.createElement('section');
    root.className = 'sl-beat sl-beat--sequence sl-seq-ground';
    root.style.cssText = `width:${W}px;height:${H}px;overflow:hidden;pointer-events:none;background:radial-gradient(ellipse 70% 70% at 38% 42%, #111b22 0%, ${C.plate} 55%, #0c1318 100%);`;

    // depth 0 — terrain: contours, spot heights, neatline
    const ground = layer(root, 0);
    const terrain = el(ground, 'svg', { width: W, height: H, viewBox: `0 0 ${r1(W)} ${r1(H)}`, style: 'position:absolute;inset:0;overflow:visible' });
    const topo = contours(f, data);
    const start = f.at(0.5, 0.5);
    for (const lv of topo.levels) {
      const g = el(terrain, 'g', {
        fill: 'none',
        stroke: lv.index ? C.index : C.contour,
        'stroke-width': r1((lv.index ? 1.5 : 1) * px),
        'stroke-linejoin': 'round',
      });
      for (const ch of lv.chains) {
        const dist = Math.hypot(ch.cx - start[0], (ch.cy - start[1]) * (16 / 9)) / f.vw;
        const p = el(g, 'path', { d: ch.d });
        p.dataset.pre = dist < 0.8 ? '0.7' : '1';
        p.dataset.delay = String(Math.min(0.55, Math.max(0, (dist - 0.5) / 7)));
        parts.contour.push(p);
      }
    }
    const peaks = [...topo.hills].sort((a, b) => b.h - a.h).slice(0, 8);
    const spot = el(terrain, 'g', { fill: C.muted, 'fill-opacity': 0.55, stroke: C.muted, 'stroke-opacity': 0.55, 'stroke-width': r1(px) });
    for (const h of peaks) {
      const [x, y] = topo.peak(h);
      const s = 7 * px;
      el(spot, 'path', { d: `M${r1(x - s)} ${r1(y)}H${r1(x + s)}M${r1(x)} ${r1(y - s)}V${r1(y + s)}` });
      el(spot, 'text', { x: r1(x + 12 * px), y: r1(y - 10 * px), stroke: 'none', 'font-family': 'IBM Plex Mono, monospace', 'font-size': r1(17 * px), 'letter-spacing': '0.04em' }, String(Math.round(180 + h.h * 320)));
    }
    parts.contour.push(spot);
    // neatline: outer hairline, alternating survey bar, inner hairline
    const m = 72 * px,
      bar = 8 * px;
    const cellW = (W - 2 * (m + bar)) / data.sheet.cols.length,
      cellH = (H - 2 * (m + bar)) / data.sheet.rows;
    const neat = el(terrain, 'g', { fill: 'none' });
    el(neat, 'rect', { x: r1(m), y: r1(m), width: r1(W - 2 * m), height: r1(H - 2 * m), stroke: C.line, 'stroke-width': r1(px) });
    el(neat, 'rect', { x: r1(m + bar), y: r1(m + bar), width: r1(W - 2 * (m + bar)), height: r1(H - 2 * (m + bar)), stroke: C.line, 'stroke-width': r1(px) });
    const mid = m + bar / 2;
    const barAttrs = (dash) => ({ stroke: C.rule, 'stroke-width': r1(bar), 'stroke-dasharray': `${r1(dash)} ${r1(dash)}` });
    el(neat, 'path', { d: `M${r1(m + bar)} ${r1(mid)}H${r1(W - m - bar)}M${r1(m + bar)} ${r1(H - mid)}H${r1(W - m - bar)}`, ...barAttrs(cellW / 8) });
    el(neat, 'path', { d: `M${r1(mid)} ${r1(m + bar)}V${r1(H - m - bar)}M${r1(W - mid)} ${r1(m + bar)}V${r1(H - m - bar)}`, ...barAttrs(cellH / 8) });
    parts.contour.push(neat);

    // depth 0.35 — sheet grid, route, region markers, names, cartouche
    const print = layer(root, 0.35);
    const sheet = el(print, 'svg', { width: W, height: H, viewBox: `0 0 ${r1(W)} ${r1(H)}`, style: 'position:absolute;inset:0;overflow:visible' });
    const grid = el(sheet, 'g', { stroke: C.line, 'stroke-width': r1(px), fill: 'none' });
    const x0 = m + bar,
      y0 = m + bar;
    let lines = '';
    for (let c = 1; c < data.sheet.cols.length; c += 1) lines += `M${r1(x0 + c * cellW)} ${r1(y0)}V${r1(H - y0)}`;
    for (let r = 1; r < data.sheet.rows; r += 1) lines += `M${r1(x0)} ${r1(y0 + r * cellH)}H${r1(W - x0)}`;
    el(grid, 'path', { d: lines, 'stroke-opacity': 0.22, 'stroke-dasharray': `${r1(2 * px)} ${r1(10 * px)}` });
    let ticks = '';
    const t = 16 * px;
    for (let c = 1; c < data.sheet.cols.length; c += 1)
      for (let r = 1; r < data.sheet.rows; r += 1) {
        const gx = x0 + c * cellW,
          gy = y0 + r * cellH;
        ticks += `M${r1(gx - t)} ${r1(gy)}H${r1(gx + t)}M${r1(gx)} ${r1(gy - t)}V${r1(gy + t)}`;
      }
    el(grid, 'path', { d: ticks, 'stroke-opacity': 0.6 });
    parts.grid.push(grid);
    const gridLabel = (x, y, text) =>
      div(print, `position:absolute;left:${r1(x)}px;top:${r1(y)}px;transform:translate(-50%,-50%);font:500 ${r1(19 * px)}px/1 'IBM Plex Mono',monospace;letter-spacing:.08em;color:${C.muted};opacity:.7;white-space:nowrap;`, text);
    [...data.sheet.cols].forEach((col, c) => {
      parts.grid.push(gridLabel(x0 + (c + 0.5) * cellW, m / 2, col), gridLabel(x0 + (c + 0.5) * cellW, H - m / 2, col));
    });
    for (let r = 0; r < data.sheet.rows; r += 1)
      parts.grid.push(gridLabel(m / 2, y0 + (r + 0.5) * cellH, String(r + 1)), gridLabel(W - m / 2, y0 + (r + 0.5) * cellH, String(r + 1)));

    const trail = spline(routePoints(f, data));
    const route = el(sheet, 'path', {
      d: trail.d,
      fill: 'none',
      stroke: C.line,
      'stroke-width': r1(3 * px),
      'stroke-linecap': 'round',
      'stroke-dasharray': `0.01 ${r1(11 * px)}`,
    });
    parts.route.push(route);

    for (const region of data.regions) {
      const [mx, my] = waypoint(region, f);
      const mark = el(sheet, 'g', {});
      el(mark, 'circle', { cx: r1(mx), cy: r1(my), r: r1(9 * px), fill: C.plate, stroke: C.muted, 'stroke-width': r1(1.5 * px) });
      el(mark, 'circle', { cx: r1(mx), cy: r1(my), r: r1(2.6 * px), fill: C.muted });
      const [lx, ly] = labelAt(region, f);
      const label = div(
        print,
        `position:absolute;left:${r1(lx)}px;top:${r1(ly)}px;display:flex;align-items:baseline;gap:${r1(26 * px)}px;white-space:nowrap;color:${C.muted};text-shadow:${halo(px)};`,
      );
      div(label, `font:600 ${r1(44 * px)}px/1 'Noto Serif KR',serif;letter-spacing:.32em;`, region.name);
      div(label, `font:500 ${r1(19 * px)}px/1 'IBM Plex Mono',monospace;letter-spacing:.1em;opacity:.75;`, cellName(region.x + 0.1, region.y + 0.15, data));
      label.dataset.region = region.id;
      mark.dataset.region = region.id;
      parts.name.push(mark, label);
    }

    if (data.cartouche) {
      const [cx, cy] = f.at(data.cartouche.at.x, data.cartouche.at.y);
      const box = div(
        print,
        `position:absolute;left:${r1(cx)}px;top:${r1(cy)}px;width:${r1(380 * px)}px;padding:${r1(16 * px)}px 0;border-top:1px solid ${C.line};border-bottom:1px solid ${C.line};color:${C.muted};`,
      );
      const [title, ...rest] = data.cartouche.lines;
      div(box, `font:600 ${r1(26 * px)}px/1.3 'Noto Serif KR',serif;color:${C.ink};letter-spacing:.04em;`, title);
      for (const line of rest)
        div(box, `margin-top:${r1(10 * px)}px;font:500 ${r1(19 * px)}px/1.2 'IBM Plex Mono',monospace;letter-spacing:.08em;`, line);
      // scale bar
      const scale = div(box, `position:relative;margin-top:${r1(18 * px)}px;height:${r1(30 * px)}px;font:500 ${r1(17 * px)}px/1 'IBM Plex Mono',monospace;letter-spacing:.06em;`);
      div(scale, `position:absolute;left:0;top:0;width:${r1(220 * px)}px;height:${r1(6 * px)}px;border:1px solid ${C.muted};background:repeating-linear-gradient(90deg, ${C.muted} 0 ${r1(55 * px)}px, transparent ${r1(55 * px)}px ${r1(110 * px)}px);opacity:.7;`);
      div(scale, `position:absolute;left:0;top:${r1(14 * px)}px;`, '0');
      div(scale, `position:absolute;left:${r1(220 * px)}px;top:${r1(14 * px)}px;transform:translateX(-50%);white-space:nowrap;`, '1 km');
      parts.cartouche.push(box);
    }

    // depth 1 — near haze, two thin veils the camera flies through
    const air = layer(root, 1);
    const veil = (X, Y, w, h, a) => {
      const [x, y] = f.at(X, Y);
      return div(
        air,
        `position:absolute;left:${r1(x - (w * f.vw) / 2)}px;top:${r1(y - (h * f.vh) / 2)}px;width:${r1(w * f.vw)}px;height:${r1(h * f.vh)}px;background:radial-gradient(closest-side, rgba(143,211,255,${a}), rgba(143,211,255,0));opacity:.35;`,
      );
    };
    parts.haze.push(veil(1.4, 1.2, 3.4, 2.6, 0.22), veil(4.3, 3.1, 3.2, 2.4, 0.16));
    return { root, parts };
  },
  build(tl, ctx) {
    const d = ctx.duration;
    const paths = ctx.beat.part('contour').filter((n) => n.dataset?.pre);
    const rest = ctx.beat.part('contour').filter((n) => !n.dataset?.pre);
    dashable(paths);
    ctx.initial(paths, { strokeDashoffset: (i, node) => Number(node.dataset.pre) * Number(node.dataset.length) });
    tl.to(
      paths,
      {
        strokeDashoffset: 0,
        duration: d * 0.45,
        ease: 'power1.out',
        stagger: (i, node) => Number(node.dataset.delay) * d,
      },
      0,
    );
    ctx.initial(rest, { autoAlpha: 0 });
    tl.to(rest, { autoAlpha: 1, duration: d * 0.5, ease: 'power2.out' }, d * 0.3);
    const fade = [...ctx.beat.part('grid'), ...ctx.beat.part('route')];
    ctx.initial(fade, { autoAlpha: 0 });
    tl.to(fade, { autoAlpha: 1, duration: d * 0.5, ease: 'power2.out' }, d * 0.15);
    const haze = ctx.beat.part('haze');
    ctx.initial(haze, { autoAlpha: 0 });
    tl.to(haze, { autoAlpha: 0.35, duration: d * 0.55, ease: 'power2.out' }, d * 0.3);
  },
};
