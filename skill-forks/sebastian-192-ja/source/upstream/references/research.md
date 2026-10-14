# 方法调研与实现取舍

2026-10-08 的命令入口、环境诊断与贡献体验对标见[本轮优化记录](../docs/open-source-improvements-2026-10-08.md)，包含六个项目的一手来源、适用判断和验证边界。

核验日期：2026-09-15。以下是来源项目公开文档描述，不是本项目实测排名。
不使用随时变化的 Star 数或未经复现的相似度数字作为性能承诺。

## 2.9.0：Slidev 与 Marp 的讲稿/公式处理

再次核验：2026-10-01。查阅 [Slidev 导出](https://sli.dev/guide/exporting.html)、[逐页讲稿](https://sli.dev/guide/syntax.html#notes)、[LaTeX](https://sli.dev/features/latex)，及 [Marp Core Markdown](https://github.com/marp-team/marp-core/blob/main/docs/markdown.md)。

Slidev 将逐页讲稿保留到图片型及可编辑 PPTX；其导出文档也明确公式等复杂元素可能作为独立图片。Marp 使用数学排版插件并提供部分块的水平缩放，同时说明底部仍可能溢出。上述是官方文档能力，未在本项目环境中安装或做性能比较。

SlideMuse 本轮独立实现 `speaker_notes` 的图片/原生导出、实际备注核对、带来源的讲稿文件及讲稿变更时复用图片。论文审阅保留准确公式和可见解释，复杂公式允许独立栅格并如实说明编辑限制；不声称已支持 KaTeX、原生 Office 公式或通用自动排版。没有复制第三方源码或改变图片优先流程。

## PPT Master（重点参考）

项目：[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)，作者 Hugo He，MIT。
查阅：[Image to PPTX profile](https://github.com/hugohe3/ppt-master/blob/main/skills/ppt-master/workflows/profiles/image-to-pptx.md)、
[生成流程](https://github.com/hugohe3/ppt-master/blob/main/skills/ppt-master/workflows/generate-pptx.md)、
[技术设计](https://github.com/hugohe3/ppt-master/blob/main/docs/technical-design.md)。

值得借鉴的是将原生信息和独立图像层分别处理，并以结构化源文件生成 PPTX。
本项目吸收其同源坐标分层、背景清理、稳定命名和结果复查思路。
SlideMuse 选择更小的 JSON 场景协议，直接生成原生对象；未实现 PPT Master 的 SVG 编译体系、母版系统、动画或旁白。
不要求安装 PPT Master，也不自动运行其工具。

## banana-slides

项目：[Anionex/banana-slides](https://github.com/Anionex/banana-slides)。
查阅：[英文功能说明](https://github.com/Anionex/banana-slides/blob/main/README_EN.md)。

提供从大纲/页面描述生成图片演示、局部修改与可编辑导出的产品流程。
本项目保留图片视觉探索，再把可修改的信息提前规划成原生对象。
只借鉴流程，不引入 Web 服务、账号、异步任务队列或其图像后端。

## PPTAgent / DeepPresenter

项目：[icip-cas/PPTAgent](https://github.com/icip-cas/PPTAgent)。
查阅：[论文](https://arxiv.org/abs/2501.03936)。

关注参考演示分析、编辑式生成和内容/设计/连贯性的评估。
本项目将“生成后回看”落实为结构审查和实际渲染两条检查路径，不把 PPTX 能解压当成视觉通过。

## 图像重建的其他实践

[BrainChen/image2ppt](https://github.com/BrainChen/image2ppt) 展示布局识别、文字补充、结构描述与 PPTX 编译的分工。
[px-image2pptx](https://github.com/JadeLiu-tech/px-image2pptx) 展示 OCR 与背景修复后恢复文本的路线。
这些方法说明“文字可编辑”和“主体也独立”是不同验收目标。本版明确区分原生信息与独立栅格素材。

## 结论：本次实际实现

| 能力 | 2.0 实现 |
|---|---|
| 逐元素表达 | Scene v1：稳定 ID、像素框、层级、来源、置信度 |
| 原生编辑 | text / shape / line / group / table / chart |
| 分离图片 | 独立 PNG，已知框/遮罩裁剪工具 |
| 背景补全 | 宿主图像工具执行，技能提供分层与核验规范 |
| 图像识别 | 宿主视觉 Agent 执行；不捆绑自动 OCR/VLM 服务 |
| 修改迭代 | 修改 scene 或单一素材，再编译 |
| 检查 | 声明对象与实际 PPTX 对比，另做渲染核验 |
| 通用 SVG 编译 / 动画 / 母版还原 | 未实现 |

以上为独立实现与方法参考，没有复制第三方源码。
如未来直接引入第三方代码或资产，需要保留对应许可证与归属，并针对其版本验证兼容性。
