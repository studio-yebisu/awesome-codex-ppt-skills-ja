import { boot } from '../../engine/index.js';
import '../../engine/engine.css';
import moves from '../../moves/index.js';
import concept from '../../concepts/canvas/index.js';
import '../../concepts/canvas/tokens.css';
import '../../concepts/canvas/layout.css';
import deck from './deck.yaml';
import ground from './sequences/ground.js';
import atlas from './sequences/atlas.js';

boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  sequences: { ground, atlas },
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,
});
