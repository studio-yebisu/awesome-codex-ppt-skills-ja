import { useEffect, useState } from 'react'
import { toSections } from './tocSections'
import type { StepMeta } from '../types'

interface TocProps {
  steps: StepMeta[]
  step: number
  onSelect: (i: number) => void
}

function isWideViewport() {
  if (typeof window === 'undefined') return true
  if (window.matchMedia) return window.matchMedia('(min-width: 1280px)').matches
  return window.innerWidth >= 1280
}

/**
 * Table of contents down the left margin, built from each step's era label.
 * The section containing the current step is highlighted; clicking an entry
 * jumps to that section's first step. Shown only when the viewport is wide
 * enough to hold it beside the centered stage (xl+); below that it's hidden and
 * the era simply isn't displayed (its only other home was the header).
 */
export function Toc({ steps, step, onSelect }: TocProps) {
  const sections = toSections(steps)
  const [visible, setVisible] = useState(isWideViewport)

  useEffect(() => {
    if (!window.matchMedia) return
    const query = window.matchMedia('(min-width: 1280px)')
    const update = () => setVisible(query.matches)
    query.addEventListener('change', update)
    return () => query.removeEventListener('change', update)
  }, [])

  return (
    <nav
      aria-label="Contents"
      data-presentation-toc
      style={{
        display: visible ? undefined : 'none',
        position: 'absolute',
        left: 32,
        top: '50%',
        zIndex: 20,
        transform: 'translateY(-50%)',
      }}
    >
      <ol data-presentation-toc-list style={{ display: 'grid', gap: 14, margin: 0, padding: 0 }}>
        {sections.map((sec) => {
          const active = step >= sec.start && step <= sec.end
          return (
            <li key={sec.era}>
              <button
                onClick={() => onSelect(sec.start)}
                aria-current={active ? 'step' : undefined}
                data-presentation-toc-item
                data-active={active ? 'true' : undefined}
              >
                {sec.era}
              </button>
            </li>
          )
        })}
      </ol>
    </nav>
  )
}
