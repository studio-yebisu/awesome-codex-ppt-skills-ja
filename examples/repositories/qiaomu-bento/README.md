# 社内検索を4週間で試す

原典: https://github.com/joeseesun/qiaomu-bento-ppt/tree/55c63c836f42bc9175757d077428c395cd93effe

原典の固定Bento shell・文書スキーマを使用。bento_deck.pyでJSONを検証し、シェルを変えずに編集版と再生版の.bento.htmlを構築。検索の同一要素が権限確認から回答へ移るmorphを制作。

    python M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\actual-upstreams\joeseesun__qiaomu-bento-ppt\scripts\bento_deck.py locate
    python M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\actual-upstreams\joeseesun__qiaomu-bento-ppt\scripts\bento_deck.py build M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\deck.json --output M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\deck.bento.html --identity-source M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\deck.bento.html --overwrite --report M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\source\bento-validation.json
    python M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\actual-upstreams\joeseesun__qiaomu-bento-ppt\scripts\bento_deck.py extract M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\deck.bento.html --output M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\deck.json --overwrite
    python M:\Codex\Projects\awesome-codex-ppt-skills-ja\.build\actual-upstreams\joeseesun__qiaomu-bento-ppt\scripts\bento_deck.py build M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\player.json --identity-source M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\deck.bento.html --output M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\player.bento.html --overwrite --report M:\Codex\Projects\awesome-codex-ppt-skills-ja\examples\repositories\qiaomu-bento\source\player-validation.json

入力: input/data.json。出典・実行の記録: PROVENANCE.json。確認範囲: QA.json。原典の条件: LICENSE.upstream。日本語書体: fonts/OFL.txt。
