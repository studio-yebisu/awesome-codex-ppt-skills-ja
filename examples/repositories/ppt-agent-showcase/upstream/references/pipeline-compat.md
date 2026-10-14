# HTML -> SVG -> PPTX 管线兼容性规则

本文档汇总所有管线兼容性教训。**HTML 设计稿生成时必须遵守，在源头规避偏移问题。**

核心原则：**html2svg + svg2pptx 不是浏览器**，很多 CSS 特性和 SVG 属性在转换过程中会丢失或产生偏移。HTML 写法必须考虑到下游转换器的能力边界。

---

## 1. CSS 禁止清单

| 禁止特性 | 转换后现象 | 正确替代写法 |
|---------|---------|-----------|
| `background-clip: text` | 渐变变色块 + 白色文字 | `color: var(--accent-1)` 直接上色 |
| `-webkit-text-fill-color` | 文字颜色丢失 | 标准 `color` 属性 |
| `mask-image` / `-webkit-mask-image` | 图片完全消失 | `<div>` 遮罩层（linear-gradient 背景） |
| `::before` / `::after`（视觉装饰用） | 内容消失 | 真实 `<div>` / `<span>` |
| `conic-gradient` | 不渲染 | 内联 SVG `<circle>` + stroke-dasharray |
| CSS border 三角形 (width:0 trick) | 形状丢失 | 内联 SVG `<polygon>` |
| `mix-blend-mode` | 不支持 | `opacity` 叠加 |
| `filter: blur()` | 光栅化变位图 | `opacity` 或 `box-shadow` |
| `content: '文字'` | 文字消失 | 真实 `<span>` |
| CSS `background-image: url(...)` | dom-to-svg 忽略 | `<img>` 标签 |

html2svg.py 兜底覆盖：前3项 + 伪元素 + conic-gradient + border三角形（共6种），但兜底效果远不如正确写法。

---

## 2. 防偏移写法（关键章节）

svg2pptx 的文本定位基于 SVG text 元素的坐标，但 PPTX textbox 的坐标系与 SVG 不同（SVG text y = baseline，PPTX y = textbox 顶部）。以下写法可从 HTML 源头避免偏移：

### 2.1 内联 SVG 中的文本标注 -- 用 HTML 叠加替代 SVG text

**问题**：内联 SVG 中的 `<text>` 元素经过 dom-to-svg 转换后坐标是 viewBox 坐标系，svg2pptx 在处理 baseline 偏移和 text-anchor 居中时有精度损失（约 +/- 3-5px），导致标注位置偏移。

**HTML 防偏移写法**：把文字标注从 SVG `<text>` 移出来，用 HTML `<div>` 绝对定位叠加在 SVG 上方。HTML div 由 dom-to-svg 精确定位，不经过 viewBox 坐标转换，偏移风险为零。

```html
<!-- 正确：HTML div 叠加标注，零偏移 -->
<div class="chart-container" style="position: relative;">
  <svg viewBox="0 0 660 340" style="width:100%; height:100%;">
    <!-- 只画柱子、线条等图形元素，不写 <text> -->
    <rect x="80" y="100" width="60" height="200" fill="#FF6900"/>
  </svg>
  <!-- 标注用 HTML 绝对定位叠加 -->
  <span style="position:absolute; left:12.5%; top:25%; font-size:14px; color:#fff;">720</span>
  <span style="position:absolute; left:12.5%; bottom:5%; font-size:12px; color:rgba(255,255,255,0.6);">标准版</span>
</div>
```

```html
<!-- 禁止：SVG text 在 PPTX 中会偏移 -->
<svg viewBox="0 0 660 340">
  <rect x="80" y="100" width="60" height="200" fill="#FF6900"/>
  <text x="110" y="90" text-anchor="middle" fill="#fff">720</text>
</svg>
```

### 2.2 不同字号混排 -- 必须用 flex 独立元素

**问题**：大小字号内嵌（`<div class="big">3.08<span class="small">s</span></div>`）经 dom-to-svg 转为独立 tspan 后，svg2pptx 给每个 tspan 按各自字号做 baseline 偏移，小字会上移。

```html
<!-- 正确：flex baseline 对齐 -->
<div style="display:flex; align-items:baseline; gap:4px;">
  <span style="font-size:48px;">3.08</span>
  <span style="font-size:18px;">s</span>
</div>
```

```html
<!-- 禁止：内嵌不同字号 span -->
<div class="big">3.08<span class="small">s</span></div>
```

### 2.3 环形图（圆弧进度条）-- SVG 画弧 + HTML 叠加文字

```html
<!-- 正确：环形图最佳实践 -->
<div class="ring-container" style="position: relative; width:120px; height:120px;">
  <!-- SVG 只画圆环弧线 -->
  <svg viewBox="0 0 120 120" style="width:100%; height:100%;">
    <!-- 底圈 -->
    <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="8"/>
    <!-- 弧线：用 dasharray 两值格式，禁止 dashoffset -->
    <circle cx="60" cy="60" r="50" fill="none" stroke="#FF6900" stroke-width="8"
            stroke-dasharray="235 314" stroke-linecap="round"
            transform="rotate(-90 60 60)"/>
  </svg>
  <!-- 中心文字用 HTML 叠加，不用 SVG text -->
  <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center;">
    <div style="font-size:22px; font-weight:700; color:#fff;">15</div>
    <div style="font-size:10px; color:rgba(255,255,255,0.6);">分钟</div>
  </div>
</div>
```

### 2.4 图例标签 -- 用 HTML flex 布局

```html
<!-- 正确：HTML flex 图例，不用 SVG text -->
<div style="display:flex; gap:16px; font-size:12px;">
  <div style="display:flex; align-items:center; gap:4px;">
    <span style="display:inline-block; width:12px; height:12px; background:#999; border-radius:2px;"></span>
    <span style="color:rgba(255,255,255,0.6);">初代SU7</span>
  </div>
  <div style="display:flex; align-items:center; gap:4px;">
    <span style="display:inline-block; width:12px; height:12px; background:#FF6900; border-radius:2px;"></span>
    <span style="color:rgba(255,255,255,0.6);">新一代SU7</span>
  </div>
</div>
```

### 2.5 x 轴标签（标准版/Pro/Max）-- 用 HTML 容器

```html
<!-- 正确: x 轴标签用 HTML -->
<div style="display:flex; justify-content:space-around; padding:0 10%;">
  <span style="font-size:13px; color:rgba(255,255,255,0.6);">标准版</span>
  <span style="font-size:13px; color:rgba(255,255,255,0.6);">Pro</span>
  <span style="font-size:13px; color:rgba(255,255,255,0.6);">Max</span>
</div>
```

---

## 3. 图片路径

| 场景 | 错误写法 | 正确写法 |
|------|---------|---------|
| img src 引用 | 依赖浏览器 resolve | html2svg 以 HTML 文件所在目录为基准 resolve 相对路径 |
| CSS background-image | 会被 dom-to-svg 忽略 | 用 `<img>` 标签 |

---

## 4. SVG circle 环形图属性

| 属性 | svg2pptx 支持 | 说明 |
|------|-------------|------|
| `stroke-dasharray="arc gap"` | 支持 | 用两个值：弧线长度 + 间隔长度 |
| `stroke-dashoffset` | **不支持** | 禁止使用，改用 dasharray 的两值格式 |
| `stroke-linecap="round"` | 支持 | 圆角弧端 |
| `transform="rotate(-90 cx cy)"` | 支持 | 从12点钟方向开始 |

正确弧线写法：`stroke-dasharray="235 314"` （弧长=235, 圆周=2*pi*50=314）

---

## 5. 底层氛围图

| 项目 | 规则 |
|------|------|
| opacity | 0.05 - 0.10（卡片内）/ 0.25 - 0.40（封面页） |
| 尺寸 | 限制在容器 40-60%，不要全覆盖 |
| z-index | 必须为 0 或 -1 |
| 实现方式 | 极低 opacity：直接 `<img>` + opacity |
| | 封面级渐隐：`<div>` 容器内 img + 遮罩 div |
| **禁止** | div 遮罩在 PPTX 中层叠不可靠时，回退到纯 opacity |

---

## 6. 配图技法管线安全等级

| 技法 | 管线安全 | 原因 |
|------|---------|------|
| 渐隐融合（div遮罩） | 安全 | 真实 div + linear-gradient |
| 色调蒙版 | 安全 | 真实 div + 半透明背景 |
| 氛围底图 | 最安全 | 纯 opacity |
| 裁切视窗 | 安全 | overflow:hidden + div 渐变 |
| 圆形裁切 | 安全 | border-radius |
| ~~CSS mask-image~~ | **禁止** | dom-to-svg 不支持 |

---

## 7. 总结：HTML 设计稿防偏移 checklist

生成每页 HTML 时，对照以下清单：

- [ ] CSS 禁止清单中的特性未使用
- [ ] 所有图片用 `<img>` 标签，不用 CSS background-image
- [ ] 内联 SVG 中**不含 `<text>` 元素**，所有文字标注用 HTML div 叠加
- [ ] 不同字号混排用 flex + 独立 span，不用嵌套 span
- [ ] 环形图用 stroke-dasharray 两值格式，不用 dashoffset
- [ ] 图例、x轴标签、数据标注全部用 HTML 元素，不用 SVG text
- [ ] 底层配图用低 opacity `<img>` 或 div 遮罩
- [ ] 伪元素 `::before`/`::after` 装饰已用真实元素替代
