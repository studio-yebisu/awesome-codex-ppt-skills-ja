#!/usr/bin/env node
/** Scrolline deck helper (CONTRACTS C3, C15, C16). */
import fs from 'node:fs';
import { printMediaNotice } from './lib/media-notice.mjs';
import { register } from 'node:module';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parse } from 'yaml';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ID = /^[a-z0-9][a-z0-9-]*$/;
// plan은 내부 덱(`_smoke`)도 받는다(C3 DECK_ID_PATTERN). new는 공개 덱 이름만.
const DECK_ID = /^_?[a-z0-9][a-z0-9-]*$/;
const option = (args, name) => {
  const index = args.indexOf(name);
  return index < 0 ? undefined : args[index + 1];
};

/** `layout` = 컨셉에 concepts/<id>/layout.css가 있으면 true(C11 v2.2, tokens.css 다음에 import). */
export function deckTemplate(id, concept, layout = false) {
  const layoutImport = layout ? `import '../../concepts/${concept}/layout.css';\n` : '';
  return {
    yaml: `id: ${id}\ntitle: "${id}"\nlang: ko\nconcept: ${concept}\nsample: false\nsources: []\nbeats: []\n`,
    html: `<!doctype html>\n<html lang="ko"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>${id}</title></head><body><div id="app"></div><script type="module" src="./main.js"></script></body></html>\n`,
    main: `import { boot } from '../../engine/index.js';\nimport '../../engine/engine.css';\nimport moves from '../../moves/index.js';\nimport concept from '../../concepts/${concept}/index.js';\nimport '../../concepts/${concept}/tokens.css';\n${layoutImport}import deck from './deck.yaml';\n\nboot({\n  host: document.getElementById('app'),\n  deck,\n  concept,\n  moves,\n  assetBase: new URL('./', document.baseURI).href,\n  mode: import.meta.env.SCROLLINE_MODE,\n});\n`,
  };
}

export function createDeck(id, concept, root = ROOT) {
  if (!ID.test(id) || !ID.test(concept)) throw new Error('deck and concept ids must be lowercase kebab-case');
  const dir = path.join(root, 'decks', id);
  if (fs.existsSync(dir)) throw new Error(`Deck already exists: ${id}`);
  const files = deckTemplate(id, concept, fs.existsSync(path.join(root, 'concepts', concept, 'layout.css')));
  fs.mkdirSync(path.join(dir, 'assets'), { recursive: true });
  for (const [name, body] of Object.entries(files))
    fs.writeFileSync(
      path.join(dir, name === 'yaml' ? 'deck.yaml' : name === 'html' ? 'index.html' : 'main.js'),
      body,
    );
  return dir;
}

export function moveRows(registry, filters = {}) {
  return registry
    .ids()
    .map((id) => registry.get(id))
    .filter((m) => !filters.family || m.family === filters.family)
    .filter((m) => !filters.role || m.role === filters.role)
    .map((m) => `${m.id}\t${m.family}\t${m.role}`);
}

/**
 * main.js가 boot에 넘기는 sequences와 같은 것: `import <use> from './sequences/<file>.js'`.
 * sequence 모듈이 deck.yaml을 import할 수 있어 yaml 로더 hook을 먼저 건다.
 */
async function deckSequences(root, id) {
  const main = path.join(root, 'decks', id, 'main.js');
  if (!fs.existsSync(main)) return {};
  const entries = [
    ...fs.readFileSync(main, 'utf8').matchAll(/import\s+(\w+)\s+from\s+['"]\.\/sequences\/([\w-]+\.js)['"]/g),
  ];
  if (!entries.length) return {};
  register('./lib/yaml-hook.mjs', import.meta.url);
  const mods = await Promise.all(
    entries.map(([, , file]) => import(pathToFileURL(path.join(root, 'decks', id, 'sequences', file)).href)),
  );
  return Object.fromEntries(entries.map(([, name], i) => [name, mods[i].default]));
}

async function loadMoves(root) {
  return (await import(pathToFileURL(path.join(root, 'moves/index.js')).href)).default;
}

export async function run(
  argv = process.argv.slice(2),
  { root = ROOT, out = console.log, err = console.error } = {},
) {
  const [command, id] = argv;
  if (command === 'new') {
    const concept = option(argv, '--concept');
    if (!id || !concept) throw new Error('new requires <deckId> --concept <id>');
    out(createDeck(id, concept, root));
    printMediaNotice();
    return 0;
  }
  if (command === 'moves') {
    for (const row of moveRows(await loadMoves(root), {
      family: option(argv, '--family'),
      role: option(argv, '--role'),
    }))
      out(row);
    return 0;
  }
  if (command === 'plan') {
    if (!id || !DECK_ID.test(id)) throw new Error('plan requires a valid <deckId>');
    const deck = parse(fs.readFileSync(path.join(root, 'decks', id, 'deck.yaml'), 'utf8'));
    const [moves, conceptMod, timeline, beats, schema, sequences] = await Promise.all([
      loadMoves(root),
      import(pathToFileURL(path.join(root, 'concepts', deck.concept, 'index.js')).href),
      import(pathToFileURL(path.join(root, 'engine/timeline.js')).href),
      import(pathToFileURL(path.join(root, 'engine/beats/index.js')).href),
      import(pathToFileURL(path.join(root, 'engine/deck-schema.js')).href),
      deckSequences(root, id),
    ]);
    const env = { registry: moves, concept: conceptMod.default, beatTypes: beats.beatTypes, sequences };
    const validation = schema.validateDeck(deck, env);
    if (!validation.ok) {
      for (const e of validation.errors) err(`${e.path}: ${e.message}`);
      return 1;
    }
    out(JSON.stringify(timeline.plan(deck, env), null, 2));
    return 0;
  }
  err(
    'Usage: cli.mjs new <deckId> --concept <id> | moves [--family <family>] [--role <role>] | plan <deckId>',
  );
  return 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  run()
    .then((code) => {
      process.exitCode = code;
    })
    .catch((error) => {
      console.error(error.message);
      process.exitCode = 1;
    });
}
