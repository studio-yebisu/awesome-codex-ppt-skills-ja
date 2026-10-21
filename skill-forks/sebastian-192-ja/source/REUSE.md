# 自分の原稿から作る

1. input/BRIEF.mdを目的・読み手・元資料・枚数・納品範囲で書き換え、同じ項目でinput/deck-spec.mdへ頁別内容稿を書く。元資料にない効果や数値を加えない。
2. 原典のsource/upstream/SKILL.mdとreferencesの作風総覧規則を読み、同じ代表頁と同じ確定文字を使って4案を別々に宿主imagegenへ依頼する。source/style-options.jsonは4案の参照形式、source/styles/はこの作例の入力例。内部の各頁も16:9で生成し確認する。
3. 4案から利用者が選ぶ。明示的な委任がある場合は代理選択を記録する。選択案の画像・文字・色・字体・余白をpage-spec.jsonのstyle.tokensとreference_imagesへ保存する。
4. source/upstream/scripts/validate_page_spec.py page-spec.json --strictで構造を確かめ、頁別の確定文字と選択案を画像生成へ渡す。生成直後に文字・図の関係・注記・裁ち切れを確認し、失敗頁を作り直す。
5. python source/build_images.py reproduced.pptxは作成済み画像の再包装。別題材へ変えたときは画像・Page Spec・話者ノートを先に作り直す。原典render_deck.pyで完成物を実描画し、全頁を確認する。

総覧用の依頼例：『この内容稿の代表頁を同じ文字・頁順で維持し、16:9の縮略頁を含む作風案を1案作る。先行案とは配置と視覚表現を変える。凡例・出典・概念図の留保を消さない。』これを別々の4案として実行する。

現作例の総覧内部16:9は未適合。自分の制作ではこの制約を満たすまで作り直す。宿主画像生成・内容判断をPythonの再包装器が代行するわけではない。
