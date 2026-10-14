# 视觉系统 / Visual System

## 目录 / Contents

1. 主题色 / Theme colors
2. 变量合同 / Token contract
3. 字体与层级 / Typography
4. 色彩使用 / Color use
5. 素材与装饰 / Assets and decoration
6. 可访问性 / Accessibility

## 1. 主题色 / Theme colors

一套演示只选择一行，并同时设置 accent、accent-rgb、accent-on。

Choose one row per deck and always set accent, accent-rgb, and accent-on together.

| 名称 / Name | accent | accent-rgb | accent-on | 气质 / Tone |
| --- | --- | --- | --- | --- |
| 飞泉绿 / Feiquan Green | #497568 | 73, 117, 104 | #ffffff | 沉静青绿 / calm blue-green |
| 藕丝秋 / Lotus Silk Autumn | #D9C6B3 | 217, 198, 179 | #0a0a0a | 温润浅茶 / warm light beige |
| 湘蓝 / Xiang Blue | #4A76A8 | 74, 118, 168 | #ffffff | 沉稳青蓝 / steady azure |
| 绛缨 / Crimson Tassel | #9E3B3B | 158, 59, 59 | #ffffff | 深绛有力 / deep crimson |
| 鸦黄 / Crow Yellow | #E6C24D | 230, 194, 77 | #0a0a0a | 明亮秋黄 / bright autumn yellow |
| 山岚 / Mountain Mist | #B2C9B2 | 178, 201, 178 | #0a0a0a | 雾霭青绿 / misty sage |

选择前打开 assets/theme-cover-gallery.html。浅色主题必须使用墨色 accent-on，不得继续使用白字。

Open assets/theme-cover-gallery.html before selection. Light themes must use the ink accent-on value, never white text.

## 2. 变量合同 / Token contract

模板中的主题变量：

    --accent
    --accent-rgb
    --accent-on
    --accent-soft
    --accent-mid
    --accent-deep

所有主题表面使用 var(--accent)，其文字使用 var(--accent-on)。透明主题色使用 rgba(var(--accent-rgb), alpha)。

Use var(--accent) for themed surfaces, var(--accent-on) for their text, and rgba(var(--accent-rgb), alpha) for translucent variants.

组件 CSS 禁止再次写入：

- 选中主题的 hex；
- 选中主题的 RGB；
- color: white；
- 固定 #fff 或 #ffffff 前景。

Do not hardcode the selected theme hex, RGB, white keyword, or white foreground inside components.

## 3. 字体与层级 / Typography

| 角色 / Role | 字体 / Font | 要求 / Requirement |
| --- | --- | --- |
| 封面与章节题 / Cover and divider title | Zhongguose Cover | 只用于少量大标题 |
| 中文标题 / Chinese title | 宋体系衬线字体栈 | 48px 以上，承担第一层 |
| 中文正文 / Chinese body | 中文黑体字体栈 | 1920×1080 下不小于 24px |
| 英文标题辅助 / English title support | Latin display stack | 中文标题的约 18%–30%，不超过 34px |
| 英文正文辅助 / English body support | Latin display stack | 中文正文的约 50%–65% |

Zhongguose Cover 只覆盖封面和章节扉页的大标题。正文使用系统字体，避免把装饰字体扩散到长段落。

Use Zhongguose Cover only for large cover and divider titles. Keep body copy in system fonts.

中英关系：

- 中文承载完整意义；
- 英文精炼翻译，不逐句等量复制长段落；
- 英文使用更小字号、更浅颜色或更低字重；
- 不把中英文做成同号双标题。
- 中文主标题、章节扉页标题、卡片标题和核心陈述保持纯中文；英文放在导航、元信息、小标签、图注或辅助正文中，不在中文标题下另起一行。

Chinese carries full meaning. Keep Chinese headings, section-divider titles, card titles, and key statements Chinese-only. Put concise English in navigation, metadata, small labels, captions, or supporting body copy rather than on a second line beneath a Chinese title.

## 4. 色彩使用 / Color use

主题色只承担：

- 当前章节导航；
- 关键判断或单个重点单元；
- 编号、分隔线与少量强调；
- 封面或结束页的一块明确色域。

Use the theme color for active navigation, one key emphasis, numbering and rules, and one defined cover or closing field.

不要使用：

- 多主题色混搭；
- 高饱和渐变；
- 大量彩色卡片；
- 模糊玻璃和发光效果；
- 与主题无关的装饰色。

Avoid mixed themes, saturated gradients, colored card grids, glass effects, glows, and unrelated decorative colors.

## 5. 素材与装饰 / Assets and decoration

优先使用用户提供或可验证来源的真实图片。没有素材时使用明确标注的占位区域，不用生成式 SVG 假装真实内容。

Prefer user-supplied or verifiable images. When assets are missing, use clearly labeled placeholder regions rather than fabricated SVG illustrations.

线条、边界与编号承担结构作用。每个装饰元素必须帮助导航、层级或文化气质，不为填空而存在。

Lines, borders, and numbers should support structure. Every decorative element must serve navigation, hierarchy, or cultural tone.

## 6. 可访问性 / Accessibility

- accent 与 accent-on 对比度至少 4.5:1；
- 所有按钮提供 aria-label；
- 键盘可以完成翻页和总览；
- 尊重 prefers-reduced-motion；
- 不只依赖颜色表达当前状态；
- 文字不得在 1366×768 下被裁切。

Require at least 4.5:1 contrast, labeled controls, full keyboard operation, reduced-motion support, non-color state cues, and zero text clipping at 1366×768.
