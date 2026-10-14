# 讲稿的保留、导出与检查

内容稿已有可选讲稿时，内容确认后同步到 Page Spec 的 `slides[].speaker_notes`。它是面向演讲者的最终文本，不参与生图或必现文字；关键证据、变量解释和必要边界仍应在页面可见。没有讲稿时不强制补写。

- `speaker_notes` 缺失：未声明交付讲稿，旧 Page Spec 兼容。
- `speaker_notes: ""`：明确要求该页讲稿为空，检查器拒绝残留备注。
- Page Spec 既有 `notes` 是工作记录，图片构建器和讲稿导出不会自动搬运。
- Scene 新任务沿用同一页 ID 与 `speaker_notes`，不从图片 OCR 重写。Scene 旧 `notes` 继续作为历史演讲备注导出；出现新字段时以新字段为准，即使为空。不要把日志、授权记录等工作记录写入演讲备注。

图片版构建器自动写入已声明讲稿。可编辑版带上游校验编译，避免还原时遗漏/改写：

```sh
python "<skill-dir>/scripts/build_editable_ppt.py" "<work>/scene.json" "<work>/output/editable.pptx" --page-spec "<work>/page-spec.json"
python "<skill-dir>/scripts/audit_speaker_notes.py" "<work>/page-spec.json" "<work>/output/editable.pptx" --scene "<work>/scene.json" --output "<work>/output/speaker-notes-audit.json"
```

`--page-spec` 检查页 ID/顺序和已声明讲稿与 Scene 一致；不要求图片存在/批准，适用于已授权的可编辑版局部修改。没有 Page Spec 的独立 Scene 编译仍支持旧命令。

构建器保存后重开实际 PPTX 核对讲稿，失败时保留已有输出。独立检查和 `evaluate_delivery.py` 都读取实际备注；错误备注不能因视觉/正文通过而过关。仅统一 CRLF/CR 为 LF，保留空行、空格、符号和原文。报告绑定当前输入哈希，不是语义深度或演讲效果评分。

需要独立讲稿时：

```sh
python "<skill-dir>/scripts/export_speaker_notes.py" "<work>/page-spec.json" "<work>/output/speaker-notes.md"
```

输出按页序保留原讲稿和去重后的已记录来源，不联网取证、不新增推断、不输出工作记录。文本围栏原样保留讲稿/来源；Page Spec 哈希识别版本。没有任何声明讲稿时拒绝制造空交付。

只改 `speaker_notes` 时，变更计划复用页面图片，但要求重建两种 PPTX；同步 Scene 与讲稿文件并重查备注，旧评分卡因输入哈希变化需重新评测。可见内容/布局变化才触发对应生图，讲稿修改不能绕过正文内容门禁。
