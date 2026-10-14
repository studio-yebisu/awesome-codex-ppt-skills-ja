# 活力鲜明板块（4 风格）

> 板块定位：高饱和 + 鲜亮 + 友好/创意/营销/儿童感。Stripe / 儿童绘本 / Bauhaus / 糖果店。

---

## 索引

| # | style_id | 灵感 | 一句话 |
|---|----------|------|-------|
| 1 | `vibrant_rainbow` | Stripe Sessions | 多层渐变 + 玻璃球反光（升级）|
| 2 | `kindergarten_pop` | Quicksand 圆润字体 | 奶油黄底 + 友好 blob + emoji |
| 3 | `bauhaus_block` | Bauhaus / Swiss | 三原色几何拼贴 + Helvetica |
| 4 | `candy_pastel` | Ladurée 糖果店 | 马卡龙圆点 + Playfair italic |

---

## 1. vibrant_rainbow（升级 - Stripe 级）

```json
{
  "style_id": "vibrant_rainbow",
  "style_name": "活力彩虹 (Stripe-grade Gradient)",
  "category": "vibrant",
  "inspiration": "Stripe Sessions / Stripe.com",
  "mood_keywords": ["多层渐变", "玻璃球反光", "高饱和高级", "大会舞台"],
  "design_soul": "Stripe Sessions 大会舞台上，多层彩色渐变像极光一样流动，玻璃球反射着舞台灯光，每个数据都骄傲地占据视野。",
  "variation_strategy": "封面用大渐变 + 多个玻璃球，产品页用单色高饱和 + 1 张玻璃卡，数据页用高对比白底 + accent 色。",
  "decoration_dna": {
    "signature_move": "多层 linear-gradient 渐变背景（粉/紫/蓝/青）+ 玻璃球（多层 radial-gradient + 内阴影 + 模糊光环）+ 圆角药丸按钮 + serif italic 关键词",
    "forbidden": ["纯色背景", "暗色调", "serif 杂志感", "马卡龙糖果色（与 candy_pastel 区分）"],
    "recommended_combos": ["多层渐变 + 大玻璃球 + 圆角按钮", "白色药丸 CTA + ghost 按钮 + tabular-nums 数据"]
  },
  "background": { "primary": "linear-gradient(135deg, #ff5b9d 0%, #b266ff 30%, #4a8cff 60%, #00d8d4 100%)", "gradient_to": "#00d8d4", "texture": { "type": "glass_orbs" } },
  "card": { "gradient_from": "rgba(255,255,255,0.18)", "gradient_to": "rgba(255,255,255,0.08)", "border": "rgba(255,255,255,0.4)", "border_radius": 100, "backdrop_blur": 20 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.85)", "title_size": 116, "body_size": 14, "card_title_size": 18 },
  "accent": { "primary": ["#ffd16b", "#ffffff"], "secondary": ["#ff5b9d", "#00d8d4"] },
  "typography": {
    "display_font": "'Inter Tight', 'Inter', -apple-system, sans-serif",
    "body_font": "'Inter', -apple-system, sans-serif",
    "serif_italic_font": "'Instrument Serif', 'Fraunces', Georgia, serif",
    "mono_font": "'JetBrains Mono', monospace",
    "display_letter_spacing": "-0.045em",
    "headline_letter_spacing": "-0.025em",
    "body_letter_spacing": "-0.005em",
    "label_letter_spacing": "0.22em",
    "feature_settings": "'ss01', 'cv11', 'calt', 'kern', 'liga', 'ccmp'",
    "tabular_nums": true
  },
  "decorations": { "label_anchor": "horizontal_line", "title_serif_italic": true, "corner_lines": false, "vertical_divider": false, "drop_cap": false, "masthead": false, "glass_orbs": true, "pill_buttons": true },
  "font_imports": ["https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap"]
}
```

Mock: [`ppt-output/style-gallery/vibrant_rainbow.html`](../../ppt-output/style-gallery/vibrant_rainbow.html)

---

## 2. kindergarten_pop（新增 - 儿童教育）

```json
{
  "style_id": "kindergarten_pop",
  "style_name": "儿童启蒙 (Kindergarten Pop)",
  "category": "vibrant",
  "inspiration": "高质量儿童绘本 / Notion 友好感 / Apple Kids",
  "mood_keywords": ["柔和阳光", "圆润 Quicksand", "彩色 blob", "友好 emoji"],
  "design_soul": "晨光下的儿童房，奶油色阳光铺满桌面，圆润的字母温柔地排列，几个彩色气球漂在角落。",
  "variation_strategy": "封面用大圆角卡片 + emoji 装饰 + 友好标题，活动页用 3 张大圆角彩色卡，结果页用 ✓⭐ 庆祝徽章。",
  "decoration_dna": {
    "signature_move": "奶油黄渐变底 + 圆形彩色 blob（粉/蓝/绿/黄）+ Quicksand 圆润字体 + 大圆角（≥ 16px）+ ✓⭐❤️ emoji 点缀",
    "forbidden": ["暗色背景", "硬朗几何", "霓虹效果", "serif 字体", "拥挤布局"],
    "recommended_combos": ["奶油黄底 + 4 色 blob + 圆角卡片", "emoji + Quicksand 圆润 + tabular-nums 数字"]
  },
  "background": { "primary": "#fff8e7", "gradient_to": "#ffeed4", "texture": { "type": "none" } },
  "card": { "gradient_from": "#ffffff", "gradient_to": "#fff8e7", "border": "rgba(255,127,193,0.2)", "border_radius": 28, "backdrop_blur": 0 },
  "text": { "primary": "#2a2a3a", "secondary": "#5a5a6a", "title_size": 36, "body_size": 14, "card_title_size": 18 },
  "accent": { "primary": ["#ff7eb9", "#ffd166"], "secondary": ["#06d6a0", "#87ceeb"] },
  "typography": {
    "display_font": "'Quicksand', 'Nunito', -apple-system, sans-serif",
    "body_font": "'Quicksand', 'Nunito', -apple-system, sans-serif",
    "serif_italic_font": "'Instrument Serif', Georgia, serif",
    "mono_font": "'JetBrains Mono', monospace",
    "display_letter_spacing": "-0.015em",
    "headline_letter_spacing": "-0.01em",
    "body_letter_spacing": "0",
    "label_letter_spacing": "0.18em",
    "feature_settings": "'kern', 'liga', 'calt', 'ss01'",
    "tabular_nums": true
  },
  "decorations": { "label_anchor": "horizontal_line", "title_serif_italic": false, "corner_lines": false, "vertical_divider": false, "drop_cap": false, "masthead": false, "color_blobs": true, "rounded_corners": true, "emoji_decorations": true },
  "font_imports": ["https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Nunito:wght@400;500;600;700&display=swap"]
}
```

Mock: [`ppt-output/style-gallery/kindergarten_pop.html`](../../ppt-output/style-gallery/kindergarten_pop.html)

---

## 3. bauhaus_block（新增 - 几何拼贴）

```json
{
  "style_id": "bauhaus_block",
  "style_name": "包豪斯几何 (Bauhaus Block)",
  "category": "vibrant",
  "inspiration": "Bauhaus / Swiss Design / Massimo Vignelli / IBM Eames",
  "mood_keywords": ["三原色", "几何拼贴", "Helvetica 800", "极致克制"],
  "design_soul": "1920 年代 Dessau 的 Bauhaus 建筑里，三原色的几何形状以严格的网格秩序排列，每一个圆和方块都精确得像数学定理。",
  "variation_strategy": "封面用大字号 Helvetica + 三原色几何，原则页用 3 张方形卡，作品页用网格图案展示。",
  "decoration_dna": {
    "signature_move": "三原色（红 #d62828 / 蓝 #003049 / 黄 #ffd60a）几何形状（圆/方/三角）+ Helvetica Now 800 字重 + 严格网格 + 极简留白",
    "forbidden": ["暗色背景", "渐变文字", "霓虹效果", "圆角大于 4px", "曲线装饰"],
    "recommended_combos": ["奶油底 + 红圆 + 蓝方 + 黄三角", "Helvetica 巨字 + 严格网格 + 三原色"]
  },
  "background": { "primary": "#f4f0e8", "gradient_to": "#f4f0e8", "texture": { "type": "none" } },
  "card": { "gradient_from": "#ffffff", "gradient_to": "#f4f0e8", "border": "#1a1a1a", "border_radius": 0, "backdrop_blur": 0 },
  "text": { "primary": "#1a1a1a", "secondary": "#666", "title_size": 92, "body_size": 14, "card_title_size": 18 },
  "accent": { "primary": ["#d62828", "#003049"], "secondary": ["#ffd60a", "#1a1a1a"] },
  "typography": {
    "display_font": "'Helvetica Neue', 'Inter Tight', 'Inter', sans-serif",
    "body_font": "'Inter', -apple-system, sans-serif",
    "serif_italic_font": "'Instrument Serif', Georgia, serif",
    "mono_font": "'JetBrains Mono', monospace",
    "display_letter_spacing": "-0.035em",
    "headline_letter_spacing": "-0.025em",
    "body_letter_spacing": "-0.005em",
    "label_letter_spacing": "0.32em",
    "feature_settings": "'kern', 'liga', 'calt', 'ss01', 'cv11'",
    "tabular_nums": true
  },
  "decorations": { "label_anchor": "horizontal_line", "title_serif_italic": false, "corner_lines": false, "vertical_divider": true, "drop_cap": false, "masthead": false, "geometric_shapes": true, "primary_colors_only": true, "strict_grid": true },
  "font_imports": ["https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;700;800;900&family=Inter:wght@400;500;600;700&display=swap"]
}
```

Mock: [`ppt-output/style-gallery/bauhaus_block.html`](../../ppt-output/style-gallery/bauhaus_block.html)

---

## 4. candy_pastel（新增 - 甜品/烘焙）

```json
{
  "style_id": "candy_pastel",
  "style_name": "马卡龙糖果 (Candy Pastel)",
  "category": "vibrant",
  "inspiration": "Ladurée / Pierre Hermé / Glossier",
  "mood_keywords": ["马卡龙圆点", "粉嫩柔和", "Playfair italic", "甜品店"],
  "design_soul": "巴黎 Ladurée 橱窗里，粉嫩马卡龙整齐排列，每一颗都像 Playfair 字母一样精致优雅。",
  "variation_strategy": "封面用 Playfair italic 大标题 + 5 色马卡龙圆点，产品页用大圆角商品卡 + 价格 tabular，结果页用粉色徽章 + 包装感。",
  "decoration_dna": {
    "signature_move": "粉嫩米白渐变底 + 马卡龙色圆点（粉/绿/黄/蓝/紫）+ Playfair italic 主标题 + 大圆角（≥ 24px）+ 圆形商品图位",
    "forbidden": ["暗色背景", "霓虹效果", "硬朗几何", "高饱和", "拥挤布局"],
    "recommended_combos": ["米白渐变 + 5 色马卡龙圆点 + Playfair italic", "圆形商品 + 价格 ¥XX tabular + 大圆角卡"]
  },
  "background": { "primary": "#fff5f0", "gradient_to": "#fff0e8", "texture": { "type": "none" } },
  "card": { "gradient_from": "#ffffff", "gradient_to": "#fff5f0", "border": "rgba(248,187,208,0.3)", "border_radius": 24, "backdrop_blur": 0 },
  "text": { "primary": "#4a2c2a", "secondary": "#7a4c4a", "title_size": 78, "body_size": 14, "card_title_size": 18 },
  "accent": { "primary": ["#f8bbd0", "#c8e6c9"], "secondary": ["#fff59d", "#b3e5fc"] },
  "typography": {
    "display_font": "'Playfair Display', 'Fraunces', Georgia, serif",
    "body_font": "'Inter', -apple-system, sans-serif",
    "serif_italic_font": "'Playfair Display', 'Fraunces', Georgia, serif",
    "mono_font": "'JetBrains Mono', monospace",
    "display_letter_spacing": "-0.025em",
    "headline_letter_spacing": "-0.015em",
    "body_letter_spacing": "-0.005em",
    "label_letter_spacing": "0.4em",
    "feature_settings": "'kern', 'liga', 'ss01', 'cv11', 'calt', 'dlig'",
    "tabular_nums": true
  },
  "decorations": { "label_anchor": "horizontal_line", "title_serif_italic": true, "corner_lines": false, "vertical_divider": false, "drop_cap": false, "masthead": false, "macaron_dots": true, "rounded_24": true, "circular_product": true },
  "font_imports": ["https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Fraunces:ital,wght@0,400;1,400&family=Inter:wght@400;500;600&display=swap"]
}
```

Mock: [`ppt-output/style-gallery/candy_pastel.html`](../../ppt-output/style-gallery/candy_pastel.html)
