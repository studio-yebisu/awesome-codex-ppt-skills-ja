/** Persistent depth ladder for zoom navigation. Used by zoom decks. */
import { colorOf } from '../_shared/color.js';
import { gridLayout } from '../_shared/grid.js';
import { px } from '../_shared/timeline.js';

export default {
  id: 'depth-ladder',
  family: 'emphasis',
  role: 'ambient',
  accepts: ['*'],
  sources: ['active-indicator-glide', 'progressive-disclosure', 'route-highlight'],
  reduce: 'fade',
  params: {
    rungs: { type: 'array', default: ['전체'], doc: '위에서 아래로 이어지는 경로 라벨' },
    level: { type: 'integer', default: 0, min: 0, max: 7, doc: '현재 깊이' },
    maxLevel: { type: 'integer', default: 0, min: 0, max: 7, doc: '지금까지 간 가장 깊은 칸' },
    appearAfter: { type: 'number', default: 0, min: 0, max: 4, doc: '나타나기 전 대기(u)' },
    side: { type: 'enum', default: 'left', values: ['left', 'right'], doc: '사다리 위치' },
  },
  timing: () => ({ duration: 'fill', stops: [] }),
  build(tl, ctx, params) {
    const x =
      params.side === 'right'
        ? ctx.viewport.w - px(ctx, ctx.tokens.ladderX ?? 72)
        : px(ctx, ctx.tokens.ladderX ?? 72);
    const top = px(ctx, ctx.tokens.ladderTop ?? 180),
      step = px(ctx, ctx.tokens.ladderStep ?? 32);
    // 초점을 뺏지 않게: accent 없음. 지금 칸만 fg, 지나온 칸은 muted, 갔다가 빠져나온 깊은 칸은 더 옅게.
    // 아직 가 보지 않은 칸은 그리지 않는다(경로는 파고든 만큼만 자란다)
    const rule = colorOf(ctx, 'rule'),
      fg = colorOf(ctx, 'fg'),
      muted = colorOf(ctx, 'fg-muted');
    const shown = Math.min(params.rungs.length, Math.max(params.level, params.maxLevel) + 1);
    const ladder = document.createElement('div');
    ladder.className = 'sl-depth-ladder';
    Object.assign(ladder.style, { position: 'absolute', left: `${x}px`, top: `${top}px`, opacity: '0' });
    const rail = document.createElement('i');
    Object.assign(rail.style, {
      position: 'absolute',
      left: '0',
      top: '0',
      height: `${Math.max(0, shown - 1) * step}px`,
      borderLeft: `1px solid ${rule}`,
    });
    ladder.append(rail);
    const cells = gridLayout({ n: shown, cols: 1, cell: step, origin: { x: 0, y: 0 } });
    const entries = cells.map(({ i, y }) => {
      const entry = document.createElement('div'),
        tick = document.createElement('i'),
        text = document.createElement('span');
      entry.className = 'sl-depth-ladder__rung';
      text.textContent = params.rungs[i] ?? '';
      const isCurrent = i === params.level,
        faded = i > params.level;
      Object.assign(entry.style, {
        position: 'absolute',
        top: `${y}px`,
        left: '0',
        display: 'flex',
        alignItems: 'center',
        whiteSpace: 'nowrap',
        translate: '0 -50%',
        opacity: String(faded ? 0.35 : 1),
        color: isCurrent ? fg : muted,
      });
      Object.assign(tick.style, {
        display: 'inline-block',
        width: `${px(ctx, isCurrent ? 12 : 6)}px`,
        marginRight: `${px(ctx, 10)}px`,
        borderTop: `1px solid ${isCurrent ? fg : rule}`,
        transformOrigin: 'left',
      });
      text.style.display = 'inline-block';
      entry.append(tick, text);
      ladder.append(entry);
      return { entry, tick, text, isCurrent };
    });
    ctx.overlay.append(ladder);
    ctx.initial(ladder, { autoAlpha: 0 });
    const at = params.appearAfter;
    // link로 들어오는 beat는 앞 beat 사다리가 끝나는 순간 그대로 이어받는다(깜빡임 없이). 첫 사다리만 서서히
    if (at > 0 && params.level > 0) tl.set(ladder, { autoAlpha: 1 }, at);
    else tl.to(ladder, { autoAlpha: 1, duration: 0.18, ease: ctx.ease('out') }, at);
    const current = entries.find((entry) => entry.isCurrent);
    if (current && params.level >= params.maxLevel) {
      ctx.initial(current.tick, { scaleX: 0 });
      ctx.initial(current.text, { clipPath: 'inset(0 100% 0 0)' });
      tl.to(current.tick, { scaleX: 1, duration: 0.2, ease: ctx.ease('out') }, at);
      tl.to(current.text, { clipPath: 'inset(0 0% 0 0)', duration: 0.3, ease: ctx.ease('out') }, at);
    }
  },
};
