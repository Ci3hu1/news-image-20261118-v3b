#!/usr/bin/env python3
"""THE DAY IN WORLD NEWS -- Wednesday, 18 November 2026.

A 1024x1024 newspaper front page summing up the world news of
Wednesday 18 November 2026: 45 stories, 13 of them flat-illustrated,
a one-line summary of the day, a BY THE NUMBERS strip, a dotted world
map with numbered pins and labels, and briefs 14-45.

Stdlib only. Pillow is used ONLY if it is importable AND every DejaVu
face this script needs exists on the system. Otherwise the bundled
entry.png is copied byte-for-byte to the output path, so the page is
identical on a machine with no Pillow at all.

    python3 main.py               # writes output.png next to main.py
    python3 main.py --output x.png
    python3 main.py --check       # verify data + renderability, no file
"""

import argparse
import os
import shutil
import sys

# ---------------------------------------------------------------- data

DATE_LINE = "Wednesday, 18 November 2026"
TITLE = "THE DAY IN WORLD NEWS"
SUMMARY = (
    "Gulf strikes and retaliation, a bridge down in the Kerch Strait, a summit "
    "in Shenzhen \u2014 and Voyager 1 a light-day from home."
)

NUMBERS = [
    ("11,000+", "Ebola cases in DR Congo"),
    ("5,412", "US measles cases in 2026"),
    ("$115.8B", "Nvidia quarterly revenue"),
    ("56\u201344", "Democrats take US Senate"),
    ("16bn miles", "Voyager 1 from Earth"),
    ("19", "killed in Siberian plane crash"),
]

# Stories 1-13: the illustrated features. lat/lon place each pin on the map.
STORIES = [
    dict(n=1, kicker="THE GULF", kind="jet",
         headline="US strikes Iranian island as Iran hits Bahrain and Kuwait",
         deck="US jets hit a Guard missile site on Qeshm after Iran fired drones "
              "at a US radar site in Bahrain and at Patriot systems in Kuwait.",
         lat=26.9, lon=56.2, bg="#1d4ed8"),
    dict(n=2, kicker="UKRAINE", kind="bridge",
         headline="Kerch Bridge hit for a second day; part of road span falls",
         deck="Ukraine struck the bridge to Crimea again; part of its road span "
              "fell into the strait.",
         lat=45.3, lon=36.5, bg="#0f766e", dy=-12),
    dict(n=3, kicker="APEC \u00b7 SHENZHEN", kind="summit",
         headline="Xi, Putin and Trump to meet in Shenzhen this week",
         deck="Xi denounced protectionism and Putin attacked sanctions as APEC "
              "opened in Shenzhen.",
         lat=22.5, lon=114.0, bg="#b91c1c"),
    dict(n=4, kicker="US MIDTERMS", kind="ballot",
         headline="Peltola wins Alaska Senate seat; Democrats reach 56 seats",
         deck="Peltola beat incumbent Dan Sullivan, giving Democrats a 56\u201344 majority.",
         lat=64.0, lon=-152.0, bg="#7c3aed"),
    dict(n=5, kicker="HEALTH \u00b7 DR CONGO", kind="virus",
         headline="Ebola outbreak more than doubles: 11,000 cases, 5,400 dead",
         deck="The outbreak reached 67 health zones in eight provinces; children "
              "bear the heaviest toll.",
         lat=-1.5, lon=29.0, bg="#9a3412"),
    dict(n=6, kicker="TECH \u00b7 EARNINGS", kind="chip",
         headline="Nvidia revenue doubles to $115.8bn in first results without Huang",
         deck="Revenue rose 103% year on year; data-centre sales hit $107.6bn. "
              "Shares +4.8% after hours.",
         lat=37.35, lon=-121.95, bg="#15803d"),
    dict(n=7, kicker="SPACE", kind="probe",
         headline="Voyager 1 reaches one light-day from Earth",
         deck="At 05:16 ET the 1977 probe passed 16 billion miles out \u2014 a record distance.",
         lat=34.2, lon=-118.1, bg="#0e7490", dx=16, dy=14),
    dict(n=8, kicker="WEATHER", kind="cyclone",
         headline="Category 5 Cyclone Xavier hits Northern Cook Islands",
         deck="Fiercest storm of the season hits the northern atolls.",
         lat=-9.8, lon=-161.0, bg="#0369a1"),
    dict(n=9, kicker="HEALTH \u00b7 USA", kind="measles",
         headline="US loses measles elimination status after 26 years",
         deck="5,412 cases in 2026 across 45 states; 10 deaths.",
         lat=38.9, lon=-77.0, bg="#be185d"),
    dict(n=10, kicker="THE HAGUE", kind="court",
         headline="World Court to rule on Myanmar genocide case",
         deck="ICJ rules tomorrow in the Rohingya genocide case.",
         lat=52.07, lon=4.3, bg="#44403c"),
    dict(n=11, kicker="DISASTER \u00b7 RUSSIA", kind="plane",
         headline="Russian military plane crashes in Siberia; 19 dead",
         deck="Aircraft came down in Kemerovo; all 19 aboard killed.",
         lat=55.36, lon=86.08, bg="#57534e"),
    dict(n=12, kicker="EARTHQUAKES", kind="quake",
         headline="6.0 quake strikes Papua New Guinea; 5.3 shakes Romania",
         deck="No major damage reported in either place by press time.",
         lat=-6.3, lon=147.0, bg="#a16207"),
    dict(n=13, kicker="CLIMATE \u00b7 COP31", kind="climate",
         headline="COP31 draft sparks Africa outrage over fossil fuels",
         deck="Draft weakens fossil-fuel exit, campaigners say.",
         lat=36.9, lon=30.7, bg="#166534", dx=-8, dy=12),
]

# Briefs 14-45: one line each, with a region tag.
BRIEFS = [
    (14, "MANILA", "Trump meets Manila, Quad allies."),
    (15, "HORMUZ", "Iran downs a US MQ-9 drone."),
    (16, "KUWAIT", "Iran drones hit US Patriot batteries."),
    (17, "SUN", "M1.1-class solar flare recorded."),
    (18, "GAZA", "Cold threatens families in tents."),
    (19, "ISRAEL", "Kahana elected Knesset speaker."),
    (20, "LONDON", "UK sanctions eight Israeli builders."),
    (21, "CANBERRA", "Australia lists Weiss, Amana."),
    (22, "NEW YORK", "Mamdani backs protest bill."),
    (23, "SKOPJE", "Mossad tip foils Iran murder plot."),
    (24, "SUDAN", "UN: 2,230 civilians killed."),
    (25, "CONGO", "Heavy combat on Kivu fronts."),
    (26, "S. SUDAN", "Lagu's daughter recalls his dream."),
    (27, "NIGERIA", "UK pastor jailed ~12 years for rape."),
    (28, "S. AFRICA", "Shopkeeper killed in arson wave."),
    (29, "KENYA", "Parity for women still 63 years away."),
    (30, "NIGERIA", "Governor probes student's death."),
    (31, "S. AFRICA", "Water curbs hit Johannesburg."),
    (32, "EGYPT", "Ex-housing official jailed 15 years."),
    (33, "FOOTBALL", "C\u00f4te d'Ivoire draw late vs Gambia."),
    (34, "GAMING", "GTA 6 unlocks midnight 19 Nov."),
    (35, "AI", "OpenAI ships GPT-6.2 Astra."),
    (36, "AI", "Anthropic IPO ~7x oversubscribed."),
    (37, "TECH", "Instagram scans for copied Reels."),
    (38, "MARKETS", "SEC probes Nvidia disclosures."),
    (39, "MARKETS", "S&P \u22121.03%; Brent $91.55."),
    (40, "USA", "Computer outages reach the NSA."),
    (41, "COP31", "EU: distractions risk 'untenable' talks."),
    (42, "COP31", "T\u00fcrkiye: triple ocean finance by 2035."),
    (43, "ECONOMY", "US retail sales +0.2% in October."),
    (44, "ECONOMY", "FOMC minutes due tomorrow."),
    (45, "COP31", "Theme: Human Development."),
]

MAP_LABELS = [  # (text, lon, lat) -- placed clear of the numbered pins
    ("NORTH AMERICA", -100, 52), ("SOUTH AMERICA", -60, -14),
    ("EUROPE", 18, 60), ("AFRICA", 5, -5), ("ASIA", 95, 40),
    ("OCEANIA", 134, -24), ("GREENLAND", -42, 74),
    ("PACIFIC OCEAN", -130, -28), ("ATLANTIC OCEAN", -30, 8),
    ("INDIAN OCEAN", 78, -32),
]

# Coarse continent outlines (lon, lat) for the dotted map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50),
     (-73, -53), (-70, -40), (-72, -20), (-80, -5), (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (25, 71), (18, 69),
     (12, 65), (5, 60), (-5, 58), (-10, 50)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (38, 22), (43, 12), (48, 11), (51, 10), (44, 0), (40, -10), (35, -18),
     (32, -26), (28, -33), (20, -35), (16, -28), (12, -18), (9, -1), (9, 4),
     (-8, 5), (-13, 8), (-17, 12)],
    [(30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76), (130, 72),
     (160, 70), (178, 66), (170, 60), (162, 56), (158, 52), (142, 50),
     (140, 40), (130, 33), (127, 35), (122, 38), (120, 30), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 13), (76, 8),
     (72, 20), (66, 25), (60, 25), (55, 26), (50, 30), (48, 30), (43, 28),
     (40, 32), (36, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (132, -32), (140, -38),
     (147, -39), (153, -32), (153, -27), (146, -19), (142, -11), (136, -12),
     (132, -11), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (174, -41), (178, -38), (173, -35)],
    [(-45, 60), (-40, 65), (-30, 68), (-22, 70), (-25, 76), (-40, 80),
     (-55, 76), (-58, 70), (-55, 64)],
]

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
MUTED = (90, 84, 72)
RED = (185, 28, 28)
RULE = (26, 26, 26)
TINT = (238, 232, 214)

REQUIRED_FONTS = [
    "DejaVuSans.ttf", "DejaVuSans-Bold.ttf",
    "DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf",
]
FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    os.path.expanduser("~/.fonts"),
]


def find_fonts():
    """Return {name: path} if Pillow and every DejaVu face exist, else None."""
    try:
        import PIL  # noqa: F401
    except Exception:
        return None
    found = {}
    for name in REQUIRED_FONTS:
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                found[name] = p
                break
        else:
            return None
    return found


def here(*parts):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *parts)

# ---------------------------------------------------------------- helpers

def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, font, x, y, max_w, max_lines, fill=INK, lh=None):
    """Draw wrapped text, truncating the last line with an ellipsis."""
    lh = lh or int(font.size * 1.22)
    lines = wrap(draw, text, font, max_w)[:max_lines]
    if len(lines) == max_lines and len(wrap(draw, text, font, max_w)) > max_lines:
        while lines and draw.textlength(lines[-1] + "\u2026", font=font) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "\u2026"
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=font, fill=fill)
    return y + len(lines) * lh


def point_in_polygon(x, y, poly):
    inside, n = False, len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


# ---------------------------------------------------------------- flat illustrations
# Every illustration is drawn from primitives only: no photos, no clip-art,
# no external assets. One distinct motif per story, flat colours, thick
# outlines -- the same visual language across all 13.

def illus(draw, kind, x, y, w, h, bg):
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    white, dark = (255, 255, 255), (26, 26, 26)
    s = min(w, h)
    if kind == "jet":  # fighter jet over a missile site
        draw.polygon([(x + 10, cy + 2), (x + w - 22, cy - 8), (x + w - 10, cy + 2),
                      (x + w - 22, cy + 10), (x + 34, cy + 8)], fill=white)
        draw.polygon([(cx - 8, cy - 2), (cx + 4, cy - 20), (cx + 12, cy - 2)], fill=white)
        draw.polygon([(cx - 2, cy + 6), (cx + 8, cy + 18), (cx + 16, cy + 6)], fill=white)
        draw.ellipse([x + w - 34, cy - 2, x + w - 26, cy + 6], fill=(147, 197, 253))
        for i in range(3):
            draw.ellipse([x + 14 + i * 16, y + h - 16, x + 24 + i * 16, y + h - 6],
                         fill=(253, 224, 71))
    elif kind == "bridge":  # bridge span, one section fallen
        draw.line([x + 6, cy, x + w - 6, cy], fill=white, width=5)
        for bx in (x + 18, x + w // 2 - 4, x + w - 26):
            draw.line([bx, y + 8, bx, cy], fill=white, width=4)
        draw.polygon([(x + w // 2 + 2, cy), (x + w // 2 + 26, cy + 22),
                      (x + w // 2 + 34, cy + 18), (x + w // 2 + 12, cy - 4)],
                     fill=(253, 224, 71))
        draw.arc([x + 8, cy + 8, x + w - 8, y + h - 4], 0, 180, fill=(147, 197, 253), width=3)
    elif kind == "summit":  # three leaders, three flags (scales to strip height)
        for i, col in enumerate(((185, 28, 28), (29, 78, 216), (220, 38, 38))):
            fx = x + 14 + i * (w // 3)
            pole_h = max(10, int(h * 0.42))
            draw.line([fx, y + 4, fx, y + 4 + pole_h], fill=white, width=3)
            draw.polygon([(fx, y + 4), (fx + 22, y + 10), (fx, y + 16)], fill=col)
            hy0 = y + 4 + pole_h + 4
            draw.ellipse([fx - 2, hy0, fx + 14, hy0 + 12], fill=(251, 191, 36))
            draw.rectangle([fx - 6, hy0 + 10, fx + 18, y + h - 4], fill=white)
    elif kind == "ballot":  # ballot box with a tick
        draw.rectangle([x + 14, cy - 6, x + w - 14, y + h - 8], fill=white)
        draw.rectangle([x + w // 2 - 14, cy - 16, x + w // 2 + 14, cy - 6], fill=dark)
        draw.line([x + 24, cy + 12, x + w // 2 - 2, cy + 26, x + w - 26, cy - 2],
                  fill=(220, 38, 38), width=5)
    elif kind == "virus":  # spiked virus cell
        draw.ellipse([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4], fill=(253, 224, 71))
        for a in range(0, 360, 45):
            import math
            r = math.radians(a)
            x1, y1 = cx + int(0.28 * s * math.cos(r)), cy + int(0.28 * s * math.sin(r))
            x2, y2 = cx + int(0.46 * s * math.cos(r)), cy + int(0.46 * s * math.sin(r))
            draw.line([x1, y1, x2, y2], fill=(253, 224, 71), width=4)
            draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(253, 224, 71))
    elif kind == "chip":  # microchip
        draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                       fill=(34, 197, 94), outline=white, width=3)
        draw.rectangle([cx - s // 8, cy - s // 8, cx + s // 8, cy + s // 8], fill=white)
        for i in range(3):
            off = -s // 6 + i * s // 6
            draw.line([cx - s // 4 - 8, cy + off, cx - s // 4, cy + off], fill=white, width=3)
            draw.line([cx + s // 4, cy + off, cx + s // 4 + 8, cy + off], fill=white, width=3)
            draw.line([cx + off, cy - s // 4 - 8, cx + off, cy - s // 4], fill=white, width=3)
            draw.line([cx + off, cy + s // 4, cx + off, cy + s // 4 + 8], fill=white, width=3)
    elif kind == "probe":  # deep-space probe and stars
        for sx, sy in ((x + 12, y + 10), (x + w - 16, y + 14), (x + w - 30, y + h - 14),
                       (x + 20, y + h - 18), (x + w // 2, y + 8)):
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=white)
        draw.line([cx - 16, cy + 10, cx + 16, cy - 14], fill=white, width=4)
        draw.ellipse([cx - 8, cy - 22, cx + 8, cy - 6], fill=(253, 224, 71))
        draw.polygon([(cx - 22, cy + 12), (cx + 4, cy + 2), (cx + 2, cy + 18)], fill=white)
    elif kind == "cyclone":  # spiral storm
        for r in range(6, s // 2, 7):
            draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 20, fill=white, width=4)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(253, 224, 71))
    elif kind == "measles":  # dotted rash pattern
        for i in range(4):
            for j in range(3):
                draw.ellipse([x + 12 + i * (w - 24) // 3, y + 12 + j * (h - 24) // 2,
                              x + 24 + i * (w - 24) // 3, y + 24 + j * (h - 24) // 2],
                             fill=(244, 114, 182) if (i + j) % 2 else white)
    elif kind == "court":  # courthouse columns and scales
        draw.rectangle([x + 10, y + 10, x + w - 10, y + 18], fill=white)
        for i in range(3):
            px = x + 18 + i * (w - 36) // 2
            draw.rectangle([px, y + 20, px + 8, y + h - 14], fill=white)
        draw.rectangle([x + 10, y + h - 14, x + w - 10, y + h - 8], fill=white)
        draw.line([cx, y + 22, cx, y + 30], fill=(253, 224, 71), width=3)
    elif kind == "plane":  # aircraft silhouette
        draw.polygon([(x + 10, cy), (x + w - 16, cy - 10), (x + w - 8, cy),
                      (x + w - 16, cy + 8), (x + 34, cy + 8)], fill=white)
        draw.polygon([(cx - 6, cy - 4), (cx + 6, cy - 20), (cx + 14, cy - 4)], fill=white)
        draw.polygon([(cx - 2, cy + 6), (cx + 10, cy + 18), (cx + 16, cy + 6)], fill=white)
    elif kind == "quake":  # cracked ground, seismograph line
        draw.line([x + 6, cy + 6, x + w // 3, cy - 12, x + w // 2, cy + 14,
                   x + 2 * w // 3, cy - 8, x + w - 6, cy + 4], fill=(253, 224, 71), width=4)
        draw.polygon([(x + w // 2 - 4, cy + 10), (x + w // 2 + 10, y + h - 6),
                      (x + w // 2 + 18, y + h - 6), (x + w // 2 + 4, cy + 10)], fill=white)
    elif kind == "climate":  # globe with a leaf
        draw.ellipse([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                     outline=white, width=3)
        draw.arc([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4], 200, 340,
                 fill=white, width=3)
        draw.ellipse([cx + 2, cy - 2, cx + s // 4, cy + s // 5], fill=(74, 222, 128))


# ---------------------------------------------------------------- map

def draw_map(draw, fonts, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 244))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    step = 7
    for py in range(y + 4, y + h - 3, step):
        for px in range(x + 4, x + w - 3, step):
            lon = (px - x) / w * 360 - 180
            lat = 90 - (py - y) / h * 180
            if any(point_in_polygon(lon, lat, c) for c in CONTINENTS):
                draw.ellipse([px, py, px + 2, py + 2], fill=(70, 110, 140))
    small = fonts["sans_b_map"]
    for text, lon, lat in MAP_LABELS:
        lx = x + int((lon + 180) / 360 * w)
        ly = y + int((90 - lat) / 180 * h)
        tw = draw.textlength(text, font=small)
        draw.text((lx - tw / 2, ly - 5), text, font=small, fill=(70, 90, 110))
    num_font = fonts["sans_b"]
    for s in STORIES:
        tx = x + int((s["lon"] + 180) / 360 * w)
        ty = y + int((90 - s["lat"]) / 180 * h)
        px, py = tx + s.get("dx", 0), ty + s.get("dy", 0)
        if (px, py) != (tx, ty):
            draw.line([tx, ty, px, py], fill=RED, width=1)
            draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
        r = 9
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=2)
        t = str(s["n"])
        tw = draw.textlength(t, font=num_font)
        draw.text((px - tw / 2, py - 6), t, font=num_font, fill=(255, 255, 255))
    draw.text((x + 8, y + h - 18), "Pins 1\u201313 mark the illustrated stories above.",
              font=fonts["sans"], fill=MUTED)


# ---------------------------------------------------------------- page

def render(fonts):
    from PIL import Image, ImageDraw, ImageFont

    def F(name, size):
        return ImageFont.truetype(fonts[name], size)

    f = {
        "mast": F("DejaVuSerif-Bold.ttf", 52),
        "serif_b": F("DejaVuSerif-Bold.ttf", 20),
        "serif_b_sm": F("DejaVuSerif-Bold.ttf", 15),
        "serif_b_xs": F("DejaVuSerif-Bold.ttf", 12),
        "serif_i": F("DejaVuSerif.ttf", 15),
        "serif_i_sm": F("DejaVuSerif.ttf", 13),
        "sans_b_map": F("DejaVuSans-Bold.ttf", 8),
        "sans": F("DejaVuSans.ttf", 10),
        "sans_sm": F("DejaVuSans.ttf", 9),
        "sans_b": F("DejaVuSans-Bold.ttf", 10),
        "sans_b_sm": F("DejaVuSans-Bold.ttf", 8),
        "num": F("DejaVuSans-Bold.ttf", 18),
        "kick": F("DejaVuSans-Bold.ttf", 9),
    }
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24

    # Masthead
    d.line([M, 10, W - M, 10], fill=RULE, width=3)
    tw = d.textlength(TITLE, font=f["mast"])
    d.text(((W - tw) / 2, 14), TITLE, font=f["mast"], fill=INK)
    d.line([M, 76, W - M, 76], fill=RULE, width=2)
    d.text((M, 82), DATE_LINE, font=f["sans_b"], fill=INK)
    right = "45 STORIES  \u00b7  ONE PAGE  \u00b7  No. 323"
    d.text((W - M - d.textlength(right, font=f["sans_b"]), 82), right,
           font=f["sans_b"], fill=INK)
    d.line([M, 100, W - M, 100], fill=RULE, width=1)

    # One-line day summary
    d.rectangle([M, 108, W - M, 150], fill=TINT)
    d.text((M + 10, 114), "THE DAY IN ONE LINE", font=f["kick"], fill=RED)
    draw_wrapped(d, SUMMARY, f["serif_i_sm"], M + 10, 128, W - 2 * M - 20, 1)

    # BY THE NUMBERS strip
    y0, y1 = 158, 214
    d.rectangle([M, y0, W - M, y1], outline=RULE, width=1)
    d.text((M + 8, y0 + 4), "BY THE NUMBERS", font=f["kick"], fill=RED)
    cw = (W - 2 * M) / len(NUMBERS)
    for i, (val, lab) in enumerate(NUMBERS):
        cx = M + i * cw
        if i:
            d.line([cx, y0 + 18, cx, y1 - 4], fill=(200, 192, 172), width=1)
        vw = d.textlength(val, font=f["num"])
        d.text((cx + (cw - vw) / 2, y0 + 20), val, font=f["num"], fill=INK)
        lw = d.textlength(lab, font=f["sans_sm"])
        d.text((cx + (cw - lw) / 2, y0 + 44), lab, font=f["sans_sm"], fill=MUTED)

    # ---- stories 1-13 in three rows: 3 + 4 + 6
    def story_box(s, x, y, w, h, tier):
        d.rectangle([x, y, x + w, y + h], outline=(200, 192, 172), width=1)
        pad = 8
        if tier == 1:  # lead: illustration left, text right
            iw = 150
            illus(d, s["kind"], x + pad, y + pad, iw, h - 2 * pad, s["bg"])
            tx, tw = x + pad + iw + 10, w - pad * 2 - iw - 10
            d.text((tx, y + pad), f"{s['n']}  \u00b7  {s['kicker']}", font=f["kick"], fill=RED)
            end = draw_wrapped(d, s["headline"], f["serif_b"], tx, y + pad + 16, tw, 3, lh=24)
            draw_wrapped(d, s["deck"], f["sans"], tx, end + 6, tw, 3, lh=13)
        elif tier == 2:  # medium: illustration top strip, text below
            ih = 44
            illus(d, s["kind"], x + pad, y + pad, w - 2 * pad, ih, s["bg"])
            ty = y + pad + ih + 6
            d.text((x + pad, ty), f"{s['n']}  \u00b7  {s['kicker']}", font=f["kick"], fill=RED)
            end = draw_wrapped(d, s["headline"], f["serif_b_sm"], x + pad, ty + 14,
                               w - 2 * pad, 3, lh=17)
            draw_wrapped(d, s["deck"], f["sans_sm"], x + pad, end + 4,
                         w - 2 * pad, 2, lh=12)
        else:  # compact: thin illustration, short headline + deck
            ih = 34
            illus(d, s["kind"], x + pad, y + pad, w - 2 * pad, ih, s["bg"])
            ty = y + pad + ih + 5
            d.text((x + pad, ty), f"{s['n']}  \u00b7  {s['kicker']}", font=f["kick"], fill=RED)
            end = draw_wrapped(d, s["headline"], f["serif_b_xs"], x + pad, ty + 13,
                               w - 2 * pad, 3, lh=14)
            draw_wrapped(d, s["deck"], f["sans_sm"], x + pad, end + 3,
                         w - 2 * pad, 2, lh=11)

    gap = 8
    # Row A: stories 1-3
    yA, hA = 222, 146
    w1 = 470
    story_box(STORIES[0], M, yA, w1, hA, 1)
    w23 = (W - 2 * M - w1 - 2 * gap) // 2
    story_box(STORIES[1], M + w1 + gap, yA, w23, hA, 2)
    story_box(STORIES[2], M + w1 + gap + w23 + gap, yA, w23, hA, 2)
    # Row B: stories 4-7
    yB, hB = yA + hA + gap, 146
    wB = (W - 2 * M - 3 * gap) // 4
    for i, s in enumerate(STORIES[3:7]):
        story_box(s, M + i * (wB + gap), yB, wB, hB, 2)
    # Row C: stories 8-13
    yC, hC = yB + hB + gap, 140
    wC = (W - 2 * M - 5 * gap) // 6
    for i, s in enumerate(STORIES[7:13]):
        story_box(s, M + i * (wC + gap), yC, wC, hC, 3)

    # ---- bottom: dotted world map (left) + briefs 14-45 (right)
    yD = yC + hC + gap
    map_w, map_h = 470, 210
    d.text((M, yD), "THE WORLD ON ONE MAP", font=f["kick"], fill=RED)
    draw_map(d, f, M, yD + 16, map_w, map_h)
    draw_wrapped(d, "Dotted map: each dot is land. Pins mark where the 13 illustrated "
                    "stories happened; offset pins are joined to their true spot by a line.",
                 f["sans_sm"], M, yD + 16 + map_h + 6, map_w, 2, lh=12)
    bx = M + map_w + gap
    bw = W - M - bx
    d.text((bx, yD), "IN BRIEF  \u00b7  14\u201345", font=f["kick"], fill=RED)
    d.line([bx, yD + 14, W - M, yD + 14], fill=RULE, width=1)
    col_w = (bw - gap) // 2
    per_col = 16
    for i, (n, tag, text) in enumerate(BRIEFS):
        col = 0 if i < per_col else 1
        row = i % per_col
        x = bx + col * (col_w + gap)
        yy = yD + 22 + row * 18
        d.text((x, yy), f"{n}.", font=f["sans_b"], fill=RED)
        d.text((x + 22, yy), tag, font=f["sans_b_sm"], fill=INK)
        tw = d.textlength(tag, font=f["sans_b_sm"])
        draw_wrapped(d, text, f["sans_sm"], x + 26 + tw, yy, col_w - 26 - tw, 1)

    # Footer
    fy = H - 26
    d.line([M, fy, W - M, fy], fill=RULE, width=1)
    d.text((M, fy + 6),
           "Sources: Reuters \u00b7 CBS News \u00b7 Al Jazeera \u00b7 TechCrunch \u00b7 XTB \u00b7 UN \u00b7 NASA JPL \u2014 "
           "headlines as reported on 18 Nov 2026. Illustrations drawn in code.",
           font=f["sans_sm"], fill=MUTED)
    return img


def check_data():
    """Validate the story data without rendering."""
    assert TITLE and SUMMARY
    assert len(STORIES) == 13, len(STORIES)
    assert [s["n"] for s in STORIES] == list(range(1, 14))
    assert len(BRIEFS) == 32, len(BRIEFS)
    assert [b[0] for b in BRIEFS] == list(range(14, 46))
    assert len(NUMBERS) == 6
    for s in STORIES:
        assert s["headline"] and s["deck"] and s["kicker"]
        assert -90 <= s["lat"] <= 90 and -180 <= s["lon"] <= 180
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render THE DAY IN WORLD NEWS, 18 Nov 2026.")
    ap.add_argument("--output", default=here("output.png"))
    ap.add_argument("--check", action="store_true",
                    help="validate data and renderability only")
    args = ap.parse_args(argv)

    check_data()
    fonts = find_fonts()
    if args.check:
        print("data: 13 illustrated stories, 32 briefs, 6 numbers -- OK")
        print("pillow+fonts:", "OK" if fonts else "MISSING -- fallback copy will be used")
        return 0
    if fonts is None:
        src = here("entry.png")
        if not os.path.isfile(src):
            print("error: no Pillow/fonts and no bundled entry.png", file=sys.stderr)
            return 1
        shutil.copyfile(src, args.output)
        print(f"fallback: copied entry.png byte-for-byte -> {args.output}")
        return 0
    img = render(fonts)
    img.save(args.output, "PNG")
    print(f"rendered {img.size[0]}x{img.size[1]} -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
