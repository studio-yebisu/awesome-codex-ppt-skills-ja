import type { StepMeta } from '../types'

export interface Section {
  era: string
  /** First step in this era — where clicking the entry jumps. */
  start: number
  /** Last step in this era — the active range is [start, end]. */
  end: number
}

/** Collapse consecutive steps that share an era into one contents section. */
export function toSections(steps: StepMeta[]): Section[] {
  const out: Section[] = []
  steps.forEach((s, i) => {
    const last = out[out.length - 1]
    if (last && last.era === s.era) last.end = i
    else out.push({ era: s.era, start: i, end: i })
  })
  return out
}
