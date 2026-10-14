import { AnimatePresence, motion } from 'motion/react'
import { EASE } from '../constants'
import type { Mode, StepMeta } from '../types'

interface FooterProps {
  steps: StepMeta[]
  step: number
  last: number
  mode: Mode
  homeHref?: string
  onPrev: () => void
  onNext: () => void
  onSelect: (i: number) => void
}

/**
 * Bottom chrome: the per-step caption (browse mode only — the title now lives
 * at the top in both modes), a row of progress dots, and prev/next.
 */
export function Footer({
  steps,
  step,
  last,
  mode,
  homeHref = '/',
  onPrev,
  onNext,
  onSelect,
}: FooterProps) {
  const current = steps[step]
  const browsing = mode === 'browse'

  return (
    <footer
      data-presentation-footer
      style={{ position: 'absolute', left: 0, right: 0, bottom: 0, zIndex: 20, padding: '0 40px 24px' }}
    >
      <div data-presentation-footer-inner style={{ maxWidth: '48rem', margin: '0 auto' }}>
        {/* Browse: the caption sits here, above the dots. Presenter: nothing —
            the title is at the top now, so the band collapses away. */}
        {browsing && (
          <div
            data-presentation-caption-shell
            style={{
              minHeight: '4.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <AnimatePresence mode="wait">
              <motion.p
                key={`caption-${step}`}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.35, ease: EASE }}
                data-presentation-caption
                style={{ textAlign: 'center' }}
              >
                {current.caption}
              </motion.p>
            </AnimatePresence>
          </div>
        )}

        <div
          data-presentation-footer-row
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: browsing ? 'space-between' : 'center',
            gap: browsing ? 12 : 0,
            marginTop: browsing ? 20 : 0,
          }}
        >
          {/* progress dots — centered on their own in presenter mode. In browse
              mode they share the row with the nav, so they take the leftover
              space and wrap rather than shoving prev/next off a narrow screen. */}
          <div
            data-testid="step-progress"
            data-step-count={steps.length}
            data-step-index={step}
            data-presentation-progress
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              minWidth: browsing ? 0 : undefined,
              flex: browsing ? '1 1 0' : undefined,
              flexWrap: browsing ? 'wrap' : undefined,
            }}
          >
            {steps.map((s, i) => (
              <button
                key={s.id}
                onClick={() => onSelect(i)}
                // Consecutive steps in an era share that label, so era alone gives
                // many dots the same name. The position + title make each dot
                // distinct for screen readers; blank-title chrome cards fall back
                // to era.
                aria-label={`Go to step ${i + 1}: ${s.title || s.era}`}
                aria-current={i === step ? 'step' : undefined}
                data-presentation-progress-dot
                data-active={i === step ? 'true' : undefined}
              />
            ))}
          </div>

          {/* nav — hidden in presenter mode */}
          {browsing && (
            <div
              data-presentation-nav
              style={{ display: 'flex', flexShrink: 0, alignItems: 'center', gap: 12 }}
            >
              <button
                onClick={onPrev}
                disabled={step === 0}
                data-presentation-button="previous"
              >
                &#x2190; prev
              </button>
              {/* On the last step there's nowhere further to advance, so the
                  next button becomes an exit back to the home route. */}
              {step === last ? (
                <a href={homeHref} data-presentation-button="home">
                  home
                </a>
              ) : (
                <button onClick={onNext} data-presentation-button="next">
                  next &#x2192;
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </footer>
  )
}
