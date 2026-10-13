import { EVENTS } from './constants.js';

/**
 * @param {{ search?: string, matchMedia?: (q: string) => { matches: boolean } }} [env]  테스트 주입용
 * @returns {boolean}
 */
export function prefersReducedMotion(env) {
  const search = env?.search ?? globalThis.location?.search ?? '';
  if (new URLSearchParams(search).get('motion') === 'reduce') return true;
  const matchMedia = env?.matchMedia ?? globalThis.matchMedia;
  return Boolean(matchMedia?.('(prefers-reduced-motion: reduce)').matches);
}

/**
 * @param {{ stage: import('./types.js').Stage, beats: import('./types.js').BeatInstance[], target?: EventTarget }} opts
 * @returns {{ announce: (text: string) => void, destroy: () => void }}
 */
export function createA11y(opts) {
  const { stage, beats, target = window } = opts;
  const live = document.createElement('div');
  live.className = 'sl-sr-only sl-live';
  live.setAttribute('aria-live', 'polite');
  live.setAttribute('aria-atomic', 'true');
  const transcript = document.createElement('ol');
  transcript.className = 'sl-sr-only sl-transcript';
  transcript.setAttribute('aria-label', 'Presentation transcript');
  for (const beat of beats) {
    const item = document.createElement('li');
    item.textContent = textFor(beat);
    transcript.append(item);
  }
  stage.root.append(live, transcript);
  const byId = new Map(beats.map((beat) => [beat.id, beat]));
  const announce = (text) => {
    live.textContent = '';
    live.textContent = text;
  };
  const onStop = (event) => {
    const beat = byId.get(event.detail?.beat);
    if (beat) announce(textFor(beat));
  };
  const onActive = (event) => {
    const beat = byId.get(event.detail?.beat);
    if (!beat) return;
    const leaving = event.detail.phase === 'leave';
    beat.root.inert = leaving;
    beat.root.toggleAttribute('inert', leaving);
  };
  target.addEventListener(EVENTS.stop, onStop);
  target.addEventListener(EVENTS.active, onActive);
  return {
    announce,
    destroy() {
      target.removeEventListener(EVENTS.stop, onStop);
      target.removeEventListener(EVENTS.active, onActive);
      live.remove();
      transcript.remove();
    },
  };
}

function textFor(beat) {
  return (beat.root?.textContent || '').replace(/\s+/g, ' ').trim();
}
