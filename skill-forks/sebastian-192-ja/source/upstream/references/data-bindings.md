# 数值、正文与讲稿的联动更新

在修改表格/图表数据，或核对其依赖文字时读取。`data-bindings.json` 是可选的独立契约，不改变旧 Page Spec/Scene 的格式。

## 先声明，再预览

契约声明 `documents`（相对路径的 `page_spec`、`scene`）、`inputs`、`formulas` 和 `bindings`。每个输入有数值、单位及来源；公式只允许数字、命名依赖、括号与加减乘除，拒绝函数调用、属性访问、循环、除零和非有限结果。脚本不使用 `eval`。

绑定使用现有叶节点的 JSON Pointer，并选择 `value`（数值名称）或 `template`（文本模板）。例如 `{share:.1f}%`。模板只允许简单数值格式，不允许访问属性、索引或嵌套格式。

完整两页合成交通示例见 `examples/data-update/`。所有数值均为演示数据，不是实际交通观测或效果结论。

```sh
python scripts/update_data_bindings.py examples/data-update/data-bindings.json --check
python scripts/update_data_bindings.py examples/data-update/data-bindings.json --set '{"north_after":110}'
python scripts/update_data_bindings.py examples/data-update/data-bindings.json --set '{"north_after":110}' --output-dir work/traffic-update-draft
```

预览不会写入文件。把 North 的 After 值从90改为110，会把总量190改为210、占比47.4%改为52.4%、总变化-5.0%改为5.0%，并同步两页的图表值、正文和讲稿。`affected_slides` 与逐项前后差异用于定位复查。

当前文档必须与契约的原值一致；存在旧百分比、旧讲稿或重复绑定时先解决冲突，不能用下一次修改掩盖旧问题。两个文档的页序/ID须一致。绑定只能修改声明的文字/数据叶节点，不能修改图片路径、几何、批准状态或元素 ID。

## 独立草稿与恢复

输出目录必须不存在。脚本复制引用素材、写入新文档/契约/更新计划，再整体发布目录；原文件不变，不复制旧评分卡与质量结论。预览后原契约或文档改变时拒绝导出。

可见内容改变时，新 Page Spec 的 `content_approved` 设为 `false`，受影响页的 `image_status` 设为 `pending`；它是待审草稿，生产校验会拒绝。只改讲稿时保留已有图片状态，但仍需重建导出和备注核对。这里的 `pending` 表示旧图片尚未核对，按实际交付范围恢复时：

1. 核对来源、单位、统计范围及所有依赖项；按当前任务授权完成受影响内容自检。已有明确修改授权不重复请求。
2. 提升内容版本、记录授权并恢复内容批准。只更新可编辑版时把旧图片标记为 `revision`；需要最新图片版时重新生成/渲染并验收受影响页。
3. 重编 Scene、核对实际图表工作簿、查看修改页，并生成新的渲染/观察/审阅记录。
4. 交付评分时显式传入 `--data-bindings`；契约指定的文档必须就是本次评分使用的文档。任何声明的绑定不一致都会使评分失败，评分卡保留契约与文档哈希。

```sh
python scripts/evaluate_delivery.py work/page-spec.json work/render/render-report.json work/visual-review.json --observations work/content-observations.json --scene work/scene.json --data-bindings work/data-bindings.json --output work/scorecard.json
```

## 边界

脚本只联动已声明的依赖，不能自动发现所有论述、证明来源真实或推断修改后的结论是否成立。输入的来源字段不是自动核验结果；不能把合成演练的新数值标成原报告事实。仍须检查排名变化、定性结论、跨页说明与讲稿。当前只支持字面量图表数据及简单算术，不支持外部 Excel 公式计算、统计推断或单位自动换算。

`--data-bindings` 是显式的交付检查选项；未提供时不会声称做了依赖检查。现有冻结基准批次仍按原契约执行，不自动追加这个新证据项或改写历史结果。
