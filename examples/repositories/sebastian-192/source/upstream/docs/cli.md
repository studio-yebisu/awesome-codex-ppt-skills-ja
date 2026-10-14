# 统一命令与环境诊断

[首页](../README.md) · [English](cli.en.md)

`slidemuse.py` 是现有本地工具的统一入口，支持 Python 3.10+。在仓库或安装的 Skill 根目录运行；也可以从其他目录传入入口的完整路径。任务路径保持相对于当前工作目录。

```sh
python slidemuse.py --help
python slidemuse.py --version
python slidemuse.py doctor
```

入口优先使用自身目录下的 `.venv/Scripts/python.exe`（Windows）或 `.venv/bin/python`（其他平台），否则使用当前解释器。路径从当前安装位置计算，搬移目录后不依赖旧 `.skill-python` 路径；虚拟环境本身仍需与操作系统及基础 Python 兼容。无需激活环境或安装 uv、pipx、新 Python 库。

## 常用命令

| 命令 | 原有工具 | 用途 |
|---|---|---|
| `init task --mode editable` | `scripts/init_deck.py` | 从已准备的规格生成任务，拒绝覆盖配置 |
| `check task/job.json task-output` | `scripts/run_deck.py --check` | 只读预检 |
| `run task/job.json task-output` | `scripts/run_deck.py` | 编译、渲染、评分或接续任务 |
| `render deck.pptx previews` | `scripts/render_deck.py` | 生成真实渲染预览 |
| `validate page-spec.json --strict` | `scripts/validate_page_spec.py` | 验证规格 |
| `audit deck.pptx --scene scene.json` | `scripts/audit_editability.py` | 检查原生对象 |
| `review task/job.json task-output` | `scripts/review_panel.py` | 生成审阅面板或导入记录 |
| `sample --verify --output sample-output` | `showcase/editable-irena/reproduce.py` | 重建公开样板的六套 PPTX |

为表内命令添加 `python slidemuse.py` 前缀。各命令的参数原样交给对应脚本，`<命令> --help` 展示其原有帮助。其他高级工具仍可直接运行 `scripts/*.py`；安装版直接调用脚本时，使用 `.skill-python` 所记录的解释器或当前安装目录下的 `.venv` Python。

流水线原有退出码保持不变：0 表示本次命令成功（也可能只是保存了请求阶段），1 表示检查失败或输入阻塞，3 表示等待审阅。参数错误通常返回 2。`check` 只读，不会创建工作目录或批准素材；`run` 的 `--stop-after`、`--status` 等选项仍由原脚本解释。内容确认、风格选择和逐页视觉检查仍按 Skill 契约执行。

## 排查环境

```sh
python slidemuse.py doctor --json
python slidemuse.py doctor --require-renderer --backend powerpoint
```

诊断不安装软件、不联网、不启动 PowerPoint、不写入任务文件。它检查 Python 是否达到 3.10，以及依赖是否安装、满足最低版本、能够导入。导入探测每包最多 15 秒，缺少或损坏的依赖返回失败和修复命令。后端检查包括 PowerPoint 的 Windows 注册与 PowerShell，或 LibreOffice 和 Poppler 的 PATH；发现程序不等于真实渲染成功。

目前支持仓库的 `包名>=数字版本` 依赖格式；不确定的预发布版本或未来新增的未支持约束明确返回失败。默认缺少渲染器返回 `warning` 和退出码 0，便于仅做规格检查或编译；指定 `--require-renderer` 后缺少所选后端返回 `fail` 和退出码 1。参数错误返回 2。JSON 包含 `schema_version`、`skill_version`、`status`、`python`、`skill_root` 和逐项 `checks`。

如果隔离环境的 Python 本身无法启动，可使用已知可运行的 Python 执行 `python scripts/doctor.py --json`，诊断该解释器；隔离环境需通过重新运行仓库安装器修复。提交问题前检查日志中的本地路径并脱敏。

诊断不探测宿主 Agent 的读材料、视觉理解或生图能力。样板复现从已批准图片与结构化输入开始，不能证明宿主生图可用。
