// Pure, deterministic explode timeline. Shared by index.html (render) and
// tools that project callout anchors, so both read the same numbers.
export const FPS = 24;
export const FRAMES = 96;

// Final layout. Plates are spaced evenly by GAP (mm) above the housing rim (z 12).
export const GAP = 19;
export const FINAL = { elev: 17, yaw: 316, distance: 392, targetZ: 37, center: { x: 0.62, y: 0.52 } };
export const START = { elev: 6, yaw: 300, distance: 232, targetZ: 0, center: { x: 0.62, y: 0.52 } };

// Closed z of each layer's visible plate (scene.js) and its exploded plate z.
// 0 fabric top, 1 halo ring, 2 mic board, 3 main board, 4 battery and 5 housing stay as the base.
const CLOSED_PLATE = [12.15, 12.72, 11.25, 8.7, 0, 0];
const FINAL_PLATE = [12 + 4 * GAP, 12 + 3 * GAP, 12 + 2 * GAP, 12 + GAP, 0, 0];
export const OFFSET = CLOSED_PLATE.map((z, i) => FINAL_PLATE[i] - z);

const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const smoother = (p) => { const q = clamp(p, 0, 1); return q * q * q * (q * (q * 6 - 15) + 10); };
const span = (f, a, b) => smoother((f - a) / (b - a));
const mix = (a, b, p) => a + (b - a) * p;

export function frameAt(time) {
  return clamp(Math.floor(time * FPS + 1e-6) + 1, 1, FRAMES);
}

export function stateAt(frame) {
  const look = span(frame, 1, 16);
  const pull = span(frame, 1, 88);
  const lift = [span(frame, 17, 40), span(frame, 19, 40), span(frame, 41, 64), span(frame, 65, 88), span(frame, 65, 88), 0];
  return {
    frame,
    elev: mix(START.elev, FINAL.elev, span(frame, 1, 20)),
    yaw: mix(START.yaw, FINAL.yaw, pull),
    distance: mix(START.distance, FINAL.distance, span(frame, 1, 56)),
    targetZ: mix(START.targetZ, FINAL.targetZ, span(frame, 1, 60)),
    center: START.center,
    lights: look,
    halo: mix(1, 0.35, look),
    haloArc: 1 - span(frame, 1, 8),
    offsets: OFFSET.map((o, i) => o * lift[i]),
  };
}
