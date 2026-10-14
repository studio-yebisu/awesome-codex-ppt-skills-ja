# 内容架构 / Content Architecture

## 目录 / Contents

1. 文稿锁定 / Source lock
2. 原稿逻辑地图 / Source logic map
3. 分组提炼 / Grouping
4. 页面合同 / Slide contract
5. 中英双语 / Bilingual hierarchy
6. PPT 参考输出 / PPT reference output
7. 禁止事项 / Prohibitions

## 1. 文稿锁定 / Source lock

先确认文稿是否定稿，以及允许大调、微调还是近原文。文稿未锁定前，只做问题诊断，不做页级排版。

Confirm whether the source is final and whether major revision, light polish, or near-verbatim preservation is allowed. Before the source is locked, diagnose only; do not design slides.

把以下内容视为不可擅自改变的合同：

- 人名、地名、机构、专有名词；
- 日期、数量、比例与单位；
- 因果、转折、范围与限定词；
- 用户明确要求保留的原句；
- 已确认的章节与顺序。

Treat names, dates, numbers, causality, scope, fixed wording, and confirmed order as protected content.

## 2. 原稿逻辑地图 / Source logic map

用一张表记录原稿，不要直接从原文跳到视觉页面：

| 字段 / Field | 要求 / Requirement |
| --- | --- |
| Source ID / 原稿编号 | 给每个标题、段落或卡片稳定编号 |
| Subject / 对象 | 这一段主要谈谁、什么事或什么概念 |
| Claim / 判断 | 作者希望听众接受什么 |
| Evidence / 证据 | 数据、事实、案例、引文或逻辑支撑 |
| Relation / 关系 | 时间、因果、对照、递进、转折或并列 |
| Fixed copy / 固定文案 | 不能改写的文字 |
| Candidate role / 页面职责 | 封面、开场、论点、证据、过程、对照、总结等 |

Create this map before choosing layouts. Every source item must be retained, intentionally merged, or explicitly excluded with user approval.

## 3. 分组提炼 / Grouping

用户提供的一级分组优先。只有原稿没有清晰分组时才提炼候选结构。

Use the user's top-level grouping when provided. Derive candidates only when the source lacks clear sections.

从原文证据选择分组轴：

- 对象：不同人物、地区、产品或概念；
- 时间：过去、现在、未来，或明确阶段；
- 因果：背景、问题、原因、行动、结果；
- 对照：两种路径、前后变化、优势与限制；
- 论证：判断、证据、反证、结论；
- 空间：区域、尺度、场所或层级。

Possible grouping axes include subjects, chronology, causality, contrast, argument, and spatial scale.

输出一至两个候选方案。每个方案必须列出：

1. 章节名称；
2. 纳入的 Source ID；
3. 分组依据；
4. 主要优点与牺牲；
5. 推荐理由。

Ask the user to confirm the derived grouping before treating it as the navigation framework.

## 4. 页面合同 / Slide contract

每页先写合同，再做 HTML 或 PPT：

| 字段 / Field | 要求 / Requirement |
| --- | --- |
| Slide ID / 页码 | 连续且稳定 |
| Source IDs / 原稿来源 | 可追溯到原稿地图 |
| Section / 章节 | 决定导航高亮 |
| Role / 页面职责 | 一页只承担一个主要职责 |
| Key claim / 核心判断 | 一句话说明本页要让听众记住什么 |
| Chinese copy / 中文文案 | 完整承载信息 |
| English support / 英文辅助 | 更短、更小，不新增观点 |
| Evidence / 证据 | 对判断真正有支撑作用 |
| Layout / 版式 | 从 layout-patterns.md 选择 |
| Asset status / 素材状态 | 已提供、待补或不需要 |

One slide may reference multiple nearby source items, but the reason for merging must be clear.

## 5. 中英双语 / Bilingual hierarchy

中文是信息合同，英文是语义辅助。

Chinese is the content contract; English is semantic support.

- 完整翻译标题、关键判断、标签和主要内容块；
- 长段落只提炼英文摘要，不逐句等量复制；
- 保留名称、数字、顺序、因果和语气边界；
- 不用英文补充中文原稿没有的新观点；
- 中文字号和视觉重量必须明显高于英文。

Translate titles, key claims, labels, and major blocks. Summarize long paragraphs in English while preserving names, numbers, sequence, causality, and scope.

## 6. PPT 参考输出 / PPT reference output

PPT 模式至少交付：

1. 原稿逻辑地图；
2. 已确认章节；
3. 导航标签；
4. 逐页合同；
5. 每页版式、字号、颜色和素材说明；
6. 需要下游 PPT 工具完成的事项。

Do not imply that a .pptx file has been created when only the framework contract is complete.

## 7. 禁止事项 / Prohibitions

- 不套用与原文无关的起承转合、问题方案结果等固定分类；
- 不为了凑页数重复同一观点；
- 不发明数据、案例、人物或引文；
- 不把多条独立判断挤进一页；
- 不因英文版式需要而改写中文原意；
- 不把装饰性元素当成证据。

Never impose stock taxonomies, invent evidence, duplicate claims, overcrowd slides, alter Chinese meaning for English layout, or treat decoration as evidence.
