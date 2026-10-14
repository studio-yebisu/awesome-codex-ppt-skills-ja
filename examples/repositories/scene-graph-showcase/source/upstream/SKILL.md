---
name: ppt-scene-graph
description: "PPT 视觉场景图 + 美化/创建流水线。从 PPTX 提取结构化布局数据（元素树、空间关系、布局模式），并提供一键美化、从大纲创建演示文稿能力。内置 DesignHub 设计系统，支持多种主题。完全独立，无需外部 python-pptx 依赖（已 vendor）。"
version: 2.0.0
license: MIT
---

# PPT Scene Graph — OpenClaw Skill

Visual Scene Graph for PowerPoint + Unified Production Pipeline

让 AI 看到并理解幻灯片布局，同时提供完整的美化/创建能力。

---

## 核心能力

| 能力 | 说明 | 状态 |
|------|------|------|
| 🎨 **PPT 美化** | 一键应用设计主题，自动调整字体/颜色/间距 | ✅ |
| 🏗️ **从零创建** | 基于大纲 YAML/JSON 自动生成完整演示文稿 | ✅ |
| 🔍 **场景图解析** | 提取元素树、空间关系、布局模式 | ✅ |
| 📊 **质量评估** | 评分 PPT 设计质量（对比度、对齐、一致性） | ✅ |
| 🎯 **智能检测** | 自动识别封面/章节/内容/结尾等幻灯片类型 | ✅ |

---

## 设计系统（内置主题）

| 主题 | 风格 | 适用场景 |
|------|------|----------|
| `designhub_warm` | 温暖希望系（奶油白 + 暖红 + 生命绿） | 学生/公众演讲、情感叙事 |
| `designhub_pro` | 专业商务系（深蓝 + 金） | 企业汇报、商务演示 |
| `projection` | 投影优化系（高对比度、大字体） | 大型会场投影 |

---

## 快速开始

### 1. 美化现有 PPT

```python
from ppt_scene_graph import beautify

# 使用默认主题美化
beautify("input.pptx", theme="designhub_warm", output_path="output.pptx")

# 不添加页码
beautify("input.pptx", add_page_numbers=False)
```

### 2. 从大纲创建 PPT

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

### 3. 解析场景图

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

### 4. 评估 PPT 质量

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

---

## CLI 使用

```bash
# 美化
python -m ppt_scene_graph.pipeline beautify input.pptx -t designhub_warm -o output.pptx

# 创建
python -m ppt_scene_graph.pipeline create --outline outline.yaml -o output.pptx

# 评估
python -m ppt_scene_graph.pipeline evaluate input.pptx
```

---

## 技术架构

### 依赖管理

**✅ 完全独立** — 无需外部 `python-pptx` 依赖

- `python-pptx` (MIT) 已 vendor 到 `ppt_scene_graph/vendor/pptx/`
- 安装 skill 后即可使用，无需 `pip install python-pptx`

### 项目结构

```
ppt-scene-graph-opensource/
├── ppt_scene_graph/
│   ├── __init__.py          # 导出 API + vendor 路径设置
│   ├── pipeline.py          # 美化/创建/评估流水线
│   ├── design.py            # DesignSystem 设计系统
│   └── vendor/             # Vendored 依赖
│       ├── __init__.py
│       └── pptx/           # python-pptx 源码 (MIT)
├── SKILL.md                # OpenClaw Skill 定义
├── README.md               # 使用文档
├── DESCRIPTION.txt         # 简短描述（347 字符）
├── LICENSE                 # MIT License
└── scripts/               # OpenClaw 调用脚本（可选）
    ├── beautify.py
    ├── create.py
    └── evaluate.py
```

---

## 集成到 OpenClaw

### 安装方式

```bash
# 方式1：直接复制到 skills 目录
cp -r ppt-scene-graph-opensource ~/.qclaw/skills/ppt-scene-graph

# 方式2：符号链接（开发模式）
ln -s $(pwd)/ppt-scene-graph-opensource ~/.qclaw/skills/ppt-scene-graph
```

### 在 OpenClaw 中使用

```python
# 在 OpenClaw agent 中调用
from ppt_scene_graph import beautify, create_from_outline, evaluate

# 美化用户上传的 PPT
beautify(upload_path, theme="projection", output_path=output_path)

# 根据用户描述创建 PPT
outline = build_outline_from_user_input(user_prompt)
create_from_outline(outline, output_path=output_path)
```

---

## 设计理念

**This is infrastructure code. It works. Skill-ified and ready to use. If you have questions, just ask the agent.**

### 已完成 Skill 化 (v2.0.0)
- ✅ **完全独立** — `python-pptx` (MIT) 已 vendor 到 `ppt_scene_graph/vendor/pptx/`
- ✅ **零外部依赖** — 安装 skill 后即可使用，无需 `pip install python-pptx`
- ✅ **标准结构** — 包含 `SKILL.md`, `README.md`, `scripts/`, `vendor/`

### 核心原则
- ✅ **规则驱动** — 基于启发式规则，无需模型
- ✅ **可预测** — 确定性的输出，便于调试
- ✅ **投影友好** — 高对比度、大字体、安全的配色方案

### 有问题？
- 📖 读 `README.md`（完整使用文档）
- 🧪 运行 `python test_skill_simple.py`（验证安装）
- 🤖 **直接问智能体**（OpenClaw Agent 已加载此 skill，支持自然语言交互）

---

## 许可证

MIT — 自由使用、修改、分发

---

## 致谢

- **Steve Canny** — `python-pptx` 原作者
- **DesignHub** — 设计系统灵感来源
- **McKinsey/PPTAgent/html-ppt-skill/pptx** — 主题预设聚合来源

---

## 更新日志

### v2.0.0 (2026-05-30)
- 🎉 **Skill 化** — 改造为独立 OpenClaw Skill
- 📦 **Vendor python-pptx** — 移除外部依赖，完全独立
- 📝 **重写文档** — SKILL.md + README.md
- ✨ **保留所有原有功能** — 美化/创建/评估/解析

### v1.0.0 (原始版本)
- 初始版本（基于 python-pptx 外部依赖）
