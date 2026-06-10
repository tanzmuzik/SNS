# 素材生成プロンプト｜AI画像生成用（v2）

## Scene ①｜日常の手元（0〜6秒）

```
Close-up of Japanese person's hands resting on table,
smartphone placed face-down beside hands,
warm natural daylight, calm everyday atmosphere,
no face visible, just hands and table,
sense of quiet before something happens,
vertical 9:16 format, photorealistic
```

---

## Scene ②A｜混雑中の画面（6〜10秒）

```
Close-up of smartphone held in hand or on table,
screen glowing softly with a plain bright UI,
no readable text on screen (blank generic interface),
cold blue-grey lighting, mostly static,
suffocating and frustrating atmosphere,
vertical 9:16 format, photorealistic
```

> ※v3変更：画面内の文字はAI生成しない（文字はAI生成の最弱点のため）。
> 画面は無地の発光状態で生成し、文言UIはCanvaで作成してPremiereで合成する。

### Canva合成用 画面UI仕様

| 項目 | 内容 |
|---|---|
| 文言 | 「ただいま大変混み合っています」＋ローディングインジケーター |
| デザイン | 汎用的なサポート画面風（実在他社のUIと一致しないこと） |
| サイズ | スマホ画面比率（生成カットの画面領域に合わせてコーナーピン変形） |
| 書き出し | 背景透過PNG。ローディング点滅はPremiere側で不透明度キーフレーム |

---

## Scene ②B｜LINEを打つ手元（10〜14秒）

```
Close-up of hands typing on smartphone,
Japanese messaging app visible,
mechanical and weary hand movement,
dim warm indoor lighting,
sense of unwanted repetitive obligation,
vertical 9:16 format, photorealistic
```

---

## Scene ③A｜電話サポート（14〜18秒）

```
Medium shot, bright Japanese call center office,
friendly female staff with headset,
phone picked up immediately, responsive expression,
warm indoor lighting, clean professional setting,
vertical 9:16 format, photorealistic
```

---

## Scene ③B｜駆けつけサポート（18〜22秒）

**第1案：徒歩到着**
```
Wide shot, Japanese technician in work uniform
arriving at apartment building entrance in Kagoshima,
carrying tools, purposeful and reliable demeanor,
daytime outdoor setting, residential area,
trustworthy and reassuring atmosphere,
vertical 9:16 format, photorealistic
```

**代替案：車両到着（歩行モーション破綻時用）**
```
Wide shot, service van parked in front of 
Japanese apartment building, side door opening,
technician's tools visible inside,
daytime outdoor setting, Kagoshima residential area,
sense of prompt arrival and reliability,
vertical 9:16 format, photorealistic
```

---

## Scene ④A｜鹿児島の空と物件（22〜26秒）

```
Aerial wide shot over Kagoshima city,
multiple apartment buildings, clear blue sky,
Sakurajima volcano visible in background,
warm golden hour lighting, open and reassuring,
sense of security and local pride,
vertical 9:16 format
```

---

## Scene ④B｜ロゴ＋QR（26〜30秒）

- シナプス光ロゴ（白背景）
- QRコード（無料資料請求LP）
- テロップ：「速度の悩みも気軽に相談　無料資料請求は下のボタンから」
