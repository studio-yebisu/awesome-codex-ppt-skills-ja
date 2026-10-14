# 生图后端与 GPT Image 2.5 接入说明

核验日期：2026-09-16。实际可用性取决于账号和宿主工具。

## 项目推荐

本项目的最佳推荐组合是 **Codex + GPT Image 2.5**：Codex 负责材料读取、状态机编排、文件与脚本操作，GPT Image 2.5 负责风格总览、逐页成品、主体分离和背景修复。
这是一项项目工作流建议，不是跨平台性能基准。

本技能也可在其他 Agent 中运行。进入需要生图或图片编辑的阶段时，必须调用该 Agent 自身提供或已经连接的图像能力；不要寻找 Codex 专属工具名，也不要把本地脚本当作生图模型。

| 角色 | 官方模型 ID | 本技能建议 |
|---|---|---|
| 快速视觉探索 | `gpt-image-2.5-flare` | 方案预览、素材初稿 |
| 精确参考编辑 | `gpt-image-2.5-sunburst` | 主体分离、复杂背景补全、最终资产 |

官方支持透明 PNG/WebP，以及自定义尺寸；16:9 可采用 `1536x864`。
编辑型素材需要真正的 alpha 通道，棋盘格画在像素里不是透明。
来源：[图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)、
[Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)。

## 宿主原生工具

Codex/ChatGPT 的生图能力与直接 API 不同。先读取当前工具 schema：
- 只有暴露模型、尺寸、背景参数时才直接设置。
- 只接受提示词和参考图时，在提示词写清尺寸意图、透明背景、需要修改和需要保留的内容，生成后检查真实结果。
- 不把 Images API 参数传给不支持的原生工具，不根据 ChatGPT 文本模型名猜生图模型。
- 不因为模型不可用就静默改成其他版本；报告实际使用的后端或“宿主未暴露型号”。

## 可选 API

本仓库不内置 API 客户端，也不会扫描密钥或发起网络请求。用户自行接入 Images API 时可采用以下请求配置；它不是本地脚本输入：

```json
{
  "model": "gpt-image-2.5-sunburst",
  "prompt": "An isolated botanical illustration, no text, transparent background.",
  "size": "1536x864",
  "quality": "high",
  "background": "transparent",
  "output_format": "png"
}
```

生成与参考图编辑使用不同请求形式；编辑时按官方接口传入参考图文件。
输出通常需要从响应中解码保存，并检查像素尺寸、alpha 与裁切后再写入 scene。
新版本参数若不确定，重新核验官方文档，不沿用旧型号限制。

## 任务提示设计

这是本项目的工作建议：
- 分开描述目标素材、构图、视觉规范、需改区域与保留项。
- 所有分层编辑以同一张原始页面为参考，避免反复编辑上一轮结果造成漂移。
- 背景补全明确移除将独立重建的所有文字和主体，包含阴影/倒影的归属。
- 精确文字、数据和几何使用原生 PPT 对象，避免依靠生图准确度。
- Step 1 先通过内容大纲确认，再按风格门禁生成四套幻灯片浏览视图；Step 2 逐页验收，不自动尝试所有型号。
