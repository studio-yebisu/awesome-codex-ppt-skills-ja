# Contributing to Sketch Notes PPT

感謝你有興趣為這個專案貢獻！以下是參與方式。

## 🤝 How to Contribute

### 提交新的 Demo 簡報

1. Fork 本倉庫
2. 使用 `skill/SKILL.md` 生成一份簡報
3. 將 `.html` 檔案放入 `demo/` 資料夾
4. 提交 Pull Request，說明主題與使用的 Style

### 改進視覺元件

1. 修改 `style/sketch-notes-base.css`
2. 確認所有現有 demo 不受影響
3. 在 PR 中附上修改前後的截圖

### 新增 Style Variant

1. 在 `skill/SKILL.md` 的 Phase 3.5 段落新增 `:root` token block
2. 在 `style/STYLE_GUIDE.md` 補充說明
3. 提供一份使用該 Style 的 demo

### 改進 SKILL.md

Skill 指令是本專案的核心。修改時請注意：
- 保持總行數 ≤ 400 行
- 不要破壞現有的 Phase 結構
- 確認修改後 AI 仍能正確生成簡報

## 📋 Pull Request 規範

- **一個 PR 只做一件事** — 別把 bugfix 和新功能混在一起
- **提供截圖** — 如果涉及視覺變更，附上瀏覽器截圖
- **寫清楚描述** — 說明你改了什麼、為什麼要改

## 🐛 Bug Reports

如果生成的簡報有問題，請提交 Issue 並附上：

1. 使用的 AI 工具（Antigravity / Claude Code / Gemini CLI 等）
2. 使用的 Style（sketch-notes / minimal / dark-pro / data-viz）
3. 問題截圖
4. 生成的 HTML 檔案（如方便）

## 📐 Code Style

- CSS 尺寸一律使用 `clamp()`，禁止寫死 `px`
- CJK 文字容器加上 `word-break: break-word`
- 高度使用 `dvh` 並提供 `vh` fallback
- 禁止使用 Inter / Roboto / Arial 等通用字型

## 🗂️ 目錄結構

```
sketch-notes-ppt/
├── skill/          # AI skill 指令（核心）
│   └── SKILL.md
├── style/          # CSS 與設計文件
│   ├── sketch-notes-base.css
│   └── STYLE_GUIDE.md
├── demo/           # 展示用範例簡報
├── output/         # 生成的簡報（gitignored）
├── LICENSE         # MIT
└── README.md
```

## License

提交 PR 即表示你同意以 [MIT License](LICENSE) 授權你的貢獻。
