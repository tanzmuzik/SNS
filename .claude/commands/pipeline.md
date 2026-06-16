---
description: ブリーフファイルからSNS CM制作パイプラインを全工程実行する
argument-hint: [briefs/xxxx.md]
---

`agents/pipeline-orchestrator.md` の手順に従い、`$1` を読み込んでSNS CM制作パイプラインを全工程実行してください。

各工程（producer → creative-director → copywriter → storyboard-artist → asset-director → sns-optimizer → producer最終チェック）を順番に実行し、`outputs/[YYYY-MM-DD]-[案件名]/`（作成日を含むフォルダ名）に成果物を保存してください。

コンセプト選定（STEP2）では、推奨案を明示した上で、人間の選択を待ってから次工程へ進んでください。
