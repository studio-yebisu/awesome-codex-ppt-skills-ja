# Style Inference Checklist

## 测试目的

验证 skill 不使用固定默认风格，而是根据主题、行业、场景、受众、语气、参考材料和关键词推断 1-3 个候选风格。

## 输入案例

> 做一份 12 页关于“医院智慧后勤管理”的 PPT，给院领导汇报。

## 必须生成的 artifacts

- `requirement_check.md`
- `route_decision.md`
- `design_spec.md`
- `spec_lock.json`
- `slides_plan.json`
- `asset_plan.json`
- `qa_report.md`

## 通过条件

- 至少给出 1 个、最多 3 个候选风格。
- 每个候选风格说明推荐理由。
- 推荐理由引用主题、受众、行业或使用场景。
- 用户未确认时问一次；用户说随便时自动选择。
- `design_spec.md` 和 `spec_lock.json` 反映最终风格。

## 失败条件

- 直接套固定默认风格。
- 候选风格与场景无关。
- 向用户抛出过多风格选项。
- 用户说随便后继续追问。

## 人工验收步骤

1. 查看 `requirement_check.md` 是否识别受众和场景。
2. 查看 `design_spec.md` 是否写明候选风格和理由。
3. 查看 `spec_lock.json` 是否锁定最终风格。
4. 查看用户沟通是否是普通中文而非内部术语。
