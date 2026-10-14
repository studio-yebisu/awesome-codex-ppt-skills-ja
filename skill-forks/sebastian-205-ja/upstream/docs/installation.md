# Paper2PPT 安装与迁移

Paper2PPT 同时提供直接 Skill 与插件两种安装方式。两者包含同一套 `SKILL.md`、`references/` 和 `scripts/`；插件另外携带客户端 manifest、版本和安装界面元数据。个人只需要一种方式，重复安装可能让客户端显示两个同名 Skill。

## 前置条件

- 已安装并登录 Codex 或 Claude Code；
- 已安装 Git；
- 能在目标目录创建文件；
- 仅在客户端没有合适的 PDF/PPTX 工具时，才需要 Python 3 与回退依赖。

Paper2PPT 不运行独立模型服务，也不要求另配模型 API key。客户端自身的账户、订阅、数据策略和工具权限仍然适用。

先获取仓库：

```bash
git clone https://github.com/wp-a/paper2ppt.git
cd paper2ppt
```

## 方案一：直接 Skill

直接 Skill 适合个人、单仓库和 Agent Skills 兼容客户端。必须复制 `plugins/paper2ppt/skills/paper2ppt/` 整个目录，因为运行时还需要 references 与 scripts。

### Codex 用户级

Codex 当前的用户级 Skill 目录是 `~/.agents/skills`：

```bash
mkdir -p ~/.agents/skills
cp -R plugins/paper2ppt/skills/paper2ppt ~/.agents/skills/
```

新建 Codex 任务并输入：

```text
使用 $paper2ppt 把这篇论文制作成 15 分钟中文组会 PPT。
```

若 `$paper2ppt` 没有出现在 Skill 选择器中，先确认 `~/.agents/skills/paper2ppt/SKILL.md` 存在，再重启 Codex。

### Codex 项目级

需要团队随仓库共享时，安装到目标仓库的 `.agents/skills`：

```bash
mkdir -p /path/to/project/.agents/skills
cp -R plugins/paper2ppt/skills/paper2ppt /path/to/project/.agents/skills/
```

Codex 会从当前目录向上扫描到仓库根目录的 `.agents/skills`。不要同时保留项目级和用户级同名副本，除非你确实需要比较两个版本。

### Claude Code 用户级

Claude Code 当前的用户级 Skill 目录是 `~/.claude/skills`：

```bash
mkdir -p ~/.claude/skills
cp -R plugins/paper2ppt/skills/paper2ppt ~/.claude/skills/
```

个人 Skill 可通过 `/paper2ppt` 调用，也可以用与 description 匹配的自然语言触发。若创建 Skill 顶层目录时 Claude Code 已经在运行，请重启一次；普通文件更新通常会被实时发现。

### Claude Code 项目级

```bash
mkdir -p /path/to/project/.claude/skills
cp -R plugins/paper2ppt/skills/paper2ppt /path/to/project/.claude/skills/
```

项目成员应在信任仓库前审查 Skill 内容与脚本。

### 通用 Agent Skills 客户端

Agent Skills 开放规范定义 `SKILL.md` 和资源目录的格式，但不定义一个跨客户端通用的发现路径。使用目标工具文档提供的目录：

```bash
cp -R plugins/paper2ppt/skills/paper2ppt <AGENT_SKILLS_DIR>/paper2ppt
```

最低验证项：客户端能发现名称 `paper2ppt`，能读取 references，并能从已加载的 Skill 目录执行 `scripts/preflight.py` 与 `scripts/inspect_pptx.py`，而不是从用户项目的当前目录查找同名脚本。如果客户端只支持单文件提示而不支持资源目录，它不能完整运行本 Skill。

## 方案二：插件

插件适合需要安装界面、版本元数据、命名空间或团队分发的场景。插件根目录是 `plugins/paper2ppt/`，不是仓库根目录。

### Codex 插件

添加仓库 marketplace：

```bash
codex plugin marketplace add wp-a/paper2ppt
codex plugin marketplace list
codex plugin add paper2ppt@personal
```

仓库 marketplace 的 manifest 名称是 `personal`，所以非交互安装选择器为 `paper2ppt@personal`。若本机已有同名 marketplace 或 manifest 后续改名，先用 `codex plugin marketplace list` 取得实际名称，再运行 `codex plugin add paper2ppt@<MARKETPLACE_NAME>`。

也可以启动 `codex` 后输入 `/plugins`，在对应 marketplace 中打开 Paper2PPT 并安装。IDE 扩展可在 Settings > Plugins 完成同一操作；桌面端在 Codex > Plugins 中安装。安装后新建任务，使用 `$paper2ppt` 或直接描述论文转 PPTX 的请求。

上述命令已用本地 Codex CLI 0.144.0 的 `codex plugin add --help` 核验；较旧版本若没有 `plugin add`，使用 `/plugins` 界面或先升级客户端。

### Claude Code marketplace 插件

Claude Code 提供完整的非交互命令：

```bash
claude plugin marketplace add wp-a/paper2ppt
claude plugin marketplace list
claude plugin install paper2ppt@paper2ppt
```

启动新的 Claude Code 会话，通过 `/paper2ppt:paper2ppt` 调用。插件 Skill 始终带 `plugin-name:skill-name` 命名空间。

### Claude Code 本地开发加载

从仓库根目录运行：

```bash
claude --plugin-dir ./plugins/paper2ppt
```

在会话内执行 `/paper2ppt:paper2ppt`。修改 manifest 或 Skill 后执行 `/reload-plugins`。`--plugin-dir` 是当前会话的开发加载方式，不等同于持久安装。

## 更新

先更新仓库并运行其校验：

```bash
git pull --ff-only
.venv/bin/python scripts/validate_repo.py
.venv/bin/python -m pytest -q
```

直接 Skill 安装建议先保留备份，再复制新目录：

```bash
mv ~/.agents/skills/paper2ppt ~/.agents/skills/paper2ppt.backup
cp -R plugins/paper2ppt/skills/paper2ppt ~/.agents/skills/
```

Claude Code 将上面的 `~/.agents/skills` 换成 `~/.claude/skills`。验证新版本后再删除备份。插件用户使用客户端 marketplace 的更新操作；Claude Code 可运行：

```bash
claude plugin marketplace update paper2ppt
claude plugin update paper2ppt@paper2ppt
```

若当前 Claude Code 版本不支持某个子命令，运行 `claude plugin --help`，或在 `/plugin` 的 Installed 页面更新。Codex 使用 `/plugins`，或先运行 `codex plugin marketplace upgrade` 刷新来源。

## 从旧版迁移

1. 保留旧安装作为临时备份，不创建兼容别名。
2. 按上文安装 `paper2ppt`。
3. 新建客户端会话，确认只调用 `paper2ppt` 并能读取 `references/` 与 `scripts/`。
4. 用一篇非敏感论文运行 preflight，确认默认输出名是 `presentation_zh.pptx`。
5. 验证通过后，归档或删除旧的品牌化 Skill 目录，确保 Skill 选择器中只剩一个当前名称。

迁移不会移动以往生成的 PPTX；已有输出仍是普通本地文件。

## 卸载

删除直接 Skill 前先核对路径：

```bash
rm -rf ~/.agents/skills/paper2ppt
rm -rf ~/.claude/skills/paper2ppt
```

Claude Code 插件：

```bash
claude plugin uninstall paper2ppt@paper2ppt
claude plugin marketplace remove paper2ppt
```

Codex 可通过命令或 `/plugins` / 桌面 Plugins 页面卸载：

```bash
codex plugin remove paper2ppt@personal
codex plugin marketplace remove <MARKETPLACE_NAME>
```

移除 marketplace 前先用 `codex plugin marketplace list` 取得实际名称；如果仍使用默认 manifest，它是 `personal`。

卸载 Skill 或插件不会删除你已生成的 `presentation_zh.pptx`、`qa_report.md`、`asset_manifest.md` 或 `assets/`。

## 安装后验证

无论使用哪种安装方式，都应确认：

1. 客户端只显示一个 `paper2ppt`；
2. 中文请求能触发 Skill，英文请求也能触发同一输出契约；
3. 默认交付物包括 `presentation_zh.pptx` 与 `qa_report.md`；
4. 只有实际提取素材时才出现 `asset_manifest.md` 与 `assets/`；
5. 没有 renderer 时，QA 报告明确标记 visual QA unavailable，而不是声称全部通过。

## 官方行为依据

- [Codex: Build skills](https://developers.openai.com/codex/build-skills) 记录 `.agents/skills` 发现路径与 `$skill` 调用方式。
- [Codex: Plugins](https://developers.openai.com/codex/plugins) 记录 `/plugins`、桌面端与 IDE 插件安装流程。
- [Claude Code: Skills](https://code.claude.com/docs/en/skills) 记录 `.claude/skills`、`/skill-name` 与实时发现行为。
- [Claude Code: Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) 记录 marketplace、安装、更新和卸载命令。

客户端行为会随版本变化。遇到差异时，以已安装客户端的 `--help` 和以上官方文档为准，并在 issue 中附上客户端版本与完整错误。
