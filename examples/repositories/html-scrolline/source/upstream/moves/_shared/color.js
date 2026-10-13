/** Resolve concrete stage colors, never CSS variable strings. */
const FALLBACKS = {
  fg: '#ffffff',
  bg: '#000000',
  accent: '#ffb000',
  'accent-2': '#4cc9f0',
  'fg-muted': '#8a8a8a',
  rule: '#444444',
  scrim: 'rgba(0,0,0,0.55)',
};
export function colorOf(ctx, name) {
  const own = ctx.colors?.[name];
  const css = globalThis.getComputedStyle?.(ctx.stage.root).getPropertyValue(`--sl-${name}`).trim();
  const value = own || css || FALLBACKS[name] || FALLBACKS.fg;
  return value.includes(`var${'('}`) ? (FALLBACKS[name] ?? FALLBACKS.fg) : value;
}
