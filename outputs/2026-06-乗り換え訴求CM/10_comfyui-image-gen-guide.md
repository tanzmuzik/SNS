# ComfyUI 静止画生成ガイド｜乗り換え訴求CM

> Flowの画像生成が使えなくなったため、静止画生成をComfyUIへ移行。
> 環境：MacBook Air M5 / 16GB ユニファイドメモリ（静止画生成には十分な構成）

---

## 1. モデル選定

| 候補 | 評価 | 用途 |
|---|---|---|
| **写実系SDXLチェックポイント**（RealVisXL V5 / Juggernaut XL等） | ◎ 本命 | 全シーン。16GBで快適、1枚1〜2分 |
| **FLUX.1 schnell（GGUF Q4量子化）** | ○ 下書き高速化 | 4ステップ生成。構図探しに |
| **FLUX.1 dev（GGUF Q4量子化）** | ○ 品質勝負 | SDXLで質感が足りないシーンのみ。1枚数分 |
| Anima Base（導入済み） | △ | アニメ・イラスト寄りなら今回の写実CMには不向き。要確認 |

> 手持ちのAnima Baseが写実系でない場合は、写実系SDXLチェックポイントを1つ追加導入するのが最短。

## 2. 共通設定（SDXL系）

| 項目 | 値 |
|---|---|
| 解像度 | **768×1344**（SDXL標準の9:16バケット） |
| サンプラー | DPM++ 2M Karras |
| ステップ | 26〜30 |
| CFG | 5〜7 |
| 共通ネガティブ | 下記 |

```
(anime, cartoon, illustration, painting, 3d render:1.3),
deformed hands, extra fingers, fused fingers, bad anatomy,
text, watermark, logo, low quality, blurry, oversaturated
```

> FLUXを使う場合：ネガティブプロンプト不要（guidance 3.5前後）。プロンプトはそのまま流用可。

### Macでの運用メモ

- 生成中はブラウザ等を閉じてメモリを空ける（16GB共有のため）
- 連続生成で本体が熱くなったら小休止（ファンレスのスロットリング対策）
- 各シーン**4〜6枚生成して選ぶ**。動画化の入力に使うため、破綻のない1枚を厳選

---

## 3. シーン別プロンプト（コピペ用・positive）

### Scene ①｜手元・日常
```
photograph, close-up of a Japanese person's hands resting on a wooden table,
smartphone placed face-down beside the hands, warm natural daylight from a window,
calm everyday atmosphere, no face visible, shallow depth of field,
quiet moment before something happens, photorealistic, high detail skin texture
```

### Scene ②A｜スマホ画面（⚠️ 画面は無地発光・文字なし。文言はCanva合成）
```
photograph, close-up of a smartphone on a table in a dim room,
screen glowing softly with a plain bright blank interface, no text on screen,
cold blue-grey ambient lighting, the glow illuminating nearby surfaces,
tense suffocating atmosphere, photorealistic, shallow depth of field
```
> チェック項目：画面が平面で歪んでいないこと（後のコーナーピン合成のため）

### Scene ②B｜LINEを打つ手元
```
photograph, close-up of hands typing on a smartphone,
messaging app layout visible on screen, mechanical weary posture of fingers,
dim warm indoor lighting at evening, sense of repetitive obligation,
photorealistic, high detail hands, natural skin texture
```
> 最重要チェック：指の本数。破綻したらシード変更で再生成

### Scene ③A｜電話サポート
```
photograph, medium shot of a friendly Japanese female call center staff
wearing a headset, picking up a phone call with a warm genuine smile,
bright clean modern office, warm welcoming lighting,
professional and responsive atmosphere, photorealistic, natural skin texture
```
> チェック項目：顔と歯の自然さ。ここだけFLUX devに切り替える価値あり

### Scene ③B｜駆けつけ（本命：車両到着）
```
photograph, wide shot of a clean white service van parked in front of
a Japanese apartment building entrance, side door open showing tools inside,
bright daytime, residential street in Kagoshima Japan,
sense of prompt reliable arrival, photorealistic
```

### Scene ③B 予備｜徒歩到着
```
photograph, wide shot of a Japanese technician in clean work uniform
arriving at an apartment building entrance, carrying a tool bag,
purposeful reliable posture, bright daytime residential area in Japan,
trustworthy atmosphere, photorealistic
```

### Scene ④A｜鹿児島の空と物件
```
photograph, aerial wide view over a residential area in Kagoshima Japan,
several mid-rise apartment buildings, clear blue sky,
Sakurajima volcano visible on the horizon across the bay,
warm golden hour light, open reassuring mood, photorealistic landscape
```

### Scene ④B｜ロゴ＋QR
```
（生成不要）Canvaで作成：シナプス光ロゴ＋QRコード＋白背景
```

---

## 4. 生成順（推奨）

1. **②A**（最も簡単・環境テストを兼ねる）
2. **③B 車両**・**④A**（人物なし・破綻リスク低）
3. **①**・**②B**（手の破綻チェックが必要）
4. **③A**（顔あり・最難関。SDXLで不満ならFLUX dev）

全シーンの「採用1枚」が揃ったら、09_comfyui-i2v-guide.md（動画化）またはFlow復旧後の動画化へ。
