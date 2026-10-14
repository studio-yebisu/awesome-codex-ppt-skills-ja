'use strict';

const {
  CONTRACT_VERSION,
  roleLayoutContract,
} = require('./role_layout_contracts.js');
const RENDERER_CAPABILITIES_V2 = require('../../schemas/renderer_capabilities_v2.json');

const V1_CONTRACT_VERSION = 'renderer_role_systems_v1';

const CANONICAL_ROLES = Object.freeze([
  'title',
  'section',
  'evidence',
  'comparison',
  'chart',
  'table',
  'decision',
  'references',
]);

const CONTENT_VARIANTS = Object.freeze([
  'standard',
  'cards-2',
  'cards-3',
  'split',
  'timeline',
  'stats',
  'kpi-hero',
  'table',
  'lab-run-results',
  'comparison-2col',
  'matrix',
  'flow',
  'chart',
  'image-sidebar',
  'scientific-figure',
  'generated-image',
]);

// Input-only aliases and known unsupported variants are included so the route
// smoke can cover every value accepted by the current dispatcher boundary.
const ROUTED_VARIANTS = Object.freeze([
  ...CONTENT_VARIANTS,
  'content',
  'hero',
  'comparison',
]);

const CONTENT_VARIANT_SET = new Set(CONTENT_VARIANTS);

const RENDERER_ADAPTERS = Object.freeze({
  title: 'renderTitle',
  section: 'renderSection',
  standard: 'renderStandard',
  'cards-2': 'renderCards2',
  'cards-3': 'renderCards3',
  split: 'renderSplit',
  timeline: 'renderTimeline',
  stats: 'renderStats',
  'kpi-hero': 'renderKpiHero',
  table: 'renderTable',
  'lab-run-results': 'renderLabRunResults',
  'comparison-2col': 'renderComparison2col',
  matrix: 'renderMatrix',
  flow: 'renderFlow',
  chart: 'renderChart',
  'image-sidebar': 'renderImageSidebar',
  'scientific-figure': 'renderScientificFigure',
  'generated-image': 'renderGeneratedImage',
});

// These are the only combinations whose current renderer actually consumes
// the selected v2 role contract. A visual variant does not imply one of these
// roles; the pair is considered only after semantic role resolution.
const SUPPORTED_VARIANT_ROLE_ADAPTERS = Object.freeze(Object.fromEntries(
  Object.entries(RENDERER_CAPABILITIES_V2.role_variants || {}).flatMap(([role, variants]) => (
    variants.map((variant) => [
      `${variant}:${role}`,
      `${RENDERER_ADAPTERS[variant]}:${role}`,
    ])
  )),
));

const ROLE_ALIASES = Object.freeze({
  cover: 'title',
  opener: 'title',
  chapter: 'section',
  divider: 'section',
  message: 'evidence',
  content: 'evidence',
  figure: 'evidence',
  image: 'evidence',
  stats: 'evidence',
  metric: 'evidence',
  metrics: 'evidence',
  process: 'evidence',
  flow: 'evidence',
  dashboard: 'evidence',
  compare: 'comparison',
  options: 'comparison',
  graph: 'chart',
  plot: 'chart',
  ledger: 'table',
  register: 'table',
  recommendation: 'decision',
  recommend: 'decision',
  action: 'decision',
  actions: 'decision',
  conclusion: 'decision',
  reference: 'references',
  source: 'references',
  sources: 'references',
  citation: 'references',
  citations: 'references',
});

const TREATMENT_ROLE_MAP = Object.freeze({
  title: 'title',
  section: 'section',
  evidence: 'evidence',
  message: 'evidence',
  process: 'evidence',
  figure: 'evidence',
  dashboard: 'evidence',
  stats: 'evidence',
  comparison: 'comparison',
  chart: 'chart',
  graph: 'chart',
  plot: 'chart',
  table: 'table',
  ledger: 'table',
  decision: 'decision',
  recommendation: 'decision',
  action: 'decision',
  references: 'references',
  reference: 'references',
  source: 'references',
  sources: 'references',
  citation: 'references',
  citations: 'references',
});

const VARIANT_DEFAULT_ROLES = Object.freeze({
  standard: 'evidence',
  content: 'evidence',
  hero: 'evidence',
  'cards-2': 'evidence',
  'cards-3': 'evidence',
  split: 'evidence',
  timeline: 'evidence',
  stats: 'evidence',
  'kpi-hero': 'decision',
  table: 'table',
  'lab-run-results': 'table',
  comparison: 'comparison',
  'comparison-2col': 'comparison',
  matrix: 'decision',
  flow: 'evidence',
  chart: 'chart',
  'image-sidebar': 'evidence',
  'scientific-figure': 'evidence',
  'generated-image': 'evidence',
});

function clone(value) {
  return value === null || value === undefined
    ? value
    : JSON.parse(JSON.stringify(value));
}

function normalizedText(value) {
  return String(value || '').trim().toLowerCase();
}

function normalizedType(value) {
  const type = normalizedText(value || 'content');
  return type === 'text' ? 'content' : type;
}

function roleForDataAlias(variant) {
  if (variant === 'table' || variant === 'lab-run-results') return 'table';
  if (variant === 'chart') return 'chart';
  return 'evidence';
}

function canonicalRoleValue(value, variant) {
  const role = normalizedText(value);
  if (!role) return '';
  if (CANONICAL_ROLES.includes(role)) return role;
  if (role === 'data') return roleForDataAlias(variant);
  return ROLE_ALIASES[role] || '';
}

function resolveVariant(slide) {
  const type = normalizedType(slide && slide.type);
  const requestedVariant = normalizedText(slide && slide.variant) || 'standard';
  if (type === 'title') {
    return { type, requestedVariant, effectiveVariant: 'title', fallbackReason: null };
  }
  if (type === 'section') {
    return { type, requestedVariant, effectiveVariant: 'section', fallbackReason: null };
  }
  if (requestedVariant === 'content') {
    return { type, requestedVariant, effectiveVariant: 'standard', fallbackReason: null };
  }
  if (requestedVariant === 'comparison') {
    return { type, requestedVariant, effectiveVariant: 'comparison-2col', fallbackReason: null };
  }
  if (CONTENT_VARIANT_SET.has(requestedVariant)) {
    return { type, requestedVariant, effectiveVariant: requestedVariant, fallbackReason: null };
  }
  return {
    type,
    requestedVariant,
    effectiveVariant: 'standard',
    fallbackReason: `unsupported_variant:${requestedVariant}->standard`,
  };
}

function resolveCanonicalRole(slide, variantInfo) {
  if (variantInfo.type === 'title') return { canonicalRole: 'title', roleSource: 'type' };
  if (variantInfo.type === 'section') return { canonicalRole: 'section', roleSource: 'type' };

  const explicitRole = canonicalRoleValue(slide && slide.role, variantInfo.requestedVariant);
  if (explicitRole) return { canonicalRole: explicitRole, roleSource: 'role' };

  const slideIntent = canonicalRoleValue(slide && slide.slide_intent, variantInfo.requestedVariant);
  const treatmentKey = normalizedText(slide && slide.treatment_key);
  const treatmentRole = treatmentKey === 'data'
    ? roleForDataAlias(variantInfo.requestedVariant)
    : (TREATMENT_ROLE_MAP[treatmentKey] || '');

  // `slide_intent` describes the story job, not necessarily the renderer
  // object. A chart can be evidence and a table can carry a decision. Prefer
  // a compatible intent/treatment pair, then let the concrete variant select
  // its v2 renderer role instead of falling back to v1 on pairs such as
  // chart:evidence or table:decision.
  const pairSupported = (role) => Boolean(
    role && SUPPORTED_VARIANT_ROLE_ADAPTERS[`${variantInfo.effectiveVariant}:${role}`],
  );
  if (pairSupported(slideIntent)) {
    return { canonicalRole: slideIntent, roleSource: 'slide_intent' };
  }
  if (pairSupported(treatmentRole)) {
    return { canonicalRole: treatmentRole, roleSource: 'treatment_key' };
  }

  const variantRole = VARIANT_DEFAULT_ROLES[variantInfo.requestedVariant] || 'evidence';
  if (pairSupported(variantRole)) {
    return { canonicalRole: variantRole, roleSource: 'variant_default' };
  }

  if (slideIntent) return { canonicalRole: slideIntent, roleSource: 'slide_intent' };
  if (treatmentRole) return { canonicalRole: treatmentRole, roleSource: 'treatment_key' };

  return {
    canonicalRole: variantRole,
    roleSource: 'variant_default',
  };
}

function rendererContractMode(preset) {
  const version = normalizedText(preset && preset.renderer_role_contract_version);
  if (version === V1_CONTRACT_VERSION) return 'v1';
  if (version === CONTRACT_VERSION) return 'v2';
  const v2 = preset && preset.renderer_role_contracts_v2;
  if (v2 && v2.schema_version === CONTRACT_VERSION) return 'v2';
  const v1 = preset && preset.renderer_role_systems_v1;
  if (v1 && (!v1.schema_version || v1.schema_version === V1_CONTRACT_VERSION)) return 'v1';
  return 'legacy';
}

function v1SystemId(slide, preset, role, v2Contract) {
  const fallback = v2Contract && v2Contract.fallback;
  if (fallback && normalizedText(fallback.version) === V1_CONTRACT_VERSION) {
    const fallbackId = normalizedText(fallback.system_id);
    if (fallbackId) return fallbackId;
  }
  const systemRole = role === 'chart' || role === 'table' ? 'data' : role;
  const slideSystems = slide && slide.role_systems && typeof slide.role_systems === 'object'
    ? slide.role_systems
    : {};
  const presetSystems = preset && preset.role_systems && typeof preset.role_systems === 'object'
    ? preset.role_systems
    : {};
  const persisted = preset && preset.renderer_role_systems_v1 && typeof preset.renderer_role_systems_v1 === 'object'
    ? preset.renderer_role_systems_v1
    : {};
  return normalizedText(
    slideSystems[systemRole]
      || presetSystems[systemRole]
      || persisted[`${systemRole}_system_id`]
      || (slide && slide.render_system_id),
  );
}

function v1ContractDescriptor(slide, preset, role, v2Contract) {
  return {
    schema_version: V1_CONTRACT_VERSION,
    role,
    system_id: v1SystemId(slide, preset, role, v2Contract) || null,
  };
}

function fallbackAdapter(source, effectiveVariant) {
  return `${source}:${RENDERER_ADAPTERS[effectiveVariant] || RENDERER_ADAPTERS.standard}`;
}

function joinReasons(reasons) {
  const unique = Array.from(new Set(reasons.filter(Boolean)));
  return unique.length ? unique.join('; ') : null;
}

/**
 * Resolve the renderer capability and semantic contract without mutating the
 * slide or preset. Callers may safely persist or compare the returned plan.
 */
function resolveRenderPlan(slide = {}, preset = {}) {
  const variantInfo = resolveVariant(slide);
  const roleInfo = resolveCanonicalRole(slide, variantInfo);
  const reasons = [variantInfo.fallbackReason];
  const mode = rendererContractMode(preset);
  const pairKey = `${variantInfo.effectiveVariant}:${roleInfo.canonicalRole}`;
  const v2Adapter = SUPPORTED_VARIANT_ROLE_ADAPTERS[pairKey] || '';

  if (mode === 'v2') {
    const resolvedV2Contract = roleLayoutContract(preset, slide, roleInfo.canonicalRole);
    if (v2Adapter && resolvedV2Contract) {
      return {
        effectiveVariant: variantInfo.effectiveVariant,
        canonicalRole: roleInfo.canonicalRole,
        roleSource: roleInfo.roleSource,
        contractSource: 'v2',
        adapter: `v2:${v2Adapter}`,
        contract: clone(resolvedV2Contract),
        fallbackReason: joinReasons(reasons),
      };
    }

    if (!v2Adapter) {
      reasons.push(`unsupported_v2_variant_role_pair:${pairKey}`);
    } else {
      reasons.push(`v2_contract_unavailable:${roleInfo.canonicalRole}`);
    }

    const v1Contract = v1ContractDescriptor(slide, preset, roleInfo.canonicalRole, resolvedV2Contract);
    if (v1Contract.system_id || resolvedV2Contract) {
      return {
        effectiveVariant: variantInfo.effectiveVariant,
        canonicalRole: roleInfo.canonicalRole,
        roleSource: roleInfo.roleSource,
        contractSource: 'v1',
        adapter: fallbackAdapter('v1', variantInfo.effectiveVariant),
        contract: v1Contract,
        fallbackReason: joinReasons(reasons),
      };
    }
    reasons.push('v1_fallback_unavailable');
  }

  if (mode === 'v1') {
    reasons.push('explicit_v1_contract_pin');
    return {
      effectiveVariant: variantInfo.effectiveVariant,
      canonicalRole: roleInfo.canonicalRole,
      roleSource: roleInfo.roleSource,
      contractSource: 'v1',
      adapter: fallbackAdapter('v1', variantInfo.effectiveVariant),
      contract: v1ContractDescriptor(slide, preset, roleInfo.canonicalRole, null),
      fallbackReason: joinReasons(reasons),
    };
  }

  reasons.push('renderer_role_contract_unavailable');
  return {
    effectiveVariant: variantInfo.effectiveVariant,
    canonicalRole: roleInfo.canonicalRole,
    roleSource: roleInfo.roleSource,
    contractSource: 'legacy',
    adapter: fallbackAdapter('legacy', variantInfo.effectiveVariant),
    contract: null,
    fallbackReason: joinReasons(reasons),
  };
}

function contractForResolvedPlan(slide = {}, preset = {}, requestedRole = '') {
  const existing = slide && slide.__renderPlan;
  const plan = existing && typeof existing === 'object'
    ? existing
    : resolveRenderPlan(slide, preset);
  const role = canonicalRoleValue(requestedRole, plan.effectiveVariant);
  if (plan.contractSource !== 'v2' || plan.canonicalRole !== role) return null;
  return clone(plan.contract);
}

module.exports = {
  CANONICAL_ROLES,
  CONTENT_VARIANTS,
  ROUTED_VARIANTS,
  SUPPORTED_VARIANT_ROLE_ADAPTERS,
  contractForResolvedPlan,
  resolveRenderPlan,
};
