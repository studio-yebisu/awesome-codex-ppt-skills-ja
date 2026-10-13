import { defineConfig } from 'vitest/config';
import { deckYaml } from './tools/vite/deck-plugin.js';

export default defineConfig({
  plugins: [deckYaml()],
  // 테스트는 사전 번들이 필요 없다. 기본값은 레포 전체 html(media-hf·out·site)을 훑어 /mnt/d에서 느리고 three 경고를 낸다.
  optimizeDeps: { noDiscovery: true, include: [] },
  test: {
    environment: 'happy-dom',
    // happy-dom을 파일마다 새로 만들던 비용이 전체 시간의 95%(141회·/mnt/d). vmThreads는 워커당 1회 만들고
    // 파일마다 새 VM 컨텍스트로 격리는 유지한다.
    pool: 'vmThreads',
    include: ['{engine,moves,concepts,decks,tools}/**/*.test.{js,mjs}'],
    exclude: ['**/node_modules/**', '**/__fixtures__/**', 'out/**'],
    passWithNoTests: false,
  },
});
