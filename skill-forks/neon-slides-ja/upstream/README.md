# Neon Slides

> 一个为技术内容创作者打造的 Claude Skill —— 用一句话生成深色科技风的 HTML 幻灯片,浏览器打开即用,投屏直播友好。

![style](https://img.shields.io/badge/style-neon%20dark-F97316)
![license](https://img.shields.io/badge/license-MIT-blue)
![claude](https://img.shields.io/badge/Claude-Skill-8A63D2)

https://github.com/user-attachments/assets/40b6f362-49bb-4986-a2e6-9cfab9af8269

## 这是什么

Neon Slides 是一个 [Claude Skill](https://www.anthropic.com/news/claude-skills),固化了一套**深色底 + 橙蓝霓虹对比色**的 slides 视觉语言。你只要把文章大纲、课程要点或直播 brief 丢给 Claude,并触发这个 skill,就能得到一份:

- **单文件 HTML** —— 双击用浏览器打开就能讲,不用装任何东西
- **键盘翻页** —— `←` `→` `Space` 翻页,`G` 跳转任意页,`Home` `End` 首末页
- **投屏就绪** —— 1920×1080 最佳,文字对齐、字号、留白都按讲台场景调过
- **语义化组件** —— 封面屏、章节过渡屏、半屏图文、对比卡、三栏架构卡、清单网格、代码块,每个都有明确使用边界

## 为什么不用 PPT

`python-pptx` 做不出描边发光、渐变标题、精细 icon box 这些效果;传统 PowerPoint 又太重,做一次改一次都很痛。Neon Slides 的定位是 **"能讲的 landing page"**——既有 landing 的设计质感,又有幻灯片的演讲能力。

适合:
- 技术直播课件(讲 AI agent、k8s、n8n 自动化、MCP 这类内容)
- 课程/训练营介绍页
- 产品架构解读、技术文章的 web 版
- 对外演讲的门面级 deck

不适合:
- 需要丢给同事编辑的 `.pptx`(选真 PowerPoint)
- 小红书封面、公众号单图(用 canvas 类工具)
- 白色商务报告风(这个 skill 就是深色 neon 美学,硬改会很违和)

## 预览

先看 `examples/template-demo.html` —— 4 屏示例,涵盖了封面屏、概念屏、架构屏、章节过渡屏四种典型组件。浏览器打开,按 `→` 翻页。

## 安装

### 方式一:Claude.ai 用户(推荐)

1. 下载 [Release](../../releases) 里的 `neon-slides.zip`(或直接克隆本仓库后打包)
2. 在 Claude.ai 进入 **Settings → Capabilities → Skills**
3. 点击 **Upload skill**,选中 zip 文件
4. 完成后就能在对话里触发了,试试说: "帮我用 neon slides 风格做一个 10 屏的直播课件,主题是 XXX"

### 方式二:Claude Code / API 用户

把整个 `neon-slides/` 目录放到 Claude 能访问的 skills 路径下。具体路径取决于你的运行环境,参考 [Claude Skills 文档](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)。

## 快速上手

触发 skill 之后,只要描述你想要的内容就行。例如:

```
用 neon slides 做一个 8 屏的课件,主题是 "n8n 如何对接飞书多维表格"
内容要点:
1. 为什么要对接
2. 整体架构
3. 三步配置
4. 常见坑
5. 一个完整案例
```

Claude 会自动:

- 规划屏数和每屏的组件类型
- 把纯内容改写成有金句和对比的"讲稿"
- 配好 tag、high-light 词、footer 金句
- 输出一个可直接用的 HTML 文件

## 组件清单

| 组件 | 用途 | 典型场景 |
|---|---|---|
| `.cover` | **首页封面**,居中大标题 + 橙色分隔线 | 第 1 屏 |
| `.hero` | **章节过渡屏**,超大描边编号 + 右侧标题 | PART 切换 |
| `.split` | 半屏图文,左文右图或反之 | 功能 + 截图 |
| `.steps` | STEP 流程卡,橙蓝交替 | 步骤/流程 |
| `.compare` | 左右对比卡 | 旧 vs 新 |
| `.layers` | 三栏 Layer 架构卡 | 系统分层 |
| `.list-grid` | 2 列清单网格 | 常见问题/漏洞清单 |
| `.code` | 橙色边框代码块 + 语法高亮 | 代码讲解 |

每个组件都有明确的使用边界,不会出现"首页被做成章节过渡"这种风格错乱。详细用法见 [`components.md`](./skill/components.md)。

## 设计哲学

1. **一屏一事** —— 信息密度靠组件,不靠往一屏塞东西
2. **金句驱动** —— 副标题、footer 都放能单独发朋友圈的话,不是功能描述
3. **橙蓝二元** —— 只有两个强调色,橙主蓝辅,绝不加第三色
4. **真实字体** —— Noto Sans SC + Space Grotesk,永不用 Inter/Roboto/Arial
5. **组件边界** —— 每个组件有自己的场景,滥用会被 SKILL.md 里的规则挡住

## 键盘快捷键

| 按键 | 作用 |
|---|---|
| `←` / `→` / `Space` | 上一页 / 下一页 |
| `Home` / `End` | 首页 / 末页 |
| `G` | 呼出跳转面板 |
| `Esc` | 关闭跳转面板 |
| 点击圆点 / 进度条 | 跳到对应位置 |

≤15 页用圆点,>15 页自动切换成进度条。

## 自定义

所有设计 token 都在 `template.html` 的 `:root` CSS 变量里:

```css
:root{
  --bg:#0A0A0A;
  --fg:#EDEDED;
  --orange:#F97316;
  --blue:#3B82F6;
  /* ... */
}
```

如果你想做自己的品牌色变体,复制 `template.html`,改 CSS 变量就行——所有组件都是用变量取色的。

## Roadmap

- [ ] 浅色变体 `neon-slides-light`
- [ ] 导出 PDF 按钮
- [ ] 更多预设主题(sunset / cyberpunk / forest)
- [ ] 演讲者备注模式(按 `S` 切换)

欢迎 PR 和 issue。

## 致谢 & 故事

这个 skill 是 [林月半子](https://mp.weixin.qq.com/s/ImHfehcRBoxMStXmSyE3Vw) 在 OpenClaw 社区做技术直播时迭代出来的——最初是为了一场 OpenClaw 安全加固直播,嫌 PPT 做起来又慢又丑,索性让 Claude 按固定的视觉规则生成 HTML。跑了几版之后发现这套风格通用性很强,就封装成 skill 开源出来。

视觉风格参考了 blocmates、Linear、Vercel 的 landing page 设计语言。

## License

MIT. 随便用、随便改、随便商用,保留版权声明即可。

---

**如果这个 skill 帮你节省了做课件的时间,欢迎给个 Star ⭐**
