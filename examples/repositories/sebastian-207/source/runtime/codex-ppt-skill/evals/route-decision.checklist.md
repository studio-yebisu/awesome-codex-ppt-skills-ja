# Route Decision Checklist

## 测试目的

验证 skill 在执行前先选择合适路线，并解释为什么选这条路线、为什么不选其他路线、可编辑性预期和交付目标。

## 输入案例

> 帮我把这篇文章做成一份可编辑的 10 页 PPT，输出 PPTX 和 PDF。

## 必须生成的 artifacts

- `requirement_check.md`
- `route_decision.md`
- `content_plan.md`
- `slides_plan.json`
- `qa_report.md`
- `delivery_manifest.json`

## 通过条件

- `route_decision.md` 明确选择 `native_pptx` 或其他合理路线。
- 说明为什么未选 `image_first`、`html_slides`、`template_pptx`。
- 写明可编辑性预期。
- 写明是否需要生图。
- 写明 required artifacts、export targets、qa_profile。

## 失败条件

- 没有 route decision 就开始生成。
- 用户要求可编辑，却默认走 image-first。
- 没有解释未选路线。
- 没有写交付格式和 QA 范围。

## 人工验收步骤

1. 打开 `route_decision.md`。
2. 检查路线解释是否具体。
3. 检查 editability 和 export targets。
4. 检查 QA profile 是否覆盖页数、尺寸、placeholder、溢出、图片、导出。
