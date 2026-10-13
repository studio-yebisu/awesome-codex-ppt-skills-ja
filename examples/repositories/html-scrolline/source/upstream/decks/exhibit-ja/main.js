import { boot } from '../../engine/index.js';
import '../../engine/engine.css';
import moves from '../../moves/index.js';
import concept from '../../concepts/rail/index.js';
import '../../concepts/rail/tokens.css';
import '../../concepts/rail/layout.css';
import deck from './deck.yaml';
import './japanese.css';

boot({
  host: document.getElementById('app'),
  deck,
  concept,
  moves,
  assetBase: new URL('./', document.baseURI).href,
  mode: import.meta.env.SCROLLINE_MODE,
}).then((session) => {
  const query = new URLSearchParams(location.search);
  if (session.driver && !query.has("stop") && !query.has("t")) session.driver.seek(session.map.stops[0].t, { immediate: true });
});
