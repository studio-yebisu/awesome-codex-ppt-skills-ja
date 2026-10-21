# create-from-one-word

## 用户输入

AI 教育

## 需求检查结果

- 已有：主题为 AI 教育
- 缺失：受众、页数、使用场景、输出格式、风格、可编辑性
- 绝对必需项已满足：有主题

## 是否需要反问

需要，除非用户补充“你看着办”。最多问 3 个问题：

1. 这套 PPT 给谁看？
2. 大概需要多少页？
3. 更偏教学课件、正式汇报，还是科技培训？

## 风格推断

候选：

- `workshop-training`：适合老师培训或课堂讲解
- `tech-system`：适合 AI 技术和系统介绍
- `executive-clean`：适合管理层汇报

## route 选择

默认 `native_pptx`，因为用户没有模板且通常需要可编辑 PPTX。

## 应生成 artifacts

- `requirement_check.md`
- `route_decision.md`
- `content_plan.md`
- `design_spec.md`
- `spec_lock.json`
- `slides_plan.json`
- `asset_plan.json`
- `qa_report.md`
- `delivery_manifest.json`

## 生图规划

- 封面主视觉：AI + 教育场景
- 关键插图：教学流程图或课堂应用场景
- 每页仍要逐页判断，不因已有两张图而跳过必需视觉

## QA 重点

- 是否有占位符残留
- 是否每页有 content_budget
- 是否生成必需视觉或记录失败

## 预期行为

先做需求检查并追问关键缺口。用户说“随便”后进入 Auto Mode，生成 8-12 页 PPTX + PDF + PNG。
