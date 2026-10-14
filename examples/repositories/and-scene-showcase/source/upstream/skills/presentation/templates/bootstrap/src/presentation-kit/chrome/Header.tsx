import { motion } from 'motion/react'
import type { ReactNode } from 'react'
import { EASE } from '../constants'

/**
 * Top chrome: a thin row carrying optional host branding (top-left) and the
 * step marker (top-right), with the step title centered just below it — in
 * **both** modes.
 * The title is keyed so it remounts and fades in on each step change.
 *
 * The era label is no longer shown here — it drives the table of contents down
 * the left margin instead (see Toc).
 *
 * Branding is configurable so adopters can drop in their own logo and home
 * link. If `brand` is omitted, the top-left slot is empty.
 */
export function Header({
  marker,
  title,
  brand,
  homeHref = '/',
  homeLabel = 'And Scene home',
}: {
  marker: string
  title: string
  brand?: ReactNode
  homeHref?: string
  homeLabel?: string
}) {
  return (
    <header
      data-presentation-header
      style={{ position: 'absolute', left: 0, right: 0, top: 0, zIndex: 20, padding: '24px 40px 0' }}
    >
      <div
        data-presentation-header-row
        style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}
      >
        {brand ? (
          <a href={homeHref} aria-label={homeLabel} data-presentation-home>
            {brand}
          </a>
        ) : (
          <span aria-hidden="true" data-presentation-home-spacer />
        )}
        <span data-presentation-marker>{marker}</span>
      </div>
      <motion.h1
        key={title}
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35, ease: EASE }}
        data-presentation-title
        style={{ margin: '12px 0 0', textAlign: 'center' }}
      >
        {title}
      </motion.h1>
    </header>
  )
}
