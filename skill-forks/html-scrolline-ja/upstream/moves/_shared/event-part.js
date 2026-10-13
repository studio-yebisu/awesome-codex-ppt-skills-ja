/**
 * chronology part 순번 변환. dot·stem·date·title·event는 사건마다 하나라 사건 순번 = part 순번이지만,
 * media·note·source는 그 필드가 있는 사건에만 생겨 part 배열이 더 짧다(C4).
 * 사건 순번을 anchor index로 바꾼다. 그 사건에 part가 없으면 순번을 그대로 둔다(덱 오류는 anchorOf가 던진다).
 */
const SPARSE = ['media', 'note', 'source'];

/**
 * @param {Array<object>} events  chronology data.events
 * @param {string} part
 * @param {number} eventIndex  음수 = 뒤에서(-1 = 마지막 사건)
 * @returns {{ part: string, index: number }}
 */
export function eventPart(events = [], part, eventIndex) {
  const n = events.length;
  const at = eventIndex < 0 ? n + eventIndex : eventIndex;
  if (!SPARSE.includes(part) || at < 0 || at >= n) return { part, index: eventIndex };
  if (events[at]?.[part] == null) return { part, index: eventIndex };
  return { part, index: events.slice(0, at).filter((event) => event?.[part] != null).length };
}
