# 交付评测：绑定实际产物的可复跑评分卡

在质量回归、版本发布或用户要求可审查的验收记录时使用。本流程评估**当前 PPTX 文件**，不是对提示词或模型能力打分。普通交付仍按 SKILL.md 逐页检查；不必为每个任务制作完整评分卡。

## 证据与门槛

已准备好的 Page Spec/Scene 可通过 [run_deck.py 流水线](pipeline.md)统一生成当前模板和待办，并在实际审阅后重新评分。流水线不会代填通过结论。

默认任务可在 [离线逐页审阅面板](review-panel.md) 对照实际画面填写，下载并导入当前绑定的记录，再运行原命令评分；导入不会自动填写通过结论或跳过检查分项。

| 维度 | 证据 | 通过条件 |
|---|---|---|
| 内容 | Page Spec、批准图片、逐页看图或 OCR 后人工校对的 `observations*.json` | 每页记录为 `complete`，已确认文字及 `required_visible_values` 均可见 |
| 数据 | `visual-review.json` 中逐个图表/表格的 `data_reviews` | 来源/数值、标签/单位，以及图表尺度/几何或表格行列对应分别通过；填写核对说明 |
| 数据视觉清单 | 每页 `data_visual_inventory` | 实际看到的图表/表格与 Page Spec 对应；无数据图的页面也检查是否多出无依据的曲线、坐标轴等 |
| 视觉 | 实际 PPTX 渲染的逐页 PNG、`review.png`、`visual-review.json` | 每页人工检查布局、画幅、裁切、字体、数字、主视觉和来源图差异，记录 `pass` 或 `fail` |
| 可编辑性 | 当前 PPTX、`scene.json` | 可编辑版传 `--scene`，结构审查没有错误，仍须按技能流程抽查实际编辑行为 |
| 讲稿（已声明时） | Page Spec/Scene `speaker_notes` 与实际 PPTX 备注 | 按页序保留原文；明确空备注不能残留。缺失/不一致会使评测失败，旧任务未声明显示 `not_declared` |
| 数值依赖（显式提供时） | `--data-bindings` 指定的契约及本次 Page Spec/Scene | 声明的原始数值、衍生算术、正文和讲稿均一致；保留契约和文档哈希，冲突使评分失败。未提供显示 `checked: false` |

`pass` 表示上述**已提供**证据均通过；没有 Scene 的图片版可通过且报告显示 `editability.checked: false`。可编辑版只有传入 `--scene` 才能称可编辑性已纳入评分。`fail` 表示发现内容、数据、视觉或结构错误；`incomplete` 表示缺少逐页内容观察、视觉复核或图表/表格数据核验。像素差异均值只帮助定位变化，不设自动通过阈值。若 PowerPoint 与 LibreOffice 渲染结果不同，记录所用后端并目视复查；不能混用不同后端的旧复核记录。

## 操作

先按 [Page Spec 内容核对](page-spec.md)为**每页**建立观察记录。`--init` 只生成模板，必须看图后填写 `observed_text` 并将 `status` 设为 `complete`。图表数据、单位和小字要在视觉复核中明确检查，不能因文字匹配而略过。

```sh
python scripts/render_deck.py output/editable.pptx output/review --page-spec work/page-spec.json
python scripts/evaluate_delivery.py work/page-spec.json output/review/render-report.json work/visual-review.json --init-review
```

打开 `output/review/review.png` 和每页渲染 PNG，对照批准图片逐页复核。填写 `visual-review.json` 中每页的 `status`（`pass`、`fail`、`pending`）及简短 `notes`。只有真正看过本次渲染结果，才能标为 `pass`。然后汇总；`--observations` 可重复传入，覆盖所有页面：

模板版本为 `1.2`，绑定 PPTX、Page Spec、参考图片、渲染 PNG 和所用后端。含图表/表格的页面自动生成 `data_reviews`，按 `element_id` 逐项记录 `status`、`notes` 和 `checks`。所有数据元素均有 `source_values`、`labels_units`；图表另有 `scale_geometry`，表格另有 `row_column_alignment`。各检查取 `pass`、`fail`、`pending`，不能只将总状态改成 `pass`。例如：

```json
{"element_id":"revenue","status":"pass","notes":"已对照 report/table-1 核对 12、15 万，类别标签对应，零轴及两根条长比例正确",
 "checks":{"source_values":"pass","labels_units":"pass","scale_geometry":"pass"}}
```

每页还要填写 `data_visual_inventory`：`observed_element_ids` 只记录实际看见并对应到 Page Spec 的数据元素 ID；额外数据图记录为新的可辨识 ID，状态 `fail` 并说明。无数据图页核对后记录空数组和说明。缺失/待检查保持 `pending`；声称清单通过但实际 ID 与规格不同会使评分失败。

总状态为 `pass` 时，任何检查缺失/待检查仍使整套 `incomplete`，任何子项失败使整套 `fail`。`pass`、`fail` 必须填写核对说明；来源和尺度核验仍是人工证据，脚本不会自动证明来源可靠或发现所有虚构图。[图表可靠性](chart-reliability.md)提供有限重试与支持图型的独立像素观察核对；可通过 `--chart-observations work/chart-observations.json` 把该核对纳入评分，其失败/缺失不能被手工总状态绕过。

```sh
python scripts/evaluate_delivery.py work/page-spec.json output/review/render-report.json work/visual-review.json \
  --observations work/observations-s01.json --observations work/observations-s02.json \
  --scene work/scene.json --output output/scorecard.json
```

图片版省略 `--scene`。输出报告保存 PPTX、Page Spec、参考图片、渲染报告、视觉复核、观察记录和可选 Scene 的 SHA-256，并保留逐元素的数据核验结果，方便回溯本次评分依据。命令仅在 `pass` 时返回 0；`fail` 或 `incomplete` 返回 1。PPTX、Page Spec、渲染 PNG 或批准图片变更后，重新渲染并重新复核；哈希不匹配会被拒绝。不要把旧评分卡沿用到新文件。

从 2.5.0 或更早版本升级后，旧渲染报告缺少参考图片哈希，旧 `1.0` 视觉复核也缺少必要绑定。保留旧证据用于历史追溯，使用新的输出目录重新渲染，再用 `--init-review` 创建新的复核文件并实际核验；不能只修改版本号或补写哈希沿用旧的 `pass`。

升级 2.8.0 后，旧 `1.1` 复核缺少几何分项与每页数据视觉清单，同样保留历史记录并创建新的 `1.2` 模板，实际复核新增项目。不能仅改版本号宣称通过新门槛；旧成品本身无需因此重新生图。
