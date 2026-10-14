import { Sparkles } from 'lucide-react'
import { presentations } from './presentations'

export function Landing() {
  return (
    <main>
      <div>
        <p>and-scene</p>
        <h1>Presentations as evolving diagrams.</h1>
        <p>
          One shared canvas holds the talk together. Each step changes positions,
          labels, focus, or connections while the audience follows one idea as it
          develops.
        </p>

        <section aria-labelledby="presentations-heading">
          <h2 id="presentations-heading">Presentations</h2>
          {presentations.length === 0 ? (
            <p>
              No presentations registered yet. Add one under{' '}
              <code>src/presentations/</code> and register it in{' '}
              <code>index.ts</code>.
            </p>
          ) : (
            <ul>
              {presentations.map((entry) => (
                <li key={entry.slug}>
                  <a href={`/${entry.slug}`}>
                    <Sparkles size={18} aria-hidden /> {entry.title}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </main>
  )
}
