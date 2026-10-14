import { Presentation } from '../../presentation-kit'
import { introStep } from './steps/intro'

/** Replace with all steps for the talk; keep order stable for navigation. */
const STEPS = [introStep]

export default function Talk() {
  return (
    <Presentation
      steps={STEPS}
      title="{{PRESENTATION_TITLE}}"
      initialMode="browse"
    />
  )
}
