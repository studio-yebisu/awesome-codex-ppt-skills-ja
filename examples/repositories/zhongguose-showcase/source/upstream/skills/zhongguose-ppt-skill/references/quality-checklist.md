# 质量检查 / Quality Checklist

## 目录 / Contents

1. 内容 / Content
2. 结构 / Structure
3. 主题与字体 / Theme and typography
4. 资源与离线 / Assets and offline
5. 浏览器与交互 / Browser and interaction
6. 交付 / Delivery

## 1. 内容 / Content

- [ ] 文稿状态和润色尺度已经确认。
- [ ] Manuscript status and polishing scope are confirmed.
- [ ] 所有原稿条目都能映射到页面，或有明确排除理由。
- [ ] Every source item maps to a slide or has an approved exclusion reason.
- [ ] 分组来自用户文档，Skill 自行提炼的分组已经确认。
- [ ] Grouping comes from the source and derived grouping has user approval.
- [ ] 中文保留名称、数字、因果、顺序和关键表述。
- [ ] Chinese preserves names, numbers, causality, sequence, and fixed wording.
- [ ] 英文更短、更小，且没有新增观点。
- [ ] English is shorter, smaller, and adds no new claims.

## 2. 结构 / Structure

- [ ] 每页 `section.slide` 都有 `data-layout`；动效页同时有 `data-animate`。
- [ ] Every `section.slide` has `data-layout`; animated slides also have `data-animate`.
- [ ] 每个一级版块前都有独立章节扉页。
- [ ] Every top-level section has its own divider slide.
- [ ] 非封面页包含 `.section-tabs`，且恰有一个 `.tab.active`。
- [ ] Every non-cover slide contains `.section-tabs` with exactly one `.tab.active`.
- [ ] 一页只承担一个核心职责。
- [ ] Every slide has one primary role.

执行：

    node "<skill_dir>/scripts/extract-deck-outline.mjs" "path/to/index.html"
    node "<skill_dir>/scripts/validate-deck.mjs" "path/to/index.html"

## 3. 主题与字体 / Theme and typography

- [ ] accent、accent-rgb、accent-on 成对正确。
- [ ] accent, accent-rgb, and accent-on form a valid set.
- [ ] 主题表面全部使用变量，没有残留飞泉绿或固定白字。
- [ ] Themed surfaces use tokens with no residual green or hardcoded white text.
- [ ] 对比度至少 4.5:1。
- [ ] Contrast is at least 4.5:1.
- [ ] 封面和章节大标题加载 Zhongguose Cover。
- [ ] Cover and divider titles load Zhongguose Cover.
- [ ] 修改 HTML 后已重新生成 WOFF2 与 manifest。
- [ ] WOFF2 and manifest were rebuilt after the last HTML edit.

执行：

    python "<skill_dir>/scripts/subset-cover-font.py" "path/to/index.html"

重建本 Skill 自带模板时，同时纳入主题色示例并检查六组封面名称：

    python "<skill_dir>/scripts/subset-cover-font.py" \
      "<skill_dir>/assets/template-zhongguose/index.html" \
      --include-html "<skill_dir>/assets/theme-cover-gallery.html"
    python "<skill_dir>/scripts/check-cover-glyphs.py" \
      "<skill_dir>/assets/template-zhongguose/assets/fonts/zhongguose-cover.woff2" \
      --text 飞泉绿 --text 藕丝秋 --text 湘蓝 --text 绛缨 --text 鸦黄 --text 山岚

## 4. 资源与离线 / Assets and offline

- [ ] Motion 与 Lucide 本地文件、对应许可证均随模板分发。
- [ ] Local Motion and Lucide files and their licenses ship with the template.
- [ ] 已明确告知：精确 Web 字体需要 Google Fonts；断网时会回退到系统字体。
- [ ] The user is told that exact web typography needs Google Fonts and falls back to system fonts offline.
- [ ] CDN 仅作为本地 Motion/Lucide 加载失败后的可选回退，不承诺完全离线等效。
- [ ] CDN is only an optional fallback after local Motion/Lucide loading fails; fully equivalent offline rendering is not promised.
- [ ] 没有本机绝对路径、完整 TTF、密钥或个人信息。
- [ ] No machine-specific path, full TTF, secret, or personal information ships.
- [ ] OFL-1.1.txt 与 FONT-NOTICE.txt 位于 WOFF2 同目录。
- [ ] OFL-1.1.txt and FONT-NOTICE.txt sit beside the WOFF2.

## 5. 浏览器与交互 / Browser and interaction

执行：

    node "<skill_dir>/scripts/browser-qa.mjs" "path/to/index.html"

- [ ] 1920×1080 无横向或纵向溢出。
- [ ] No overflow at 1920×1080.
- [ ] 1366×768 无横向或纵向溢出。
- [ ] No overflow at 1366×768.
- [ ] 左右、上下、PageUp、PageDown、空格、Home、End 工作正常。
- [ ] Arrow, paging, Space, Home, and End keys work.
- [ ] Esc 打开或关闭页面总览。
- [ ] Esc opens or closes the overview.
- [ ] B 切换静态模式。
- [ ] B toggles static mode.
- [ ] 浏览器 Console 没有错误，Network 没有 404。
- [ ] Browser Console has no errors and Network has no 404s.

本地预览：

    node "<skill_dir>/scripts/preview-deck.mjs" "path/to/index.html"

## 6. 交付 / Delivery

- [ ] index.html 的标题和示例内容已经替换。
- [ ] The document title and seed content are replaced.
- [ ] assets/ 只保留成稿运行所需文件。
- [ ] assets/ contains only runtime files needed by the deck.
- [ ] 断网时核心翻页、内容和本地封面字体可用；已接受系统字体回退造成的视觉差异。
- [ ] Offline, core paging, content, and the local cover font work; system-font fallback differences are accepted.
- [ ] 如果交付 PPT 参考，明确说明尚未生成 .pptx。
- [ ] If delivering PPT guidance, state clearly that no .pptx has been generated.
