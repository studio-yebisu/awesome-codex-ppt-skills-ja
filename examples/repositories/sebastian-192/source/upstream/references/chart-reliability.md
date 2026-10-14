# 定量图表：数值、几何与有限修复

在 S5 含定量图表、修复图表或完整交付评测时读取。继续按图片优先流程完成页面；本参考不授权跳过内容/风格门禁，也不提前创建原生 PPTX。

## 两类准确性分别验收

数字标签正确不代表图形正确。对照 Page Spec 与来源检查：

- 数值、类别/系列、单位、统计对象、衍生计算与来源；不能只检查图上的几个大数字。
- 条形图的零轴、线性刻度、正负方向、条长及类别顺序；小值不能被画成与大值接近的长条。截断轴必须符合已确认表达且显著说明，不能静默截断来夸大差异。
- 饼/环形图的扇区比例、总和及图例对应；折线等图检查每个点的坐标与真实时间/类别顺序。非线性尺度按已确认设计另行检查。
- 整页是否多出了 Page Spec 未声明的数据视觉，包括没有数字标签的曲线、散点、坐标轴或趋势箭头。概念图和研究设想不能画成已观测的结果；用机制示意、问题—数据—检验关系表达，并保留假设标记。

普通交付在规格中记录检查结论；完整评测分别填写 v1.2 数据检查项与每页数据视觉清单。脚本验证记录，不具备视觉识别能力，不能代替真正看图。

## 重试停止条件

同一图表几何问题初次检查失败后，最多再做一次针对性生图修复，可提供按真实数据绘制的独立参考图；连续两次检查失败就停止同类生图重试。

对支持的线性、零基线、单系列或分组水平条形图/竖直柱状图，可用 `build_chart_image.py` 先生成精确独立图表参考，或在宿主授权允许时替换精确区域；其他图型使用可靠绘图工具，或明确尚未解决的限制。先看清要替换的矩形和需要保留的类别、单位、图例、正文，避免覆盖旁边内容。

程序替换受宿主工具权限约束：若当前生图工具要求用户明确授权程序改图，确认现有授权是否覆盖本页/本区域；有授权就继续，没有则先做好可审阅的独立图表和替换方案，再请求对应授权。不能把本次局部授权当作以后所有图片编辑的授权。未解决的几何问题不得标为已验收。

替换输出写新文件，保留原图；实际查看修复页，更新 Page Spec 的图片路径/提示词及修复说明，重新生成当前图的内容/几何观察、渲染与评分。构造坐标不是独立看图证据。

## 独立观察的几何核对

`audit_chart_geometry.py` 支持单系列或分组、类别唯一、零基线的水平条形图和竖直柱状图。它用两处实际观察到的轴值/像素锚点计算线性尺度，再比对每根条的起点/终点；水平数值轴须向右递增、竖直数值轴须向上递增。不做 OCR、自动找条或来源核验。堆叠、对数轴、饼图等仍需相应视觉检查，不可声称该脚本已验证。

分组图要求系列名称非空且唯一；观察按类别优先、系列次序填写，每根条增加 `series` 字段，不能用另一系列的条代替。旧单系列观察格式保持兼容。布局可用 `series_colors` 指定系列颜色；图例须留在绘图区上方。正、负、零值共用同一零轴。`construction_geometry` 的 `coordinate_space` 区分独立图表的区域坐标与替换后的整页坐标，它仍不是实际观察。两种分组图的布局与命令示例见 `examples/data-update/`。

Page Spec 图表 `data` 使用 `chart_type`、`categories`、`series[].values`；可记录 `baseline: 0`。生成当前图片的观察模板：

```sh
python scripts/audit_chart_geometry.py work/page-spec.json work/chart-observations.json --init
```

打开当前页面，用实际图片像素坐标填写 `axis` 两个锚点；水平图取 x 坐标，竖直图取 y 坐标。按类别顺序记录 `bars[].start/end`，真正测量后将状态改为 `complete`。例如：

```json
{
  "slide_id": "s04", "element_id": "growth-chart",
  "image_sha256": "current image hash", "status": "complete",
  "axis": [{"value": -6, "pixel": 258}, {"value": 4, "pixel": 1088}],
  "bars": [{"category": "轨道", "start": 756, "end": 1022}]
}
```

顶层 `version: 1.0` 和 `page_spec_sha256`、图的 `image_sha256` 由模板填入。上例只演示一根条，实际必须覆盖全部类别。默认像素容差 2.5；允许按测量分辨率调整到 0–10 像素，不能调大容差掩盖明显错误。

```sh
python scripts/audit_chart_geometry.py work/page-spec.json work/chart-observations.json --output output/chart-geometry.json
```

可用 `--slide s04` 只检查指定页。缺失/待测记录保持 `incomplete`，比例或方向错误为 `fail`；图片或 Page Spec 已变更的旧记录会被拒绝。`--chart-observations` 可将此检查纳入交付评分。

## 精确水平条形区域

`build_chart_image.py` 从 Page Spec 直接读取真实数据。布局文件示例（像素坐标）：

```json
{
  "slide_id": "s04", "element_id": "growth-chart",
  "region": [100, 100, 850, 450], "plot": [150, 30, 600, 330],
  "axis_min": -8, "axis_max": 5, "ticks": [-8, -4, 0, 5],
  "font": "C:/Windows/Fonts/msyh.ttc", "font_size": 20,
  "decimals": 1, "signed": true, "suffix": "%",
  "show_categories": true,
  "background": "#FFFFFF", "positive_color": "#9582DE",
  "negative_color": "#B8A8E2", "text_color": "#242638", "grid_color": "#DED9EF"
}
```

`region` 为整页 `[x,y,w,h]` 整数矩形；`plot` 为该矩形内部 `[x,y,w,h]`。颜色、字体、刻度和数值精度应符合锁定风格，字体需覆盖当前文字。保留原页类别标签时设 `show_categories: false`，替换区域仍必须覆盖旧条形、零轴和刻度。留足标签空间，溢出会拒绝导出；不自动缩小字或改写数值。

先输出独立参考区域，无需修改页面：

```sh
python scripts/build_chart_image.py work/page-spec.json work/chart-layout.json output/chart-reference.png
```

允许替换时，在布局中增加当前原图的 `source_sha256` 后执行：

```sh
python scripts/build_chart_image.py work/page-spec.json work/chart-layout.json slides/04-fixed.png --replace-region --report output/chart-repair.json
```

只修改该矩形，输出为 PNG，矩形外解码像素保持一致；不覆盖原图。报告绑定输入/输出哈希，记录构造坐标供复现，不能直接复制它作为独立观察记录。圆环、复杂渐变背景或其他图型不在此兜底脚本的支持范围。
