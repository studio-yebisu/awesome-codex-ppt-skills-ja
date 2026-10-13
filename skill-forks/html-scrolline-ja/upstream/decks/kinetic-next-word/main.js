import { boot } from '../../engine/index.js';
import '../../engine/engine.css';
import moves from '../../moves/index.js';
import concept from '../../concepts/kinetic/index.js';
import '../../concepts/kinetic/tokens.css';
import '../../concepts/kinetic/layout.css';
import deck from './deck.yaml';

boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,
});
