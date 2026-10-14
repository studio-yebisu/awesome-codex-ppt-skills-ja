# IRENA 六页可编辑样板

这套样板将 IRENA《Renewable capacity statistics 2025》的部分统计整理为六页中文导读。你可以直接下载成品，在 PowerPoint 中修改文字、移动图表、编辑表格和图表数据，也可以用随附的 Scene 和 Page Spec 重建。

[打开离线浏览器](index.html) · [English](README.en.md) · [官方报告](https://www.irena.org/Publications/2025/Mar/Renewable-capacity-statistics-2025)

## 先打开成品

- [原版可编辑 PPTX](decks/editable.pptx)：六页原生文字、一张原生表格、三张原生图表，图表含嵌入工作簿。
- [图片版 PPTX](decks/image.pptx)：批准页面图片组成的六页演示。
- [修改演示视频](demo.mp4)：真实 PPTX 的 PowerPoint 导出画面，展示各次修改前后结果。
- [完整样板 ZIP](https://github.com/helloo1568/slidemuse/raw/refs/heads/main/showcase/editable-irena/sample.zip)：成品、源材料、页面图片、复现输入、运行时脚本和核验记录。

样板使用 Microsoft YaHei（微软雅黑）。缺少该字体时，替代字体可能改变换行和外观。图片版与可编辑版保留同一内容，可编辑版使用平面色块和原生图表，轴线位置、刻度间隔等外观有已说明的差异。

## 亲手试一次修改

先另存一份 `editable.pptx`。四个练习分别从原版开始，互不叠加。

| 练习 | 操作位置 | 本次结果 | 参考成品 |
| :--- | :--- | :--- | :--- |
| 修改文字 | 第6页的“时间”说明 | 将末尾“解读”改为“阅读”，同步说明备注 | [text-edit.pptx](decks/text-edit.pptx) |
| 移动对象 | 第3页原生条形图 | 整张图右移8、上移4个画布像素，轴线与标签一起移动 | [object-move.pptx](decks/object-move.pptx) |
| 修改表格 | 第2页2024年末装机容量 | 将4,448,051改为练习值4,450,000 MW，差额587,119 MW，增长率15.2% | [table-edit.pptx](decks/table-edit.pptx) |
| 修改图表 | 第3页图表的太阳能数据 | 将452改为练习值460 GW，三项合计593 GW，太阳能份额77.6% | [chart-edit.pptx](decks/chart-edit.pptx) |

点击文字框直接编辑。选中图表可整体移动，右键图表选择“编辑数据”可打开嵌入工作簿。原生表格的单元格可直接编辑。

表格和图表练习页均显著标明“合成编辑练习”。练习值及派生结果不是 IRENA 新统计。手动修改数值后，需要同步相关结论、计算说明、来源边界及演讲备注。此样板提供已经同步的独立练习输入，不宣称 PowerPoint 会自动更新所有正文。

## 一条命令重建六套成品

使用 Python 3.10 或更高版本。完整 ZIP 已包含固定的 SlideMuse 运行时，在解压后的样板目录运行：

```sh
python -m pip install -r runtime/requirements.txt
python reproduce.py --verify
```

从 Git 仓库运行时，在仓库根目录执行：

```sh
python -m pip install -r requirements.txt
python showcase/editable-irena/reproduce.py --verify
```

输出位于样板的 `outputs/` 目录。包括图片版、原版可编辑版、四套练习版、讲稿和 `reproduction.json`。每个原生成品都检查对象、图表缓存和嵌入工作簿，并核对演讲备注。

Windows 安装 PowerPoint 后，可以进一步导出全部36页：

```sh
python reproduce.py --verify --render --backend powerpoint
```

Linux 可在安装 LibreOffice、Poppler 和所需字体后使用 `--render --backend libreoffice`。渲染结果会随平台、字体和软件版本变化，需实际看图核对。构建和对象核验不要求 PowerPoint。

`--output` 可指定新的输出目录。`--runtime` 可指定其他 SlideMuse 仓库根目录。`--verify` 检查公开样板的文件哈希；自己修改 Scene 后，可在自己的副本中省略这个参数重建。

## 来源和核验范围

- 原始报告：[本地75页 PDF](source/IRENA_Renewable_Capacity_Statistics_2025.pdf)，© IRENA 2025。报告PDF第2页说明带署名和版权年份的使用及分享条件；报告材料不因放入本仓库而改用 MIT 许可。
- [来源清单](source/source.json)保存官方下载链接、SHA-256、核对日期和逐页引用位置。2026-10-06重新下载的官方 PDF 与此前验收的文件一致。
- 数据基于2024年统计和报告在2025年提出的情景。本样板仅覆盖选定内容，保留容量与发电量、存量与增量的区别。
- [历史独立审阅](evidence/historical-review.md)对应 v2.10.0 的原案例，保留范围文字错误修复后的 `attempt-002` 记录。[本次核验](evidence/verification.json)对应当前公开文件，并区分历史验收与本次重建。
- [文件清单](manifest.json)绑定当前下载文件和预览图；[外观差异](evidence/historical-limitations.md)说明原生重建边界。

原案例已完成小规模独立验收。本次公开样板的重建和演示不代表所有材料的普遍成功率。图片生成过程已完成，复现命令从已批准的图片和结构化输入开始，不重新调用生图服务。
