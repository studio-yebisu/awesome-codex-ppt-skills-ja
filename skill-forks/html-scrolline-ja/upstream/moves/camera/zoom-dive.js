/** Dive through a selected port into the next beat's already-contained world. */
import { colorOf } from '../_shared/color.js';
import { gridLayout } from '../_shared/grid.js';
import { finishLink } from '../_shared/link.js';
import { px } from '../_shared/timeline.js';

const boxRect = (rect, box) => ({
  x: rect.x + rect.w * box.x,
  y: rect.y + rect.h * box.y,
  w: rect.w * box.w,
  h: rect.h * box.h,
});
const center = (rect) => ({ x: rect.x + rect.w / 2, y: rect.y + rect.h / 2 });
const union = (rects) => {
  const live = rects.filter((r) => r.w > 0 && r.h > 0);
  if (!live.length) return null;
  const x = Math.min(...live.map((r) => r.x)),
    y = Math.min(...live.map((r) => r.y));
  return {
    x,
    y,
    w: Math.max(...live.map((r) => r.x + r.w)) - x,
    h: Math.max(...live.map((r) => r.y + r.h)) - y,
  };
};
const originFor = (rect, fixed) => `${fixed.x - rect.x}px ${fixed.y - rect.y}px`;
const includes = (nodes, node) => nodes.some((other) => other !== node && other.contains(node));
const unique = (nodes) => [...new Set(nodes)];
const rectFor = (beat, node) => {
  for (const [name, nodes] of Object.entries(beat.parts)) {
    const index = nodes.indexOf(node);
    if (index >= 0) return beat.anchor(name, index).rect;
  }
  return { x: 0, y: 0, w: 0, h: 0 };
};
const worldParts = (beat, hud, ctx) =>
  unique(
    Object.entries(beat.parts)
      .filter(([name]) => !hud.has(name) && !ctx.skipParts.includes(name))
      .flatMap(([, nodes]) => nodes)
      .filter((node) => !ctx.skipNodes?.includes(node)),
  ).filter((node, _, all) => !includes(all, node));
const hudParts = (beat, names, ctx) =>
  unique(names.flatMap((name) => beat.part(name))).filter(
    (node) => !ctx.skipParts.includes(node.dataset.part) && !ctx.skipNodes?.includes(node),
  );
const autoK = (port, frame, tokens) =>
  Math.min(
    tokens.diveKMax ?? 40,
    1 / ((tokens.diveFill ?? 0.86) * Math.min(port.w / frame.w, port.h / frame.h)),
  );
/** Linear-in-scale ease whose scale reads k^z: (k^base(p) - 1) / (k - 1). */
export const expEase = (gsap, k, ease) => {
  const base = gsap.parseEase(ease) ?? ((p) => p);
  return (p) => (k ** base(p) - 1) / (k - 1);
};
/** Step overlays the beat left on stage (port-aim ring, rule-mark line): they ride the zoom like world. */
/** An 'out' ease that holds 0 for the first `wait` of the tween: B's fade starts at span start (no flash of an
 * earlier initial) but becomes visible only after the wait. */
const late = (ctx, wait) => {
  const out = ctx.gsap.parseEase(ctx.ease('out')) ?? ((p) => p);
  return (p) => (p <= wait ? 0 : out((p - wait) / (1 - wait)));
};
const stepOverlays = (ctx, beat) =>
  [...ctx.stage.overlay.children].filter((node) => (node.dataset.overlayKey ?? '').startsWith(`${beat.id}:step:`));

function corners(ctx, rect) {
  const accent = colorOf(ctx, 'accent');
  const length = px(ctx, ctx.tokens.cornerLen ?? 28);
  const positions = gridLayout({ n: 4, cols: 2, cell: 1 }).map(({ i }) => [i % 2, Math.floor(i / 2)]);
  return positions.map(([column, row]) => {
    const corner = document.createElement('i');
    corner.className = 'sl-zoom-corner';
    Object.assign(corner.style, {
      position: 'absolute',
      left: `${rect.x + (column ? rect.w - length : 0)}px`,
      top: `${rect.y + (row ? rect.h - length : 0)}px`,
      width: `${length}px`,
      height: `${length}px`,
      borderColor: accent,
      borderStyle: 'solid',
      borderWidth: `${row ? 0 : 1.5}px ${column ? 0 : 1.5}px ${row ? 1.5 : 0}px ${column ? 1.5 : 0}px`,
      pointerEvents: 'none',
    });
    ctx.overlay.append(corner);
    return corner;
  });
}

export default {
  id: 'zoom-dive',
  family: 'camera',
  role: 'link',
  accepts: ['chart', 'number', 'compare', 'photo', 'video', 'text'],
  sources: ['infinite-zoom', 'zoom-to-detail', 'zoom-through', 'giant-mask-reveal', 'push-in'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 1.4, max: 4, doc: '전체 길이(u)' },
    fromPart: { type: 'part', default: '', doc: 'A 포트 part. 비우면 primary' },
    fromIndex: { type: 'integer', default: 0, min: 0, max: 31, doc: 'A 포트 요소 index' },
    fromBox: { type: 'object', default: { x: 0, y: 0, w: 1, h: 1 }, doc: '포트 안 부분 상자(0..1)' },
    toPart: { type: 'part', default: '', doc: 'B frame part. 비우면 primary' },
    toIndex: { type: 'integer', default: 0, min: 0, max: 31, doc: 'B frame 요소 index' },
    frameAll: { type: 'boolean', default: false, doc: 'B frame = B world part 전체를 감싸는 rect(나란한 화면 두 장 등)' },
    k: { type: 'number', default: 0, min: 0, max: 60, doc: '0=자동, 아니면 4..60 배율' },
    portFade: { type: 'number', default: 0.25, min: 0, max: 1, doc: '포트가 옅어져 남는 불투명도(안의 세계가 보이게)' },
    hudParts: {
      type: 'array',
      default: ['title', 'dek', 'note', 'source', 'legend', 'caption', 'verdict'],
      doc: 'A에서 배율을 받지 않고 먼저 사라지는 HUD part',
    },
    toHudParts: {
      type: 'array',
      default: ['title', 'dek', 'note', 'source', 'legend', 'caption', 'verdict'],
      doc: 'B에서 배율을 받지 않고 끝에 초점이 맞는 HUD part(chart label은 축 라벨이라 world)',
    },
    ease: { type: 'ease', default: 'dive', doc: 'dive | none | in | out' },
    corners: { type: 'boolean', default: true, doc: '도착 frame viewfinder 표시' },
  },
  handoff(params) {
    return {
      from: { part: params.fromPart || undefined, index: params.fromIndex },
      to: { part: params.toPart || undefined, index: params.toIndex || undefined },
    };
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const d = params.duration;
    const free = { ...ctx, skipParts: [], skipNodes: [] };
    const fromWorld = worldParts(ctx.from, new Set(params.hudParts), free);
    const toWorld = worldParts(ctx.beat, new Set(params.toHudParts), free);
    const fromHud = hudParts(ctx.from, params.hudParts, free);
    const toHud = hudParts(ctx.beat, params.toHudParts, free);
    const port = boxRect(ctx.handoff.from.rect, params.fromBox);
    const frame =
      (params.frameAll && union(toWorld.map((node) => rectFor(ctx.beat, node)))) || ctx.handoff.to.rect;
    const k = Math.max(1.01, params.k || autoK(port, frame, ctx.tokens));
    const P = center(port),
      F = center(frame);
    const fixed = { x: (k * P.x - F.x) / (k - 1), y: (k * P.y - F.y) / (k - 1) };
    const portNode = ctx.handoff.from.node;
    const aimed = stepOverlays(ctx, ctx.from);
    const finder = params.corners ? corners(ctx, frame) : [];
    // A 쪽 초기값은 앞 link의 B 초기값과 같은 요소에 겹칠 수 있다: B 쪽 등장은 전부 fromTo라 순서와 무관하다
    ctx.initial(fromWorld, { autoAlpha: 1 });
    ctx.initial(toWorld, { autoAlpha: 0 });
    ctx.initial(toHud, { autoAlpha: 0, y: px(ctx, ctx.tokens.hudRise ?? 16), filter: ctx.reduce ? 'none' : 'blur(4px)' });
    ctx.initial(finder, { autoAlpha: 0 });
    if (ctx.reduce) {
      tl.to(fromWorld, { autoAlpha: 0, duration: d * 0.5, ease: ctx.ease('in') }, 0);
      tl.fromTo(toWorld, { autoAlpha: 0 }, { autoAlpha: 1, duration: d * 0.5, ease: ctx.ease('out'), immediateRender: false }, d * 0.5);
    } else {
      // 배율: A world part = k^z, B world part = k^(z−1), 같은 고정점 X*. fromTo라 앞뒤 move의 초기값과 섞이지 않는다
      const ease = expEase(ctx.gsap, k, ctx.ease(params.ease));
      const zoom = (nodes, beat, a, b) =>
        nodes.forEach((node) => {
          const transformOrigin = originFor(rectFor(beat, node), fixed);
          tl.fromTo(
            node,
            { scale: a, transformOrigin },
            { scale: b, transformOrigin, duration: d, ease, force3D: false, immediateRender: false },
            0,
          );
        });
      zoom(fromWorld, ctx.from, 1, k);
      zoom(toWorld, ctx.beat, 1 / k, 1);
      // 앞 beat의 조준 링·기준선은 world와 함께 커지며 사라진다(포트를 지나가는 문)
      aimed.forEach((node) =>
        tl.fromTo(
          node,
          { scale: 1, transformOrigin: `${fixed.x}px ${fixed.y}px` },
          { scale: k, transformOrigin: `${fixed.x}px ${fixed.y}px`, duration: d, ease, force3D: false, immediateRender: false },
          0,
        ),
      );
      const aimedMarks = aimed.flatMap((node) => [...node.children]);
      if (aimedMarks.length) tl.to(aimedMarks, { opacity: 0, duration: d * 0.3, ease: ctx.ease('in') }, d * 0.12);
      // 포트 안 작은 세계가 켜지고, 포트 자신은 옅어져 창이 된다
      tl.fromTo(toWorld, { autoAlpha: 0 }, { autoAlpha: 1, duration: d * 0.45, ease: late(ctx, 0.1 / 0.45), immediateRender: false }, 0);
      tl.to(portNode, { autoAlpha: params.portFade, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.1);
      tl.to(fromWorld, { autoAlpha: 0, duration: d * 0.3, ease: ctx.ease('in') }, d * 0.55);
      tl.to(finder, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, 0);
      tl.to(finder, { autoAlpha: 0, duration: d * 0.12, ease: ctx.ease('in') }, d * 0.88);
    }
    tl.to(fromHud, { y: -px(ctx, 12), autoAlpha: 0, duration: d * 0.12, ease: ctx.ease('in') }, 0);
    tl.to(toHud, { y: 0, autoAlpha: 1, filter: 'blur(0px)', duration: d * 0.12, ease: ctx.ease('out') }, d * 0.88);
    // A의 사다리(ambient)는 B의 사다리가 같은 자리에 켜지기 직전(d − 0.1u)에 내려 둘이 겹쳐 보이지 않게 한다.
    // 덱은 B의 depth-ladder appearAfter를 link 길이 − 0.1로 맞춘다
    const leftLadders = [...ctx.stage.overlay.children]
      .filter((node) => (node.dataset.overlayKey ?? '').startsWith(`${ctx.from.id}:ambient:`))
      .flatMap((node) => [...node.children]);
    if (leftLadders.length) tl.set(leftLadders, { opacity: 0 }, Math.max(0, d - 0.1));
    finishLink(tl, ctx, { at: d, cross: 0.15, from: [portNode], to: [ctx.handoff.to.node] });
    tl.set(toWorld, { autoAlpha: 1 }, d);
  },
};
