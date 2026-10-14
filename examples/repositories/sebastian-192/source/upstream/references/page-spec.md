# Page Spec v1：图片生成与可编辑还原的中间契约

[机器 Schema](page-spec.schema.json) · [示例](../examples/page-spec.example.json)

新任务在 `style.visual_spec` 保留可读说明，并填写 `style.tokens`：`palette` 的背景/正文/主色/强调色，`typography` 的中英文实际字体和标题/正文字号，`layout` 的网格、边距与间距，以及 `image_treatment`。`reference_images` 可指向任务目录内已选总览或关键参考页，路径相对 Page Spec；验证器会检查文件。旧任务缺少 `tokens` 仍可读取，恢复时可逐步补齐。

`page-spec.json` 在内容大纲已确认、视觉方向已锁定后创建。它保存已经知道的准确内容和语义结构，避免 Step 3 从整页图片重新 OCR 或猜测图表数据。

它不是 PPTX 导出场景：位置只允许写 `bbox_hint`，不要求像 Scene 一样精确；最终坐标、原生样式与素材路径仍写入 `scene.json`。

## 生命周期

1. Step 1 内容确认后，把页序、标题、核心结论、准确文字/数据和来源写入 `deck-spec.md`。
2. 风格锁定后进入 S5，将已确认内容与 `style` 一起写入 Page Spec，再运行验证器；不得提前写入虚假的风格授权。
3. Step 2 每完成一页，记录最终 `image_file`、`image_status`、实际提示词和更新后的布局提示。
4. 交付图片版前使用 `--require-images` 再验证一次，确保所有页面图片存在且状态为 `approved`。
5. Step 3 以 Page Spec 为语义事实源、页面图片为视觉事实源。按[变更与恢复规则](workflow-updates.md)区分已授权修改与未知冲突；仅对未知冲突请求确认，不得静默用 OCR 覆盖已确认内容。

直接还原现有页面时，将 `style.decision` 设为 `locked-reference`，`visual_spec` 写明保持原页，`authorization` 记录用户要求还原原图的指令；低置信度内容按元素标记为 `unresolved`。

## 关键字段

- `content_approved` 固定为 `true`，表示新材料任务的大纲已经确认，或直接还原任务已明确授权保留原页内容；`content_version` 与 `content_authorization` 记录对应版本和用户原话。它不代表每个模糊字符都已确认。
- `style.decision` 记录 `selected`、`locked-reference`、`skipped` 或 `delegated`，并保留相关授权原文。
- `slides[].elements` 使用稳定 ID。准确文字写 `text`，表格/图表原始值写 `data`，来源写 `source_ref`。
- 图表或图片上必须直接读出的数字、日期、单位可加入该页 `required_visible_values`；不要求把未打印在图上的底层图表数据当作可见文字。
- 页面包含总页数（如 `1/10`）、目录总量或依赖整套页数的构图时，设置 `depends_on_slide_count: true`。页数变化会使这些页面重新生成；未设置或为 `false` 时，计划按本页内容、页序和图片是否变化判断是否复用。所有实际可见的页码和总页数也应写入文字元素或 `required_visible_values`，不能只留在提示词里。
- `confirmation_status` 区分用户确认、来源可验证和未解决内容；直接还原中的低置信度文字必须标为 `unresolved` 并记录 `confidence`，不能伪装成已确认。
- `native_intent` 表示 Step 3 期望的输出：`native`、`raster` 或 `either`。
- `bbox_hint` 是 `[x, y, w, h]` 的整页画布坐标提示；它可以在图片页验收后更新，但不能冒充最终 Scene 坐标。
- `separate_asset: true` 表示该视觉对象在可编辑版中需要独立移动或替换。
- `slides[].speaker_notes` 保存已确定的可选讲稿，允许明确空字符串，缺失表示未声明；`notes` 工作记录不会自动导出。讲稿不参与图片提示/必现文字，但写入图片版 PPTX，重建时沿用到 Scene；见[讲稿保留](speaker-notes.md)。

## 验证

内容与风格锁定、尚未生成图片时：

```sh
python "<skill-dir>/scripts/validate_page_spec.py" "<work>/page-spec.json" --strict
```

图片版交付前：

```sh
python "<skill-dir>/scripts/validate_page_spec.py" "<work>/page-spec.json" --require-images --strict
python "<skill-dir>/scripts/build_image_ppt.py" "<work>/page-spec.json" "<work>/output/image-deck.pptx"
```

验证器检查 Schema、有限数值、连续页码、唯一 ID、画布边界和不重复的相对图片路径。`--require-images` 还检查批准状态、文件存在性、PNG/JPEG 可读性和 EXIF 校正后的画幅比例（允许单像素取整误差）。`--strict` 拒绝未解决元素；直接还原任务可先不加 `--strict` 以保留低置信度项，但交付前必须逐项说明。验证器不检查图片中的文字是否正确，也不替代逐页视觉验收。

图片构建器以 Page Spec 为输入时会自动执行上述两项严格检查，只导出 `slides` 中声明的图片，并继承列表顺序与 `canvas` 比例。可指定 `--width` 或 `--height` 改变物理尺寸；同时指定两者时必须保持该比例。直接传图片目录仍使用旧版自然排序模式，仅适用于没有 Page Spec 的独立合并任务。

## 图片页内容核对

宿主看图或使用其已有识别能力后，可把观察到的文字填入哈希绑定模板。单页示例：

```sh
python "<skill-dir>/scripts/audit_page_content.py" "<work>/page-spec.json" "<work>/observations-s02.json" --init --slide s02
```

将 `observed_text` 填为图片中实际可见的文字，完整转录后把 `status` 从 `partial` 改为 `complete`。再运行：

```sh
python "<skill-dir>/scripts/audit_page_content.py" "<work>/page-spec.json" "<work>/observations-s02.json" --slide s02 --require-complete --output "<work>/content-audit-s02.json"
```

脚本对照已确认文本及 `required_visible_values`，标出缺失文字、数字和单位。图片文件变化会使旧观察记录失效；`partial` 不能通过完整核对。识别结果只是检查证据，不能覆盖 Page Spec。图表/表格中未明确要求显示的底层数据和识别漏字仍需人工检查。
