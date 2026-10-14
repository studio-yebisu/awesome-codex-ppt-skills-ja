# Minimal Markdown 示例

这是一个**最小可跑**示例，用来展示 `thesis-defense-pptx` skill 的核心形态：

1. 从一份很小的 Markdown 论文摘要中抽取答辩内容；
2. 现场生成一个极简 `.pptx` 模板；
3. 在保留模板视觉风格的基础上生成可编辑 `final.pptx`；
4. 运行仓库自带的 `dump_pptx_content.py` 和 `scan_pptx_text.py`；
5. 用纯 Python 渲染一组示意 PNG，并调用 `make_contact_sheet.py` 生成总览图。

> 注意：这个示例故意不依赖 Microsoft PowerPoint，因此 macOS / Linux / Windows
> 都能跑通。真实交付时仍建议在 Windows + PowerPoint 下执行 COM 导出、文字溢出
> 检查和最终人工视觉检查。

## 文件清单

```text
examples/minimal_markdown/
├── README.md
├── thesis.md                 # 极简论文内容
├── build_template.py          # 生成 sample_template.pptx
├── build_deck.py              # 基于模板生成可编辑 final.pptx
├── render_preview.py          # 纯 Python 生成示意 slide PNG
├── run_example.py             # 一键跑完整示例
└── expected/
    ├── generated_overview_01.png # 生成后 slides 1-4 总览图
    ├── generated_overview_02.png # 生成后 slides 5-8 总览图
    ├── detail_slide_01.png     # 封面细节图
    ├── detail_slide_06.png     # 方法页细节图
    └── README.md
```

仓库不直接提交 `sample_template.pptx` / `final.pptx` 等中间产物，它们由脚本现场
生成，避免二进制文件干扰 review。

## 运行

在仓库根目录：

```bash
python examples/minimal_markdown/run_example.py
```

成功后会看到这些产物：

```text
examples/minimal_markdown/
├── sample_template.pptx
├── final.pptx
├── dump.md
├── scan.json
├── rendered_slides/
│   ├── slide_01.png
│   ├── slide_02.png
│   ├── slide_03.png
│   └── slide_04.png
└── contact_sheet.png
```

### 用真实学校模板跑

不传参数时走的是"build_template + build_deck"这条 demo 路径，输出可重现
但视觉简陋。如果你想看 skill 在**真实学校模板**上的效果（也就是仓库里
`expected/generated_overview_01.png` / `expected/generated_overview_02.png`
和两张 detail 图的来源），传一个本地的 `.pptx` 模板路径即可：

```bash
python examples/minimal_markdown/run_example.py \
    --template /path/to/your-real-template.pptx \
    --detail-slides "1,6"
```

`--template` 模式会调用 `build_deck.py --real-template`：

1. 打开真实 `.pptx` 模板，但不清空其中的复杂 shape，避免破坏图片、组合对象
   或嵌入素材的关系；
2. 在模板原生页面上覆盖 `thesis.md` 生成的示例内容，输出真正可编辑的
   `final.pptx`；
3. 对生成后的 `final.pptx` 跑 `dump_pptx_content.py`、`scan_pptx_text.py`、
   PowerPoint COM 导出 PNG 和 `make_contact_sheet.py`。

README 里的图不是模板原页截图；每页右上角都有 `Generated from thesis.md`
标记，用来说明这些页面已经经过 example 生成流程。

模板本身**不**会被 commit（已在 `.gitignore` 里），仅产出落到
`examples/minimal_markdown/`。

## 预览

下面是本示例基于真实模板生成的参考图：

![Generated slides 1-4 overview](expected/generated_overview_01.png)

![Generated slides 5-8 overview](expected/generated_overview_02.png)

![Cover detail](expected/detail_slide_01.png)

![Method-slide detail](expected/detail_slide_06.png)

## 示例覆盖了哪些能力

- `python-pptx` 生成可编辑 PPTX；
- 复制/延续模板配色、字体、顶部导航和卡片式正文布局；
- `pptx_template_tools.py` 的 `add_text` / `add_para` / `tag` / `rect` / `write_table`；
- `dump_pptx_content.py` 导出每页 shape/text/table 清单；
- `scan_pptx_text.py` 检查旧模板词 / 临时填充内容残留；
- `make_contact_sheet.py` 基于导出的 PNG 生成整套 PPT 总览图。

## 和真实工作流的差异

这个最小示例只为了让读者快速跑通仓库脚本。真实毕业论文答辩 PPT 还需要：

- 读取完整论文 PDF/LaTeX 和候选图表；
- 分析用户自己的 `.pptx` 模板；
- 在 Windows + PowerPoint 下导出真实幻灯片 PNG；
- 跑 COM 文字溢出检查；
- 人工检查封面、目录、导航、图表比例、文字密度和学校格式要求。
