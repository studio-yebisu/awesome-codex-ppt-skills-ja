# style-inference

## 用户输入

做一份 12 页关于“医院智慧后勤管理”的 PPT，给院领导汇报。

## 需求检查结果

- 已有：主题、页数、受众、场景
- 缺失：输出格式、可编辑性、是否需要讲稿
- 可默认：PPTX/PDF/PNG，可编辑

## 是否需要反问

只需问一次是否确认推荐风格；用户说随便则自动选择。

## 风格推断

候选：

- `executive-clean`：适合院领导汇报，结论清楚
- `data-room`：适合管理数据、效率指标、对比分析
- `tech-system`：适合智慧后勤系统架构

默认推荐 `executive-clean + data-room`。

## route 选择

`native_pptx`。

## 应生成 artifacts

- `design_spec.md`
- `spec_lock.json`
- `slides_plan.json`
- `asset_plan.json`

## 生图规划

- 封面医院后勤智慧化主视觉
- 系统架构图、流程图、数据看板按页判断

## QA 重点

- 是否先推断风格再确认
- 风格是否符合院领导场景

## 预期行为

不要固定默认风格，要解释推荐理由。
