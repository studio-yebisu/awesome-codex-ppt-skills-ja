'use strict';

const path = require('path');

const CATALOG = require(path.resolve(__dirname, '..', '..', 'references', 'renderer_role_contracts_v2.json'));
const CONTRACT_VERSION = 'renderer_role_contracts_v2';
const SUPPORTED_VARIANTS = new Set(CATALOG.supported_layout_variants || []);

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function normalizedVariant(value) {
  const variant = String(value || 'primary').trim().toLowerCase();
  return SUPPORTED_VARIANTS.has(variant) ? variant : 'primary';
}

function canonicalRoles(grammarId) {
  const raw = CATALOG.grammars && CATALOG.grammars[grammarId];
  if (!raw) return null;
  const roles = clone(raw);
  for (const [role, contract] of Object.entries(roles)) {
    contract.grammar_id = grammarId;
    contract.role = role;
  }
  return roles;
}

function validateResolvedRoleContracts(payload) {
  const failures = [];
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    return ['renderer_role_contracts_v2 must be an object'];
  }
  if (payload.schema_version !== CONTRACT_VERSION) {
    failures.push(`schema_version must be '${CONTRACT_VERSION}'`);
  }
  if (payload.catalog_version !== CATALOG.schema_version) {
    failures.push(`catalog_version must be '${CATALOG.schema_version}'`);
  }
  const grammarId = String(payload.composition_grammar_id || '').trim();
  const canonical = canonicalRoles(grammarId);
  if (!canonical) {
    failures.push(`unknown composition_grammar_id '${grammarId}'`);
    return failures;
  }
  if (JSON.stringify(payload.roles || {}) !== JSON.stringify(canonical)) {
    failures.push('roles must match the canonical contracts for the composition grammar');
  }
  return failures;
}

function contractsForGrammar(grammarId, stylePreset = '') {
  const key = String(grammarId || '').trim().toLowerCase();
  const roles = canonicalRoles(key);
  if (!roles) return null;
  return {
    schema_version: CONTRACT_VERSION,
    catalog_version: CATALOG.schema_version,
    composition_grammar_id: key,
    style_preset: String(stylePreset || '').trim(),
    supported_layout_variants: Array.from(SUPPORTED_VARIANTS),
    roles: clone(roles),
  };
}

function transformSlots(slots, variant) {
  const out = {};
  for (const [name, raw] of Object.entries(slots || {})) {
    if (!Array.isArray(raw) || raw.length !== 4) continue;
    const [x, y, w, h] = raw.map(Number);
    if (variant === 'alternate') {
      out[name] = [Number((1 - x - w).toFixed(6)), y, w, h];
      continue;
    }
    if (variant === 'dense') {
      const left = Math.max(0, x - 0.012);
      const top = Math.max(0, y - 0.018);
      const right = Math.min(1, x + w + 0.012);
      const bottom = Math.min(1, y + h + 0.018);
      out[name] = [left, top, right - left, bottom - top]
        .map((value) => Number(value.toFixed(6)));
      continue;
    }
    out[name] = [x, y, w, h];
  }
  return out;
}

function roleLayoutContract(preset, slideData, role) {
  const version = String((preset && preset.renderer_role_contract_version) || '').trim();
  if (version === 'renderer_role_systems_v1') return null;
  const requestedRole = String(role || '').trim().toLowerCase();
  const persisted = preset && preset.renderer_role_contracts_v2;
  const grammarId = String(
    (persisted && persisted.composition_grammar_id)
      || (slideData && slideData.composition_grammar)
      || (preset && preset.composition_grammar)
      || '',
  ).trim().toLowerCase();
  const resolved = persisted && persisted.schema_version === CONTRACT_VERSION
    ? persisted
    : contractsForGrammar(grammarId, preset && preset.style_preset);
  if (!resolved || !resolved.roles || !resolved.roles[requestedRole]) return null;
  const contract = clone(resolved.roles[requestedRole]);
  const variant = normalizedVariant(slideData && slideData.role_layout_variant);
  if (!Array.isArray(contract.supported_variants) || !contract.supported_variants.includes(variant)) {
    contract.variant = 'primary';
  } else {
    contract.variant = variant;
  }
  contract.slots = transformSlots(contract.slots, contract.variant);
  contract.schema_version = CONTRACT_VERSION;
  contract.composition_grammar_id = grammarId;
  return contract;
}

function absoluteSlot(contract, slotName, bodyBox) {
  if (!contract || !contract.slots || !Array.isArray(contract.slots[slotName])) return null;
  const [x, y, w, h] = contract.slots[slotName].map(Number);
  const box = bodyBox || { x: 0, y: 0, w: 1, h: 1 };
  return {
    x: box.x + x * box.w,
    y: box.y + y * box.h,
    w: w * box.w,
    h: h * box.h,
  };
}

module.exports = {
  CATALOG,
  CONTRACT_VERSION,
  SUPPORTED_VARIANTS,
  absoluteSlot,
  contractsForGrammar,
  normalizedVariant,
  roleLayoutContract,
  validateResolvedRoleContracts,
};
