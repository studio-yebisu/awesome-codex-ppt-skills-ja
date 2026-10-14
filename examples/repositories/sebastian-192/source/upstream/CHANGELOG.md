# Changelog

本项目的所有显著变更都记录在此文件中。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循语义化版本。

## [Unreleased]

## [2.17.0] - 2026-10-08

### Added

- A dependency-free `slidemuse.py` entry point for common existing tools, preserving arguments, working directory and pipeline exit codes while selecting the local isolated Python.
- Read-only runtime diagnosis with structured JSON, minimum-version and bounded import checks, shared renderer discovery, and actionable repair commands even when dependencies are missing.
- Bilingual CLI documentation, structured bug/feature forms and a pull request template with reproduction, validation and compatibility context.

### Changed

- Installation includes the unified entry point and CLI guides; package and relocation regressions exercise the installed commands.

## [2.16.3] - 2026-10-07

### Changed

- Replace the README hero's transportation cover with Weld Inspect and its architecture slide with the second red-and-gold showcase image, the ceramic restoration process page.
- Keep Snowline Watch in the hero and update both READMEs' descriptions and image cache version for the new selection.

## [2.16.2] - 2026-10-07

### Changed

- Refresh the bilingual README hero with a light background, prominent SlideMuse wordmark and presentation cards based on the existing transportation, glacier-inspection and manufacturing showcases.
- Include the lossless WebP hero in the release package and update both READMEs to use the same asset.

## [2.16.1] - 2026-10-06

### Added

- A public six-slide editable IRENA sample with image/native decks, four independent editing exercises, source PDF, portable inputs, before/after previews and a PowerPoint-export comparison video.
- A complete sample archive containing pinned runtime scripts and a reproduction command that checks native objects, embedded chart workbooks and speaker notes.
- Bilingual guides and homepage download links, with historical independent acceptance and current rebuild verification recorded separately.
- The installer includes the public sample when present; packaged-install regression rebuilds all six decks from the installed files.

### Scope

- The sample covers selected 2024 statistics and the original 2025 report-time scenario. Edited table/chart pages explicitly identify synthetic values.
- Reproduction starts from approved images and structured inputs. Native fills and chart axes differ visually from the image version as documented.

## [2.16.0] - 2026-10-03

### Added

- Bounded renderer subprocesses with configurable timeout, limited safe retries and ownership-checked PowerPoint cleanup that preserves pre-existing interactive sessions.
- Automatic render-cache fingerprints for renderer executable bytes, installed fonts, system and Python dependency versions.
- Optional actual PowerPoint text/table bounds and text-overlap diagnostics, cached with page evidence and surfaced as actionable review tasks.
- Six-page real-backend regression controls and a dedicated LibreOffice/Poppler CI job with exported images.
- Append-only production event logs with explicit generation calls, revised pages, measured review time, wall time and preserved first/final delivery outcomes.

### Fixed

- A shared BOM-tolerant JSON reader keeps Page Spec, Scene, data bindings and review evidence consistent throughout validation and delivery.
- Visible numeric dependency changes invalidate only the relevant pages and their transitive provenance; unrelated rendered pages and genuinely recorded reviews remain reusable.

### Scope

- PowerPoint measurements are diagnostics, not automatic visual approval; grouped/rotated text and chart labels still require visual inspection.
- Production metrics cover explicitly recorded events only; missing times remain unknown, and repaired final success does not erase first-delivery failure.

## [2.15.0] - 2026-10-02

### Added

- Conservative native text layout estimates in editable compilation, object auditing and delivery scorecards, including individual table cells and grouped objects.
- Page/element-specific Chinese overflow tasks in pipeline summaries and the existing review panel. Explicit current visual review resolves tasks while retaining estimates in reports.

### Changed

- Reorganize both READMEs around installation and current capabilities, including speaker notes, linked data updates, resumable delivery, and optional review tooling.
- Document rendering prerequisites, prepared-task CLI usage, output files, and pending-review semantics; remove duplicated installation instructions and the fixed installation-time claim.
- Unresolved inheritance, auto-fit, transformed groups and unsupported text layouts remain explicitly unverified. Estimates neither modify content nor replace actual rendering and visual review.

## [2.14.1] - 2026-10-02

### Changed

- Clarify in both READMEs that the review panel is optional, records findings and issue locations, and does not require users to fill every page manually. Agents may record checks after actual visual inspection or use the existing JSON workflow.
- Document the exported-text fallback and the requirement to rerun evaluation after importing review records.

## [2.14.0] - 2026-10-02

### Added

- Offline per-page review panel with embedded source/render images, current tasks, visual notes, content observations, data subchecks and actual data-visual inventory.
- Download/load review drafts and explicitly import them through `review_panel.py`; exact current input/artifact/record bindings reject stale or concurrently changed evidence.
- Import archives prior records and invalidates the old scorecard. A checked journal completes interrupted two-file commits before subsequent scoring; external evidence remains read-only.

### Changed

- Pipeline summaries link to the current panel; pending and failed checks remain explicit and require a new evaluation after import.
- Pipeline JSON writes use deterministic LF bytes for cross-platform import recovery hashes.

## [2.13.0] - 2026-10-02

### Added

- `init_deck.py` generates portable image/editable job configuration with exclusive creation; existing jobs, source files and approval states are preserved.
- Read-only `run_deck.py --check` collects missing page images, approval states, invalid specifications/assets/notes, workspace ownership and renderer environment problems before execution.
- Chinese status labels, page-specific review tasks with current file/image paths, retained original diagnostics and a readable Chinese summary. Stable machine status/kind fields remain compatible.
- Actual per-stage tool timings for validation, build/object checks, rendering/template preparation and evaluation; preparation and human review are explicitly outside these timings.

### Fixed

- A stopped stage summary no longer describes the entire delivery as passed.
- UTF-8 BOM job files are accepted consistently with Page Spec inputs.
- Review-sheet thumbnails adapt to the actual page aspect ratio, making portrait source pages readable without a fixed landscape thumbnail box.

## [2.12.0] - 2026-10-02

### Added

- Unified `run_deck.py` command for validated image/editable builds, rendering, review templates, live evaluation and a consolidated action queue.
- Atomic checkpoints, process-released workspace locking, hash-verified artifacts and resumable stages, including recovery after actual process termination.
- Per-page render keys and conservative migration of genuine recorded reviews for unchanged pages. Changed pages stay pending; whole-deck scorecards are regenerated each run.
- Selected-slide PowerPoint export and selected-page LibreOffice rasterization, with full PDF conversion retained. Backend changes invalidate all cached renders.
- Read-only status, deliberate stage stops and forced rendering refresh after font or renderer environment changes.
- Pipeline configuration example and documentation covering approval prerequisites, cache boundaries, external evidence preservation and exit codes.

### Changed

- Runtime and schema changes invalidate cached work; speaker-note-only changes rebuild the deck and recheck notes while retaining unchanged page images.
- Superseded scorecards and review records are archived before replacement, so interrupted work does not leave an old pass as the current result.

## [2.11.0] - 2026-10-02

### Added

- Precise standalone grouped horizontal bar and vertical column figures with named series, legends, shared zero axes, signed values, bounded labels, atomic PNG writes and optional authorized region replacement.
- Independent observed endpoint checks for grouped bar/column charts; category and series identity and numeric-axis direction are checked. Existing single-series observations remain supported.
- Optional explicit numeric dependency contracts for Page Spec/Scene chart/table leaves, derived arithmetic, visible prose and speaker notes. Preview changes without writes, or export a separate asset-preserving review draft; reject stale bindings, cycles, unsafe expressions, zero division and nonfinite results.
- Optional `evaluate_delivery.py --data-bindings` checks with hash-bound contract/document evidence; inconsistent declared prose, data or notes fail delivery.
- A reproducible two-page synthetic transport example with grouped charts and 26 bindings, demonstrating a data change propagated to 14 targets.

### Changed

- Visible-content draft exports invalidate Page Spec approval and affected image status; old source files and quality records remain unchanged. Source/semantic review and fresh rendering are still required under the task's existing authorization.
- Standalone construction geometry uses region coordinates, while replaced-page geometry uses page coordinates. Construction values are not independent observations.

### Scope

- Stacked/logarithmic charts, external workbook formula evaluation and automatic semantic dependency discovery remain unsupported. New example figures are synthetic engineering checks, not a general first-pass reliability claim or new formal holdout acceptance.

## [2.10.0] - 2026-10-01

### Added

- Multi-material benchmark records with a frozen source registry and rubric, hash-bound evidence, append-only delivery history, separate first/final results, and all registered materials in the denominator. Actual delivery checks and editing exercises are rerun; missing or changed evidence cannot become a pass.
- A verified content-contract projection for independent review that excludes generation prompts and author work judgments. Review input isolation and actual source/visual judgments remain the reviewer's responsibility.

### Fixed

- Native chart auditing now checks the actual embedded workbook cells referenced by each series, category and label. Changing only the display cache cannot pass as an editable data update.
- Benchmark evidence includes reference images actually consumed by Scene auditing, including references used by editing exercises.
- Data-update review covers dependent differences, percentages, conclusions and presenter notes; native cell changes alone do not establish a consistent edited page.

### Scope

- These tools support evaluation; they do not prove semantic correctness or reviewer identity. A development prototype or passing software tests do not demonstrate the 30-material acceptance target.

## [2.9.0] - 2026-10-01

### Added

- Optional Page Spec/Scene `speaker_notes` preserved in image and editable PPTX, checked after save/reopen. Editable compilation can verify upstream slide IDs/order and declared notes with `--page-spec`.
- Exact-note auditing of actual PPTX and optional Scene, integrated into delivery scorecards and object auditing. Explicit empty notes reject residual text; old Page Specs without declared notes remain compatible, and legacy Scene notes remain supported.
- A hash-bound Markdown speaker-note companion with recorded source references, preserving text without inferring presenter content from work records.
- Material-specific semantic review for research mechanisms/formulas, experiment scope, source conflicts, policy targets and observed effects, informed by official Slidev/Marp documentation.

### Changed

- Notes-only updates rebuild exports while reusing approved page images. Visible copy/layout changes retain the existing regeneration and approval rules.
- Production notes are separated from Page Spec work records. Notes fidelity is not a semantic depth score and does not replace required visible evidence or user approval.

## [2.8.0] - 2026-09-30

### Added

- Separate chart source/label/geometry checks and a per-page data-visual inventory in hash-bound visual review v1.2. Missing checks keep delivery incomplete; failed subchecks and unlisted data visuals fail delivery.
- A finite-retry chart repair workflow, a hash-bound audit of independently observed zero-based single-series bar/column geometry, and a precise horizontal-bar raster region fallback that preserves pixels outside an explicitly selected rectangle. Host image-edit authorization still applies.
- Scene-native chart point colors, negative-value inversion, label position/size, axis visibility/order, bar gaps, doughnut hole/angle, normalized inner plot layout, and rounded rectangle adjustment. Exported settings are audited without reapplying them.

### Changed

- Image prompts forbid decorative unsupported data visuals, including unlabeled curves/scatter/axes on research-proposal slides. Numeric labels and geometry are reviewed separately.
- Default presentation of artifacts avoids redisplaying tool-visible images, historical drafts, and intermediate repair previews; all inspection evidence remains saved.
- Legacy v1.1 reviews remain historical evidence and require actual additional checks in a new v1.2 template; no version-only migration. Content-depth and approval gates retain their scope.

## [2.7.0] - 2026-09-30

### Added

- Content-depth reference with a reviewable slide-by-slide draft, purpose-specific guidance, traceable evidence, interpretation boundaries, and a worked example of repairing an unsupported claim.
- A semantic content-quality review before style selection, with versioned findings and repairs recorded separately from user approval or explicit content delegation. It is not an automated depth score.

### Changed

- Step 1A and the deck specification now include the deck's central question and answer, narrative progression, actual visible copy/chart content, and optional speaker notes. Covers and transitions remain concise without universal word counts or text ratios.
- Style previews, Page Spec creation, and image prompts preserve approved supporting explanations and qualifications instead of reducing the draft to titles and large numbers. Content updates repeat only affected reviews and retain existing authorization.
- Bilingual documentation and the Codex starter prompt describe content review and the subsequent approval gate. The new reference is included in release packages and runtime installations.

## [2.6.1] - 2026-09-30

### Fixed

- Installer success output uses an ASCII status label so Windows GBK output does not raise a UnicodeEncodeError after a successful installation.
- Release archives include their manifest so the bundled installer can register every required runtime root. A regression test installs from the exact manifest-packaged ZIP rather than only from the source checkout.

## [2.6.0] - 2026-09-30

### Fixed

- Delivery evaluation verifies each current Page Spec reference image against the render report hash, rejecting replaced images even when new content observations are supplied with an old deck and review.
- Visual review v1.1 binds Page Spec, reference image hashes and the render backend as well as the deck and rendered PNGs. Legacy evidence must be recreated and reviewed instead of silently passing.

### Added

- Chart and table elements have independent data-review entries with required notes for pass/fail. Missing or pending data reviews keep delivery incomplete; failed data reviews fail delivery. Scorecards retain per-element findings.
- Optional Page Spec `depends_on_slide_count` marks pages displaying total-page counts or depending on deck size.

### Changed

- Appending or removing pages no longer regenerates every unchanged image. Updates target new pages, changed content/order and explicit total-count dependencies while still rebuilding exported decks.

## [2.5.0] - 2026-09-24

### Added

- `evaluate_delivery.py` combines hash-bound render output, complete content observations, per-slide visual review, and optional Scene editability audit into a repeatable delivery scorecard. Missing review evidence remains `incomplete`; stale artifacts are rejected.
- Render reports now record the PPTX, Page Spec, and per-slide PNG hashes so evaluation cannot silently reuse an earlier render.

## [2.4.0] - 2026-09-24

### Added

- `audit_page_content.py` compares hash-bound visual transcriptions with confirmed Page Spec text and explicitly required visible values. Incomplete or stale observations cannot pass its strict gate.
- `plan_deck_update.py` snapshots approved page and style-reference hashes, then reports slides to reuse, review or regenerate after content, order or style changes.
- Optional per-slide `required_visible_values` captures chart labels and other facts that must be readable in the final image.

## [2.3.0] - 2026-09-24

### Added

- `render_deck.py` renders every PPTX slide using PowerPoint or LibreOffice/Poppler, producing numbered PNGs, a review sheet, and a JSON report. With Page Spec it adds source/render/difference comparison, including historical `revision` references.
- Optional structured `style.tokens` in Page Spec records palette, typography, layout, image treatment and selected reference images; new tasks use it while older specs remain valid.

### Changed

- Raster text overlay fails instead of exporting a page when text exceeds its box. Documentation and skill steps now route image and editable PPTX through the same rendering review tool.

## [2.2.3] - 2026-09-23

### Fixed

- Windows 刚使用完虚拟环境时可能短暂锁定技能目录；安装器在目录切换时对该类错误进行有界重试，使完整安装与升级能继续完成。

## [2.2.2] - 2026-09-23

### Added

- Scene 图表新增数值轴范围、主网格线及其颜色、坐标轴标签颜色和数据标签颜色；导出和对象审查均支持这些设置。

### Changed

- 缩短技能入口描述，保留完整流程说明在正文中。
- 发布流程覆盖清单中的文件路径，并在同一版本的打包内容发生变化时要求升版。
- 文档中的反馈入口改为仓库已开放的 Discussions。

### Fixed

- 安装器在同时检测到多个受支持客户端时不再静默优先选择 Codex；现在会要求通过 `--client` 明确指定目标，避免安装到错误的 Skill 目录。
- 安装器现在也能发现旧 Codex 技能目录中的 `image-ppt`，在安装新名称后给出迁移提示。
- 安装与升级先在临时目录完成依赖安装和自检；新目录激活后再次验证，失败时恢复旧版，避免半更新状态。
- `--skip-deps` 升级不再沿用旧环境的 `.skill-python` 路径；CI 增加真实隔离安装与升级检查。

## [2.2.1] - 2026-09-20

### Changed

- 统一 GitHub 与技能元数据定位：以大学生竞赛 PPT 为重点，同时保留学术汇报、论文答辩、项目路演、课程展示、电影质感 PPT 与图片转可编辑 PPT 等通用场景。
- README 重点赛事补充全国大学生交通运输科技大赛（交科赛），并继续覆盖挑战杯（大挑/小挑）、中国国际大学生创新大赛、三创赛、正大杯和大创等场景。
- 中英文 README、SKILL.md、Agent 元数据与 manifest 同步更新；新增交科赛和课程展示相关触发词。


## [2.2.0] - 2026-09-20

### Changed

- 项目品牌由 image-ppt 升级为 **SlideMuse**；GitHub 仓库同步更名为 `helloo1568/slidemuse`，旧地址由 GitHub 重定向兼容。
- Skill 正式调用名改为 `$slidemuse`，并同步 README、OpenAI Agent 元数据、使用指南与发布包命名。
- README 首屏增加 30 秒安装入口，优先引导用户让 Agent 自动执行安装器。

### Added

- 强化 `install.py`：自动识别 Codex / Claude Code / OpenCode，创建隔离虚拟环境、安装依赖、运行自检，并安全提示旧 `image-ppt` 安装目录。
- 增加安装器 dry-run 测试，确保 Codex 默认安装路径与新 Skill 名保持一致。

## [2.1.1] - 2026-09-18

### Fixed

- 风格阶段默认一次调用直接生成一套缩略总览，正常四套四次；新增本地缩略图排版工具，利用已有图片或明确裁切框完成缩放、网格和页码，不再为排版重复生图。
- 风格预览明确使用横向缩略网格，禁止纵向整页长图；新增当前四套候选清单与结构验证，阻止竖图、缺图、重复方案和将修正稿误计成额外方案。网格与文字内容仍需视觉核验。
- 图片版导出支持直接读取 Page Spec，仅按批准清单与页序合并，沿用画布比例，避免目录中的旧稿混入；验证失败保留既有输出。
- Page Spec 交付验证拒绝重复图片路径与错误画幅，允许单像素取整误差并应用 EXIF 方向。
- 可编辑性审查补齐图片位置、尺寸、裁切、翻转，以及嵌套组合的父子坐标变换和旋转检查。
- 文字兜底保留完整非文字主体，避免在 Step 2 提前移除 Step 3 才需拆分的素材。
- 统一内容代定授权后的继续规则；四套风格总览支持短稿、单页和任务指定比例。

### Changed

- 新增变更与恢复规则及规格记录：保存基准快照、版本和授权差异，按修改范围回退状态并使受影响产物失效。
- 中英文作品集统一为单列等宽大图，保持原始宽高比；取消双列缩略图与单张展开大图混排。
- 在中英文首页、应用场景和技能元数据中补充竞赛 PPT、电影质感 PPT、创新创业路演、学术汇报及图片转可编辑 PPT 等相关关键词。
- 重设计中英文 GitHub 首页：品牌横幅、项目徽章、作品画廊、六项核心优势、三步流程与可复制的上手提示。
- 将详细流程与技术命令整理到中英文使用指南，保留能力边界、验收方法和来源说明。

### Added

- 记录 2026-09-18 三页蓝图实战验收：133 项测试、PowerPoint 实际渲染、24→30 图表与工作簿更新、独立终端移动，以及 Scene 图表外观后处理的现有限制。
- 增加挑战杯两类赛事、中国国际大学生创新大赛、三创赛和正大杯的具体应用场景、常见搜索词及官方来源链接。
- 新增 SVG 品牌横幅和双语贡献指南，并将首页引用的新资源纳入分发清单。
- 在中英文 README 首屏增加两套真实作品展示，并将安全页面预览图纳入仓库。
- 红金案例作品集收录第 2–4 页。
- 作品集图片改用源页面的 1672×941 像素尺寸，不再生成缩小版。

### Removed

- 删除旧版历史视觉素材、可编辑示例 PPTX、示例场景及其 README 展示。

## [2.1.0] - 2026-09-16

### Changed

- 将 Step 1 拆为“内容大纲确认”和“风格方案确认”两个硬门禁；未确认内容时不得生成风格总览。
- 明确四套方案的确定性豁免：严格沿用指定参考、明确跳过预览或明确授权代选，Agent 不得自行推断。
- Step 3 改为 Page Spec 提供语义事实、页面图片提供视觉事实；已确认文字和数据不再通过 OCR 重新猜测。

### Added

- Page Spec v1、JSON Schema、示例和验证脚本，记录准确内容、来源、稳定元素 ID、原生/图片意图、位置提示与页面图片状态。
- Page Spec 的 Schema、唯一 ID、连续页码、画布边界、路径约束和交付图片测试。
- CI 增加 Page Spec 示例验证。

## [2.0.1] - 2026-09-16

### Changed

- 将入口规范为唯一三阶段流程：内容提炼与四套幻灯片浏览视图 → 图片版逐页生成 → 经明确授权后的可编辑 PPTX 还原。
- 恢复硬状态机与五项需求门禁；普通任务表达不再被解释为允许自主推断、代选或跳步。
- Scene v1、分层素材和原生对象编译固定为第三阶段能力，不再作为绕过图片版的“编辑优先”替代路线。
- 规范项目定位与平台说明：最佳推荐 Codex + GPT Image 2.5，其他 Agent 调用其自身生图/编辑能力；本地脚本不冒充图像后端。
- 同步更新制作规格、阶段提示词、中英文 README、技能元数据和模型使用说明。

### Compatibility

- 保留 2.0.0 的 Scene v1、原生编译、素材裁剪、审查脚本和文件格式，不影响已有 scene.json。
- 已有页面图片/扫描 PDF 的可编辑还原可按明确请求直接从第三阶段开始；已有可编辑 PPTX 的普通修改不进入本流程。

## [2.0.0] - 2026-09-15

### Changed

- 默认改为编辑优先：先规划原生信息，再生成独立视觉素材；图片版仍可单独使用。
- 移除普通请求强制确认四项需求及四轮风格门禁；用户要求风格选择时继续等待选型。
- 更新 GPT Image 2.5 Sunburst / Flare 指南，区分宿主工具与直接 API，不假定工具支持指定模型。
- 基于 PPT Master 等项目的公开方法补齐分层重建、背景清理、稳定坐标和逐元素验收规范。

### Added

- Scene v1 JSON Schema 与原生 PPTX 编译器，支持文字、形状、线/箭头、嵌套组合、独立图片、表格、五类图表及内嵌数据工作簿。
- 素材裁剪与可选遮罩工具，记录来源、实际 bbox、透明度与文件哈希。
- 可编辑性审查，检查原生对象、内容、数据、几何、层级、素材和原图残留。
- 三页可运行场景、PowerPoint 导出的示例与预览、重建与调研参考文档。
- 原生对象往返、编辑数据、错误场景、alpha、裁剪与兼容性测试；Windows/Linux CI。

### Compatibility

- 原有 build_image_ppt.py / overlay_text.py 命令和示例继续可用。
- 新脚本增加 jsonschema 依赖，要求 Python 3.10+。
- 本地脚本不自动识图、执行 OCR、调用生图 API 或推断隐藏信息；宿主 Agent 完成识别和生图。
- 复杂插画是独立可替换图片，不宣称所有像素或曲线均已原生化。

## [1.5.0] - 2026-09-05

### Fixed

- `build_image_ppt.py`：`--fit cover` 不再把图片以负坐标溢出画布，改为整页放置 + 居中裁剪。放映效果不变，但 PowerPoint 编辑视图里不再出现挂在画布外的图片。
- `build_image_ppt.py`：自动应用 EXIF 方向信息，带旋转元数据的照片不再出现宽高比计算错误。

### Added

- `build_image_ppt.py`：新增 `--max-width` 与 `--jpeg-quality`，嵌入前等比缩小 / 重编码 JPEG，大型图片版 PPT 的体积可降低一个数量级；透明图片会先合成到 `--background` 指定的背景色。
- 新增 `scripts/overlay_text.py`：按 JSON 规格将准确文字确定性叠加到背景图上（百分比坐标、自动换行、对齐、行距、加粗、纯色页），作为生图模型文字不可靠时的兜底，对应 SKILL.md Step 2 的混合制作方式。
- 新增 `tests/` pytest 测试套件（20 个用例）与 GitHub Actions CI（ruff lint + pytest，Python 3.10–3.13 矩阵）。
- 新增 `CHANGELOG.md`、`requirements-dev.txt` 与 `examples/overlay-spec.example.json`。

### Changed

- `build_image_ppt.py`：页面背景改用幻灯片背景填充替代整页矩形，减少编辑时可误选中的形状；图片形状以源文件名命名，便于在 PowerPoint 中识别与导航。
- 中文 README 效果展示补齐缺失图片并改用仓库内相对路径，不再依赖外部 CDN 热链。
- `manifest.yaml` 版本升至 1.5.0，文件清单与仓库实际内容同步。

## [1.4.0] 及更早

见提交历史。
