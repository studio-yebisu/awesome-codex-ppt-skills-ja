/** Deterministic numeric text tweening. */
import { driveValue } from './drive.js';

export function formatNumber(v, { lang = 'ko', decimals = 0, prefix = '', suffix = '' } = {}) {
  return `${prefix}${new Intl.NumberFormat(lang, { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(v)}${suffix}`;
}
export function countTo(tl, node, { from, to, at, duration, ease, lang, decimals, prefix, suffix }) {
  node.textContent = formatNumber(from, { lang, decimals, prefix, suffix });
  driveValue(tl, (v) => (node.textContent = formatNumber(v, { lang, decimals, prefix, suffix })), {
    from,
    to,
    at,
    duration,
    ease,
  });
  tl.set(node, { textContent: formatNumber(to, { lang, decimals, prefix, suffix }) }, at + duration);
}
