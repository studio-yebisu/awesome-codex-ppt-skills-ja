# asset-plan-no-lazy

## 用户输入

做一套 10 页“AI Agent 在企业落地”的 PPT，其中流程、架构、场景都要讲清楚。

## 需求检查结果

- 已有：主题、页数、内容重点
- 可推断：企业培训/汇报，结构型内容

## 是否需要反问

可问受众是老板、技术团队还是业务团队；用户说随便则 Auto Mode。

## 风格推断

候选：

- `tech-system`
- `executive-clean`
- `data-room`

## route 选择

`native_pptx`，核心文字、架构标签和数据保持可编辑。

## 应生成 artifacts

- `asset_plan.json` 是重点
- `slides_plan.json`
- `qa_report.md`
- `delivery_manifest.json`

## 生图规划

这套 10 页可能至少 5 页需要视觉资产：

- slide_01 cover hero: required
- slide_03 enterprise scenario illustration: required
- slide_04 agent workflow diagram: required
- slide_05 system architecture diagram: required
- slide_07 risk/control diagram: required

不能因为已经满足“封面 + 1-2 张关键插图”就跳过 slide_05 或 slide_07。

## QA 重点

- `asset_plan.json` 中 `generation_required=true` 的页面是否完成
- 失败原因是否写入 QA 和 delivery manifest
- 是否把核心文本画死进图片

## 预期行为

逐页判断视觉需求；最低数量不是上限。
