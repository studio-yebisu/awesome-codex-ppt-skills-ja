# reference-style-and-structure

## 用户输入

参考这个 PPT，主题换成“城市更新趋势”，你看着办。

## 需求检查结果

- 已有：参考 PPT、新主题、Auto Mode 触发
- 参考范围未明确，但用户说你看着办

## 是否需要反问

不反问。默认参考风格 + 结构，内容根据新主题重写。

## 风格推断

从参考 PPT 提取视觉系统，同时判断城市更新适合新闻专题、政策解读或商业分析语气。

## route 选择

优先 `template_pptx`，如果参考 PPT 的 layouts/placeholders 可用；否则 `native_pptx`。

## 应生成 artifacts

- `reference_analysis.md`
- `reference_style_profile.json`
- `reference_structure_profile.json`
- `template_profile.md/json` 如适用

## 生图规划

- 封面城市更新主视觉
- 城市问题、改造前后、政策/社区场景按页判断

## QA 重点

- 是否记录默认参考 style + structure
- 是否说明不复制原内容
- 是否保留可编辑性

## 预期行为

直接进入 Auto Mode，不继续追问。
