<p align="center">
  <img src="examples/slide-writer.png" alt="Slide-Writer" width="200"/>
</p>

# Slide-Writer

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/FeeiCN/slide-writer/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-feei.cn-blue.svg)](https://feei.cn/slide-writer/examples/)
[![中文](https://img.shields.io/badge/文档-中文-red.svg)](README.zh-CN.md)

> Focus on goals, viewpoints, and judgment. Slide-Writer handles structure, writing, refinement, and presentation.

<p align="center">
  <a href="https://feei.cn/slide-writer/examples/">
    <img src="examples/before-after.png" alt="Slide-Writer Demo" width="100%"/>
  </a>
</p>

## Quick Start

> Works best with **Claude Code** or **Codex**, paired with a capable model — Claude Sonnet, Claude Opus, or GPT-4o recommended.

```bash
# Claude Code
git clone https://github.com/FeeiCN/slide-writer.git ~/.claude/skills/slide-writer

# Codex
git clone https://github.com/FeeiCN/slide-writer.git ~/.agents/skills/slide-writer
```

```text
/slide-writer Generate a presentation on "Why do humans need to eat?" using Alipay style.
```

```text
/slide-writer Use the speech draft in examples/tencent-pony-ma.md to generate a presentation.
```

```text
/slide-writer I have a speech tomorrow. Turn examples/alibaba-ai-rollout.md into a deck.
```

## Core Features

**Any input → enterprise-grade deck**: sentence, outline, speech draft, notes, or existing HTML — Slide-Writer restructures and rewrites it into a presentation-ready format.

**14 brand themes, auto-detected**: covers Ant Group, Alibaba, Tencent, ByteDance, and more. Drop a keyword and the right theme, logo, and colors are applied automatically.

**Single-file delivery**: outputs one standalone HTML file — CSS, JS, and images all embedded. Opens in any browser. No PowerPoint, no Keynote, no dependencies.

**Always up to date**: pulls the latest themes, components, and generation rules automatically on every run.

## Repository Structure

- `SKILL.md`: skill definition and execution rules
- `themes/_index.md`: theme identification and logo index
- `themes/[id].md`: per-theme style and logo rules
- `components.md`: page component library
- `template.html`: baseline generation shell
- `examples/index.html`: page skeleton gallery and full example deck
- `examples/`: sample inputs and outputs
- `TESTING.md`: testing notes

### Quick Test

1. Pick one sample from [examples](examples).
2. Ask the model to generate a `test-*.html` based on this repo's `SKILL.md`.
3. Run:

```bash
./scripts/preview.sh
```

4. Open `http://localhost:8000/test-xxx.html` in a browser.

See [TESTING.md](TESTING.md) for the full testing flow and regression checklist.

---

If Slide-Writer saved you time, consider giving it a ⭐ — it helps others find the project.
