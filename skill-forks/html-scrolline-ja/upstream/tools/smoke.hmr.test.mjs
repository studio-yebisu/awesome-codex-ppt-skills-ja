// @vitest-environment node
import { expect, it } from 'vitest';
import { HMR_FREEZE, parseArgs } from './smoke.mjs';

// 회귀: 다른 에이전트가 파일을 저장하면 Vite가 탭을 새로 고쳐 window.__smoke가 사라졌다("reading 'at'").
it('drops Vite reload/update messages on the HMR socket only', () => {
  class FakeSocket {
    constructor(url, protocols) {
      this.url = url;
      this.protocols = protocols;
      this.listeners = [];
    }
    addEventListener(type, fn) {
      this.listeners.push({ type, fn });
    }
    emit(type, data) {
      for (const l of this.listeners) if (l.type === type) l.fn({ data });
    }
  }
  const window = { WebSocket: FakeSocket };
  new Function('window', HMR_FREEZE)(window);
  new Function('window', HMR_FREEZE)(window); // 두 번 주입해도 한 겹

  const got = [];
  const hmr = new window.WebSocket('ws://localhost:5190/', 'vite-hmr');
  hmr.addEventListener('message', ({ data }) => got.push(data.startsWith('{') ? JSON.parse(data).type : data));
  for (const type of ['connected', 'full-reload', 'update', 'prune', 'custom']) hmr.emit('message', JSON.stringify({ type }));
  hmr.emit('message', 'not json');
  expect(got).toEqual(['connected', 'custom', 'not json']);

  const other = [];
  const app = new window.WebSocket('ws://example/', ['chat']);
  app.addEventListener('message', ({ data }) => other.push(data));
  app.emit('message', JSON.stringify({ type: 'full-reload' }));
  expect(other).toHaveLength(1);
});

it('accepts --out for a run that must not overwrite the deck owner shots', () => {
  expect(parseArgs(['rail-ai-decade', '--shots', '--out', '/tmp/x'])).toMatchObject({ out: '/tmp/x', driver: 'chrome' });
  expect(parseArgs(['rail-ai-decade']).out).toBeNull();
});

// 회귀(canvas 통합): 부팅이 15초를 넘으면 맨 engine.boot로 대신 띄워 덱의 sequences가 빠져 검증 실패했다.
it('waits for the page boot and retries main.js instead of a bare engine boot', async () => {
  const { probeSource, BOOT_WAIT_MS } = await import('./smoke.mjs');
  const src = probeSource('canvas-pitch');
  expect(BOOT_WAIT_MS).toBeGreaterThanOrEqual(60000);
  expect(src).toContain(`const BOOT_WAIT_MS = ${BOOT_WAIT_MS};`);
  expect(src).toContain("'/decks/' + DECK + '/main.js'");
  expect(src).not.toContain('engine.boot(');
  expect(() => new Function(src)).not.toThrow();
});

// 회귀(rail 보고): 부하 때 media가 그려지기 전에 찍어 시트에 가짜 빈 칸이 나왔다.
it('waits for visible media before measuring and reports what never painted', async () => {
  const { probeSource, MEDIA_WAIT_MS, summarize, formatReport } = await import('./smoke.mjs');
  const src = probeSource('rail-ai-decade');
  expect(MEDIA_WAIT_MS).toBeGreaterThanOrEqual(10000);
  expect(src).toContain('mediaSettled(MEDIA_WAIT_MS)');
  expect(src).toContain('readyState < 2');
  expect(src).toContain("c.dataset.drawn !== c.dataset.frame");
  const stop = { index: 0, name: 'b-title', beat: 'b-title', t: 1, errors: [], visibleBeats: ['b-title'], overlaps: [], clipped: [], minFont: 20, mediaPending: ['video a.mp4'] };
  const report = { deck: 'd', driver: 'chrome', viewport: { w: 1920, h: 1080 }, stops: [stop] };
  expect(summarize(report)).toMatchObject({ errors: 0, mediaPending: ['b-title'] });
  expect(formatReport(report)).toContain('media wait video a.mp4');
});
