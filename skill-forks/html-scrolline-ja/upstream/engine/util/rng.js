/**
 * 문자열 → 32bit 정수 seed(FNV-1a 32).
 * @param {string} s
 * @returns {number}
 */
export function hashSeed(s) {
  let hash = 0x811c9dc5;
  for (const char of String(s)) {
    hash ^= char.codePointAt(0);
    hash = Math.imul(hash, 0x01000193);
  }
  return hash >>> 0;
}

/**
 * mulberry32. 같은 seed → 같은 수열, 값은 [0, 1).
 * @param {number|string} seed  문자열이면 hashSeed
 * @returns {() => number}
 */
export function createRng(seed) {
  let state = typeof seed === 'string' ? hashSeed(seed) : Number(seed) >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let value = state;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}
