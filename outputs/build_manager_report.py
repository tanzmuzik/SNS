from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE

C_ACCENT  = RGBColor(0x00, 0x72, 0xC6)
C_GREEN   = RGBColor(0x00, 0xB0, 0x50)
C_ORANGE  = RGBColor(0xFF, 0x6B, 0x00)
C_RED     = RGBColor(0xC0, 0x00, 0x00)
C_DARK    = RGBColor(0x1F, 0x1F, 0x1F)
C_GRAY    = RGBColor(0x76, 0x76, 0x76)
C_LIGHT   = RGBColor(0xF2, 0xF6, 0xFB)
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_NAVY    = RGBColor(0x00, 0x33, 0x66)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(blank)


def rect(slide, l, t, w, h, fill=None, line=None, line_w=Pt(0)):
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    s.line.width = line_w
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = line
    else:
        s.line.fill.background()
    return s


def tx(slide, text, l, t, w, h, size=14, bold=False,
        color=C_DARK, align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
    return tb


def header(slide, title, sub=""):
    rect(slide, 0, 0, 13.33, 1.0, fill=C_NAVY)
    tx(slide, title, 0.4, 0.12, 11, 0.55, size=22, bold=True, color=C_WHITE)
    if sub:
        tx(slide, sub, 0.4, 0.65, 11, 0.3, size=11,
           color=RGBColor(0xAA, 0xCC, 0xFF))


def kpi(slide, label, value, sub, l, t, w=2.9, h=1.5,
        val_color=C_ACCENT, bg=C_LIGHT):
    rect(slide, l, t, w, h, fill=bg,
         line=RGBColor(0xCC, 0xD9, 0xEA), line_w=Pt(1))
    tx(slide, label, l+0.15, t+0.08, w-0.2, 0.32, size=10, color=C_GRAY)
    tx(slide, value, l+0.15, t+0.38, w-0.2, 0.72,
       size=30, bold=True, color=val_color)
    tx(slide, sub,   l+0.15, t+1.1,  w-0.2, 0.32, size=9, color=C_GRAY)


def bar_chart(slide, title, cats, series, l, t, w, h, colors=None):
    cd = ChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    ch = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(l), Inches(t), Inches(w), Inches(h), cd).chart
    ch.has_title = True
    ch.chart_title.text_frame.text = title
    tf = ch.chart_title.text_frame
    tf.paragraphs[0].runs[0].font.size = Pt(11)
    tf.paragraphs[0].runs[0].font.bold = True
    tf.paragraphs[0].runs[0].font.color.rgb = C_DARK
    ch.has_legend = len(series) > 1
    if ch.has_legend:
        ch.legend.position = 2
        ch.legend.include_in_layout = False
    dc = [C_ACCENT, C_GREEN, C_ORANGE]
    for i, s in enumerate(ch.series):
        c = colors[i] if colors and i < len(colors) else dc[i % 3]
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = c
        s.data_labels.show_value = True
        s.data_labels.font.size = Pt(10)
        s.data_labels.font.bold = True
        s.data_labels.font.color.rgb = C_DARK
    ch.value_axis.tick_labels.font.size = Pt(9)
    ch.category_axis.tick_labels.font.size = Pt(9)
    return ch


# ─── スライド1：表紙 ───────────────────────────────
s = add_slide()
rect(s, 0, 0, 13.33, 7.5, fill=C_NAVY)
rect(s, 0, 3.8, 13.33, 3.7, fill=RGBColor(0x00, 0x22, 0x44))
tx(s, "SNS広告 月次報告", 0, 1.3, 13.33, 0.7,
   size=18, color=RGBColor(0x88, 0xBB, 0xFF),
   align=PP_ALIGN.CENTER)
tx(s, "2026年6月", 0, 2.0, 13.33, 1.4,
   size=52, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
tx(s, "報告日：2026年6月19日　　営業課", 0, 5.5, 13.33, 0.5,
   size=13, color=RGBColor(0x88, 0xBB, 0xFF), align=PP_ALIGN.CENTER)


# ─── スライド2：エグゼクティブサマリー ────────────────
s = add_slide()
header(s, "エグゼクティブサマリー", "2026/06/05〜06/17　対象：Meta広告 2キャンペーン")

# 3つのハイライトボックス
for i, (icon, title, body, bg, tc) in enumerate([
    ("✅", "初リード獲得",
     "Metaフォームキャンペーンから\n初の問い合わせ1件を獲得\n（¥4,256/件）",
     RGBColor(0xE8,0xF5,0xEE), C_GREEN),
    ("📊", "LP到達コスト半減",
     "LPV単価が前月比-50%改善\n（¥115 → ¥58）\nLPV件数も+155%増加",
     C_LIGHT, C_ACCENT),
    ("⚠", "動画継続率が課題",
     "フック率32%で引きつけながら\n継続率3.84%と低水準\n新CMで改善を図る",
     RGBColor(0xFF,0xF3,0xE8), C_ORANGE),
]):
    x = 0.4 + i * 4.3
    rect(s, x, 1.2, 4.0, 4.5, fill=bg,
         line=RGBColor(0xCC,0xD9,0xEA), line_w=Pt(1))
    tx(s, icon, x+0.2, 1.3, 0.6, 0.6, size=24)
    tx(s, title, x+0.85, 1.35, 3.0, 0.55, size=15, bold=True, color=tc)
    tx(s, body,  x+0.2,  2.0,  3.6, 2.5,  size=12, color=C_DARK)

tx(s, "▶ 直近の最優先事項：新CM（乗り換えv2）の完成・投入によりフック後の離脱を改善する",
   0.4, 6.0, 12.5, 0.5, size=11, bold=True, color=C_NAVY)


# ─── スライド3：広告パフォーマンス推移 ───────────────
s = add_slide()
header(s, "広告パフォーマンス推移", "前月同時期（5/5〜5/18）vs 今月（6/5〜6/17）")

bar_chart(s, "LPV件数（件）",
    ["前月同時期\n5/5〜5/18", "今月\n6/5〜6/17"],
    [("LPV件数", (89, 74))],
    l=0.4, t=1.1, w=3.9, h=4.5,
    colors=[RGBColor(0x99,0xBB,0xDD), C_ACCENT])

bar_chart(s, "LPV単価（円）",
    ["前月同時期\n5/5〜5/18", "今月\n6/5〜6/17"],
    [("LPV単価", (49, 58))],
    l=4.6, t=1.1, w=3.9, h=4.5,
    colors=[RGBColor(0x99,0xBB,0xDD), C_ORANGE])

bar_chart(s, "フォームリード（件）",
    ["前月同時期\n5/5〜5/18", "今月\n6/5〜6/17"],
    [("リード", (0, 1))],
    l=8.8, t=1.1, w=4.1, h=4.5,
    colors=[RGBColor(0x99,0xBB,0xDD), C_GREEN])

tx(s, "※ 今月は2キャンペーン体制（LPV+フォーム）。消化金額は前月¥4,321→今月¥8,537（2キャンペーン合計）。",
   0.4, 5.85, 12.5, 0.4, size=9, color=C_GRAY)


# ─── スライド4：A/Bテスト結果 ─────────────────────
s = add_slide()
header(s, "A/Bテスト：LP経由 vs Meta直接フォーム")

# 左：LP経由
rect(s, 0.4, 1.1, 5.8, 5.2, fill=C_LIGHT,
     line=RGBColor(0xCC,0xD9,0xEA), line_w=Pt(1))
tx(s, "パターンA　LP経由", 0.55, 1.18, 5.5, 0.45,
   size=14, bold=True, color=C_ACCENT)
tx(s, "広告　→　LP　→　問い合わせフォーム", 0.6, 1.62, 5.3, 0.35,
   size=11, color=C_GRAY)

for row, (k, v) in enumerate([
    ("消化金額", "¥4,281"),
    ("LP到達数", "74件"),
    ("メール問い合わせ", "0件"),
    ("リード単価", "—"),
]):
    y = 2.1 + row * 0.72
    rect(s, 0.5, y, 5.6, 0.65,
         fill=C_WHITE if row%2 else C_LIGHT,
         line=RGBColor(0xCC,0xD9,0xEA), line_w=Pt(0.5))
    tx(s, k, 0.65, y+0.12, 3.0, 0.42, size=11, color=C_GRAY)
    tx(s, v, 3.8, y+0.10, 2.2, 0.45, size=13, bold=True,
       color=C_DARK, align=PP_ALIGN.RIGHT)

tx(s, "LPに74件誘導するも問い合わせゼロ",
   0.5, 5.0, 5.6, 0.4, size=11, bold=True, color=C_RED)

# 右：直接フォーム
rect(s, 6.8, 1.1, 6.1, 5.2, fill=RGBColor(0xE8,0xF5,0xEE),
     line=C_GREEN, line_w=Pt(2))
tx(s, "パターンB　Meta直接フォーム  ★", 6.95, 1.18, 5.8, 0.45,
   size=14, bold=True, color=C_GREEN)
tx(s, "広告　→　Meta上のフォームで直接獲得", 7.0, 1.62, 5.6, 0.35,
   size=11, color=C_GRAY)

for row, (k, v) in enumerate([
    ("消化金額", "¥4,256"),
    ("フォームリード", "★ 1件"),
    ("リード単価", "¥4,256"),
    ("動画継続率", "13.29%（全体最高）"),
]):
    y = 2.1 + row * 0.72
    rect(s, 6.9, y, 5.8, 0.65,
         fill=C_WHITE if row%2 else RGBColor(0xE8,0xF5,0xEE),
         line=RGBColor(0xCC,0xD9,0xEA), line_w=Pt(0.5))
    tx(s, k, 7.05, y+0.12, 3.2, 0.42, size=11, color=C_GRAY)
    tx(s, v, 10.4, y+0.10, 2.2, 0.45, size=13, bold=True,
       color=C_GREEN if "★" in v else C_DARK, align=PP_ALIGN.RIGHT)

tx(s, "直接フォームが初リード獲得  ＝ 優位",
   6.9, 5.0, 5.8, 0.4, size=11, bold=True, color=C_GREEN)

tx(s,
   "※ まだサンプル1件のため断定は早い。2〜3週間データを積んだ後に予算配分を判断する。",
   0.4, 6.4, 12.5, 0.4, size=9, color=C_GRAY)


# ─── スライド5：動画パフォーマンス比較 ───────────────
s = add_slide()
header(s, "動画パフォーマンス比較（フック率・継続率）")

bar_chart(s, "フック率（%）― 冒頭3秒で止まった割合",
    ["前作A\n(参考)", "前作B\n(参考)", "今月LPV\n(駆けつけ)", "今月FO\n(桜島)"],
    [("フック率", (31, 24, 32, 24))],
    l=0.4, t=1.1, w=5.8, h=4.5,
    colors=[RGBColor(0xCC,0xCC,0xCC), RGBColor(0xCC,0xCC,0xCC),
            C_ACCENT, C_GREEN])

bar_chart(s, "継続率（%）― 動画を最後まで観た割合",
    ["前作A\n(参考)", "前作B\n(参考)", "今月LPV\n(駆けつけ)", "今月FO\n(桜島)"],
    [("継続率", (6, 6, 3.84, 13.29))],
    l=6.8, t=1.1, w=6.1, h=4.5,
    colors=[RGBColor(0xCC,0xCC,0xCC), RGBColor(0xCC,0xCC,0xCC),
            C_ORANGE, C_GREEN])

rect(s, 0.4, 5.85, 12.5, 1.3, fill=RGBColor(0xFF,0xF3,0xE8),
     line=C_ORANGE, line_w=Pt(1))
tx(s, "⚠ 課題：フックした後の中盤離脱",
   0.6, 5.9, 5, 0.38, size=12, bold=True, color=C_ORANGE)
tx(s,
   "LPVキャンペーンはフック率32%（過去最高）ながら継続率3.84%（最低水準）。"
   "冒頭で引きつけた視聴者の大半が4秒以降に離脱。"
   "制作中の新CM（乗り換えv2）で中盤構成を強化し、継続率の改善を図る。",
   0.6, 6.28, 12.1, 0.8, size=10, color=C_DARK)


# ─── スライド6：次のアクション ────────────────────
s = add_slide()
header(s, "次のアクション")

actions = [
    ("🔴 最優先", "新CM（乗り換えv2）を完成させてLPVキャンペーンへ投入",
     "フック後の離脱を改善し継続率を前作6%以上へ回復させる", C_RED),
    ("🔴 最優先", "v2投入後3〜4日でフック率・継続率を前作と比較",
     "改善が確認できればパターンAも差し替え", C_RED),
    ("🟡 次点",   "フォームリードの継続観察",
     "現状1件。2〜3件以上獲得できれば直接フォームへの予算シフトを検討する", C_ORANGE),
    ("🟢 中期",   "継続率・リード数が改善を確認後に予算増額を判断",
     "現状¥320/日×2キャンペーン。データが揃ってから増額が鉄則", C_GREEN),
]

for i, (priority, task, detail, color) in enumerate(actions):
    y = 1.15 + i * 1.45
    rect(s, 0.4, y, 1.6, 1.2, fill=color)
    tx(s, priority, 0.42, y+0.32, 1.55, 0.55,
       size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    rect(s, 2.2, y, 10.7, 1.2, fill=C_LIGHT,
         line=RGBColor(0xCC,0xD9,0xEA), line_w=Pt(1))
    tx(s, task,   2.35, y+0.08, 10.4, 0.48, size=13, bold=True, color=C_DARK)
    tx(s, detail, 2.35, y+0.58, 10.4, 0.55, size=11, color=C_GRAY)


out = r"c:\Users\fukuyama\Claude Code\SNS\outputs\上長報告_2026-06-19.pptx"
prs.save(out)
print("saved:", out)
