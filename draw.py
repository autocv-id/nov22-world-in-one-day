#!/usr/bin/env python3
"""NI22 v3 — News Image 22 November 2026. Flat/drawn broadsheet, PIL only.

Build tool: renders entry.png (1024x1024). Never imported by main.py.
v3 = v1's EXACT style + format (user order 18:46 WIB, locked): same layout,
same type sizes/weights, same section positions, 27 stories. The ONLY changes
vs v1 are (a) fresh fact strings (COP31 plenary stalls, Kyiv 14 may be
trapped, HK final turnout 98.79%, press time) and (b) the two v2 defect fixes
(TANKERS/MECCA 2-line decks; map LABEL_DXDY + the ly-clamp bug fix).
All story strings live in the STORIES tables below so the string audit and
the tally audit can check them without parsing drawing code.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
CW = W - 2 * MARGIN  # 996 content width

CREAM = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
NAVY_DK = (20, 38, 64)
RED = (178, 35, 27)
RED_DK = (140, 28, 22)
GOLD = (154, 106, 31)
TEAL = (46, 110, 98)
PURPLE = (91, 74, 138)
CHARCOAL = (68, 68, 68)
SKY = (207, 227, 238)
SEA = (163, 198, 220)
LAND = (232, 220, 192)
LAND_LINE = (176, 158, 118)
WHITE = (255, 255, 255)
PAPER2 = (238, 231, 210)
GREY = (110, 110, 105)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# Regions: counted FROM the stories below, then written into the bar.
# Europe 6: M3 M4 M12 B23 B24 B26
# Mid East 10: M2 M9 M11 B14 B15 B18 B19 B20 B21 B27
# Asia 4: M7 M10 M13 B16
# Oceania 2: M6 B17
# Americas 2: M5 B22
# Global 3: M1 M8 B25
# Total 27.
REGIONS = [("EUROPE", 6, NAVY), ("MID EAST", 10, RED_DK), ("ASIA", 4, TEAL),
           ("OCEANIA", 2, PURPLE), ("AMERICAS", 2, GOLD), ("GLOBAL", 3, CHARCOAL)]

STRIP = [
    ("186", "drones in the overnight wave", "STORY 3"),
    ("720/9", "India's Test total, biggest away", "STORY 6"),
    ("98.79%", "Hong Kong final turnout, a record", "STORY 7"),
    ("723", "Hong Kong seats contested", "STORY 7"),
    ("1,300", "guests at the Pope's lunch", "STORY 12"),
    ("0", "fossil-fuel mentions in COP31 text", "STORY 1"),
]

# (num, banner, headline, deck, tag, source, scene_number, scene_label)
LARGES = [
    (1, "COP31 \u00b7 ANTALYA", "THE GAVEL WAITS",
     "Final text drops fossil fuels; plenary stalls in Antalya. "
     "No adoption yet at press time.",
     "CONFIRMED", "CarrZee \u00b7 The Curtain", "0", "FOSSIL-FUEL MENTIONS"),
    (2, "BAHRAIN \u00b7 IRAN WAR", "CENTCOM: NO F-16 LOST",
     "Bahrain takes Iran to the UN after a civilian site is hit. "
     "Iran claims 2 radars hit \u2014 unconfirmed.",
     "CONFIRMED + CLAIM", "CENTCOM \u00b7 Bahrain", "2", "RADARS CLAIMED"),
    (3, "UKRAINE \u00b7 KYIV", "186 DRONES OVERNIGHT",
     "Kyiv downs 161; flats hit in Vyshhorod, 14 may be trapped. "
     "Russia claims 170 downed.",
     "CONFIRMED", "Ukrainian Air Force", "186", "DRONES LAUNCHED"),
]

# (num, banner, headline, deck, tag, source, scene_number, scene_label)
MEDIUMS = [
    (4, "BALTIC", "SPARTA II STILL BURNING",
     "Fire crews fight on as Estonia warns of new strikes.",
     "CONFIRMED", "Reuters", "121M", "SHIP'S LENGTH"),
    (5, "F1", "VERSTAPPEN WINS VEGAS",
     "Norris 0.6s back; Piastri 3rd from 17th. Sat night = Sun 04:00 UTC.",
     "CONFIRMED", "F1 \u00b7 FIA", "35", "LEAD CHANGES"),
    (6, "CRICKET", "720/9: INDIA'S BIGGEST AWAY TOTAL",
     "NZ 119/2 at stumps, trail by 233.",
     "CONFIRMED", "ESPNcricinfo", "720/9", "DECLARED"),
    (7, "HONG KONG", "HONG KONG VOTES",
     "98.79% turnout, a record; 723 seats, 856 candidates.",
     "OFFICIAL", "Electoral Affairs Comm.", "98.79%", "RECORD TURNOUT"),
    (8, "SPACE", "BEPICOLOMBO ARRIVES",
     "Europe's probe enters Mercury orbit. Burn 18:24 GMT Sat = 01:24 WIB Sun.",
     "OFFICIAL", "ESA", "37 MIN", "ORBIT BURN"),
    (9, "HORMUZ", "TANKERS STILL BURNING",
     "3 hit near Khasab; convoy hasn't sailed. Fake \u2018line-breaker\u2019 signal.",
     "CONFIRMED", "Reuters \u00b7 UKMTO", "3", "TANKERS HIT"),
    (10, "SERANG", "SERANG FIRE: 36 MISSING",
     "3 dead at a candy factory; 6 body bags recovered.",
     "CONFIRMED", "Reuters \u00b7 Basarnas", "36", "MISSING"),
    (11, "MECCA", "MISSILE NEAR MECCA STOPPED",
     "Saudi defences stop Houthi strike. Early Sun Riyadh (Sat 22:42 UTC).",
     "REPORTED", "Anadolu", "1", "MISSILE"),
    (12, "VATICAN", "POPE'S LUNCH FOR 1,300",
     "Leo XIV shares a meal on World Day of the Poor.",
     "CONFIRMED", "Vatican News", "1,300", "GUESTS"),
    (13, "NEPAL", "NEPAL'S PM LANDS IN DELHI",
     "Balendra Shah's first trip abroad since taking office.",
     "CONFIRMED", "ANI", "34", "IN DELEGATION"),
]

# (num, text) — each brief is one item; wraps to at most 2 lines.
BRIEFS = [
    (14, "EISENKOT\u2013LIKUD TALKS BEGIN \u2014 coalition talks open; Likud sets terms. (AFP)"),
    (15, "IRAN POWER RATIONING BEGINS \u2014 ~2-hour cuts as gas supply lags. (RFE/RL)"),
    (16, "CHINA HITS BACK AT FCC \u2014 Beijing calls phone-number ban \u2018malicious\u2019. (Reuters)"),
    (17, "MARLES: CBO IS WRONG \u2014 AUKUS subs \u2018very much happening\u2019. (Reuters)"),
    (18, "HAMAS SEEKS URGENT MEDIATOR TALKS \u2014 after weekend violations. (Anadolu)"),
    (19, "GAZA: FRESH STRIKES KILL AT LEAST 2 \u2014 ceasefire violations mount. (Anadolu)"),
    (20, "LEBANON: STRIKES KILL AT LEAST 1 \u2014 7 hurt in the south. (Health Ministry)"),
    (21, "WEST BANK: PALESTINIAN SHOT DEAD \u2014 Ammar Hijazi, 34. (Health Ministry)"),
    (22, "NWSL: KC WIN 2-1 \u2014 first title. Sat night Washington = Sun 01:00 UTC."),
    (23, "ATP FINAL TONIGHT 17:00 UTC \u2014 Zverev v Alcaraz, Turin. Result not yet known."),
    (24, "LIVERPOOL v MAN UTD 16:30 UTC \u2014 Pochettino's debut. Result not yet known."),
    (25, "BITCOIN STEADIES NEAR $60K \u2014 range $57,794\u2013$60,996 in Sunday trading. (Finnhub)"),
    (26, "EU CONDEMNS GAZA VIOLATIONS \u2014 calls for full adherence to humanitarian law. (EU)"),
    (27, "GULF BOURSES RETREAT \u2014 Saudi \u22121.7%, Qatar \u22121.5%, Bahrain \u22120.4%. (Reuters)"),
]

TIMELINE = [
    ("SAT 18:24", "BepiColombo burn"),
    ("SAT 22:42", "Mecca missile down"),
    ("04:00", "F1 Las Vegas"),
    ("06:00", "161/186 down"),
    ("08:00", "COP31 plenary"),
    ("10:00", "HK polls close"),
]

DATE_CHECK = (
    "DATE CHECK \u2014 Left out: Kryvyi Rih strike (Fri 20) \u00b7 "
    "400-drone barrage (Thu night\u2013Fri) \u00b7 El Chapo Isidro capture (Fri) \u00b7 "
    "Bayelsa boat (Fri, 24 dead) \u00b7 Bolsonaro ICU (Sat 21) \u00b7 "
    "Gaza aid-van strike (Sat) \u00b7 Sparta II evacuation (Sat) \u00b7 "
    "148-drone wave (Fri\u2013Sat) \u00b7 EU\u2013Indonesia signing (Sat) \u00b7 "
    "Nvidia probe (Fri) \u00b7 Ladakh polls (Sat, 70.03%) \u00b7 "
    "Basra fire (Sat, 4 dead) \u00b7 Vulcan failure (Sun 15 Nov). "
    "Not yet: COP31 adoption \u00b7 ATP champion (final 17:00 UTC) \u00b7 "
    "Liverpool\u2013United result (16:30 UTC) \u00b7 Hong Kong final results."
)

HOW_TO_READ = (
    "HOW TO READ \u2014 At thumbnail size: the date, three leads, ten big stories. "
    "At full size: 14 briefs, the map, and the DATE CHECK."
)

LEGEND = (
    "CONFIRMED 2+ outlets \u00b7 OFFICIAL on the record \u00b7 REPORTED one outlet \u00b7 "
    "CLAIM one side's claim \u2014 Wires read to 12:18 UTC \u00b7 Original drawings."
)

# Map pins: (story num, lon, lat, label, pin_dx, pin_dy, label_side)
# Small nudges separate pins that sit within a few px of each other at this
# scale (Bahrain/Hormuz/Mecca; Rome/ESA-Ops; Kyiv/Finland). The map is
# schematic; nudges keep pins legible without moving them to another place.
PINS = [
    (1, 30.7, 36.9, "ANTALYA", 0, 0, "r"),
    (2, 50.6, 26.2, "", 0, -6, "l"),
    (3, 30.5, 50.7, "", 0, 0, "l"),
    (4, 27.0, 60.0, "FINLAND", 0, -4, "r"),
    (5, -115.1, 36.2, "LAS VEGAS", 0, 0, "r"),
    (6, 174.8, -41.3, "WELLINGTON", 0, 0, "l"),
    (7, 114.2, 22.3, "HONG KONG", 0, 0, "r"),
    (8, 8.7, 49.9, "", -6, -4, "l"),
    (9, 56.2, 26.2, "", 10, 8, "r"),
    (10, 106.1, -6.1, "SERANG", 0, 0, "r"),
    (11, 39.8, 21.4, "", 0, 6, "l"),
    (12, 12.5, 41.9, "", 0, 4, "r"),
    (13, 77.2, 28.6, "DELHI", 0, 0, "r"),
]

# Label-only offsets (dx, dy) from the pin centre, for labels whose default
# right-side slot collides with another pin's circle. Pins never move.
# (v2 map fix, carried into v3: pin 2 covered "ANTALYA" as "TALYA",
# pin 13 grazed "DELHI", pin 7 touched "HONG KONG".)
LABEL_DXDY = {
    1: (9, -13),    # ANTALYA — up-right of pin 1
    13: (8, -14),   # DELHI — up-right of pin 13
    7: (-30, 8),    # HONG KONG — below pin 7
}


# ---------------------------------------------------------------- helpers
def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(d, y, text, fnt, fill, cx=W // 2):
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def badge_number(d, x, y, w, h, number, label, num_size=32):
    """Big scene number on a dark badge, bottom-right of a scene box."""
    f_num = font(F_SANS_B, num_size)
    f_lab = font(F_SANS_B, 9)
    tw = max(d.textlength(number, font=f_num), d.textlength(label, font=f_lab))
    bw, bh = int(tw) + 16, num_size + 22
    bx, by = x + w - bw - 6, y + h - bh - 6
    d.rectangle([bx, by, bx + bw, by + bh], fill=(20, 20, 20))
    d.text((bx + 8, by + 2), number, font=f_num, fill=WHITE)
    d.text((bx + 8, by + num_size + 5), label, font=f_lab, fill=(255, 210, 90))


def badge_number_med(d, x, y, w, h, number):
    """Medium scene number: 30px bold white with a dark stroke, drawn
    straight onto the scene (no box — a box this wide collides with the
    banner in a 191px column). The card's headline/deck explain the number."""
    f_num = font(F_SANS_B, 30)
    tw = d.textlength(number, font=f_num)
    d.text((x + w - tw - 6, y + h - 36), number, font=f_num, fill=WHITE,
           stroke_width=2, stroke_fill=(20, 20, 20))


def banner(d, x, y, text, color=RED):
    f = font(F_SANS_B, 11)
    tw = d.textlength(text, font=f) + 12
    d.rectangle([x, y, x + tw, y + 17], fill=color)
    d.text((x + 6, y + 2), text, font=f, fill=WHITE)


# ---------------------------------------------------------------- scenes
def scene_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy, r = x + w // 2 - 30, y + h // 2, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180),
              outline=NAVY_DK, width=2)
    d.ellipse([cx - 18, cy - 20, cx + 2, cy - 2], fill=(110, 180, 110))
    d.ellipse([cx + 2, cy + 6, cx + 22, cy + 24], fill=(110, 180, 110))
    d.ellipse([cx - 8, cy + 10, cx + 10, cy + 26], fill=(110, 180, 110))
    # thermometer
    tx = x + w - 78
    d.rectangle([tx, y + 12, tx + 10, y + h - 22], fill=WHITE,
                outline=NAVY_DK)
    d.rectangle([tx + 2, y + 30, tx + 8, y + h - 24], fill=RED)
    d.ellipse([tx - 5, y + h - 26, tx + 15, y + h - 6], fill=RED)


def scene_night_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_DK)
    for sx, sy in [(20, 14), (70, 30), (140, 12), (210, 26), (260, 10),
                   (110, 44), (180, 48)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    for bx in (40, 150):
        d.rectangle([x + bx, y + h - 46, x + bx + 34, y + h - 8],
                    fill=(200, 205, 210))
        d.polygon([(x + bx + 4, y + h - 46), (x + bx + 30, y + h - 46),
                   (x + bx + 17, y + h - 62)], fill=(200, 205, 210))
        d.ellipse([x + bx + 12, y + h - 70, x + bx + 22, y + h - 60],
                  fill=(230, 230, 230))
    # jet silhouette
    jx, jy = x + w - 90, y + 16
    d.polygon([(jx, jy + 6), (jx + 34, jy), (jx + 60, jy + 6),
               (jx + 34, jy + 10)], fill=(160, 170, 180))


def scene_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 32, 48))
    for i, (dx, dy) in enumerate([(30, 18), (90, 30), (150, 14), (210, 34),
                                  (60, 52), (180, 56), (250, 18)]):
        d.ellipse([x + dx, y + dy, x + dx + 5, y + dy + 5], fill=(255, 220, 120))
        d.line([x + dx - 14, y + dy + 2, x + dx, y + dy + 2],
               fill=(255, 220, 120), width=1)
    # apartment block, top floors burning
    bx, bw = x + 24, 90
    d.rectangle([bx, y + h - 62, bx + bw, y + h - 6], fill=(150, 148, 140))
    for r in range(4):
        for c in range(4):
            d.rectangle([bx + 8 + c * 20, y + h - 56 + r * 13,
                         bx + 20 + c * 20, y + h - 48 + r * 13],
                        fill=(255, 230, 140) if (r + c) % 3 else (90, 90, 90))
    for fx in (bx + 10, bx + 40, bx + 66):
        d.polygon([(fx, y + h - 62), (fx + 8, y + h - 78), (fx + 16, y + h - 62)],
                  fill=(255, 140, 30))


def scene_ship(d, x, y, w, h, big=True):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    for wy in (h - 14, h - 24):
        d.arc([x + 10, y + wy, x + 60, y + wy + 12], 180, 360,
              fill=WHITE, width=2)
        d.arc([x + 120, y + wy, x + 170, y + wy + 12], 180, 360,
              fill=WHITE, width=2)
    d.rectangle([x + 16, y + h - 34, x + w - 16, y + h - 16],
                fill=(120, 30, 25))
    d.rectangle([x + 30, y + h - 52, x + w - 50, y + h - 34],
                fill=(40, 60, 90))
    d.rectangle([x + w - 48, y + h - 58, x + w - 20, y + h - 34],
                fill=(220, 220, 220))
    for fx in (x + 40, x + 80, x + 120):
        d.polygon([(fx, y + h - 52), (fx + 9, y + h - 74), (fx + 18, y + h - 52)],
                  fill=(255, 140, 30))
    d.ellipse([x + 60, y + 6, x + 84, y + 18], fill=(90, 90, 90))
    d.ellipse([x + 100, y + 2, x + 118, y + 14], fill=(90, 90, 90))


def scene_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 40))
    for i in range(12):
        c = WHITE if i % 2 == 0 else (20, 20, 20)
        d.rectangle([x + i * 16, y, x + i * 16 + 16, y + 12], fill=c)
    # car
    cx, cy = x + 30, y + h - 34
    d.rounded_rectangle([cx, cy, cx + 110, cy + 16], radius=6, fill=(200, 30, 30))
    d.rounded_rectangle([cx + 30, cy - 10, cx + 78, cy + 2], radius=5,
                        fill=(200, 30, 30))
    d.ellipse([cx + 12, cy + 10, cx + 34, cy + 26], fill=(15, 15, 15))
    d.ellipse([cx + 78, cy + 10, cx + 100, cy + 26], fill=(15, 15, 15))
    d.line([x + 8, y + h - 6, x + w - 8, y + h - 6], fill=GOLD, width=3)


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 100))
    d.ellipse([x + 20, y + h - 30, x + w - 20, y + h - 6], fill=(200, 185, 150))
    d.rectangle([x + 60, y + 12, x + 68, y + 44], fill=(210, 180, 130))
    d.rectangle([x + 74, y + 12, x + 82, y + 44], fill=(210, 180, 130))
    d.rectangle([x + 88, y + 12, x + 96, y + 44], fill=(210, 180, 130))
    d.ellipse([x + 120, y + 16, x + 134, y + 30], fill=(178, 35, 27))
    d.rectangle([x + 30, y + h - 44, x + 44, y + h - 14], fill=(190, 150, 100))


def scene_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 245))
    d.rectangle([x + 40, y + 22, x + 130, y + h - 10], fill=(43, 74, 127))
    d.rectangle([x + 58, y + 16, x + 112, y + 24], fill=(20, 38, 64))
    d.rectangle([x + 72, y - 2, x + 98, y + 18], fill=WHITE,
                outline=NAVY_DK)
    d.text((x + 62, y + 34), "\u2713", font=font(F_SANS_B, 28), fill=WHITE)


def scene_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 12, 24))
    for sx, sy in [(14, 10), (60, 22), (150, 12), (30, 44), (170, 40)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    mx, my, mr = x + w - 62, y + h // 2, 26
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(200, 140, 90))
    d.ellipse([mx - 12, my - 8, mx - 2, my + 2], fill=(170, 110, 70))
    d.ellipse([mx + 4, my + 8, mx + 14, my + 18], fill=(170, 110, 70))
    d.rectangle([x + 24, y + h // 2 - 8, x + 52, y + h // 2 + 8],
                fill=(180, 190, 200))
    d.rectangle([x + 8, y + h // 2 - 3, x + 24, y + h // 2 + 3],
                fill=(90, 120, 180))
    d.rectangle([x + 52, y + h // 2 - 3, x + 68, y + h // 2 + 3],
                fill=(90, 120, 180))


def scene_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.rectangle([x + 12, y + h - 30, x + w - 12, y + h - 14], fill=(30, 30, 30))
    d.rectangle([x + 26, y + h - 44, x + w - 40, y + h - 30], fill=(150, 40, 30))
    for fx in (x + 44, x + 96):
        d.polygon([(fx, y + h - 44), (fx + 9, y + h - 64), (fx + 18, y + h - 44)],
                  fill=(255, 140, 30))
    d.ellipse([x + 60, y + 8, x + 86, y + 20], fill=(90, 90, 90))


def scene_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 200))
    d.rectangle([x + 20, y + 26, x + w - 20, y + h - 8], fill=(150, 148, 140))
    for i in range(4):
        sx = x + 24 + i * 36
        d.polygon([(sx, y + 26), (sx + 18, y + 10), (sx + 36, y + 26)],
                  fill=(110, 110, 110))
    for fx in (x + 60, x + 110):
        d.polygon([(fx, y + 12), (fx + 8, y - 2), (fx + 16, y + 12)],
                  fill=(255, 140, 30))
    d.ellipse([x + 40, y + 2, x + 70, y + 14], fill=(90, 90, 90))
    d.ellipse([x + 110, y + 0, x + 140, y + 12], fill=(90, 90, 90))
    d.rectangle([x + 40, y + h - 26, x + 64, y + h - 8], fill=(60, 60, 60))


def scene_mosque(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 60))
    for sx, sy in [(16, 10), (70, 16), (140, 8), (110, 26)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    d.rectangle([x + 50, y + h - 34, x + 130, y + h - 6], fill=(200, 190, 160))
    d.pieslice([x + 70, y + h - 58, x + 110, y + h - 22], 180, 360,
               fill=(200, 190, 160))
    d.rectangle([x + 36, y + h - 52, x + 44, y + h - 6], fill=(200, 190, 160))
    d.rectangle([x + 136, y + h - 52, x + 144, y + h - 6], fill=(200, 190, 160))
    d.line([x + 150, y + 8, x + 110, y + 30], fill=(255, 220, 120), width=3)
    d.ellipse([x + 106, y + 26, x + 114, y + 34], fill=(255, 220, 120))


def scene_lunch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 230, 205))
    d.rectangle([x + 16, y + h - 30, x + w - 16, y + h - 18], fill=(160, 120, 70))
    for gx in (34, 70, 106, 142):
        d.ellipse([x + gx, y + h - 52, x + gx + 14, y + h - 38],
                  fill=(220, 180, 140))
        d.rectangle([x + gx + 1, y + h - 38, x + gx + 13, y + h - 30],
                    fill=(90, 120, 160))
    for px in (30, 66, 102, 138):
        d.ellipse([x + px, y + h - 34, x + px + 16, y + h - 28], fill=WHITE)


def scene_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 20, y + 10, x + 60, y + 24], fill=WHITE)
    d.ellipse([x + 120, y + 6, x + 160, y + 20], fill=WHITE)
    px, py = x + 40, y + 26
    d.polygon([(px, py + 8), (px + 50, py), (px + 100, py + 8),
               (px + 50, py + 14)], fill=(220, 220, 220))
    d.polygon([(px + 44, py - 6), (px + 56, py - 6), (px + 52, py + 8),
               (px + 48, py + 8)], fill=(180, 180, 180))
    d.rectangle([x + 30, y + h - 26, x + 66, y + h - 6], fill=(255, 153, 51))
    d.rectangle([x + 30, y + h - 19, x + 66, y + h - 12], fill=WHITE)
    d.rectangle([x + 30, y + h - 12, x + 66, y + h - 6], fill=(19, 136, 8))
    d.polygon([(x + 110, y + h - 26), (x + 146, y + h - 26),
               (x + 110, y + h - 6)], fill=(220, 20, 60))


SCENES_LARGE = {1: scene_globe, 2: scene_night_radar, 3: scene_drones}
SCENES_MED = {4: scene_ship, 5: scene_f1, 6: scene_cricket, 7: scene_ballot,
              8: scene_space, 9: scene_tanker, 10: scene_factory,
              11: scene_mosque, 12: scene_lunch, 13: scene_plane}


# ---------------------------------------------------------------- map
# Very rough continent blobs (equirectangular, lon -180..180, lat 75..-60).
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-110, 68), (-95, 69), (-80, 73), (-65, 62),
     (-55, 52), (-70, 42), (-80, 32), (-90, 21), (-97, 26), (-105, 23),
     (-110, 30), (-125, 40), (-125, 49), (-150, 60)],
    # South America
    [(-80, 9), (-60, 5), (-50, 0), (-35, -8), (-40, -22), (-48, -28),
     (-58, -38), (-65, -50), (-70, -54), (-73, -37), (-70, -20), (-77, -12),
     (-81, -4)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (46, 0), (40, -15), (35, -25), (28, -33), (18, -35),
     (15, -25), (12, -10), (9, 4), (-8, 4)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 53), (5, 58), (10, 60), (18, 56),
     (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (30, 50), (28, 45),
     (23, 40), (15, 40), (10, 44), (3, 43)],
    # Asia
    [(35, 36), (45, 40), (55, 37), (60, 25), (66, 25), (72, 20), (77, 8),
     (80, 15), (88, 22), (92, 16), (100, 7), (105, 10), (110, 20), (120, 25),
     (122, 32), (130, 42), (140, 45), (142, 55), (160, 60), (178, 65),
     (170, 70), (140, 72), (110, 74), (80, 73), (60, 69), (45, 68), (40, 55),
     (35, 45)],
    # SE Asia islands / Indonesia
    [(95, 5), (105, -5), (115, -8), (125, -9), (135, -8), (140, -3),
     (130, 0), (120, 2), (110, 1), (100, 0)],
    # Australia
    [(113, -22), (122, -14), (132, -12), (142, -11), (147, -19), (153, -27),
     (150, -37), (140, -38), (132, -32), (124, -33), (115, -33)],
    # New Zealand
    [(167, -46), (173, -41), (178, -38), (175, -40), (169, -47)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 220, 235),
                outline=NAVY_DK, width=1)
    lon0, lon1, lat0, lat1 = -180, 180, 75, -60

    def pt(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([pt(lo, la) for lo, la in poly], fill=LAND,
                  outline=LAND_LINE)
    f_pin = font(F_SANS_B, 10)
    f_lab = font(F_SANS_B, 8)
    for num, lon, lat, lab, pdx, pdy, side in PINS:
        px, py = pt(lon, lat)
        px, py = px + pdx, py + pdy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=WHITE, width=1)
        t = str(num)
        d.text((px - d.textlength(t, font=f_pin) / 2, py - 7), t,
               font=f_pin, fill=WHITE)
        # label on the pin's free side, clamped inside the map
        if not lab:
            continue
        lw = d.textlength(lab, font=f_lab)
        if num in LABEL_DXDY:
            # label-only offset: clears pin-on-label collisions without
            # moving any pin (v2 map fix, carried into v3).
            dx, dy = LABEL_DXDY[num]
            lx, ly = px + dx, py + dy
        elif side == "l":
            lx = px - 10 - lw
            ly = py - 5
        else:
            lx = px + 10
            ly = py - 5
        lx = min(max(lx, x + 2), x + w - lw - 2)
        ly = min(max(ly, y + 1), y + h - 10)
        d.text((lx, ly), lab, font=f_lab, fill=NAVY_DK)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- top bar
    d.rectangle([0, 0, W, 20], fill=NAVY_DK)
    f_top = font(F_SANS_B, 12)
    d.text((MARGIN, 3), "THE WORLD IN ONE DAY", font=f_top, fill=WHITE)
    rt = "PRESS TIME 12:18 UTC"
    d.text((W - MARGIN - d.textlength(rt, font=f_top), 3), rt, font=f_top,
           fill=(255, 210, 90))

    # --- masthead
    f_mast = font(F_SERIF, 58)
    draw_center(d, 24, "Sunday 22 November 2026", f_mast, NAVY_DK)
    d.line([MARGIN, 88, W - MARGIN, 88], fill=NAVY_DK, width=2)
    f_deck = font(F_SERIF_R, 15)
    draw_center(d, 92,
                "COP31 text drops fossil fuels  \u00b7  CENTCOM: no F-16 lost  "
                "\u00b7  Verstappen wins Vegas",
                f_deck, INK)
    f_kick = font(F_SANS_B, 13)
    draw_center(d, 112,
                "27 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED "
                "SUNDAY 22 NOVEMBER 2026",
                f_kick, RED)

    # --- number strip
    y0 = 134
    cell_w = CW // 6
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + 52], outline=NAVY_DK, width=1)
    f_num = font(F_SANS_B, 26)
    f_lab = font(F_SANS, 10)
    f_ref = font(F_SANS_B, 9)
    for i, (num, lab, ref) in enumerate(STRIP):
        cx = MARGIN + i * cell_w
        if i:
            d.line([cx, y0 + 4, cx, y0 + 48], fill=(200, 195, 175), width=1)
        d.text((cx + 8, y0 + 2), num, font=f_num, fill=NAVY)
        for j, ln in enumerate(wrap(d, lab, f_lab, cell_w - 14)):
            d.text((cx + 8, y0 + 30 + j * 12), ln, font=f_lab, fill=INK)
        rw = d.textlength(ref, font=f_ref)
        d.text((cx + cell_w - rw - 6, y0 + 4), ref, font=f_ref, fill=RED)

    # --- region bar
    y0 = 190
    total = sum(n for _, n, _ in REGIONS)
    x = MARGIN
    f_reg = font(F_SANS_B, 12)
    for i, (name, n, col) in enumerate(REGIONS):
        if i == len(REGIONS) - 1:
            wseg = W - MARGIN - x  # last segment takes the remainder
        else:
            wseg = int(CW * n / total)
        d.rectangle([x, y0, x + wseg - 1, y0 + 20], fill=col)
        t = "%s %d" % (name, n)
        d.text((x + (wseg - d.textlength(t, font=f_reg)) / 2, y0 + 3),
               t, font=f_reg, fill=WHITE)
        x += wseg

    # --- large mains
    y0 = 216
    gap = 12
    lw = (CW - 2 * gap) // 3
    scene_h = 78
    f_lh = font(F_SERIF, 20)
    f_ld = font(F_SANS, 13)
    f_tag = font(F_SANS_B, 10)
    for i, (num, banner_txt, head, deck, tag, src, snum, slab) in enumerate(LARGES):
        x = MARGIN + i * (lw + gap)
        SCENES_LARGE[num](d, x, y0, lw, scene_h)
        banner(d, x, y0 + 5, banner_txt)
        badge_number(d, x, y0, lw, scene_h, snum, slab, num_size=30)
        d.text((x, y0 + scene_h + 4), "%d" % num, font=font(F_SANS_B, 12),
               fill=RED)
        hy = y0 + scene_h + 4
        for j, ln in enumerate(wrap(d, head, f_lh, lw - 22)):
            d.text((x + 20, hy + j * 24), ln, font=f_lh, fill=INK)
        dy = hy + 24 * len(wrap(d, head, f_lh, lw - 22)) + 2
        for j, ln in enumerate(wrap(d, deck, f_ld, lw)):
            d.text((x, dy + j * 16), ln, font=f_ld, fill=INK)
        ty = dy + 16 * len(wrap(d, deck, f_ld, lw)) + 2
        d.text((x, ty), tag, font=f_tag, fill=RED)
        tw = d.textlength(tag, font=f_tag)
        d.text((x + tw + 8, ty), "\u00b7 " + src, font=font(F_SANS, 10),
               fill=GREY)

    # --- mediums, two rows of five
    y_top = 380
    mgap = 10
    mw = (CW - 4 * mgap) // 5
    mscene = 54
    mrow_h = 132
    f_mh = font(F_SANS_B, 14)
    f_md = font(F_SANS, 11)
    f_mt = font(F_SANS_B, 9)
    for row in range(2):
        for col in range(5):
            k = row * 5 + col
            num, banner_txt, head, deck, tag, src, snum, slab = MEDIUMS[k]
            x = MARGIN + col * (mw + mgap)
            y = y_top + row * mrow_h
            SCENES_MED[num](d, x, y, mw, mscene)
            banner(d, x, y + 3, banner_txt)
            badge_number_med(d, x, y, mw, mscene, snum)
            hy = y + mscene + 3
            hl = wrap(d, head, f_mh, mw)
            for j, ln in enumerate(hl[:3]):
                d.text((x, hy + j * 17), ln, font=f_mh, fill=INK)
            dy = hy + 17 * min(len(hl), 3) + 1
            dl = wrap(d, deck, f_md, mw)
            for j, ln in enumerate(dl[:3]):
                d.text((x, dy + j * 14), ln, font=f_md, fill=INK)
            ty = dy + 14 * min(len(dl), 3) + 1
            d.text((x, ty), tag, font=f_mt, fill=RED)
            tw = d.textlength(tag, font=f_mt)
            d.text((x + tw + 5, ty), src, font=font(F_SANS, 9), fill=GREY)

    # --- timeline strip
    y0 = 648
    d.rectangle([MARGIN, y0, W - MARGIN, y0 + 26], fill=NAVY_DK)
    f_tl = font(F_SANS_B, 10)
    f_tlb = font(F_SANS, 10)
    tl_w = d.textlength("BY THE CLOCK (UTC)", font=f_tl) + 12
    for t, ev in TIMELINE:
        tl_w += (d.textlength(t, font=f_tl) + 4
                 + d.textlength(ev, font=f_tlb) + 4 + 12)
    assert tl_w + 16 <= CW, "timeline overflows by %dpx" % (tl_w + 16 - CW)
    parts = []
    tx = MARGIN + 8
    d.text((tx, y0 + 6), "BY THE CLOCK (UTC)", font=f_tl, fill=(255, 210, 90))
    tx += d.textlength("BY THE CLOCK (UTC)", font=f_tl) + 12
    for t, ev in TIMELINE:
        d.text((tx, y0 + 6), t, font=f_tl, fill=WHITE)
        tx += d.textlength(t, font=f_tl) + 4
        d.text((tx, y0 + 6), ev, font=f_tlb, fill=(220, 225, 235))
        tx += d.textlength(ev, font=f_tlb) + 4
        d.text((tx, y0 + 6), "\u00b7", font=f_tlb, fill=(255, 210, 90))
        tx += 12

    # --- map + briefs band
    y0 = 682
    map_w = 300
    d.text((MARGIN, y0), "WHERE IT HAPPENED", font=font(F_SANS_B, 12),
           fill=NAVY_DK)
    draw_map(d, MARGIN, y0 + 18, map_w, 148)
    d.text((MARGIN, y0 + 170), "Red numbers mark stories 1\u201313 on the map.",
           font=font(F_SANS, 10), fill=GREY)
    # HOW TO READ box under the map
    hy = y0 + 190
    d.rectangle([MARGIN, hy, MARGIN + map_w, hy + 52], fill=PAPER2,
                outline=NAVY_DK, width=1)
    f_how = font(F_SANS, 11)
    for j, ln in enumerate(wrap(d, HOW_TO_READ, f_how, map_w - 14)):
        d.text((MARGIN + 7, hy + 4 + j * 14), ln, font=f_how, fill=INK)

    bx0 = MARGIN + map_w + 16
    bw = (W - MARGIN - bx0 - 12) // 2
    d.text((bx0, y0), "ALSO ON SUNDAY 22 NOVEMBER \u2014 14 MORE STORIES",
           font=font(F_SANS_B, 12), fill=NAVY_DK)
    f_br = font(F_SANS, 13)
    f_brn = font(F_SANS_B, 13)
    row_h = 33
    for i, (num, txt) in enumerate(BRIEFS):
        col, r = divmod(i, 7)
        x = bx0 + col * (bw + 12)
        y = y0 + 20 + r * row_h
        d.text((x, y), "%d" % num, font=f_brn, fill=RED)
        nw = d.textlength("%d " % num, font=f_brn) + 4
        bl = wrap(d, txt, f_br, bw - nw)
        assert len(bl) <= 2, "brief %d wraps to %d lines" % (num, len(bl))
        for j, ln in enumerate(bl[:2]):
            d.text((x + nw, y + j * 15), ln, font=f_br, fill=INK)

    # --- DATE CHECK
    y0 = 940
    f_dc = font(F_SANS_B, 11)
    lines = wrap(d, DATE_CHECK, f_dc, CW - 16)
    assert len(lines) <= 4, "DATE CHECK wraps to %d lines" % len(lines)
    d.rectangle([MARGIN, y0 - 4, W - MARGIN, y0 + 14 * len(lines) + 4],
                fill=(255, 235, 230), outline=RED, width=1)
    for j, ln in enumerate(lines):
        d.text((MARGIN + 8, y0 + j * 14), ln, font=f_dc, fill=INK)
    # --- colophon / legend
    f_leg = font(F_SANS, 10)
    assert d.textlength(LEGEND, font=f_leg) <= CW, "legend too long"
    draw_center(d, y0 + 14 * len(lines) + 8, LEGEND, f_leg, GREY)

    return img


def audits():
    """Tally + string audits; prints results, raises on failure."""
    total = sum(n for _, n, _ in REGIONS)
    n_stories = len(LARGES) + len(MEDIUMS) + len(BRIEFS)
    print("tally: regions sum=%d stories=%d (13 mains + %d briefs)"
          % (total, n_stories, len(BRIEFS)))
    assert total == n_stories == 27, "TALLY MISMATCH"
    assert len(PINS) == 13, "pin count"
    # every strip number appears in its main/medium
    all_main_text = " ".join(h + " " + dk for _, _, h, dk, _, _, _, _
                             in LARGES + MEDIUMS)
    for num, _, ref in STRIP:
        assert num in all_main_text or num in " ".join(
            s for _, _, _, _, _, _, s, _ in LARGES + MEDIUMS), \
            "strip number not cross-referenced: " + num
    print("strip cross-refs: all 6 numbers appear in mains/mediums")
    # cross-audit: DATE CHECK exclusions must not be carried as stories
    page = " ".join(h + " " + dk for _, _, h, dk, _, _, _, _
                    in LARGES + MEDIUMS)
    page += " " + " ".join(t for _, t in BRIEFS)
    forbidden = ["Kryvyi Rih", "El Chapo", "Bayelsa", "Bolsonaro",
                 "EU\u2013Indonesia", "Nvidia", "Ladakh", "Basra",
                 "Vulcan", "400-drone", "148-drone"]
    for f in forbidden:
        assert f not in page, "DATE CHECK story carried on page: " + f
    assert "16 crew" not in page and "crew safe" not in page, \
        "Sparta evacuation carried as Sunday news"
    assert "aid-van" not in page, "Gaza aid-van strike carried as Sunday news"
    print("cross-audit: no DATE CHECK story appears as a main/brief")
    # string audit: no other-day date refs outside DATE CHECK + dual labels
    bad = ["Fri 20", "Thu ", "Wed ", "15 Nov", "21 Nov", "20 Nov",
           "November 202", "December", "October", "January"]
    for b in bad:
        assert b not in page, "stray date reference in stories: " + b
    for b in ["Friday", "Thursday", "Wednesday"]:
        assert b not in page, "stray weekday in stories: " + b
    print("string audit: no non-22-Nov date refs in story strings")
    print("audits OK")


if __name__ == "__main__":
    audits()
    im = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    im.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
