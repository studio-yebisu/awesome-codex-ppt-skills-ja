# Presentation Delivery Skills

Build presentations that look intentional and explain the point in plain language.

This repository packages three complementary Codex skills:

- `visual-deck-studio`: designs and produces high-fidelity HTML decks, editable PPTX files, PDFs, prototypes, and visual demonstrations.
- `human-intent-audit`: traces a user's natural-language goal to observable outcomes and evidence, so a green check does not hide a missed requirement.
- `owner-facing-reporting`: turns implementation evidence into a concise owner-readable result, including what is usable now and what remains.

## The two-part delivery model

1. **Visual deck**: make the presentation clear, distinctive, and pleasant to use.
2. **Plain-language brief**: state the problem, the decision, the result, and any remaining gap without implementation jargon.

The skills can be used independently. Together they provide a simple path:

```text
User goal
  -> human-intent-audit
  -> visual-deck-studio
  -> owner-facing-reporting
  -> an inspectable presentation and a clear decision summary
```

## Demo: From chat to delivery

[![Cover of the Agent, Skill, Harness, and Hermes presentation](demos/agent-skill-harness-hermes/previews/01-cover.png)](demos/agent-skill-harness-hermes/README.md)

The [Agent, Skill, Harness, and Hermes](demos/agent-skill-harness-hermes/README.md)
deck is a finished nine-slide artifact made with this delivery model. It explains
why a chat model alone leaves work unfinished, how the three skills close that
gap, and how a concrete Agent runtime fits into the relationship.

- [View the walkthrough and previews](demos/agent-skill-harness-hermes/README.md)
- [Download the editable PPTX](demos/agent-skill-harness-hermes/agent-skill-harness-hermes-demo.pptx)
- [Read the native PowerPoint PDF](demos/agent-skill-harness-hermes/agent-skill-harness-hermes-demo.pdf)

## Install

Copy the three directories under `skills/` into your Codex skills directory.

```powershell
$target = if ($env:CODEX_HOME) {
  Join-Path $env:CODEX_HOME 'skills'
} else {
  Join-Path $HOME '.codex\skills'
}

New-Item -ItemType Directory -Force -Path $target | Out-Null
Get-ChildItem '.\skills' -Directory | Copy-Item -Recurse -Force -Destination $target
```

`visual-deck-studio` uses Node.js dependencies for its export and verification helpers:

```powershell
Set-Location '.\skills\visual-deck-studio'
npm install
```

## Verify the package

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-package.ps1
```

The validator checks that the three skill entrypoints are present, the Ethan license is in place, and common local-only artifacts or stale identifiers are absent.

## Repository layout

```text
skills/
  visual-deck-studio/
  human-intent-audit/
  owner-facing-reporting/
scripts/
  validate-package.ps1
```

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Do not include credentials, private customer data, or machine-specific paths in contributions.

## Security

Read [SECURITY.md](SECURITY.md) for responsible reporting guidance.

## License

MIT. See [LICENSE](LICENSE).
