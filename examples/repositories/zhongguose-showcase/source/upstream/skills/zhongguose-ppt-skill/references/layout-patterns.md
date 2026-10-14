# 版式模式 / Layout Patterns

## 目录 / Contents

1. 选择原则 / Selection rules
2. 模式库 / Pattern library
3. 密度与适配 / Density and fit
4. 导航规则 / Navigation rules

## 1. 选择原则 / Selection rules

先确定页面职责，再选择最接近的模式。不得因为模板有某种版式，就改变原稿逻辑去迎合它。

Choose the layout after the slide role is clear. Never reshape source logic merely to fill a template.

每页只使用一个主版式。正文区不叠加三个以上视觉层级，不用大量圆角卡片分割连续论述。

Use one primary layout per slide. Avoid more than three competing visual tiers and avoid card grids for continuous arguments.

## 2. 模式库 / Pattern library

### Cover / 封面

适用：标题、主题、副标题和署名。

Use for title, theme, subtitle, and authorship.

- 中文标题使用 Zhongguose Cover；
- 英文副标题小一至两级；
- 主题色只承担一块明确色域；
- 不在封面堆目录、长摘要或多组数字。

### Statement / 核心判断

适用：开场观点、转折判断、阶段结论。

Use for opening claims, pivots, and section conclusions.

- 一个大编号或单字作为节奏锚点；
- 一句中文判断占主位；
- 英文只提供精炼翻译；
- 最多增加一段支撑说明。

### Principles / 并列原则

适用：二至三条同级原则、维度或标准。

Use for two or three peer principles, dimensions, or criteria.

- 每列保持同一信息结构；
- 标题短，说明不超过两行主要语义；
- 三列出现明显长短差异时改用 Ledger。

### Divider / 章节扉页

适用：进入新的一级章节。

Use at the start of a top-level section.

- 展示章节编号、中文章节名和一句说明；
- 不显示完整导航轨道；
- 使用封面字体，但不要重复封面全部信息。

### Ledger / 条目账册

适用：定义、分类、要点及其解释。

Use for definitions, categories, points, and explanations.

- 左栏负责本页判断或关键数字；
- 右栏用横向条目建立秩序；
- 条目超过四个时拆页；
- 每条英文紧跟对应中文。

### Sequence / 顺序路径

适用：时间线、流程、阶段或因果链。

Use for chronology, process, stages, or causal chains.

- 二至四步为宜；
- 用编号和边界表达顺序，不依赖装饰箭头；
- 每一步只保留动作和必要解释；
- 复杂分支改用独立流程图，不塞入此模式。

### Matrix / 二乘二关系

适用：四组对应关系、双轴分类或正反组合。

Use for four related groups, two-axis classification, or paired contrasts.

- 四格必须真正具有同一比较维度；
- 只突出一个关键格；
- 浅色主题必须使用 accent-on 的墨色前景；
- 若内容不存在二维关系，改用 Principles 或 Ledger。

### Closing / 收束

适用：总结、主张回扣和结束页。

Use for synthesis, final claim, and closing.

- 回扣全文主线，不新增论点；
- 中文结论保持最大视觉权重；
- 右侧色域只放页码、署名或简短信息。

## 3. 密度与适配 / Density and fit

在 1920×1080 下：

- 中文正文不小于 24px；
- 中文主标题通常为 48–88px；
- 英文辅助通常为中文正文的 55%–72%；
- 每页主要内容块不超过四个；
- 页面四周保留明确安全边界。

At 1920×1080, keep Chinese body copy at least 24px, main titles 48–88px, English support visibly smaller, no more than four primary blocks, and clear safe margins.

在 1366×768 下出现溢出时，按顺序处理：

1. 删除重复和次级说明；
2. 拆页；
3. 改用更适合长文的 Ledger；
4. 降低非核心字号；
5. 最后才微调间距。

When 1366×768 overflows, remove repetition, split the slide, choose a denser layout, reduce secondary type, and only then tighten spacing.

不要通过整体缩小到不可读字号解决溢出。

Never solve overflow by shrinking the entire slide below readable sizes.

## 4. 导航规则 / Navigation rules

内容页使用 chapter-rail：

- 展示全部一级章节；
- 当前章节恰有一个 aria-current="step"；
- 标签来自用户文档，不套用模板标签；
- 封面、章节扉页和结束页可不显示完整导航。

Content slides show all top-level sections in chapter-rail with exactly one active item. Labels must come from the source, while cover, divider, and closing slides may omit the full rail.
