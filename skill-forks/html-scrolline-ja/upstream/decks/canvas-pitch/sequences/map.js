/**
 * Shared survey-map geometry for the canvas-pitch ground and atlas sequences.
 * Everything is read from deck.yaml (b-ground data + every world beat), so the
 * two sequences never keep their own copy of region coordinates.
 */
import deck from '../deck.yaml';
import { createRng } from '../../../engine/index.js';

const groundBeat = deck.beats.find((b) => b.type === 'sequence' && b.use === 'ground');

/** b-ground data: size, seed, sheet, regions, route, cartouche. */
export const GROUND = groundBeat.data;
/** World position of the ground (and atlas) root: map local (0,0). */
export const ORIGIN = { x: groundBeat.place.world.x, y: groundBeat.place.world.y };

/** Tile anatomy in 1920-design px (× viewport.px) and tile fractions. */
export const LABEL = Object.freeze({ left: 120, top: 0.12, size: 44, marker: 30, mid: 23 });
/** Where content beats sit inside their tile (canvas.md §3 grid). */
export const CONTENT = Object.freeze({ x0: 0.0625, x1: 0.72, y0: 0.5, y1: 0.88 });

const ASPECT = 16 / 9;

/** Pixel frame of the map for one viewport. */
export function frameOf(viewport, data = GROUND) {
  const vw = viewport.w,
    vh = viewport.h,
    px = viewport.px ?? Math.min(vw, (vh * 16) / 9) / 1920;
  return {
    vw,
    vh,
    px,
    W: data.size.w * vw,
    H: data.size.h * vh,
    /** world → map-local px */
    at: (X, Y) => [(X - ORIGIN.x) * vw, (Y - ORIGIN.y) * vh],
  };
}

export const regionById = (data = GROUND) => new Map(data.regions.map((r) => [r.id, r]));

/** Region marker = route waypoint, hanging in the gutter left of the place name. */
export function waypoint(region, f) {
  const [x, y] = f.at(region.x, region.y);
  return [x + (LABEL.left - LABEL.marker) * f.px, y + LABEL.top * f.vh + LABEL.mid * f.px];
}

/** Top-left of a region's place-name label (map-local px). */
export function labelAt(region, f) {
  const [x, y] = f.at(region.x, region.y);
  return [x + LABEL.left * f.px, y + LABEL.top * f.vh];
}

/** Sheet grid cell name for a world point, e.g. "B-1". */
export function cellName(X, Y, data = GROUND) {
  const cols = data.sheet.cols,
    rows = data.sheet.rows;
  const c = Math.min(cols.length - 1, Math.max(0, Math.floor(((X - ORIGIN.x) / data.size.w) * cols.length)));
  const r = Math.min(rows - 1, Math.max(0, Math.floor(((Y - ORIGIN.y) / data.size.h) * rows)));
  return `${cols[c]}-${r + 1}`;
}

/**
 * Give stroked paths a real dash length (pathLength-normalised dashoffset is unreliable in Chrome).
 * Returns each path's length; the rendered state stays fully drawn (offset 0).
 */
export function dashable(paths) {
  return paths.map((node) => {
    const length = Math.ceil(node.getTotalLength?.() || 4000) + 2;
    node.removeAttribute('pathLength');
    node.style.strokeDasharray = `${length} ${length}`;
    node.dataset.length = String(length);
    return length;
  });
}

/** Route waypoints (map-local px) in route order. */
export function routePoints(f, data = GROUND) {
  const byId = regionById(data);
  return data.route.map((id) => byId.get(id)).filter(Boolean).map((r) => waypoint(r, f));
}

const r1 = (n) => Math.round(n * 10) / 10;

/**
 * Catmull-Rom through points → cubic Bézier path, plus arc-length samples.
 * @returns {{ d: string, samples: number[][], length: number, at: number[] }} at = arc fraction per point
 */
export function spline(points, closed = false, steps = 24) {
  const n = points.length;
  const P = (i) => (closed ? points[(i + n) % n] : points[Math.max(0, Math.min(n - 1, i))]);
  let d = `M${r1(points[0][0])} ${r1(points[0][1])}`;
  const samples = [points[0]];
  const at = [0];
  let length = 0;
  const segs = closed ? n : n - 1;
  for (let i = 0; i < segs; i += 1) {
    const p0 = P(i - 1),
      p1 = P(i),
      p2 = P(i + 1),
      p3 = P(i + 2);
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += `C${r1(c1[0])} ${r1(c1[1])} ${r1(c2[0])} ${r1(c2[1])} ${r1(p2[0])} ${r1(p2[1])}`;
    for (let k = 1; k <= steps; k += 1) {
      const t = k / steps,
        u = 1 - t;
      const q = [
        u * u * u * p1[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * p2[0],
        u * u * u * p1[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * p2[1],
      ];
      const last = samples[samples.length - 1];
      length += Math.hypot(q[0] - last[0], q[1] - last[1]);
      samples.push(q);
    }
    at.push(length);
  }
  if (closed) d += 'Z';
  return { d, samples, length, at: at.map((x) => (length ? x / length : 0)) };
}

/** Rects (world) the terrain keeps calm: content blocks of every world beat + place-name labels. */
function calmRects(data) {
  const rects = [];
  for (const b of deck.beats) {
    const w = b.place?.world;
    if (!w || b.type === 'sequence') continue;
    rects.push({ x0: w.x + CONTENT.x0, x1: w.x + CONTENT.x1, y0: w.y + CONTENT.y0, y1: w.y + CONTENT.y1 });
  }
  for (const r of data.regions)
    rects.push({ x0: r.x + 0.02, x1: r.x + 0.42, y0: r.y + 0.07, y1: r.y + 0.22, label: true });
  return rects;
}

/** Physical (aspect-corrected) distance from a world point to a world rect. */
function rectDistance(X, Y, r) {
  const dx = Math.max(r.x0 - X, 0, X - r.x1) * ASPECT;
  const dy = Math.max(r.y0 - Y, 0, Y - r.y1);
  return Math.hypot(dx, dy);
}

function valueNoise(rng, size = 64) {
  const lattice = Float64Array.from({ length: size * size }, () => rng());
  const v = (i, j) => lattice[(((j % size) + size) % size) * size + (((i % size) + size) % size)];
  const s = (t) => t * t * (3 - 2 * t);
  return (x, y) => {
    const i = Math.floor(x),
      j = Math.floor(y),
      fx = s(x - i),
      fy = s(y - j);
    const a = v(i, j) + (v(i + 1, j) - v(i, j)) * fx;
    const b = v(i, j + 1) + (v(i + 1, j + 1) - v(i, j + 1)) * fx;
    return a + (b - a) * fy;
  };
}

/**
 * Deterministic elevation field over the map (world units). Hills sit between
 * regions and along the sheet edge; content blocks and labels lie on plains.
 */
export function elevation(data = GROUND) {
  const rng = createRng(data.seed ?? 1849);
  const rects = calmRects(data);
  const x0 = ORIGIN.x,
    y0 = ORIGIN.y,
    x1 = x0 + data.size.w,
    y1 = y0 + data.size.h;
  const calm = (X, Y) => Math.min(...rects.map((r) => rectDistance(X, Y, r)));
  // smooth elliptical plains centred on each calm rect (no straight creases at rect edges)
  const blobs = rects.map((r) => ({
    X: (r.x0 + r.x1) / 2,
    Y: (r.y0 + r.y1) / 2,
    ax: ((r.x1 - r.x0) / 2) * ASPECT * 1.15,
    ay: ((r.y1 - r.y0) / 2) * 1.5,
  }));
  const soft = (X, Y) => {
    let m = 0;
    for (const b of blobs) {
      const dx = ((X - b.X) * ASPECT) / b.ax,
        dy = (Y - b.Y) / b.ay;
      m = Math.max(m, Math.exp(-((dx * dx + dy * dy) ** 2) * 0.7));
    }
    return m;
  };
  const hills = [];
  for (let tries = 0; hills.length < 34 && tries < 3000; tries += 1) {
    const X = x0 + rng() * data.size.w,
      Y = y0 + rng() * data.size.h;
    const sigma = 0.14 + rng() * 0.28;
    if (calm(X, Y) < sigma * 0.7) continue;
    if (hills.some((h) => Math.hypot((h.X - X) * ASPECT, h.Y - Y) < (h.sigma + sigma) * 0.75)) continue;
    hills.push({ X, Y, sigma, h: 0.55 + rng() * 0.75, sx: 0.75 + rng() * 0.6 });
  }
  const noise = valueNoise(rng);
  const fbm = (X, Y) =>
    noise(X * 1.3 + 7, Y * 1.3 + 2) * 0.5 + noise(X * 2.6, Y * 2.6) * 0.32 + noise(X * 5.2 + 17, Y * 5.2 + 5) * 0.18;
  const field = (X, Y) => {
    let z = 0;
    for (const h of hills) {
      const dx = ((X - h.X) * ASPECT) / h.sx,
        dy = (Y - h.Y) * h.sx;
      z += h.h * Math.exp(-(dx * dx + dy * dy) / (2 * h.sigma * h.sigma));
    }
    const edge = Math.min((X - x0) * ASPECT, (x1 - X) * ASPECT, Y - y0, y1 - Y);
    z += 0.95 * Math.max(0, 1 - edge / 0.55) ** 2;
    const plain = soft(X, Y);
    z += (fbm(X, Y) - 0.5) * 1.1 * (1 - 0.5 * plain);
    return z * (1 - 0.45 * plain);
  };
  return { field, hills };
}

/**
 * Marching squares contours of the elevation field, in map-local px.
 * @returns {{ level: number, index: boolean, chains: { d: string, cx: number, cy: number, len: number }[] }[]}
 */
export function contours(f, data = GROUND, { perUnit = 52, levels = 34 } = {}) {
  const { field, hills } = elevation(data);
  const nx = Math.round(data.size.w * perUnit) + 1,
    ny = Math.round(data.size.h * perUnit * (9 / 16)) + 1;
  const Z = new Float64Array(nx * ny);
  for (let j = 0; j < ny; j += 1)
    for (let i = 0; i < nx; i += 1)
      Z[j * nx + i] = field(ORIGIN.x + (i / (nx - 1)) * data.size.w, ORIGIN.y + (j / (ny - 1)) * data.size.h);
  const sorted = Float64Array.from(Z).sort();
  const lo = sorted[Math.floor(sorted.length * 0.06)],
    hi = sorted[Math.floor(sorted.length * 0.995)];
  const sx = f.W / (nx - 1),
    sy = f.H / (ny - 1);
  const out = [];
  for (let k = 0; k < levels; k += 1) {
    const level = lo + ((hi - lo) * (k + 0.5)) / levels;
    out.push({ level, index: k % 5 === 3, chains: trace(Z, nx, ny, level, sx, sy) });
  }
  return { levels: out, hills, peak: (h) => f.at(h.X, h.Y) };
}

function trace(Z, nx, ny, level, sx, sy) {
  const pts = new Map();
  const point = (key, ax, ay, bx, by) => {
    if (pts.has(key)) return key;
    const za = Z[ay * nx + ax],
      zb = Z[by * nx + bx];
    const t = za === zb ? 0.5 : (level - za) / (zb - za);
    pts.set(key, [(ax + (bx - ax) * t) * sx, (ay + (by - ay) * t) * sy]);
    return key;
  };
  const H = (i, j) => point(`h${i},${j}`, i, j, i + 1, j);
  const V = (i, j) => point(`v${i},${j}`, i, j, i, j + 1);
  const adj = new Map();
  const link = (a, b) => {
    (adj.get(a) ?? adj.set(a, []).get(a)).push(b);
    (adj.get(b) ?? adj.set(b, []).get(b)).push(a);
  };
  for (let j = 0; j < ny - 1; j += 1)
    for (let i = 0; i < nx - 1; i += 1) {
      const a = Z[j * nx + i] > level,
        b = Z[j * nx + i + 1] > level,
        c = Z[(j + 1) * nx + i + 1] > level,
        d = Z[(j + 1) * nx + i] > level;
      const code = (a ? 8 : 0) | (b ? 4 : 0) | (c ? 2 : 0) | (d ? 1 : 0);
      if (code === 0 || code === 15) continue;
      const top = () => H(i, j),
        right = () => V(i + 1, j),
        bottom = () => H(i, j + 1),
        left = () => V(i, j);
      switch (code) {
        case 1: case 14: link(left(), bottom()); break;
        case 2: case 13: link(bottom(), right()); break;
        case 3: case 12: link(left(), right()); break;
        case 4: case 11: link(top(), right()); break;
        case 6: case 9: link(top(), bottom()); break;
        case 7: case 8: link(left(), top()); break;
        case 5: link(left(), top()); link(bottom(), right()); break;
        case 10: link(left(), bottom()); link(top(), right()); break;
        default: break;
      }
    }
  const seen = new Set();
  const chains = [];
  const walk = (startKey) => {
    const keys = [startKey];
    seen.add(startKey);
    let cur = startKey;
    for (;;) {
      const next = (adj.get(cur) ?? []).find((k) => !seen.has(k));
      if (!next) break;
      seen.add(next);
      keys.push(next);
      cur = next;
    }
    return keys;
  };
  // open chains first (start at degree-1 ends), then closed loops
  for (const [key, list] of adj) if (list.length === 1 && !seen.has(key)) chains.push({ keys: walk(key), closed: false });
  for (const key of adj.keys()) if (!seen.has(key)) chains.push({ keys: walk(key), closed: true });
  return chains
    .filter((c) => c.keys.length >= 7)
    .map((c) => {
      const points = c.keys.map((k) => pts.get(k));
      const s = spline(points, c.closed, 1);
      const cx = points.reduce((n, p) => n + p[0], 0) / points.length;
      const cy = points.reduce((n, p) => n + p[1], 0) / points.length;
      return { d: s.d, cx, cy, len: s.length };
    });
}
