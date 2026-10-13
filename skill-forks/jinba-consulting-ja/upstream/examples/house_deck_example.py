#!/usr/bin/env python3
"""作例: 既存の資料へ差し込む 2 ページを、その資料のマスターの上に組む（slide-rules §8.7）。内容は架空。

  python3 examples/house_deck_example.py house.pptx pages.pptx    # house.pptx を土台に。書式はその場で測る
  python3 examples/house_deck_example.py                         # 土台なし（python-pptx の白紙）で形だけ試す

組んだあと: python3 scripts/check_deck.py pages.pptx --house house.skin.json → 目視（slide-rules §8）。
位置はインチ。高さは「行数 ×（pt × 1.2 ÷ 72）」で見積もり、1〜2 行ぶんの余裕を残す。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from deck_pptx import Deck, P  # noqa: E402


def table_page(d):
    """行＝工程・列＝観点の表。右端の列を面で立て、行見出しに番号の丸を置く。"""
    s = d.slide("経費精算の待ち時間は、承認の工程で最も長い")
    y = d.top + 0.1
    w = d.x1 - d.x0
    cols = [w * 0.24, w * 0.36, w * 0.40]   # 版面の幅は資料ごとに違うので、列は割合で決める
    rh = min(1.1, (d.bottom - y - 0.5) / 4)
    rows_data = [
        ("申請", ["申請者が領収書を撮影する", "科目と金額を手で入力する"], "AIが領収書を読み取り、\n申請者は金額を確かめる"),
        ("承認", ["上長が全件を目で確かめる", "差し戻しはメールで伝える"], "規程内の申請は自動で通し、\n上長は例外だけを見る"),
        ("支払い", ["経理が月末にまとめて処理する", "振込データを手で作る"], "承認の翌営業日に、\n経理が一括で確定する"),
        ("保管", ["部門が紙の領収書を保管する", "監査のたびに担当者が探し直す"], "電子で保管し、\n監査は検索で確かめる"),
    ]
    d.panel(s, d.x0 + cols[0] + cols[1] - 0.15, y - 0.08, cols[2] + 0.2, 0.35 + rh * len(rows_data) + 0.12)
    rows = [[None, d.bullets(now), P(after)] for _, now, after in rows_data]
    t = d.table(s, d.x0, y, cols, ["工程", "現状", "見直し後"], rows, [rh] * len(rows), x1=d.x1)
    for i, ((name, _, _), ry) in enumerate(zip(rows_data, t["ys"])):
        d.num_circle(s, d.x0, ry + (rh - 0.31) / 2, i + 1)
        d.text(s, d.x0 + 0.45, ry, cols[0] - 0.6, rh, P(name, b=True), anchor="m")
    return s


def steps_page(d):
    """矢羽の帯と、その下の段ごとの説明。比較の行には ✓ ✕ を図形で置く。"""
    s = d.slide("試行は1部門で2か月行い、効果を確かめてから全社へ広げる")
    y = d.top + 0.1
    steps = [("準備", "1か月目"), ("試行", "2〜3か月目"), ("全社展開", "4か月目以降")]
    segs = d.chevrons(s, d.x0, y, d.x1 - d.x0, 0.62,
                      [P([(a, {}), ("\n" + b, dict(sz=d.sz_dense, b=False))], b=True, c="bg1") for a, b in steps],
                      pad_left=0.3)
    notes = [
        ["規程を機械が読める形に直す", "対象の部門と承認者を決める"],
        ["営業部の申請を新しい流れで処理する", "差し戻しの件数と理由を毎週見る"],
        ["試行の数値を経営会議に報告する", "部門ごとに開始日を決める"],
    ]
    for (sx, sw), items in zip(segs, notes):
        d.text(s, sx + 0.1, y + 0.8, sw - 0.3, 1.3, d.bullets(items))
    yy = y + 2.4
    d.head(s, d.x0, yy, (d.x1 - d.x0) / 2, "全社展開へ進む条件")
    d.rule(s, yy + 0.41, heavy=True)
    checks = [("ok", "承認までの日数が試行前の半分以下になる"), ("ok", "差し戻しの割合が試行前より増えない"),
              ("ng", "規程外の申請が自動で通る（1件でも出たら止める）")]
    t = d.table(s, d.x0, yy + 0.46, [d.x1 - d.x0], None, [[None] for _ in checks], [0.42] * len(checks), x1=d.x1)
    for (mk, label), ry in zip(checks, t["ys"]):
        d.mark(s, mk, d.x0 + 0.04, ry + 0.11)
        d.text(s, d.x0 + 0.4, ry, d.x1 - d.x0 - 0.5, 0.42, P(label), anchor="m")
    return s


def build(template=None, out="pages.pptx", skin=None):
    d = Deck(template, skin)
    table_page(d)
    steps_page(d)
    d.save(out)
    return d


if __name__ == "__main__":
    a = sys.argv[1:]
    build(a[0] if len(a) > 1 else None, a[-1] if a else "pages.pptx")
    print("saved", a[-1] if a else "pages.pptx")
