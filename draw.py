#!/usr/bin/env python3
"""Renderer for the news-image-20261124 front page. Fresh code, written
for this entry. Draws a 1024x1024 newspaper front page with Pillow and
real TrueType fonts. Deterministic: same inputs, same bytes.

Layout is built by stacking measured text blocks: every block is wrapped
first, its height measured, and the cursor only advances by that height,
so nothing overlaps. An assertion guards the bottom margin.

Usage: python3 draw.py [A|B|C] [output-path]
Default variant A, default output entry.png next to this script.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (252, 250, 243)
INK = (17, 17, 17)
GRAY = (85, 85, 85)
LIGHT = (210, 205, 190)
RED = (179, 38, 30)
NAVY = (31, 58, 95)
NAVY_DK = (22, 42, 70)
GOLD = (201, 162, 39)
SKY = (216, 232, 244)
GREEN = (196, 214, 74)

FD = "/usr/share/fonts/truetype/dejavu/"
_cache = {}


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _cache:
        if serif:
            name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
        else:
            name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        _cache[key] = ImageFont.truetype(FD + name, size)
    return _cache[key]


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def block_h(d, text, fnt, max_w, leading):
    return len(wrap(d, text, fnt, max_w)) * leading


def rule(d, x, y, w, fill=INK, width=2):
    d.line([(x, y), (x + w, y)], fill=fill, width=width)


# ---------------- pictograms (simple flat shapes, no text) ----------------

def pic_trophy(d, cx, cy, s, bg=NAVY):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=bg)
    u = s / 50.0
    d.arc([cx - 30 * u, cy - 26 * u, cx - 2 * u, cy + 6 * u], 90, 270,
          fill=GOLD, width=max(2, int(4 * u)))
    d.arc([cx + 2 * u, cy - 26 * u, cx + 30 * u, cy + 6 * u], 270, 90,
          fill=GOLD, width=max(2, int(4 * u)))
    d.polygon([(cx - 20 * u, cy - 28 * u), (cx + 20 * u, cy - 28 * u),
               (cx + 14 * u, cy + 2 * u), (cx - 14 * u, cy + 2 * u)],
              fill=GOLD)
    d.rectangle([cx - 4 * u, cy + 2 * u, cx + 4 * u, cy + 16 * u], fill=GOLD)
    d.rectangle([cx - 16 * u, cy + 16 * u, cx + 16 * u, cy + 24 * u], fill=GOLD)
    d.rectangle([cx - 20 * u, cy + 24 * u, cx + 20 * u, cy + 28 * u], fill=GOLD)


def pic_gauge(d, cx, cy, s, bg=(238, 236, 228)):
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=int(s * 0.18),
                        fill=bg, outline=LIGHT, width=2)
    u = s / 50.0
    d.arc([cx - 30 * u, cy - 22 * u, cx + 30 * u, cy + 38 * u], 180, 360,
          fill=INK, width=max(2, int(4 * u)))
    for ang in (-60, -30, 0, 30, 60):
        a = math.radians(270 + ang)
        x1 = cx + 30 * u * math.cos(a)
        y1 = cy + 8 * u + 30 * u * math.sin(a)
        x2 = cx + 24 * u * math.cos(a)
        y2 = cy + 8 * u + 24 * u * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=INK, width=max(1, int(2 * u)))
    a = math.radians(270 + 38)
    d.line([(cx, cy + 8 * u),
            (cx + 26 * u * math.cos(a), cy + 8 * u + 26 * u * math.sin(a))],
           fill=RED, width=max(2, int(4 * u)))
    d.ellipse([cx - 5 * u, cy + 3 * u, cx + 5 * u, cy + 13 * u], fill=RED)
    d.line([(cx - 26 * u, cy + 30 * u), (cx + 26 * u, cy + 30 * u)],
           fill=INK, width=max(2, int(3 * u)))


def pic_rain(d, cx, cy, s, bg=SKY):
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=int(s * 0.18),
                        fill=bg, outline=LIGHT, width=2)
    u = s / 50.0
    d.ellipse([cx - 30 * u, cy - 26 * u, cx + 2 * u, cy + 2 * u],
              fill=(250, 250, 250), outline=GRAY, width=max(1, int(2 * u)))
    d.ellipse([cx - 10 * u, cy - 32 * u, cx + 30 * u, cy + 2 * u],
              fill=(250, 250, 250), outline=GRAY, width=max(1, int(2 * u)))
    d.rectangle([cx - 26 * u, cy - 8 * u, cx + 28 * u, cy + 2 * u],
                fill=(250, 250, 250))
    for dx in (-20, -7, 6, 19):
        d.line([(cx + dx * u, cy + 12 * u), (cx + (dx - 6) * u, cy + 28 * u)],
               fill=(40, 110, 180), width=max(2, int(4 * u)))


def pic_moon(d, cx, cy, s, bg=NAVY_DK):
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=int(s * 0.18),
                        fill=bg, outline=LIGHT, width=2)
    u = s / 50.0
    d.ellipse([cx - 26 * u, cy - 26 * u, cx + 26 * u, cy + 26 * u],
              fill=(240, 230, 180))
    for ox, oy, r in ((-10, -8, 6), (9, 6, 8), (4, -14, 4)):
        d.ellipse([cx + (ox - r) * u, cy + (oy - r) * u,
                   cx + (ox + r) * u, cy + (oy + r) * u],
                  fill=(214, 202, 150))
    for sx, sy in ((-34, -30), (34, -26), (-32, 30), (32, 32)):
        d.ellipse([cx + sx * u - 2, cy + sy * u - 2,
                   cx + sx * u + 2, cy + sy * u + 2], fill=(255, 255, 255))


def pic_tennis(d, cx, cy, s, bg=(238, 236, 228)):
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=int(s * 0.18),
                        fill=bg, outline=LIGHT, width=2)
    u = s / 50.0
    d.ellipse([cx - 28 * u, cy - 28 * u, cx + 28 * u, cy + 28 * u], fill=GREEN,
              outline=INK, width=max(1, int(2 * u)))
    d.arc([cx - 40 * u, cy - 20 * u, cx + 6 * u, cy + 20 * u], 300, 60,
          fill=(250, 250, 250), width=max(2, int(4 * u)))
    d.arc([cx - 6 * u, cy - 20 * u, cx + 40 * u, cy + 20 * u], 120, 240,
          fill=(250, 250, 250), width=max(2, int(4 * u)))


# ---------------- content ----------------

MASTHEAD = "THE DAY'S NEWS"
DATE_LINE = "TUESDAY, 24 NOVEMBER 2026"

LEAD = {
    "kicker": "AFRICA  •  SPORT  •  LAW",
    "head": "CAS TO RULE TODAY ON SENEGAL'S CUP TITLE",
    "deck": "Sport's top court gives its verdict this afternoon on Senegal's "
            "appeal against losing the Africa Cup of Nations title to Morocco "
            "after January's chaotic final.",
}

STORIES = [
    {"kicker": "ASIA  •  ECONOMY",
     "head": "JAPAN: FACTORIES UP, SERVICES COOL",
     "body": "Flash PMI: manufacturing 53.7, up from 53.3; services 50.5, down "
             "from 51.7. The composite eased to 51.5, a six-month low.",
     "pic": pic_gauge},
    {"kicker": "SOUTH-EAST ASIA  •  WEATHER",
     "head": "HEAVY-RAIN ALERTS ACROSS INDONESIA",
     "body": "BMKG warns of heavy to very heavy rain in many provinces on "
             "Tuesday, with seas up to 2.5 metres.",
     "pic": pic_rain},
    {"kicker": "SCIENCE  •  THE SKY",
     "head": "BEAVER SUPERMOON LIGHTS THE NIGHT",
     "body": "The full moon peaks at 14:53 UTC, about 360,800 km away, near "
             "the Pleiades — the first of a run of supermoons.",
     "pic": pic_moon},
    {"kicker": "EUROPE  •  TENNIS",
     "head": "DAVIS CUP FINALS OPEN IN BOLOGNA",
     "body": "Czechia meet Canada in the first quarter-final at 16:00 CET. "
             "Eight nations chase the title; Italy defend it.",
     "pic": pic_tennis},
]

STRIP = ("ALSO TODAY  —  KYIV AIR-RAID ALERT IN THE EARLY HOURS  •  "
         "GERMANY'S IFO SURVEY DUE")
FOOTER = ("Stories checked against two or more outlets. "
          "Researched 24 Nov 2026, 01:00–01:35 UTC.")


def masthead_centered(d, y, size=92):
    f = font(size, bold=True, serif=True)
    w = d.textlength(MASTHEAD, font=f)
    d.text(((W - w) / 2, y), MASTHEAD, font=f, fill=INK)
    return y + size + 14


def date_bar(d, y):
    rule(d, 36, y, W - 72, width=3)
    f = font(25, bold=True)
    w = d.textlength(DATE_LINE, font=f)
    d.text(((W - w) / 2, y + 8), DATE_LINE, font=f, fill=INK)
    rule(d, 36, y + 44, W - 72, width=3)
    return y + 56


def strip_bar(d, y, h=44):
    d.rectangle([36, y, W - 36, y + h], fill=INK)
    size = 18
    f = font(size, bold=True)
    while d.textlength(STRIP, font=f) > W - 72 - 16 and size > 10:
        size -= 1
        f = font(size, bold=True)
    tw = d.textlength(STRIP, font=f)
    d.text(((W - tw) / 2, y + (h - size - 4) / 2), STRIP, font=f,
           fill=(255, 255, 255))
    return y + h


def footer(d, y):
    f = font(14)
    for line in wrap(d, FOOTER, f, W - 72):
        w = d.textlength(line, font=f)
        d.text(((W - w) / 2, y), line, font=f, fill=GRAY)
        y += 19
    return y


def finish(img, d, y):
    assert y <= 990, f"layout overflow: ends at y={y}"
    return img


# ---------------- variant A: lead + 2x2 grid ----------------

def render_a():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((36, 26), "THE WORLD IN ONE PAGE", font=font(16, bold=True), fill=GRAY)
    ed = "EARLY EDITION"
    d.text((W - 36 - d.textlength(ed, font=font(16, bold=True)), 26), ed,
           font=font(16, bold=True), fill=GRAY)
    y = masthead_centered(d, 44, size=78)
    y = date_bar(d, y + 2)
    # lead block, measured
    ly = y + 16
    kf, hf, bf = font(16, bold=True), font(42, bold=True, serif=True), font(19)
    text_w = 600
    hh = block_h(d, LEAD["head"], hf, text_w, 48)
    bh = block_h(d, LEAD["deck"], bf, text_w, 25)
    lead_h = 14 + 6 + hh + 6 + bh
    panel_h = max(lead_h + 20, 200)
    d.text((36, ly), LEAD["kicker"], font=kf, fill=RED)
    block(d, 36, ly + 20, LEAD["head"], hf, INK, text_w, 48)
    block(d, 36, ly + 20 + hh + 6, LEAD["deck"], bf, INK, text_w, 25)
    px, pw = 664, 324
    d.rectangle([px, ly - 6, px + pw, ly - 6 + panel_h], fill=NAVY)
    d.rectangle([px + 10, ly + 4, px + pw - 10, ly - 6 + panel_h - 10],
                outline=GOLD, width=2)
    pic_trophy(d, px + pw // 2, ly - 6 + panel_h // 2 - 16, 84)
    cap = "THE TITLE AT STAKE"
    d.text((px + (pw - d.textlength(cap, font=font(15, bold=True))) / 2,
            ly - 6 + panel_h - 30), cap, font=font(15, bold=True),
           fill=(255, 255, 255))
    y = ly - 6 + panel_h + 20
    rule(d, 36, y, W - 72, width=2)
    y += 14
    # 2x2 grid, row height measured from content
    cw, gap = 466, 20
    gx = [36, 36 + cw + gap]
    for row in range(2):
        cells = STORIES[row * 2:(row + 1) * 2]
        heights = []
        for st in cells:
            hh2 = block_h(d, st["head"], font(26, bold=True, serif=True),
                          cw - 104, 30)
            bh2 = block_h(d, st["body"], font(18), cw - 104, 24)
            heights.append(10 + 20 + 4 + hh2 + 4 + bh2)
        rh = max(heights + [140])
        for j, st in enumerate(cells):
            x = gx[j]
            rule(d, x, y, cw, fill=RED, width=3)
            d.text((x, y + 10), st["kicker"], font=font(14, bold=True), fill=RED)
            ny = block(d, x, y + 34, st["head"],
                       font(26, bold=True, serif=True), INK, cw - 104, 30)
            block(d, x, ny + 4, st["body"], font(18), INK, cw - 104, 24)
            st["pic"](d, x + cw - 46, y + 52, 40)
        y += rh + 12
    rule(d, 36, y, W - 72, width=2)
    y = strip_bar(d, y + 12)
    y = footer(d, y + 10)
    return finish(img, d, y)


# ---------------- variant B: banner lead + 4 columns ----------------

def render_b():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f = font(58, bold=True, serif=True)
    d.text((36, 30), MASTHEAD, font=f, fill=INK)
    y = 30 + 58 + 8
    df = font(22, bold=True)
    d.text((36, y), DATE_LINE, font=df, fill=RED)
    d.text((W - 36 - d.textlength("EARLY EDITION", font=df), y),
           "EARLY EDITION", font=df, fill=GRAY)
    y += 32
    rule(d, 36, y, W - 72, width=3)
    y += 12
    d.text((36, y), "THE WORLD IN ONE PAGE", font=font(16, bold=True), fill=GRAY)
    y += 28
    # banner, measured
    kf, hf, bf = font(16, bold=True), font(40, bold=True, serif=True), font(19)
    text_w = 560
    hh = block_h(d, LEAD["head"], hf, text_w, 46)
    bh = block_h(d, LEAD["deck"], bf, text_w, 25)
    banner_h = 18 + 16 + 8 + hh + 8 + bh + 18
    d.rectangle([36, y, W - 36, y + banner_h], fill=NAVY)
    d.text((60, y + 18), LEAD["kicker"], font=kf, fill=(255, 214, 110))
    block(d, 60, y + 42, LEAD["head"], hf, (255, 255, 255), text_w, 46)
    block(d, 60, y + 42 + hh + 8, LEAD["deck"], bf, (235, 235, 235), text_w, 25)
    pic_trophy(d, 838, y + banner_h // 2, 78, bg=NAVY_DK)
    y += banner_h + 14
    # 4 columns, height measured
    cw, gap = 226, 8
    col_h = 0
    for st in STORIES:
        kh = block_h(d, st["kicker"], font(13, bold=True), cw, 17)
        hh2 = block_h(d, st["head"], font(22, bold=True, serif=True), cw, 27)
        bh2 = block_h(d, st["body"], font(16), cw, 22)
        col_h = max(col_h, 3 + 12 + kh + 8 + hh2 + 8 + 84 + 8 + bh2)
    for i, st in enumerate(STORIES):
        x = 36 + i * (cw + gap)
        rule(d, x, y, cw, fill=RED, width=3)
        ny = block(d, x, y + 12, st["kicker"], font(13, bold=True), RED, cw, 17)
        ny = block(d, x, ny + 8, st["head"], font(22, bold=True, serif=True),
                   INK, cw, 27)
        st["pic"](d, x + cw // 2, ny + 50, 40)
        block(d, x, ny + 100, st["body"], font(16), INK, cw, 22)
    y += col_h + 14
    rule(d, 36, y, W - 72, width=2)
    y = strip_bar(d, y + 12)
    y = footer(d, y + 10)
    return finish(img, d, y)


# ---------------- variant C: stacked bands ----------------

def render_c():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((36, 26), "THE WORLD IN ONE PAGE", font=font(16, bold=True), fill=GRAY)
    ed = "EARLY EDITION"
    d.text((W - 36 - d.textlength(ed, font=font(16, bold=True)), 26), ed,
           font=font(16, bold=True), fill=GRAY)
    y = masthead_centered(d, 48, size=64)
    y = date_bar(d, y + 2)
    y += 12
    # lead band
    kf, hf, bf = font(15, bold=True), font(36, bold=True, serif=True), font(18)
    text_w = W - 72 - 190
    hh = block_h(d, LEAD["head"], hf, text_w, 42)
    bh = block_h(d, LEAD["deck"], bf, text_w, 24)
    band_h = 14 + 14 + 6 + hh + 6 + bh + 10
    d.rectangle([36, y, W - 36, y + band_h], fill=NAVY)
    d.text((60, y + 14), LEAD["kicker"], font=kf, fill=(255, 214, 110))
    block(d, 60, y + 36, LEAD["head"], hf, (255, 255, 255), text_w, 42)
    block(d, 60, y + 36 + hh + 6, LEAD["deck"], bf, (235, 235, 235), text_w, 24)
    pic_trophy(d, W - 36 - 80, y + band_h // 2, 62, bg=NAVY_DK)
    y += band_h + 10
    # four bands
    for st in STORIES:
        kf2 = font(14, bold=True)
        hf2 = font(26, bold=True, serif=True)
        bf2 = font(18)
        text_w2 = W - 72 - 120
        hh2 = block_h(d, st["head"], hf2, text_w2, 29)
        bh2 = block_h(d, st["body"], bf2, text_w2, 22)
        bh_total = 10 + 18 + 4 + hh2 + 4 + bh2 + 10
        rule(d, 36, y, W - 72, fill=RED, width=3)
        d.text((168, y + 10), st["kicker"], font=kf2, fill=RED)
        ny = block(d, 168, y + 32, st["head"], hf2, INK, text_w2, 29)
        block(d, 168, ny + 4, st["body"], bf2, INK, text_w2, 22)
        st["pic"](d, 36 + 52, y + bh_total // 2, 40)
        y += bh_total + 6
    rule(d, 36, y, W - 72, width=2)
    y = strip_bar(d, y + 10)
    y = footer(d, y + 10)
    return finish(img, d, y)


RENDER = {"A": render_a, "B": render_b, "C": render_c}


def main():
    variant = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
    out = sys.argv[2] if len(sys.argv) > 2 else "entry.png"
    img = RENDER[variant]()
    img.save(out, "PNG", optimize=True)
    print(f"variant {variant} -> {out} {img.size}")


if __name__ == "__main__":
    main()
