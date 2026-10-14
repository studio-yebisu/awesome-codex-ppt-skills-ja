# 开源对标优化记录 · 2026-10-08

本轮目标：阅读至少五个相关优秀开源项目的一手资料，实现三项上手、诊断或贡献体验改进；保持制作流程兼容，以回归、打包、隔离安装和实际使用验收，并形成可审阅提交。

基线为 SlideMuse 2.16.3，提交 `2e5da4073a5a816d02bd15ad4dd56f77e1bd23e5`。已有隔离安装、断点恢复、逐页检查与公开可复现样板；本轮从现有能力的入口和排障成本寻找改进机会。以下“适用判断”为本项目的取舍，不是上游项目的效果承诺。

## 对标依据与取舍

资料于 2026-10-08 查阅。只参考官方仓库或文档，不以星数判定适用性，不复制上游代码或资产。

| 项目与一手来源 | 已核对的做法 | SlideMuse 适用判断与落点 |
|---|---|---|
| [Marp CLI](https://github.com/marp-team/marp-cli#basic-usage) | 统一 CLI 承载转换，明确输出参数及浏览器前提 | 采用一个可发现的本地入口；继续使用现有 Python/PPTX 工具 |
| [Slidev CLI](https://sli.dev/builtin/cli) | build/export 等命令共用入口，逐项说明参数 | 使用 init/check/run/render 等命令；保留原工具帮助和工作目录 |
| [uv 工具环境](https://docs.astral.sh/uv/concepts/tools/) | 工具在独立虚拟环境运行，与项目环境分开 | 自动选择现有安装 `.venv`；这一轮无需新增包管理器 |
| [pipx](https://pipx.pypa.io/stable/) | 按应用隔离环境，文档区分命令、环境、退出码与 JSON 输出 | 明确实际解释器、诊断 JSON 和退出码；继续使用当前安装器 |
| [Homebrew doctor](https://docs.brew.sh/Manpage#doctor-dr---list-checks---audit-debug-diagnostic_check-) | 单独检查环境问题，提供诊断命令及失败退出码 | 提供缺依赖也能运行的只读诊断；可选要求发现渲染器 |
| [Ruff 问题表单](https://github.com/astral-sh/ruff/blob/main/.github/ISSUE_TEMPLATE/1_bug_report.yaml) | 收集最小复现、实际命令、配置和版本 | 提供中英 Bug/功能表单与 PR 模板，减少复现信息缺失 |

## 实际实现

1. **统一入口**：根目录 `slidemuse.py` 提供九个常用命令和版本/帮助。复用原工具；任务路径、交互输出和退出码保持原行为。根据当前位置选择隔离 Python，覆盖路径含空格和搬移安装目录的情形。
2. **独立诊断**：`doctor` 只依赖标准库，检查 Python、最低依赖版本、实际导入和共享后端发现。每包导入最多 15 秒；默认缺渲染器为警告，指定 `--require-renderer` 才阻塞。修复命令只作为建议显示。
3. **贡献入口**：增加 Bug/功能表单、PR 模板，并更新贡献说明。故障报告要求环境、阶段、最短步骤、预期/实际结果；使用咨询继续进入 Discussions。

新增中英文 [CLI 指南](cli.md) / [English guide](cli.en.md)，更新 README、Skill 入口和安装/打包清单。安装版同时包含现有文档、README 和许可证。原脚本与内容/风格/视觉审阅契约继续适用；候选版本为 2.17.0。

## 验收记录

证据放在本地 `work/opensource-20261008/`。当前改动位于独立功能分支，公开版本尚未更新。

| 验证 | 结果与证据 |
|---|---|
| 代码检查 | `python -m ruff check .` 通过 |
| 完整回归 | 444 项测试通过，486.57 秒；`full-tests.log` |
| 最终打包/安装复查 | 版本和文档清单调整后，14 项安装、发布包与品牌检查通过；`final-package-tests.log`；隔离升级至候选 2.17.0 成功，`isolated-upgrade.log` |
| 缺依赖与命令兼容 | 新增 26 项回归，覆盖无依赖帮助/诊断、导入损坏/超时、最低版本、后端选择、参数/cwd/退出码、只读预检、安装搬移 |
| 打包 | 发布清单包含 158 个文件；回归从 manifest 生成 ZIP、解压、安装后调用新入口，重建六套样板 |
| 真实隔离安装 | Windows Python 3.14 下新建独立环境，安装成功；新入口的诊断和严格规格验证通过，实际使用的解释器位于安装 `.venv`；`isolated-install.log` / `installed-doctor.json` |
| 已安装样板重建 | 六套共 36 页 PPTX 编译、对象和讲稿检查通过；`installed-sample/reproduction.json` |
| 当前对象审查 | 新入口审查原生样板，错误和警告均为零；`installed-object-audit.json` |
| 实际 PowerPoint 渲染 | 安装后的新入口导出六页 1600×900 PNG；原版和重建版在同一环境渲染逐像素一致，已查看对照总览；`installed-render/` / `same-environment-comparison.json` |

历史 WebP 预览与当前 PNG 的像素不完全相等，本轮因此额外重渲染原版做同环境比较；逐像素一致结论只针对这两次同环境 PNG。完整回归之后只调整版本与文档安装清单，这些调整另行复查打包/安装。远端 CI 与发布属于独立证据，不把本地通过称为正式发布。

## 边界与后续建议

- 环境发现只检查路径与注册，不能证明 PowerPoint/LibreOffice 真能导出，也不能代替逐页看图。
- 诊断不检测宿主的读材料、视觉、生图权限。未测量新用户完成时间或减少的支持工单，不声明效率提升百分比。
- 当前依赖契约为数字最低版本；未支持的约束和不确定的预发布版本显式失败。未来扩展依赖格式时一起更新解析与测试。
- 下一轮可从真实用户报告选择最常见的失败路径，测量首次成功交付、失败分类和复现信息完整性；再评估交互任务向导或更广泛的格式支持。

## English summary

Six official projects informed three focused changes: a unified entry point with local isolated Python selection, dependency-free runtime diagnosis, and structured contribution templates. Existing tools, task paths and pipeline exit codes remain intact. No upstream code/assets or new runtime dependencies were introduced. Renderer discovery does not establish successful rendering, host capability or visual acceptance. User onboarding time and support-ticket effects have not been measured.
