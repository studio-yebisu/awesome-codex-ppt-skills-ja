/** Word-part discovery and ghost splitting. */
import { words } from '../../engine/index.js';
import { ghost } from './link.js';
export function wordsIn(beat, partName) {
  const roots = beat.part(partName);
  const found = roots.flatMap((node) => [...node.querySelectorAll('[data-part="word"]')]);
  return found.length ? found : beat.part('word');
}
export function ghostWords(ctx, node, rect) {
  const copy = ghost(ctx, node, rect);
  const text = copy.textContent ?? '';
  copy.replaceChildren();
  return words(copy, text);
}
