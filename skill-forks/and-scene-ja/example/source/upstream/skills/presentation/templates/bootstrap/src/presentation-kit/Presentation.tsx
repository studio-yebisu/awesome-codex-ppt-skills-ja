import type { ReactNode } from 'react'
import { Footer } from './chrome/Footer'
import { Header } from './chrome/Header'
import { Toc } from './chrome/Toc'
import { Stage } from './Stage'
import { stepMarker } from './stepMarker'
import { usePresentationNav } from './usePresentationNav'
import type { Mode, Step } from './types'

export interface PresentationProps<P extends Record<string, unknown> = Record<string, unknown>> {
  steps: Step<P>[]
  initialMode?: Mode
  title?: string
  /** Optional header brand. Omitted by default; pass a logo or title node to add one. */
  brand?: ReactNode
  /** Home link target for the header brand and the last-step footer button. */
  homeHref?: string
  /** Accessible label for the home link. */
  homeLabel?: string
  /** Full-bleed layer rendered behind the content. */
  background?: ReactNode
  /**
   * Full-bleed layer rendered *above* the content (e.g. a CRT/scanline overlay).
   * Unlike `background`, it paints over the chrome. Pointer events pass through,
   * so it never intercepts clicks. Use `background` for true backdrops.
   */
  overlay?: ReactNode
  /**
   * Override the per-step marker (top-right). Defaults to a zero-padded count.
   * A callback (not a per-step field) so hosts can number relationally — e.g.
   * skip chrome cards and count only body steps.
   */
  marker?: (index: number, steps: Step<P>[]) => string
  /** Small bottom-right attribution link. Defaults to and-scene; pass `null` for an intentional opt-out. */
  attribution?: ReactNode
  /** Attribution target; defaults to the and-scene GitHub repository. */
  attributionHref?: string
}

export function Presentation<P extends Record<string, unknown> = Record<string, unknown>>({
  steps,
  initialMode = 'browse',
  title = 'Presentation',
  brand,
  homeHref = '/',
  homeLabel,
  background,
  overlay,
  marker,
  attribution = 'made by and-scene',
  attributionHref = 'https://github.com/Codagent-AI/and-scene',
}: PresentationProps<P>) {
  const { step, setStep, next, prev, last, mode } = usePresentationNav(steps.length, initialMode)
  // An empty deck has no current step; render a clear placeholder instead of
  // crashing on `steps[step].title`. (Hooks above run unconditionally first.)
  if (steps.length === 0) {
    return (
      <div
        data-presentation={title}
        data-presentation-empty
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        No steps to present.
      </div>
    )
  }
  const current = steps[step]
  const markerText = (marker ?? ((i) => stepMarker(i)))(step, steps)

  return (
    <div
      data-presentation={title}
      style={{
        position: 'relative',
        minHeight: '100vh',
        userSelect: 'none',
        overflow: 'hidden',
      }}
    >
      {background && (
        <div
          data-presentation-background
          style={{ position: 'absolute', inset: 0, zIndex: 0 }}
        >
          {background}
        </div>
      )}
      <div data-presentation-content style={{ position: 'relative', zIndex: 10, minHeight: '100vh' }}>
        <Stage step={current} mode={mode} />
        <Header
          marker={markerText}
          title={current.title}
          brand={brand}
          homeHref={homeHref}
          homeLabel={homeLabel}
        />
        {mode === 'browse' && <Toc steps={steps} step={step} onSelect={setStep} />}
        <Footer
          steps={steps}
          step={step}
          last={last}
          mode={mode}
          homeHref={homeHref}
          onPrev={prev}
          onNext={next}
          onSelect={setStep}
        />
      </div>
      {overlay && (
        <div
          data-presentation-overlay
          style={{ pointerEvents: 'none', position: 'absolute', inset: 0, zIndex: 50 }}
        >
          {overlay}
        </div>
      )}
      {attribution && (
        <a
          href={attributionHref}
          data-presentation-attribution
          style={{
            position: 'absolute',
            right: 16,
            bottom: 8,
            zIndex: 60,
            fontSize: 12,
          }}
        >
          {attribution}
        </a>
      )}
    </div>
  )
}
