# 蓝图风格三页实战验收 / Three-slide acceptance

日期：2026-09-18。环境：Windows、Python 3.13、Microsoft PowerPoint；图像由宿主 image_gen 生成，未暴露具体模型。本记录描述本地验收结果，不代表远端 CI 或发布已完成。

## 结果

- 用户确认三页大纲并选择方案 3：封面、合成监测数据、监测终端。
- 四套当前候选通过结构检查；历史修订稿不作为新增方案。缩略网格仍需人工视觉检查。
- 用已有长图完成本地裁切排版，并从最终 PPT 渲染生成缩略总览；这两项本地操作均未调用生图。
- 三页图片版按 Page Spec 清单导出，并用 PowerPoint 打开及渲染。
- 可编辑版的文字为文本框，柱形图含原生数据工作簿，终端为独立透明 PNG。
- 第三天由 24 改为 30，图表缓存和内嵌工作簿均核对为 12、18、30；其他两页渲染保持一致。
- 移动测试只改变终端对象的横坐标（左移 200 画布像素）；渲染检查未发现原位置残影。
- 三个可编辑测试文件的结构审查均无错误。大幅栅格警告保留，并人工核对清理后的背景。
- 133 项自动测试通过；Ruff、严格 Page Spec 示例验证及技能入口检查通过。

## 已知边界

- 复杂山体、人物、图标仍为栅格；独立终端可以移动，但内部线条不是原生矢量。
- AI 补全背景与终端细节不保证逐像素复原；采用微软雅黑近似字体，原图斜线柱形填充改为实色。
- 更新版纵轴上限由 30 改为 40，以留出数据标签空间。
- 本次图表透明底、轴范围、网格线及标签颜色由任务内可复现后处理脚本设置。Scene v1 尚未表达全部这些样式，仅重编 Scene 不保证外观一致。后处理脚本随交付保存，不能把该能力宣传为 Scene 已原生支持。
- 本次历史预览包含错误长图和额外修订，不能把实际累计生图消耗称为四次。更新后的正常流程目标才是每套直接生成一张总览、四套四次；内容错误仍可能需要额外调用。
- 缩略图尺寸本身不保证宿主按更低额度计费；节省来自减少不必要的生成调用。

验收文件保存在独立任务目录，未把用户任务文件自动加入公开作品集。仓库中只保存此结果记录。

## English

The local three-slide blueprint trial passed image export, real PowerPoint rendering, native chart/workbook updates (24 to 30), and independent terminal movement without a ghost at its original location. All 133 tests passed, along with Ruff, strict Page Spec example validation and skill entrypoint validation.

Thumbnail layout used existing images locally with zero image-generation calls. The earlier exploratory run included retries; four calls is the updated normal preview workflow, not a claim about that run's total usage or provider billing.

Complex artwork remains raster, and AI reconstruction and font substitution are not pixel-exact. This trial used a task-local reproducible chart postprocessor; later Scene support covers value-axis bounds, major gridlines, and tick/data-label colors, while other unsupported chart settings still require the postprocessor. Preserve it with the delivery. These are local acceptance results, not a remote CI result or a published release.
