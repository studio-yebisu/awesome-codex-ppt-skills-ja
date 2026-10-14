import type { ComponentType } from 'react'

export type Mode = 'browse' | 'present'

/** Narration + identity for one beat of the evolving diagram. */
export interface StepMeta<P extends Record<string, unknown> = Record<string, unknown>> {
  /** Stable key for AnimatePresence + React reconciliation. */
  id: string
  /** Header label, e.g. "the model". */
  era: string
  /** Presenter-mode one-liner. */
  title: string
  /** Browsing-mode paragraph. */
  caption: string
  /**
   * AnimatePresence key override. Consecutive steps that share a groupKey are
   * NOT remounted when you navigate between them — the Scene instance persists
   * and only its `step` prop changes, so elements already on screen never fade
   * out and back in; they update in place (and a newly added element animates
   * in on its own). Steps sharing a groupKey must also share the same `Scene`
   * component. Defaults to `id`.
   */
  groupKey?: string
  /** Per-step data handed to the Scene (e.g. how many chips to show). */
  payload?: P
}

/**
 * Props every Scene receives. Most scenes ignore them; a grouped scene reads
 * `step.payload` to decide which sub-state of its diagram to render.
 */
export interface SceneProps<P extends Record<string, unknown> = Record<string, unknown>> {
  step: Step<P>
}

/**
 * A step = its narration + the diagram layer rendered while it is active.
 *
 * `Scene` composes the shared nodes (see ./nodes). Elements that should morph
 * between steps share a layoutId — that's the only contract between one step
 * and the next.
 */
export interface Step<P extends Record<string, unknown> = Record<string, unknown>> extends StepMeta<P> {
  Scene: ComponentType<SceneProps<P>>
}
