import type { Step } from '../../../presentation-kit'
import { Box, SceneLayer } from '../../../presentation-kit'
import { ENTITIES } from '../entities'

/**
 * Single-step template — copy into steps/ and customize metadata + layout.
 * Register the step in Talk.tsx STEPS array.
 */
function StepScene() {
  return (
    <SceneLayer>
      <Box
        layoutId={ENTITIES.hero}
        label="{{STEP_TITLE}}"
        subtitle="{{STEP_SUBTITLE}}"
        accent="amber"
      />
    </SceneLayer>
  )
}

export const step: Step = {
  id: '{{STEP_ID}}',
  era: '{{ERA}}',
  title: '{{STEP_TITLE}}',
  caption: '{{STEP_CAPTION}}',
  Scene: StepScene,
}
