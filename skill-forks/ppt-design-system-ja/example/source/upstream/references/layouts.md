# 布局模板 (蒸馏自 guizang-ppt-skill)

10 种页面布局骨架，覆盖演示文稿常见场景。每种包含 HTML 代码和设计要点。

## 图片比例规范

| 场景 | 推荐比例 | 说明 |
|------|---------|------|
| 左文右图主图 | 16:10 或 4:3 | 标准图文排版 |
| 图片网格 | 固定 `height:Nvh` | 同组必须同高 |
| 左小图+右文字 | 1:1 或 3:2 | 辅助插图 |
| 全屏主视觉 | 16:9 | Hero 页背景 |
| 竖版插图 | 3:4 | 图文混排辅助图 |

## 主题节奏规划 (硬规则)

- 连续 3 页以上同主题 = 视觉疲劳，不允许
- 8 页以上必须有 ≥1 个 `hero dark` + ≥1 个 `hero light`
- 不能只有 `light` 正文页，必须有 `dark` 正文页制造呼吸
- 每 3-4 页插入 1 个 hero 页

---

### Layout 1: 开场封面 (Hero Cover)

```html
<section class="slide hero dark">
  <div class="chrome"><div>场景标签</div><div>Vol.01</div></div>
  <div class="frame" style="display:grid;gap:3vh;align-content:center;min-height:80vh">
    <div class="kicker" data-anim>引导语 · 一句话定调</div>
    <h1 class="h-hero" data-anim>主标题</h1>
    <h2 class="h-sub" data-anim>副标题 · 补充说明</h2>
    <p class="lead" style="max-width:50vw" data-anim>一句话简介，说明这个演示的核心内容。</p>
    <div class="meta-row" data-anim>
      <span>汇报人</span><span>·</span><span>日期</span>
    </div>
  </div>
  <div class="foot"><div>项目信息</div><div>— 年份 —</div></div>
</section>
```

**要点**: 用 `hero dark` 让 WebGL 透出；`h-hero` 最大字号(10vw)；内容垂直居中。

---

### Layout 2: 章节幕封 (Act Divider)

```html
<section class="slide hero light">
  <div class="chrome"><div>第一幕 · 章节名</div><div>Act I</div></div>
  <div class="frame" style="display:grid;gap:4vh;align-content:center;min-height:80vh">
    <div class="kicker" data-anim>Act I</div>
    <h1 class="h-hero" data-anim>章节标题</h1>
    <p class="lead" style="max-width:50vw" data-anim>一句话引子。</p>
  </div>
  <div class="foot"><div>章节描述</div><div>— · —</div></div>
</section>
```

**要点**: 极简，只需 kicker + 大标题 + 一行引语；相邻幕封交替 `hero light/hero dark`。

---

### Layout 3: 数据大字报 (Big Numbers Grid)

```html
<section class="slide light">
  <div class="chrome"><div>主题 · 数据篇</div><div>页码</div></div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim>KPI · 分类</div>
    <h2 class="h-xl" data-anim>大标题</h2>
    <p class="lead" data-anim>一句话说明。</p>
    <div class="grid-6" style="margin-top:4vh">
      <div class="stat-card" data-anim>
        <div class="stat-label">指标名</div>
        <div class="stat-nb">数字 <span class="stat-unit">单位</span></div>
        <div class="stat-note">注释</div>
      </div>
      <!-- 重复 stat-card × N -->
    </div>
  </div>
  <div class="foot"><div>数据来源/截止时间</div><div>页码</div></div>
</section>
```

**要点**: 3×2 网格最稳；stat-card 结构固定：label → nb → note；数字用 K/M 简写。

---

### Layout 4: 左文右图 (Quote + Image)

```html
<section class="slide light">
  <div class="chrome"><div>章节</div><div>页码</div></div>
  <div class="frame grid-2-7-5" style="padding-top:4vh">
    <div style="display:flex;flex-direction:column;justify-content:space-between;gap:3vh">
      <div>
        <div class="kicker" data-anim>引导句</div>
        <h2 class="h-xl" data-anim>标题</h2>
        <p class="lead" data-anim>正文内容</p>
      </div>
      <div class="callout" data-anim>
        "引用金句"
        <div class="callout-src">— 出处</div>
      </div>
    </div>
    <figure class="frame-img r-16x10" data-anim>
      <img src="images/xx.png" alt="描述">
      <figcaption class="img-cap">图注</figcaption>
    </figure>
  </div>
  <div class="foot"><div>页脚说明</div><div>— · —</div></div>
</section>
```

**要点**: 用 `grid-2-7-5` (左7右5)，左列 flex column + justify-content:space-between 让 callout 贴底。

---

### Layout 5: 图片网格 (Image Grid)

```html
<section class="slide light">
  <div class="frame" style="padding-top:4vh">
    <div class="kicker" data-anim>类型</div>
    <h2 class="h-xl" data-anim>标题</h2>
    <div class="grid-3-3" style="margin-top:3vh">
      <figure class="frame-img" style="height:26vh" data-anim>
        <img src="images/01.png" alt="描述1">
        <figcaption class="img-cap">说明1</figcaption>
      </figure>
      <!-- 重复 × N，确保高度一致 -->
    </div>
  </div>
</section>
```

**要点**: 关键是用 `height:NNvh` 固定，不用 aspect-ratio；图片自动 object-fit:cover + object-position:top。

---

### Layout 6: 流水线 (Pipeline)

```html
<section class="slide light" data-animate="pipeline">
  <div class="frame">
    <div class="kicker">流程</div>
    <h2 class="h-xl">标题</h2>
    <div class="pipeline-section">
      <div class="pipeline-label">阶段名 · Label</div>
      <div class="pipeline">
        <div class="step" data-anim="step">
          <div class="step-nb">01</div>
          <div class="step-title">步骤名</div>
          <div class="step-desc">描述文字</div>
        </div>
        <!-- 重复 step × N -->
      </div>
    </div>
  </div>
</section>
```

**要点**: 单行最好 ≤5 个 step；可以有多个 pipeline-section 表示多阶段。

---

### Layout 7: 悬念问题页 (Hero Question)

```html
<section class="slide hero dark">
  <div class="frame" style="display:grid;gap:6vh;align-content:center;min-height:80vh">
    <div class="kicker" data-anim>The Question</div>
    <h1 class="h-hero" data-anim>
      一个核心问题？
    </h1>
    <p class="lead" style="max-width:50vw" data-anim>
      点破问题的引导句。
    </p>
  </div>
</section>
```

**要点**: 留白越多越好，只放一个问题；`h-hero` 字号按文字长度调整。

---

### Layout 8: 大引用页 (Big Quote)

```html
<section class="slide light" data-animate="quote">
  <div class="frame" style="display:grid;gap:4vh;align-content:center;min-height:80vh">
    <blockquote class="bq">
      "金句内容"
    </blockquote>
    <p class="lead">出处 · 日期</p>
  </div>
</section>
```

**要点**: 整页留白，只放大引用+出处；衬线字体加粗显示。

---

### Layout 9: 并列对比 (Before / After)

```html
<section class="slide light">
  <div class="frame grid-2-6-6" style="gap:3vw">
    <div class="before-col">
      <div class="col-header">旧模式 · Before</div>
      <h3 class="h-md">方案 A</h3>
      <ul class="col-list">
        <li>缺点 1</li>
        <li>缺点 2</li>
      </ul>
    </div>
    <div class="after-col">
      <div class="col-header">新模式 · After</div>
      <h3 class="h-md">方案 B</h3>
      <ul class="col-list">
        <li>优点 1</li>
        <li>优点 2</li>
      </ul>
    </div>
  </div>
</section>
```

**要点**: 1:1 左右分半；旧列 opacity 降低做视觉弱化；两列结构统一。

---

### Layout 10: 图文混排 (Lead Image + Side Text)

```html
<section class="slide light">
  <div class="frame grid-2-8-4" style="padding-top:4vh">
    <div>
      <div class="kicker" data-anim>标签</div>
      <h2 class="h-xl" data-anim>标题</h2>
      <p class="lead" data-anim>正文段落 1</p>
      <p data-anim>正文段落 2</p>
      <div class="callout" data-anim>引用块</div>
    </div>
    <figure class="frame-img r-3x4" data-anim>
      <img src="images/xx.png" alt="描述">
    </figure>
  </div>
</section>
```

**要点**: `grid-2-8-4` (8:4) 让正文占主导；右列用竖版 3:4，避免和文字竞争注意力。

---

### 常用网格模板 (HTML)

| 类名 | 配比 | 用途 |
|------|------|------|
| `.grid-2-6-6` | 6:6 (1:1) | 对半分（对比页） |
| `.grid-2-7-5` | 7:5 | 文字为主+辅助图 |
| `.grid-2-8-4` | 8:4 (2:1) | 大段文字+小图 |
| `.grid-3` | 1:1:1 | 3 项并列 |
| `.grid-3-3` | 3x2 | 6 图矩阵 |
| `.grid-6` | 3x2 | 6 个数据卡片 |
| `.grid-4` | 1:1:1:1 | 4 项并列 |

### 常用 CSS 类名

```css
/* 字体层级 */
.h-hero { font-family: var(--serif-zh); font-weight: 900; font-size: clamp(36px,6vw,80px); }
.h-xl   { font-family: var(--serif-zh); font-weight: 700; font-size: clamp(28px,3.5vw,52px); }
.h-sub  { font-family: var(--serif-zh); font-weight: 600; font-size: clamp(20px,2vw,32px); }
.h-md   { font-family: var(--sans-en);  font-weight: 600; font-size: clamp(16px,1.3vw,22px); }
.lead   { font-family: var(--sans-zh);  font-weight: 300; font-size: clamp(15px,1.15vw,20px); line-height:1.7; opacity:.75; }
.kicker { font-family: var(--mono);     font-size: clamp(11px,0.8vw,15px); letter-spacing:.15em; opacity:.6; text-transform:uppercase; }

/* 数据卡片 */
.stat-card { padding: 2.5vh 1.5vw; border-left: 3px solid var(--accent); background: rgba(var(--ink-rgb),.03); }
.stat-label { font-family: var(--mono); font-size: clamp(10px,.7vw,13px); letter-spacing:.1em; opacity:.5; }
.stat-nb { font-family: var(--sans-en); font-weight: 700; font-size: clamp(32px,3.5vw,56px); letter-spacing:-.03em; }
.stat-unit { font-size: .5em; opacity: .6; }
.stat-note { font-size: clamp(12px,.8vw,15px); opacity: .5; }

/* 引用块 */
.callout { border-left: 3px solid; padding: 1.5vh 1.5vw; font-family: var(--serif-zh); font-weight: 600; font-size: clamp(14px,1.1vw,20px); opacity: .85; }
.callout-src { font-family: var(--mono); font-size: clamp(10px,.65vw,13px); opacity: .5; }

/* 流水线 */
.step { padding: 2vh 1.2vw; border: 1px solid; opacity: .35; }
.step.active { opacity: 1; border-color: var(--accent); }
.step-nb { font-family: var(--mono); font-size: clamp(12px,.8vw,15px); opacity: .4; }
.step-title { font-weight: 600; font-size: clamp(14px,1vw,18px); }
.step-desc { font-size: clamp(11px,.7vw,14px); opacity: .6; }

/* 网格 */
.grid-2-6-6, .grid-2-7-5, .grid-2-8-4 { display: grid; gap: 3vw; align-items: start; }
.grid-2-6-6 { grid-template-columns: 1fr 1fr; }
.grid-2-7-5 { grid-template-columns: 7fr 5fr; }
.grid-2-8-4 { grid-template-columns: 8fr 4fr; }
.grid-6 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2vw; }

/* 图片容器 */
.frame-img { width: 100%; overflow: hidden; border-radius: 4px; }
.frame-img img { width: 100%; height: 100%; object-fit: cover; object-position: top center; }
.frame-img.r-16x10 { aspect-ratio: 16 / 10; }
.frame-img.r-3x4 { aspect-ratio: 3 / 4; }
