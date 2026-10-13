# qiaomu-bento-ppt 产品介绍 deck plan

## 目标与受众

- 受众：GitHub 首次访客、Agent Skills 用户、需要 AI 生成演示文稿的内容创作者。
- 场景：GitHub README 首屏证据、产品介绍、一分钟快速演示。
- 交付：7 个主页面 + 1 个隐藏 state，16:9，中文主叙事 + 英文微标签，完全离线。
- 受众需要相信：这不是“又一个写 bullet 的 PPT prompt”，而是一条能产出、验证和交付真实 bento deck 的独立工作流。

## 一句话结论

`qiaomu-bento-ppt` 把资料变成一份会动、可编辑、能验证、可离线分发的单文件 deck。

## 叙事弧

1. 打破惯性：AI PPT 不应是静态文字墙。
2. 给出结果：一个文件就是完整交付。
3. 解释路径：从 brief 到 plan、author、gate、deck。
4. 展示方法：内容映射到 chart / table / morph / state / motion。
5. 提供证据：14/14 路由、598 KB shell、0 项目依赖、远程安装通过。
6. 收束为交付：文件同时拥有 data / runtime / editor。
7. 行动：一行安装，用自然语言开始。

## 逐页计划

| # | 任务 | 核心信息 | 视觉所有者 | bento 能力 | notes 要点 | 来源 |
|---|---|---|---|---|---|---|
| 1 | 封面 | 不是静态文字页，是会动且会验证的 deck | 超大标题 + 浮动流程瓦片 | entrance + motion-path | 先给结论，不解释实现 | `README.md`, `SKILL.md` |
| 2 | 问题翻转 | AI PPT 的惯性是写满；成品应该直接工作 | 左侧文字墙 vs 右侧单文件 | morph | 强调用户要的是成品 | `README.md` |
| 3 | 工作流 | brief → plan → author → gate → deck | 横向节点与动态路径 | morph + dash-march | proposal-first 不是拖延，而是质量控制 | `SKILL.md` |
| 4 | 能力映射 | 内容类型决定表达方式 | 2×2 大型内容块 | native shapes + motion | 不把所有资料压成 bullet | `references/workflow.md` |
| 5 | 可验证证据 | 每一项公开声明都有本地或远程证据 | 大数字 + 真实验证表格 | countUp + table | 说清脚本验证与视觉验收的边界 | `reports/output-eval.json`, `reports/publication.md` |
| 6 | 单文件交付 | 文件就是 data + runtime + editor | 巨型文件卡 + 三层能力 | morph + link | 点击文件进入隐藏 state | `README.md`, bento 格式规范 |
| 6s | 隐藏详情 | 单文件内部的三层契约 | data / runtime / editor 展开视图 | stateOf + morph | 展示交互不打断主线 | bento 格式规范 |
| 7 | CTA | 一行安装，一句话触发 | 巨型安装命令 | zoom + entrance | 给出 GitHub 和自然语言示例 | `README.md`, `reports/publication.md` |

## 视觉方向

- 色彩：深墨黑 `#101115`、暖纸白 `#F3EEE5`、珊瑚橙 `#FF6B4A`、酸性黄绿 `#D9F06B`、电光蓝 `#5B7CFF`。
- 字体：系统 sans，中英文一致；靠字号、留白、整体色面和节奏建立层级。
- 不使用左侧彩色竖线、施工网格、出戏的玻璃卡片墙。
- README hero 截图：真实演示模式封面，16:9，文字在 GitHub 首屏缩放后仍可读。

## 素材清单

- 不使用外链图片或媒体；保持 deck 完全离线。
- 产品证据使用仓库内已验证数据，不伪造用户数、star 或业务指标。

## 风险与 missing evidence

- 生成后必须完成真实浏览器编辑态和演示态验收。
- README 截图只证明可见输出，不等于跨平台浏览器评测。
- 本 deck 不声称未经证实的人工评分、用户数或性能指标。
