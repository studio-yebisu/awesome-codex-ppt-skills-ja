# Scene v1：可编辑场景协议

[机器 schema](scene.schema.json)

## 单一来源

scene.json 保存可编辑内容和版面；assets/ 保存视觉素材。重新生成 PPTX 时不再调用生图。
原始图片只供核对，用 slide.source_image 记录；编译器不会自动把它放进幻灯片。

有讲稿时沿用 Page Spec 的 `speaker_notes`，编译传 `--page-spec` 核对上游。新字段优先于 Scene 旧 `notes`（历史演讲备注）；不要把工作日志当讲稿。对象审查会核对实际备注，见[讲稿保留](speaker-notes.md)。

Step 2 的 `page-spec.json` 是上游语义契约，保存已确认文字、数据、来源和稳定 ID；Scene 必须沿用这些 ID 和内容，再补齐精确坐标、原生样式与实际素材路径。按[变更记录](workflow-updates.md)区分已授权修改和未知图文冲突；只对未知冲突请求确认，不得以图片 OCR 静默覆盖 Page Spec。

```json
{
  "version": "1.0",
  "title": "示例",
  "canvas": {"width": 1600, "height": 900, "width_inches": 13.333333},
  "slides": [{
    "id": "s01",
    "background": "#FFFFFF",
    "elements": [{
      "id": "title", "type": "text",
      "x": 100, "y": 80, "w": 1400, "h": 100,
      "text": "文字可以编辑", "font": "Microsoft YaHei", "font_size": 36
    }]
  }]
}
```

## 坐标、路径和层级

- 坐标是 canvas 像素，使用左上角 x/y 与宽高 w/h；不是归一化 0–1。
- 字号、线宽、文本框 margin 使用 PowerPoint pt。导出按画布换算，字号不会再按像素缩放。
- 整个 PPTX 只有一种比例。width_inches 默认 13.333333，高度按比例计算。
- 所有路径相对 scene.json 所在目录，必须位于该目录内；素材只支持 PNG/JPEG。
- 每页 ID 唯一，每页所有元素（包含组合内）ID 唯一。ID 用字母、数字、点、下划线或短横线。
- 数组从后向前绘制。group.children 采用整页坐标，不能用组内相对坐标；嵌套组合也相同。
- PowerPoint 选择窗格显示 `id | name`，audit 用 ID 比较对象。
- 图片 fit 默认 contain（保留比例）；cover 居中裁剪；stretch 仅在明确接受变形时使用。
- 每个元素可带 source、confidence、note，供记录与审查。confidence < 0.85 产生警告。
- rotation 支持普通 bbox 元素，旋转后越界需渲染核验；line 用两个端点定义。

## 类型

| type | 必填 | 可选 |
|---|---|---|
| text | id, type, x,y,w,h,text | font,font_size,color,bold,italic,align,valign,margin,line_spacing,rotation |
| shape | id,type,x,y,w,h,shape | fill,line,line_width,rotation |
| line | id,type,x1,y1,x2,y2 | color,line_width,arrow: none/end/both |
| image | id,type,x,y,w,h,path | fit,role: asset/background/reference,rotation |
| group | id,type,children | name |
| table | id,type,x,y,w,h,rows | column_widths,header,header_fill,header_color,fill 及文字样式 |
| chart | id,type,x,y,w,h,chart_type,categories,series | legend,data_labels,number_format,font,font_size,rotation |

颜色格式 #RRGGBB，shape 的 fill/line 可设 null 表示无填充/无边框。
shape 支持 rect、roundRect、ellipse、triangle、diamond、chevron、rightArrow。
`roundRect` 可设置 `corner_radius`（0–0.5 的 Office 调整值，非像素半径），其他形状不能使用。
文本 align 为 left/center/right；valign 为 top/middle/bottom。
文本换行写 \n。富文本分段样式暂未实现，必要时拆成多个稳定命名的文本框。

table.rows 为二维字符串数组，所有行列数一致；列宽是正数权重。
本版不支持合并单元格；复杂表格需扩展实现或记录限制。
chart_type 支持 column/bar/line/pie/doughnut。
series 为 [{name, values, color?}]，数值数量匹配 categories。
pie/doughnut 只接受单组非负且总和大于 0 的数据。原生图表包含可编辑工作簿。
不支持的统计图不可谎称已实现，可用独立图片保真并说明数据不可编辑。

图表可设置 `value_axis_min`、`value_axis_max`、`major_gridlines`、`major_gridline_color`、`tick_label_color` 和 `data_label_color`，导出后由对象审查核对。前五项只适用于有坐标轴的图表；网格线颜色会自动启用主网格线，`data_label_color` 要求 `data_labels: true`。其他 Scene v1 未表达的图表外观若用后处理调整，必须随交付保存可复现脚本，并说明单独编译 Scene 无法完全还原这些设置。后处理完成后重新执行对象审查和实际渲染；不要将未支持的属性写入 Scene。

从 2.8.0 起以下外观也由 Scene 编译与审查，无需后处理：

|设置|范围与用途|
|---|---|
|`data_label_position`|`outside_end`、`inside_end`、`center`、`above`、`below`、`best_fit`；需 `data_labels: true`，按图型选择并实际渲染检查|
|`data_label_font_size`|正数 pt；需启用数据标签|
|`category_axis_visible`、`value_axis_visible`|有轴图表的轴/刻度标签可见性|
|`category_reverse_order`|有轴图表的类别顺序|
|`gap_width`|条形/柱状图的类别间距百分比，整数 0–500|
|`series[].point_colors`|与类别等长的颜色数组；可用于各类别/扇区配色|
|`series[].invert_if_negative`|仅条形/柱状图；显式控制系列及各数据点的负值反色，`false` 保持指定颜色|
|`hole_size`|仅环形图，孔径百分比，整数 10–90|
|`first_slice_angle`|饼/环形图起始角度，整数 0–360|
|`plot_layout`|`{x,y,w,h}` 为外部图表框内的归一化内绘图区，全部 0–1，宽高正数且不能越界；为外侧标签预留空间|

这些设置只保证原生对象配置可复现，不代替 PowerPoint/LibreOffice 渲染核对。修改数据后仍需检查标签和原图差异。

## 检查和局部修改

按[变更与恢复规则](workflow-updates.md)记录基准版本、修改授权与失效图片，再同步 Page Spec，修改 ID 对应的文字、数据、几何或 path，重新运行 build_editable_ppt.py。
导出失败不会替换既有 PPTX。先执行完整 schema 和素材检查，再写文件。
audit 的 --strict 将所有警告视为失败，适合无复杂栅格/低置信度项的用例。
使用背景图片的合法案例仍可能产生警告；记录人工判断，不要改小 bbox 来规避检查。
审查包括图片的 contain/cover/stretch 实际位置、尺寸、裁切与翻转，以及嵌套组合的父子坐标变换和旋转。它仍只对照 Scene 声明的对象，不能证明 Page Spec 到 Scene 无遗漏或视觉完全一致。
