import { useMemo } from 'react'
import { Landing } from './Landing'
import { resolveRoute } from './router'
import { PresentationRouter } from './presentations/PresentationRouter'
import { presentationSlugs } from './presentations'

export function Root() {
  const route = useMemo(() => resolveRoute(window.location.pathname, presentationSlugs), [])

  if (route.kind === 'landing') {
    return <Landing />
  }

  return <PresentationRouter slug={route.slug} />
}
