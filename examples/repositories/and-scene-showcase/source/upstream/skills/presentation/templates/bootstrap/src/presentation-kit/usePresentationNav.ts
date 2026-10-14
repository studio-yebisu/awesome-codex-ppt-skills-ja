import { useCallback, useEffect, useState } from 'react'
import type { Mode } from './types'

/**
 * Step index + presenter/browse mode, driven by the keyboard and surfaced for
 * the on-screen controls.
 *
 *   →/Space/PageDown  next        ←/PageUp  prev        P  toggle mode
 *
 * On touch screens the same next/prev is driven by a horizontal swipe: swipe
 * left to advance, right to go back.
 */
// A swipe must travel this far horizontally, and be clearly more horizontal
// than vertical, before it counts — so taps and vertical scrolls never trip it.
const SWIPE_MIN_PX = 50
const SWIPE_RATIO = 1.5

export function usePresentationNav(stepCount: number, initialMode: Mode = 'browse') {
  const [step, setStep] = useState(0)
  const [mode, setMode] = useState<Mode>(initialMode)

  const last = stepCount - 1
  const next = useCallback(() => setStep((s) => Math.min(last, s + 1)), [last])
  const prev = useCallback(() => setStep((s) => Math.max(0, s - 1)), [])
  const toggleMode = useCallback(
    () => setMode((m) => (m === 'browse' ? 'present' : 'browse')),
    [],
  )

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      // Don't hijack keys aimed at a focused control: Space/arrows on the
      // prev/next buttons or a progress dot should drive that control, not also
      // advance the deck.
      const target = e.target
      if (
        target instanceof HTMLElement &&
        (target.closest('button, a, input, textarea, select') ||
          target.isContentEditable)
      ) {
        return
      }
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault()
        next()
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault()
        prev()
      } else if (e.key === 'p' || e.key === 'P') {
        toggleMode()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [next, prev, toggleMode])

  useEffect(() => {
    // Horizontal swipe = next/prev. We track the start point and decide on
    // release, so the gesture never interferes with scrolling or tapping a
    // control mid-drag.
    let startX = 0
    let startY = 0
    let tracking = false

    const onStart = (e: TouchEvent) => {
      // Single-finger only; a pinch/two-finger gesture isn't a page swipe.
      tracking = e.touches.length === 1
      if (tracking) {
        startX = e.touches[0].clientX
        startY = e.touches[0].clientY
      }
    }
    const onEnd = (e: TouchEvent) => {
      if (!tracking) return
      tracking = false
      const t = e.changedTouches[0]
      const dx = t.clientX - startX
      const dy = t.clientY - startY
      if (Math.abs(dx) < SWIPE_MIN_PX || Math.abs(dx) < Math.abs(dy) * SWIPE_RATIO) return
      if (dx < 0) next()
      else prev()
    }

    window.addEventListener('touchstart', onStart, { passive: true })
    window.addEventListener('touchend', onEnd, { passive: true })
    return () => {
      window.removeEventListener('touchstart', onStart)
      window.removeEventListener('touchend', onEnd)
    }
  }, [next, prev])

  return { step, setStep, next, prev, last, mode, toggleMode }
}
