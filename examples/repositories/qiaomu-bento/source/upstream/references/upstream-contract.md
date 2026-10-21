# bento 上游契约与边界

## 固定上游快照

本 skill 独立携带：

- `assets/bento/Bento_Slides.bento.html`
- `references/upstream/bento-official-skill.md`
- `references/upstream/bento-agents.md`
- `references/upstream/bento-format.md`

具体版本、Git commit 和 SHA-256 见根目录 `NOTICE.md`。这些文件来自
MIT 许可的 `nyblnet/bento`，因此 clean install 后不需要原始仓库或网络。
机器可读锁文件是根目录 `upstream.lock.json`；package validation 会逐个核对
文件大小和 SHA-256，防止文档与 shell 来自不同 release。

格式和运行时会继续演进。固定快照之间发生冲突时，优先级为：

1. 内置 shell 实际能打开的文档格式。
2. `bento-format.md`。
3. `bento-agents.md` 与官方 skill。

不要凭记忆发明字段。

## 冻结不变量

- 一个 `.bento.html` 是文档、viewer 和 editor 的完整单文件。
- `#bento-doc` 必须保持 plaintext、同一 id、可用正则提取。
- 写回 JSON 时 `<` 必须序列化为 `\u003c`。
- 既有文档的 `docId` 永不重建；只有“新建独立文档”能生成新 id。
- 文档格式是 additive；编辑时保留未知字段。
- collab 凭据属于文档能力，不由内容生成 skill 创造或轮换。
- 发布、签名和部署属于维护者流程，不属于本 skill。

## shell 策略

默认使用内置 `assets/bento/Bento_Slides.bento.html`。可通过以下方式显式
替换，但都不属于正常运行前置条件：

- `--shell /path/to/Bento_Slides.bento.html`
- `BENTO_SHELL=/path/to/Bento_Slides.bento.html`

本地 checkout 只用于上游兼容性复核或刷新快照。刷新属于 skill 维护任务，
必须重新记录版本、commit、hash，并重跑 standalone clean-install eval。

## 上游同步策略

- 只跟踪 GitHub 正式 release，不直接打包 `main` 的未发布状态。
- shell release asset、官方 skill、`docs/agents.md` 和 `docs/format.md` 必须来自
  同一个 tag；不得混用“最新文档 + 旧 runtime”。
- `python3 scripts/sync_upstream.py` 只检查差异，不写文件。
- `python3 scripts/sync_upstream.py --update` 先下载到 staging，验证完整集合，
  再以可回滚 transaction 更新四个快照、`upstream.lock.json` 和 `NOTICE.md`。
- `.github/workflows/sync-bento-upstream.yml` 每日检查一次。发现新 release 后
  生成自动 PR，重跑可自动化门禁，并把 browser visual review 留作人工 merge gate。
- 普通安装者和普通 deck 生成不联网；独立运行能力不受 GitHub 可用性影响。

## rollback boundary

- 默认输出新文件。
- 不原地重写用户的 source deck。
- 不修改 bento 源码、generated dirs、release manifests 或密钥。
- 若用户明确要求覆盖，仍先生成临时结果并验证，再执行覆盖；报告原文件
  是否有备份以及如何恢复。
