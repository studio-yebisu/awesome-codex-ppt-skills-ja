import { Sparkles } from 'lucide-react'
import { Box, SceneLayer } from '../../../presentation-kit'
import type { Step } from '../../../presentation-kit'
import { ENTITIES } from '../entities'

function IntroScene() {
  return (
    <SceneLayer>
      <Box
        layoutId={ENTITIES.hero}
        Icon={Sparkles}
        label="{{TITLE}}"
        subtitle="{{SUBTITLE}}"
        accent="cyan"
      />
    </SceneLayer>
  )
}

export const introStep: Step = {
  id: 'intro',
  era: '{{ERA}}',
  title: '{{STEP_TITLE}}',
  caption: '{{STEP_CAPTION}}',
  Scene: IntroScene,
}
