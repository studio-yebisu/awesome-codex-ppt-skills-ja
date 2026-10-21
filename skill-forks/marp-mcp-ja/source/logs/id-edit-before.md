---
marp: true
theme: default
header: ''
paginate: true
style: |

  /* ===== Minimal Style for Marp ===== */

  /* --- Minimal Title --- */
  section.min-title {
    background: #111827;
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.min-title h1 {
    color: #ffffff;
    font-size: 2.5em;
    font-weight: 700;
    margin-bottom: 0.3em;
  }
  section.min-title p {
    color: rgba(255,255,255,0.7);
    font-size: 1.1em;
  }

  /* --- Minimal Section --- */
  section.min-section {
    background: #111827;
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.min-section h2 {
    color: #ffffff;
    font-size: 2em;
  }
  section.min-section p {
    color: rgba(255,255,255,0.7);
  }

  /* --- Minimal Table --- */
  section.min-table table {
    border-collapse: collapse;
    width: 100%;
    margin: 1rem auto;
    font-size: 0.9em;
  }
  section.min-table thead th {
    background: #111827;
    color: #ffffff;
    padding: 0.7rem 1rem;
    font-weight: 600;
    border: 1px solid #111827;
    text-align: left;
  }
  section.min-table tbody td {
    padding: 0.6rem 1rem;
    color: #111827;
    border: 1px solid #e5e7eb;
    text-align: left;
  }
  section.min-table tbody tr:nth-child(even) {
    background: #f9fafb;
  }

  /* --- Minimal Image Right --- */
  .min-split {
    display: grid;
    grid-template-columns: 3fr 2fr;
    gap: 1.5rem;
    align-items: center;
    margin-top: 1rem;
  }
  .min-split img {
    width: 100%;
    object-fit: cover;
  }
  .min-split-content ul {
    padding-left: 1.2rem;
  }
  .min-split-content li {
    margin-bottom: 0.4rem;
    color: #111827;
  }

  /* --- Minimal Image Center --- */
  section.min-img-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .min-image-center-wrap {
    text-align: center;
    margin-top: 1rem;
  }
  .min-image-center-wrap img {
    max-height: 380px;
    object-fit: contain;
  }

  /* --- Minimal Quote --- */
  section.min-quote {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  section.min-quote blockquote {
    border-left: 3px solid #2563eb;
    padding: 1.2rem 1.8rem;
    margin: 1rem auto;
    max-width: 85%;
    font-size: 1.2em;
    font-style: italic;
    color: #374151;
    background: transparent;
  }
  section.min-quote blockquote p:last-child {
    font-style: normal;
    font-size: 0.85em;
    color: #6b7280;
    margin-top: 0.5rem;
  }

  /* --- Minimal Two Column --- */
  .min-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 1rem;
  }
  .min-2col-left {
    border-right: 1px solid #e5e7eb;
    padding-right: 1.5rem;
  }
  .min-2col-right {
    padding-left: 0.5rem;
  }
  .min-2col h3 {
    color: #111827;
    font-size: 1em;
    margin-top: 0;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 0.3rem;
  }
  .min-2col ul {
    padding-left: 1.2rem;
    margin: 0;
  }
  .min-2col li {
    margin-bottom: 0.3rem;
    color: #374151;
  }

  /* --- Minimal Big Statement --- */
  section.min-statement {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: #ffffff;
  }
  section.min-statement h1 {
    color: #111827;
    font-size: 3em;
    font-weight: 800;
    line-height: 1.1;
    max-width: 80%;
  }
  section.min-statement p {
    color: #6b7280;
    font-size: 1.1em;
    margin-top: 0.5rem;
  }

  /* --- Minimal Statistics --- */
  .min-stat-box {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1rem;
    flex-wrap: wrap;
  }
  .min-stat-box > div {
    text-align: center;
    min-width: 140px;
    flex: 1 1 calc(33.333% - 1.5rem);
    max-width: calc(50% - 1rem);
    padding: 1rem 1.5rem;
    border-bottom: 2px solid #111827;
  }
  .min-stat-number {
    font-size: 2.4em;
    font-weight: 800;
    color: #111827;
    line-height: 1.1;
  }
  .min-stat-label {
    font-size: 0.85em;
    color: #6b7280;
    margin-top: 0.3rem;
  }

  /* --- Minimal Highlight Box --- */
  .min-highlight {
    background: #111827;
    color: #ffffff;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem auto;
    max-width: 80%;
  }
  .min-highlight h3 {
    margin-top: 0;
    font-size: 1.3em;
    color: #ffffff;
  }
  .min-highlight p {
    margin-bottom: 0;
    font-size: 1.05em;
    color: rgba(255,255,255,0.85);
  }

  /* --- Minimal Pull Quote --- */
  section.min-pull-quote {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: #ffffff;
  }
  .min-pull-quote-wrap {
    max-width: 80%;
    position: relative;
    padding: 2rem 1rem;
  }
  .min-pull-quote-wrap::before {
    content: '\201C';
    font-size: 6em;
    color: rgba(17,24,39,0.08);
    position: absolute;
    top: -0.3em;
    left: -0.1em;
    line-height: 1;
    font-family: Georgia, serif;
  }
  .min-pull-quote-text {
    font-size: 1.6em;
    font-weight: 600;
    color: #111827;
    line-height: 1.3;
    font-style: italic;
  }
  .min-pull-quote-attr {
    font-size: 1em;
    color: #111827;
    margin-top: 0.8rem;
    font-weight: 600;
  }
  .min-pull-quote-ctx {
    font-size: 0.85em;
    color: #6b7280;
    margin-top: 0.3rem;
  }

  /* --- Minimal Image Caption --- */
  .min-image-caption {
    font-size: 0.8em;
    color: #6b7280;
    text-align: center;
    margin-top: 0.5rem;
  }

  /* --- Minimal Agenda --- */
  .min-agenda-subtitle {
    color: #6b7280;
    font-size: 0.9em;
    margin: -0.5rem 0 0.5rem 0;
  }
  .min-agenda {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }
  .min-agenda-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid #e5e7eb;
  }
  .min-agenda-item:last-child {
    border-bottom: none;
  }
  .min-agenda-num {
    font-family: monospace;
    font-size: 1em;
    font-weight: 700;
    color: #111827;
    min-width: 2rem;
    flex-shrink: 0;
  }
  .min-agenda-title {
    flex: 1;
    font-size: 0.95em;
    color: #1f2937;
  }
  .min-agenda-dur {
    font-size: 0.8em;
    color: #6b7280;
    flex-shrink: 0;
    background: #f3f4f6;
    padding: 0.1rem 0.5rem;
    border-radius: 4px;
  }

  /* --- Minimal Comparison --- */
  .min-compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    margin-top: 0.5rem;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
  }
  .min-compare-panel {
    padding: 1rem 1.2rem;
  }
  .min-compare-panel:first-child {
    border-right: 1px solid #e5e7eb;
  }
  .min-compare-title {
    font-size: 0.85em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #374151;
    margin: 0 0 0.7rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #111827;
  }
  .min-compare-panel ul {
    margin: 0;
    padding-left: 1.2rem;
  }
  .min-compare-panel li {
    font-size: 0.9em;
    color: #374151;
    margin-bottom: 0.3rem;
  }
---

<!-- slide-id: 6eab75b8-400d-463b-b8ff-bac1d363d691 -->

<!-- _class: min-title -->

# ひとつの服を、<br>もう一度。

衣服お直しワークショップ<br><small>架空の企画案 / 開催日時・会場は未定</small>

---

<!-- slide-id: bb37fa6e-4c5f-4251-992a-3abad125981f -->

## 一着と、ひとつの気がかり。

<div class="min-2col">
<div class="min-2col-left">
<h3>持ってくるもの</h3><ul>
<li>洗濯した、直したい服を一着</li>
<li>気になる箇所のメモ</li>
<li>持ち帰るための袋</li>
</ul>
</div>
<div class="min-2col-right">
<h3>会場で用意するもの</h3><ul>
<li>基本の道具と材料</li>
<li>相談できる案内役</li>
<li>作業と記録のスペース</li>
</ul>
</div>
</div>

<!--
架空の企画案。具体的な道具・材料の適合は運営側で確認する。参加者に技法手順を指示する資料ではない。
-->

---

<!-- slide-id: 941a5484-4052-4c0e-b730-7713a5d5247d -->

## 見つけて、相談し、試して、記録する。

<div class="journey"><div><b>01</b><h3>見つける</h3><p>気になる箇所を共有</p><span>20 min</span></div><div><b>02</b><h3>相談する</h3><p>今日の範囲を決める</p><span>20 min</span></div><div><b>03</b><h3>試してみる</h3><p>案内役と手を動かす</p><span>60 min</span></div><div><b>04</b><h3>記録する</h3><p>次にすることを残す</p><span>20 min</span></div></div>

<div class="caption">当日の行程案 / 合計120分。作業範囲は服の状態に合わせて相談する。</div>

<!--
時間は仮の企画設定で、実測ではない。修理の完成や効果を保証する内容ではない。
-->

---

<!-- slide-id: 3c5194ee-6f93-43ce-806a-68c9fae40fb8 -->

<!-- _class: min-table -->

## 役割を、先に分けておく。

| 役割 | 当日すること | 次へ渡すもの |
| :-- | :-- | :-- |
| 参加者 | 気がかりと希望を伝える | 今日の作業範囲 |
| 案内役 | 服の状態を見て相談に応じる | 続け方と注意点 |
| 記録役 | 作業前後と次の予定を残す | 持ち帰る記録 |

架空の運営案。少人数なら案内役と記録役を兼ねる。

<!--
実在の人名・会社・運営実績は示していない。役割の仮案。
-->

---

<!-- slide-id: feeac38f-9c8c-4bf8-ab18-0874dd54fc44 -->

## 持ち帰るのは、この三つ。

<div class="takeaways"><div><span>01</span><h3>服</h3><p>今日、手を入れた一着</p></div><div><span>02</span><h3>記録</h3><p>変えた箇所と気づき</p></div><div><span>03</span><h3>次の一手</h3><p>家で続けることを一つ</p></div></div>

<div class="caption">完成していない箇所も、そのまま記録する。続きは無理のない範囲で。</div>

<!--
持ち帰る内容の企画案。完成・効果の実績ではない。
-->

---

<!-- slide-id: c7ece041-3574-4c26-ba4a-6b3f261340d5 -->

<!-- _class: min-statement -->

# 直せたところも、<br>次の一手も。

持ち帰ろう。<br><small>開催前の企画案 / 日時・会場・参加条件は未定</small>

<!--
架空の衣服お直しワークショップ企画。開催・効果・売上の実績はない。
-->