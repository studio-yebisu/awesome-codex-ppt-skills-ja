/** Precomputed glyph tables and seek-safe scramble rendering. */
export function scrambleTable(rng, length, frames, glyphs) {
  const chars = [...glyphs];
  return Array.apply(null, { length: frames }).map(() =>
    Array.apply(null, { length })
      .map(() => chars[Math.floor(rng() * chars.length)] ?? '')
      .join(''),
  );
}
export function scrambleAt(from, to, p, table) {
  if (p <= 0) return from;
  if (p >= 1) return to;
  const fixed = Math.floor(p * to.length),
    row = table[Math.min(table.length - 1, Math.max(0, Math.floor(p * (table.length - 1))))] ?? '';
  const width = Math.max(from.length, to.length);
  return Array.apply(null, { length: width })
    .map((_, i) => (i < fixed ? (to[i] ?? '') : (row[i] ?? from[i] ?? '')))
    .join('');
}
