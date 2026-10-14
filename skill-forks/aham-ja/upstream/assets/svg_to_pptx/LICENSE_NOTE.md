# SVG to PPTX 工具链 · 来源声明

## 基本信息

- **项目名**:svg_to_pptx
- **来源**:[GitHub hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)
- **License**:MIT License
- **快照日期**:2026-04-17
- **原始路径**:`ppt-master/skills/ppt-master/scripts/svg_to_pptx/`

## 引入这套代码的原因

在 ppt-svg 技能 V4.0 升级过程中,我们验证了 `ppt-master` 项目的 `svg_to_pptx` 模块:
- 在某真实项目的 55 张 SVG 上测试,100% 成功(0 失败 0 跳过)
- 生成的 PPT 每个元素都是原生 DrawingML 形状,文字可直接双击编辑
- 体积小(55 页 209 KB,纯矢量)
- 视觉效果与 SVG 源 100% 对齐

本技能引入这套代码,替换 V3.0 中失败的"手工 python-pptx 拼形状"路径。

## 核心感谢

特别感谢 **Hugo He** 和 ppt-master 开源社区的工作。其技术方案的关键创新:
1. 精确的 baseline 偏移参数(0.85)
2. 字符级精确的文字宽度估算(CJK/英文/空格分类)
3. 东亚+拉丁字体双字段设置
4. `wrap="none"` + `<a:spAutoFit/>` + `lIns/tIns/rIns/bIns="0"` 的关键 XML 配置

## 版本维护

- 固定在 2026-04-17 快照版本
- 上游有重大更新时,手动 review 后合并关键修复
- 不自动同步(避免上游破坏性变更影响本技能稳定性)

## 如何使用

不要直接调用 `svg_to_pptx/` 内部模块。
统一通过上层封装 `assets/svg_to_pptx_wrapper.py` 的 `svg_to_native_pptx()` 函数使用。

## MIT License 全文

MIT License

Copyright (c) hugohe3/ppt-master contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
