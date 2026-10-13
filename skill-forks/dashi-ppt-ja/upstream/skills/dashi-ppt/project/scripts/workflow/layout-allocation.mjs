import { hashSeed, layoutFamily } from './layout-query.mjs';

const CANDIDATE_LIMIT = 18;
const CHOICE_LIMIT = 96;
const FIT_BAND = 16;
const FIT_WEIGHT = 150;

export function allocateDeckLayouts(candidateMatrix, seed = 'layout-allocation') {
  const choices = candidateMatrix.map((candidates, pageIndex) => {
    const unique = dedupeCandidates(candidates);
    if (unique.length < 3) {
      throw new Error(`Layout allocation page ${pageIndex + 1} has only ${unique.length} compatible layouts; required 3`);
    }
    const pageChoices = boundedChoices(unique, `${seed}:page-${pageIndex + 1}`);
    if (!pageChoices.length) {
      throw new Error(`Layout allocation page ${pageIndex + 1} cannot form 3 structurally distinct template variants`);
    }
    return pageChoices;
  });
  const selected = choices.map(items => items[0]);

  for (let pass = 0; pass < 3; pass += 1) {
    let changed = false;
    for (let pageIndex = 0; pageIndex < selected.length; pageIndex += 1) {
      let best = selected[pageIndex];
      let bestScore = allocationScore(selected);
      let bestTie = assignmentTie(selected, seed);
      for (const choice of choices[pageIndex]) {
        const trial = selected.map((item, index) => (index === pageIndex ? choice : item));
        const score = allocationScore(trial);
        const tie = assignmentTie(trial, seed);
        if (score < bestScore || (score === bestScore && tie < bestTie)) {
          best = choice;
          bestScore = score;
          bestTie = tie;
        }
      }
      if (layoutCombinationKey(best.items) !== layoutCombinationKey(selected[pageIndex].items)) {
        selected[pageIndex] = best;
        changed = true;
      }
    }
    if (!changed) break;
  }

  const assignments = selected.map(item => item.items);
  const orderState = { positionFamilyUsage: [new Map(), new Map(), new Map()], previousFamilies: [] };
  assignments.forEach((items, pageIndex) => {
    assignments[pageIndex] = orderVariants(items, orderState, `${seed}:page-${pageIndex + 1}`);
    recordVariantOrder(assignments[pageIndex], orderState);
  });
  return { assignments, diagnostics: allocationDiagnostics(assignments, selected) };
}

export function layoutCombinationKey(candidates) {
  return candidates.map(item => item.layout).sort().join('|');
}

function boundedChoices(candidates, seed) {
  const pool = structurallyDiversePool(candidates, CANDIDATE_LIMIT);
  const combinations = [];
  let maxFit = -Infinity;
  for (let left = 0; left < pool.length - 2; left += 1) {
    for (let middle = left + 1; middle < pool.length - 1; middle += 1) {
      for (let right = middle + 1; right < pool.length; right += 1) {
        const items = [pool[left], pool[middle], pool[right]];
        if (new Set(items.map(structureComposition)).size !== 3) continue;
        const fit = pageFit(items);
        maxFit = Math.max(maxFit, fit);
        combinations.push({ items, fit });
      }
    }
  }
  return combinations
    .filter(item => item.fit >= maxFit - FIT_BAND)
    .map(item => ({ ...item, maxFit }))
    .sort((left, right) => (
      right.fit - left.fit
      || intraPagePenalty(left.items) - intraPagePenalty(right.items)
      || combinationTie(left.items, seed) - combinationTie(right.items, seed)
    ))
    .slice(0, CHOICE_LIMIT);
}

function structurallyDiversePool(candidates, limit) {
  const representatives = new Map();
  for (const candidate of candidates) {
    const composition = structureComposition(candidate);
    if (!representatives.has(composition)) representatives.set(composition, candidate);
  }
  const selected = [...representatives.values()].slice(0, limit);
  for (const candidate of candidates) {
    if (selected.length >= limit) break;
    if (!selected.includes(candidate)) selected.push(candidate);
  }
  return selected;
}

function allocationScore(selected) {
  const assignments = selected.map(item => item.items);
  const fitLoss = selected.reduce((sum, item) => sum + item.maxFit - item.fit, 0);
  return fitLoss * FIT_WEIGHT + diversityPenalty(assignments);
}

function intraPagePenalty(items) {
  const families = items.map(layoutFamily);
  const compositions = items.map(item => item?.structureFingerprint?.composition || layoutFamily(item));
  return (items.length - new Set(families).size) * 300
    + (items.length - new Set(compositions).size) * 450;
}

function diversityPenalty(assignments) {
  let penalty = assignments.reduce((sum, items) => sum + intraPagePenalty(items), 0);
  for (let pageIndex = 1; pageIndex < assignments.length; pageIndex += 1) {
    const previousFamilies = new Set(assignments[pageIndex - 1].map(layoutFamily));
    penalty += assignments[pageIndex].filter(item => previousFamilies.has(layoutFamily(item))).length * 90;
  }
  penalty += repeatPenalty(assignments.flat().map(item => item.layout), 600);
  penalty += repeatPenalty(assignments.map(layoutCombinationKey), 1400);
  penalty += repeatPenalty(assignments.flat().map(layoutFamily), 14);
  return penalty;
}

function repeatPenalty(values, weight) {
  const counts = new Map();
  values.forEach(value => increment(counts, value));
  return [...counts.values()].reduce((sum, count) => sum + (count * (count - 1) / 2) * weight, 0);
}

function combinationTie(items, seed) {
  return hashSeed(`${seed}:${layoutCombinationKey(items)}`);
}

function assignmentTie(selected, seed) {
  return hashSeed(`${seed}:${selected.map(item => layoutCombinationKey(item.items)).join('::')}`);
}

function orderVariants(items, state, seed) {
  const permutations = [
    [items[0], items[1], items[2]], [items[0], items[2], items[1]],
    [items[1], items[0], items[2]], [items[1], items[2], items[0]],
    [items[2], items[0], items[1]], [items[2], items[1], items[0]],
  ];
  return permutations.sort((left, right) => (
    variantOrderPenalty(left, state) - variantOrderPenalty(right, state)
    || combinationTie(left, seed) - combinationTie(right, seed)
  ))[0];
}

function variantOrderPenalty(items, state) {
  return items.reduce((sum, item, index) => (
    sum + (state.positionFamilyUsage[index].get(layoutFamily(item)) || 0) * 20
    + Number(state.previousFamilies[index] === layoutFamily(item)) * 30
  ), 0);
}

function recordVariantOrder(items, state) {
  state.previousFamilies = items.map(layoutFamily);
  items.forEach((item, index) => increment(state.positionFamilyUsage[index], layoutFamily(item)));
}

function allocationDiagnostics(assignments, selected) {
  const layouts = assignments.flat().map(item => item.layout);
  const families = assignments.flat().map(layoutFamily);
  const combinations = assignments.map(layoutCombinationKey);
  const pageFits = assignments.map(pageFit);
  const maxFits = selected.map(item => item.maxFit);
  return {
    pages: assignments.map((items, index) => ({
      page: index + 1,
      layouts: items.map(item => item.layout),
      families: items.map(layoutFamily),
      compositions: items.map(structureComposition),
      queryScores: items.map(candidateFit),
      fitTotal: pageFit(items),
      fitMax: maxFits[index],
      fitLoss: maxFits[index] - pageFit(items),
      combination: layoutCombinationKey(items),
    })),
    fit: {
      total: pageFits.reduce((sum, value) => sum + value, 0),
      maxTotal: maxFits.reduce((sum, value) => sum + value, 0),
      loss: maxFits.reduce((sum, value) => sum + value, 0) - pageFits.reduce((sum, value) => sum + value, 0),
      min: Math.min(...pageFits),
      max: Math.max(...pageFits),
    },
    layout: repeatStats(layouts),
    family: repeatStats(families),
    combination: repeatStats(combinations),
  };
}

function dedupeCandidates(candidates) {
  const seen = new Set();
  return (candidates || []).filter(candidate => {
    if (!candidate?.layout || seen.has(candidate.layout)) return false;
    seen.add(candidate.layout);
    return true;
  });
}

function structureComposition(candidate) {
  return candidate?.structureFingerprint?.composition
    || candidate?.projectionPlan?.structureFingerprint?.composition
    || layoutFamily(candidate);
}

function candidateFit(candidate) {
  return Math.round(Number(candidate?.queryScore || 0));
}

function pageFit(items) {
  return items.reduce((sum, item) => sum + candidateFit(item), 0);
}

function repeatStats(values) {
  const counts = new Map();
  values.forEach(value => increment(counts, value));
  return {
    total: values.length,
    unique: counts.size,
    repeated: [...counts.entries()].filter(([, count]) => count > 1).map(([value, count]) => ({ value, count })),
    maxUse: counts.size ? Math.max(...counts.values()) : 0,
  };
}

function increment(map, key) {
  map.set(key, (map.get(key) || 0) + 1);
}
