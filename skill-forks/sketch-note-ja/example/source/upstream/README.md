<div align="center">

# 🎨 Sketch Notes PPT

**AI-generated Sketch Notes style presentations — self-contained HTML, zero dependencies**

[Demo](#-demo) · [Quick Start](#-quick-start) · [Use with AI Tools](#-use-with-ai-coding-tools) · [Visual Components](#-visual-components) · [Style Guide](style/STYLE_GUIDE.md) · [Contributing](CONTRIBUTING.md)

</div>

> 💛 Sponsored by **[PathUnfold](https://pathunfold.com)** — 用 AI 發電，探索 AI 時代的個人成長路徑。

---

## What is this?

**Sketch Notes PPT** is an AI skill that generates beautiful, self-contained HTML presentations in a distinctive **Sketch Notes** visual style — manga-inspired comic borders, speech bubbles, halftone patterns, and crosshatch textures.

Just tell any AI coding tool: *"Make a PPT about [topic]"* and get a complete `.html` file you can open in any browser. No npm, no build step, no dependencies.

> **Philosophy:** One idea per slide. One personality per deck.

---

## 🎨 Demo

Open any demo in your browser — no build step required:

| Demo | Description |
|------|-------------|
| [`demo-index.html`](demo/demo-index.html) | AI Agent 工具選擇指南（sketch-notes style） |
| [`notebooklm-intro-ppt.html`](demo/notebooklm-intro-ppt.html) | NotebookLM 介紹簡報（sketch-notes style） |

**Keyboard shortcuts:**
| Key | Action |
|-----|--------|
| `→` or `Space` | Next slide |
| `←` | Previous slide |
| Swipe left/right | Mobile navigation |

---

## 🚀 Quick Start

### Option A: Let AI generate a deck

1. Copy [`skill/SKILL.md`](skill/SKILL.md) into your AI agent
2. Tell the AI: *"Make a PPT about [your topic]"*
3. The AI outputs a complete `.html` file — open in browser, done!

### Option B: Build from the template

1. Copy `demo/demo-index.html` as a starting point
2. Edit slide content directly in HTML

### Option C: Use the CSS library

```html
<link rel="stylesheet" href="style/sketch-notes-base.css">
```

---

## 🤖 Use with AI Coding Tools

The [`skill/SKILL.md`](skill/SKILL.md) file is a universal instruction set that works with any AI coding assistant. Pick your tool:

### Antigravity (Google Agent Manager)

```bash
# Install as a skill
cp skill/SKILL.md ~/.gemini/antigravity/skills/sketch-notes-ppt/SKILL.md
```

Trigger: *"做一個 PPT 關於 [主題]"* or *"Make a PPT about [topic]"*

### Claude Code

```bash
claude "Read skill/SKILL.md and generate a PPT about [topic]"
```

Or paste `skill/SKILL.md` content directly into the conversation as system instructions.

### OpenAI Codex

```bash
codex "Read skill/SKILL.md and generate a PPT about [topic]"
```

### Gemini CLI

```bash
gemini "Generate a presentation about [topic] following these instructions: @skill/SKILL.md"
```

### OpenClaw

Add `skill/SKILL.md` as a skill file in your OpenClaw configuration, then trigger via Discord/chat.

### Any Other AI Tool

The skill works with **any** LLM that can follow markdown instructions:

1. Copy the contents of [`skill/SKILL.md`](skill/SKILL.md)
2. Paste it into the AI's system prompt or conversation
3. Ask: *"Make a PPT about [your topic]"*
4. The AI outputs a self-contained `.html` file — open in browser, done!

---

## 🎨 Visual Components

See [`style/STYLE_GUIDE.md`](style/STYLE_GUIDE.md) for full details.

| Component | Class | Best For |
|-----------|-------|---------|
| Speech bubble | `.bubble` | Key takeaways, author voice |
| Tool cards | `.tools-grid` + `.tool-card` | Comparing 4–6 items |
| Insight cards | `.insight-grid` + `.insight-card` | Numbered principles |
| Decision tree | `.decision-tree` | "How to choose?" flows |
| Comparison table | `.compare-table` | Head-to-head features |
| Emphasis box | `.emphasis-box` | One powerful statement |

---

## 🎬 Want more?

Check out [**agentic-ppt**](https://github.com/Watermelon4000/agentic-ppt) for additional tools:
- ✏️ **Canvas Drag Editor** — visually edit slides in browser
- 🎬 **A-roll → Video** — turn slides into explainer videos (Remotion)
- 🎙️ **TTS → Video** — script-to-video pipeline

---

## 🤝 Contributing

Welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT — use freely, attribution appreciated.

---

<div align="center">

Made with ✦ AI + human taste · Sponsored by [PathUnfold](https://pathunfold.com)

</div>
