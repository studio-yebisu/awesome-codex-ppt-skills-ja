/** Folds a masked media glyph into one bar of the next chart.
 *  글리프 속 영상을 가로 띠로 잘라(글리프 허리) → 띠가 대상 막대 자리·길이로 접히고 → 막대 색으로 식는다.
 *  나머지 막대는 기준선에서 자라고, 값 표·제목이 뒤따른다. */
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { clearMask } from '../_shared/mask.js';

const inset = (r, W, H) => `inset(${r.y}px ${W - r.x - r.w}px ${H - r.y - r.h}px ${r.x}px)`;
export default {
  id: 'glyph-to-bar',
  family: 'morph',
  role: 'link',
  accepts: ['chart'],
  sources: ['text-cutout-zoom', 'shape-morph', 'bar-grow'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 0.8, max: 4, doc: '전체 길이(u)' },
    toIndex: { type: 'integer', default: 0, min: 0, max: 40, doc: 'B 쪽 대상 막대 index' },
    band: { type: 'number', default: 0.5, min: 0.2, max: 0.8, doc: '처음 자를 띠의 세로 위치(영상 높이 비율)' },
  },
  handoff(p) {
    return { from: { part: 'frame' }, to: { part: 'mark', index: p.toIndex } };
  },
  timing: (p) => ({ duration: p.duration ?? 2.4, stops: [] }),
  build(tl, ctx, p) {
    const { from, to } = ctx.handoff,
      d = p.duration,
      R = ctx.reduce ? 0.001 : 1,
      A = ctx.from,
      B = ctx.beat,
      fr = from.rect,
      W = fr.w,
      H = fr.h;
    const bar = { x: to.rect.x - fr.x, y: to.rect.y - fr.y, w: to.rect.w, h: to.rect.h };
    const mid = { x: W * 0.12, y: H * p.band - bar.h / 2, w: W * 0.76, h: bar.h };
    const caption = [...A.part('caption'), ...A.part('credit')];
    const media = A.part('media');
    const bars = B.part('mark').filter((m) => m.dataset.series === '0' && m.tagName.toLowerCase() !== 'path');
    const others = bars.filter((m) => m !== to.node);
    const horizontal = B.data.orient === 'h';
    ctx.initial(from.node, { clipPath: inset({ x: 0, y: 0, w: W, h: H }, W, H), autoAlpha: 1 });
    ctx.initial(caption, { autoAlpha: 1 });
    tl.to(caption, { autoAlpha: 0, duration: d * 0.1 * R, ease: ctx.ease('in') }, 0);
    // ① 글리프 허리를 가로 띠로
    tl.to(from.node, { clipPath: inset(mid, W, H), duration: d * 0.3 * R, ease: ctx.ease('inout') }, d * 0.05);
    // ② 마스크를 걷고 띠가 막대 자리·길이로
    clearMask(tl, media[0] ?? from.node, d * 0.36);
    tl.to(from.node, { clipPath: inset(bar, W, H), duration: d * 0.26 * R, ease: ctx.ease('inout') }, d * 0.36);
    // ③ 영상 띠 → 주홍 막대
    tl.to(from.node, { autoAlpha: 0, duration: d * 0.12 * R, ease: ctx.ease('in') }, d * 0.62);
    // B: 축·이름표, 나머지 막대는 기준선에서
    const support = [...B.part('axis'), ...B.part('baseline'), ...B.part('label')];
    ctx.initial(support, { autoAlpha: 0 });
    tl.to(support, { autoAlpha: 1, duration: d * 0.12 * R, ease: ctx.ease('out') }, d * 0.55);
    // SVG 막대는 속성으로 자람(GSAP transform은 CSS scale을 지움)
    others.forEach((m, k) => {
      const a = (key) => Number(m.getAttribute(key));
      const neg = m.dataset.sign === 'neg';
      const to = horizontal ? { x: a('x'), width: a('width') } : { y: a('y'), height: a('height') };
      const from = horizontal ? (neg ? { x: a('x') + a('width'), width: 0 } : { width: 0 }) : neg ? { height: 0 } : { y: a('y') + a('height'), height: 0 };
      ctx.initial(m, { attr: from });
      tl.to(m, { attr: to, duration: d * 0.16 * R, ease: ctx.ease('settle') }, d * (0.66 + (0.16 * k) / Math.max(1, others.length)));
    });
    const tags = valueTagsLite(ctx, B);
    ctx.initial(tags, { autoAlpha: 0 });
    tl.to(tags, { autoAlpha: 1, duration: d * 0.08 * R, stagger: d * 0.01 * R }, d * 0.8);
    const copy = ['title', 'dek', 'unit', 'source'].flatMap((n) => B.part(n)).filter((n) => (n.dataset.state ?? 'base') === 'base');
    ctx.initial(copy, { autoAlpha: 0, yPercent: 30 });
    tl.to(copy, { autoAlpha: 1, yPercent: 0, duration: d * 0.14 * R, ease: ctx.ease('settle') }, d * 0.7);
    finishLink(tl, ctx, { at: d * 0.72, cross: 0.1, from: [from.node], to: [to.node] });
  },
};

/** 막대 값 표(morph family는 data family를 import할 수 없어 같은 규칙을 짧게 둠). */
function valueTagsLite(ctx, beat) {
  const values = beat.data.series[0].values,
    unit = beat.data.unit ?? '',
    hi = beat.data.highlight?.index,
    px = (n) => n * ctx.viewport.px;
  const marks = beat.part('mark').filter((m) => m.dataset.series === '0');
  return marks.map((m, i) => {
    const r = beat.anchor('mark', beat.part('mark').indexOf(m)).rect,
      v = values[i],
      neg = v < 0,
      strong = i === hi;
    const node = document.createElement('span');
    node.className = 'sl-data-tag';
    const inner = document.createElement('span');
    inner.textContent = `${new Intl.NumberFormat('ko', { maximumFractionDigits: 1 }).format(v)}${unit}`;
    Object.assign(inner.style, { position: 'absolute', left: '0', top: '0', translate: neg ? '-100% -50%' : '0 -50%', whiteSpace: 'nowrap' });
    node.append(inner);
    Object.assign(node.style, {
      position: 'absolute',
      left: `${neg ? r.x - px(12) : r.x + r.w + px(12)}px`,
      top: `${r.y + r.h / 2}px`,
      width: '0',
      height: '0',
      fontFamily: '"Pretendard Variable", Pretendard, system-ui, sans-serif',
      fontVariantNumeric: 'tabular-nums',
      fontWeight: strong ? '800' : '600',
      fontSize: `${px(strong ? 34 : 26)}px`,
      color: colorOf(ctx, strong ? 'accent' : 'fg'),
    });
    ctx.overlay.append(node);
    return node;
  });
}
