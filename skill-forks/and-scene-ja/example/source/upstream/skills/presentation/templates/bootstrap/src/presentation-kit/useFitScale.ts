import { useLayoutEffect, useState } from 'react'
import { DESIGN_H, MIN_SCALE, type StageLayout } from './constants'

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v))

/**
 * Uniform scale that fits the diagram into the space between header and footer
 * for the active mode's stage geometry. Recomputed on resize and whenever the
 * mode (layout) changes; constant during a step morph, so layoutId transitions
 * stay clean at every viewport size.
 */
export function useFitScale(layout: StageLayout) {
  const [scale, setScale] = useState(1)
  useLayoutEffect(() => {
    const compute = () => {
      const availW = window.innerWidth - layout.padX * 2
      const availH = window.innerHeight - layout.top - layout.bottom
      setScale(clamp(Math.min(availW / layout.fitW, availH / DESIGN_H), MIN_SCALE, layout.maxScale))
    }
    compute()
    window.addEventListener('resize', compute)
    return () => window.removeEventListener('resize', compute)
  }, [layout])
  return scale
}
