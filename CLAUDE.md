# CLAUDE.md

このファイルは、Claude Code がこのリポジトリで作業するときに参照するプロジェクト指示です。

## プロジェクト概要

SNSCMマーケティングチームのプロジェクト。

<!-- TODO: Claude.ai の「SNSCMマーケティングチーム」プロジェクトの指示文をここに貼り付けてください -->

## チームの目的・役割

<!-- TODO: チームのミッション、対象SNS、ターゲット層などを記載 -->

## 運用ルール・トーン

<!-- TODO: 投稿のトーン&マナー、NG事項、承認フローなどを記載 -->

## 参考資料

<!-- TODO: プロジェクトナレッジにあった資料は docs/ フォルダに置き、ここからリンクする -->

## エージェント構成・パイプライン

SNS CM制作パイプラインは `agents/` 配下の各エージェント定義に従い、`agents/pipeline-orchestrator.md` の手順で順番に実行する。

- `agents/producer.md` — ブリーフ整理・最終チェック
- `agents/creative-director.md` — コンセプト立案
- `agents/copywriter.md` — 台本作成
- `agents/storyboard-artist.md` — 絵コンテ作成
- `agents/asset-director.md` — AI生成プロンプト作成
- `agents/sns-optimizer.md` — SNS別投稿設定

### 使い方

```
/pipeline briefs/[ファイル名].md
```

ブリーフは `briefs/brief-template.md` を元に作成し、`briefs/` に保存する。成果物は `outputs/[YYYY-MM-DD]-[案件名]/` に保存される。
