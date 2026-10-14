# 制作成本与首次交付记录

使用 `record_work.py` 记录实际发生的材料准备、生图、返修、审阅及交付。每次生图调用记一条 `generation`，风格预览和失败调用也计入；并发调用的 duration 不相加当作墙钟时间。`revision` 必须给出页 ID。开始与结束的真实时间用于计算整个任务历时，未记录结束时返回 null。

```bash
python scripts/record_work.py task/production.jsonl --task demo-01 --kind start --note "开始材料阅读"
python scripts/record_work.py task/production.jsonl --task demo-01 --kind generation --page s01 --seconds 95 --note "实际生成第1页，结果文件 slides/01.png"
python scripts/record_work.py task/production.jsonl --task demo-01 --kind review --page s01 --seconds 45 --note "实际查看原尺寸渲染，标题重叠"
python scripts/record_work.py task/production.jsonl --task demo-01 --kind delivery --delivery-status fail --note "首次完整交付：第1页标题重叠"
python scripts/record_work.py task/production.jsonl --task demo-01 --kind revision --page s01 --note "调整标题框后重新渲染"
python scripts/record_work.py task/production.jsonl --task demo-01 --kind delivery --delivery-status pass --note "修复版当前检查通过"
python scripts/record_work.py task/production.jsonl --task demo-01 --kind end --note "交付与检查完成"
python scripts/record_work.py task/production.jsonl
```

`--at` 接受含时区的 ISO 时间，供已有真实日志迁入；不能凭回忆补造耗时或首次通过。`--seconds` 只在实测时填写，未计时的 review 保留缺失数量；没有实测审阅时间时总用时为 null，不能解释为零。

`job.json` 可选加入 `"work_log": "production.jsonl"`。日志放在材料目录，与流水线工作目录分开；摘要显示已记录生图次数、返修页数、审阅用时、任务历时以及首次交付状态。质量检查仍按当前成品与审阅证据执行。

日志用进程锁、逐条哈希链与同步写入保护。已结束任务拒绝续写；发现半条记录或哈希不一致时拒绝统计，应保留原文件排查，不自动删除历史。哈希不认证事件真实性，亦不证明 Agent 的记录完整。

多个不同任务可汇总：

```bash
python scripts/record_work.py task-a/production.jsonl --aggregate task-b/production.jsonl task-c/production.jsonl
```

首次通过率 = 首次完整交付记录为 pass 的任务数 / 提供的全部任务数。首次失败后修复通过仍保留首次失败；未交付任务留在分母并单列 pending。重复 task_id 拒绝汇总。调用者负责完整登记任务，不能只挑选成功案例。此统计不证明普遍成功率或独立盲评结果。
