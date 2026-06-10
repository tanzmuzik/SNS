# ComfyUI 動画生成（I2V）切り替えガイド

> Flow停止を受けた代替プラン。環境：MacBook Air M5 / 16GB ユニファイドメモリ / ComfyUI導入済み
> 方針：**静止画はこれまで通りComfyUI、動画化はLTX-Videoをまず試し、難シーンはクラウドにフォールバック**

---

## 0. その前に：Flow停止の原因確認

「一日置いても生成されない」場合、故障より**AIクレジット枯渇**の可能性が高い。

- Google FlowはGoogle One AI（Pro/Ultra）の月間AIクレジット制。使い切ると**翌月のリセットまで生成不可**（1日待っても回復しない）
- 確認場所：Flow画面右上のクレジット残高 / Google Oneの特典ページ
- クレジット切れなら：リセット日を確認。リセット後はFlow続行が品質的には最有力

→ 並行してComfyUI体制を整えるのが正解（以下）。

---

## 1. モデル選定（M5 Air 16GB向け）

| 候補 | 評価 | 理由 |
|---|---|---|
| **LTX-Video（distilled）** | ◎ まず試す | 軽量・少ステップで高速。16GBで現実的に回る。縦9:16対応 |
| **Wan 2.2 5B（GGUF量子化）** | ○ 品質バックアップ | 品質はLTXより上だが1クリップ数十分覚悟。ヒーローカットのみ |
| Wan 2.2 14B | ✕ | 16GBユニファイドメモリでは実用外 |
| AnimateDiff（SD1.5） | ✕ | 写実CM品質に届かない |

### M5 Air特有の注意

- ファンレスのため長時間生成で**サーマルスロットリング**が起きる。クリップ間に休憩を挟む／冷えた状態で回す
- メモリ16GBは画像生成と共有。生成中は他アプリ（ブラウザ等）を閉じる
- VAEデコードでメモリが跳ねる：**Tiled VAE Decode**ノードを使う
- 解像度は欲張らない：**480×832（9:16）で生成 → 編集時にアップスケール**（Topaz/Premiere内蔵でOK）

### 推奨生成設定（LTX-Video）

| 項目 | 値 |
|---|---|
| 解像度 | 480×832（仕上げでアップスケール） |
| フレーム | 97〜121フレーム @ 24fps（約4〜5秒） |
| ワークフロー | ComfyUI公式テンプレート「LTX-Video Image to Video」 |
| 入力画像 | Anima Baseで生成済みの各シーン静止画 |

---

## 2. シーン別プロンプト（LTX-Video / Wan共通・I2V用）

> LTXは「何がどう動くか」を文章で具体的に書くと安定する。
> 各プロンプトはFlow版を I2V向けに変換済み。入力静止画＋このテキストで生成。

### 共通ネガティブプロンプト
```
worst quality, blurry, jittery, warped hands, extra fingers,
morphing objects, text artifacts, flickering, sudden cuts,
fast camera movement, distorted face
```

### Scene ①｜手元・日常（6秒 → 5秒生成し編集で調整）
```
A pair of hands rests quietly on a wooden table beside a face-down
smartphone. The fingers shift very slightly, a small restless movement.
The camera pushes in toward the hands extremely slowly and smoothly.
Soft natural daylight, calm still atmosphere, minimal motion overall.
```

### Scene ②A｜混雑中の画面（4秒）⚠️ 画面は無地発光のまま動かす
```
A smartphone screen glows softly in a dim room. The glow flickers
very subtly as if the display is waiting. Nothing else moves.
The camera pushes in toward the screen at a constant, very slow,
perfectly straight pace. Cold blue-grey lighting, tense stillness.
```
> 文言「ただいま大変混み合っています」は引き続きCanva合成。push-in等速厳守

### Scene ②B｜LINEを打つ手元（4秒）
```
Hands type short messages on a smartphone keyboard in a dim room.
The typing is mechanical and steady, without emotion. Only the
fingers and thumbs move. The camera stays completely fixed.
Dim indoor lighting, repetitive weary mood.
```

### Scene ③A｜電話サポート（4秒）
```
A friendly call center staff member wearing a headset picks up
the phone immediately and begins speaking with a warm smile,
nodding slightly. The camera slowly pulls back from medium shot.
Bright warm office lighting, welcoming professional atmosphere.
```

### Scene ③B｜駆けつけ（4秒）★いきなり車両到着案を本命に
```
A clean service van pulls up smoothly and stops in front of a
Japanese apartment building. The sliding door opens. The camera
holds a steady wide shot with a slight slow push-in as the van stops.
Bright daylight, dependable and prompt atmosphere.
```
> ローカル生成では歩行モーションの破綻率が特に高い。
> Flowでは「徒歩→破綻なら車両」だったが、**ComfyUI体制では車両到着を第1案に昇格**

### Scene ④A｜鹿児島の空と物件（4秒）
```
A slow aerial drone view glides forward over a residential area
with apartment buildings, a volcano visible in the far distance.
The camera rises gently, revealing more of the clear sky.
Warm golden light, open and reassuring feeling.
```
> 空撮の広域モーションは軽量モデルが苦手。**破綻したら最優先でクラウド送り**（下記）

### Scene ④B｜ロゴ＋QR（4秒）
```
（動画生成不要）
ロゴ＋QRはCanva静止画をPremiereでフェードインさせるだけ。
生成リソースを使わない。
```

---

## 3. フォールバック設計（プロデューサー判断基準）

| シーン | ローカル成功見込み | 破綻時の行き先 |
|---|---|---|
| ① 手元 | 高 | — |
| ②A 画面 | 高（動きが少ない） | — |
| ②B タイピング | 中（指の破綻に注意） | Kling（人物・手の動きに強い） |
| ③A スタッフ | 中（顔の破綻に注意） | Kling / Runway |
| ③B 車両到着 | 中 | Runway Gen-4 |
| ④A 空撮 | 低 | **最初からクラウド推奨**（Runway / Kling / Flowクレジット回復後） |

- 各シーン**リトライは2回まで**。3回目はクラウドへ。Air 16GBでリトライ沼に入ると1日溶ける
- クラウド無料枠の目安：Kling（毎日無料クレジット）、Runway（初回無料枠）
- Flowのクレジットがリセットされたら、残っていた難シーン（④A等）をFlowで仕上げるのが最短

---

## 4. 当面の進行順（推奨）

1. Flowのクレジット残高を確認（原因特定）
2. ComfyUIにLTX-Video（distilled）を導入、公式I2Vテンプレートで Scene ②A をテスト生成（最も動きが少なく成功しやすい＝環境検証に最適）
3. 成功したら ① → ②B → ③A → ③B の順に生成（簡単な順）
4. ④Aはクラウド or Flow回復待ち
5. 全素材が揃い次第、08_production-checklist.md のフェーズ4（Vrew）へ
