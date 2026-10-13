/** Move registry and its eager C16 contract validation. */
import { FAMILIES, ID_PATTERN, ROLES } from './constants.js';
import { ENGINE_MOVE_DEFS } from './timeline.js';

function fail(message) {
  throw new Error(`Invalid move definition: ${message}`);
}
function validate(def) {
  if (!def || typeof def !== 'object') fail('definition must be an object');
  if (
    typeof def.id !== 'string' ||
    (!ID_PATTERN.test(def.id) && !(def.family === 'engine' && def.id.startsWith('engine:')))
  )
    fail('id');
  if (def.id.startsWith('seq:')) fail(`${def.id}.id is reserved`);
  if (!FAMILIES.includes(def.family)) fail(`${def.id}.family`);
  if (!ROLES.includes(def.role)) fail(`${def.id}.role`);
  if (!Array.isArray(def.accepts) || !def.accepts.length) fail(`${def.id}.accepts`);
  if (!Array.isArray(def.sources) || !def.sources.length) fail(`${def.id}.sources`);
  if (def.reduce !== 'self' && def.reduce !== 'fade') fail(`${def.id}.reduce`);
  if (!def.params || typeof def.params !== 'object' || Array.isArray(def.params)) fail(`${def.id}.params`);
  for (const [name, field] of Object.entries(def.params)) {
    if (!field || !Object.hasOwn(field, 'default')) fail(`${def.id}.params.${name}.default`);
    if (typeof field.doc !== 'string' || !field.doc.trim()) fail(`${def.id}.params.${name}.doc`);
  }
  if (typeof def.timing !== 'function') fail(`${def.id}.timing`);
  if (typeof def.build !== 'function') fail(`${def.id}.build`);
  if (def.handoff !== undefined && typeof def.handoff !== 'function') fail(`${def.id}.handoff`);
  if (def.handoff !== undefined && def.role !== 'link') fail(`${def.id}.handoff requires link role`);
}

/** @param {import('./types.js').MoveDef[]} defs */
export function createRegistry(defs = []) {
  const byId = new Map();
  for (const def of [...ENGINE_MOVE_DEFS, ...defs]) {
    validate(def);
    if (byId.has(def.id)) fail(`duplicate id ${def.id}`);
    byId.set(def.id, def);
  }
  return Object.freeze({
    get(id) {
      const result = byId.get(id);
      if (!result) throw new Error(`Unknown move: ${id}`);
      return result;
    },
    has: (id) => byId.has(id),
    ids: () => [...byId.keys()],
    byFamily: (family) => [...byId.values()].filter((move) => move.family === family),
    byRole: (role) => [...byId.values()].filter((move) => move.role === role),
  });
}
