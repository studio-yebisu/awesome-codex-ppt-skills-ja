import { AnimatePresence, LayoutGroup } from 'motion/react'
import { DESIGN_H, STAGE_LAYOUT } from './constants'
import { useFitScale } from './useFitScale'
import type { Mode, Step } from './types'

/**
 * The fixed design canvas, scaled to fit the gap between header and footer.
 * transform-origin is the canvas center and the canvas is flex-centered, so the
 * diagram stays centered at any scale.
 *
 * Hosts the LayoutGroup + AnimatePresence: only the active step's Scene is
 * mounted (keyed by groupKey, falling back to id), so when the step changes the
 * outgoing and incoming scenes coexist briefly and their shared layoutId
 * elements morph between them. Steps that share a groupKey (and Scene) are NOT
 * remounted when navigating between them — the same instance persists and only
 * its `step` prop changes, so on-screen elements update in place instead of
 * re-animating. See StepMeta.groupKey.
 */
export function Stage<P extends Record<string, unknown> = Record<string, unknown>>({
  step,
  mode,
}: {
  step: Step<P>
  mode: Mode
}) {
  const layout = STAGE_LAYOUT[mode]
  const scale = useFitScale(layout)
  const Scene = step.Scene

  return (
    <div
      data-presentation-stage-shell
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: layout.top,
        bottom: layout.bottom,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        data-presentation-stage
        style={{
          position: 'relative',
          flexShrink: 0,
          width: layout.fitW,
          height: DESIGN_H,
          transform: `scale(${scale})`,
        }}
      >
        <LayoutGroup>
          <AnimatePresence>
            <Scene key={step.groupKey ?? step.id} step={step} />
          </AnimatePresence>
        </LayoutGroup>
      </div>
    </div>
  )
}
