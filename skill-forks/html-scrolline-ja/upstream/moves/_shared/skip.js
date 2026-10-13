/**
 * A beat part minus what a link handed over: skipParts drops the whole part, skipNodes drops the handed
 * element and everything inside it (C5 skip rule — enter/step must not set or tween them).
 */
export function partFree(ctx, name) {
  if (ctx.skipParts.includes(name)) return [];
  const skip = ctx.skipNodes ?? [];
  return ctx.beat.part(name).filter((node) => !skip.some((s) => s === node || s.contains(node)));
}
