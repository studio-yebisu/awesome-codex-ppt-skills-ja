# Asset Plan No-Lazy Checklist

## 测试目的

验证 skill 在新建 PPT 时会逐页判断视觉资产需求，不会因为已经满足“封面 + 1-2 张关键插图”的最低要求，就跳过后面真正需要概念图、流程图、架构图或场景图的页面。

## 输入案例

来自 `examples/asset-plan-no-lazy.md`：

> 做一套 10 页“AI Agent 在企业落地”的 PPT，其中流程、架构、场景都要讲清楚。

约束：

- planning-only
- 不生成真实 PPT
- 不调用图片 API
- 不安装依赖
- 假设 10 页
- 至少 5 页需要视觉资产
- 至少 4 页 `generation_required=true`

## 必须生成的 artifacts

- `requirement_check.md`
- `route_decision.md`
- `content_plan.md`
- `design_spec.md`
- `spec_lock.json`
- `slides_plan.json`
- `asset_plan.json`
- `qa_report.md`
- `delivery_manifest.json`

## 通过条件

1. `asset_plan.json` 覆盖所有页面。
2. 每页都有 `visual_need`。
3. 所有 `visual_need=required` 的页面都有 `generation_required=true`，或明确说明采用截图、原生图表、原生流程图、用户素材替代。
4. 不能出现“已满足最低图片数量，所以不生成”的逻辑。
5. `qa_report.md` 检查了 required visual assets 是否完成。
6. `delivery_manifest.json` 记录 image generation status。
7. Required 页的 `reason` 具体说明为什么需要视觉资产。
8. Required 页必须有 `must_not_skip=true`。
9. Planning-only 状态必须明确说明图片未实际生成，而不是假装生成完成。
10. 核心标题、正文、关键数据和图表结论不能被规划为画死在图片里。

## 失败条件

1. 只生成封面 + 2 张图就停止。
2. 某页需要概念图却被标记 `not_needed`，且没有理由。
3. `generation_required=true` 但没有 `output_path`，也没有 failed reason 或 planning-only 说明。
4. 用 icon / 色块 / 空白框冒充 concept illustration。
5. 图片生成失败但 QA 仍然通过。
6. `asset_plan.json` 缺少任意页面。
7. 任意页面缺少 `visual_need`、`asset_type`、`generation_required`、`reason`、`must_not_skip` 或 `status`。
8. `delivery_manifest.json` 没有记录 planning-only 和 image generation status。

## 人工验收步骤

1. 打开 `ppt_runs/test_asset_plan_no_lazy/slides_plan.json`，确认有 10 页。
2. 打开 `asset_plan.json`，确认也有 10 页，并且 slide_id 与 slides_plan 对齐。
3. 统计 `visual_need=required / optional / not_needed` 数量。
4. 检查 required 页是否至少 5 页，且至少 4 页 `generation_required=true`。
5. 逐页阅读 `reason`，确认 required 判断不是套话。
6. 搜索 `最低`、`minimum`、`2 张`、`skip` 等词，确认没有“满足最低数量所以跳过”的逻辑。
7. 打开 `qa_report.md`，确认 QA 明确检查 no-lazy 规则。
8. 打开 `delivery_manifest.json`，确认本次是 planning-only，未生成真实图片或 PPT。
