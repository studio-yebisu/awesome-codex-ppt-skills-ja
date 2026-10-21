# Single Slide Lock Checklist

## 测试目的

验证用户指定只修改第 N 页时，skill 会锁定其他页面，不改变非目标页内容、版式、顺序、字体、颜色、图片或图表。

## 输入案例

> 只改第 7 页，其他页不要动。

## 必须生成的 artifacts

- `requirement_check.md`
- `route_decision.md`
- `single_slide_edit_plan.md`
- `locked_slides.json`
- `preview_before/slide_07.png`
- `preview_after/slide_07.png`
- `change_log.md`
- `qa_report.md`
- `delivery_manifest.json`

## 通过条件

- `route_decision.md` 选择 `single_slide_edit`。
- `locked_slides.json` 明确锁定所有非目标页。
- `single_slide_edit_plan.md` 只描述第 7 页修改。
- 修改页继承原 PPT 的颜色、字体、标题层级、密度、页眉页脚、图标风格和图片风格。
- QA 检查非目标页是否被误改。

## 失败条件

- 修改了第 7 页以外的页面。
- 改变了非目标页顺序、布局或样式。
- 未生成锁定清单。
- 默认生成多个版本，但用户没有要求。

## 人工验收步骤

1. 查看 `locked_slides.json` 是否列出非目标页。
2. 查看 `change_log.md` 是否只包含第 7 页。
3. 对比 before/after 预览。
4. 查看 QA 是否包含非目标页变更检查。
