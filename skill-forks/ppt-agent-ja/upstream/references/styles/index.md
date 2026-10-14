# 风格系统索引（26 风格 / 5 板块）

> 本目录下每个 `<quadrant>.md` 文件包含一个板块的所有风格定义。
>
> **新风格的添加**：在对应板块的 `.md` 中追加 JSON Schema + CSS Variables + Mock HTML。
>
> **跨风格共享**：[排版铁律](../typography.md) · [失败模式](../principles/failure-modes.md) · [Bento Grid 布局](../bento-grid.md) · [管线兼容性](../pipeline-compat.md)

---

## 1. 26 风格全景表

| # | style_id | 板块 | 灵感 | 适用场景 | 板块文件 |
|---|----------|------|------|---------|---------|
| 1 | `dark_tech` | 暗色专业 | Linear.app | AI / SaaS / 开发者工具 | [dark.md](dark.md) |
| 2 | `xiaomi_orange` | 暗色专业 | Apple Keynote (硬件) | 硬件 / IoT / 汽车发布 | [dark.md](dark.md) |
| 3 | `luxury_purple` | 暗色专业 | Tom Ford | 奢侈品 / 高端品牌 | [dark.md](dark.md) |
| 4 | `nocturne_violet` | 暗色专业 | Linear (紫光版) | 设计师 SaaS / 产品发布 | [dark.md](dark.md) |
| 5 | `cyberpunk_neon` | 暗色专业 | Cyberpunk 2077 | 电竞 / 游戏 / Web3 | [dark.md](dark.md) |
| 6 | `chrome_y2k` | 暗色专业 | Y2K / Vaporwave | Web3 / 千禧年复古 | [dark.md](dark.md) |
| 7 | `noir_film` | 暗色专业 | 黑白电影 | 纪录片 / 影像艺术 | [dark.md](dark.md) |
| 8 | `blue_white` | 浅色高级 | Apple 企业页面 | 企业 SaaS / 培训 | [light.md](light.md) |
| 9 | `fresh_green` | 浅色高级 | Aesop | 护肤 / 养生 / 食品 | [light.md](light.md) |
| 10 | `minimal_gray` | 浅色高级 | NYT Magazine | 学术 / 法务 / 咨询 | [light.md](light.md) |
| 11 | `mocha_editorial` | 浅色高级 | Anthropic / Pantone 2025 | AI 安全研究 / 出版 | [light.md](light.md) |
| 12 | `medical_pulse` | 浅色高级 | 医疗白蓝 + ECG | 医疗 / 医药 / 保险 | [light.md](light.md) |
| 13 | `earth_concrete` | 浅色高级 | Suisse Int'l | 建筑 / 工业 / 咖啡 | [light.md](light.md) |
| 14 | `champagne_gold` | 浅色高级 | 香槟金 | 婚庆 / 宴会 / 庆典 | [light.md](light.md) |
| 15 | `liquid_glass` | 浅色高级 | iOS 26 / visionOS | XR / AR / 苹果生态 | [light.md](light.md) |
| 16 | `vibrant_rainbow` | 活力鲜明 | Stripe Sessions | 营销 / 创作者 | [vibrant.md](vibrant.md) |
| 17 | `kindergarten_pop` | 活力鲜明 | Quicksand 童趣 | 儿童教育 / 启蒙 | [vibrant.md](vibrant.md) |
| 18 | `bauhaus_block` | 活力鲜明 | Bauhaus / Swiss | 教育 / 创意品牌 | [vibrant.md](vibrant.md) |
| 19 | `candy_pastel` | 活力鲜明 | 马卡龙糖果 | 甜品 / 烘焙 / 零食 | [vibrant.md](vibrant.md) |
| 20 | `royal_red` | 东方文化 | 北京冬奥开幕式 | 中国风 / 政务 / 文化 | [cultural.md](cultural.md) |
| 21 | `sakura_wabi` | 东方文化 | 日本侘寂 | 日系 / 茶道 / 酒店 | [cultural.md](cultural.md) |
| 22 | `ink_jade` | 东方文化 | 墨色+浅米+朱红 | 国潮 / 茶饮 / 古风 | [cultural.md](cultural.md) |
| 23 | `botanic_forest` | 自然/复古 | 深绿森林秘境 | 户外 / 可持续 / 林产 | [natural.md](natural.md) |
| 24 | `safari_savanna` | 自然/复古 | 萨凡纳暖橙 | 旅行 / 探险 / 纪录片 | [natural.md](natural.md) |
| 25 | `retro_70s` | 自然/复古 | 70 年代复古 | 独立咖啡 / 唱片 / 复古 | [natural.md](natural.md) |
| 26 | `gov_authority` | 自然/复古 | 国徽 / 国宴 | 党政 / 重大会议 / 严肃 | [natural.md](natural.md) |

---

## 2. 板块决策矩阵

按主题关键词快速匹配板块：

| 主题关键词 | 推荐板块 | 默认风格 |
|-----------|---------|---------|
| AI / SaaS / 开发者 / 大模型 / 数据 | 暗色专业 | `dark_tech` |
| 硬件 / 手机 / IoT / 汽车 / 智能家居 | 暗色专业 | `xiaomi_orange` |
| 奢侈品 / 时尚 / 高端品牌 | 暗色专业 | `luxury_purple` 或 `noir_film` |
| 游戏 / 电竞 / Web3 | 暗色专业 | `cyberpunk_neon` 或 `chrome_y2k` |
| 企业 / 培训 / 商务 / 金融 | 浅色高级 | `blue_white` |
| 学术 / 研究 / 白皮书 / 法务 | 浅色高级 | `minimal_gray` 或 `mocha_editorial` |
| 医疗 / 医药 / 健康 | 浅色高级 | `medical_pulse` |
| 建筑 / 工业 / 制造 | 浅色高级 | `earth_concrete` |
| 婚礼 / 庆典 / 颁奖 | 浅色高级 | `champagne_gold` |
| 苹果生态 / XR / AR / VR | 浅色高级 | `liquid_glass` |
| 环保 / 自然 / 护肤 / 养生 | 浅色高级 | `fresh_green` |
| 营销 / 推广 / 创作者 / 社交 | 活力鲜明 | `vibrant_rainbow` |
| 儿童 / 教育 / 启蒙 / 亲子 | 活力鲜明 | `kindergarten_pop` |
| 创意品牌 / 独立设计 | 活力鲜明 | `bauhaus_block` |
| 甜品 / 烘焙 / 烘焙店 | 活力鲜明 | `candy_pastel` |
| 中国风 / 政务 / 党建 / 文化 | 东方文化 | `royal_red` |
| 日系 / 茶道 / 民宿 / 侘寂 | 东方文化 | `sakura_wabi` |
| 国潮 / 茶饮 / 古风文创 | 东方文化 | `ink_jade` |
| 户外 / 林业 / 露营 | 自然/复古 | `botanic_forest` |
| 旅行 / 探险 / 自驾 | 自然/复古 | `safari_savanna` |
| 复古 / 黑胶 / 独立咖啡 | 自然/复古 | `retro_70s` |
| 党政 / 重大会议 / 国家级活动 | 自然/复古 | `gov_authority` |
| **未匹配的通用主题** | — | `blue_white`（最通用） |

---

## 3. 风格 JSON Schema

每个风格在板块文件中按以下 JSON Schema 定义：

```json
{
  "style_id": "dark_tech",
  "style_name": "暗黑科技 (Dark Tech)",
  "category": "dark_professional",

  "inspiration": "Linear.app",
  "mood_keywords": ["深空冷寂", "精密仪器", "微光脉搏", "数据洪流", "未来感"],
  "design_soul": "天文台穹顶内部，深蓝黑幕中冷青的仪器扫描光有节奏地划过 -- 精密、冷寂、但每一次扫描都暗含脉搏。",
  "variation_strategy": "数据页用网格点阵+角标装饰线（紧张高密度），章节封面用大面积深空留白+单一光晕（释放），产品页用全屏暗底+中央悬浮发光数据面板（聚焦）",

  "decoration_dna": {
    "signature_move": "网格点阵底纹 + L 形角标装饰线 + 极光辉光",
    "forbidden": ["渐变色块", "叶片装饰", "波浪分隔线", "马卡龙糖果色", "serif 杂志感"],
    "recommended_combos": [
      "网格点阵 + 角标 + 大号水印数字",
      "光晕效果 + 脉冲圆点 + 半透明数字水印"
    ]
  },

  "background": {
    "primary": "#050b1f",
    "gradient_to": "#0a1f3d",
    "texture": { "type": "grid_dot", "size": 80, "opacity": 0.015 },
    "glow": [
      { "x": "80%", "y": "30%", "color": "#6366f1", "opacity": 0.35, "blur": 60 },
      { "x": "20%", "y": "70%", "color": "#22D3EE", "opacity": 0.25, "blur": 60 }
    ]
  },

  "card": {
    "gradient_from": "#1E293B",
    "gradient_to": "#0F172A",
    "border": "rgba(255,255,255,0.05)",
    "border_radius": 12,
    "backdrop_blur": 10
  },

  "text": {
    "primary": "#FFFFFF",
    "secondary": "rgba(255,255,255,0.7)",
    "title_size": 28,
    "body_size": 14,
    "card_title_size": 20
  },

  "accent": {
    "primary": ["#22D3EE", "#3B82F6"],
    "secondary": ["#FDE047", "#F59E0B"]
  },

  "typography": {
    "display_font": "'Inter Tight', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    "body_font": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    "serif_italic_font": "'Instrument Serif', 'Fraunces', Georgia, serif",
    "mono_font": "'JetBrains Mono', 'DM Mono', 'Courier New', monospace",
    "display_letter_spacing": "-0.045em",
    "headline_letter_spacing": "-0.015em",
    "body_letter_spacing": "-0.005em",
    "label_letter_spacing": "0.18em",
    "feature_settings": "'ss01', 'cv11', 'calt', 'kern', 'liga'",
    "tabular_nums": true
  },

  "decorations": {
    "label_anchor": "dot_pulse",
    "title_serif_italic": true,
    "corner_lines": true,
    "vertical_divider": false,
    "drop_cap": false,
    "masthead": false
  },

  "font_imports": [
    "https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
  ]
}
```

### 字段定义

| 字段 | 必填 | 说明 |
|------|------|------|
| `style_id` | ✓ | 唯一英文 ID（snake_case） |
| `style_name` | ✓ | 人类可读名（中文+英文括号）|
| `category` | ✓ | 5 板块之一：`dark_professional` / `light_premium` / `vibrant` / `cultural_oriental` / `natural_retro` |
| `inspiration` | ✓ | 灵感来源（品牌/网站名）|
| `mood_keywords` | ✓ | 3-5 个情绪标签 |
| `design_soul` | ✓ | 一句话设计灵魂（诗意描述） |
| `variation_strategy` | ✓ | 跨页面节奏策略 |
| `decoration_dna.signature_move` | ✓ | 招牌动作（一句话）|
| `decoration_dna.forbidden` | ✓ | 明确禁用的元素 |
| `decoration_dna.recommended_combos` | ✓ | 推荐组合 |
| `background` | ✓ | 背景定义（含 texture / glow）|
| `card` | ✓ | 卡片定义 |
| `text` | ✓ | 文字定义 |
| `accent` | ✓ | 强调色（primary 2 色 + secondary 2 色）|
| `typography` | ✓ | 字体栈 + 字距 + OpenType 特性 |
| `decorations` | ✓ | 签名手法清单（boolean 开关） |
| `font_imports` | ✓ | Google Fonts URL 数组 |

---

## 4. 兼容性

- 8 个原 `style_id`（`dark_tech` / `xiaomi_orange` / `blue_white` / `royal_red` / `fresh_green` / `luxury_purple` / `minimal_gray` / `vibrant_rainbow`）保留不变，但视觉按世界级标杆重做。
- 18 个新风格使用诗意新名。
- 旧的 `references/style-system.md` 改为引导文件，redirect 到本目录。
- Prompt #4 中所有原字段保持兼容；新字段（`mood_keywords` / `design_soul` / `decoration_dna` / `typography` / `decorations`）为可选注入。

---

## 5. 质量自检

每个风格定义完成后，对照以下 7 条自检：

- [ ] 完整 7 大字段（style_id / style_name / category / inspiration / mood_keywords / design_soul / decoration_dna）
- [ ] CSS 变量完整（bg/card/text/accent 全有）
- [ ] 字体栈三层降级（商业/Google/系统）
- [ ] `decoration_dna.forbidden` 明确列出至少 3 个禁用项
- [ ] `font_imports` Google Fonts URL 正确
- [ ] 配套 mock HTML 在 1280×720 画布中渲染正确（无控制台错误）
- [ ] 通过 `scripts/smoke_test.py --style <id>` 校验
