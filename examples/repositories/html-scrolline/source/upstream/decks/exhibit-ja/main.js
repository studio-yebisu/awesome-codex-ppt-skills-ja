import { boot } from '../../engine/index.js';
import '../../engine/engine.css';
import moves from '../../moves/index.js';
import concept from '../../concepts/rail/index.js';
import '../../concepts/rail/tokens.css';
import '../../concepts/rail/layout.css';
import deck from './deck.yaml';
import './japanese.css';

// Default to the first original stop before boot; survives the original font rebuild.
const query = new URLSearchParams(location.search);
if (!query.has("stop") && !query.has("t")) { const u = new URL(location.href); u.searchParams.set("stop", "opening"); history.replaceState(null, "", u); }
boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,
});
