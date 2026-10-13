/**
 * 레일 초점: 「지금」 선에 선 사건 하나만 줄기·제목·설명·썸네일·날짜·출처를 보이고, 나머지는 점만 남긴다(촘촘한 해에 날짜끼리 겹침).
 * `now` part가 없는 chronology(전체 레일)는 건드리지 않는다.
 */
export const RAIL_DETAIL = ['stem', 'title', 'note', 'media', 'date', 'source'];

/** event i 안의 상세 part 요소들 */
export function eventDetail(beat, index) {
  const event = beat.part('event')[index];
  if (!event) return [];
  return [...event.querySelectorAll('[data-part]')].filter((node) => RAIL_DETAIL.includes(node.dataset.part));
}

/**
 * focus 밖 사건들의 상세를 ctx.initial로 숨긴다. 숨긴 요소를 돌려준다.
 * @param {object} ctx  move ctx(initial·skipNodes)
 * @param {object} beat  BeatInstance(chronology)
 * @param {number} focus  남길 사건 순번
 */
export function railFocus(ctx, beat, focus) {
  if (!beat.part('now').length) return [];
  const skip = ctx.skipNodes ?? [];
  const hidden = beat
    .part('event')
    .flatMap((_, index) => (index === focus ? [] : eventDetail(beat, index)))
    .filter((node) => !skip.includes(node));
  if (hidden.length) ctx.initial(hidden, { autoAlpha: 0 });
  return hidden;
}
