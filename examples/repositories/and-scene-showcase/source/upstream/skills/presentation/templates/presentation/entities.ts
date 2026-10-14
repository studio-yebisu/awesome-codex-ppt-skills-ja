/**
 * Stable layoutId namespace for this presentation.
 * Every entity that persists or morphs across steps gets a constant here.
 */
export const ENTITIES = {
  /** Primary focal node — rename to match your topic. */
  hero: 'hero',
  /** Supporting label or annotation. */
  caption: 'caption',
  /** Connector between entities. */
  flow: 'flow',
} as const

export type EntityId = (typeof ENTITIES)[keyof typeof ENTITIES]
