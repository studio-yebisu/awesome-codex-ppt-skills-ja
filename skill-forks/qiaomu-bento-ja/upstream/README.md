# qiaomu-bento-ppt

> AI 做 PPT 最常见的失败，是交付一堆静态文字页。这个 skill 把资料变成可编辑、可演示、可离线分发的单文件 bento deck。
>
> Turn source material into an editable, presentable, offline-ready bento deck — one self-contained HTML file.

<p align="center">
  <a href="https://github.com/joeseesun/qiaomu-bento-ppt/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/joeseesun/qiaomu-bento-ppt?style=flat-square&logo=github" /></a>
  <a href="https://github.com/joeseesun/qiaomu-bento-ppt/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/joeseesun/qiaomu-bento-ppt?style=flat-square&logo=github" /></a>
  <a href="https://github.com/joeseesun/qiaomu-bento-ppt/issues"><img alt="Issues" src="https://img.shields.io/github/issues/joeseesun/qiaomu-bento-ppt?style=flat-square&logo=github" /></a>
  <a href="https://github.com/joeseesun/qiaomu-bento-ppt/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/joeseesun/qiaomu-bento-ppt?style=flat-square&logo=git" /></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" /></a>
</p>

```bash
npx skills add joeseesun/qiaomu-bento-ppt
```

[![qiaomu-bento-ppt 真实生成的 bento 演示文稿](docs/assets/qiaomu-bento-ppt-hero.png)](examples/qiaomu-bento-ppt-intro.bento.html)

<p align="center">
  <a href="examples/qiaomu-bento-ppt-intro.bento.html">下载示例 deck</a>
  ·
  <a href="examples/qiaomu-bento-ppt-intro-deck-plan.md">查看 deck plan</a>
  ·
  <a href="examples/build_intro_deck.py">查看生成脚本</a>
</p>

真实输出不是一段 JSON，而是一套可交付文件：

```text
市场洞察-deck-plan.md
市场洞察-deck.json
市场洞察.bento.html          ← 双击即可编辑、演示、保存
reports/deck-validation.json ← identity + structure + shell gate
```

仓库里的[介绍 deck](examples/qiaomu-bento-ppt-intro.bento.html)就是由本 skill
生成并在真实浏览器中验收的成品；对应的
[deck plan](examples/qiaomu-bento-ppt-intro-deck-plan.md)、
[JSON](examples/qiaomu-bento-ppt-intro.json)、
[生成脚本](examples/build_intro_deck.py)和
[验证报告](reports/intro-deck-validation.json)全部可复现。

**[中文](#中文) | [English](#english)**

---

<a name="中文"></a>
## 中文

### 为什么值得用

普通 PPT agent 容易停在“标题 + 三个 bullet”。`qiaomu-bento-ppt` 会先判断
受众、结论和叙事弧，再把不同内容交给真正合适的演示能力：

- 趋势和量级 → chart
- 规格和价格 → table
- 同一对象的前后变化 → morph
- 次级解释 → state slide
- 主视觉 → image + scrim + ken-burns
- 流程和时间线 → path / connector + motion
- 关键数字 → countUp

最终的 `.bento.html` 同时带着文档、viewer 和 editor。收件人不需要安装
PowerPoint，也不需要登录云服务。

### 真正独立运行

这个仓库已经内置：

- `upstream.lock.json` 固定的官方 bento/slides release shell
- 官方 bento agent guide
- 官方格式规范
- JSON 提取、构建、身份保护和 shell 校验脚本

因此安装后不需要 clone 原始 bento 项目，也不需要联网下载运行时。
`BENTO_REPO` 只用于上游兼容性复核，不是前置条件。

### 跟随上游，但不在运行时漂移

普通使用始终读取安装包里的固定快照。维护时可以检查 nyblnet/bento 的最新
正式 release：

```bash
python3 scripts/sync_upstream.py \
  --report reports/upstream-sync-check.json
```

确认需要刷新后：

```bash
python3 scripts/sync_upstream.py \
  --update \
  --report reports/upstream-sync.json
```

同步器要求 shell、官方 skill、`docs/agents.md` 和格式规范来自同一个 release，
全部暂存并验证成功后才替换。仓库还会每日检查一次上游；发现新 release 时
只创建带完整门禁结果的 PR，不会绕过 review 直接修改 `main`。

### 安装

1. 安装 skill：

   ```bash
   npx skills add joeseesun/qiaomu-bento-ppt
   ```

2. 验证：

   ```bash
   test -f ~/.agents/skills/qiaomu-bento-ppt/SKILL.md
   python3 ~/.agents/skills/qiaomu-bento-ppt/scripts/bento_deck.py locate
   ```

   `locate` 应返回 `"standalone": true`。

### 你可以直接这样说

- “用 qiaomu-bento-ppt 把这份报告做成 12 页离线演示文稿。”
- “修改这个 `.bento.html`，保留 docId，增加 morph 和演讲者备注。”
- “跳过确认，按默认决策型结构生成一个单文件 HTML 发布会 deck。”
- “把这些数据做成可交互图表，并在浏览器里验收。”

### 工作流

1. 生成 `deck-plan.md`：受众、目标、叙事弧、逐页计划、视觉方向和证据。
2. 读取包内固定版本的官方 bento 规范。
3. 新建 `deck.json`，或从既有 `.bento.html` 提取 JSON。
4. 把内容映射到 chart、table、morph、state、media 和 motion。
5. 使用包内 shell 构建新的 `.bento.html`，默认不覆盖源文件。
6. 检查文档结构、`docId`、文档块和 shell。
7. 在真实浏览器中检查编辑态、演示态、字体、图片、图表和动效。

### 前置条件

- [ ] 安装时需要 Node.js / npx：`node --version && npx --version`
- [ ] 运行时需要 Python 3.10+：`python3 --version`
- [ ] 需要现代浏览器打开 `.bento.html`
- [ ] 如使用外链图片或视频，需自行保证网络可用性和版权

正常生成不需要 API key、账号、bento checkout 或云服务。

### 命令行工具

检查独立资产：

```bash
python3 scripts/bento_deck.py locate
```

新建 deck：

```bash
python3 scripts/bento_deck.py build deck.json \
  --output result.bento.html \
  --new-document \
  --report reports/deck-validation.json
```

编辑已有 deck，同时锚定原始身份和 shell：

```bash
python3 scripts/bento_deck.py extract original.bento.html --output deck.json

python3 scripts/bento_deck.py build deck.json \
  --identity-source original.bento.html \
  --output original.updated.bento.html \
  --report reports/deck-validation.json
```

脚本会拒绝 `deck.json` 与原文件 `docId` 不一致的构建。

### 可选配置

| 变量 | 必需 | 说明 |
|---|---:|---|
| `BENTO_SHELL` | 否 | 显式使用另一份可信 bento shell |
| `BENTO_REPO` | 否 | 仅用于上游项目兼容性 gate |

### 验证这个 skill

```bash
python3 scripts/validate_skill.py .
python3 scripts/trigger_eval.py . \
  --cases evals/trigger_cases.json \
  --output reports/trigger-eval.json
python3 evals/output/run_fixture.py \
  --output reports/output-eval.json
```

fixture 会在临时目录完成新建和编辑两条路径，证明：

- 内置 shell 可以独立构建 deck
- 新文档只 mint 一次 UUID
- 编辑时 `docId` 保持不变
- source deck 和 fixture 都不会被改写
- 生成文件通过结构和 shell gate

### 风险与限制

- 默认会写入计划、JSON、报告和新的 `.bento.html`。
- 默认拒绝覆盖已有输出；只有明确需要时才使用 `--overwrite`。
- 外链媒体会破坏完全离线承诺。
- 固定 shell 不会自动升级；上游更新需要重新做兼容性和 clean-install 验证。
- 脚本通过不等于视觉正确。没有实际打开浏览器时，必须标记
  `missing evidence: browser visual review`。
- 本 skill 不执行 bento release、签名或部署，也不会读取签名密钥。

### Troubleshooting

| 问题 | 原因 | 解决 |
|---|---|---|
| `standalone: false` | 安装包缺少内置 shell 或规范快照 | 重新运行 `npx skills add joeseesun/qiaomu-bento-ppt` |
| `output exists` | rollback boundary 阻止覆盖 | 换输出名；明确需要时才加 `--overwrite` |
| `input docId does not match` | 编辑 JSON 与原 deck 身份不一致 | 从原文件重新 extract，并传 `--identity-source` |
| shell gate 失败 | 文档块损坏或 shell 不兼容 | 使用包内 shell 重新 build，不要手工拼 HTML |
| deck 能打开但画面不对 | 字段遗漏、越界、素材或字体不可用 | 查 validation report，再做浏览器验收 |
| 视频离线不可播放 | 使用了外链媒体 | 改成小型内嵌 data URI，或明确联网依赖 |
| 上游显示 `outdated: true` | 官方已有新 release | 审阅同步 PR，完成浏览器 gate 后再合并；普通生成不受影响 |

### 致谢

- [nyblnet/bento](https://github.com/nyblnet/bento)：bento/slides shell、官方
  skill、文档模型和格式规范。固定版本与 SHA-256 见
  [NOTICE.md](NOTICE.md)。
- `qiaomu-meta-skill`：Skill IR、触发评测与证据边界；其方法受
  [yaojingang/yao-meta-skill](https://github.com/yaojingang/yao-meta-skill)
  启发。

---

<a name="english"></a>
## English

`qiaomu-bento-ppt` turns briefs, notes, reports, datasets, or an existing
`.bento.html` file into a complete bento/slides presentation.

It is standalone: the repository includes a release-locked bento shell,
official authoring references, and deterministic build/validation tools.
No bento checkout or network download is required after installation.

Upstream maintenance is explicit and coherent: `scripts/sync_upstream.py`
checks the latest official nyblnet/bento release and can refresh the shell and
all three references from the same tag. A daily GitHub workflow opens a review
PR when a new release appears; normal deck generation never updates itself.

The preview above is a real seven-slide product deck generated by this skill
and reviewed in a browser. Download the
[single-file deck](examples/qiaomu-bento-ppt-intro.bento.html), inspect its
[deck plan](examples/qiaomu-bento-ppt-intro-deck-plan.md), or reproduce it with
the [generator](examples/build_intro_deck.py).

### Install

```bash
npx skills add joeseesun/qiaomu-bento-ppt
```

Verify:

```bash
python3 ~/.agents/skills/qiaomu-bento-ppt/scripts/bento_deck.py locate
```

Expected: `"standalone": true`.

### Natural-language examples

- “Turn this report into a 12-slide offline bento presentation.”
- “Edit this `.bento.html` deck, preserve its docId, and add morph transitions.”
- “Create a single-file HTML product-launch deck with charts and speaker notes.”

### What it protects

- the plaintext `#bento-doc` splice contract
- stable document identity when editing
- one-time UUID minting for new documents
- source-file rollback
- structural and shell integrity
- explicit evidence boundaries for browser and human visual review

### Requirements

- [ ] Node.js / npx for installation
- [ ] Python 3.10+ for build and validation
- [ ] A modern browser to edit and present the generated file

No API key or bento source checkout is required.

### Limitations

The bundled shell is pinned rather than auto-updated. External media breaks
the fully offline guarantee. Mechanical validation does not replace a real
browser review.

<!-- qiaomu-profile:start -->
## 关于向阳乔木

向阳乔木（乔向阳 / Joe）是一位实践型 AI 产品与内容创作者，长期把前沿 AI 变化转译成可复用的工作流、产品判断、AI 编程实践、AI 搜索实践和 GEO/AI 营销方法。

- 个人网站: https://qiaomu.ai
- 博客: https://blog.qiaomu.ai
- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/
- 微信公众号: 向阳乔木推荐看

### 支持与关注

| 打赏支持 | 微信公众号 |
|---|---|
| <img src="assets/qiaomu-profile/qiaomu_reward_qr.png" alt="向阳乔木打赏二维码" width="180" /> | <img src="assets/qiaomu-profile/qiaomu_wechat_public_account_qr.jpg" alt="向阳乔木推荐看公众号二维码" width="180" /> |
| 感谢支持乔木持续分享 AI 实践 | 扫码关注「向阳乔木推荐看」 |

<!-- qiaomu-profile:end -->

## License

The skill code is MIT licensed, Copyright (c) 向阳乔木.

Bundled bento assets remain MIT licensed, Copyright (c) 2026 The Bento
authors. See [NOTICE.md](NOTICE.md) and
[THIRD_PARTY_LICENSES/bento-MIT.txt](THIRD_PARTY_LICENSES/bento-MIT.txt).
