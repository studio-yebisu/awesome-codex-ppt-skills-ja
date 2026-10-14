# edit-existing-deck

## 用户输入

这份 PPT 内容不要大改，帮我变高级一点。

## 需求检查结果

- 已有：待处理 PPT、修改目标
- 约束：内容不要大改
- 需要推断：视觉升级、排版优化、字体配色、插图

## 是否需要反问

通常不需要。可以复述：不改变核心内容，只做视觉和表达优化。

## 风格推断

根据原 PPT 行业、受众和现有风格，推荐 1-3 个升级方向，例如 `executive-clean`、`data-room`、`tech-system`。

## route 选择

`edit_deck`。如果指定页码，转 `single_slide_edit`。

## 应生成 artifacts

- `change_plan.md`
- `change_log.md`
- before/after previews
- `qa_report.md`
- `delivery_manifest.json`

## 生图规划

如需新增视觉资产，写入 `asset_plan.json`，但不能替换或篡改原关键数据。

## QA 重点

- 核心意思是否保持
- 事实和数据是否保持
- 是否误改不该改的页面

## 预期行为

先写 change_plan，再执行修改。
