---
name: neon-slides
description: 生成深色科技感(neon dark)风格的 HTML 幻灯片/演示页面,橙蓝对比配色,适合技术文章解读、架构讲解、产品介绍、课程大纲、直播课件等技术类内容。中文触发:「做一份深色科技风幻灯片」「把这篇文章做成 slides」「生成一个技术课件」「做个直播 deck」「把大纲变成演示页面」「dark tech 风格的幻灯片」。English triggers: "make a dark tech slide deck", "turn this outline into neon slides", "generate an HTML presentation for my tech talk", "create a landing-style slide deck". 只生成单文件 HTML(非 .pptx),支持键盘翻页、跳转、投屏直播。不要用于短图文封面、小红书配图、需要 PowerPoint 格式交付的场景。
---

# Neon Slides

## ⚠️ 硬性规则 — 所有模型必须遵守(MUST READ FIRST)

这一节的规则**优先级最高**,如果与后文任何说明冲突,以本节为准。违反任何一条都会导致风格崩坏。

### 规则 1:必须基于 template.html 而不是重写

**正确流程:** 打开 `template.html` → 复制完整文件 → **只修改 `<body>` 里 `<div class="deck">` 内部的 `<section class="slide">` 块** → 保存为新文件。

**禁止:**
- ❌ 禁止重写、精简、"优化"、替换 `<style>` 块里的 CSS。一行都不要改。
- ❌ 禁止重写 `<script>` 块里的导航 JS(键盘翻页、跳转面板、圆点点击逻辑)。
- ❌ 禁止修改 `:root` 里的 CSS 变量。颜色就是 `--orange:#F97316` 和 `--blue:#3B82F6`,不要调。
- ❌ 禁止删除 `<link>` 字体引用。字体就是 Noto Sans SC + Space Grotesk,不要换。

**唯一允许的修改范围:**
1. `<title>` 标签内的文字
2. `<div class="deck">` 里的所有 `<section class="slide">` 内容
3. 如果真的需要一个模板里没有的组件样式,在 `<style>` 块**末尾追加**新类(不要改已有的类)

### 规则 2:只用已定义的类名,禁止发明

下列类名是 skill 的公共词汇,已在 template.html 和 components.md 里定义好了。生成内容时**只从这个清单里选**:

- 屏壳: `.slide` `.slide.active` `.inner` `.deck`
- 封面: `.cover` `.center` `.bg` `.divider` `.meta`
- 过渡屏: `.hero` `.numeral` `.chapter-meta` `.part-label` `.long-divider` `.content`
- 标题高亮: `.accent-o`(橙色渐变文字) `.accent-b`(蓝色渐变文字)
- 小标签: `.tag`(只有一种,永远是橙色,不要造 `.tag.blue` `.tag.green`)
- 流程: `.steps` `.step.o` `.step.b` `.arrow.o` `.arrow.b`
- 对比: `.compare` `.cmp.old` `.cmp.new`
- 架构卡: `.layers` `.layer.o` `.layer.b` `.icon` `.thumb` `.foot`
- 清单: `.list-grid` `.item` `.num` `.txt`
- 图文: `.split` `.split.reverse` `.text` `.media` `.media.o` `.media.b` `.caption`
- 代码: `.code` `.code .k` `.code .s` `.code .c`

**禁止:**
- ❌ 禁止发明新类名(如 `.citem` `.lgi` `.myitem` 等)。
- ❌ 禁止改缩写(`.compare` 就是 `.compare`,不要缩成 `.cmp-grid`)。
- ❌ 如果一个元素在这个清单里找不到合适的类,说明它不该存在——用 components.md 里已有的组件组合来表达同一个意思。

### 规则 3:禁止 inline style 覆盖已有类

**禁止这样写:**
```html
<!-- ❌ 错误:用 inline style 改已有类的颜色 -->
<span style="color:var(--orange)">关键词</span>
<div class="tag" style="display:none">...</div>
<h1 style="background:linear-gradient(...)">...</h1>
```

**正确写法:**
```html
<!-- ✅ 正确:用已定义的类 -->
<span class="accent-o">关键词</span>
<!-- 不想要 tag?直接删掉 HTML,不要 display:none -->
<!-- 标题渐变已经在 .accent-o 里了,不需要自己写 -->
```

**`style="..."` 属性只有三种场景可以用:** (a) 图片 URL 等动态值;(b) 唯一性的微调(如 `margin-top:40px`);(c) `data-num` 等数据属性。**颜色、字体、渐变、背景、display 值一律禁止 inline。**

### 规则 4:组件有明确使用边界,不能乱用

- **第 1 屏必须是 `.cover`** —— 绝对不要用 `.hero` 做首页。`.hero` 只能用于章节过渡(PART 切换),一份 deck 里最多出现 1-2 次。
- **封面必须有 `.tag`** —— 不要用 `display:none` 隐藏它,也不要"为了居中而重造一个"。tag 本身就支持居中,放在 `.cover .center` 里会自动居中。
- **每屏只用一个 `.accent-o`/`.accent-b`** —— 标题里只高亮一个关键词,不要整句染色。
- **`.code` 连续使用不超过 2 屏** —— 代码屏太多观众会累。

### 规则 5:自检清单(生成完后自己过一遍)

在输出 HTML 之前,自问:

1. 我的 `<style>` 块跟 template.html 的 `<style>` 块**一字不差**吗? → 如果改了,回滚。
2. 我有没有用 `.citem` `.lgi` `.myitem` 这种自己造的类名? → 如果有,全部换回规则 2 的清单。
3. 我的 HTML 里有几个 `style="..."`? → 如果超过 5 个,或者里面有 `color/background/gradient/display`,全部清理。
4. 第 1 屏的 `<section>` 有没有 `.cover` 类? → 如果没有,改。
5. 我的 `<script>` 块是不是保留了 `openJumper` `closeJumper` `manyMode` 这些函数名? → 如果没有,说明 JS 被我重写了,回滚到 template.html 的原版 script。

---

## 概述

## 何时用

触发场景:
- 直播课件、课程/训练页、产品介绍页
- 技术架构解读(AI agent、自动化工作流、基础设施、后端架构等)
- 产品/功能拆解(多栏卡片 + 对比)
- 观点型长图文的 web 版

不要用:
- 真需要 .pptx 文件(丢给同事编辑、传统会议场景)→ 用 pptx skill
- 小红书单图、公众号封面 → 用 shouhui-infographic 或 canvas-design
- 纯文本文章 → 用 linyuebanzi-writer

## 视觉规范(不要改)

**配色 CSS 变量:**
```css
--bg:#0A0A0A;      /* 底色,不用纯黑 */
--fg:#EDEDED;      /* 正文 */
--muted:#8A8A8A;   /* 副文案 */
--orange:#F97316;  /* 主强调色 */
--blue:#3B82F6;    /* 次强调色 */
--card:#161616;    /* 卡片背景 */
```

**字体:** Noto Sans SC(中文 400/700/900) + Space Grotesk(英文标签 500/700)。**绝不用** Inter、Roboto、Arial、系统字体。

**标题处理:** 标题里的关键词用 `<span class="accent-o">` 或 `<span class="accent-b">` 包一下,做橙/蓝线性渐变文字。每屏**只高亮一个**词,不要整句染色。

**氛围:** body 背景左上角橙 radial glow + 右下角蓝 radial glow,极淡(透明度 .06-.08),不要调亮。

## 组件库

基础组件(在 `template.html` 里都有现成的类):

1. **`.cover`** — **首页封面专用**,居中构图,大号标题 + 橙色分隔线 + 副标题 + 底部 meta 信息。模糊大图作背景(透明度 35%)+ 中心径向暗化渐变,保证标题视觉居中且不被背景抢戏。**首页必须用这个**,绝对不要用 `.hero` 做首页。
2. **`.tag`** — 左上角小标签,如 `CORE CONCEPT`、`ARCHITECTURE`、`SECURITY`。英文大写,带橙色发光圆点。每屏一个。
3. **`.steps` + `.step.o` / `.step.b`** — STEP 流程卡,橙蓝交替,中间 `→` 箭头。3-5 步最佳。
4. **`.compare`** — 左右两栏对比卡(旧 vs 新 / 传统 vs 我们)。左灰右橙。
5. **`.layers`** — 三栏卡片网格,每张卡顶部 icon box + 标题 + 正文 + 底部虚线 footer 金句。2-4 栏都行。
6. **`.list-grid`** — 用于清单/checklist 类内容,如「7 个常见漏洞」。
7. **`.split`** — 半屏图文(左文右图或 `.split.reverse` 左图右文),讲功能配截图最常用。
8. **`.hero`** — 章节过渡屏专用,左侧超大描边编号 `01/02/03` + 右侧 PART 标签 + 章节标题 + 橙色长分隔线 + 副文案。**只能用作章节切换**(如 10 屏 deck 的第 5 屏从原理篇切到实战篇),**绝对不要用作首页**。10 屏 deck 最多放 1-2 个 `.hero`。
9. **`.layer .thumb`** — Layer 卡内缩略图,替代 icon box,用于产品/工具对比。

### 屏位规则(重要)

- **首页(Slide 0)必须用 `.cover`** — 居中大标题是门面,放左下角会被背景图压住、观众抓不住重点
- **章节过渡屏才用 `.hero`** — 比如 10 屏的 deck,第 1 屏是 `.cover` 封面,第 5 屏如果要从"概念篇"切到"实战篇",这时候用 `.hero` 配一张震撼图做过渡
- **`.cover` 和 `.hero` 视觉上很像但角色完全不同** — cover 是"主角登场",hero 是"场景切换",别搞混

图片来源:网图贴 URL,或在 HTML 旁建 `images/` 目录用相对路径。不确定时用 `https://placehold.co/800x500/0D0D0D/F97316?text=XXX` 先占位。详细用法见 `components.md` 第 8 节。

## 内容套路(neon dark 风格)

- **每屏一个主题** — 不要塞。一屏讲一件事。
- **副标题放金句** — 不是功能描述,是观点。例如不要写「介绍某个架构」,写「XX 不像功能堆砌的 Agent,而像一个真正的生产力栈」。
- **底部 footer 金句** — 每张卡片底部虚线框里放那句能单独发朋友圈的话(如「Agent 不再只是临时聪明,而是能积累认知」)。
- **节奏交替** — 概念屏 → 架构屏 → 对比屏 → 代码/案例屏 → 总结屏。不要连续两屏都是三栏卡。

## 使用步骤

1. 先看 `template.html` 拿基础骨架和已有的两屏范例(CORE CONCEPT + ARCHITECTURE)
2. 根据用户大纲规划屏数和每屏组件类型
3. 一屏一个 `<section class="slide">`,第一屏加 `active` 类
4. 用户给的纯内容 → 按 neon dark 内容套路改写(加金句、加对比、加 footer)
5. 输出单个 HTML 文件,放到 `/mnt/user-data/outputs/`
6. 用 `present_files` 展示

## 针对直播场景的额外提示

- 屏数控制在 8-15 屏,多了现场讲不完
- 代码展示用 `<pre>` 块,底色 `#0D0D0D`,橙色左边框
- 投屏 1920×1080 最佳,`.inner` 的 `max-width:1200px` 保证两边不顶满
- 键盘 ← → 翻页,空格也是下一页,直播时不用碰鼠标

## 导航交互(已内置,不用改)

模板自带完整导航系统,屏数自适应:

- **15 页以内** — 底部圆点可点击跳转
- **15 页以上** — 自动切换为细进度条(可点击任意位置跳转)
- **键盘快捷键(任意页数)**:
  - `←` / `→` / `Space` — 上下翻页
  - `Home` / `End` — 跳首页/末页
  - `G` — 呼出跳转面板,输入页码回车直达,或点击缩略格子
  - `Esc` — 关闭跳转面板

直播中观众问"第 8 页那个配置",按 `G` 输入 `8` 回车就跳过去,零停顿。
