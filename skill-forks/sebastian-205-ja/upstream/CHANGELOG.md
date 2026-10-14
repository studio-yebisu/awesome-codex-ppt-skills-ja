# Changelog

本文件记录 Paper2PPT 的用户可见变化。格式参考 Keep a Changelog，版本遵循 Semantic Versioning。

## [0.1.0] - 2026-07-15

### Added

- 新增中文优先、英文等价的仓库文档与 Codex / Claude Code / Agent Skills 安装路径。
- 新增 evidence-first 论文转 PPTX 工作流、六类论文叙事路由、适应性幻灯片设计与三层质量门。
- 新增输入预检、PPTX 结构检查和仓库契约校验脚本。
- 新增 Codex 与 Claude Code 插件 manifest、marketplace 目录和 canonical Skill 同步检查。
- 新增基于 CC BY 4.0 开放获取论文的 9 页可编辑中文示例、speaker notes、素材清单、QA 报告和真实渲染预览。
- 新增 trigger fixtures、forward evaluation 记录，以及 Skill、脚本、插件、文档和示例的自动化测试。

### Changed

- 仓库、Skill ID、插件 ID 与公开产品身份统一更名为 `paper2ppt` / Paper2PPT，不保留兼容别名。
- 默认交付物统一为 `presentation_zh.pptx` 与 `qa_report.md`；只在提取素材时生成 `asset_manifest.md` 和 `assets/`。
- 默认视觉语言改为中性、自适应的学术呈现系统，不绑定期刊品牌。
- 默认面向 15-20 分钟、12-16 页简体中文学术汇报，同时允许用户覆盖语言、听众、时长和模板。

### Removed

- 移除独立模型运行时与 PyPI 发布路线；Paper2PPT 在现有 Agent 客户端内运行，不要求额外模型 API 密钥。
- 移除只输出大纲即可完成、未核验完整来源却声称全文分析、以及缺少 renderer 却声称 visual QA 通过的交付路径。

[0.1.0]: https://github.com/wp-a/paper2ppt/releases/tag/v0.1.0
