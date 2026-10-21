export type Route =
  | { kind: 'landing' }
  | { kind: 'presentation'; slug: string }

export function resolveRoute(pathname: string, slugs: ReadonlySet<string>): Route {
  if (pathname === '/' || pathname === '') return { kind: 'landing' }
  const slug = pathname.replace(/^\//, '').replace(/\/$/, '')
  if (slug && slugs.has(slug)) return { kind: 'presentation', slug }
  return { kind: 'landing' }
}
