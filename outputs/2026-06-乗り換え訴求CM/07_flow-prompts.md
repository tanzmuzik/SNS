# Google Flow｜画像→動画変換プロンプト（v2）

## Scene ①｜手元・日常（0〜6秒）

```
The hands rest still on the table.
After a brief pause, the fingers shift slightly
as if distracted or uncertain.
Very subtle idle movement.
Slow gentle push-in toward the hands.
Calm and quiet atmosphere,
natural light softly changing.
```

---

## Scene ②A｜混雑中の画面（6〜10秒）

```
The phone screen shows the busy hold message.
The screen's glow flickers very subtly,
as if the display is alive but nothing changes.
A loading indicator pulses slowly.
Very slow, almost imperceptible push-in toward the screen.
The near-stillness creates tension and frustration.
Cold blue-grey lighting throughout.
```

> ※v2変更：完全静止→光の微かな明滅＋ローディング表示の点滅を追加
> （完全静止はAI生成だと「止め絵」に見えるため）
>
> ※v3変更：画面の文言はCanva合成に変更。元素材は無地発光の画面で生成し、
> push-inは等速・直線的に保つこと（Premiereでのコーナーピン追従を容易にするため）。
> ローディングの点滅は合成側（Premiere）で付ける

---

## Scene ②B｜LINEを打つ手元（10〜14秒）

```
Fingers type short repetitive messages
on the smartphone keyboard.
Mechanical, automatic motion —
no hesitation, no emotion.
Camera stays fixed, close on the hands.
Dim indoor lighting, no camera movement.
```

---

## Scene ③A｜電話サポート（14〜18秒）

```
Staff member picks up the phone immediately
as if answering without delay.
Smiles and begins speaking warmly.
Slight nod of the head.
Camera slowly pulls back from medium to wider shot.
Warm lighting brightens slightly as scene opens up —
strong contrast from the cold tones of previous scenes.
```

---

## Scene ③B｜駆けつけサポート（18〜22秒）

**第1案：徒歩到着**
```
Technician in work uniform walks
purposefully toward the apartment building entrance.
Steady confident stride, carrying equipment.
Camera follows at mid-level,
slowly tracking forward alongside the technician.
Bright outdoor daylight,
sense of momentum and reliability.
```

**代替案：車両到着（歩行モーション破綻時用）**
```
A service van pulls up smoothly and stops
in front of the apartment building.
The side door slides open.
Camera holds a steady wide shot,
slight slow push-in as the van stops.
Bright outdoor daylight,
sense of prompt arrival and reliability.
```

> ※AI動画は歩行の破綻が起きやすい。第1案で失敗が続く場合は代替案を使用

---

## Scene ④A｜鹿児島の空と物件（22〜26秒）

```
Slow aerial drone shot moving forward
over Kagoshima residential area.
Apartment buildings pass below.
Sakurajima visible in the distance.
Camera gradually rises slightly,
opening up the sky.
Warm golden light,
wide and reassuring atmosphere.
```

---

## Scene ④B｜ロゴ＋QR（26〜30秒）

```
Logo and QR code fade in cleanly
on a white background.
No camera movement.
Subtle soft light pulse around the logo.
Static and clear —
easy to read, nothing distracting.
```

---

## 💡 Flow使用時のポイント

| ポイント | 内容 |
|---|---|
| 動きは控えめに | 情報伝達が目的なので過度なモーションは避ける |
| ②Aはマイクロモーションのみ | 光の明滅・ローディングの点滅程度。静止感が演出 |
| ②→③の転換 | 色温度・明るさが最も大きく変わる。つなぎは短めのカットで |
| ③Bは代替案を先に用意 | 歩行破綻のリトライで時間を溶かさないため |
| ④Bは2秒以上静止 | QRコードを読み取らせるため動きは最小限に |
