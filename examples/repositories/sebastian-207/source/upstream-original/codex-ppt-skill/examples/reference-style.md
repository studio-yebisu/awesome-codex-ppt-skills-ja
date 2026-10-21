# reference-style

## 用户输入

参考这个 PPT 的风格，帮我做一份关于 AI 客服的产品介绍。

## 需求检查结果

- 已有：新主题、参考 PPT、参考范围为风格
- 需要确认：页数、输出格式、可编辑性

## 是否需要反问

不需要追问参考范围，因为用户明确只参考风格。可只问页数或直接按 Auto Mode 推断。

## 风格推断

从参考 PPT 提取颜色、字体、图文密度、布局节奏、图片处理方式，并与 AI 客服产品场景融合。

## route 选择

如果参考 PPT 是 PPTX 且用户要可编辑，优先 `template_pptx`；否则 `native_pptx`。

## 应生成 artifacts

- `reference_analysis.md`
- `reference_style_profile.json`
- `route_decision.md`
- `design_spec.md`
- `spec_lock.json`
- `slides_plan.json`

## 生图规划

- 封面主视觉要贴合 AI 客服
- 不复制参考 PPT 的具体业务内容

## QA 重点

- 是否明确“只参考风格”
- 是否未复制原内容
- 是否输出 reference scope

## 预期行为

告诉用户本次只参考视觉风格，不参考原页面结构和原内容。
