# Contributing to Neon Slides

欢迎贡献!这个项目欢迎两类 PR:**新组件** 和 **新主题变体**。

## 提 issue

先搜一下有没有重复。提问题时尽量带:
- 你触发 skill 的原话(让我们看到 trigger 是怎么被匹配的)
- 生成的 HTML(或截图)
- 期望的效果

## 加新组件

1. 在 `template.html` 的 `<style>` 块里加 CSS,用已有的 `:root` 变量取色,**不要硬编码颜色**
2. 在 `template.html` 里新增一屏作为示例(方便 agent 后续生成时对照)
3. 在 `components.md` 加一节,写清楚:
   - 组件 HTML 片段(可以直接复制粘贴的那种)
   - 使用边界("什么时候该用"和"什么时候不该用")
   - 至少一个反例
4. 在 `SKILL.md` 的组件清单表格里加一行

## 加新主题变体

- 复制 `template.html` 到 `themes/<theme-name>.html`
- 只改 `:root` 里的 CSS 变量,不要动组件结构
- 在 README 的 "主题预览" 小节加个截图和链接

## 设计原则(不要违反)

1. **一屏一事** —— 新组件必须能单独撑起一屏,不是"另一个组件的装饰"
2. **二元主色** —— 只用 `--orange` 和 `--blue`,不要引入第三种强调色
3. **组件要有边界** —— 如果一个新组件的使用场景你自己都说不清,它就还没准备好
4. **别用 Inter** —— 也别用 Roboto、Arial、system-ui。我们有 Noto Sans SC + Space Grotesk 就够了

## 提 PR

- 一个 PR 一个组件/主题,别打包
- commit message 写清楚做了什么,中英文都行
- 有截图最好

谢谢 🙏
