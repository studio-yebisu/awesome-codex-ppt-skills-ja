# PPT Scene Graph — OpenClaw Skill  v2.0.0

> PowerPoint 视觉场景图 + 统一生产流水线  
> Visual Scene Graph for PowerPoint + Unified Production Pipeline

🌐 [中文](#中文) · [English](#english)

---

## 中文

PowerPoint 视觉场景图 + 统一生产流水线

让 AI 看到并理解幻灯片布局，同时提供完整的美化/创建能力。

### 🎯 核心能力

| 能力 | 说明 | 状态 |
|------|------|------|
| 🎨 **PPT 美化** | 一键应用设计主题，自动调整字体/颜色/间距 | ✅ |
| 🏗️ **从零创建** | 基于大纲 YAML/JSON 自动生成完整演示文稿 | ✅ |
| 🔍 **场景图解析** | 提取元素树、空间关系、布局模式 | ✅ |
| 📊 **质量评估** | 评分 PPT 设计质量（对比度、对齐、一致性） | ✅ |
| 🎯 **智能检测** | 自动识别封面/章节/内容/结尾等幻灯片类型 | ✅ |

### ✨ 设计系统（内置主题）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `designhub_warm` | 温暖希望系（奶油白 + 暖红 + 生命绿） | 学生/公众演讲、情感叙事 |
| `designhub_pro` | 专业商务系（深蓝 + 金） | 企业汇报、商务演示 |
| `projection` | 投影优化系（高对比度、大字体） | 大型会场投影 |

### 🚀 快速开始

#### 安装（OpenClaw Skill）

```bash
# 方式1：复制到 skills 目录
cp -r ppt-scene-graph-opensource ~/.qclaw/skills/ppt-scene-graph

# 方式2：符号链接（开发模式）
ln -s $(pwd)/ppt-scene-graph-opensource ~/.qclaw/skills/ppt-scene-graph
```

#### 使用

**1. 美化现有 PPT**

```python
from ppt_scene_graph import beautify

# 使用默认主题美化
beautify("input.pptx", theme="designhub_warm", output_path="output.pptx")

# 不添加页码
beautify("input.pptx", add_page_numbers=False)
```

**2. 从大纲创建 PPT**

```python
from ppt_scene_graph import create_from_outline
from ppt_scene_graph.pipeline import SlideSpec, OutlineSpec

outline = OutlineSpec(
    title="我的演示",
    subtitle="副标题",
    slides=[
        SlideSpec(type='cover', title="封面标题", subtitle="封面副标题"),
        SlideSpec(type='section', title="1. 第一章"),
        SlideSpec(type='content', title="内容页", body=["要点1", "要点2", "要点3"]),
        SlideSpec(type='ending', title="谢谢", subtitle="Q&A"),
    ]
)

create_from_outline(outline, theme="designhub_warm", output_path="output.pptx")
```

**3. 解析场景图**

```python
from ppt_scene_graph import parse_slide

slide_data = parse_slide("presentation.pptx", slide_idx=0)
print(slide_data)
# {
#     "elements": [...],
#     "relations": [...],
#     "layout_pattern": "two_column"
# }
```

**4. 评估 PPT 质量**

```python
from ppt_scene_graph import evaluate

report = evaluate("presentation.pptx")
print(report)
# {
#     "total_score": 85,
#     "contrast_ratio": "PASS",
#     "alignment": "GOOD",
#     ...
# }
```

### 🛠️ CLI 使用

```bash
# 美化
python -m ppt_scene_graph.pipeline beautify input.pptx -t designhub_warm -o output.pptx

# 创建
python -m ppt_scene_graph.pipeline create --outline outline.json -o output.pptx

# 评估
python -m ppt_scene_graph.pipeline evaluate input.pptx
```

### 📂 项目结构

```
ppt-scene-graph-opensource/
├── ppt_scene_graph/              # 核心 Python 包
│   ├── __init__.py              # 导出 API + vendor 路径设置
│   ├── pipeline.py              # 美化/创建/评估流水线
│   ├── design.py                # DesignSystem 设计系统
│   └── vendor/                 # Vendored 依赖
│       ├── __init__.py
│       └── pptx/               # python-pptx 源码（MIT）
├── scripts/                     # OpenClaw 调用脚本
│   ├── beautify.py
│   ├── create.py
│   └── evaluate.py
├── SKILL.md                     # OpenClaw Skill 定义
├── README.md                    # 本文件
├── DESCRIPTION.txt              # 简短描述（347 字符）
└── LICENSE                      # MIT License
```

### 🔧 技术细节

**Vendor 机制**

`python-pptx` (MIT) 已完整 vendor 到 `ppt_scene_graph/vendor/pptx/`，无需外部安装。

原理：`ppt_scene_graph/__init__.py` 中添加 vendor 路径到 `sys.path`，使 `from pptx import ...` 指向 vendored 版本。

**设计系统**

`design.py` 定义 `DesignSystem` dataclass，包含：
- 颜色（`bg`, `text_title`, `primary`, `secondary`, `accent` 等）
- 字体（`font_title`, `font_body`）
- 间距（`margin_left`, `margin_top` 等）
- 装饰（`left_bar_width`, `top_line_height`）

**技能调用**

OpenClaw 通过 `scripts/beautify.py` 等包装脚本调用 `pipeline.py` 中的 `beautify()`, `create_from_outline()`, `evaluate()`。

### 📞 联系方式

- GitHub Issues: https://github.com/eluckydog/ppt-scene-graph/issues
- OpenClaw Skill: 集成后可通过 OpenClaw agent 调用

---

## English

Visual Scene Graph for PowerPoint + Unified Production Pipeline

Let AI see and understand slide layouts, while providing complete beautification/creation capabilities.

### 🎯 Core Capabilities

| Capability | Description | Status |
|------------|-------------|--------|
| 🎨 **PPT Beautification** | One-click design theme application, auto-adjust fonts/colors/spacing | ✅ |
| 🏗️ **Create from Scratch** | Auto-generate complete presentations from YAML/JSON outlines | ✅ |
| 🔍 **Scene Graph Parsing** | Extract element trees, spatial relationships, layout patterns | ✅ |
| 📊 **Quality Evaluation** | Score PPT design quality (contrast, alignment, consistency) | ✅ |
| 🎯 **Smart Detection** | Auto-detect slide types (cover/section/content/ending) | ✅ |

### ✨ Design System (Built-in Themes)

| Theme | Style | Use Case |
|-------|-------|----------|
| `designhub_warm` | Warm Hope (Creamy White + Warm Red + Life Green) | Student/Public Speaking, Emotional Narratives |
| `designhub_pro` | Professional Business (Deep Blue + Gold) | Corporate Reports, Business Presentations |
| `projection` | Projection Optimized (High Contrast, Large Fonts) | Large Venue Projections |

### 🚀 Quick Start

#### Installation (OpenClaw Skill)

```bash
# Method 1: Copy to skills directory
cp -r ppt-scene-graph-opensource ~/.qclaw/skills/ppt-scene-graph

# Method 2: Symbolic link (development mode)
ln -s $(pwd)/ppt-scene-graph-opensource ~/.qclaw/skills/ppt-scene-graph
```

#### Usage

**1. Beautify Existing PPT**

```python
from ppt_scene_graph import beautify

# Beautify with default theme
beautify("input.pptx", theme="designhub_warm", output_path="output.pptx")

# Without page numbers
beautify("input.pptx", add_page_numbers=False)
```

**2. Create PPT from Outline**

```python
from ppt_scene_graph import create_from_outline
from ppt_scene_graph.pipeline import SlideSpec, OutlineSpec

outline = OutlineSpec(
    title="My Presentation",
    subtitle="Subtitle",
    slides=[
        SlideSpec(type='cover', title="Cover Title", subtitle="Cover Subtitle"),
        SlideSpec(type='section', title="1. Chapter One"),
        SlideSpec(type='content', title="Content Page", body=["Point 1", "Point 2", "Point 3"]),
        SlideSpec(type='ending', title="Thank You", subtitle="Q&A"),
    ]
)

create_from_outline(outline, theme="designhub_warm", output_path="output.pptx")
```

**3. Parse Scene Graph**

```python
from ppt_scene_graph import parse_slide

slide_data = parse_slide("presentation.pptx", slide_idx=0)
print(slide_data)
# {
#     "elements": [...],
#     "relations": [...],
#     "layout_pattern": "two_column"
# }
```

**4. Evaluate PPT Quality**

```python
from ppt_scene_graph import evaluate

report = evaluate("presentation.pptx")
print(report)
# {
#     "total_score": 85,
#     "contrast_ratio": "PASS",
#     "alignment": "GOOD",
#     ...
# }
```

### 🛠️ CLI Usage

```bash
# Beautify
python -m ppt_scene_graph.pipeline beautify input.pptx -t designhub_warm -o output.pptx

# Create
python -m ppt_scene_graph.pipeline create --outline outline.json -o output.pptx

# Evaluate
python -m ppt_scene_graph.pipeline evaluate input.pptx
```

### 📂 Project Structure

```
ppt-scene-graph-opensource/
├── ppt_scene_graph/              # Core Python package
│   ├── __init__.py              # Export API + vendor path setup
│   ├── pipeline.py              # Beautify/Create/Evaluate pipeline
│   ├── design.py                # DesignSystem design system
│   └── vendor/                 # Vendored dependencies
│       ├── __init__.py
│       └── pptx/               # python-pptx source code (MIT)
├── scripts/                     # OpenClaw call scripts
│   ├── beautify.py
│   ├── create.py
│   └── evaluate.py
├── SKILL.md                     # OpenClaw Skill definition
├── README.md                    # This file
├── DESCRIPTION.txt              # Brief description (347 chars)
└── LICENSE                      # MIT License
```

### 🔧 Technical Details

**Vendor Mechanism**

`python-pptx` (MIT) is fully vendored into `ppt_scene_graph/vendor/pptx/`, no external installation needed.

Principle: `ppt_scene_graph/__init__.py` adds vendor path to `sys.path`, making `from pptx import ...` point to vendored version.

**Design System**

`design.py` defines `DesignSystem` dataclass, containing:
- Colors (`bg`, `text_title`, `primary`, `secondary`, `accent`, etc.)
- Fonts (`font_title`, `font_body`)
- Spacing (`margin_left`, `margin_top`, etc.)
- Decorations (`left_bar_width`, `top_line_height`)

**Skill Invocation**

OpenClaw calls `beautify()`, `create_from_outline()`, `evaluate()` in `pipeline.py` via wrapper scripts like `scripts/beautify.py`.

### 📞 Contact

- GitHub Issues: https://github.com/eluckydog/ppt-scene-graph/issues
- OpenClaw Skill: Can be invoked via OpenClaw agent after integration

---

## License (双语 / Bilingual)

MIT License

---

**Skill 化完成 / Skill-ified**: v2.0.0  
**维护者 / Maintainer**: OpenClaw Agent (ux-workshop)  
**原始项目 / Original**: [eluckydog/ppt-scene-graph](https://github.com/eluckydog/ppt-scene-graph)
