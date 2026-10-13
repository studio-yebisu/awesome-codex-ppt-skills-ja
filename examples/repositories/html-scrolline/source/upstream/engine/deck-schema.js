/** Deck shape validation and C3 content audit. */
import {
  BASE_STATE,
  BEAT_TYPES,
  DECK_ID_PATTERN,
  ID_PATTERN,
  NO_MOVE,
  PLACEHOLDER_PATTERNS,
  SOURCED_TYPES,
  TONE_RANGE,
} from './constants.js';
import { validateSchema } from './util/schema.js';

const issue = (errors, path, message) => errors.push({ path, message });
function walkStrings(value, path, errors) {
  if (typeof value === 'string') {
    if (PLACEHOLDER_PATTERNS.some((pattern) => pattern.test(value)))
      issue(errors, path, 'placeholder text is not allowed');
  } else if (Array.isArray(value))
    value.forEach((item, index) => walkStrings(item, `${path}[${index}]`, errors));
  else if (value && typeof value === 'object')
    Object.entries(value).forEach(([key, item]) => walkStrings(item, `${path}.${key}`, errors));
}
function defaultMove(beat, role, concept, isLast = false) {
  if (beat[role]) return beat[role];
  // The final screen remains visible unless its author explicitly supplied an exit.
  if (role === 'exit' && isLast) return null;
  const move = concept.defaults?.byType?.[beat.type]?.[role] ?? concept.defaults?.[role];
  return move
    ? { move }
    : role === 'enter'
      ? { move: 'engine:fade-in' }
      : role === 'exit'
        ? { move: 'engine:fade-out' }
        : null;
}
function requiresSource(beat) {
  if (!SOURCED_TYPES.includes(beat.type)) return false;
  return beat.type !== 'compare' || beat.items?.some((item) => Object.hasOwn(item ?? {}, 'value'));
}

function validateSource(value, ids, path, errors) {
  const values = Array.isArray(value) ? value : [value];
  if (!values.length) {
    issue(errors, path, 'must not be an empty array');
    return;
  }
  const seen = new Set();
  for (const [index, id] of values.entries()) {
    const itemPath = Array.isArray(value) ? `${path}[${index}]` : path;
    if (typeof id !== 'string' || !id) issue(errors, itemPath, 'must be a source id');
    else if (seen.has(id)) issue(errors, itemPath, 'must not contain duplicate source ids');
    else if (!ids.has(id)) issue(errors, itemPath, 'source is not in deck.sources');
    seen.add(id);
  }
}

function validateChartAudit(beat, path, errors) {
  if (beat.type !== 'chart') return;
  const stepNames = new Set((beat.steps ?? []).map((step) => step?.name));
  for (const [index, state] of (beat.states ?? []).entries()) {
    const statePath = `${path}.states[${index}].name`;
    if (state?.name === BASE_STATE) issue(errors, statePath, 'must not be base');
    if (!stepNames.has(state?.name)) issue(errors, statePath, 'must match a step name');
  }
  const maxIndex = (beat.categories?.length ?? 0) - 1;
  for (const [key, entries] of [
    ['notes', beat.notes ?? []],
    ['highlight', beat.highlight ? [beat.highlight] : []],
  ])
    entries.forEach((entry, index) => {
      if (!Number.isInteger(entry?.index) || entry.index < 0 || entry.index > maxIndex)
        issue(
          errors,
          `${path}.${key}${key === 'notes' ? `[${index}]` : ''}.index`,
          'must be within categories',
        );
    });
}

/** @param {import('./types.js').DeckSpec} deck */
export function validateDeck(deck, env) {
  const errors = [];
  if (!deck || typeof deck !== 'object')
    return { ok: false, errors: [{ path: 'deck', message: 'must be an object' }] };
  walkStrings(deck, 'deck', errors);
  if (typeof deck.id !== 'string' || !DECK_ID_PATTERN.test(deck.id)) issue(errors, 'deck.id', 'invalid id');
  if (!['ko', 'en'].includes(deck.lang)) issue(errors, 'deck.lang', 'must be ko or en');
  if (deck.concept !== env.concept.id) issue(errors, 'deck.concept', 'does not match concept');
  if (!Array.isArray(deck.beats) || !deck.beats.length)
    issue(errors, 'deck.beats', 'must contain at least one beat');
  const sourceIds = new Set();
  for (const [index, source] of (deck.sources ?? []).entries()) {
    if (!source?.id || sourceIds.has(source.id)) issue(errors, `deck.sources[${index}].id`, 'must be unique');
    sourceIds.add(source?.id);
  }
  const ids = new Set();
  const usage = new Map();
  for (const [i, beat] of (deck.beats ?? []).entries()) {
    const path = `deck.beats[${i}]`;
    if (!beat || typeof beat !== 'object') {
      issue(errors, path, 'must be an object');
      continue;
    }
    if (typeof beat.id !== 'string' || !ID_PATTERN.test(beat.id) || ids.has(beat.id))
      issue(errors, `${path}.id`, 'must be a unique valid id');
    ids.add(beat.id);
    if (!BEAT_TYPES.includes(beat.type) || !env.concept.beats?.allow?.includes(beat.type))
      issue(errors, `${path}.type`, 'beat type is not allowed by concept');
    const type = beat.type === 'sequence' ? env.sequences?.[beat.use] : env.beatTypes?.[beat.type];
    if (!type) issue(errors, `${path}.type`, 'unknown beat type');
    else {
      const fields = Object.fromEntries(
        Object.keys(type.fields)
          .filter((key) => Object.hasOwn(beat, key))
          .map((key) => [key, beat[key]]),
      );
      errors.push(...validateSchema(type.fields, fields, path));
    }
    if (beat.link && i === deck.beats.length - 1) issue(errors, `${path}.link`, 'last beat cannot have link');
    if (beat.persist === true && !beat.place?.world)
      issue(errors, `${path}.persist`, 'is only allowed on place.world beats');
    if (
      beat.tone !== undefined &&
      (!Number.isInteger(beat.tone) || beat.tone < TONE_RANGE.min || beat.tone > TONE_RANGE.max)
    )
      issue(errors, `${path}.tone`, `must be an integer from ${TONE_RANGE.min} to ${TONE_RANGE.max}`);
    validateChartAudit(beat, path, errors);
    for (const [eventIndex, event] of (beat.type === 'chronology' ? (beat.events ?? []) : []).entries())
      if (event?.source !== undefined)
        validateSource(event.source, sourceIds, `${path}.events[${eventIndex}].source`, errors);
    if (!deck.sample && requiresSource(beat)) {
      if (!beat.source) issue(errors, `${path}.source`, 'source is required');
      else validateSource(beat.source, sourceIds, `${path}.source`, errors);
    }
    if (beat.source !== undefined && (deck.sample || !requiresSource(beat)))
      validateSource(beat.source, sourceIds, `${path}.source`, errors);
    if (beat.type === 'sequence' && beat.enter !== undefined)
      issue(errors, `${path}.enter`, 'sequence beat cannot specify enter');
    const refs = [];
    for (const role of ['enter', 'exit', 'link', 'camera']) {
      if (role === 'enter' && beat.type === 'sequence') continue;
      if (role === 'exit' && beat.link) continue; // C3: link가 있으면 exit 무시(plan과 같게)
      const ref = defaultMove(beat, role, env.concept, i === deck.beats.length - 1);
      if (ref) refs.push([role, ref]);
    }
    for (const step of beat.steps ?? []) refs.push(['step', step]);
    for (const ambient of beat.ambient ?? []) refs.push(['ambient', ambient]);
    for (const [role, ref] of refs) {
      if (!ref || typeof ref.move !== 'string') {
        issue(errors, `${path}.${role}`, 'move reference is invalid');
        continue;
      }
      if (!env.registry.has(ref.move)) {
        issue(errors, `${path}.${role}.move`, 'unknown move');
        continue;
      }
      const move = env.registry.get(ref.move);
      // C6 v2: engine:none은 role 검사·반복 검사 면제(「움직임 없음」 표기).
      if (ref.move === NO_MOVE) continue;
      if (move.role !== role) issue(errors, `${path}.${role}.move`, `must have ${role} role`);
      // C5: link accepts는 받는 beat(다음 beat) 기준.
      const target = role === 'link' ? deck.beats[i + 1] : beat;
      if (target && !move.accepts.includes('*') && !move.accepts.includes(target.type))
        issue(errors, `${path}.${role}.move`, 'does not accept beat type');
      if (!env.concept.moves?.allow?.includes(ref.move) && !ref.move.startsWith('engine:') && !ref.override)
        issue(errors, `${path}.${role}.override`, 'required for move outside concept allow list');
      const key = JSON.stringify([role, ref.move]);
      usage.set(key, (usage.get(key) ?? 0) + 1);
    }
  }
  for (const [key, count] of usage)
    if (count > 1) {
      const [role, move] = JSON.parse(key);
      const allowed = (deck.beats ?? []).some(
        (beat) =>
          beat.repeat === 'intended' &&
          [
            beat[role],
            ...(role === 'step' ? (beat.steps ?? []) : role === 'ambient' ? (beat.ambient ?? []) : []),
          ].some((ref) => ref?.move === move),
      );
      if (!allowed) issue(errors, `deck.beats`, `${move} repeats as ${role} without repeat: intended`);
    }
  return { ok: errors.length === 0, errors };
}
