# 多材料评测：冻结、记录与汇总

只在跨材料质量回归或评测集验收时使用；普通单套制作仍走原有内容/风格确认与逐页验收。脚本检验证据及统计，来源含义、讲解深度、实际可读性和审阅者独立性仍需真实审阅。

## 冻结批次

`evaluate_benchmark.py freeze registry.json batch.json` 先于运行。注册表版本 `1.0`，声明实际候选源码的40位 `candidate_commit`、非空规则文件 `rubric`，以及批次全部 `cases`。案例记录 `id`、`category`（paper/statistics/policy/teaching/project/reconstruction）、`split`（development/holdout）、材料稳定身份 `source_id`、其他同源地址 `source_aliases`、`delivery_scope`（image_and_editable/reconstruction）。holdout 必须声明 `used_for_tuning: false`。脚本归一常见 DOI/arXiv 版本及网页片段，但不同机构转载等同源关系仍由注册者在 aliases 中如实登记。

冻结文件和规则绑定哈希，拒绝意外覆盖或重复材料。规则变化另建批次并保留旧规则文件。小批次可运行工具验证，不能据此宣称30材料终验达标。

## 记录每次交付

独立审阅前，用 `review-contract page-spec.json contract.json` 导出仅含可见内容、数据、来源与讲稿的合同，再用 `verify-review-contract page-spec.json contract.json` 核验。原始 Page Spec 仍供脚本评分，但不要把其中的生成提示、修复建议或工作 notes 打印给审阅者。投影只支持明确表格/图表字段，未知数据字段计数；有遗漏时先整理完整的数据合同，不能把不完整投影当成完整评审输入。

调用台账也需分离：审阅者读取实际次数、时间、产物路径和修改事务，作者的页面质量 pass/fail、自评和拟议修复另存。脚本绑定原始台账，审阅上下文只读取客观事务投影；不能因命令已去掉 Page Spec 提示就声称整套输入已经隔离。记录意外暴露并保留该次判断，后续严格评测使用新的未暴露审阅者。

为每次尝试使用独立目录，保留旧产物，不在原位置修复首次文件。尝试JSON包含：

- `case_id`、实际 `candidate_commit`、`producer_id`、`execution_status`（delivered/aborted）；holdout 另声明 `holdout_clean: true`。中断仍计入冻结分母。
- `sources`：实际源材料快照文件列表。
- `records`：`content_draft`、`authorizations`、`run_log`、`edit_check` 的路径。
- `deliveries`：图片和可编辑分别为 `image`、`editable`；还原入口只有 editable。每项给 `page_spec`、`render_report`、`visual_review`、`observations` 文件列表；可编辑项必须有 `scene`，支持几何观察时可加 `chart_observations`。
- `independent_review`：独立审阅JSON路径。

所有尝试路径相对该JSON所在目录。授权文件保存实际 `user_quote` 与 `stages.content/style/editable: true`。运行台账保存 `complete: true`、实际 `elapsed_seconds` 和 events：每项 stage（style/initial_page/repair/program_fallback/build/render/edit）、outcome（pass/fail）、本地调用证据文件 `evidence`。标准图片入口须保留四次风格调用和初始页面调用；本工具当前仅覆盖这个选型入口，不适用于跳过四套风格的图片批次。调用成本、有限重试政策及是否如实执行由独立审阅核验。

任务特有的构建脚本、安装/复现记录等放入 `records.additional_evidence` 路径数组，使它们也纳入当前审阅绑定。审阅者核对实际候选版本、调用成本、重试上限及来源关系；不能仅以一个非空日志文件证明这些事实。

编辑检查JSON为 `operations` 列表，至少 text_edit 和 object_move；含图表/表格时分别加 chart_data_edit/table_data_edit。每项给 kind、status: pass、notes、slide_id、element_id、before_scene、after_scene、after_deck、render_report。路径相对编辑检查文件；每项起点的Scene内容必须与正式交付一致。脚本验证指定对象实际变化、修改后PPTX匹配Scene、当前实际渲染及素材哈希；渲染可读性仍需独立审阅。

先调用 `inspect batch.json attempt.json review-input.json` 得到 `review_input_sha256`，不写入交付历史。让实际独立审阅者读取原材料、规则、全部产物和修改证据，不提供预期结论；从混合日志中分离作者自评，提供原始调用和修改事务。审阅JSON：version: 1.0、input_sha256、reviewer_id（与producer不同）、independent: true、prior_conclusions_exposed: false、非负整数 major_factual_errors，及 dimensions 五项 content/facts_sources/visual_data/editing_updates/delivery_reproduction，每项有 status（pass/fail/incomplete）和实际判断 notes。漏报或已暴露作者判断不能计通过，另由新审阅者核验；原始记录保留。独立性和身份是可检查的记录声明，脚本无法证明其真实性。

正式首次交付应先取得完整审阅再 record。缺审阅的已封存首次成绩不能事后补成通过。

```sh
python scripts/evaluate_benchmark.py record batch.json attempt.json history
python scripts/evaluate_benchmark.py report batch.json history report-001.json
```

record 使用排他创建的连续文件、前序哈希和当前 head 记录，检测意外覆盖、记录改动和尾部删除。它是文件完整性检查，不是防篡改签名系统。写入中断导致记录/head不一致时保留原文件，人工核验后恢复，不能悄悄忽略记录。report 实际重跑交付评分，不接受手填旧scorecard；依赖文件变化使该版本不再有效。晚补证据不能提升封存结果；修复另记新尝试。首次与最终结果、类别、开发/holdout分别统计；未执行也留在分母。

`ultimate_goal_checks_passed` 仅指该批次已提供证据符合当前数值与状态门槛（30份、每类5份、holdout10份、首次≥90%、最终全部通过且重大事实错误0），不能代替对未参与调优、实际候选版本、身份和语义判断真实性的核验，也不会自动完成宿主目标。
