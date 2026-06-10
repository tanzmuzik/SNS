# SNS CM動画制作パイプライン

## プロジェクト概要
Facebook・Instagram・YouTube向けのSNS用CM動画を月1〜4本制作するためのAIエージェントチームです。
縦型動画（9:16）メインで、各プラットフォームに最適化した投稿設定まで一気通貫で出力します。

## ディレクトリ構成
```
sns-cm-pipeline/
├── CLAUDE.md              # このファイル（エージェント定義・ルール）
├── agents/                # 各エージェントのシステムプロンプト定義
│   ├── producer.md
│   ├── creative-director.md
│   ├── copywriter.md
│   ├── storyboard-artist.md
│   ├── asset-director.md
│   └── sns-optimizer.md
├── briefs/                # ブリーフ入力ファイル（案件ごとに作成）
│   └── brief-template.md
└── outputs/               # 生成された制作物
    └── YYYY-MM-案件名/
        ├── concept.md
        ├── script.md
        ├── storyboard.md
        ├── asset-prompts.md
        └── posting-settings.md
```

## パイプラインの起動方法

### 新規案件の開始
```
/run-pipeline briefs/brief-template.md
```
または、ブリーフファイルを指定して：
```
ブリーフ: briefs/[案件名].md を読み込んで、SNS CMパイプラインを全工程実行してください
```

### 個別エージェントの実行
各エージェントの定義は `agents/` フォルダ内を参照。
「[エージェント名]として、[タスク]を実行してください」で個別起動可能。

## エージェント定義（ロール一覧）

### 1. プロデューサー (Producer)
- **役割**: 全体進行管理・品質チェック・最終承認
- **入力**: ブリーフ
- **出力**: 制作ブリーフ（整理済み）、各エージェントへの指示、最終チェックリスト
- **詳細**: `agents/producer.md`

### 2. クリエイティブディレクター (Creative Director)
- **役割**: コンセプト立案・ブランドトーン管理
- **入力**: 制作ブリーフ
- **出力**: コンセプト3案（各案に方向性・ターゲット感情・差別化ポイントを記載）
- **詳細**: `agents/creative-director.md`

### 3. コピーライター (Copywriter)
- **役割**: 脚本・ナレーション・テロップ原稿の作成
- **入力**: 選定コンセプト
- **出力**: 台本（15秒・30秒・60秒の3バージョン、秒数タイムライン付き）
- **詳細**: `agents/copywriter.md`

### 4. 絵コンテアーティスト (Storyboard Artist)
- **役割**: 画面構成の言語的設計
- **入力**: 台本
- **出力**: シーン別絵コンテ（カメラアングル・テロップ位置・トランジション指示含む）
- **詳細**: `agents/storyboard-artist.md`

### 5. 素材ディレクター (Asset Director)
- **役割**: AI動画・画像生成ツール向けプロンプト最適化
- **入力**: 絵コンテ
- **出力**: シーン別生成プロンプト集（Sora/Runway/Pika対応）
- **詳細**: `agents/asset-director.md`

### 6. SNSオプティマイザー (SNS Optimizer)
- **役割**: 各プラットフォーム向け最適化
- **入力**: 完成した制作物
- **出力**: 投稿設定シート（FB・Instagram・YouTube別）
- **詳細**: `agents/sns-optimizer.md`

## 品質基準
- 縦型動画: 9:16比率を前提に設計
- テロップ: 上下15%はセーフゾーン（UIに隠れる）
- 動画長: Instagram Reels=最大90秒、Facebook=最大60秒推奨、YouTube Shorts=最大60秒
- ブランドトーン: ブリーフに記載のトーンを必ず遵守
- CTA: 必ず各動画に1つ明確なCTAを含める
