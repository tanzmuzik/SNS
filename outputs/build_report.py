from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION

# ---- Palette: "Ocean Gradient" (trust / blue) ----
NAVY = RGBColor(0x21, 0x29, 0x5C)
DEEP_BLUE = RGBColor(0x06, 0x5A, 0x82)
TEAL = RGBColor(0x1C, 0x72, 0x93)
ICE = RGBColor(0xCA, 0xDC, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFFWHITE = RGBColor(0xF4, 0xF7, 0xFB)
DARK_TEXT = RGBColor(0x21, 0x29, 0x5C)
MUTED = RGBColor(0x5A, 0x6B, 0x8C)
ACCENT_RED = RGBColor(0xE0, 0x5A, 0x47)
ACCENT_GREEN = RGBColor(0x1F, 0x9D, 0x55)

HEADER_FONT = "游明朝"
BODY_FONT = "游ゴシック"

SW, SH = Inches(13.333), Inches(7.5)  # 16:9 wide

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
blank = prs.slide_layouts[6]


def add_slide(bg=WHITE):
    s = prs.slides.add_slide(blank)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s


def textbox(slide, x, y, w, h, text, size=14, color=DARK_TEXT, bold=False,
            font=BODY_FONT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
            line_spacing=1.15, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
    return tb


def bullet_list(slide, x, y, w, h, items, size=14, color=DARK_TEXT, font=BODY_FONT,
                space_after=8, line_spacing=1.1, bullet_color=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    bcol = bullet_color or color
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            txt, lvl = item
        else:
            txt, lvl = item, 0
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        p.level = lvl
        # bullet char via XML
        pPr = p._pPr if p._pPr is not None else p.get_or_add_pPr()
        for tag in ("a:buChar", "a:buAutoNum", "a:buNone"):
            existing = pPr.find(qn(tag))
            if existing is not None:
                pPr.remove(existing)
        buFont = pPr.makeelement(qn('a:buFont'), {'typeface': 'Arial'})
        buChar = pPr.makeelement(qn('a:buChar'), {'char': '●' if lvl == 0 else '–'})
        pPr.append(buFont)
        pPr.append(buChar)
        pPr.set('marL', str(Inches(0.25 + 0.25 * lvl)))
        pPr.set('indent', str(-Inches(0.25)))
        r = p.add_run()
        r.text = txt
        r.font.size = Pt(size if lvl == 0 else size - 1.5)
        r.font.color.rgb = color
        r.font.name = font
    return tb


def rect(slide, x, y, w, h, fill=DEEP_BLUE, line_color=None, shadow=False, radius=None):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
    sh.shadow.inherit = False
    if radius is not None:
        sh.adjustments[0] = radius
    return sh


def stat_card(slide, x, y, w, h, number, label, sub=None, accent=DEEP_BLUE, number_color=None):
    card = rect(slide, x, y, w, h, fill=OFFWHITE, radius=0.08)
    rect(slide, x, y, 0.09, h, fill=accent)
    ncolor = number_color or accent
    textbox(slide, x + 0.3, y + 0.18, w - 0.4, h * 0.55, number, size=30, color=ncolor,
            bold=True, font=HEADER_FONT, anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, x + 0.3, y + h * 0.62, w - 0.4, h * 0.22, label, size=12.5, color=DARK_TEXT,
            bold=True, anchor=MSO_ANCHOR.TOP)
    if sub:
        textbox(slide, x + 0.3, y + h * 0.80, w - 0.4, h * 0.20, sub, size=10, color=MUTED,
                anchor=MSO_ANCHOR.TOP)


def trend_chart(slide, x, y, w, h, title, categories, values, value_fmt="0",
                bar_color=DEEP_BLUE, highlight_last=True, highlight_color=ACCENT_GREEN):
    """Simple single-series column chart with data labels, styled to match the deck."""
    card = rect(slide, x, y, w, h, fill=OFFWHITE, radius=0.06)
    textbox(slide, x + 0.3, y + 0.18, w - 0.6, 0.4, title, size=14, color=NAVY, bold=True, font=HEADER_FONT)

    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series("series", values)

    cx, cy = x + 0.3, y + 0.75
    cw, ch = w - 0.6, h - 1.05
    gframe = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(cx), Inches(cy),
                                     Inches(cw), Inches(ch), chart_data)
    chart = gframe.chart
    chart.has_legend = False
    chart.has_title = False

    plot = chart.plots[0]
    plot.gap_width = 70
    plot.has_data_labels = True
    dls = plot.data_labels
    dls.font.size = Pt(13)
    dls.font.bold = True
    dls.font.color.rgb = NAVY
    dls.position = XL_LABEL_POSITION.OUTSIDE_END
    dls.number_format = value_fmt
    dls.number_format_is_linked = False

    series = plot.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = bar_color
    # color the last point distinctly to highlight the latest result
    if highlight_last:
        pt = series.points[len(values) - 1]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = highlight_color

    cat_ax = chart.category_axis
    cat_ax.tick_labels.font.size = Pt(12)
    cat_ax.tick_labels.font.color.rgb = DARK_TEXT
    cat_ax.has_major_gridlines = False
    cat_ax.format.line.color.rgb = MUTED

    val_ax = chart.value_axis
    val_ax.visible = False
    val_ax.has_major_gridlines = False
    val_ax.minimum_scale = 0


def page_number(slide, n):
    textbox(slide, 12.55, 7.05, 0.6, 0.35, str(n), size=11, color=MUTED, align=PP_ALIGN.RIGHT)


def section_title(slide, title, subtitle=None):
    textbox(slide, 0.6, 0.45, 12.0, 0.9, title, size=28, color=NAVY, bold=True, font=HEADER_FONT)
    rect(slide, 0.62, 1.28, 0.7, 0.06, fill=TEAL)
    if subtitle:
        textbox(slide, 0.6, 1.42, 12.0, 0.5, subtitle, size=13, color=MUTED, italic=True)


# =====================================================================
# SLIDE 1 - Cover
# =====================================================================
s = add_slide(bg=NAVY)
rect(s, 0, 0, 13.333, 7.5, fill=NAVY)
# Decorative diagonal-ish bands using ovals for subtle motif
circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.3), Inches(-2.6), Inches(6.5), Inches(6.5))
circ.fill.solid(); circ.fill.fore_color.rgb = DEEP_BLUE; circ.fill.transparency = 0
circ.line.fill.background(); circ.shadow.inherit = False
try:
    circ.fill.transparency = 0.55
except Exception:
    pass
circ2 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.6), Inches(4.0), Inches(4.2), Inches(4.2))
circ2.fill.solid(); circ2.fill.fore_color.rgb = TEAL
circ2.line.fill.background(); circ2.shadow.inherit = False

textbox(s, 0.9, 2.55, 9.5, 0.5, "SNS広告 月次報告", size=16, color=ICE, bold=True, font=BODY_FONT)
textbox(s, 0.9, 3.05, 11.0, 1.5, "6月のSNS広告状況報告", size=44, color=WHITE, bold=True, font=HEADER_FONT)
textbox(s, 0.9, 4.35, 10.5, 0.6, "Meta広告（Facebook / Instagram）運用状況と改善の取り組み", size=16, color=ICE)
rect(s, 0.95, 5.35, 0.55, 0.045, fill=TEAL)
textbox(s, 0.9, 5.55, 6, 0.5, "発表者：ふくやま やすひと", size=14, color=WHITE, bold=True)
textbox(s, 0.9, 5.95, 6, 0.4, "2026年6月", size=12, color=ICE)

# =====================================================================
# SLIDE 2 (NEW) - Background / context for newcomers to FB ads
# =====================================================================
s = add_slide()
section_title(s, "これまでの経緯｜広告運用の背景共有", "今回初めてご担当される方にも分かるよう、まず前提からご説明します。")

# Timeline (3 steps)
steps2 = [
    ("4月下旬", "広告運用スタート", "「マンションまるごとプラン」の\n認知拡大・サイト誘導を目的に開始"),
    ("5月", "実績分析・課題発見", "視聴離脱とフォーム不具合という\n2つの課題を特定"),
    ("6月（現在）", "改善実施・効果検証中", "フォーム修正を実施し、\n新クリエイティブの制作を推進中"),
]
tx = 0.6
tw = 4.0
for i, (when, title_, desc) in enumerate(steps2):
    fill = [DEEP_BLUE, TEAL, NAVY][i]
    rect(s, tx + i * (tw + 0.13), 2.05, tw, 1.85, fill=OFFWHITE, radius=0.07)
    rect(s, tx + i * (tw + 0.13), 2.05, tw, 0.55, fill=fill, radius=0.09)
    rect(s, tx + i * (tw + 0.13), 2.3, tw, 0.3, fill=fill)
    textbox(s, tx + i * (tw + 0.13), 2.05, tw, 0.55, when, size=14, color=WHITE, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=HEADER_FONT)
    textbox(s, tx + i * (tw + 0.13) + 0.25, 2.72, tw - 0.5, 0.4, title_, size=14, color=NAVY, bold=True)
    textbox(s, tx + i * (tw + 0.13) + 0.25, 3.12, tw - 0.5, 0.75, desc, size=11, color=DARK_TEXT, line_spacing=1.25)
    if i < len(steps2) - 1:
        textbox(s, tx + i * (tw + 0.13) + tw - 0.05, 2.05, 0.3, 1.85, "→", size=20, color=MUTED,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Two context cards: purpose / campaign structure
rect(s, 0.6, 4.15, 5.85, 1.55, fill=OFFWHITE, radius=0.06)
textbox(s, 0.9, 4.35, 5.3, 0.4, "何のために運用しているか", size=14, color=NAVY, bold=True, font=HEADER_FONT)
textbox(s, 0.9, 4.78, 5.4, 0.85,
        "鹿児島のマンションオーナー向け「マンションまるごとプラン」\n（インターネット無料設備）の認知拡大と、資料請求の獲得が目的です。",
        size=12, color=DARK_TEXT, line_spacing=1.3)

rect(s, 6.85, 4.15, 5.9, 1.55, fill=OFFWHITE, radius=0.06)
textbox(s, 7.15, 4.35, 5.4, 0.4, "2つのキャンペーンを並行運用", size=14, color=NAVY, bold=True, font=HEADER_FONT)
textbox(s, 7.15, 4.78, 5.5, 0.85,
        "① LPVキャンペーン：サイトへの誘導・認知拡大\n② リード獲得キャンペーン：資料請求フォームでの問い合わせ獲得",
        size=12, color=DARK_TEXT, line_spacing=1.3)

# Mini glossary row
textbox(s, 0.6, 5.92, 11.8, 0.35, "（参考）よく出てくる用語", size=12.5, color=MUTED, bold=True)
terms = [
    ("最適化スコア", "Metaが広告の改善余地を\n点数化した指標（100点満点）"),
    ("LPV（ランディングページビュー）", "広告から自社サイトに\n訪問された回数"),
    ("リード（フォーム）", "資料請求フォームから\n送信された問い合わせの件数"),
]
gx = 0.6
gw = 3.93
for i, (term, desc) in enumerate(terms):
    rect(s, gx + i * (gw + 0.1), 6.32, gw, 1.0, fill=ICE, radius=0.1)
    textbox(s, gx + i * (gw + 0.1) + 0.25, 6.42, gw - 0.5, 0.35, term, size=12, color=NAVY, bold=True)
    textbox(s, gx + i * (gw + 0.1) + 0.25, 6.74, gw - 0.5, 0.55, desc, size=10, color=DARK_TEXT, line_spacing=1.15)
page_number(s, 2)

# =====================================================================
# SLIDE 3 (NEW) - KPI評価（5月度報告書のフォーマットに準拠）
# =====================================================================
s = add_slide()
section_title(s, "6月のKPI評価", "目標に対する実績を5段階評価（◎○△×）で確認")

ACCENT_ORANGE = RGBColor(0xE0, 0x8E, 0x2B)

textbox(s, 0.6, 1.98, 12.0, 0.32,
        "KPI実績（集計期間：4/30〜6/7　※直近2週間データを中心に集計）",
        size=12.5, color=NAVY, bold=True)

kpi_rows = [
    ("LP到達単価（CPLPV）", "¥60〜150", "¥49〜56", "◎", ACCENT_GREEN),
    ("フック率（動画冒頭の惹きつけ）", "30%以上", "31%", "◎", ACCENT_GREEN),
    ("継続率（最後まで見た割合）", "10%以上", "約6%", "△", ACCENT_ORANGE),
    ("LP問い合わせ件数", "1件以上/月", "0件", "×", ACCENT_RED),
    ("最適化スコア（Metaの広告品質指標）", "改善傾向", "70点（前回66点）", "○", DEEP_BLUE),
    ("消化金額（4/30〜6/7累計）", "¥9,600以内/月換算", "¥11,299", "○", DEEP_BLUE),
]

n_rows = len(kpi_rows) + 1
tbl_shape = s.shapes.add_table(n_rows, 4, Inches(0.6), Inches(2.42), Inches(12.13), Inches(3.68))
table = tbl_shape.table
table.columns[0].width = Inches(4.6)
table.columns[1].width = Inches(2.8)
table.columns[2].width = Inches(2.83)
table.columns[3].width = Inches(1.9)
table.rows[0].height = Inches(0.5)
for r in range(1, n_rows):
    table.rows[r].height = Inches(0.53)

header_cells = ["指標", "目標", "実績", "評価"]
for c, txt in enumerate(header_cells):
    cell = table.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = cell.margin_right = Inches(0.15)
    p = cell.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER if c else PP_ALIGN.LEFT
    r_ = p.add_run(); r_.text = txt
    r_.font.size = Pt(13); r_.font.bold = True; r_.font.color.rgb = WHITE; r_.font.name = HEADER_FONT

for ri, (name, target, actual, icon, icon_color) in enumerate(kpi_rows, start=1):
    row_vals = [name, target, actual, icon]
    for c, txt in enumerate(row_vals):
        cell = table.cell(ri, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = OFFWHITE if ri % 2 else WHITE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.15)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if c else PP_ALIGN.LEFT
        r_ = p.add_run(); r_.text = txt
        if c == 3:
            r_.font.size = Pt(20); r_.font.bold = True; r_.font.color.rgb = icon_color
        elif c == 0:
            r_.font.size = Pt(12.5); r_.font.bold = True; r_.font.color.rgb = NAVY
        else:
            r_.font.size = Pt(12.5); r_.font.bold = False; r_.font.color.rgb = DARK_TEXT
        r_.font.name = BODY_FONT if c != 3 else HEADER_FONT

# Legend strip explaining the evaluation marks
legend_items = [
    ("◎", ACCENT_GREEN, "目標を大きく上回る"),
    ("○", DEEP_BLUE, "目標どおり／改善傾向"),
    ("△", ACCENT_ORANGE, "目標未達・改善余地あり"),
    ("×", ACCENT_RED, "目標に届かず要対策"),
]
lx = 0.6
ly = 6.45
for icon, color, desc in legend_items:
    textbox(s, lx, ly, 0.4, 0.4, icon, size=18, color=color, bold=True, font=HEADER_FONT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, lx + 0.42, ly + 0.02, 2.65, 0.4, desc, size=10.5, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
    lx += 3.05

page_number(s, 3)

# =====================================================================
# SLIDE 4 - Summary
# =====================================================================
s = add_slide()
section_title(s, "実績の推移とハイライト",
              "最適化スコアは 66点 → 70点（+4pt）に改善、LPVキャンペーンも前週比 +48.1%（27件→40件）と伸長中です。")

# Two LPV trend graphs side by side — actual screenshots from Ads Manager (日次推移をそのまま掲載)
CHARTS_DIR = r"C:\Users\fukuyama\Claude Code\sns-cm-pipeline\outputs\charts"

def chart_card(slide, x, y, w, h, title, img_path, caption):
    rect(slide, x, y, w, h, fill=OFFWHITE, radius=0.05)
    textbox(slide, x + 0.3, y + 0.16, w - 0.6, 0.36, title, size=13.5, color=NAVY, bold=True, font=HEADER_FONT)
    avail_w = w - 0.6
    # solve for image height so title + image + caption fit within the card
    pic_h = h - 0.16 - 0.36 - 0.06 - 0.34 - 0.18 - 0.16  # top pad, title, gap, caption, gap, bottom pad
    pic_w = pic_h * (640 / 255)
    if pic_w > avail_w:
        pic_w = avail_w
        pic_h = pic_w * (255 / 640)
    pic_x = x + (w - pic_w) / 2
    pic_y = y + 0.16 + 0.36 + 0.06
    slide.shapes.add_picture(img_path, Inches(pic_x), Inches(pic_y), width=Inches(pic_w), height=Inches(pic_h))
    textbox(slide, x + 0.3, pic_y + pic_h + 0.1, w - 0.6, 0.34, caption, size=10.5, color=MUTED)

# Note: A案は実績推移グラフ、B案は実績ゼロのため状況メモという「異なる種類の情報」であることを明示し、
# 同列の比較ではなく「主＝グラフで追える実績」「副＝今は数値が出ていない案件の状況共有」という構成にする。
textbox(s, 0.6, 1.97, 12.0, 0.3,
        "A案は実績を推移グラフで、B案はまだ実績が出ていないため状況メモで共有します（同じ形式での比較はできません）",
        size=10.5, color=MUTED)

# Left（メイン）: A案（LPVキャンペーン）の推移グラフ（累計期間に集約）／ 表・カードと同じ7.0インチ幅で列を揃える
chart_card(s, 0.6, 2.34, 7.0, 2.66,
           "A案｜LPVキャンペーンの推移（累計：4/30〜6/7）",
           f"{CHARTS_DIR}\\lpv_trend_cumulative_4-30_6-7.png",
           "期間合計 232件　／　LPVあたり ¥49　／　消化金額 ¥11,299")

# Right（サブ）: B案（リード獲得キャンペーン）は実績が無いため、グラフではなく状況メモとして掲載／ 4.65インチ幅でアカウント概要カードと列を揃える
rect(s, 7.85, 2.34, 4.65, 2.66, fill=NAVY, radius=0.05)
textbox(s, 8.15, 2.5, 4.05, 0.7, "B案｜リード獲得キャンペーン\n（実績ゼロのため状況メモ）", size=12.5, color=WHITE, bold=True, font=HEADER_FONT, line_spacing=1.15)
textbox(s, 8.15, 3.18, 1.7, 0.8, "0件", size=34, color=ACCENT_RED, bold=True, font=HEADER_FONT)
textbox(s, 8.15, 3.84, 4.05, 0.3, "過去7日間の獲得実績（グラフ化できる推移データなし）", size=10, color=ICE)
rect(s, 8.15, 4.26, 4.05, 0.025, fill=TEAL)
bullet_list(s, 8.15, 4.4, 4.05, 0.58, [
    "原因：フォームの言語設定不具合＋確認ステップ過多",
    "対応：言語設定とフォーム形式を修正済み",
    "見通し：来週には効果を数値で確認予定",
], size=9.5, color=WHITE, space_after=3, line_spacing=1.05)

# Bottom-left: period comparison table (mirrors the captured Ads Manager figures as-is)
textbox(s, 0.6, 5.18, 7.0, 0.32, "期間別パフォーマンス（広告管理画面の実数値）", size=12.5, color=NAVY, bold=True)
tbl_shape = s.shapes.add_table(4, 3, Inches(0.6), Inches(5.55), Inches(7.0), Inches(1.65))
table = tbl_shape.table
table.columns[0].width = Inches(2.0)
table.columns[1].width = Inches(2.5)
table.columns[2].width = Inches(2.5)
table.rows[0].height = Inches(0.5)
for r in range(1, 4):
    table.rows[r].height = Inches(0.38)

header_cells = ["指標", "直近2週間（5/27〜6/7）", "累計（4/30〜6/7）"]
body_rows = [
    ["ランディングページビュー", "55件", "232件"],
    ["LPVあたり単価", "¥56", "¥49"],
    ["消化金額", "¥3,073", "¥11,299"],
]
for c, txt in enumerate(header_cells):
    cell = table.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = DEEP_BLUE
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = cell.margin_right = Inches(0.12)
    p = cell.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER if c else PP_ALIGN.LEFT
    r_ = p.add_run(); r_.text = txt
    r_.font.size = Pt(11.5); r_.font.bold = True; r_.font.color.rgb = WHITE; r_.font.name = BODY_FONT

for ri, row in enumerate(body_rows, start=1):
    for c, txt in enumerate(row):
        cell = table.cell(ri, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = OFFWHITE if ri % 2 else WHITE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.12)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if c else PP_ALIGN.LEFT
        r_ = p.add_run(); r_.text = txt
        r_.font.size = Pt(12.5 if c else 11.5)
        r_.font.bold = bool(c)
        r_.font.color.rgb = DEEP_BLUE if c else DARK_TEXT
        r_.font.name = BODY_FONT

# Bottom-right: account-level snapshot (as shown on the overview screen)
rect(s, 7.85, 5.18, 4.65, 1.85, fill=NAVY, radius=0.07)
textbox(s, 8.15, 5.36, 4.2, 0.4, "アカウント概要（直近7日間）", size=13, color=ICE, bold=True, font=HEADER_FONT)
bullet_list(s, 8.15, 5.78, 4.25, 1.2, [
    "消化金額：¥4,196　／　アクティブなキャンペーン：2件",
    "LPVキャンペーン：40件（前週比 ↑48.1%）",
    "リード（フォーム）：0件　※直近7日間、結果なし",
], size=11.5, color=WHITE, space_after=6, line_spacing=1.15)
page_number(s, 4)

# =====================================================================
# SLIDE 5 - Two issues found
# =====================================================================
s = add_slide()
section_title(s, "発見した2つの課題", "数値の裏付けをもとに、課題を構造的に特定しました。")

# Card 1
rect(s, 0.6, 2.05, 5.85, 4.55, fill=OFFWHITE, radius=0.05)
rect(s, 0.6, 2.05, 5.85, 0.65, fill=DEEP_BLUE, radius=0.05)
rect(s, 0.6, 2.45, 5.85, 0.25, fill=DEEP_BLUE)  # square off bottom corners of header
textbox(s, 0.9, 2.05, 5.4, 0.65, "① 動画クリエイティブの離脱問題", size=15, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
bullet_list(s, 0.95, 2.95, 5.25, 3.5, [
    "冒頭4秒で視聴者の約60%が離脱",
    "フック率 31% は目標達成も、継続率 約6% に課題",
    ("原因：冒頭が「会社目線の説明」から始まり、", 0),
    ("視聴者が“自分ごと”として捉えられていない", 1),
], size=13.5, color=DARK_TEXT, space_after=10)

# Card 2
rect(s, 6.85, 2.05, 5.9, 4.55, fill=OFFWHITE, radius=0.05)
rect(s, 6.85, 2.05, 5.9, 0.65, fill=TEAL, radius=0.05)
rect(s, 6.85, 2.45, 5.9, 0.25, fill=TEAL)
textbox(s, 7.15, 2.05, 5.4, 0.65, "② リード獲得フォームの技術的不具合", size=15, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
bullet_list(s, 7.2, 2.95, 5.35, 3.5, [
    ("フォームの言語設定が English (US) のままで、", 0),
    ("送信ボタンが「Continue」と英語表示に", 1),
    ("フォームタイプも「高い意向」（確認ステップあり）", 0),
    ("で、送信のハードルが高い状態だった", 1),
], size=13.5, color=DARK_TEXT, space_after=10)
page_number(s, 5)

# =====================================================================
# SLIDE 6 - Improvement actions taken
# =====================================================================
s = add_slide()
section_title(s, "実施した改善アクション", "発見した課題に対して、即座に手を打ちました。")

steps = [
    ("1", "フォームを新規複製し、言語設定を「Japanese (Japan)」に変更"),
    ("2", "フォームタイプを「大量用」（確認ステップなし）に変更し、送信ハードルを軽減"),
    ("3", "パターンBの広告に新フォームを差し替え済み"),
    ("4", "効果反映には2〜3日のMeta学習期間が必要 — 来週には数値で確認できる見込み"),
]
y = 2.15
for i, (num, txt) in enumerate(steps):
    card_h = 1.12
    fill = DEEP_BLUE if i < 3 else TEAL
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), Inches(y + (card_h - 0.62) / 2), Inches(0.62), Inches(0.62))
    circ.fill.solid(); circ.fill.fore_color.rgb = fill
    circ.line.fill.background(); circ.shadow.inherit = False
    tf = circ.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = num
    r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = HEADER_FONT
    rect(s, 1.55, y, 10.8, card_h, fill=OFFWHITE, radius=0.08)
    style_note = "  ［効果待ち］" if i == 3 else ""
    textbox(s, 1.85, y, 10.2, card_h, txt + style_note, size=14.5, color=DARK_TEXT, anchor=MSO_ANCHOR.MIDDLE, bold=(i == 3))
    y += card_h + 0.28
page_number(s, 6)

# =====================================================================
# SLIDE 7 - Meta AI diagnostics (objective evidence)
# =====================================================================
s = add_slide()
section_title(s, "Meta AIによる新しい診断結果", "課題認識を裏付ける、客観的なベンチマークデータが得られました。")

# left card
rect(s, 0.6, 2.1, 5.85, 4.5, fill=OFFWHITE, radius=0.06)
textbox(s, 0.95, 2.4, 5.2, 0.5, "クリエイティブ診断", size=15, color=NAVY, bold=True, font=HEADER_FONT)
textbox(s, 0.95, 2.95, 5.2, 0.65, "「平均以下」", size=26, color=ACCENT_RED, bold=True, font=HEADER_FONT)
textbox(s, 0.95, 3.7, 5.25, 2.6,
        "品質・エンゲージメント率・コンバージョン率の\n"
        "すべての項目で「平均以下」と診断されました。\n\n"
        "現在のクリエイティブが、ターゲットの関心を\n"
        "十分に引けていないことを示しています。",
        size=13, color=DARK_TEXT, line_spacing=1.4)

# right card
rect(s, 6.85, 2.1, 5.9, 4.5, fill=OFFWHITE, radius=0.06)
textbox(s, 7.2, 2.4, 5.3, 0.5, "ランディングページビュー単価", size=15, color=NAVY, bold=True, font=HEADER_FONT)
textbox(s, 7.2, 2.95, 5.3, 0.65, "同業他社より +19% 高い", size=24, color=ACCENT_RED, bold=True, font=HEADER_FONT)
textbox(s, 7.2, 3.7, 5.4, 2.6,
        "類似広告セットのLPV単価の中央値 $39.00 に対し、\n"
        "自社は ¥49〜56 という結果に（広告管理画面の表示）。\n\n"
        "→ 現在制作中の新クリエイティブの必要性を\n"
        "裏付ける、客観的な根拠となります。",
        size=13, color=DARK_TEXT, line_spacing=1.4)
page_number(s, 7)

# =====================================================================
# SLIDE 8 - New CM video production
# =====================================================================
s = add_slide()
section_title(s, "今後の取り組み｜新CM動画の制作", "課題を踏まえ、新しいクリエイティブの制作を推進中です。")

# Left: brief info
rect(s, 0.6, 2.1, 5.7, 4.5, fill=OFFWHITE, radius=0.06)
textbox(s, 0.95, 2.35, 5.1, 0.4, "企画概要", size=14, color=NAVY, bold=True, font=HEADER_FONT)
bullet_list(s, 0.95, 2.85, 5.15, 3.6, [
    "ターゲット：鹿児島の個人マンションオーナー",
    "テーマ：インターネット無料設備の導入提案",
    ("フックコンセプト：", 0),
    ("「鹿児島の入居者、もうWi-Fi無しでは決めません」", 1),
    ("（空室危機への問題提起から入る構成）", 1),
], size=13, color=DARK_TEXT, space_after=10)

# Right: production flow
rect(s, 6.55, 2.1, 6.2, 4.5, fill=NAVY, radius=0.06)
textbox(s, 6.9, 2.35, 5.6, 0.4, "AIエージェントチームによる制作体制", size=14, color=WHITE, bold=True, font=HEADER_FONT)
roles = ["企画", "台本", "絵コンテ", "素材生成", "投稿最適化"]
rx = 6.9
rw = 1.06
for i, role in enumerate(roles):
    rect(s, rx + i * (rw + 0.13), 3.05, rw, 0.85, fill=DEEP_BLUE, radius=0.12)
    textbox(s, rx + i * (rw + 0.13), 3.05, rw, 0.85, role, size=11, color=WHITE, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < len(roles) - 1:
        textbox(s, rx + i * (rw + 0.13) + rw, 3.05, 0.13, 0.85, "→", size=14, color=ICE,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 6.9, 4.25, 5.6, 2.1,
        "各専門エージェントが連携し、ブリーフから台本・絵コンテ・\n"
        "AI生成プロンプト・投稿設定までを一気通貫で制作。\n\n"
        "完成後は現行クリエイティブと差し替え、\n"
        "「冒頭4秒の離脱」の改善を狙います。",
        size=13, color=ICE, line_spacing=1.4)
page_number(s, 8)

# =====================================================================
# SLIDE 9 - Schedule & summary
# =====================================================================
s = add_slide()
section_title(s, "今後のスケジュール・まとめ")

timeline = [
    ("今週〜来週", "フォーム改善の効果を数値で確認"),
    ("今月中", "新CM動画を完成させ、現行クリエイティブと差し替え"),
    ("来月以降", "結果を見ながら予算増額を検討"),
]
x = 0.6
card_w = 3.95
for i, (when, what) in enumerate(timeline):
    rect(s, x + i * (card_w + 0.18), 2.15, card_w, 2.15, fill=OFFWHITE, radius=0.07)
    rect(s, x + i * (card_w + 0.18), 2.15, card_w, 0.6, fill=[DEEP_BLUE, TEAL, NAVY][i], radius=0.07)
    rect(s, x + i * (card_w + 0.18), 2.45, card_w, 0.3, fill=[DEEP_BLUE, TEAL, NAVY][i])
    textbox(s, x + i * (card_w + 0.18), 2.15, card_w, 0.6, when, size=15, color=WHITE, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=HEADER_FONT)
    textbox(s, x + i * (card_w + 0.18) + 0.3, 2.95, card_w - 0.6, 1.25, what, size=13.5,
            color=DARK_TEXT, line_spacing=1.3)

textbox(s, 0.6, 4.75, 11.8, 0.4, "まとめ", size=16, color=NAVY, bold=True, font=HEADER_FONT)
rect(s, 0.6, 5.2, 11.8, 1.55, fill=NAVY, radius=0.06)
textbox(s, 0.95, 5.4, 11.2, 1.2,
        "「分析 → 原因特定 → 改善実施 → 新クリエイティブ制作」の一連の流れを着実に進め、\n"
        "来月の問い合わせ獲得を目指します。",
        size=15, color=WHITE, line_spacing=1.45, bold=True)
page_number(s, 9)

prs.save(r"C:\Users\fukuyama\Claude Code\sns-cm-pipeline\outputs\6月SNS広告状況報告.pptx")
print("saved")
