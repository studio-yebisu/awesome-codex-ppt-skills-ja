# Paper2PPT 维护指南

根目录 `SKILL.md`、`references/` 和运行时 `scripts/` 是规范源。`plugins/paper2ppt/skills/paper2ppt/` 是生成的客户端分发副本；不要只手改副本。

## 本地环境

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
```

所有维护命令均从仓库根目录运行。CI 不调用模型 API，也不依赖本机渲染器。

## 修改 Skill

1. 先在 `tests/` 或 `tests/trigger_cases.json` 添加会失败的契约或行为测试。
2. 修改根目录 `SKILL.md`、`references/` 或 `scripts/`。
3. 同步插件副本：

```bash
python scripts/sync_plugin.py
python scripts/sync_plugin.py --check
```

4. 运行聚焦测试，再运行全套校验。

`--check` 只报告 drift，不修改文件；发布前必须返回 0。

## 校验与测试

最小本地门禁：

```bash
python scripts/sync_plugin.py --check
python scripts/validate_repo.py
python -m pytest -q
python scripts/inspect_pptx.py examples/output/paper2ppt-example-zh.pptx --require-notes
```

`validate_repo.py` 校验 Skill frontmatter、引用、客户端 manifest、marketplace、版本、插件镜像、遗留标识和文档策略。`inspect_pptx.py` 只证明 PPTX 的包结构、关系、素材、讲稿和明显边界合理；它不能替代 content QA 或 visual QA。

GitHub Actions 在 push 与 pull request 上用 Python 3.10 和 3.12 运行仓库校验与 pytest。官方 `skills-ref` 要求 Python 3.11+，因此 Skill reference validation 只在 3.12 job 运行。需要在本地复现完整 CI 时，另建 Python 3.11+ 临时虚拟环境：

```bash
python3 -m venv /tmp/paper2ppt-ci
/tmp/paper2ppt-ci/bin/pip install -r requirements-dev.txt
/tmp/paper2ppt-ci/bin/pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
/tmp/paper2ppt-ci/bin/python scripts/sync_plugin.py --check
/tmp/paper2ppt-ci/bin/python scripts/validate_repo.py
mkdir -p /tmp/paper2ppt-ci-root
ln -s "$PWD" /tmp/paper2ppt-ci-root/paper2ppt
/tmp/paper2ppt-ci/bin/skills-ref validate /tmp/paper2ppt-ci-root/paper2ppt
/tmp/paper2ppt-ci/bin/skills-ref validate plugins/paper2ppt/skills/paper2ppt
/tmp/paper2ppt-ci/bin/pytest -q
```

CI 不调用模型 API，也不安装 LibreOffice、Poppler 等渲染器。示例视觉 QA 仍按“刷新真实示例”中的本地流程执行。

根 Skill 通过名为 `paper2ppt` 的临时符号链接传给 `skills-ref`。这避开 0.1.0 对字面量 `.` 的空目录名解析，也不依赖 checkout 目录是否已随 GitHub 仓库改名，同时保留 Skill 名称与目录名一致性检查。

修改 trigger description 或执行规则后，还要运行 `docs/evaluation.md` 中的人工 forward evaluation。不要把带预期答案的 primed probe 当成盲测结果。

## 刷新真实示例

示例不是截图占位符，而是一次完整 Paper2PPT 运行的可复核产物。刷新时：

1. 选择许可允许再分发的开放获取论文；在 `examples/source/paper-metadata.json` 与 `examples/source/README.md` 记录 DOI、文章 URL、全文 URL、许可 URL、获取日期和图像署名。
2. 使用当前 canonical Skill 从全文制作 8-10 页简体中文可编辑 PPTX；不得复用无法追溯的旧数字或图片。
3. 更新 `examples/output/paper2ppt-example-zh.pptx`。每页写 meaningful speaker notes，所有结果页保留可见来源标签。
4. 更新 `asset_manifest.md`，只列实际嵌入素材，并记录 URL、source anchor、figure/panel、crop、destination、license 与 SHA-256。
5. 更新 `qa_report.md`，分别记录 source sufficiency、content QA、structural QA、visual QA、未解决项与 completion state。
6. 用可用的 LibreOffice/PowerPoint renderer 导出全部页面，并逐页检查；用图像工具生成 `overview.png` 和三个有代表性的 `slide-*.png`。仓库只提交这四张 showcase 图片，不提交临时渲染目录。
7. 运行：

```bash
python scripts/inspect_pptx.py examples/output/paper2ppt-example-zh.pptx --require-notes
python -m pytest tests/test_example.py -v
```

如果没有 renderer，不得把新示例标记为 visual QA pass；正式 showcase 更新应等待可完成全页视觉复核的环境。

## 版本更新

发布版本以根目录 `VERSION` 为准。更新同一版本号到：

- `VERSION`；
- `plugins/paper2ppt/.codex-plugin/plugin.json`；
- `plugins/paper2ppt/.claude-plugin/plugin.json`；
- `.claude-plugin/marketplace.json` 中的插件条目；
- `README.md` 与 `README.en.md` 的版本 badge；
- `CHANGELOG.md`。

用以下命令检查遗漏：

```bash
rg -n '"version"|version-' VERSION README.md README.en.md .claude-plugin plugins
python scripts/validate_repo.py
```

保持 SemVer。只有文档更正且不改变已发布行为时才使用 patch；输出契约或行为的兼容新增使用 minor；不兼容更改使用 major，并在 CHANGELOG 中给出迁移说明。

## CHANGELOG

采用 Keep a Changelog 风格：最新版本在上，按 Added、Changed、Fixed、Removed 等类别记录用户可见变化。不要把测试内部重构写成产品功能，也不要把已移除的名称继续当成当前标识。

每个 release 条目至少说明：

- Skill 或输出契约变化；
- Codex / Claude Code packaging 变化；
- 脚本、QA 或示例变化；
- 迁移或已知限制。

## Release 清单

1. 工作区干净，目标提交已合入 `main`。
2. `VERSION`、两个插件 manifest、marketplace、README badge 和 CHANGELOG 一致。
3. 运行全部本地门禁，记录 pytest 数量与示例 inspector 结果。
4. 在实际 Codex 与 Claude Code 客户端各做一次发现/触发验证。
5. 检查示例 PPTX 可下载、showcase 路径有效、许可与归属完整。
6. 创建签名或普通 tag，并发布 GitHub Release：

```bash
git tag v0.1.0
git push origin v0.1.0
gh release create v0.1.0 \
  --title "Paper2PPT v0.1.0" \
  --notes-file CHANGELOG.md \
  examples/output/paper2ppt-example-zh.pptx
```

将示例中的版本替换为 `VERSION` 的实际值。确认 release 指向预期 commit、附件可下载、远程 CI 通过后再宣布完成。

Paper2PPT 不发布 PyPI 包；不要创建 wheel、sdist 或 PyPI Trusted Publisher 流程。

## 回滚

若 release 后发现问题，保留 Git 历史，修复后发布新的 patch 版本。不要移动已公开 tag 指向，也不要静默替换 release 附件。对会生成错误科学内容的缺陷，应先在 release notes 标记影响范围，必要时撤下受影响附件，再发布可验证修复。
