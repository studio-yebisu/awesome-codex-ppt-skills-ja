import type { CSSProperties, ReactNode } from 'react'
import { motion, type HTMLMotionProps } from 'motion/react'
import type { LucideIcon } from 'lucide-react'
import { ENTER_T, LAYOUT_T } from '../constants'

/**
 * Newcomer entrance. Wrap a *genuinely new* element (one that has no prior
 * layoutId to morph from) in this, and it fades in after a short beat instead of
 * appearing at full strength immediately. The point is sequencing: the pieces
 * already on screen morph to their new positions first and lead the eye, then
 * the new piece arrives — rather than everything happening at once, which reads
 * as confusing. Continuing elements should NOT use this; they morph via layoutId
 * and are the motion the newcomer waits on. Pass a `key` (e.g. the node id) when
 * the same slot hosts a different newcomer each step, so it re-fades each time.
 */
export function Appear({
  children,
  delay,
  className,
}: {
  children: ReactNode
  delay?: number
  className?: string
}) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={delay === undefined ? ENTER_T : { ...ENTER_T, delay }}
      className={className}
    >
      {children}
    </motion.div>
  )
}

/**
 * One step's diagram layer: absolutely-positioned and self-centered inside the
 * fixed design canvas. Because layers don't share normal flow, mounting one
 * never reflows another — so shared layoutId elements morph between steps
 * without a reflow jump. Defaults can be overridden per step (e.g. a custom
 * exit) by passing the prop through.
 */
export function SceneLayer({ children, style, ...rest }: HTMLMotionProps<'div'>) {
  return (
    <motion.div
      exit={{ opacity: 0 }}
      transition={LAYOUT_T}
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        ...(style as CSSProperties | undefined),
      }}
      {...rest}
    >
      {children}
    </motion.div>
  )
}

type Accent = string

export function MotionNode({
  transition = LAYOUT_T,
  ...rest
}: HTMLMotionProps<'div'>) {
  return <motion.div transition={transition} {...rest} />
}

export function Box({
  layoutId,
  Icon,
  label,
  subtitle,
  accent = 'gray',
  className = '',
  style,
}: {
  layoutId: string
  Icon?: LucideIcon
  label: string
  subtitle?: string
  accent?: Accent
  className?: string
  style?: CSSProperties
}) {
  return (
    <motion.div
      layoutId={layoutId}
      transition={LAYOUT_T}
      className={className}
      style={style}
      data-node="box"
      data-accent={accent}
    >
      {Icon && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ ...LAYOUT_T, delay: 0.15 }}
          data-node-part="icon"
          aria-hidden
        >
          <Icon />
        </motion.div>
      )}
      <div data-node-part="label">{label}</div>
      {subtitle && <div data-node-part="subtitle">{subtitle}</div>}
    </motion.div>
  )
}

export function Label({
  layoutId,
  children,
  className = '',
  style,
}: {
  layoutId: string
  children: ReactNode
  className?: string
  style?: CSSProperties
}) {
  return (
    <motion.div
      layoutId={layoutId}
      transition={LAYOUT_T}
      className={className}
      style={style}
      data-node="label"
    >
      {children}
    </motion.div>
  )
}

export function Arrow({
  layoutId,
  children,
  className = '',
  style,
}: {
  layoutId: string
  children?: ReactNode
  className?: string
  style?: CSSProperties
}) {
  return (
    <motion.div
      layoutId={layoutId}
      transition={LAYOUT_T}
      className={className}
      style={style}
      data-node="arrow"
    >
      {children ?? '→'}
    </motion.div>
  )
}

export function Frame({
  layoutId,
  label,
  children,
  className = '',
  style,
}: {
  layoutId: string
  label?: string
  children: ReactNode
  className?: string
  style?: CSSProperties
}) {
  return (
    <motion.div
      layoutId={layoutId}
      transition={LAYOUT_T}
      className={className}
      style={style}
      data-node="frame"
    >
      {label && <span data-node-part="frame-label">{label}</span>}
      {children}
    </motion.div>
  )
}

export function Emphasis({
  layoutId,
  children,
  accent = 'cyan',
  className = '',
  style,
}: {
  layoutId: string
  children: ReactNode
  accent?: Accent
  className?: string
  style?: CSSProperties
}) {
  return (
    <motion.div
      layoutId={layoutId}
      transition={LAYOUT_T}
      className={className}
      style={style}
      data-node="emphasis"
      data-accent={accent}
    >
      {children}
    </motion.div>
  )
}

export function SymbolChip({
  layoutId,
  Icon,
  label,
  subtitle,
  accent = 'cyan',
  variant,
  className = '',
  style,
}: {
  layoutId: string
  Icon: LucideIcon
  label: string
  subtitle?: string
  accent?: Accent
  variant: 'symbol' | 'chip'
  className?: string
  style?: CSSProperties
}) {
  const isSymbol = variant === 'symbol'

  return (
    <motion.div
      layoutId={layoutId}
      transition={LAYOUT_T}
      className={className}
      style={style}
      data-node="symbol-chip"
      data-accent={accent}
      data-variant={variant}
    >
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ ...LAYOUT_T, delay: isSymbol ? 0.22 : 0.06 }}
        data-node-part="icon"
        aria-hidden
      >
        <Icon />
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ ...LAYOUT_T, delay: isSymbol ? 0.3 : 0.1 }}
        data-node-part="body"
      >
        <div data-node-part="label">{label}</div>
        {isSymbol && subtitle && <div data-node-part="subtitle">{subtitle}</div>}
      </motion.div>
    </motion.div>
  )
}
