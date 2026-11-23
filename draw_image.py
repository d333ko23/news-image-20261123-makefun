#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: a newspaper front page summing up
Monday, 23 November 2026 in 18 illustrated stories. Pure PIL, flat
procedural pictograms only -- no photographs, no real media logos.

Layout (1024x1024): masthead, two feature stories, then a 4x4 grid of
sixteen story cards, then a neutral footer line.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 20
PAPER = (253, 251, 244)
INK = (18, 18, 18)
MUTED = (96, 92, 82)
RED = (172, 32, 32)
RULE = (18, 18, 18)
CARD = (255, 255, 255)
CARD_LINE = (205, 200, 188)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap measured in pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, path, start, minimum, max_w, max_lines, leading):
    """Shrink the font until the text fits in max_lines; return (font, lines)."""
    size = start
    while size > minimum:
        fnt = font(path, size)
        lines = wrap(d, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, minimum)
    return fnt, wrap(d, text, fnt, max_w)


def draw_lines(d, lines, x, y, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ------------------------------------------------------------------ icons --
# Each icon draws inside a square of side `s` at (x, y). Flat pictograms.

def icon_chip(d, x, y, s, c):
    m = s * 0.14
    d.rounded_rectangle([x + m, y + m, x + s - m, y + s - m], radius=4, fill=c)
    d.rounded_rectangle([x + s * 0.32, y + s * 0.32, x + s * 0.68, y + s * 0.68],
                        radius=3, fill=PAPER)
    d.ellipse([x + s * 0.44, y + s * 0.44, x + s * 0.56, y + s * 0.56], fill=c)
    for i in range(3):
        t = 0.28 + i * 0.22
        d.rectangle([x + s * t, y + s * 0.02, x + s * (t + 0.08), y + m], fill=c)
        d.rectangle([x + s * t, y + s - m, x + s * (t + 0.08), y + s * 0.98], fill=c)
        d.rectangle([x + s * 0.02, y + s * t, x + m, y + s * (t + 0.08)], fill=c)
        d.rectangle([x + s - m, y + s * t, x + s * 0.98, y + s * (t + 0.08)], fill=c)


def icon_blockade(d, x, y, s, c):
    # warship silhouette above waves, with a no-entry ring
    d.polygon([(x + s * 0.10, y + s * 0.55), (x + s * 0.90, y + s * 0.55),
               (x + s * 0.78, y + s * 0.74), (x + s * 0.22, y + s * 0.74)], fill=c)
    d.rectangle([x + s * 0.30, y + s * 0.30, x + s * 0.55, y + s * 0.55], fill=c)
    d.line([x + s * 0.52, y + s * 0.16, x + s * 0.52, y + s * 0.30], fill=c, width=3)
    for wy in (0.82, 0.92):
        d.arc([x + s * 0.05, y + s * wy, x + s * 0.35, y + s * (wy + 0.12)],
              0, 180, fill=c, width=3)
        d.arc([x + s * 0.40, y + s * wy, x + s * 0.70, y + s * (wy + 0.12)],
              0, 180, fill=c, width=3)
        d.arc([x + s * 0.72, y + s * wy, x + s * 0.98, y + s * (wy + 0.12)],
              0, 180, fill=c, width=3)
    d.ellipse([x + s * 0.70, y + s * 0.04, x + s * 0.96, y + s * 0.30],
              outline=RED, width=3)
    d.line([x + s * 0.74, y + s * 0.26, x + s * 0.92, y + s * 0.08],
           fill=RED, width=3)


def icon_seadrone(d, x, y, s, c):
    d.polygon([(x + s * 0.30, y + s * 0.42), (x + s * 0.70, y + s * 0.42),
               (x + s * 0.58, y + s * 0.62), (x + s * 0.42, y + s * 0.62)], fill=c)
    d.ellipse([x + s * 0.46, y + s * 0.28, x + s * 0.54, y + s * 0.36], fill=c)
    d.line([x + s * 0.50, y + s * 0.36, x + s * 0.50, y + s * 0.42], fill=c, width=3)
    for wy in (0.72, 0.84):
        d.arc([x + s * 0.08, y + s * wy, x + s * 0.38, y + s * (wy + 0.12)],
              0, 180, fill=c, width=3)
        d.arc([x + s * 0.42, y + s * wy, x + s * 0.72, y + s * (wy + 0.12)],
              0, 180, fill=c, width=3)
        d.arc([x + s * 0.74, y + s * wy, x + s * 0.96, y + s * (wy + 0.12)],
              0, 180, fill=c, width=3)
    d.polygon([(x + s * 0.82, y + s * 0.10), (x + s * 0.90, y + s * 0.26),
               (x + s * 0.74, y + s * 0.26)], fill=RED)


def icon_stars(d, x, y, s, c):
    # circle of small stars (EU-style ring) around a bank
    cx, cy, r = x + s / 2, y + s / 2, s * 0.36
    for k in range(8):
        import math
        a = math.pi * 2 * k / 8 - math.pi / 2
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=c)
    d.rectangle([x + s * 0.30, y + s * 0.38, x + s * 0.70, y + s * 0.46], fill=c)
    for wx in (0.34, 0.47, 0.60):
        d.rectangle([x + s * wx, y + s * 0.50, x + s * (wx + 0.06), y + s * 0.72],
                    fill=c)
    d.rectangle([x + s * 0.28, y + s * 0.74, x + s * 0.72, y + s * 0.80], fill=c)


def icon_apartment(d, x, y, s, c):
    d.rectangle([x + s * 0.20, y + s * 0.14, x + s * 0.80, y + s * 0.86], fill=c)
    for wy in (0.26, 0.44, 0.62):
        for wx in (0.30, 0.50, 0.68):
            d.rectangle([x + s * wx, y + s * wy, x + s * (wx + 0.08),
                         y + s * (wy + 0.08)], fill=PAPER)
    d.polygon([(x + s * 0.62, y + s * 0.86), (x + s * 0.72, y + s * 0.55),
               (x + s * 0.82, y + s * 0.86)], fill=RED)
    d.polygon([(x + s * 0.78, y + s * 0.86), (x + s * 0.86, y + s * 0.64),
               (x + s * 0.94, y + s * 0.86)], fill=(255, 140, 0))


def icon_factory(d, x, y, s, c):
    d.rectangle([x + s * 0.14, y + s * 0.55, x + s * 0.86, y + s * 0.86], fill=c)
    d.rectangle([x + s * 0.16, y + s * 0.26, x + s * 0.30, y + s * 0.55], fill=c)
    d.polygon([(x + s * 0.40, y + s * 0.72), (x + s * 0.50, y + s * 0.44),
               (x + s * 0.60, y + s * 0.72)], fill=RED)
    d.polygon([(x + s * 0.58, y + s * 0.72), (x + s * 0.68, y + s * 0.52),
               (x + s * 0.78, y + s * 0.72)], fill=(255, 140, 0))
    d.ellipse([x + s * 0.70, y + s * 0.14, x + s * 0.82, y + s * 0.26], fill=(255, 200, 0))


def icon_pause_bomb(d, x, y, s, c):
    d.ellipse([x + s * 0.18, y + s * 0.42, x + s * 0.82, y + s * 0.88], fill=c)
    d.rectangle([x + s * 0.44, y + s * 0.30, x + s * 0.56, y + s * 0.44], fill=c)
    d.line([x + s * 0.56, y + s * 0.30, x + s * 0.70, y + s * 0.16], fill=c, width=3)
    d.rectangle([x + s * 0.38, y + s * 0.55, x + s * 0.46, y + s * 0.76],
                fill=PAPER)
    d.rectangle([x + s * 0.54, y + s * 0.55, x + s * 0.62, y + s * 0.76],
                fill=PAPER)


def icon_plane(d, x, y, s, c):
    d.polygon([(x + s * 0.50, y + s * 0.12), (x + s * 0.62, y + s * 0.50),
               (x + s * 0.50, y + s * 0.88), (x + s * 0.38, y + s * 0.50)], fill=c)
    d.polygon([(x + s * 0.30, y + s * 0.46), (x + s * 0.50, y + s * 0.56),
               (x + s * 0.50, y + s * 0.44)], fill=c)
    d.polygon([(x + s * 0.70, y + s * 0.46), (x + s * 0.50, y + s * 0.56),
               (x + s * 0.50, y + s * 0.44)], fill=c)
    d.line([x + s * 0.10, y + s * 0.90, x + s * 0.90, y + s * 0.90], fill=c, width=3)


def icon_hands(d, x, y, s, c):
    # two cupped hands holding a small house (aid / rebuild)
    d.arc([x + s * 0.10, y + s * 0.45, x + s * 0.90, y + s * 0.95], 0, 180,
          fill=c, width=4)
    d.polygon([(x + s * 0.36, y + s * 0.44), (x + s * 0.50, y + s * 0.28),
               (x + s * 0.64, y + s * 0.44)], fill=RED)
    d.rectangle([x + s * 0.39, y + s * 0.44, x + s * 0.61, y + s * 0.62], fill=c)
    d.rectangle([x + s * 0.47, y + s * 0.50, x + s * 0.53, y + s * 0.62], fill=PAPER)


def icon_shield(d, x, y, s, c):
    d.polygon([(x + s * 0.50, y + s * 0.08), (x + s * 0.84, y + s * 0.22),
               (x + s * 0.84, y + s * 0.55), (x + s * 0.50, y + s * 0.92),
               (x + s * 0.16, y + s * 0.55), (x + s * 0.16, y + s * 0.22)], fill=c)
    d.line([x + s * 0.34, y + s * 0.50, x + s * 0.46, y + s * 0.64,
            x + s * 0.68, y + s * 0.36], fill=PAPER, width=4)
    d.ellipse([x + s * 0.74, y + s * 0.06, x + s * 0.94, y + s * 0.26],
              fill=(255, 200, 0))


def icon_office(d, x, y, s, c):
    d.rectangle([x + s * 0.24, y + s * 0.22, x + s * 0.76, y + s * 0.86], fill=c)
    for wy in (0.34, 0.52, 0.70):
        for wx in (0.34, 0.50, 0.66):
            d.rectangle([x + s * wx, y + s * wy, x + s * (wx + 0.07),
                         y + s * (wy + 0.07)], fill=PAPER)
    d.rectangle([x + s * 0.12, y + s * 0.12, x + s * 0.30, y + s * 0.24],
                outline=RED, width=3)
    d.line([x + s * 0.15, y + s * 0.18, x + s * 0.27, y + s * 0.18],
           fill=RED, width=2)
    d.line([x + s * 0.21, y + s * 0.14, x + s * 0.21, y + s * 0.22],
           fill=RED, width=2)


def icon_ballot(d, x, y, s, c):
    d.rectangle([x + s * 0.18, y + s * 0.48, x + s * 0.82, y + s * 0.88], fill=c)
    d.rectangle([x + s * 0.14, y + s * 0.38, x + s * 0.86, y + s * 0.50], fill=c)
    d.rectangle([x + s * 0.44, y + s * 0.30, x + s * 0.56, y + s * 0.40], fill=c)
    d.polygon([(x + s * 0.30, y + s * 0.12), (x + s * 0.50, y + s * 0.36),
               (x + s * 0.72, y + s * 0.06)], fill=RED)


def icon_ball(d, x, y, s, c):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=3)
    d.polygon([(cx, cy - r * 0.35), (cx + r * 0.33, cy - r * 0.10),
               (cx + r * 0.20, cy + r * 0.30), (cx - r * 0.20, cy + r * 0.30),
               (cx - r * 0.33, cy - r * 0.10)], fill=c)
    d.line([cx, cy - r * 0.35, cx, cy - r], fill=c, width=2)
    d.line([cx + r * 0.33, cy - r * 0.10, cx + r * 0.94, cy - r * 0.28],
           fill=c, width=2)
    d.line([cx - r * 0.33, cy - r * 0.10, cx - r * 0.94, cy - r * 0.28],
           fill=c, width=2)


def icon_math(d, x, y, s, c):
    d.rectangle([x + s * 0.10, y + s * 0.14, x + s * 0.90, y + s * 0.86],
                outline=c, width=3)
    fnt = font(SANS_B, int(s * 0.42))
    d.text((x + s * 0.18, y + s * 0.22), "\u03c0", font=fnt, fill=c)
    d.text((x + s * 0.52, y + s * 0.22), "\u221a", font=fnt, fill=RED)
    d.line([x + s * 0.22, y + s * 0.70, x + s * 0.78, y + s * 0.70],
           fill=c, width=3)


def icon_budget(d, x, y, s, c):
    d.rectangle([x + s * 0.16, y + s * 0.24, x + s * 0.84, y + s * 0.80],
                outline=c, width=3)
    d.line([x + s * 0.24, y + s * 0.38, x + s * 0.76, y + s * 0.38],
           fill=c, width=2)
    fnt = font(SANS_B, int(s * 0.30))
    d.text((x + s * 0.24, y + s * 0.46), "\u20ac", font=fnt, fill=c)
    d.line([x + s * 0.18, y + s * 0.18, x + s * 0.82, y + s * 0.86],
           fill=RED, width=4)


def icon_ferry(d, x, y, s, c):
    d.rectangle([x + s * 0.16, y + s * 0.30, x + s * 0.84, y + s * 0.62], fill=c)
    for wx in (0.26, 0.44, 0.62):
        d.rectangle([x + s * wx, y + s * 0.38, x + s * (wx + 0.10),
                     y + s * 0.50], fill=PAPER)
    d.polygon([(x + s * 0.12, y + s * 0.62), (x + s * 0.88, y + s * 0.62),
               (x + s * 0.74, y + s * 0.78), (x + s * 0.26, y + s * 0.78)], fill=c)
    d.line([x + s * 0.10, y + s * 0.88, x + s * 0.90, y + s * 0.88],
           fill=c, width=3)


def icon_helmet(d, x, y, s, c):
    d.pieslice([x + s * 0.14, y + s * 0.18, x + s * 0.86, y + s * 0.86],
               180, 360, fill=c)
    d.rectangle([x + s * 0.10, y + s * 0.62, x + s * 0.90, y + s * 0.70], fill=c)
    d.ellipse([x + s * 0.44, y + s * 0.10, x + s * 0.56, y + s * 0.22], fill=RED)
    d.line([x + s * 0.20, y + s * 0.86, x + s * 0.34, y + s * 0.76,
            x + s * 0.46, y + s * 0.86], fill=c, width=3)
    d.line([x + s * 0.54, y + s * 0.86, x + s * 0.68, y + s * 0.76,
            x + s * 0.80, y + s * 0.86], fill=c, width=3)


def icon_chart_down(d, x, y, s, c):
    d.line([x + s * 0.12, y + s * 0.22, x + s * 0.38, y + s * 0.40,
            x + s * 0.58, y + s * 0.34, x + s * 0.88, y + s * 0.70], fill=RED,
           width=4)
    d.polygon([(x + s * 0.88, y + s * 0.70), (x + s * 0.72, y + s * 0.64),
               (x + s * 0.80, y + s * 0.84)], fill=RED)
    for bx, bh in ((0.16, 0.28), (0.38, 0.42), (0.60, 0.30)):
        d.rectangle([x + s * bx, y + s * (0.88 - bh), x + s * (bx + 0.12),
                     y + s * 0.88], outline=c, width=2)


def icon_arrow_up(d, x, y, s, c):
    d.line([x + s * 0.15, y + s * 0.75, x + s * 0.45, y + s * 0.45,
            x + s * 0.62, y + s * 0.55, x + s * 0.88, y + s * 0.20], fill=c,
           width=5)
    d.polygon([(x + s * 0.88, y + s * 0.20), (x + s * 0.70, y + s * 0.18),
               (x + s * 0.84, y + s * 0.38)], fill=c)
    for bx, bh in ((0.15, 0.25), (0.38, 0.38), (0.61, 0.28)):
        d.rectangle([x + s * bx, y + s * (0.90 - bh), x + s * (bx + 0.11),
                     y + s * 0.90], fill=c)


# ------------------------------------------------------------- the stories --
# Titles + summaries copied verbatim from the verified research file.
FEATURES = [
    ("TOP STORY · TECHNOLOGY", "HUANG IS BACK",
     "Nvidia reinstates Jensen Huang as CEO, 11 days after he resigned; "
     "shares jump about 33% and the S&P 500 rises 4.82%.",
     icon_chip, (34, 120, 70)),
    ("GULF CRISIS · MIDDLE EAST", "IRAN VOWS TO FIGHT BLOCKADE",
     "Iran says it will use \"all means\" against the US naval blockade; "
     "it says it shot down a US drone over the Gulf; Trump says strikes "
     "could resume after the New Year.",
     icon_blockade, (30, 90, 120)),
]

GRID = [
    ("UKRAINE SINKS MERKURY",
     "Zelenskyy says seven sea drones sank the Russian corvette Merkury "
     "at Benghazi; a Ka-27 helicopter aboard was destroyed; cargo ship "
     "MV Angara also hit.", icon_seadrone, (30, 90, 120)),
    ("EU'S 22ND SANCTIONS",
     "The Commission proposes a 22nd package: about 60 Russian banks off "
     "SWIFT, a crypto sanctions task force, 70+ shadow-fleet ships, a visa "
     "ban on ex-combatants.", icon_stars, (30, 60, 130)),
    ("DYMER TOLL NOW 11",
     "A Russian strike on an apartment block near Kyiv; the death toll "
     "rises to at least 11.", icon_apartment, (120, 60, 60)),
    ("FACTORY FIRE TOLL 24",
     "Fire at a candy factory in Cikande, Indonesia; 24 killed, dozens "
     "still missing.", icon_factory, (120, 60, 60)),
    ("TRUMP HALTS LEAD BLAST",
     "Trump orders the Army to pause detonation of a toxic lead azide "
     "stockpile in Iowa.", icon_pause_bomb, (90, 60, 60)),
    ("PUIGDEMONT FREE TO RETURN",
     "Spain's Supreme Court shelves the case; the Catalan ex-leader can "
     "return after nearly a decade in exile.", icon_plane, (30, 90, 120)),
    ("INDIA PLEDGES $1.62BN TO NEPAL",
     "Flood-rebuild aid after Modi meets PM Balendra Shah in New Delhi.",
     icon_hands, (34, 120, 70)),
    ("CROWDSTRIKE BUYS ZSCALER",
     "A $43.9bn all-stock deal, the biggest cybersecurity takeover on "
     "record.", icon_shield, (30, 90, 120)),
    ("PYONGYANG MULLS CLOSING SWISS OFFICE",
     "North Korea may shut Switzerland's diplomatic office after sanctions "
     "on a children's camp.", icon_office, (90, 60, 60)),
    ("M\u00c9LENCHON GAINS IN POLL",
     "French hard-left leader at 35% vs Le Pen's 65% in a runoff poll.",
     icon_ballot, (120, 60, 60)),
    ("UK TO HOST 2035 WOMEN'S WORLD CUP",
     "FIFA confirms the UK as 2035 hosts; a US-led bid takes 2031.",
     icon_ball, (34, 120, 70)),
    ("RIEMANN RIVAL PROOF",
     "A Stanford mathematician posts a rival human-written proof, "
     "challenging Anthropic's AI-assisted claim; neither is verified yet.",
     icon_math, (30, 90, 120)),
    ("EU BUDGET REJECTED",
     "Czech and Hungarian leaders reject the new EU budget proposal.",
     icon_budget, (120, 60, 60)),
    ("RUSSIA'S $576M FERRIES",
     "Russia to spend $576m on two rail ferries to supply Kaliningrad.",
     icon_ferry, (30, 90, 120)),
    ("US TO TRAIN SYRIAN TROOPS",
     "The US is discussing its first training mission with Syrian forces "
     "since 2024, in demining.", icon_helmet, (90, 60, 60)),
    ("BRAZIL'S REAL SLIDES",
     "The real falls through 6.00/$, down 17% since the election runoff "
     "a month ago.", icon_chart_down, (120, 60, 60)),
]


def tint(rgb):
    return (min(255, rgb[0] + 165), min(255, rgb[1] + 165),
            min(255, rgb[2] + 165))


def draw_feature(d, x, y, w, h, kicker, title, summary, icon_fn, colour):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=1)
    # illustration panel on the left
    iw = 150
    d.rectangle([x + 10, y + 10, x + 10 + iw, y + h - 10], fill=tint(colour))
    d.rectangle([x + 10, y + 10, x + 10 + iw, y + h - 10], outline=CARD_LINE)
    icon_fn(d, x + 10 + (iw - 110) / 2, y + (h - 110) / 2, 110, colour)
    tx = x + 10 + iw + 14
    tw = x + w - 12 - tx
    cy = y + 12
    kf = font(SANS_B, 13)
    d.text((tx, cy), kicker, font=kf, fill=RED)
    cy += 22
    tf, tlines = fit_lines(d, title, SERIF_B, 27, 22, tw, 2, 32)
    cy = draw_lines(d, tlines, tx, cy, tf, INK, 32)
    cy += 6
    sf, slines = fit_lines(d, summary, SANS, 15, 12, tw, 5, 19)
    draw_lines(d, slines, tx, cy, sf, (52, 52, 48), 19)
    print(f"FEATURE {title}: title {len(tlines)} lines, "
          f"summary {len(slines)} lines @ {sf.size}px")


def draw_card(d, x, y, w, h, title, summary, icon_fn, colour):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=1)
    pad = 9
    isz = 46
    d.rectangle([x + pad, y + pad, x + pad + isz, y + pad + isz],
                fill=tint(colour))
    d.rectangle([x + pad, y + pad, x + pad + isz, y + pad + isz],
                outline=CARD_LINE)
    icon_fn(d, x + pad + 3, y + pad + 3, isz - 6, colour)
    tx = x + pad + isz + 8
    tw = x + w - pad - tx
    tf, tlines = fit_lines(d, title, SANS_B, 15, 12, tw, 3, 18)
    ty = y + pad + 2
    draw_lines(d, tlines, tx, ty, tf, INK, 18)
    title_h = len(tlines) * 18
    sy = y + pad + max(isz, title_h) + 7
    sw = w - 2 * pad
    sf, slines = fit_lines(d, summary, SANS, 13, 11, sw, 5, 16)
    draw_lines(d, slines, x + pad, sy, sf, (52, 52, 48), 16)
    print(f"CARD {title[:28]:28s}: title {len(tlines)} lines @ {tf.size}px, "
          f"summary {len(slines)} lines @ {sf.size}px, bottom y={sy + len(slines) * 16} / {y + h}")
    if sy + len(slines) * 16 > y + h - 6:
        print(f"  !! OVERFLOW in card: {title}")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    title_f = font(SERIF_B, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 14), title, font=title_f, fill=INK)
    date_f = font(SANS, 22)
    date = "Monday, 23 November 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 84), date, font=date_f, fill=MUTED)
    d.rectangle([MARGIN, 120, W - MARGIN, 124], fill=RULE)
    d.rectangle([MARGIN, 128, W - MARGIN, 129], fill=RULE)

    # ---- features ----
    fy, fh = 140, 204
    fw = (W - 2 * MARGIN - 12) // 2
    for i, (kicker, title, summary, icon_fn, colour) in enumerate(FEATURES):
        draw_feature(d, MARGIN + i * (fw + 12), fy, fw, fh,
                     kicker, title, summary, icon_fn, colour)

    # ---- grid ----
    gy = fy + fh + 14
    gw = (W - 2 * MARGIN - 3 * 12) // 4
    gh = 148
    for i, (title, summary, icon_fn, colour) in enumerate(GRID):
        r, c = divmod(i, 4)
        draw_card(d, MARGIN + c * (gw + 12), gy + r * (gh + 10), gw, gh,
                  title, summary, icon_fn, colour)

    # ---- footer ----
    foot_f = font(SANS, 14)
    foot = "The world's news on Monday, 23 November 2026."
    fw_ = d.textlength(foot, font=foot_f)
    d.text(((W - fw_) / 2, gy + 4 * gh + 3 * 10 + 8), foot, font=foot_f,
           fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"saved {out}: {os.path.getsize(out)} bytes, {img.size}")


if __name__ == "__main__":
    main()
