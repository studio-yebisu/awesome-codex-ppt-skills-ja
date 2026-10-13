# Current Options

## themePack

| themePack | 风格名 | 适配场景 | 适配人群 |
|---|---|---|---|
| `theme01` | 轻拟态风 | 产品介绍、企业汇报、方案说明、轻量级发布 | 创业团队、产品经理、销售顾问、企业内部汇报者 |
| `theme02` | 炫光紫绿风 | 科技发布会、AI/自动驾驶/机器人主题、增长故事、创新项目展示 | 科技公司创始人、技术负责人、品牌市场团队、投资路演团队 |
| `theme03` | 深浅代码风 | 技术方案、开发者大会、系统架构、AI 工程实践 | 工程师、技术管理者、架构师、开发者社区 |
| `theme04` | 玻璃糖果风 | 年轻化品牌、消费产品、创意提案、社媒感内容 | 品牌团队、设计师、内容创作者、消费品团队 |
| `theme05` | 色谱图表风 | 数据报告、市场分析、KPI 复盘、行业研究 | 数据分析师、咨询顾问、研究员、业务负责人 |
| `theme06` | 深色图谱风 | 高密度数据展示、战略分析、科技/金融/产业报告 | 战略团队、投资人、产业研究团队、高管汇报者 |
| `theme07` | 冷白调研风 | 调研报告、白皮书、竞品分析、学术/政策型表达 | 研究机构、咨询团队、政府/高校/智库、B2B 团队 |
| `theme08` | 黑金实验风 | 高端发布、品牌提案、实验性概念、奢华科技叙事 | 高端品牌、创意总监、科技品牌、发布会策划团队 |
| `theme09` | 深蓝杂志风 | 品牌故事、人物访谈、企业形象册、深度专题 | 公关团队、媒体编辑、创始人、企业品牌部 |
| `theme10` | 金色指数风 | 金融数据、投资报告、商业指数、年度榜单 | 投资机构、金融分析师、咨询公司、商业媒体 |
| `theme11` | 高能增长风 | 增长复盘、商业计划、融资路演、市场扩张方案 | 创业者、增长团队、销售团队、VC/PE 路演团队 |
| `theme12` | 声波霓虹风 | 音乐娱乐、潮流活动、直播内容、年轻化发布 | 娱乐品牌、活动策划、内容团队、潮流消费品牌 |

用户没有明确指定风格时,先列出以上风格并询问。

默认风格选择回复只给极简适配提示:

- `theme01` 轻拟态风: 适合 产品介绍 / 企业汇报; 人群 创业团队 / 产品经理
- `theme02` 炫光紫绿风: 适合 科技发布会 / AI/自动驾驶/机器人主题; 人群 科技公司创始人 / 技术负责人
- `theme03` 深浅代码风: 适合 技术方案 / 开发者大会; 人群 工程师 / 技术管理者
- `theme04` 玻璃糖果风: 适合 年轻化品牌 / 消费产品; 人群 品牌团队 / 设计师
- `theme05` 色谱图表风: 适合 数据报告 / 市场分析; 人群 数据分析师 / 咨询顾问
- `theme06` 深色图谱风: 适合 高密度数据展示 / 战略分析; 人群 战略团队 / 投资人
- `theme07` 冷白调研风: 适合 调研报告 / 白皮书; 人群 研究机构 / 咨询团队
- `theme08` 黑金实验风: 适合 高端发布 / 品牌提案; 人群 高端品牌 / 创意总监
- `theme09` 深蓝杂志风: 适合 品牌故事 / 人物访谈; 人群 公关团队 / 媒体编辑
- `theme10` 金色指数风: 适合 金融数据 / 投资报告; 人群 投资机构 / 金融分析师
- `theme11` 高能增长风: 适合 增长复盘 / 商业计划; 人群 创业者 / 增长团队
- `theme12` 声波霓虹风: 适合 音乐娱乐 / 潮流活动; 人群 娱乐品牌 / 活动策划

## slide

新生成 deck 使用 `schemaVersion: 2`;每个逻辑页只保存一份 `content`,并包含 3 个 template variants 和 1 个无 layout 的 bespoke variant。旧 deck 的单 layout 和旧 3 候选仍可读取:

- `layout`: 直接指定页面 key,例如 `theme01_page001` 或 `theme12_page001`。
- template: `{id, kind:"template", layout, props, contentMap}`。
- bespoke: `{id:"v4", kind:"bespoke", adjustable:false, composition, contentMap}`,不写 `layout`、`props` 或 `controls`。
- `contentMap`: `{目标路径: content内源路径}`,源路径不加 `content.`。
- `role`: 只允许草稿阶段辅助选页,渲染前必须换成具体 `layout`。

每套主题的前 5 页都是封面候选。一个 deck 只能有 1 个逻辑封面页,它的 3 个模板方案都从前 5 页选择;正文模板方案从第 6 页以后选择。3N 个模板 layout 全局唯一。

选页先使用 `npm --prefix <skill-root>/project run layout:query -- --theme <themePack> --role <role> --limit 8 --seed <randomSeed>:slide-<n>`,为每个逻辑页选 3 个不同 template layout;相同 seed 和输入必须稳定,也不要固定只用未打散列表的前三条。v4 独立分析目标、受众、叙事作用、重点和主题特征,使用受限 `composition` 设计;不新增事实、不写自由 HTML/JSX、不微调模板,失败时仍输出安全 bespoke 组合。动态背景页用 `--role ambient`。需要图片槽时加 `--needs-media`、`--planned-images <n>`、`--provided-images <n>` 或 `--image-gen`。

长 deck 先按逐页语义 brief 为第 2 到倒数第 2 页确定正文 role,再用 `npm --prefix <skill-root>/project run goal:scaffold -- --title <title> --goal <goal> --theme <themePack> --pages <n> --roles <page2-role,...,pageN-1-role> --layout-variants 3 --seed <randomSeed> --chunk-size 5 --out output/<deck-name>/goal.json` 生成 schema v2 骨架和 `goal.fill-plan.json`;这里的 3 是模板数,scaffold 另追加 v4。输出目录写在当前会话工作目录,不要写入 `<skill-root>/project/output`。

单页契约优先使用 `npm --prefix <skill-root>/project run inspect:layout -- --compact <layout...>`,一次传多个 layout 或多次 `--layout`。`fillPlan` 给出标题/正文长度、可见数组数量、嵌套数组数量和媒体写入字段;`propShapes` 给出 `copy`、对象数组和嵌套数组的内部 key。写 `copy`、`cells`、`items`、`rows` 等对象字段时只使用 `fillPlan` / `propShapes` 列出的 key,不要凭字段名猜测。写数组、数量或图片时使用 `npm --prefix <skill-root>/project run props:safe -- <layout> '<props-json>' [--images <path...>]`;写完整 `goal.json` 后使用 `npm --prefix <skill-root>/project run props:safe -- --goal <goal-json> --write` 做整份 props 规范化。

图片/视频只写 `mediaSlots[].canPresetMedia: true` 的槽,按该槽 `presetProp` / `fieldPath` 写 deck 内相对路径。不要写 `slides[].media` 或不可 preset 的媒体槽;用户提供本地素材时先运行 `npm --prefix <skill-root>/project run media:stage -- <deck-output-dir-or-ppt-dir> <media-file...>`,再把返回的 `relative` 路径写入真实 media slot。同一逻辑页的 4 个方案共用同一素材,不同逻辑页之间每个素材最多使用一次。用户明确要求原创视觉图/生图时用 image-gen;未明确生图时先询问用户。需要 image-gen 生成 2 张以上独立图片时,用多个 subagent 并行,不要串行逐张等待;每张图独立生成,不要用一张拼图/素材板再拆分。subagent 只用于生图。用户只计划后续插图时选择并保留带 media slot 的页面。

`variantOutputMode:"comparison"` 默认按逻辑页顺序展开 4N 个物理页;`"selected-only"` 只输出每组标记的方案,共 N 页。v4 继承当前主题且无模板属性控件,但仍可选择、保存和导出。

需要调整卡片/条目数量时,用 `cardCount`、`itemCount`、`stepCount` 等 count 参数控制显示数量。数组字段是模板内容池;只覆盖当前显示的前 N 项。被 count/显隐控制隐藏的尾项可保留“请输入文本”占位。

不要使用旧的 `theme`、`fontSet`、`fontWeight`、`typeScale`、`styleVariant`、token 或开发者模式字段。
