# auto-mode

## 用户输入

帮我做一个关于个人知识管理的 PPT，你看着办，直接做。

## 需求检查结果

- 已有：主题
- Auto Mode 触发：你看着办、直接做
- 缺失项自动补全

## 是否需要反问

不反问。

## 风格推断

候选：

- `workshop-training`：适合方法论教学
- `editorial-ink`：适合知识管理、人文/写作气质
- `executive-clean`：适合职场方法汇报

自动选择最适合的组合。

## route 选择

`native_pptx`，默认 8-12 页，可编辑，输出 PPTX/PDF/PNG。

## 应生成 artifacts

- 全套新 deck artifacts
- `asset_plan.json` 强制

## 生图规划

- 封面主视觉
- 知识流转/笔记系统概念图
- 工具链或流程图按页判断

## QA 重点

- Auto Mode 假设是否写入
- 必需资产是否完成
- 默认交付物是否齐全

## 预期行为

直接执行，不继续追问。
