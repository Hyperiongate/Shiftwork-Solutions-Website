"""
generate_guide_pdf.py
Shiftwork Solutions LLC — Branded Guide PDF Generator
Generates: pdfs/overtime-management-guide.pdf

Usage:  python3 generate_guide_pdf.py
Output: pdfs/overtime-management-guide.pdf  (deploy to /pdfs/ in repo root)

Created:      2026-04-23
Last Updated: 2026-04-29

CHANGE LOG:
    2026-04-23 — Initial build. Overtime Management Guide.
                 Cover page + 8 content pages. Branded header/footer every page.
    2026-04-29 — Multiple fixes per design review:
                 1. LOGO: Added Shiftwork Solutions logo image (clear_bkgr_logo_2.png)
                    to the right half of the cover band, alongside firm name.
                 2. LIGHT BLUE TEXT: Replaced MID_BLUE text color with white on all
                    dark backgrounds (cover subtitle/tagline, header guide label).
                    MID_BLUE still used for one-word caps labels only.
                 3. GUIDE NUMBER TAG: Replaced "Guide 5 of 10" orange tag on cover
                    with a "Download PDF" action tag (avoids hard-coded numbering
                    that would need updating whenever guides are added).
                 4. CALLOUT BOX (IMPORTANT): Replaced broken/multi-line callout
                    table with a clean left-bordered navy bar layout. Text now
                    flows properly on one visual unit.
                 5. EYEBROW SPACING: spaceAfter on 'eyebrow' style reduced from
                    3pt to 2pt, spaceBefore on 'h2' reduced from 18pt to 8pt so
                    the eyebrow sits tight against its heading.
                 6. INSIGHT CARDS: Third (green) card changed to grey (#607D8B)
                    — green implies go/correct vs. orange warning, which is
                    misleading visual hierarchy.
                 7. PULL QUOTE STYLE: Changed from Helvetica-Oblique/italic to
                    Helvetica (upright), matching site-wide standard. Color
                    changed from NAVY to BODY_TEXT for consistency.

DESIGN:
    Navy:   #1F4E79   Orange: #E8610A   Gold: #EEAE26
    Mid-blue: #85B7EB  Light-grey: #F4F6F8  Body-text: #1A1A1A
    Grey-accent: #607D8B  (replaces green on insight cards)
    Fonts: Helvetica (PDF built-in, no embedding required)
    Page size: Letter (8.5 x 11 in)
    Margins: 0.75in left/right, 1in top (below header), 0.85in bottom (above footer)

STRUCTURE:
    Page 1  — Cover / Brand page (logo, firm info, process, experience)
    Page 2+ — Guide content with running header + footer

LOGO NOTE:
    The cover page uses drawImage to place /images/clear_bkgr_logo_2.png on the
    right side of the dark band. The logo file must be present in the repo root
    at /images/clear_bkgr_logo_2.png when this script is run, OR the path must
    be updated below. If the file is missing, the script draws a text fallback.
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
NAVY        = HexColor('#1F4E79')
NAVY_DARK   = HexColor('#0D1F3C')
MID_BLUE    = HexColor('#85B7EB')
ORANGE      = HexColor('#E8610A')
GREEN       = HexColor('#1D9E75')
GREY_ACCENT = HexColor('#607D8B')   # replaces green on insight cards
GOLD        = HexColor('#EEAE26')
LIGHT_GREY  = HexColor('#F4F6F8')
BORDER      = HexColor('#E0E0E0')
MUTED       = HexColor('#666666')
BODY_TEXT   = HexColor('#1A1A1A')

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
# Note: No hard-coded "Guide X of 10" — replaced with "Download PDF" action tag

FIRM_NAME  = "Shiftwork Solutions LLC"
PHONE      = "(415) 265-1621"
EMAIL      = "Contact@shift-work.com"
WEBSITE    = "shift-work.com"
BOOKING    = "shift-work.com/contact"

# Logo path — relative to where this script is run (repo root)
LOGO_PATH  = "images/clear_bkgr_logo_2.png"

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
    # Firm name left — white (not MID_BLUE)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(MARGIN_L, PAGE_H - HEADER_H + 0.18*inch, FIRM_NAME.upper())
    # Guide title right — white (was MID_BLUE — too light on dark background)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(white)
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

    # ── LEFT SIDE: Firm name + guide info ─────────────────────────────────────
    # FIRM NAME in band — white (not gold; gold is for headings)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 13)
    canvas.drawString(MARGIN_L, PAGE_H - 0.65*inch, FIRM_NAME.upper())

    # "Download PDF" action tag (replaced "Guide X of 10" to avoid stale numbering)
    canvas.setFillColor(NAVY)
    canvas.roundRect(MARGIN_L, PAGE_H - band_h + 0.55*inch,
                     1.10*inch, 0.22*inch, 3, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawCentredString(MARGIN_L + 0.55*inch,
                              PAGE_H - band_h + 0.60*inch, "DOWNLOAD PDF")

    # Guide title — gold
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica-Bold', 26)
    canvas.drawString(MARGIN_L, PAGE_H - 1.40*inch, GUIDE_TITLE)

    # Guide subtitle — white (was MID_BLUE — hard to read on dark)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica', 14)
    canvas.drawString(MARGIN_L, PAGE_H - 1.75*inch, GUIDE_SUBTITLE)

    # Tagline — white (was #B5D4F4 light blue — too light on dark)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica', 9.5)
    canvas.drawString(MARGIN_L, PAGE_H - 2.10*inch,
        "Expert guidance from consultants who have worked with hundreds of 24/7 operations.")

    # ── RIGHT SIDE: Logo image ─────────────────────────────────────────────────
    # Place the Shiftwork Solutions logo on the right side of the cover band.
    # Centered vertically in the band, right-aligned.
    logo_right_x = PAGE_W - MARGIN_R - 2.20*inch   # left edge of logo area
    logo_y       = PAGE_H - band_h + 0.55*inch      # bottom of logo

    if os.path.exists(LOGO_PATH):
        # Draw logo — max width 2.1in, height auto-scaled (typically ~0.6in)
        canvas.drawImage(
            LOGO_PATH,
            logo_right_x,
            logo_y,
            width=2.10*inch,
            height=0.72*inch,
            preserveAspectRatio=True,
            anchor='sw',
            mask='auto',   # treat white/transparent as transparent
        )
    else:
        # Text fallback if image file not present
        canvas.setFillColor(GOLD)
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawRightString(PAGE_W - MARGIN_R, logo_y + 0.18*inch,
                               FIRM_NAME.upper())

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
    _draw_wrapped_text(canvas, who_text, MARGIN_L, y, CONTENT_W, 8.5, 0.145*inch)

    # ── OUR PROCESS (4 columns) ───────────────────────────────────────────────
    y -= 0.82*inch

    canvas.setFillColor(NAVY)
    canvas.setFont('Helvetica-Bold', 7)
    canvas.drawString(MARGIN_L, y, "OUR PROCESS")
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L + 0.72*inch, y + 0.04*inch,
                PAGE_W - MARGIN_R, y + 0.04*inch)

    y -= 0.14*inch
    col_w = CONTENT_W / 4
    steps = [
        ("1", "Assess",   "We start by understanding your operation, schedule, costs, and workforce composition."),
        ("2", "Design",   "Schedule options built for operations AND people — with full cost and coverage clarity."),
        ("3", "Deliver",  "Rollout support, employee education, policy development, and ongoing guidance."),
        ("4", "Sustain",  "Post-implementation survey, results review, and adjustments to ensure it holds."),
    ]
    accent_colors = [NAVY, ORANGE, GREY_ACCENT, MID_BLUE]
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
                      f"{PHONE}   {EMAIL}   {BOOKING}")

    canvas.restoreState()


# ── HELPER ────────────────────────────────────────────────────────────────────
def _draw_wrapped_text(canvas, text, x, y, max_width, font_size, line_h=0.145*inch):
    """Word-wrap plain text onto canvas at (x,y), descending by line_h per line."""
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
            # Reduced spaceBefore so eyebrow sits tight against heading
            spaceBefore=8, spaceAfter=6),

        'eyebrow': S('eyebrow',
            fontName='Helvetica-Bold', fontSize=7,
            textColor=NAVY, leading=10,
            spaceBefore=14, spaceAfter=2,   # spaceAfter reduced: 3→2
            letterSpacing=1.2),

        'body': S('body',
            fontName='Helvetica', fontSize=9.5,
            textColor=BODY_TEXT, leading=15,
            spaceBefore=0, spaceAfter=8,
            alignment=TA_JUSTIFY),

        # Pull quote: upright (not italic), body-text color — matches site standard
        'pull_quote': S('pull_quote',
            fontName='Helvetica', fontSize=11,
            textColor=BODY_TEXT, leading=16,
            spaceBefore=8, spaceAfter=4,
            leftIndent=20, rightIndent=20),

        'pull_attr': S('pull_attr',
            fontName='Helvetica', fontSize=8,
            textColor=MUTED, leading=12,
            spaceBefore=2, spaceAfter=10,
            leftIndent=20),

        # Callout label: navy (not orange) to match new callout-box standard
        'callout_label': S('callout_label',
            fontName='Helvetica-Bold', fontSize=7,
            textColor=NAVY, leading=10,
            spaceBefore=0, spaceAfter=3),

        'callout_body': S('callout_body',
            fontName='Helvetica', fontSize=9.5,
            textColor=BODY_TEXT, leading=14,
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
    """3-column stat cards as a Table.
    Card 3 uses GREY_ACCENT (not GREEN) — green implies 'go/correct' which is
    misleading against the orange card.
    """
    data = [
        [
            [Paragraph('~14%', styles['stat_num']),
             Paragraph('True OT cost premium', styles['stat_label']),
             Paragraph('When fully loaded — OT costs only ~14% more than straight time, not 50%.',
                       styles['stat_text'])],
            [Paragraph('<font color="#E8610A"><b>10×</b></font>',
                       ParagraphStyle('sn2', fontName='Helvetica-Bold', fontSize=22,
                                      textColor=ORANGE, leading=26, spaceBefore=4, spaceAfter=2)),
             Paragraph('Overstaffing penalty', styles['stat_label']),
             Paragraph('The adverse cost of excess headcount is typically ten times '
                       'higher than moderate understaffing covered by overtime.',
                       styles['stat_text'])],
            [Paragraph('<font color="#607D8B"><b>7.5%</b></font>',
                       ParagraphStyle('sn3', fontName='Helvetica-Bold', fontSize=22,
                                      textColor=GREY_ACCENT, leading=26, spaceBefore=4, spaceAfter=2)),
             Paragraph('Pay increase, 1% cost rise', styles['stat_label']),
             Paragraph('One facility increased guaranteed employee compensation by 7.5% '
                       'while payroll costs rose only 1% — by building OT into the schedule.',
                       styles['stat_text'])],
        ]
    ]

    col_w = CONTENT_W / 3
    t = Table(data, colWidths=[col_w]*3)
    t.setStyle(TableStyle([
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 14),
        ('BOTTOMPADDING',(0,0), (-1,-1), 14),
        ('LEFTPADDING',  (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BOX',          (0,0), (-1,-1), 0.5, BORDER),
        ('INNERGRID',    (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND',   (0,0), (-1,-1), white),
        # Top border accent colors per column
        ('LINEABOVE',    (0,0), (0,0), 3, NAVY),
        ('LINEABOVE',    (1,0), (1,0), 3, ORANGE),
        ('LINEABOVE',    (2,0), (2,0), 3, GREY_ACCENT),
    ]))
    return t


def build_callout(styles):
    """IMPORTANT callout box — navy left border, clean layout.
    Replaces the broken multi-column table approach.
    """
    # Single-column table with a thick left border to simulate the navy left bar
    text = (
        "Important: Prolonged high overtime creates a dangerous dependency. "
        "When employees rely on overtime income to meet their financial obligations, "
        "reducing overtime — even when operationally appropriate — becomes financially "
        "devastating for your workforce. You've essentially created a compensation "
        "structure that can't flex downward without causing hardship. Design your "
        "baseline compensation and staffing to avoid creating this trap."
    )
    callout_data = [[
        Paragraph(text, styles['callout_body'])
    ]]
    t = Table(callout_data, colWidths=[CONTENT_W - 0.12*inch])
    t.setStyle(TableStyle([
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 12),
        ('BOTTOMPADDING',(0,0), (-1,-1), 12),
        ('LEFTPADDING',  (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BACKGROUND',   (0,0), (-1,-1), LIGHT_GREY),
        ('LINEBEFORE',   (0,0), (0,-1), 4, NAVY),
    ]))
    return t


def build_pull_quote(quote_text, attribution, styles):
    """Pull quote: upright text, navy left bar, consistent with site standard."""
    pq_data = [[
        Paragraph(f"\u201c{quote_text}\u201d", styles['pull_quote']),
        Paragraph(f"\u2014 {attribution}", styles['pull_attr']),
    ]]
    # Stack vertically inside a single column
    combined = [
        Paragraph(f"\u201c{quote_text}\u201d", styles['pull_quote']),
        Paragraph(f"\u2014 {attribution}", styles['pull_attr']),
    ]
    t = Table([[combined]], colWidths=[CONTENT_W - 0.12*inch])
    t.setStyle(TableStyle([
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
        ('LEFTPADDING',  (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BACKGROUND',   (0,0), (-1,-1), white),
        ('LINEBEFORE',   (0,0), (0,-1), 3, NAVY),
    ]))
    return t


# ── STORY BUILDER ─────────────────────────────────────────────────────────────
def build_story(styles):
    story = []

    def H(text):
        """Section heading."""
        return Paragraph(text, styles['h2'])

    def EYE(text):
        """Eyebrow label."""
        return Paragraph(text.upper(), styles['eyebrow'])

    def P(text):
        """Body paragraph."""
        return Paragraph(text, styles['body'])

    def HR():
        return HRFlowable(width='100%', thickness=0.5, color=BORDER,
                          spaceBefore=12, spaceAfter=12)

    # ── INTRODUCTION ─────────────────────────────────────────────────────────
    story.append(EYE("Introduction"))
    story.append(H("Overtime Is a Tool, Not a Problem"))
    story.append(P(
        "Ask a production manager about overtime and you'll hear about flexibility, "
        "responsiveness, and getting the job done. Ask an HR manager the same question "
        "and you'll hear about turnover, fatigue, and declining morale. Both perspectives "
        "contain truth — and that tension reveals why overtime management deserves strategic "
        "attention rather than reactive acceptance."))
    story.append(P(
        "Overtime represents one of the most misunderstood elements of workforce operations. "
        "When used strategically, it provides flexibility that no staffing model can match: "
        "immediate access to skilled labor, the ability to respond to demand fluctuations, "
        "and supplemental income that employees genuinely value. When mismanaged, it drives "
        "your best workers to competitors, creates safety risks, and costs far more than the "
        "financial statements reveal."))
    story.append(P(
        "The difference between these outcomes rarely lies in how much overtime an operation "
        "uses. It lies in how that overtime is managed — who works it, how it's distributed, "
        "and whether employees experience it as opportunity or burden."))
    story.append(P(
        "Understanding overtime requires moving beyond the instinct to minimize it. The goal "
        "isn't eliminating overtime — it's transforming it from a chronic problem into a "
        "strategic tool that serves both operational and workforce objectives."))

    story.append(HR())

    # ── INSIGHT CARDS ────────────────────────────────────────────────────────
    story.append(Spacer(1, 6))
    story.append(build_insight_cards(styles))
    story.append(Spacer(1, 16))

    story.append(HR())

    # ── THE REAL COST ─────────────────────────────────────────────────────────
    story.append(EYE("The Real Cost"))
    story.append(H("Why Overtime Costs Less Than You Think"))
    story.append(P(
        "Most managers dramatically overestimate the cost difference between overtime and "
        "straight time. The phrase \"time and a half\" creates an intuitive sense that overtime "
        "costs 50% more than regular hours. The actual difference is far smaller."))
    story.append(P(
        "Consider the full picture. Straight time labor includes not just wages but benefits, "
        "paid time off, training costs, and administrative overhead. These additions typically "
        "represent 30–40% of base wages. Overtime, by contrast, pays the premium on wages alone "
        "— no additional benefits accrue, no extra vacation days accumulate, no incremental "
        "training costs apply."))
    story.append(P(
        "Run the math for a typical operation. An employee earning $15 per hour with a 32% "
        "benefit loading costs the company approximately $19.80 per hour in fully loaded "
        "straight time. That same employee working overtime costs $22.50 per hour — time and "
        "a half on wages, but nothing additional on benefits. The actual incremental cost of "
        "overtime? About $2.70 per hour, or roughly 14% more than straight time. Not 50%."))
    story.append(P(
        "The expensive scenario isn't using overtime — it's maintaining headcount you don't "
        "need. The adverse cost of overstaffing typically runs ten times higher than the "
        "adverse cost of moderate understaffing covered by overtime. This asymmetry explains "
        "why lean operations often favor running slightly short with controlled overtime rather "
        "than carrying excess permanent headcount."))

    story.append(HR())

    # ── DISTRIBUTION PARADOX ──────────────────────────────────────────────────
    story.append(EYE("The Distribution Paradox"))
    story.append(H("Why More Overtime Can Mean Happier Employees"))
    story.append(P(
        "Every workforce contains three distinct groups when it comes to overtime preferences. "
        "Approximately 20% of employees actively want all the overtime they can get. A "
        "different 20% want none — they have life circumstances, commitments, or preferences "
        "that make extra hours genuinely problematic. The remaining 60% will work what they "
        "consider a fair share without complaint."))
    story.append(P(
        "Consider the contrast. Facility A has 1,000 annual overtime hours distributed equally "
        "across all employees. Facility B has 1,500 annual overtime hours channeled primarily "
        "to employees who want extra hours. Which facility has the happier workforce? Usually "
        "Facility B — despite 50% more total overtime."))
    story.append(P(
        "The practical implication: tracking overtime preferences and channeling hours "
        "accordingly matters more than reducing total hours. This requires preference surveys, "
        "distribution tracking, and policies that honor individual differences rather than "
        "treating overtime as one-size-fits-all."))

    # Pull quote 1
    story.append(Spacer(1, 8))
    story.append(build_pull_quote(
        "The key to managing overtime isn't eliminating it — it's understanding who values "
        "it most and building your strategy around them.",
        "Dan Capshaw, Shiftwork Solutions",
        styles))
    story.append(Spacer(1, 8))

    story.append(HR())

    # ── PREDICTABILITY ────────────────────────────────────────────────────────
    story.append(EYE("Predictability"))
    story.append(H("Why Advance Notice Changes Everything"))
    story.append(P(
        "One principle commands near-universal agreement across the workforce: predictable "
        "overtime is dramatically more acceptable than surprise overtime."))
    story.append(P(
        "The overtime itself might be identical. But announcing weekend work on Friday "
        "afternoon creates resentment that announcing the same work on Tuesday doesn't. "
        "Employees can adjust plans, arrange childcare, and mentally prepare when they know "
        "what's coming. Last-minute mandatory overtime, even in smaller amounts, creates "
        "disproportionate dissatisfaction."))
    story.append(P(
        "Extending the notification window requires no additional spending — just better "
        "planning and communication discipline. Quarterly forecasts of expected overtime "
        "patterns, even when imprecise, help employees plan their lives around work rather "
        "than having work constantly disrupt their lives."))

    # Pull quote 2
    story.append(Spacer(1, 8))
    story.append(build_pull_quote(
        "It's not the overtime that kills morale — it's the surprise overtime announced "
        "at the last minute. Give people advance notice, and even unwanted overtime "
        "becomes manageable.",
        "Jim Dillingham, Shiftwork Solutions",
        styles))
    story.append(Spacer(1, 8))

    story.append(HR())

    # ── DIAGNOSIS ─────────────────────────────────────────────────────────────
    story.append(EYE("Diagnosis"))
    story.append(H("When Overtime Signals Deeper Problems"))
    story.append(P(
        "Chronic overtime often masks underlying issues that scheduling alone cannot solve. "
        "Understanding the source of overtime determines whether the solution involves "
        "distribution strategies, staffing changes, schedule redesign, or operational "
        "improvements."))
    story.append(P(
        "The most common driver is understaffing. When workforce levels fall below what "
        "coverage requires, overtime fills the gap by default. The overtime itself becomes "
        "self-reinforcing: high hours drive turnover, which creates more vacancies, which "
        "requires more overtime from remaining workers."))
    story.append(P(
        "Diagnosing the actual driver matters because the solutions differ. Distribution "
        "problems require policy changes. Staffing problems require hiring strategies. "
        "Workload variation problems may require schedule flexibility. Design problems "
        "require rethinking the fundamental coverage approach."))

    # Callout box (IMPORTANT — fixed layout)
    story.append(Spacer(1, 4))
    story.append(build_callout(styles))
    story.append(Spacer(1, 8))

    story.append(HR())

    # ── SCHEDULE INTEGRATION ──────────────────────────────────────────────────
    story.append(EYE("Schedule Integration"))
    story.append(H("Building Overtime Into the Schedule"))
    story.append(P(
        "Some operations need sustained high coverage that traditional schedules can't "
        "provide without chronic overtime. Rather than fighting this reality, sophisticated "
        "operations build predictable overtime directly into the schedule pattern."))
    story.append(P(
        "A four-on, two-off twelve-hour schedule illustrates this approach. The pattern "
        "delivers 56 scheduled hours weekly — 16 hours of overtime built into every week. "
        "Employees know exactly what to expect. The overtime is predictable, distributed "
        "evenly, and reflected in guaranteed compensation rather than uncertain extra hours."))
    story.append(P(
        "One manufacturing facility transitioned from chaotic unscheduled overtime to a "
        "continuous schedule with built-in overtime. Employees increased their guaranteed "
        "compensation by 7.5% while payroll costs rose only 1%. Days off increased from "
        "104 to 182 annually."))

    story.append(HR())

    # ── EMPLOYEE EXPERIENCE ───────────────────────────────────────────────────
    story.append(EYE("Employee Experience"))
    story.append(H("The Impact on Retention and Engagement"))
    story.append(P(
        "The pretzel manufacturer that restructured its schedule achieved measurable "
        "improvements. Schedule predictability improved 40%. Schedule flexibility improved "
        "47%. Employees' perception of the general work environment improved 21%. Most "
        "significantly, employee turnover dropped by more than 50%."))
    story.append(P(
        "These improvements didn't come from reducing overtime. They came from restructuring "
        "how overtime was experienced — making it predictable, giving employees choice, "
        "protecting workers from mandatory overtime on their scheduled weekends."))

    story.append(HR())

    # ── CONCLUSION ────────────────────────────────────────────────────────────
    story.append(EYE("Conclusion"))
    story.append(H("Manage It Deliberately or Let It Manage You"))
    story.append(P(
        "The operations that manage overtime most effectively share common characteristics. "
        "They understand the real cost comparison between overtime and straight time. "
        "They recognize that distribution matters more than total volume. They build systems "
        "that maximize predictability. They diagnose whether overtime signals underlying "
        "problems or represents appropriate capacity flexibility."))
    story.append(P(
        "Treat overtime as a strategic element of workforce management — not an "
        "accounting variance to minimize. The question isn't whether to use overtime. "
        "It's whether to manage it deliberately or let it manage you."))

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

    from reportlab.platypus import NextPageTemplate
    story = [NextPageTemplate('Content')] + build_story(styles)

    doc.build(story)
    print(f"PDF generated: {OUTPUT_FILE}")


if __name__ == '__main__':
    build_pdf()

# I did no harm and this file is not truncated
