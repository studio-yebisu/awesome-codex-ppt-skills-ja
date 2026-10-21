# Reference Scope Checklist

## 测试目的

验证用户提供参考 PPT 时，skill 会明确参考范围：只参考风格、只参考结构、风格和结构都参考，或内容改写。

## 输入案例

> 参考这个 PPT，主题换成城市更新趋势，你看着办。

## 必须生成的 artifacts

- `requirement_check.md`
- `route_decision.md`
- `reference_analysis.md`
- `reference_style_profile.json`
- `reference_structure_profile.json`
- `content_plan.md`
- `slides_plan.json`
- `qa_report.md`
- `delivery_manifest.json`

## 通过条件

- 用户未明确范围但触发 Auto Mode 时，默认 style + structure。
- `reference_analysis.md` 明确说明参考了什么、没有参考什么。
- 不直接照搬原 PPT 内容。
- 如果复用模板，说明是否保留 placeholder/layout。
- QA 检查 reference scope 是否已说明。

## 失败条件

- 未确认或记录参考范围。
- 偷偷复制原内容。
- 用户只要求风格时却照搬结构。
- 用户只要求结构时却照搬视觉风格。

## 人工验收步骤

1. 查看 `reference_analysis.md` 的参考范围说明。
2. 对比新 deck plan 与参考 PPT 内容是否混淆。
3. 查看 `delivery_manifest.json` 是否记录 reference mode。
4. 查看 QA 是否检查参考范围。
