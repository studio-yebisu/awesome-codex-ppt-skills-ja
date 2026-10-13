/** Carries same-named bars of one chart to their new ranked positions in the next chart.
 *  이름이 같은 막대(matchBy label)는 대역이 A 자리에서 B 자리로 걸어가며 세로→가로로 모양을 바꾸고,
 *  B에만 있는 막대는 기준선에서 자라 순위표를 채운다. A에만 있는 막대는 먼저 물러난다. */
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { px } from '../_shared/timeline.js';
import { growBar, overlaysOf } from './annotation-pin.js';
import { valueTags } from './aggregate-split.js';

const base = (nodes) => nodes.filter((node) => (node.dataset.state ?? 'base') === 'base');
const bars = (beat) => beat.part('mark').filter((m) => m.dataset.series === '0' && m.tagName.toLowerCase() !== 'path');

export default {
  id: 'rank-reorder',
  family: 'data',
  role: 'link',
  accepts: ['chart'],
  sources: ['rank-transition', 'object-constant-update', 'bump-rank-reveal'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 0.8, max: 4, doc: '전체 길이(u)' },
    matchBy: { type: 'enum', default: 'label', values: ['label', 'index'], doc: '같은 막대 찾는 기준' },
  },
  handoff: (params, { from, to }) => {
    const name = from.categories?.[from.highlight?.index ?? 0];
    const index = params.matchBy === 'label' ? Math.max(0, (to.categories ?? []).indexOf(name)) : 0;
    return { from: { part: 'mark', index: from.highlight?.index ?? 0 }, to: { part: 'mark', index } };
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      R = ctx.reduce ? 0.001 : 1,
      A = ctx.from,
      B = ctx.beat;
    const aBars = bars(A),
      bBars = bars(B);
    const aNames = A.data.categories,
      bNames = B.data.categories;
    const rectA = (m) => A.anchor('mark', A.part('mark').indexOf(m)).rect;
    const rectB = (m) => B.anchor('mark', B.part('mark').indexOf(m)).rect;
    const pairOf = (j) => (params.matchBy === 'label' ? aNames.indexOf(bNames[j]) : j);
    const hiA = A.data.highlight?.index,
      hiB = B.data.highlight?.index;
    // A 정리: 글자·값 표·축은 빠르게, 짝 없는 막대도 퇴장
    const aText = [...Object.entries(A.parts)].filter(([name]) => !['mark', 'plot'].includes(name)).flatMap(([, n]) => n);
    tl.to([...aText, ...overlaysOf(ctx, A.id, (k) => !k.includes(':link:'))], { autoAlpha: 0, duration: d * 0.12 * R, ease: ctx.ease('in') }, 0);
    const matched = new Set(bBars.map((_, j) => pairOf(j)).filter((i) => i >= 0));
    const lonely = aBars.filter((_, i) => !matched.has(i));
    tl.to(lonely, { autoAlpha: 0, duration: d * 0.12 * R, ease: ctx.ease('in') }, 0);
    // 짝 막대: 대역이 걸어감(같은 이름 = 같은 물체)
    const ghosts = [];
    bBars.forEach((m, j) => {
      const i = pairOf(j);
      if (i < 0 || !aBars[i]) return;
      const a = rectA(aBars[i]),
        b = rectB(m);
      const g = document.createElement('i');
      Object.assign(g.style, { position: 'absolute', left: `${a.x}px`, top: `${a.y}px`, width: `${a.w}px`, height: `${a.h}px`, backgroundColor: colorOf(ctx, i === hiA ? 'accent' : 'fg') });
      ctx.overlay.append(g);
      ghosts.push(g);
      ctx.initial(g, { autoAlpha: 0 });
      tl.set(g, { autoAlpha: 1 }, 0);
      tl.set(aBars[i], { autoAlpha: 0 }, 0);
      const at = d * (0.12 + 0.05 * ghosts.length);
      // 먼저 가로 막대 두께로 눕고(폭·높이 교환) 순위 자리로 이동
      tl.to(g, { left: b.x, top: b.y, width: b.w, height: b.h, backgroundColor: colorOf(ctx, j === hiB ? 'accent' : 'fg'), duration: d * 0.4 * R, ease: ctx.ease('inout') }, at);
      // 이름표도 같이 걸어감
      const la = A.part('label')[i],
        lb = B.part('label')[j];
      if (la && lb) {
        const ra = A.anchor('label', i).rect,
          rb = B.anchor('label', j).rect;
        const s = A.anchor('plot').rect.w / 1600 || 1; // SVG 안 이동은 viewBox 단위
        tl.to(la, { x: (rb.x - ra.x) / s, y: (rb.y + rb.h / 2 - (ra.y + ra.h / 2)) / s, duration: d * 0.4 * R, ease: ctx.ease('inout') }, at);
        tl.set(la, { autoAlpha: 0 }, d * 0.62);
      }
    });
    // B: 축·이름표, 짝 없는 막대는 기준선(왼쪽)에서 자람
    const support = [...B.part('axis'), ...B.part('baseline'), ...B.part('label')];
    ctx.initial(support, { autoAlpha: 0 });
    tl.to(support, { autoAlpha: 1, duration: d * 0.14 * R, ease: ctx.ease('out') }, d * 0.5);
    const horizontal = B.data.orient === 'h';
    const fresh = bBars.filter((_, j) => pairOf(j) < 0 || !aBars[pairOf(j)]);
    fresh.forEach((m, k) =>
      growBar(tl, ctx, m, { at: d * (0.5 + (0.22 * k) / Math.max(1, fresh.length)), duration: d * 0.2 * R, ease: ctx.ease('settle'), horizontal }),
    );
    const paired = bBars.filter((m) => !fresh.includes(m));
    ctx.initial(paired, { autoAlpha: 0 });
    tl.set(paired, { autoAlpha: 1 }, d * 0.9);
    tl.set(ghosts, { autoAlpha: 0 }, d * 0.9);
    const tags = valueTags(ctx, B);
    ctx.initial(tags, { autoAlpha: 0 });
    tl.to(tags, { autoAlpha: 1, duration: d * 0.1 * R, ease: ctx.ease('out'), stagger: d * 0.01 * R }, d * 0.76);
    const copy = ['title', 'dek', 'unit', 'note', 'source'].flatMap((n) => base(B.part(n)));
    ctx.initial(copy, { autoAlpha: 0, yPercent: 30 });
    tl.to(copy, { autoAlpha: 1, yPercent: 0, duration: d * 0.16 * R, ease: ctx.ease('settle') }, d * 0.3);
    finishLink(tl, ctx, { at: d, cross: 0, from: [ctx.handoff.from.node], to: [ctx.handoff.to.node] });
  },
};
