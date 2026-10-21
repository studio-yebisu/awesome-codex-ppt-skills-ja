# 主题色预设 (蒸馏自 guizang-ppt-skill)

5 套精心调配的主题色板。**不允许用户自定义色值**，只从以下预设中挑选。

## 使用方法

替换模板 `:root {` 块中标注"主题色"的 6 行 CSS 变量：
```css
--ink / --ink-rgb      /* 文字/主色 */
--paper / --paper-rgb  /* 背景色 */
--paper-tint            /* 背景微染色 */
--ink-tint              /* 文字微染色 */
```

其余 CSS 都走 `var(--...)`，改 `:root` 一处即可全局生效。

---

## 🟦 靛蓝瓷 (Indigo Porcelain)

| 属性 | 值 | 适合场景 |
|------|-----|---------|
| **色值** | `--ink: #0a1f3d` | 工程汇报、技术方案、进度报告 |
| **调性** | 深靛蓝 + 瓷白，冷静、理性、专业 | 数据展示、项目管理 |

```css
--ink: #0a1f3d;
--ink-rgb: 10, 31, 61;
--paper: #f1f3f5;
--paper-rgb: 241, 243, 245;
--paper-tint: #e4e8ec;
--ink-tint: #152a4a;
--accent: #3b82f6;
--success: #16a34a;
--warning: #d97706;
--danger: #dc2626;
```

---

## ⬛ 墨水经典 (Monocle Classic)

| 属性 | 值 | 适合场景 |
|------|-----|---------|
| **色值** | `--ink: #0a0a0b` | 商务演示、项目提案、通用发布 |
| **调性** | 纯墨黑 + 暖米白，杂志感最强 | 不知道选啥的默认选择 |

```css
--ink: #0a0a0b;
--ink-rgb: 10, 10, 11;
--paper: #f1efea;
--paper-rgb: 241, 239, 234;
--paper-tint: #e8e5de;
--ink-tint: #18181a;
--accent: #3b82f6;
--success: #16a34a;
--warning: #d97706;
--danger: #dc2626;
```

---

## 🟩 森林墨 (Forest Ink)

| 属性 | 值 | 适合场景 |
|------|-----|---------|
| **色值** | `--ink: #1a2e1f` | 教学培训、课件、自然主题 |
| **调性** | 深森林绿 + 象牙，沉稳、有呼吸感 | 需要亲和力的内容 |

```css
--ink: #1a2e1f;
--ink-rgb: 26, 46, 31;
--paper: #f5f1e8;
--paper-rgb: 245, 241, 232;
--paper-tint: #ece7da;
--ink-tint: #253d2c;
--accent: #2d8a4e;
--success: #16a34a;
--warning: #d97706;
--danger: #dc2626;
```

---

## 🟫 沙丘 (Dune)

| 属性 | 值 | 适合场景 |
|------|-----|---------|
| **色值** | `--ink: #1f1a14` | 创意展示、设计分享、个人品牌 |
| **调性** | 炭灰 + 沙色，克制、高级、中性 | 审美优先的场景 |

```css
--ink: #1f1a14;
--ink-rgb: 31, 26, 20;
--paper: #f0e6d2;
--paper-rgb: 240, 230, 210;
--paper-tint: #e3d7bf;
--ink-tint: #2d2620;
--accent: #c9955e;
--success: #5b8c5a;
--warning: #d97706;
--danger: #dc2626;
```

---

## ⬜ 极简数据 (Minimal Data)

| 属性 | 值 | 适合场景 |
|------|-----|---------|
| **色值** | `--ink: #0c0c09` | 数据报告、Dashboard、分析报告 |
| **调性** | 纯粹黑白灰，干净利落 | Open Design Minimal 风格 |

```css
--ink: #0c0c09;
--ink-rgb: 12, 12, 9;
--paper: #f4f4f1;
--paper-rgb: 244, 244, 241;
--paper-tint: #e8e8e4;
--ink-tint: #1a1a17;
--accent: #404040;
--success: #16a34a;
--warning: #d97706;
--danger: #dc2626;
```

---

## PPTX 字体映射 (Windows 环境)

由于 PPTX 无法保证自定义字体在所有电脑上显示，按以下规则映射：

| HTML 字体层 | CSS 字体 | PPTX 映射(Windows) |
|-------------|---------|-------------------|
| 中文衬线标题 | Noto Serif SC | 微软雅黑 Bold |
| 英文衬线标题 | Playfair Display | Georgia Bold |
| 中文非衬线正文 | Noto Sans SC | 微软雅黑 Regular |
| 英文非衬线正文 | Inter | Calibri |
| 中文等宽元数据 | IBM Plex Mono | Consolas |

## 禁止事项

- ❌ 不允许混搭（如 ink 取靛蓝瓷、paper 取沙丘）
- ❌ 不允许用户给任意 hex 值
- ❌ 不要修改模板中其他地方的颜色（所有散落 rgba 都走 var）
- ❌ 一份 deck 只用一套主题，不要中途换色
