# Neon Slides 组件片段

所有组件复制即用。每个组件外层都要包在 `<section class="slide">...<div class="inner">...</div></section>` 里。第一屏记得加 `active` 类。

## 1. Tag 小标签

```html
<span class="tag">CORE CONCEPT</span>
```

常用词: `CORE CONCEPT` / `ARCHITECTURE` / `SECURITY` / `WORKFLOW` / `CASE STUDY` / `DEEP DIVE` / `QUICK START` / `ROADMAP`

## 2. 标题 + 副标

```html
<h1>安全加固:<span class="accent-o">OpenClaw</span> 的三道防线</h1>
<p class="sub">不是事后补救,而是从 AGENTS.md 开始就把口子堵死</p>
```

高亮用 `accent-o`(橙)或 `accent-b`(蓝)。每屏**只**高亮一个词。

## 3. STEP 流程卡(4 步)

```html
<div class="steps">
  <div class="step o"><div class="label">STEP 1</div><div class="title">识别</div><div class="desc">攻击面在哪</div></div>
  <div class="arrow o">→</div>
  <div class="step b"><div class="label">STEP 2</div><div class="title">脱敏</div><div class="desc">AGENTS.md 规则</div></div>
  <div class="arrow b">→</div>
  <div class="step o"><div class="label">STEP 3</div><div class="title">隔离</div><div class="desc">SecretRef</div></div>
  <div class="arrow o">→</div>
  <div class="step b"><div class="label">STEP 4</div><div class="title">审计</div><div class="desc">secrets audit</div></div>
</div>
```

3 步或 5 步同理,橙蓝交替。

## 4. 对比卡(2 栏)

```html
<div class="compare">
  <div class="cmp old">
    <h3>裸奔的 Agent</h3>
    <p>凭证写在配置里,日志全量输出,AGENTS.md 直接暴露内网地址。</p>
  </div>
  <div class="cmp new">
    <h3>加固后的 OpenClaw</h3>
    <p>SecretRef 分离凭证,输出自动脱敏,1Password Vault 托管密钥。</p>
  </div>
</div>
```

## 5. 三栏 Layer 卡

```html
<div class="layers">
  <div class="layer o">
    <div class="icon">🔒</div>
    <h3>凭证层</h3>
    <div class="meta">SecretRef、File/Keychain/1Password-Vault providers、keyRef 模式</div>
    <div class="foot">密钥不落地,配置可提交到 Git</div>
  </div>
  <div class="layer b">
    <div class="icon">📝</div>
    <h3>输出层</h3>
    <div class="meta">AGENTS.md 脱敏规则、日志过滤、内网地址屏蔽</div>
    <div class="foot">别让 Agent 把家底说漏了</div>
  </div>
  <div class="layer o">
    <div class="icon">🛡️</div>
    <h3>审计层</h3>
    <div class="meta">secrets audit、allowInsecureAuth 检查、SlowMist 指南</div>
    <div class="foot">能审的才是安全的</div>
  </div>
</div>
```

## 6. 代码块(直播讲解专用)

在 `<style>` 里加:

```css
.code{
  background:#0D0D0D;border-left:3px solid var(--orange);
  padding:22px 26px;border-radius:8px;
  font-family:"JetBrains Mono",Menlo,monospace;font-size:13px;
  color:#D4D4D4;line-height:1.7;overflow-x:auto;
  margin-top:24px;
}
.code .k{color:var(--orange)}    /* 关键词 */
.code .s{color:#86EFAC}          /* 字符串 */
.code .c{color:#6B7280}          /* 注释 */
```

用法:

```html
<pre class="code"><span class="c"># AGENTS.md 脱敏规则</span>
<span class="k">redact</span>:
  - pattern: <span class="s">"sk-[A-Za-z0-9]{20,}"</span>
  - pattern: <span class="s">"Bearer .*"</span></pre>
```

## 8. 图片组件

Neon Slides 支持四种配图模式,所有样式已经在 `template.html` 里,直接写 HTML 即可。

### 8.0 封面屏 `.cover`(首页必用)

居中大标题 + 橙色分隔线 + 副标题 + 底部 meta,背景图透明度 35% 配中心径向暗化,保证标题稳稳立在视觉中心。**10 屏 deck 的第 1 屏永远用这个**。

```html
<section class="slide active">
  <div class="cover">
    <div class="bg"><img src="images/cover-bg.png" alt=""/></div>
    <div class="center">
      <span class="tag">SECURITY</span>
      <h1>OpenClaw <span class="accent-o">安全加固</span><br/>实战手册</h1>
      <div class="divider"></div>
      <p>从 AGENTS.md 到 SecretRef——一场完整的防御战</p>
    </div>
    <div class="meta">Tech Talk · 2026</div>
  </div>
</section>
```

**要点:**
- 直接放在 `<section class="slide active">` 里,**不用 `.inner`**
- 主标题支持换行 `<br/>`,两行是最佳节奏
- 一个词用 `.accent-o` 渐变即可,别整句染色
- 背景图可以是抽象视觉/产品截图虚化版/自己画的海报
- 底部 `.meta` 放署名、日期、场次信息,可省略

### 8.1 半屏图文(最常用)

左文右图。讲功能 + 配截图,或讲概念 + 配示意图。

```html
<section class="slide">
  <div class="inner">
    <span class="tag">DEEP DIVE</span>
    <h1>SecretRef <span class="accent-o">凭证分离</span></h1>
    <div class="split">
      <div class="text">
        <h3 class="o">密钥不再落地</h3>
        <p>配置文件里只留 SecretRef 引用,真正的密钥由 File / Keychain / 1Password-Vault 三种 provider 托管。</p>
        <p>配置可以放心提交到 Git,审计也能一眼看清楚哪些地方用了敏感凭证。</p>
      </div>
      <div class="media o">
        <img src="images/secretref.png" alt="SecretRef 配置截图"/>
        <div class="caption">图示:auth-profiles.json 中的 keyRef 用法</div>
      </div>
    </div>
  </div>
</section>
```

**要点:**
- 图右加 `.reverse` 类切换为左图右文: `<div class="split reverse">`
- `.media.o` / `.media.b` 控制边框和光晕颜色(橙/蓝)
- `.caption` 是图下方浮层文字说明,可省略
- 图建议宽高比 16:10 或 4:3,太长会挤压文字

### 8.2 章节过渡屏 `.hero`(⚠️ 仅限章节切换,不要用作首页)

**使用边界:** 只在 deck 中段切换章节时用,作用是"仪式感停顿 + 视觉换气"。**首页封面请用 `.cover`(见 8.0)**,不要用 `.hero`。

新版 `.hero` 的视觉结构:**左侧超大描边编号 + 右侧 PART 标签 / 章节标题 / 橙色长分隔线 / 副文案**。背景图透明度仅 25%,配合双层暗化渐变,不会抢戏。进入动画:编号从 0.7 倍缩放 + 左侧渐入,文字块错位 0.15s 右侧渐入。

```html
<section class="slide">
  <div class="hero">
    <div class="bg"><img src="images/part2-bg.png" alt=""/></div>
    <div class="content">
      <div class="numeral" data-num="02">02</div>
      <div class="chapter-meta">
        <span class="part-label">PART II · 实战篇</span>
        <h1>从原理到<span class="accent-o">动手</span></h1>
        <div class="long-divider"></div>
        <p>前面讲完了防御模型,接下来我们一行一行改配置。</p>
      </div>
    </div>
  </div>
</section>
```

**要点:**
- `.numeral` 的 `data-num` 属性要和元素内文字一致,这是用来做描边+半透明填充的双层叠印效果
- 编号用 `01` `02` `03` 两位数格式,别用 `1` `2` `3`(Space Grotesk 的两位数节奏才对)
- `.part-label` 格式推荐 `PART II · 实战篇`,罗马数字 + 中文说明,仪式感足
- h1 里依然保留 `.accent-o` 高亮一个关键词
- 背景图选抽象/意象类,不要选具象截图(具象截图即便虚化也会让观众"想去读细节")
- 10 屏的 deck 最多 1-2 个章节过渡屏,用多了节奏会散

**反例(不要这么做):**
- ❌ 把首页做成 `.hero` —— 用 `.cover`
- ❌ 数字编号用 `1` 而不是 `01`
- ❌ 背景图放清晰的代码截图 —— 容易让观众分心去读代码
- ❌ 一个 10 屏 deck 里塞 3 个以上章节过渡屏 —— 节奏会碎

**要点:**
- 用 `.hero` 替代 `.inner`(**注意** `section.slide` 里直接放 `.hero`,不要再包 `.inner`)
- 图会被 `object-fit:cover` 裁剪铺满
- 自动叠一层 135° 黑色渐变保证文字可读
- 图片透明度降到 55% 配合暗底,不会抢戏

### 8.3 Layer 卡内缩略图(替代 icon)

三栏卡片的 icon box 换成小图,适合产品对比、工具陈列。

```html
<div class="layers">
  <div class="layer o">
    <div class="thumb"><img src="images/openclaw-logo.png" alt="OpenClaw"/></div>
    <h3>OpenClaw</h3>
    <div class="meta">本地 Agent 运行时,凭证托管 + 脱敏输出</div>
    <div class="foot">安全左移,从源头控住</div>
  </div>
  <!-- 其他两张卡同理 -->
</div>
```

把 `.icon` 换成 `.thumb` 就行,结构其他部分不变。

### 图片来源两条路

**网图:** 直接贴 URL,如 `<img src="https://example.com/foo.png"/>`。直播前先下载到本地稳妥,别让网络抽风影响直播。

**本地图:** 在 HTML 文件旁边建一个 `images/` 目录,把图放进去,用相对路径 `images/xxx.png` 引用。分发时把 HTML 和 images 一起打包。

**占位符:** 不确定用什么图时,用 `https://placehold.co/800x500/0D0D0D/F97316?text=SCREENSHOT` 先占位,后面替换。

### 通用 10 屏技术直播图片规划模板

下面这张表可以作为任何技术直播 deck 的脚手架,照着填内容就行:

| 屏 | 组件 | 图片建议 |
|---|---|---|
| 1 封面 | `.cover` | 品牌 logo / 产品视觉 / 抽象科技背景(透明度会自动压到 35%) |
| 2 痛点 | `.compare` 或 `.split` | 可选:一张"现状很糟"的截图(打码) |
| 3 CORE CONCEPT | `.steps` | 流程图或 STEP 卡,通常不配图 |
| 4 架构 | `.layers` | 每张卡顶部放对应模块的小图标/截图(用 `.thumb`) |
| 5 过渡屏 | `.hero` | 抽象氛围图,不要用具象代码截图(会让观众分心去读) |
| 6 实战 1 | `.split` | 左文讲原理,右边配关键配置截图 |
| 7 实战 2 | `.split reverse` | 左边配 CLI 输出截图,右文讲结果 |
| 8 常见坑 | `.list-grid` | 通常不配图,文字清单即可 |
| 9 代码详解 | `.code` | 无需外部图,代码块本身就是视觉 |
| 10 总结 | `.cover` 或普通屏 | 呼应封面视觉,首尾形成闭环 |

**重要节奏提醒:** 10 屏里 `.hero` 最多 1-2 个,`.code` 最多 2-3 个,剩下的给半屏图文和架构卡。代码屏连着放超过 2 屏观众会累。

---

## 9. 清单网格(原第 7 节)

在 `<style>` 里加:

```css
.list-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:32px}
.item{
  padding:18px 22px;border-radius:10px;
  background:var(--card);border:1px solid var(--card-line);
  display:flex;gap:14px;align-items:flex-start;
}
.item .num{
  font-family:"Space Grotesk",sans-serif;font-weight:700;
  color:var(--orange);font-size:20px;min-width:32px;
}
.item .txt{font-size:14px;color:var(--fg)}
.item .txt small{display:block;color:var(--muted);font-size:12px;margin-top:4px}
```

用法:

```html
<div class="list-grid">
  <div class="item"><span class="num">01</span><div class="txt">硬编码凭证<small>写在 agent config 里</small></div></div>
  <div class="item"><span class="num">02</span><div class="txt">日志泄漏<small>debug 模式打印完整 prompt</small></div></div>
  <!-- ... -->
</div>
```

## 屏数建议模板(直播 40min)

10 屏为宜:

1. 封面 — 标题 + 金句 + 一个 tag
2. CORE CONCEPT — 为什么要讲这个(痛点)
3. 对比 — 裸奔 vs 加固
4. ARCHITECTURE — 三层架构(Layer 卡)
5. 常见漏洞清单 — list-grid
6. STEP 流程 — 加固四步
7. 代码屏 — AGENTS.md 脱敏示例
8. 代码屏 — SecretRef 配置示例
9. 审计 — secrets audit 流程
10. 总结金句 + 下一步
