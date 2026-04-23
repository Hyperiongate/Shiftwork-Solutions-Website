"""
generate_guide_pdf.py
Shiftwork Solutions LLC — Branded Guide PDF Generator
Generates: pdfs/overtime-management-guide.pdf

Usage:  python3 generate_guide_pdf.py
Output: pdfs/overtime-management-guide.pdf  (deploy to /pdfs/ in repo root)

Created:      2026-04-23
Last Updated: 2026-04-23

CHANGE LOG:
    2026-04-23 — Initial build. Overtime Management Guide (Guide 5 of 10).
                 Cover page + 8 content pages. Branded header/footer every page.

DESIGN:
    Navy:   #1F4E79   Orange: #E8610A   Gold: #EEAE26
    Mid-blue: #85B7EB  Light-grey: #F4F6F8  Body-text: #1A1A1A
    Fonts: Helvetica (PDF built-in, no embedding required)
    Page size: Letter (8.5 x 11 in)
    Margins: 0.75in left/right, 1in top (below header), 0.85in bottom (above footer)

STRUCTURE:
    Page 1  — Cover / Brand page (logo area, firm info, process, experience)
    Page 2+ — Guide content with running header + footer
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib import colors

# ── COLOR PALETTE ─────────────────────────────────────────────────────────────
NAVY       = HexColor('#1F4E79')
NAVY_DARK  = HexColor('#0D1F3C')
MID_BLUE   = HexColor('#85B7EB')
ORANGE     = HexColor('#E8610A')
GREEN      = HexColor('#1D9E75')
GOLD       = HexColor('#EEAE26')
LIGHT_GREY = HexColor('#F4F6F8')
BORDER     = HexColor('#E0E0E0')
MUTED      = HexColor('#666666')
BODY_TEXT  = HexColor('#1A1A1A')

PAGE_W, PAGE_H = letter
MARGIN_L  = 0.75 * inch
MARGIN_R  = 0.75 * inch
MARGIN_T  = 1.10 * inch   # space for header
MARGIN_B  = 0.85 * inch   # space for footer
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

HEADER_H  = 0.55 * inch
FOOTER_H  = 0.40 * inch

# ── GUIDE META ────────────────────────────────────────────────────────────────
GUIDE_TITLE    = "Overtime Management"
GUIDE_SUBTITLE = "Strategy, Distribution & Cost Control"
GUIDE_NUM      = "Guide 5 of 10"

FIRM_NAME  = "Shiftwork Solutions LLC"
PHONE      = "(415) 265-1621"
EMAIL      = "Contact@shift-work.com"
WEBSITE    = "shift-work.com"
BOOKING    = "shift-work.com/contact"

OUTPUT_DIR  = "pdfs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "overtime-management-guide.pdf")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── HEADER / FOOTER CALLBACKS ─────────────────────────────────────────────────
def draw_header(canvas, doc):
    """Branded header on every page after page 1."""
    if doc.page == 1:
        return
    canvas.saveState()
    # Navy bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)
    # Firm name left
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(MARGIN_L, PAGE_H - HEADER_H + 0.18*inch, FIRM_NAME.upper())
    # Guide title right
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MID_BLUE)
    label = f"{GUIDE_TITLE}: {GUIDE_SUBTITLE}"
    canvas.drawRightString(PAGE_W - MARGIN_R, PAGE_H - HEADER_H + 0.18*inch, label)
    canvas.restoreState()


def draw_footer(canvas, doc):
    """Branded footer on every page after page 1."""
    if doc.page == 1:
        return
    canvas.saveState()
    # Light rule
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, FOOTER_H, PAGE_W - MARGIN_R, FOOTER_H)
    # Contact info left
    canvas.setFillColor(MUTED)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(MARGIN_L, FOOTER_H - 0.18*inch,
                      f"{PHONE}  |  {EMAIL}  |  {WEBSITE}")
    # Page number right
    canvas.setFont('Helvetica', 7.5)
    canvas.drawRightString(PAGE_W - MARGIN_R, FOOTER_H - 0.18*inch,
                           f"Page {doc.page}")
    # Orange accent bar bottom
    canvas.setFillColor(ORANGE)
    canvas.rect(0, 0, PAGE_W, 3, fill=1, stroke=0)
    canvas.restoreState()


# ── COVER PAGE ────────────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    """Full custom cover — page 1 only."""
    if doc.page != 1:
        return
    canvas.saveState()

    # Dark navy background top band (~3.2 in)
    band_h = 3.2 * inch
    canvas.setFillColor(NAVY_DARK)
    canvas.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)

    # Gold accent stripe at bottom of band
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - band_h, PAGE_W, 4, fill=1, stroke=0)

    # FIRM NAME in band
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 13)
    canvas.drawString(MARGIN_L, PAGE_H - 0.65*inch, FIRM_NAME.upper())

    # Guide number tag
    canvas.setFillColor(ORANGE)
    canvas.roundRect(MARGIN_L, PAGE_H - band_h + 0.55*inch,
                     1.05*inch, 0.22*inch, 3, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawCentredString(MARGIN_L + 0.525*inch,
                              PAGE_H - band_h + 0.60*inch, GUIDE_NUM.upper())

    # Guide title
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica-Bold', 26)
    canvas.drawString(MARGIN_L, PAGE_H - 1.40*inch, GUIDE_TITLE)

    # Guide subtitle
    canvas.setFillColor(MID_BLUE)
    canvas.setFont('Helvetica', 14)
    canvas.drawString(MARGIN_L, PAGE_H - 1.75*inch, GUIDE_SUBTITLE)

    # Tagline
    canvas.setFillColor(HexColor('#B5D4F4'))
    canvas.setFont('Helvetica', 9.5)
    canvas.drawString(MARGIN_L, PAGE_H - 2.10*inch,
        "Expert guidance from consultants who have worked with hundreds of 24/7 operations.")

    # ── WHO WE ARE section ────────────────────────────────────────────────────
    y = PAGE_H - band_h - 0.45*inch

    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(MARGIN_L, y, "WHO WE ARE")
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L + 0.72*inch, y + 0.04*inch,
                PAGE_W - MARGIN_R, y + 0.04*inch)

    y -= 0.22*inch
    canvas.setFillColor(BODY_TEXT)
    canvas.setFont('Helvetica', 8.5)
    who_text = (
        "Shiftwork Solutions LLC is a leading U.S.-based management consulting firm "
        "specializing in shift schedule design, workforce engagement, and operational "
        "optimization for 24/7 industrial operations. For over 30 years we have helped "
        "hundreds of manufacturing plants, distribution centers, mines, utilities, and "
        "processing facilities across more than 16 industries build better schedules, "
        "reduce costs, and create workforces that stay."
    )
    # Wrap text manually
    _draw_wrapped_text(canvas, who_text, MARGIN_L, y, CONTENT_W, 8.5, line_h=0.145*inch)

    # ── OUR PROCESS ───────────────────────────────────────────────────────────
    y -= 0.85*inch

    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(MARGIN_L, y, "OUR PROCESS")
    canvas.setStrokeColor(NAVY)
    canvas.line(MARGIN_L + 0.78*inch, y + 0.04*inch,
                PAGE_W - MARGIN_R, y + 0.04*inch)

    y -= 0.22*inch
    col_w = CONTENT_W / 4
    steps = [
        ("1", "Assess",   "Cost-benefit modeling, workforce surveys, benchmarking, schedule impact analysis."),
        ("2", "Design",   "Schedule options built for operations AND people — with full cost and coverage clarity."),
        ("3", "Deliver",  "Rollout support, employee education, policy development, and ongoing guidance."),
        ("4", "Sustain",  "Post-implementation survey, results review, and adjustments to ensure it holds."),
    ]
    accent_colors = [NAVY, ORANGE, GREEN, MID_BLUE]
    for i, (num, title, desc) in enumerate(steps):
        x = MARGIN_L + i * col_w
        # Accent top bar
        canvas.setFillColor(accent_colors[i])
        canvas.rect(x, y + 0.02*inch, col_w - 0.10*inch, 3, fill=1, stroke=0)
        # Step number
        canvas.setFillColor(accent_colors[i])
        canvas.setFont('Helvetica-Bold', 18)
        canvas.drawString(x, y - 0.22*inch, num)
        # Step title
        canvas.setFillColor(NAVY_DARK)
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(x, y - 0.42*inch, title)
        # Step desc
        canvas.setFillColor(MUTED)
        canvas.setFont('Helvetica', 7.5)
        _draw_wrapped_text(canvas, desc, x, y - 0.58*inch,
                           col_w - 0.12*inch, 7.5, line_h=0.13*inch)

    # ── EXPERIENCE STATS ──────────────────────────────────────────────────────
    y -= 1.38*inch

    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(MARGIN_L, y, "OUR EXPERIENCE")
    canvas.setStrokeColor(NAVY)
    canvas.line(MARGIN_L + 1.0*inch, y + 0.04*inch,
                PAGE_W - MARGIN_R, y + 0.04*inch)

    y -= 0.22*inch
    stats = [
        ("30+",      "Years of dedicated\nshiftwork consulting"),
        ("Hundreds", "Operations helped\nacross North America"),
        ("16+",      "Industries served\nin every engagement"),
        ("Fixed",    "Fee model — no hourly\nbilling surprises"),
    ]
    s_col_w = CONTENT_W / 4
    for i, (num, label) in enumerate(stats):
        x = MARGIN_L + i * s_col_w
        canvas.setFillColor(NAVY)
        canvas.setFont('Helvetica-Bold', 17)
        canvas.drawString(x, y - 0.18*inch, num)
        canvas.setFillColor(MUTED)
        canvas.setFont('Helvetica', 7.5)
        for j, line in enumerate(label.split('\n')):
            canvas.drawString(x, y - 0.38*inch - j*0.13*inch, line)

    # ── CONTACT / CTA ─────────────────────────────────────────────────────────
    y -= 0.90*inch

    # Orange CTA box
    box_h = 0.72*inch
    canvas.setFillColor(ORANGE)
    canvas.roundRect(MARGIN_L, y - box_h, CONTENT_W, box_h, 5, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 11)
    canvas.drawString(MARGIN_L + 0.22*inch, y - 0.28*inch,
                      "Ready to discuss your operation?  The first conversation is free.")
    canvas.setFont('Helvetica', 9)
    canvas.drawString(MARGIN_L + 0.22*inch, y - 0.50*inch,
                      f"Call {PHONE}  |  Email {EMAIL}  |  Book online: {BOOKING}")

    # Bottom strip
    canvas.setFillColor(NAVY_DARK)
    canvas.rect(0, 0, PAGE_W, 0.25*inch, fill=1, stroke=0)
    canvas.setFillColor(HexColor('#AAAAAA'))
    canvas.setFont('Helvetica', 7)
    canvas.drawCentredString(PAGE_W/2, 0.08*inch,
        f"{FIRM_NAME}  |  {WEBSITE}  |  {PHONE}  |  © 2026")

    canvas.restoreState()


def _draw_wrapped_text(canvas, text, x, y, max_width, font_size, line_h=0.14*inch):
    """Simple word-wrap helper for canvas text blocks."""
    words = text.split()
    line = ''
    current_y = y
    canvas.setFont('Helvetica', font_size)
    for word in words:
        test = (line + ' ' + word).strip()
        if canvas.stringWidth(test, 'Helvetica', font_size) <= max_width:
            line = test
        else:
            if line:
                canvas.drawString(x, current_y, line)
                current_y -= line_h
            line = word
    if line:
        canvas.drawString(x, current_y, line)


# ── PARAGRAPH STYLES ─────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    styles = {
        'h2': S('h2',
            fontName='Helvetica-Bold', fontSize=14,
            textColor=NAVY_DARK, leading=18,
            spaceBefore=18, spaceAfter=6),

        'eyebrow': S('eyebrow',
            fontName='Helvetica-Bold', fontSize=7,
            textColor=NAVY, leading=10,
            spaceBefore=14, spaceAfter=3,
            letterSpacing=1.2),

        'body': S('body',
            fontName='Helvetica', fontSize=9.5,
            textColor=BODY_TEXT, leading=15,
            spaceBefore=0, spaceAfter=8,
            alignment=TA_JUSTIFY),

        'pull_quote': S('pull_quote',
            fontName='Helvetica-Oblique', fontSize=11,
            textColor=NAVY, leading=16,
            spaceBefore=8, spaceAfter=4,
            leftIndent=20, rightIndent=20),

        'pull_attr': S('pull_attr',
            fontName='Helvetica', fontSize=8,
            textColor=MUTED, leading=12,
            spaceBefore=2, spaceAfter=10,
            leftIndent=20),

        'callout_label': S('callout_label',
            fontName='Helvetica-Bold', fontSize=7,
            textColor=ORANGE, leading=10,
            spaceBefore=0, spaceAfter=3),

        'callout_body': S('callout_body',
            fontName='Helvetica', fontSize=8.5,
            textColor=BODY_TEXT, leading=13,
            spaceBefore=0, spaceAfter=0),

        'stat_num': S('stat_num',
            fontName='Helvetica-Bold', fontSize=22,
            textColor=NAVY, leading=26,
            spaceBefore=4, spaceAfter=2),

        'stat_label': S('stat_label',
            fontName='Helvetica-Bold', fontSize=8,
            textColor=BODY_TEXT, leading=11,
            spaceBefore=0, spaceAfter=2),

        'stat_text': S('stat_text',
            fontName='Helvetica', fontSize=7.5,
            textColor=MUTED, leading=11,
            spaceBefore=0, spaceAfter=0),
    }
    return styles


# ── CONTENT BUILDERS ─────────────────────────────────────────────────────────
def build_insight_cards(styles):
    """3-column stat cards as a Table."""
    data = [
        [
            [Paragraph('~14%', styles['stat_num']),
             Paragraph('True OT cost premium', styles['stat_label']),
             Paragraph('When fully loaded — OT costs only ~14% more than straight time, not 50%.', styles['stat_text'])],

            [Paragraph('<font color="#E8610A">10×</font>', styles['stat_num']),
             Paragraph('Overstaffing penalty', styles['stat_label']),
             Paragraph('Excess headcount costs ~10× more than moderate understaffing covered by OT.', styles['stat_text'])],

            [Paragraph('<font color="#1D9E75">7.5%</font>', styles['stat_num']),
             Paragraph('Pay increase, 1% cost rise', styles['stat_label']),
             Paragraph('One facility raised compensation 7.5% while payroll costs rose only 1% — via built-in OT.', styles['stat_text'])],
        ]
    ]
    col_w = CONTENT_W / 3
    t = Table(data, colWidths=[col_w]*3)
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), white),
        ('BOX',          (0,0), (0,0),   0.5, BORDER),
        ('BOX',          (1,0), (1,0),   0.5, BORDER),
        ('BOX',          (2,0), (2,0),   0.5, BORDER),
        ('LINEABOVE',    (0,0), (0,0),   3,   NAVY),
        ('LINEABOVE',    (1,0), (1,0),   3,   ORANGE),
        ('LINEABOVE',    (2,0), (2,0),   3,   GREEN),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 12),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t


def build_20_60_20_viz(styles):
    """Visual bar representing 20/60/20 distribution."""
    bar_data = [[
        Paragraph('<font color="white"><b>20%</b><br/>Want max OT</font>',
                  ParagraphStyle('bv', fontName='Helvetica-Bold', fontSize=8,
                                 textColor=white, leading=11, alignment=TA_CENTER)),
        Paragraph('<font color="white"><b>60%</b><br/>Work fair share</font>',
                  ParagraphStyle('bv2', fontName='Helvetica-Bold', fontSize=8,
                                 textColor=white, leading=11, alignment=TA_CENTER)),
        Paragraph('<font color="#1F4E79"><b>20%</b><br/>Want none</font>',
                  ParagraphStyle('bv3', fontName='Helvetica-Bold', fontSize=8,
                                 textColor=NAVY, leading=11, alignment=TA_CENTER)),
    ]]
    bar = Table(bar_data,
                colWidths=[CONTENT_W*0.20, CONTENT_W*0.60, CONTENT_W*0.20],
                rowHeights=[0.55*inch])
    bar.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (0,0), NAVY),
        ('BACKGROUND',   (1,0), (1,0), HexColor('#5A9BD5')),
        ('BACKGROUND',   (2,0), (2,0), HexColor('#9DC3E6')),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0), (-1,-1), 8),
        ('LEFTPADDING',  (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return bar


def build_callout(styles, label, text):
    inner = [
        [Paragraph(label.upper(), styles['callout_label']),
         Paragraph(text, styles['callout_body'])]
    ]
    t = Table(inner, colWidths=[0.55*inch, CONTENT_W - 0.55*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), LIGHT_GREY),
        ('BOX',          (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('LINEABOVE',    (0,0), (-1,0),  2, ORANGE),
    ]))
    return t


def hr(width=CONTENT_W):
    return HRFlowable(width=width, thickness=0.5, color=BORDER,
                      spaceAfter=10, spaceBefore=10)


# ── STORY BUILDER ─────────────────────────────────────────────────────────────
def build_story(styles):
    story = []

    # ── PAGE 1 placeholder (cover drawn by canvas callback) ──
    story.append(PageBreak())

    # ── SECTION: Introduction ─────────────────────────────────────────────────
    story.append(Paragraph('INTRODUCTION', styles['eyebrow']))
    story.append(Paragraph('Overtime Is a Tool, Not a Problem', styles['h2']))
    story.append(Paragraph(
        "Ask a production manager about overtime and you'll hear about flexibility, "
        "responsiveness, and getting the job done. Ask an HR manager and you'll hear "
        "about turnover, fatigue, and declining morale. Both perspectives contain truth "
        "— and that tension reveals why overtime management deserves strategic attention "
        "rather than reactive acceptance.", styles['body']))
    story.append(Paragraph(
        "Overtime represents one of the most misunderstood elements of workforce "
        "operations. When used strategically, it provides flexibility that no staffing "
        "model can match. When mismanaged, it drives your best workers to competitors, "
        "creates safety risks, and costs far more than the financial statements reveal.",
        styles['body']))
    story.append(Paragraph(
        "The difference between these outcomes rarely lies in how much overtime an "
        "operation uses — it lies in how that overtime is managed: who works it, how "
        "it's distributed, and whether employees experience it as opportunity or burden. "
        "Operations with higher total overtime often have happier workforces than those "
        "with less, simply because they've mastered the strategy behind the hours.",
        styles['body']))

    story.append(hr())

    # ── 20/60/20 visualization ────────────────────────────────────────────────
    story.append(Paragraph('THE 20/60/20 RULE', styles['eyebrow']))
    story.append(Paragraph('Workforce Overtime Preference Distribution', styles['h2']))
    story.append(Spacer(1, 6))
    story.append(build_20_60_20_viz(styles))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Distribution is consistent across industries and demographics. Channeling "
        "overtime to the 20% who want it produces higher satisfaction than distributing "
        "it equally. Source: Shiftwork Solutions analysis across hundreds of client facilities.",
        ParagraphStyle('caption', fontName='Helvetica', fontSize=7.5,
                       textColor=MUTED, leading=11, spaceBefore=4, spaceAfter=8)))

    story.append(Spacer(1, 10))
    story.append(build_insight_cards(styles))
    story.append(Spacer(1, 16))
    story.append(hr())

    # ── SECTION: Real Cost ────────────────────────────────────────────────────
    story.append(Paragraph('THE REAL COST', styles['eyebrow']))
    story.append(Paragraph('Why Overtime Costs Less Than You Think', styles['h2']))
    story.append(Paragraph(
        "Most managers dramatically overestimate the cost difference between overtime "
        "and straight time. The phrase 'time and a half' creates an intuitive sense "
        "that overtime costs 50% more — the actual difference is far smaller.",
        styles['body']))
    story.append(Paragraph(
        "An employee earning $15/hr with 32% benefit loading costs ~$19.80 fully "
        "loaded. That same employee on overtime costs $22.50 — time-and-a-half on "
        "wages only, no additional benefits. True incremental cost: ~$2.70/hr, or "
        "roughly 14% more than straight time. Not 50%.",
        styles['body']))
    story.append(Paragraph(
        "This calculation changes how operations should think about staffing. Overtime "
        "provides flexibility straight time cannot — you can add it when needed and "
        "remove it when not. The expensive scenario isn't using overtime; it's "
        "maintaining headcount you don't need. The adverse cost of overstaffing "
        "typically runs ten times higher than moderate understaffing covered by overtime.",
        styles['body']))

    story.append(hr())

    # ── SECTION: Distribution Paradox ────────────────────────────────────────
    story.append(Paragraph('THE DISTRIBUTION PARADOX', styles['eyebrow']))
    story.append(Paragraph('Why More Overtime Can Mean Happier Employees', styles['h2']))
    story.append(Paragraph(
        "Every workforce contains three distinct groups. Approximately 20% actively "
        "want all the overtime they can get. A different 20% want none — they have "
        "life circumstances that make extra hours genuinely problematic. The remaining "
        "60% will work what they consider a fair share without complaint.",
        styles['body']))
    story.append(Paragraph(
        "Most operations ignore this distribution entirely. They spread overtime "
        "equally — treating it as a burden to be shared — or rely on seniority systems "
        "that give desirable overtime to senior employees while forcing undesirable "
        "overtime onto newer workers. Both approaches generate dissatisfaction that "
        "has nothing to do with overtime quantity.",
        styles['body']))

    # Pull quote
    story.append(KeepTogether([
        Paragraph(
            "\u201cThe key to managing overtime isn't eliminating it — it's understanding "
            "who values it most and building your strategy around them.\u201d",
            styles['pull_quote']),
        Paragraph('— Dan Capshaw, Shiftwork Solutions', styles['pull_attr']),
    ]))

    story.append(hr())

    # ── SECTION: Predictability ───────────────────────────────────────────────
    story.append(Paragraph('PREDICTABILITY', styles['eyebrow']))
    story.append(Paragraph('Why Advance Notice Changes Everything', styles['h2']))
    story.append(Paragraph(
        "One principle commands near-universal agreement: predictable overtime is "
        "dramatically more acceptable than surprise overtime. Announcing weekend work "
        "on Friday afternoon creates resentment that announcing the same work on "
        "Tuesday doesn't. Employees can adjust plans, arrange childcare, and mentally "
        "prepare when they know what's coming.",
        styles['body']))
    story.append(Paragraph(
        "Extending the notification window requires no additional spending — just "
        "better planning and communication discipline. Moving from Friday announcements "
        "to Thursday creates measurable improvement. Quarterly forecasts of expected "
        "overtime patterns, even when imprecise, help employees plan their lives.",
        styles['body']))

    story.append(KeepTogether([
        Paragraph(
            "\u201cIt's not the overtime that kills morale — it's the surprise overtime "
            "announced at the last minute. Give people advance notice, and even "
            "unwanted overtime becomes manageable.\u201d",
            styles['pull_quote']),
        Paragraph('— Jim Dillingham, Shiftwork Solutions', styles['pull_attr']),
    ]))

    story.append(hr())

    # ── SECTION: Deeper Problems ──────────────────────────────────────────────
    story.append(Paragraph('DIAGNOSIS', styles['eyebrow']))
    story.append(Paragraph('When Overtime Signals Deeper Problems', styles['h2']))
    story.append(Paragraph(
        "Chronic overtime often masks underlying issues that scheduling alone cannot "
        "solve. The most common driver is understaffing — when workforce levels fall "
        "below coverage requirements, overtime fills the gap by default. This typically "
        "arises in growing operations that haven't kept pace with demand, or facilities "
        "experiencing turnover that outpaces hiring. The overtime becomes self-reinforcing: "
        "high hours drive turnover → more vacancies → more overtime for remaining workers.",
        styles['body']))

    story.append(build_callout(styles, 'Important',
        "Prolonged high overtime creates dangerous dependency. When employees rely on "
        "overtime income to meet financial obligations, reducing overtime becomes "
        "financially devastating for your workforce. Design your baseline compensation "
        "and staffing to avoid creating this trap."))

    story.append(Spacer(1, 10))
    story.append(hr())

    # ── SECTION: Schedule Integration ────────────────────────────────────────
    story.append(Paragraph('SCHEDULE INTEGRATION', styles['eyebrow']))
    story.append(Paragraph('Building Overtime Into the Schedule', styles['h2']))
    story.append(Paragraph(
        "Some operations need sustained high coverage that traditional schedules "
        "can't provide without chronic overtime. Rather than fighting this reality, "
        "sophisticated operations build predictable overtime directly into the pattern.",
        styles['body']))
    story.append(Paragraph(
        "A four-on, two-off twelve-hour schedule illustrates this. Three crews rotate "
        "through a six-week cycle, working four consecutive twelve-hour shifts followed "
        "by two days off — delivering 56 scheduled hours weekly. 16 hours of overtime "
        "built into every week. Employees know exactly what to expect.",
        styles['body']))
    story.append(Paragraph(
        "One manufacturing facility using this approach increased guaranteed employee "
        "compensation by 7.5% while payroll costs rose only 1%. Days off increased "
        "from 104 to 182 annually. Unscheduled overtime dropped to minimal levels.",
        styles['body']))

    story.append(hr())

    # ── SECTION: Conclusion ───────────────────────────────────────────────────
    story.append(Paragraph('CONCLUSION', styles['eyebrow']))
    story.append(Paragraph('Manage It Deliberately or Let It Manage You', styles['h2']))
    story.append(Paragraph(
        "Overtime isn't inherently problematic. Poorly managed overtime is. The "
        "operations that manage it most effectively understand the real cost comparison, "
        "recognize that distribution matters more than total volume, build systems that "
        "maximize predictability, and diagnose whether overtime signals underlying "
        "problems or represents appropriate capacity flexibility.",
        styles['body']))
    story.append(Paragraph(
        "Treat overtime as a strategic element of workforce management — not an "
        "accounting variance to minimize. The question isn't whether to use overtime. "
        "It's whether to manage it deliberately or let it manage you.",
        styles['body']))

    story.append(Spacer(1, 20))

    # ── CLOSING CTA BOX ───────────────────────────────────────────────────────
    cta_data = [[
        Paragraph(
            f"<font color='white'><b>Ready to improve how overtime works in your operation?</b><br/>"
            f"Call {PHONE}  |  {EMAIL}  |  Book a free consultation: {BOOKING}</font>",
            ParagraphStyle('cta', fontName='Helvetica', fontSize=9,
                           textColor=white, leading=14, alignment=TA_CENTER))
    ]]
    cta_t = Table(cta_data, colWidths=[CONTENT_W])
    cta_t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), ORANGE),
        ('ROUNDEDCORNERS', [5]),
        ('TOPPADDING',   (0,0), (-1,-1), 14),
        ('BOTTOMPADDING',(0,0), (-1,-1), 14),
        ('LEFTPADDING',  (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(cta_t)

    return story


# ── DOCUMENT BUILD ────────────────────────────────────────────────────────────
def build_pdf():
    doc = BaseDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title=f"{GUIDE_TITLE}: {GUIDE_SUBTITLE}",
        author=FIRM_NAME,
        subject="Shiftwork Operations Guide",
        creator=FIRM_NAME,
    )

    # Cover page frame (full bleed — no margins since canvas draws everything)
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')

    # Content frame (normal margins)
    content_frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W,
                          PAGE_H - MARGIN_T - MARGIN_B, id='content')

    def cover_page(canvas, doc):
        draw_cover(canvas, doc)

    def content_page(canvas, doc):
        draw_header(canvas, doc)
        draw_footer(canvas, doc)

    doc.addPageTemplates([
        PageTemplate(id='Cover',   frames=[cover_frame],  onPage=cover_page),
        PageTemplate(id='Content', frames=[content_frame], onPage=content_page),
    ])

    styles = build_styles()

    # First element switches to Content template after cover
    from reportlab.platypus import NextPageTemplate
    story = [NextPageTemplate('Content')] + build_story(styles)

    doc.build(story)
    print(f"PDF generated: {OUTPUT_FILE}")


if __name__ == '__main__':
    build_pdf()
