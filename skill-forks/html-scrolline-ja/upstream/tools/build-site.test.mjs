import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import {
  brokenLinks,
  captureTimes,
  clipWindow,
  conceptPalette,
  deckMoves,
  esc,
  parseArgs,
  pickEvenly,
  renderIndex,
  renderMoves,
  t,
} from './build-site.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const content = JSON.parse(fs.readFileSync(path.join(ROOT, 'site/content.json'), 'utf8'));
const catalog = fs
  .readFileSync(path.join(ROOT, 'plan/moves.catalog.jsonl'), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((l) => JSON.parse(l));
const lines = JSON.parse(fs.readFileSync(path.join(ROOT, 'site/data/moves.lines.json'), 'utf8'));
const fakeDecks = (preview = { kind: 'none' }) =>
  content.decks.map((d) => ({
    ...d,
    title: { ko: d.id, en: d.title.en },
    sample: true,
    palette: { bg: '#000', fg: '#fff', accent: '#f50' },
    moveCount: 3,
    built: true,
    preview,
  }));

describe('build-site helpers', () => {
  it('parses flags', () => {
    expect(parseArgs([])).toMatchObject({ decks: true, capture: true, recapture: false, out: 'out/site' });
    expect(parseArgs(['--no-decks', '--no-capture', '--decks', 'a,b'])).toMatchObject({
      decks: false,
      capture: false,
      only: ['a', 'b'],
    });
    expect(() => parseArgs(['--nope'])).toThrow(/unknown option/);
  });

  it('escapes html and pairs languages', () => {
    expect(esc('<a href="x">&</a>')).toBe('&lt;a href=&quot;x&quot;&gt;&amp;&lt;/a&gt;');
    expect(t({ ko: '덱', en: 'Deck' })).toBe(
      '<span class="ko" lang="ko">덱</span><span class="en" lang="en">Deck</span>',
    );
    expect(t({ ko: 'scrub', en: 'scrub' })).toBe('scrub');
    expect(t({ en: 'only' })).toBe('only');
  });

  it('picks evenly with both ends', () => {
    expect(pickEvenly([1, 2, 3], 6)).toEqual([1, 2, 3]);
    expect(pickEvenly([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4)).toEqual([1, 4, 7, 10]);
  });

  it('reads the concept palette from tokens.css', () => {
    expect(
      conceptPalette(
        '.sl-concept-x {\n  --sl-bg: #efe9dd;\n  --sl-fg: #17140f;\n  --sl-fg-muted: #666;\n  --sl-accent: #8a5a1f;\n}',
      ),
    ).toEqual({
      bg: '#efe9dd',
      fg: '#17140f',
      accent: '#8a5a1f',
    });
    for (const d of content.decks) {
      const css = fs.readFileSync(path.join(ROOT, 'concepts', d.concept, 'tokens.css'), 'utf8');
      expect(conceptPalette(css).bg).toMatch(/^#/);
    }
  });

  it('counts distinct non-engine moves in a deck yaml', () => {
    const yaml =
      'enter: { move: line-mask-rise }\nexit: { move: "engine:fade-out" }\nlink: { move: zoom-dive }\nenter: { move: line-mask-rise }';
    expect(deckMoves(yaml)).toEqual(['line-mask-rise', 'zoom-dive']);
  });

  it('keeps the clip window inside the video', () => {
    expect(clipWindow(60, 0.5, 8)).toEqual({ start: 30, len: 8 });
    expect(clipWindow(60, 0.99, 8)).toEqual({ start: 52, len: 8 });
    expect(clipWindow(5, 0.3, 8)).toEqual({ start: 0, len: 5 });
  });

  it('samples capture times between two 1-based stops, clamped', () => {
    const stops = [{ t: 1 }, { t: 3 }, { t: 7 }];
    expect(captureTimes(stops, 1, 3, 5)).toEqual([1, 2.5, 4, 5.5, 7]);
    expect(captureTimes(stops, 2, 9, 2)).toEqual([3, 7]);
    expect(captureTimes([], 1, 2, 3)).toEqual([]);
  });

  it('flags absolute, escaping and missing local links', () => {
    const out = '/site';
    const exists = (p) => ['/site/index.html', '/site/moves/index.html', '/site/assets/a.css'].includes(p);
    const html =
      '<a href="moves/"></a><link href="assets/a.css"><a href="/x"></a><img src="../up.png"><a href="#how"></a><a href="https://e.com"></a><img src="gone.jpg">';
    expect(brokenLinks(html, '/site', out, exists)).toEqual([
      '/x (absolute path breaks under a sub-path)',
      '../up.png (outside site)',
      '../up.png',
      'gone.jpg',
    ]);
  });
});

describe('pages', () => {
  it('index shows the six decks first, every link relative', () => {
    const html = renderIndex(
      content,
      fakeDecks(),
      content.how.items.map(() => ({ kind: 'none' })),
      '/site',
    );
    const decks = html.indexOf('class="decks"');
    expect(decks).toBeGreaterThan(0);
    expect(decks).toBeLessThan(html.indexOf('id="how"'));
    expect(html.match(/<li class="deck/g)).toHaveLength(6);
    for (const d of content.decks) expect(html).toContain(`href="decks/${d.id}/"`);
    expect(html).not.toMatch(/\s(?:href|src)="\/(?!\/)/);
  });

  it('index uses video previews when a clip exists', () => {
    const clip = { kind: 'video', src: '/site/media/x.mp4', poster: '/site/media/x.jpg' };
    const html = renderIndex(
      content,
      fakeDecks(clip),
      content.how.items.map(() => clip),
      '/site',
    );
    expect(html.match(/<video muted loop playsinline/g)).toHaveLength(9);
    expect(html).toContain('src="media/x.mp4"');
  });

  it('moves page lists all 80 moves with KO/EN lines and family filters', () => {
    const html = renderMoves(content, catalog, lines, fakeDecks());
    expect(html.match(/<li class="move"/g)).toHaveLength(catalog.length);
    expect(catalog.length).toBe(80);
    for (const f of Object.keys(content.movesPage.families)) expect(html).toContain(`data-family="${f}"`);
    expect(Object.keys(lines).sort()).toEqual(catalog.map((m) => m.id).sort());
    expect(html).toContain('href="../decks/rail-ai-decade/"');
    expect(html).not.toMatch(/\s(?:href|src)="\/(?!\/)/);
  });

  it('home link is explicit and the moves search sits in the page head', () => {
    const index = renderIndex(content, fakeDecks(), content.how.items.map(() => ({ kind: 'none' })), '/site');
    expect(index).toContain('<a class="brand" href="./">');
    const moves = renderMoves(content, catalog, lines, fakeDecks());
    expect(moves.indexOf('class="search"')).toBeLessThan(moves.indexOf('class="filters"'));
    expect(moves).toContain('<a class="brand" href="../">');
  });

  it('no emoji in site copy', () => {
    const text = JSON.stringify(content) + JSON.stringify(lines);
    expect(text).not.toMatch(/\p{Extended_Pictographic}/u);
  });
});
