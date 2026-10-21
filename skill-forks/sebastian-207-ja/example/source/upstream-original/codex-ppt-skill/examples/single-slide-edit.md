# single-slide-edit

## 用户输入

只改第 7 页，其他页不要动。

## 需求检查结果

- 已有：待处理 PPT、目标页码、锁定要求
- 缺失：修改方向，除非上下文已有

## 是否需要反问

如果用户没有说明第 7 页要怎么改，需要问一个问题：第 7 页主要想解决内容表达、视觉排版，还是图表呈现？

## 风格推断

从整套 PPT 继承颜色、字体、标题层级、密度、页眉页脚、图标风格和图片风格。

## route 选择

`single_slide_edit`。

## 应生成 artifacts

- `locked_slides.json`
- `single_slide_edit_plan.md`
- `preview_before/slide_07.png`
- `preview_after/slide_07.png`
- `change_log.md`

## 生图规划

仅当第 7 页需要新增视觉资产时规划，不影响其他页。

## QA 重点

- 非目标页是否完全未变
- 第 7 页是否与全 deck 风格一致

## 预期行为

默认只给一个最优版本；用户要求多版本时再给 2-3 个候选。
