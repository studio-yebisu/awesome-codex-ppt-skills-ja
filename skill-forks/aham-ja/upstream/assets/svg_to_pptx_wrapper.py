# -*- coding: utf-8 -*-
"""
svg_to_pptx_wrapper.py — V4.0 对外统一入口

将 SVG 文件列表转换为原生可编辑的 PPTX。
底层调用 ppt-master 的 svg_to_pptx 工具链(见 svg_to_pptx/ 目录)。

使用示例:
    from svg_to_pptx_wrapper import svg_to_native_pptx
    from pathlib import Path

    svg_files = sorted(Path('svg_final').glob('*.svg'))
    svg_to_native_pptx(svg_files, Path('output.pptx'))

核心保证:
- 每个 SVG 元素 → 独立的 PPT 原生形状(不是图片嵌入)
- 所有文字都是可编辑的 textbox
- 矩形、圆、线条都是 PPT 原生 shape,可单独选中、改色、改边框
- 多边形(如梯形)通过 custGeom 实现,仍是可编辑形状
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional


def svg_to_native_pptx(
    svg_files: list[Path],
    output_path: Path,
    canvas_format: str = 'auto',
    verbose: bool = True,
    notes: Optional[dict[str, str]] = None,
) -> bool:
    """
    将 SVG 文件列表转换为原生可编辑的 PPTX。

    Args:
        svg_files: SVG 文件路径列表(按顺序对应 PPT 的各页)
        output_path: 输出 PPTX 路径
        canvas_format: 画布格式。默认 'auto' 会从 SVG 的 viewBox 自动推导画布尺寸,
                      保证内容不被裁切。其他可选值:
                        - 'ppt169' (强制 1280×720 · 16:9)
                        - None (同 'auto')
        verbose: 是否输出转换日志
        notes: 可选的讲稿字典,key 为 SVG stem,value 为 markdown 讲稿

    Returns:
        bool: 全部转换成功返回 True,有失败返回 False

    关键参数说明:
        - use_native_shapes=True:启用原生 DrawingML 形状模式(而不是 SVG 图片嵌入)
        - use_compat_mode=False:不生成 PNG 后备(纯矢量)
        - transition=None:不添加页面切换动画(切换动画能力已下线)
    """
    # 'auto' 等价于 None,触发底层 viewBox 自动检测
    if canvas_format == 'auto':
        canvas_format = None

    # 确保能找到底层工具链
    wrapper_dir = Path(__file__).parent
    if str(wrapper_dir) not in sys.path:
        sys.path.insert(0, str(wrapper_dir))

    from svg_to_pptx.pptx_builder import create_pptx_with_native_svg


    # 转换为 Path 对象(以防传入的是字符串)
    svg_files = [Path(p) if not isinstance(p, Path) else p for p in svg_files]
    output_path = Path(output_path) if not isinstance(output_path, Path) else output_path

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    return create_pptx_with_native_svg(
        svg_files=svg_files,
        output_path=output_path,
        canvas_format=canvas_format,
        verbose=verbose,
        transition=None,
        use_compat_mode=False,
        enable_notes=bool(notes),
        notes=notes,
        use_native_shapes=True,
    )


if __name__ == '__main__':
    # CLI 测试入口
    import argparse

    parser = argparse.ArgumentParser(
        description='SVG 批量转原生可编辑 PPTX(V4.0)'
    )
    parser.add_argument('svg_dir', type=str, help='SVG 文件目录')
    parser.add_argument('output', type=str, help='输出 .pptx 路径')
    parser.add_argument('--format', default='ppt169', help='画布格式')
    args = parser.parse_args()

    svg_files = sorted(Path(args.svg_dir).glob('*.svg'))
    if not svg_files:
        print(f"[Error] 目录 {args.svg_dir} 下无 SVG 文件")
        sys.exit(1)

    ok = svg_to_native_pptx(svg_files, Path(args.output))
    sys.exit(0 if ok else 1)
