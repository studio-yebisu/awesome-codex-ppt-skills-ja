import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import { deckYaml } from './tools/vite/deck-plugin.js';

const ROOT = path.dirname(fileURLToPath(import.meta.url));

/** decks/<id>/index.html 전부 → 다중 페이지 입력 */
function deckInputs(root = ROOT) {
  const dir = path.join(ROOT, 'decks');
  const ids = fs.existsSync(dir)
    ? fs.readdirSync(dir).filter((d) => fs.existsSync(path.join(dir, d, 'index.html')))
    : [];
  return Object.fromEntries(ids.map((d) => [d, path.join(dir, d, 'index.html')]));
}

const selectedDeck = process.env.SCROLLINE_DECK;
const selectedRoot = selectedDeck ? path.join(ROOT, 'decks', selectedDeck) : ROOT;

export default defineConfig({
  // A selected deck is a standalone composition: keeping its own index.html as
  // Vite's root prevents Rollup from reproducing `decks/<id>/` under outDir.
  root: selectedRoot,
  base: './',
  plugins: [deckYaml()],
  define: { 'import.meta.env.SCROLLINE_MODE': JSON.stringify(process.env.SCROLLINE_MODE || 'live') },
  build: {
    outDir: process.env.SCROLLINE_OUT || path.join(ROOT, 'out', 'build'),
    emptyOutDir: true,
    assetsInlineLimit: 0,
    rollupOptions: { input: selectedDeck ? path.join(selectedRoot, 'index.html') : deckInputs() },
  },
});
