import type { ComponentType } from 'react'

export interface PresentationEntry {
  slug: string
  title: string
  load: () => Promise<{ default: ComponentType }>
}

/** Explicit registry — add a folder + one line here for each presentation. */
export const presentations: PresentationEntry[] = []

export const presentationSlugs = new Set(presentations.map((p) => p.slug))
