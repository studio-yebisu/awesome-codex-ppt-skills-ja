# Contributing

Thanks for considering a contribution to MBB Page Maker.

## Pull Request Rules

- `main` is a protected branch.
- Saitop may push directly to `main`.
- All other collaborators and external contributors should submit changes through pull requests.
- Keep each PR focused on one purpose.
- Avoid unrelated formatting churn, generated artifacts, or broad rewrites unless they are the point of the PR.

## Before Opening a PR

- Describe the motivation and user-facing impact of the change.
- Include screenshots, rendered output, or deck previews when the change affects visual presentation.
- Run the relevant checks for the files you changed. For deck/template changes, use:

```bash
scripts/check-deck-quality.sh path/to/deck.html
scripts/check-deck-contrast.sh path/to/deck.html
```

- Note any checks you could not run.

## Repository Hygiene

- Prefer static HTML, CSS, and JavaScript. Do not add a build step without prior discussion.
- Do not introduce CDN dependencies into source decks or generated packages.
- Keep templates reusable and avoid embedding private client data.
- Keep examples and generated demo artifacts intentional.
