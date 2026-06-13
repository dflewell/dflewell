"""Generate a Drive-friendly PDF of the consent walkthrough.

Renders the same content as consent-deck.html into a 16:9 PDF (one slide per page),
so it uploads to Google Drive / Slides and renders + shares cleanly in any browser.

Re-run after editing the slide content below:
    pip install reportlab
    python governance/build_pdf.py
"""
import os
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# --- palette (matches the HTML deck) ---
CREAM   = HexColor("#f4f1ea")
INK     = HexColor("#2b2b2b")
BODY    = HexColor("#3a3a3a")
MUTED   = HexColor("#6b6b6b")
TERRA   = HexColor("#b5651d")
CARD    = HexColor("#ffffff")
BLUEBG  = HexColor("#e8f0fe")
REDBG   = HexColor("#fce8e6")
GREENBG = HexColor("#e6f4ea")

# 16:9 slide in points (PowerPoint default 13.333" x 7.5").
PAGE_W, PAGE_H = 960, 540
MARGIN = 70

OUT = os.path.join(os.path.dirname(__file__), "consent-deck.pdf")

c = canvas.Canvas(OUT, pagesize=(PAGE_W, PAGE_H))


def top(y):
    """Convert a top-origin y into reportlab's bottom-origin."""
    return PAGE_H - y


def wrap(text, font, size, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, font="Helvetica", size=18, color=BODY, max_w=None, leading=None):
    """Draw text from a top-origin y. Returns the y just below the text block."""
    c.setFont(font, size)
    c.setFillColor(color)
    leading = leading or size * 1.35
    lines = wrap(s, font, size, max_w) if max_w else [s]
    for line in lines:
        c.drawString(x, top(y) - size, line)
        y += leading
    return y


def kicker(s, y=MARGIN):
    return text(x=MARGIN, y=y, s=s.upper(), font="Helvetica-Bold", size=12, color=TERRA)


def bg():
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def card(x, y, w, h, fill=CARD, radius=12, border=None):
    if border:
        c.setStrokeColor(border)
        c.setLineWidth(2)
    c.setFillColor(fill)
    c.roundRect(x, top(y) - h, w, h, radius, fill=1, stroke=1 if border else 0)


def footer(n, total):
    c.setFont("Helvetica", 10)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - 30, 24, f"{n} / {total}")


# ---------------- slides ----------------

def slide_title():
    bg()
    kicker("True North AI · Email Triage")
    y = text(MARGIN, 120, "Before we connect anything,", "Helvetica-Bold", 40, INK)
    y = text(MARGIN, y + 4, "here's exactly how this works.", "Helvetica-Bold", 40, INK)
    y = text(MARGIN, y + 24, "What it does · where your data goes · how you stay in control.",
             "Helvetica", 20, MUTED, max_w=PAGE_W - 2 * MARGIN)
    text(MARGIN, 430,
         "You can stop me at any point, and you can revoke my access yourself at any time "
         "— without involving me.", "Helvetica", 16, MUTED, max_w=PAGE_W - 2 * MARGIN)


def slide_promise():
    bg()
    kicker("The promise")
    # terra accent bar
    c.setFillColor(TERRA)
    c.rect(MARGIN, top(290), 6, 120, fill=1, stroke=0)
    text(MARGIN + 28, 150, "“Nothing touches your inbox", "Helvetica-Bold", 34, INK)
    text(MARGIN + 28, 198, "unless you press the button.”", "Helvetica-Bold", 34, INK)
    text(MARGIN, 340,
         "There is no background process reading your mail. The tool runs only when you click "
         "“Start my morning.” No button press, no activity.",
         "Helvetica", 19, BODY, max_w=PAGE_W - 2 * MARGIN)


def slide_loop():
    bg()
    kicker("What happens when you click")
    text(MARGIN, 110, "It proposes. You decide.", "Helvetica-Bold", 30, INK)
    steps = ["Pull overnight mail", "Sort into 4 buckets", "Draft suggested replies", "Show you a summary"]
    x, y, h = MARGIN, 190, 56
    c.setFont("Helvetica-Bold", 15)
    for i, s in enumerate(steps):
        w = c.stringWidth(s, "Helvetica-Bold", 15) + 36
        card(x, y, w, h)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(x + 18, top(y) - 35, s)
        x += w
        if i < len(steps) - 1:
            c.setFillColor(TERRA)
            c.setFont("Helvetica-Bold", 22)
            c.drawString(x + 6, top(y) - 38, "→")
            x += 34
    text(MARGIN, 300,
         "At this stage it only proposes. It does not send, delete, or move anything. "
         "You review everything before any action is ever taken.",
         "Helvetica", 19, BODY, max_w=PAGE_W - 2 * MARGIN)


def slide_buckets():
    bg()
    kicker("The four buckets")
    text(MARGIN, 110, "So nothing time-sensitive gets lost.", "Helvetica-Bold", 30, INK)
    cats = [
        ("Client", "From or about a client — highest care, always reviewed."),
        ("Important", "Time-sensitive or needs your personal attention."),
        ("Shopping", "Receipts, orders, promotions, coupons."),
        ("Read later", "Newsletters, FYI, low-priority."),
    ]
    cw, ch, gap = (PAGE_W - 2 * MARGIN - 24) / 2, 110, 24
    for i, (title, desc) in enumerate(cats):
        col, row = i % 2, i // 2
        x = MARGIN + col * (cw + gap)
        y = 175 + row * (ch + gap)
        card(x, y, cw, ch)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 20)
        c.drawString(x + 22, top(y) - 36, title)
        c.setFillColor(MUTED); c.setFont("Helvetica", 14)
        for j, line in enumerate(wrap(desc, "Helvetica", 14, cw - 44)):
            c.drawString(x + 22, top(y) - 60 - j * 19, line)


def slide_data():
    bg()
    kicker("Where your data goes")
    text(MARGIN, 110, "Three places. No more.", "Helvetica-Bold", 30, INK)
    places = [
        ("1 · Gmail", "Your mail stays in your own account. We request read access only.", BLUEBG),
        ("2 · Claude API", "Each message's text is sent to sort it — in transit only, and not used to train models.", REDBG),
        ("3 · Your private database", "A categorized copy, yours alone — no sharing with anyone else I work with — with the bodies encrypted.", GREENBG),
    ]
    cw, ch, gap = (PAGE_W - 2 * MARGIN - 2 * 20) / 3, 230, 20
    for i, (title, desc, fill) in enumerate(places):
        x = MARGIN + i * (cw + gap)
        y = 175
        card(x, y, cw, ch, fill=fill)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 16)
        for j, line in enumerate(wrap(title, "Helvetica-Bold", 16, cw - 40)):
            c.drawString(x + 20, top(y) - 34 - j * 20, line)
        c.setFillColor(BODY); c.setFont("Helvetica", 13.5)
        for j, line in enumerate(wrap(desc, "Helvetica", 13.5, cw - 40)):
            c.drawString(x + 20, top(y) - 80 - j * 19, line)


def slide_delete():
    bg()
    kicker("How long · how to delete")
    text(MARGIN, 110, "You can erase it all in one click.", "Helvetica-Bold", 30, INK)
    bullets = [
        "The categorized history is kept so you get a durable, searchable archive — the goal is "
        "that you never lose an email again, so nothing is auto-deleted.",
        "On a single request, I delete your entire database and the stored access token.",
        "You can also cut off my access yourself in your Google security settings in ~30 seconds.",
        "I confirm any deletion in writing.",
    ]
    y = 180
    for b in bullets:
        c.setFillColor(TERRA); c.setFont("Helvetica-Bold", 18)
        c.drawString(MARGIN, top(y) - 18, "•")
        y2 = text(MARGIN + 24, y, b, "Helvetica", 18, BODY, max_w=PAGE_W - 2 * MARGIN - 24)
        y = y2 + 10


def slide_scope():
    bg()
    kicker("The access I'll request")
    text(MARGIN, 110, "Read-and-modify — but I only ever propose.", "Helvetica-Bold", 28, INK)
    y = text(MARGIN, 180,
             "The modify permission is there for later, only if and when you decide you want the tool "
             "to move or file mail for you. Today, at the starting rung, it reads and suggests — "
             "nothing more.", "Helvetica", 19, BODY, max_w=PAGE_W - 2 * MARGIN)
    text(MARGIN, y + 16, "We move at your pace.", "Helvetica-Oblique", 18, MUTED)


def slide_ladder():
    bg()
    kicker("The trust ladder")
    text(MARGIN, 105, "We start at the top of caution.", "Helvetica-Bold", 30, INK)
    rungs = [
        ("1 · Assisted", "You click, the tool proposes, you review everything before any send or move.", True),
        ("2 · Supervised", "Tool auto-handles safe buckets (shopping, read-later); drafts and client mail still reviewed.", False),
        ("3 · Automated", "Scheduled runs, minimal review. Only if you ask for it.", False),
    ]
    y, h = 165, 92
    for title, desc, start in rungs:
        card(MARGIN, y, PAGE_W - 2 * MARGIN, h, border=TERRA if start else None)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 18)
        c.drawString(MARGIN + 22, top(y) - 32, title)
        if start:
            label = "WE START HERE"
            lw = c.stringWidth(label, "Helvetica-Bold", 10) + 20
            c.setFillColor(TERRA)
            c.roundRect(MARGIN + 160, top(y) - 38, lw, 22, 11, fill=1, stroke=0)
            c.setFillColor(CARD); c.setFont("Helvetica-Bold", 10)
            c.drawString(MARGIN + 170, top(y) - 33, label)
        c.setFillColor(MUTED); c.setFont("Helvetica", 14)
        for j, line in enumerate(wrap(desc, "Helvetica", 14, PAGE_W - 2 * MARGIN - 44)):
            c.drawString(MARGIN + 22, top(y) - 56 - j * 18, line)
        y += h + 16


def slide_close():
    bg()
    kicker("Your call")
    text(MARGIN, 150, "Comfortable with this?", "Helvetica-Bold", 44, INK)
    text(MARGIN, 230, "Any questions before we connect your account?", "Helvetica", 22, BODY)
    text(MARGIN, 430, "True North AI · governance-first by design.", "Helvetica", 16, MUTED)


SLIDES = [slide_title, slide_promise, slide_loop, slide_buckets, slide_data,
          slide_delete, slide_scope, slide_ladder, slide_close]

for n, fn in enumerate(SLIDES, 1):
    fn()
    footer(n, len(SLIDES))
    c.showPage()

c.save()
print(f"Wrote {OUT} ({len(SLIDES)} pages)")
