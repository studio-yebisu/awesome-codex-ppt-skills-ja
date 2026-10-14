# Third-Party Notices / 第三方说明

## qiji-font / 齊伋體

- Project: qiji-font
- Author: Lingdong Huang
- Source: https://github.com/LingDong-/qiji-font
- Upstream copyright: Copyright (c) 2020, Lingdong Huang
- License: SIL Open Font License 1.1
- Reserved Font Name: QIJI

The repository contains the pinned source archive at:

    skills/zhongguose-ppt-skill/assets/font-sources/qijic-original.ttf.gz

The Skill generates renamed WOFF2 subsets under the family name Zhongguose Cover. Generated decks must distribute OFL-1.1.txt and FONT-NOTICE.txt beside the WOFF2 file.

本仓库包含固定哈希的 qiji-font 源字体归档。Skill 会将逐稿子集改名为 Zhongguose Cover；生成的演示必须把 OFL-1.1.txt 与 FONT-NOTICE.txt 和 WOFF2 放在同一目录。

The complete OFL text and upstream notice are included at:

    skills/zhongguose-ppt-skill/assets/font-sources/OFL-1.1.txt
    skills/zhongguose-ppt-skill/assets/font-sources/FONT-NOTICE.txt

## motion@11.11.17

- Project: Motion
- Source: https://github.com/motiondivision/motion
- Bundled file: `skills/zhongguose-ppt-skill/assets/template-zhongguose/assets/motion.min.js`
- License: MIT License
- Copyright: Copyright (c) 2018 Framer B.V.
- SHA-256: `45615c1e7639fb9828942d0689c897e745690b0f6df13022223c9409fc01557c`

The complete license text is distributed at:

    skills/zhongguose-ppt-skill/assets/template-zhongguose/assets/licenses/MOTION-MIT.txt

## lucide@0.525.0

- Project: Lucide
- Source: https://github.com/lucide-icons/lucide
- Bundled file: `skills/zhongguose-ppt-skill/assets/template-zhongguose/assets/lucide.min.js`
- License: ISC License; Feather-derived icon portions use the MIT License
- Copyright: Lucide Contributors and Cole Bemis
- SHA-256: `2e8b4b1c419d4d41442a497a19b7ab5a727fefb3d25202af3c4f97d3aac14d0d`

The ISC and Feather MIT notices are distributed at:

    skills/zhongguose-ppt-skill/assets/template-zhongguose/assets/licenses/LUCIDE-ISC-AND-FEATHER-MIT.txt

## External network resources / 外部网络资源

The HTML template references Google Fonts for optional typography enhancement and jsDelivr only as a fallback if the bundled Motion or Lucide file fails to load. These remote resources are not stored in this repository. Offline use falls back to local or system assets with reduced typographic fidelity.

HTML 模板会通过 Google Fonts 增强字体效果，并仅在本地 Motion 或 Lucide 加载失败时使用 jsDelivr 回退。这些远程资源不存储在仓库中；断网时使用本地或系统资源，字体效果会有所差异。
