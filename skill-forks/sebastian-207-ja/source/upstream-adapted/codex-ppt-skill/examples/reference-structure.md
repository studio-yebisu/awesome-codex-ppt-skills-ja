# reference-structure

## 用户输入

参考这个 PPT 的结构，内容换成我们公司的年度培训方案。

## 需求检查结果

- 已有：参考 PPT、新主题、参考范围为结构
- 可能缺失：受众、页数是否沿用、输出格式

## 是否需要反问

可问是否沿用相同页数；如果用户说随便，默认沿用结构但根据内容调整页数。

## 风格推断

不要复制参考 PPT 的视觉风格，除非用户另说。根据年度培训方案推断 `workshop-training` 或 `executive-clean`。

## route 选择

`native_pptx` 或 `template_pptx`。如果用户只要结构，不一定复用模板。

## 应生成 artifacts

- `reference_analysis.md`
- `reference_structure_profile.json`
- `content_plan.md`
- `slides_plan.json`

## 生图规划

- 培训流程图、课程模块图、学习路径图按页判断

## QA 重点

- 是否明确“只参考结构”
- 是否没有误用参考 PPT 的视觉风格
- 新内容是否完整替换

## 预期行为

抽取章节和叙事逻辑，重写为培训方案内容。
