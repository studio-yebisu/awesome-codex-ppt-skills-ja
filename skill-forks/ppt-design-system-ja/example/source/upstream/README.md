# 🎨 PPT Design System

> 从 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) × [Open Design](https://github.com/nexu-io/open-design) 蒸馏而来的 AI 设计系统技能。
>
> **5 套主题色 × 10 种布局 × 字体三层体系**，支持 HTML 单页版和 PPTX 双格式输出。

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-8A2BE2)](https://www.codebuddy.cn)

---

## ✨ 特性

| # | 特性 | 说明 |
|---|------|------|
| 🎨 | **5 套精致主题** | 靛蓝瓷、墨水经典、森林墨、沙丘、极简数据 — 覆盖工程/商务/培训/创意/数据场景 |
| 📐 | **10 种布局模板** | 开场封面、数据大字报、流水线、对比页、大引用…即贴即用 |
| 🔤 | **字体三层体系** | 衬线标题 × 非衬线正文 × 等宽元数据，杂志级排版 |
| 📄 | **双格式输出** | HTML（浏览器直看，效果最佳）+ PPTX（可发送可编辑） |
| 🚫 | **反模式清单** | 内置 P0/P1/P2 自检清单，防 AI 垃圾产出 |
| 🧩 | **WorkBuddy 原生** | 安装即用，自然语言触发，无需手动配置 |

---

## 🖌 5 套主题色

| 风格 | 场景 | 色板 |
|------|------|------|
| 🟦 **靛蓝瓷** | 工程汇报、技术方案 | `#0a1f3d` + `#f1f3f5` |
| ⬛ **墨水经典** | 商务演示、项目提案 | `#0a0a0b` + `#f1efea` |
| 🟩 **森林墨** | 教学培训、课件 | `#1a2e1f` + `#f5f1e8` |
| 🟫 **沙丘** | 创意展示、设计分享 | `#1f1a14` + `#f0e6d2` |
| ⬜ **极简数据** | 数据报告、Dashboard | `#0c0c09` + `#f4f4f1` |

---

## 📐 10 种布局

| 布局 | 用途 | 主题建议 |
|------|------|---------|
| 开场封面 | 首页 Hero | `hero dark` |
| 章节幕封 | 章节分隔 | `hero light/dark` 交替 |
| 数据大字报 | 抛关键数据 | `light` |
| 左文右图 | 图文故事 | `light/dark` 交替 |
| 图片网格 | 多图对比 | `light` |
| 流水线 Pipeline | 工作流程 | `light` |
| 悬念问题 | 引发思考 | `hero dark` |
| 大引用 | 金句高亮 | `dark` |
| 并列对比 | 旧 vs 新 | `light` |
| 图文混排 | 信息密集页 | `light/dark` 交替 |

---

## 🚀 快速开始

### 安装

**方式一：手动安装（推荐）**

将整个仓库克隆或下载到 WorkBuddy 的技能目录：

```bash
# 用户级技能（个人使用）
cp -r ppt-design-system ~/.workbuddy/skills/ppt-design-system
```

**方式二：WorkBuddy 技能市场上传**

打开 WorkBuddy → 技能栏 → 添加技能 → 上传技能 → 选择本项目的 zip 包。

### 使用

安装后，直接对 WorkBuddy 说：

> _"帮我做一份工程汇报 PPT"_
> _"靛蓝瓷风格，做 8 页的季度总结"_
> _"用森林墨样式生成一份培训课件"_

系统会自动加载技能，按以下流程工作：

1. 确认场景 → 选择风格主题
2. 选择输出格式（HTML 或 PPTX）
3. 选取布局 → 填充内容
4. 自检清单 → 输出交付

---

## 📂 项目结构

```
ppt-design-system/
├── SKILL.md                    # 技能主文件（工作流 + 设计规范）
├── README.md                   # 本文件
├── README.en.md                # English version
├── LICENSE                     # MIT 许可证
├── .gitignore
├── references/
│   ├── themes.md               # 5 套主题色完整 CSS 变量 + 字体映射
│   ├── layouts.md              # 10 种布局骨架 + CSS 类名
│   └── presets.md              # 场景推荐 + 典型案例结构
├── assets/
│   └── template.html           # 可直接运行的 HTML 演示模板
└── examples/
    ├── demo-design.html        # 工程汇报 Demo（HTML 版）
    └── demo-engineering-report.pptx  # 工程汇报 Demo（PPTX 版）
```

---

## 🧠 设计哲学

本技能的设计规范蒸馏自两个优秀开源项目：

1. **克制优于炫技** — 依靠字体对比 + 网格留白，不靠阴影和浮动装饰
2. **结构优于装饰** — 信息层级由字号和字体共同定义
3. **排版三层体系** — 衬线标题 / 非衬线正文 / 等宽元数据
4. **图片是第一公民** — 标准比例，只裁底部不裁顶部
5. **节奏靠暗亮交替** — hero 页与正文页交替，避免视觉疲劳
6. **反模式清单** — 禁止紫色渐变、禁止 emoji、禁止圆角卡片左边界线

---

## 🙏 致谢

本技能的设计规范灵感来源于：

- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) by [歸藏](https://x.com/op7418) — 杂志风网页 PPT 技能，本技能的 5 套主题色和 10 种布局模板均蒸馏自此
- [Open Design](https://github.com/nexu-io/open-design) by nexu-io — Claude Design 的开源替代，129 套设计系统为本技能的企业规范提供参考

感谢这两个优秀开源项目的启发，让 AI 生成的设计不再"一眼 AI"。

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🤝 贡献

欢迎提交 Issue 和 PR！如果你想新增一套主题色：

1. 在 `references/themes.md` 中新增主题色 CSS 变量
2. 在 `references/presets.md` 中补充场景说明
3. 在 `SKILL.md` 的风格一览表中添加新条目
