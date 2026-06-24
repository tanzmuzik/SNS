from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

C_ACCENT  = RGBColor(0x00, 0x72, 0xC6)
C_ACCENT2 = RGBColor(0x00, 0xB0, 0x50)
C_WARN    = RGBColor(0xFF, 0x6B, 0x00)
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_DARK    = RGBColor(0x1F, 0x1F, 0x1F)
C_GRAY    = RGBColor(0x76, 0x76, 0x76)
C_LIGHT   = RGBColor(0xF2, 0xF6, 0xFB)
C_RED     = RGBColor(0xC0, 0x00, 0x00)

path = r"c:\Users\fukuyama\Claude Code\SNS\outputs\活動報告_2026-06-05_2026-06-18.pptx"
prs = Presentation(path)
blank_layout = prs.slide_layouts[6]


def rect(slide, l, t, w, h, fill=None, line=None, line_w=Pt(0)):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.width = line_w
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
    else:
        shape.line.fill.background()
    return shape


def txbox(slide, text, l, t, w, h, size=14, bold=False, color=C_DARK,
          align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return tb


def header(slide, title, subtitle=""):
    rect(slide, 0, 0, 13.33, 1.1, fill=C_ACCENT)
    txbox(slide, title, 0.4, 0.15, 10, 0.55, size=24, bold=True, color=C_WHITE)
    if subtitle:
        txbox(slide, subtitle, 0.4, 0.68, 10, 0.35, size=13,
              color=RGBColor(0xCC, 0xE4, 0xFF))


def add_bar_chart(slide, title, categories, series_data, l, t, w, h,
                  colors=None, y_label=""):
    cd = ChartData()
    cd.categories = categories
    for name, vals in series_data:
        cd.add_series(name, vals)

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(l), Inches(t), Inches(w), Inches(h),
        cd
    ).chart

    chart.has_title = True
    chart.chart_title.text_frame.text = title
    chart.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    chart.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
    chart.chart_title.text_frame.paragraphs[0].runs[0].font.color.rgb = C_DARK

    chart.has_legend = True
    chart.legend.position = 2  # bottom
    chart.legend.include_in_layout = False

    # 系列の色設定
    default_colors = [C_ACCENT, C_ACCENT2, C_WARN]
    for i, series in enumerate(chart.series):
        c = colors[i] if colors and i < len(colors) else default_colors[i % 3]
        fill = series.format.fill
        fill.solid()
        fill.fore_color.rgb = c

        # データラベル表示
        series.data_labels.show_value = True
        series.data_labels.font.size = Pt(10)
        series.data_labels.font.bold = True
        series.data_labels.font.color.rgb = C_DARK

    # 軸フォント
    chart.value_axis.tick_labels.font.size = Pt(9)
    chart.category_axis.tick_labels.font.size = Pt(9)

    return chart


# ─────────────────────────────────────────
# 新スライド：前月同時期比較グラフ（スライド2の後に挿入）
# ─────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
header(s, "前月同時期比較", "5/5〜5/18（前月）　vs　6/5〜6/17（今月）　※LPVキャンペーン")

# ── グラフ1：LPV件数
add_bar_chart(
    s, "LPV件数（件）",
    categories=["前月同時期\n5/5〜5/18", "今月\n6/5〜6/17"],
    series_data=[("LPV件数", (89, 74))],
    l=0.4, t=1.2, w=3.8, h=4.5,
    colors=[RGBColor(0x99,0xBB,0xDD), C_ACCENT]
)

# ── グラフ2：LPV単価
add_bar_chart(
    s, "LPV単価（円）",
    categories=["前月同時期\n5/5〜5/18", "今月\n6/5〜6/17"],
    series_data=[("LPV単価", (49, 58))],
    l=4.6, t=1.2, w=3.8, h=4.5,
    colors=[RGBColor(0x99,0xBB,0xDD), C_WARN]
)

# ── グラフ3：消化金額
add_bar_chart(
    s, "消化金額（円）※今月は2キャンペーン合計",
    categories=["前月同時期\n5/5〜5/18", "今月\n6/5〜6/17"],
    series_data=[("消化金額", (4321, 8537))],
    l=8.8, t=1.2, w=4.1, h=4.5,
    colors=[RGBColor(0x99,0xBB,0xDD), C_ACCENT2]
)

# 注釈
rect(s, 0.4, 5.85, 12.5, 1.3, fill=RGBColor(0xFF,0xF3,0xE8),
     line=C_WARN, line_w=Pt(1))
txbox(s, "⚠ 読み方の注意",
      0.6, 5.9, 3, 0.35, size=11, bold=True, color=C_WARN)
txbox(s,
    "LPV件数は前月89件→今月74件で減少、単価も¥49→¥58に上昇。"
    "ただし今月は新たにフォームキャンペーンを追加しており、消化金額の増加分はそちらに投下。"
    "フォームキャンペーンで初リード1件を獲得しており、チャネル分散の効果が出始めている。",
    0.6, 6.25, 12.1, 0.8, size=10, color=C_DARK)

# スライドを2番目（KPIサマリーの後）に移動
# 現在末尾にあるので、xmlを入れ替える
from pptx.oxml.ns import qn
import copy

slides = prs.slides._sldIdLst
# 最後のスライド（今追加したもの）を index=2（3枚目）に移動
last = slides[-1]
slides.remove(last)
slides.insert(2, last)

prs.save(path)
print("saved:", path)
