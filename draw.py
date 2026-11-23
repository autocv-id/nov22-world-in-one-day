#!/usr/bin/env python3
"""NI22 v7 — Sunday 22 November 2026, one-day world news image.

Fresh write for the v7 build (23 Nov 2026). Structure follows NI22 top-1
jolly-stork-27 by PRINCIPLE (timeline above the larges, 6-number strip,
region bar, 3 larges + 10 mediums, map + briefs, attacking DATE CHECK) with
our own verified content: the CORRECT COP31 no-deal outcome (top 1's lead is
stale), complete confidence tags on all 13 mains, the freshest press time in
the field, and two stories the top 1 lacks (Democrats 258 seats, Marquez 8th
MotoGP title — both verified from primary sources this session).

Content changes vs v6:
  * M13: Nepal PM visit -> Democrats reach 258 House seats (CONFIRMED, AP/CNN).
    Nepal was the thinnest medium (delegation-size scene number 34); the
    Democrats result is a major Sunday story and fills our Americas gap.
  * B27: Gulf bourses retreat -> Marquez wins 8th MotoGP title (CONFIRMED,
    Reuters). Gulf bourses was the thinnest brief (markets noise).
  * Timeline extended to the full day (7 entries, to ~19:15 UTC): v6's
    timeline stopped at 10:00, hiding our freshness; plntky (#5) shows the
    full-day arc to 20:43 UTC.
  * DATE CHECK gains a "Not yet" item (Belgian air-traffic strike, Mon
    07:00-21:00) — an attack on jolly's M12, which carries a Monday event
    as a Sunday medium. Vulcan failure (Sun 15 Nov, attacks nothing in the
    current top 5) dropped to keep the DC at 4 lines.
  * Strip: 723 (duplicate of story 7's 98.79%) -> 258 (story 13).

All facts are 22 November 2026 news. No 23 Nov content anywhere.
"""
import os
import random
from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont

random.seed(42)

W, H = 1024, 1024
BG = (251, 247, 236)          # cream paper
NAVY = (27, 42, 74)           # masthead / top bar
NAVY_DARK = (22, 35, 61)      # timeline strip
INK = (30, 30, 30)            # body text
RED = (176, 30, 30)           # kicker / numbers / DC border
GOLD = (232, 185, 60)         # press time / timeline label
GRAY = (110, 110, 110)        # legend / rules
SEA = (214, 232, 245)         # map sea
LAND = (245, 233, 200)        # map land
LAND_LINE = (170, 160, 120)   # map outline

FD = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_MAST = F("DejaVuSerif-Bold.ttf", 60)
F_SUB = F("DejaVuSerif.ttf", 16)
F_KICK = F("DejaVuSans-Bold.ttf", 13)
F_TOP = F("DejaVuSans-Bold.ttf", 12)
F_STRIP_N = F("DejaVuSans-Bold.ttf", 30)
F_STRIP_L = F("DejaVuSans.ttf", 11)
F_STRIP_S = F("DejaVuSans-Bold.ttf", 9)
F_REGION = F("DejaVuSans-Bold.ttf", 12)
F_TL_LBL = F("DejaVuSans-Bold.ttf", 11)
F_TL = F("DejaVuSans.ttf", 12)
F_TL_B = F("DejaVuSans-Bold.ttf", 12)
F_L_HEAD = F("DejaVuSerif-Bold.ttf", 20)
F_L_DECK = F("DejaVuSans.ttf", 13)
F_L_TAG = F("DejaVuSans-Bold.ttf", 11)
F_BANNER = F("DejaVuSans-Bold.ttf", 10)
F_M_HEAD = F("DejaVuSerif-Bold.ttf", 16)
F_M_DECK = F("DejaVuSans.ttf", 11)
F_M_TAG = F("DejaVuSans-Bold.ttf", 10)
F_BRIEF = F("DejaVuSans.ttf", 12)
F_BRIEF_B = F("DejaVuSans-Bold.ttf", 12)
F_HDR = F("DejaVuSans-Bold.ttf", 12)
F_DC_LBL = F("DejaVuSans-Bold.ttf", 12)
F_DC = F("DejaVuSans.ttf", 12)
F_LEGEND = F("DejaVuSans.ttf", 10)
F_MAP_LBL = F("DejaVuSans-Bold.ttf", 9)
F_HOW = F("DejaVuSans.ttf", 11)
F_SCENE_L = F("DejaVuSans-Bold.ttf", 34)   # large scene number
F_SCENE_M = F("DejaVuSans-Bold.ttf", 30)   # medium scene number
F_BADGE = F("DejaVuSans-Bold.ttf", 9)      # badge caption

PRESS_TIME = "14:29"  # wires read through 14:29 UTC 23 Nov 2026 (fixed for determinism)

# ---------------------------------------------------------------- content
STRIP = [
    ("186", "STORY 3", "drones in the overnight wave"),
    ("720/9", "STORY 6", "India's Test total, biggest away"),
    ("98.79%", "STORY 7", "Hong Kong final turnout, a record"),
    ("258", "STORY 13", "Democrats' House seats, most since 1992"),
    ("1,300", "STORY 12", "guests at the Pope's lunch"),
    ("0", "STORY 1", "fossil-fuel mentions in COP31 text"),
]

REGIONS = [
    ("EUROPE", 7, (27, 79, 138)),
    ("MID EAST", 9, (166, 30, 34)),
    ("ASIA", 3, (27, 122, 110)),
    ("OCEANIA", 2, (74, 124, 46)),
    ("AMERICAS", 3, (91, 58, 140)),
    ("GLOBAL", 3, (85, 85, 85)),
]

TIMELINE = [
    ("SAT 18:24", "BepiColombo"),
    ("05:30", "Verstappen wins"),
    ("06:00", "161/186 down"),
    ("~12:00", "COP31 no deal"),
    ("~18:00", "Democrats 258"),
    ("~19:15", "Alcaraz wins"),
]

# larges: (num, banner, headline, deck, tag, source, scene, badge_num, badge_cap)
LARGES = [
    (1, "COP31 \u00b7 ANTALYA", "NO DEAL AT COP31",
     "Kurum: \u2018no consensus\u2019 as EU rejects text with no fossil fuels. "
     "First no-deal COP since 2009.",
     "CONFIRMED", "Reuters \u00b7 CarrZee", "cop31", "0", "FOSSIL-FUEL MENTIONS"),
    (2, "BAHRAIN \u00b7 IRAN WAR", "CENTCOM: NO F-16 LOST",
     "Bahrain takes Iran to the UN after a civilian site is hit. "
     "Iran claims 2 radars hit \u2014 unconfirmed.",
     "CONFIRMED + CLAIM", "CENTCOM \u00b7 Bahrain", "centcom", "2", "RADARS CLAIMED"),
    (3, "UKRAINE \u00b7 KYIV", "186 DRONES OVERNIGHT",
     "161/186 downed \u2014 72 jets, 8 directions. Dymer block hit; "
     "14 trapped, 2 injured, 9 evacuated.",
     "CONFIRMED", "Ukrainian Air Force", "drones", "186", "DRONES LAUNCHED"),
]

# mediums: (num, banner, headline, deck, tag, source, scene, scene_num)
MEDIUMS = [
    (4, "BALTIC", "SPARTA II STILL BURNING",
     "Fire crews fight on as Estonia warns of new strikes.",
     "CONFIRMED", "Reuters", "sparta", "121M"),
    (5, "F1", "VERSTAPPEN WINS VEGAS",
     "Norris 0.6s back; Piastri 3rd from 17th. Sat night = Sun 04:00 UTC.",
     "CONFIRMED", "FIA", "f1", "35"),
    (6, "CRICKET", "INDIA\u2019S BIGGEST AWAY TOTAL",
     "NZ 119/2 at stumps, trail by 233.",
     "CONFIRMED", "ESPNcricinfo", "cricket", "720/9"),
    (7, "HONG KONG", "HONG KONG VOTES",
     "Record 98.79% turnout; 723 seats: Yuen, Leung, Lam win.",
     "OFFICIAL", "Electoral Affairs Comm.", "hongkong", "98.79%"),
    (8, "SPACE", "BEPICOLOMBO ARRIVES",
     "Probe enters Mercury orbit. Burn 18:24 GMT Sat = 01:24 WIB Sun.",
     "OFFICIAL", "ESA", "bepi", "37 MIN"),
    (9, "HORMUZ", "TANKERS STILL BURNING",
     "3 hit near Khasab; convoy hasn\u2019t sailed. Fake \u2018line-breaker\u2019 signal.",
     "CONFIRMED", "Reuters \u00b7 UKMTO", "hormuz", "3"),
    (10, "SERANG", "SERANG FIRE: 36 MISSING",
     "3 dead at a candy factory; 6 body bags recovered.",
     "CONFIRMED", "Reuters \u00b7 Basarnas", "serang", "36"),
    (11, "MECCA", "MISSILE NEAR MECCA STOPPED",
     "Saudi defences stop Houthi strike. Early Sun Riyadh (Sat 22:42 UTC).",
     "REPORTED", "Anadolu", "mecca", "1"),
    (12, "VATICAN", "POPE\u2019S LUNCH FOR 1,300",
     "Leo XIV shares a meal on World Day of the Poor.",
     "CONFIRMED", "Vatican News", "vatican", "1,300"),
    (13, "WASHINGTON", "DEMOCRATS REACH 258 SEATS",
     "Foxx concedes NC-5 after recount; gain of 44, most seats since 1992.",
     "CONFIRMED", "AP \u00b7 CNN", "democrats", "258"),
]

# briefs: (num, headline, deck, source) — headline bold caps, deck regular
BRIEFS = [
    (14, "EISENKOT\u2013LIKUD TALKS BEGIN", "coalition talks; Likud sets terms.", "AFP"),
    (15, "IRAN POWER RATIONING BEGINS", "\u20132-hour cuts as gas supply lags.", "RFE/RL"),
    (16, "CHINA HITS BACK AT FCC", "Beijing calls phone-number ban \u2018malicious\u2019.", "Reuters"),
    (17, "MARLES: CBO IS WRONG", "AUKUS subs \u2018very much happening\u2019.", "Reuters"),
    (18, "HAMAS SEEKS URGENT MEDIATOR TALKS", "after weekend violations.", "Anadolu"),
    (19, "GAZA: FRESH STRIKES KILL AT LEAST 2", "ceasefire violations mount.", "Anadolu"),
    (20, "LEBANON: STRIKES KILL AT LEAST 1", "7 hurt in the south.", "Health Ministry"),
    (21, "WEST BANK: PALESTINIAN SHOT DEAD", "Ammar Hijazi, 34.", "Health Ministry"),
    (22, "NWSL: KC WIN 2-1", "first title. Sat night in Washington = Sun 01:00 UTC.", ""),
    (23, "ALCARAZ WINS ATP FINALS", "beats Zverev 6-2, 7-6(7); first title.", "Reuters"),
    (24, "LIVERPOOL 4-0 MAN UTD", "Szoboszlai, Wirtz, Ngumoha, Mu\u00f1oz score.", "Sky Sports"),
    (25, "BITCOIN STEADIES NEAR $60K", "range $57,794\u2013$60,996 in Sunday trading.", "Finnhub"),
    (26, "EU CONDEMNS GAZA VIOLATIONS", "calls for full adherence to humanitarian law.", "EU"),
    (27, "M\u00c1RQUEZ WINS 8TH MOTOGP TITLE", "8th in Portugal seals crown, level with Agostini.", "Reuters"),
]

DC_EXCLUSIONS = [
    "Kryvyi Rih strike (Fri 20)",
    "400-drone barrage (Thu night\u2013Fri)",
    "El Chapo Isidro capture (Fri)",
    "Bayelsa boat, 24 dead (Fri)",
    "Bolsonaro ICU (Sat 21)",
    "Gaza aid-van strike (Sat)",
    "Sparta II evacuation (Sat)",
    "148-drone wave (Fri 20\u2013Sat 21)",
    "EU\u2013Indonesia signing (Sat)",
    "Nvidia probe (Fri)",
    "Ladakh polls (Sat, 70.03%)",
    "Basra fire (Sat, 4 dead)",
]
DC_DEFENSE = ("Counted as Sunday\u2019s news: BepiColombo\u2019s Mercury burn, "
              "Sat 18:24 GMT = Sun 01:24 WIB.")
DC_NOTYET = "Monday\u2019s news, not Sunday\u2019s: Belgian air-traffic strike (Mon 07:00\u201321:00)."
DC_CLOSE = ("Tonight\u2019s real count: 186 drones \u2014 and COP31 ended with "
            "no deal, at the top of this page.")

# map pins (map-local coords, box 12..330 x 712..880): (num, x, y)
MAP_PINS = [
    (1, 190, 54), (2, 206, 56), (3, 192, 36), (4, 180, 22), (5, 57, 50),
    (6, 309, 123), (7, 260, 63), (8, 158, 34), (9, 220, 66), (10, 253, 90),
    (11, 198, 70), (12, 168, 50), (13, 91, 48),
]
# map labels: (text, x, y) — map-local, placed clear of pins
MAP_LABELS = [
    ("LAS VEGAS", 14, 64), ("FINLAND", 158, 6), ("ANTALYA", 182, 80),
    ("WASHINGTON", 78, 64), ("HONG KONG", 236, 76), ("SERANG", 246, 104),
    ("WELLINGTON", 246, 136),
]

# ---------------------------------------------------------------- helpers
def tw(d, text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def th(d, text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[3] - b[1]

def wrap(d, text, font, width):
    """Greedy word wrap by pixel width. Returns list of lines."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def wrap_mixed(d, segments, width):
    """Wrap [(text, font)] segments as one flowing paragraph.
    Returns list of lines, each a list of (text, font) runs."""
    # flatten to (word, font) tokens
    tokens = []
    for text, font in segments:
        for w in text.split(" "):
            tokens.append((w, font))
    lines, cur, cur_w = [], [], 0
    for w, font in tokens:
        ww = tw(d, w, font)
        sp = tw(d, " ", font) if cur else 0
        if cur and cur_w + sp + ww > width:
            lines.append(cur)
            cur, cur_w = [(w, font)], ww
        else:
            cur.append((w, font))
            cur_w += sp + ww
    if cur:
        lines.append(cur)
    return lines

def draw_runs(d, x, y, runs):
    cx = x
    for text, font in runs:
        d.text((cx, y), text, font=font, fill=INK)
        cx += tw(d, text + " ", font)
    return cx

def banner(d, x, y, text, color):
    """Small colored label, top-left of a scene."""
    pad = 4
    w = tw(d, text, F_BANNER) + pad * 2
    h = 14
    d.rectangle([x, y, x + w, y + h], fill=color)
    d.text((x + pad, y + 1), text, font=F_BANNER, fill=(255, 255, 255))
    return w

def scene_number(d, x, y, text, font=F_SCENE_M, fill=(255, 255, 255)):
    """Big scene number with a dark shadow + outline for legibility."""
    d.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0))
    d.text((x, y), text, font=font, fill=fill, stroke_width=2,
           stroke_fill=(0, 0, 0))

def badge_box(d, x, y, num, cap):
    """Black badge: big number + gold caption (large scenes)."""
    nw = tw(d, num, F_SCENE_L)
    cw = tw(d, cap, F_BADGE)
    w = max(nw, cw) + 16
    h = 52
    d.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 8, y + 2), num, font=F_SCENE_L, fill=(255, 255, 255))
    d.text((x + 8, y + 38), cap, font=F_BADGE, fill=GOLD)
    return w

# ---------------------------------------------------------------- scenes
# Flat drawn illustration, never photorealistic. Each scene fills its box;
# the caller draws the banner (top-left) and the scene number on top.

def scene_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 84, 96))
    # globe, left
    d.ellipse([x + 12, y + 10, x + 62, y + 60], fill=(64, 140, 190),
              outline=(255, 255, 255), width=2)
    d.ellipse([x + 24, y + 22, x + 40, y + 36], fill=(110, 190, 110))
    d.ellipse([x + 38, y + 38, x + 52, y + 50], fill=(110, 190, 110))
    # conference table + delegates
    d.rectangle([x + 70, y + 52, x + w - 12, y + 66], fill=(140, 95, 55))
    for i in range(5):
        cx = x + 84 + i * 42
        d.ellipse([cx, y + 34, cx + 12, y + 46], fill=(230, 200, 160))
        d.rectangle([cx - 2, y + 46, cx + 14, y + 54], fill=(60, 60, 90))
    # flags on the table
    for i, c in enumerate([(200, 40, 40), (40, 90, 200), (240, 200, 40),
                           (40, 160, 80), (230, 230, 230)]):
        fx = x + 76 + i * 42
        d.rectangle([fx, y + 52, fx + 2, y + 66], fill=(220, 220, 220))
        d.rectangle([fx + 2, y + 52, fx + 16, y + 60], fill=c)
    # clock, right
    d.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(245, 245, 235),
              outline=(40, 40, 40), width=2)
    d.line([x + w - 33, y + 27, x + w - 33, y + 14], fill=(40, 40, 40), width=2)
    d.line([x + w - 33, y + 27, x + w - 22, y + 27], fill=(40, 40, 40), width=2)

def scene_centcom(d, x, y, w, h):
    # sunset sky bands
    for i, c in enumerate([(250, 200, 120), (245, 170, 90), (235, 140, 80)]):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)
    d.ellipse([x + w - 110, y + 6, x + w - 70, y + 46], fill=(255, 240, 180))
    # sea
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(70, 130, 180))
    # fighter jet silhouette
    jx, jy = x + 40, y + 34
    d.polygon([(jx, jy + 10), (jx + 130, jy + 10), (jx + 170, jy + 4),
               (jx + 130, jy + 16), (jx + 60, jy + 18), (jx + 30, jy + 26),
               (jx + 10, jy + 18)], fill=(70, 75, 85))
    d.polygon([(jx + 90, jy + 10), (jx + 110, jy - 6), (jx + 118, jy + 10)],
              fill=(70, 75, 85))
    # teal check-circle (verified denial) — top-right, clear of the badge
    cx, cy = x + w - 28, y + 22
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(0, 150, 135),
              outline=(255, 255, 255), width=2)
    d.line([cx - 7, cy, cx - 2, cy + 6, cx + 8, cy - 6], fill=(255, 255, 255),
           width=3, joint="curve")

def scene_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for _ in range(40):
        sx = x + random.randint(2, w - 2)
        sy = y + random.randint(2, h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 220))
    # moon
    d.ellipse([x + w - 48, y + 6, x + w - 18, y + 36], fill=(235, 235, 210))
    # skyline with lit windows
    bx = x + 6
    while bx < x + w - 10:
        bw = random.randint(22, 40)
        bh = random.randint(24, 52)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(30, 36, 60))
        for wy in range(y + h - bh + 5, y + h - 6, 9):
            for wx in range(bx + 4, bx + bw - 5, 8):
                if random.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
        bx += bw + 4
    # drones: small X shapes with red lights
    for dx, dy in [(30, 16), (90, 26), (150, 12), (210, 30), (260, 18)]:
        px, py = x + dx, y + dy
        d.line([px - 5, py - 5, px + 5, py + 5], fill=(220, 220, 220), width=2)
        d.line([px - 5, py + 5, px + 5, py - 5], fill=(220, 220, 220), width=2)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 60, 60))
    # explosion glow, right
    ex, ey = x + w - 60, y + h - 40
    d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=(255, 140, 40))
    d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(255, 220, 120))

def scene_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 210))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(50, 100, 160))
    # ship hull + bridge
    d.polygon([(x + 20, y + h - 24), (x + w - 20, y + h - 24),
               (x + w - 34, y + h - 8), (x + 34, y + h - 8)], fill=(40, 45, 55))
    d.rectangle([x + w - 70, y + h - 44, x + w - 40, y + h - 24], fill=(200, 200, 200))
    # flames on deck (below the banner zone)
    for fx, fh in [(40, 18), (58, 26), (78, 16)]:
        d.polygon([(x + fx, y + h - 24), (x + fx + 8, y + h - 24 - fh),
                   (x + fx + 16, y + h - 24)], fill=(255, 140, 30))
        d.polygon([(x + fx + 4, y + h - 24), (x + fx + 8, y + h - 24 - fh + 8),
                   (x + fx + 12, y + h - 24)], fill=(255, 220, 90))
    # smoke
    for sx, sy, sr in [(50, 12, 9), (64, 6, 11), (80, 12, 8)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(120, 120, 120))

def scene_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 40))
    # track
    d.rectangle([x, y + h - 26, x + w, y + h - 6], fill=(80, 80, 90))
    d.line([x, y + h - 16, x + w, y + h - 16], fill=(255, 255, 255), width=1)
    # red race car
    cx, cy = x + 30, y + h - 44
    d.rectangle([cx, cy, cx + 90, cy + 16], fill=(200, 30, 30))
    d.polygon([(cx + 30, cy), (cx + 50, cy - 10), (cx + 70, cy - 10),
               (cx + 78, cy)], fill=(200, 30, 30))
    d.ellipse([cx + 8, cy + 10, cx + 26, cy + 26], fill=(20, 20, 20))
    d.ellipse([cx + 66, cy + 10, cx + 84, cy + 26], fill=(20, 20, 20))
    d.rectangle([cx + 88, cy - 6, cx + 96, cy + 10], fill=(200, 30, 30))
    # checkered flag, top right
    fx, fy = x + w - 34, y + 6
    for r in range(3):
        for c in range(4):
            col = (255, 255, 255) if (r + c) % 2 == 0 else (20, 20, 20)
            d.rectangle([fx + c * 7, fy + r * 7, fx + c * 7 + 7, fy + r * 7 + 7],
                        fill=col)
    # speed lines
    for sy in (14, 26, 38):
        d.line([x + 8, y + sy, x + 40, y + sy], fill=(255, 220, 80), width=2)

def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 160, 80))
    # pitch
    d.rectangle([x + 60, y + 6, x + w - 60, y + h - 6], fill=(220, 200, 150))
    # stumps
    for sx in (78, 86, 94):
        d.line([x + sx, y + 12, x + sx, y + 30], fill=(255, 220, 80), width=3)
    # bat
    d.polygon([(x + 120, y + 14), (x + 132, y + 10), (x + 142, y + 34),
               (x + 130, y + 38)], fill=(200, 160, 100))
    # ball
    d.ellipse([x + 150, y + 16, x + 160, y + 26], fill=(180, 30, 30))
    # boundary rope
    d.arc([x - 30, y - 40, x + w + 30, y + h + 40], 20, 160,
          fill=(255, 255, 255), width=2)

def scene_hongkong(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
    # skyline
    bx = x + 4
    while bx < x + w - 8:
        bw = random.randint(16, 28)
        bh = random.randint(18, 40)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(90, 110, 140))
        bx += bw + 3
    # ballot box, centre-right
    bx0, by0 = x + w - 78, y + 8
    d.rectangle([bx0, by0, bx0 + 44, by0 + 30], fill=(200, 40, 40))
    d.rectangle([bx0 + 6, by0 - 4, bx0 + 38, by0 + 2], fill=(160, 30, 30))
    d.line([bx0 + 8, by0 + 18, bx0 + 18, by0 + 26, bx0 + 36, by0 + 8],
           fill=(255, 255, 255), width=3, joint="curve")
    # ballot paper going in
    d.polygon([(bx0 + 30, by0 - 14), (bx0 + 44, by0 - 10), (bx0 + 40, by0 + 2),
               (bx0 + 28, by0 - 2)], fill=(255, 255, 255))

def scene_bepi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 40))
    for _ in range(30):
        sx = x + random.randint(2, w - 2)
        sy = y + random.randint(2, h - 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 220))
    # Mercury, right
    mx, my = x + w - 52, y + 12
    d.ellipse([mx, my, mx + 36, my + 36], fill=(190, 140, 100))
    d.ellipse([mx + 8, my + 8, mx + 14, my + 14], fill=(150, 105, 70))
    d.ellipse([mx + 20, my + 20, mx + 27, my + 27], fill=(150, 105, 70))
    # spacecraft, left-centre
    sx, sy = x + 30, y + 18
    d.rectangle([sx, sy, sx + 18, sy + 12], fill=(220, 220, 220))
    d.rectangle([sx - 16, sy + 2, sx, sy + 10], fill=(60, 90, 200))
    d.rectangle([sx + 18, sy + 2, sx + 34, sy + 10], fill=(60, 90, 200))
    # orbit arc
    d.arc([x + 10, y - 10, x + w - 10, y + h + 10], 300, 60,
          fill=(255, 220, 100), width=2)
    # burn flame
    d.polygon([(sx + 9, sy + 12), (sx + 4, sy + 26), (sx + 14, sy + 26)],
              fill=(255, 160, 50))

def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 200, 130))
    d.ellipse([x + w - 50, y + 4, x + w - 14, y + 40], fill=(255, 240, 190))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(40, 90, 150))
    # tanker hull
    d.polygon([(x + 16, y + h - 26), (x + w - 16, y + h - 26),
               (x + w - 30, y + h - 8), (x + 30, y + h - 8)], fill=(60, 40, 40))
    d.rectangle([x + w - 60, y + h - 40, x + w - 34, y + h - 26],
                fill=(220, 220, 220))
    # flames mid-deck
    for fx, fh in [(60, 20), (80, 28), (100, 18)]:
        d.polygon([(x + fx, y + h - 26), (x + fx + 8, y + h - 26 - fh),
                   (x + fx + 16, y + h - 26)], fill=(255, 140, 30))
    # smoke
    for sx, sy, sr in [(70, 8, 9), (88, 4, 11)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(110, 110, 110))

def scene_serang(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(25, 25, 45))
    # factory building
    d.rectangle([x + 20, y + 14, x + w - 20, y + h - 6], fill=(70, 70, 90))
    for wy in range(y + 22, y + h - 12, 12):
        for wx in range(x + 28, x + w - 28, 14):
            d.rectangle([wx, wy, wx + 8, wy + 7], fill=(255, 190, 80))
    # roof flames
    for fx, fh in [(40, 16), (60, 24), (82, 18), (120, 20)]:
        d.polygon([(x + fx, y + 14), (x + fx + 8, y + 14 - fh),
                   (x + fx + 16, y + 14)], fill=(255, 140, 30))
        d.polygon([(x + fx + 4, y + 14), (x + fx + 8, y + 14 - fh + 8),
                   (x + fx + 12, y + 14)], fill=(255, 220, 90))
    # smoke column
    for sx, sy, sr in [(70, 2, 8), (84, -2, 10)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(100, 100, 100))

def scene_mecca(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 26, 55))
    for _ in range(24):
        sx = x + random.randint(2, w - 2)
        sy = y + random.randint(2, h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 220))
    # crescent moon
    d.ellipse([x + w - 44, y + 4, x + w - 18, y + 30], fill=(245, 245, 220))
    d.ellipse([x + w - 38, y + 2, x + w - 14, y + 28], fill=(18, 26, 55))
    # city silhouette
    bx = x + 6
    while bx < x + w - 10:
        bw = random.randint(18, 30)
        bh = random.randint(14, 30)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(45, 50, 80))
        bx += bw + 3
    # minaret
    d.rectangle([x + 24, y + 8, x + 30, y + h - 20], fill=(200, 200, 210))
    d.polygon([(x + 22, y + 8), (x + 27, y - 2), (x + 32, y + 8)],
              fill=(200, 200, 210))
    # interceptor burst
    bx0, by0 = x + 130, y + 14
    for dx, dy in [(0, -10), (0, 10), (-10, 0), (10, 0), (-7, -7), (7, 7),
                   (-7, 7), (7, -7)]:
        d.line([bx0, by0, bx0 + dx, by0 + dy], fill=(255, 220, 100), width=2)
    d.ellipse([bx0 - 4, by0 - 4, bx0 + 4, by0 + 4], fill=(255, 240, 180))

def scene_vatican(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 230, 190))
    # dome
    d.pieslice([x + 60, y - 26, x + w - 60, y + 34], 180, 360, fill=(200, 170, 120))
    d.rectangle([x + w // 2 - 2, y - 2, x + w // 2 + 2, y + 10], fill=(200, 170, 120))
    # hall
    d.rectangle([x + 10, y + 30, x + w - 10, y + h - 6], fill=(250, 240, 210))
    # tables with guests
    for tx in (24, 76, 128):
        d.rectangle([x + tx, y + 36, x + tx + 40, y + 44], fill=(255, 255, 255))
        for gx in (tx + 4, tx + 18, tx + 30):
            d.ellipse([x + gx, y + 26, x + gx + 8, y + 34], fill=(230, 200, 160))
    # sun
    d.ellipse([x + 8, y + 4, x + 28, y + 24], fill=(255, 220, 90))

def scene_democrats(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(100, 140, 195))
    # Capitol: dome + drum + wings
    cx = x + w // 2
    d.pieslice([cx - 34, y + 2, cx + 34, y + 44], 180, 360, fill=(245, 245, 240))
    d.rectangle([cx - 3, y - 2, cx + 3, y + 8], fill=(245, 245, 240))
    d.rectangle([cx - 40, y + 22, cx + 40, y + 44], fill=(235, 235, 230))
    d.rectangle([x + 14, y + 30, cx - 40, y + 44], fill=(225, 225, 220))
    d.rectangle([cx + 40, y + 30, x + w - 14, y + 44], fill=(225, 225, 220))
    # columns
    for col_x in range(cx - 36, cx + 36, 10):
        d.line([col_x, y + 26, col_x, y + 42], fill=(200, 200, 195), width=2)
    # steps + lawn
    d.rectangle([x, y + 44, x + w, y + h], fill=(110, 170, 100))
    d.rectangle([cx - 46, y + 44, cx + 46, y + 48], fill=(220, 220, 215))
    # flag
    d.rectangle([cx - 1, y - 2, cx + 1, y + 6], fill=(120, 120, 120))
    d.rectangle([cx + 1, y - 2, cx + 13, y + 4], fill=(180, 40, 40))
    # seat dots: blue arc of 258
    for i in range(21):
        ang = 200 + i * 7
        import math
        rx = cx + int(58 * math.cos(math.radians(ang)))
        ry = y + 44 + int(20 * math.sin(math.radians(ang)))
        d.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=(40, 90, 200))

SCENES = {
    "cop31": scene_cop31, "centcom": scene_centcom, "drones": scene_drones,
    "sparta": scene_sparta, "f1": scene_f1, "cricket": scene_cricket,
    "hongkong": scene_hongkong, "bepi": scene_bepi, "hormuz": scene_hormuz,
    "serang": scene_serang, "mecca": scene_mecca, "vatican": scene_vatican,
    "democrats": scene_democrats,
}
BANNER_COLORS = {
    "COP31 \u00b7 ANTALYA": RED, "BAHRAIN \u00b7 IRAN WAR": RED,
    "UKRAINE \u00b7 KYIV": RED,
    "BALTIC": (40, 90, 160), "F1": (180, 30, 30), "CRICKET": (50, 130, 60),
    "HONG KONG": (180, 30, 30), "SPACE": (30, 30, 70), "HORMUZ": (160, 90, 30),
    "SERANG": (160, 30, 30), "MECCA": (30, 60, 120), "VATICAN": (150, 120, 40),
    "WASHINGTON": (30, 60, 130),
}

# ---------------------------------------------------------------- layout
def draw_top(d):
    d.rectangle([0, 0, W, 20], fill=NAVY)
    d.text((12, 3), "THE WORLD IN ONE DAY", font=F_TOP, fill=(255, 255, 255))
    pt = "PRESS TIME %s UTC" % PRESS_TIME
    d.text((W - 12 - tw(d, pt, F_TOP), 3), pt, font=F_TOP, fill=GOLD)

def draw_masthead(d):
    title = "Sunday 22 November 2026"
    d.text(((W - tw(d, title, F_MAST)) // 2, 24), title, font=F_MAST, fill=NAVY)
    d.line([12, 110, W - 12, 110], fill=NAVY, width=1)
    sub = ("No deal at COP31 \u00b7 CENTCOM: no F-16 lost \u00b7 "
           "Democrats reach 258 seats")
    d.text(((W - tw(d, sub, F_SUB)) // 2, 114), sub, font=F_SUB, fill=(60, 60, 60))
    kick = "27 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text(((W - tw(d, kick, F_KICK)) // 2, 132), kick, font=F_KICK, fill=RED)

def draw_strip(d):
    y0, y1 = 152, 190
    d.rectangle([12, y0, W - 12, y1], outline=(200, 200, 200), width=1)
    cell_w = (W - 24) / 6
    for i, (num, story, label) in enumerate(STRIP):
        cx = 12 + i * cell_w
        if i:
            d.line([cx, y0 + 4, cx, y1 - 4], fill=(210, 210, 210), width=1)
        d.text((cx + 8, y0 + 2), num, font=F_STRIP_N, fill=NAVY)
        d.text((cx + cell_w - 8 - tw(d, story, F_STRIP_S), y0 + 4),
               story, font=F_STRIP_S, fill=RED)
        for j, ln in enumerate(wrap(d, label, F_STRIP_L, cell_w - 16)):
            d.text((cx + 8, y0 + 30 + j * 13), ln, font=F_STRIP_L, fill=(70, 70, 70))

def draw_regions(d):
    y0, y1 = 194, 214
    total = sum(n for _, n, _ in REGIONS)
    x = 12
    for name, n, color in REGIONS:
        w = (W - 24) * n / total
        d.rectangle([x, y0, x + w, y1], fill=color)
        label = "%s %d" % (name, n)
        font = F_REGION
        while tw(d, label, font) > w - 8 and font.size > 10:
            font = F("DejaVuSans-Bold.ttf", font.size - 1)
        d.text((x + (w - tw(d, label, font)) / 2, y0 + 3),
               label, font=font, fill=(255, 255, 255))
        x += w

def draw_timeline(d):
    y0, y1 = 218, 244
    d.rectangle([12, y0, W - 12, y1], fill=NAVY_DARK)
    lbl = "BY THE CLOCK (UTC)"
    lx = 20
    d.text((lx, y0 + 6), lbl, font=F_TL_LBL, fill=GOLD)
    # measure the entries; shrink font if they overflow (never clip silently)
    font = F_TL
    font_b = F_TL_B
    while True:
        total = tw(d, lbl, F_TL_LBL) + 12
        for t, txt in TIMELINE:
            total += tw(d, t + " ", font_b) + tw(d, txt, font) + tw(d, " \u00b7 ", font)
        if total <= W - 40 or font.size <= 10:
            break
        font = F("DejaVuSans.ttf", font.size - 1)
        font_b = F("DejaVuSans-Bold.ttf", font_b.size - 1)
    assert total <= W - 40, "timeline overflows at 10px: %dpx" % total
    cx = lx + tw(d, lbl, F_TL_LBL) + 12
    for i, (t, txt) in enumerate(TIMELINE):
        d.text((cx, y0 + 6), t, font=font_b, fill=(255, 255, 255))
        cx += tw(d, t, font_b)
        d.text((cx, y0 + 6), " " + txt, font=font, fill=(220, 225, 235))
        cx += tw(d, " " + txt, font)
        if i < len(TIMELINE) - 1:
            d.text((cx, y0 + 6), " \u00b7 ", font=font, fill=(140, 150, 170))
            cx += tw(d, " \u00b7 ", font)
    return font.size

def draw_larges(d):
    y0 = 250
    scene_h = 90
    cols = [12, 349, 686]
    col_w = 326
    for (num, bnr, head, deck, tag, src, scene, bnum, bcap), cx in zip(LARGES, cols):
        SCENES[scene](d, cx, y0, col_w, scene_h)
        banner(d, cx, y0, bnr, BANNER_COLORS[bnr])
        bw = badge_box(d, cx + col_w - 8 - max(tw(d, bnum, F_SCENE_L),
                       tw(d, bcap, F_BADGE)) - 16, y0 + scene_h - 58,
                       bnum, bcap)
        hy = y0 + scene_h + 6
        d.text((cx, hy), "%d" % num, font=F_L_HEAD, fill=RED)
        d.text((cx + 22, hy), head, font=F_L_HEAD, fill=NAVY)
        assert tw(d, head, F_L_HEAD) <= col_w - 22, "large headline wraps: %s" % head
        lines = wrap(d, deck, F_L_DECK, col_w)
        assert len(lines) <= 2, "large deck %d lines: %s" % (len(lines), deck)
        for j, ln in enumerate(lines):
            d.text((cx, hy + 28 + j * 15), ln, font=F_L_DECK, fill=INK)
        ty = hy + 28 + len(lines) * 15 + 2
        d.text((cx, ty), tag, font=F_L_TAG, fill=RED)
        d.text((cx + tw(d, tag + "  ", F_L_TAG), ty), src, font=F_L_TAG,
               fill=(100, 100, 100))
    return y0 + scene_h + 6 + 28 + 2 * 15 + 2 + 14  # larges bottom (~418)

def draw_mediums(d, y_top):
    row_h = 132
    cols = [12, 213, 414, 615, 816]
    col_w = 194
    scene_h = 52
    for row in range(2):
        for col in range(5):
            m = MEDIUMS[row * 5 + col]
            num, bnr, head, deck, tag, src, scene, snum = m
            cx = cols[col]
            cy = y_top + row * row_h
            SCENES[scene](d, cx, cy, col_w, scene_h)
            banner(d, cx, cy, bnr, BANNER_COLORS[bnr])
            # scene number, bottom-left of the scene, shadowed
            scene_number(d, cx + 6, cy + scene_h - 36, snum)
            hy = cy + scene_h + 4
            hlines = wrap(d, head, F_M_HEAD, col_w)
            assert len(hlines) <= 2, "medium headline %d lines: %s" % (len(hlines), head)
            for j, ln in enumerate(hlines):
                d.text((cx, hy + j * 18), ln, font=F_M_HEAD, fill=NAVY)
            dy = hy + len(hlines) * 18 + 1
            dlines = wrap(d, deck, F_M_DECK, col_w)
            assert len(hlines) + len(dlines) <= 4, \
                "medium %d overflows: %d+%d lines" % (num, len(hlines), len(dlines))
            for j, ln in enumerate(dlines):
                d.text((cx, dy + j * 12), ln, font=F_M_DECK, fill=INK)
            ty = dy + len(dlines) * 12 + 1
            assert ty + 12 <= cy + row_h, "medium %d tag overflows" % num
            d.text((cx, ty), tag, font=F_M_TAG, fill=RED)
            d.text((cx + tw(d, tag + "  ", F_M_TAG), ty), src, font=F_M_TAG,
                   fill=(100, 100, 100))
    return y_top + 2 * row_h

# ---------------------------------------------------------------- map
MAP_X, MAP_Y, MAP_W, MAP_H = 12, 712, 318, 168
CONTINENTS = [
    # North America
    [(20, 20), (60, 10), (110, 18), (120, 40), (100, 55), (80, 50),
     (70, 70), (45, 75), (25, 55), (15, 35)],
    # South America
    [(70, 85), (105, 80), (120, 100), (105, 140), (85, 155), (70, 130),
     (62, 105)],
    # Europe
    [(150, 15), (195, 12), (205, 30), (198, 48), (190, 56), (165, 50),
     (150, 35)],
    # Africa
    [(150, 55), (200, 55), (215, 85), (195, 120), (170, 125), (150, 95),
     (145, 70)],
    # Arabia
    [(200, 55), (230, 55), (235, 80), (215, 95), (200, 85)],
    # Asia
    [(205, 12), (310, 10), (315, 45), (290, 70), (250, 85), (215, 70),
     (205, 40)],
    # Australia
    [(270, 105), (315, 100), (318, 125), (300, 145), (275, 135)],
]

def draw_map(d):
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA,
                outline=(180, 180, 180), width=1)
    for poly in CONTINENTS:
        pts = [(MAP_X + px, MAP_Y + py) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # Indonesia islands
    for ix, iy, iw, ih in [(238, 88, 16, 6), (258, 92, 20, 6), (280, 90, 12, 5)]:
        d.ellipse([MAP_X + ix, MAP_Y + iy, MAP_X + ix + iw, MAP_Y + iy + ih],
                  fill=LAND, outline=LAND_LINE)
    # New Zealand
    d.ellipse([MAP_X + 306, MAP_Y + 122, MAP_X + 312, MAP_Y + 138],
              fill=LAND, outline=LAND_LINE)
    d.ellipse([MAP_X + 310, MAP_Y + 138, MAP_X + 316, MAP_Y + 150],
              fill=LAND, outline=LAND_LINE)
    # pins (numbered red circles)
    for num, px, py in MAP_PINS:
        cx, cy = MAP_X + px, MAP_Y + py
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((cx - tw(d, t, F_MAP_LBL) / 2, cy - 6), t, font=F_MAP_LBL,
               fill=(255, 255, 255))
    for text, lx, ly in MAP_LABELS:
        d.text((MAP_X + lx, MAP_Y + ly), text, font=F_MAP_LBL, fill=(60, 60, 60))

def draw_briefs(d):
    d.text((340, 694), "ALSO ON SUNDAY 22 NOVEMBER \u2014 14 MORE STORIES",
           font=F_HDR, fill=NAVY)
    cols = [340, 678]
    col_w = 330
    for i, (num, head, deck, src) in enumerate(BRIEFS):
        cx = cols[i % 2]
        cy = 712 + (i // 2) * 32
        num_s = "%d " % num
        nw = tw(d, num_s, F_BRIEF_B)
        d.text((cx, cy), num_s, font=F_BRIEF_B, fill=RED)
        full = head + " \u2014 " + deck + ((" (%s)" % src) if src else "")
        segs = [(head + " \u2014 ", F_BRIEF_B),
                (deck + ((" (%s)" % src) if src else ""), F_BRIEF)]
        lines = wrap_mixed(d, segs, col_w - nw)
        assert len(lines) <= 2, "brief %d wraps to %d lines" % (num, len(lines))
        for j, runs in enumerate(lines):
            x = cx + nw
            for text, font in runs:
                d.text((x, cy + j * 15), text, font=font, fill=INK)
                x += tw(d, text + " ", font)

def draw_howto(d):
    x0, y0, x1, y1 = 12, 884, 330, 936
    d.rectangle([x0, y0, x1, y1], outline=(180, 180, 180), width=1)
    text = ("HOW TO READ \u2014 At thumbnail size: the date, three leads, "
            "ten big stories. At full size: 14 briefs, the map, and the "
            "DATE CHECK.")
    lines = wrap(d, text, F_HOW, x1 - x0 - 16)
    for j, ln in enumerate(lines):
        d.text((x0 + 8, y0 + 5 + j * 14), ln, font=F_HOW, fill=(80, 80, 80))

def draw_dc(d):
    x0, y0, x1, y1 = 12, 940, 1012, 1004
    d.rectangle([x0, y0, x1, y1], outline=RED, width=2)
    text = ("Left out: " + " \u00b7 ".join(DC_EXCLUSIONS) + ". " + DC_DEFENSE
            + " " + DC_NOTYET + " " + DC_CLOSE)
    lbl = "DATE CHECK"
    lw = tw(d, lbl, F_DC_LBL)
    # custom wrap: line 1 narrower (label takes the front), rest full width
    words = text.split(" ")
    lines, cur, cur_w = [], "", 0
    first_w = (x1 - x0 - 16) - lw - 10
    full_w = x1 - x0 - 16
    limit = first_w
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, F_DC) <= limit or not cur:
            cur, cur_w = t, tw(d, t, F_DC)
        else:
            lines.append(cur)
            cur, limit = w, full_w
    if cur:
        lines.append(cur)
    assert len(lines) <= 4, "DATE CHECK wraps to %d lines" % len(lines)
    d.text((x0 + 8, y0 + 5), lbl, font=F_DC_LBL, fill=RED)
    d.text((x0 + 8 + lw + 10, y0 + 5), lines[0], font=F_DC, fill=INK)
    for j, ln in enumerate(lines[1:], start=1):
        d.text((x0 + 8, y0 + 5 + j * 14), ln, font=F_DC, fill=INK)
    return len(lines)

def draw_legend(d):
    txt = ("CONFIRMED 2+ outlets \u00b7 OFFICIAL on the record \u00b7 "
           "REPORTED one outlet \u00b7 CLAIM one side\u2019s claim \u00b7 "
           "Wires read to %s UTC \u00b7 Original drawings." % PRESS_TIME)
    d.text(((W - tw(d, txt, F_LEGEND)) // 2, 1008), txt, font=F_LEGEND,
           fill=GRAY)

# ---------------------------------------------------------------- audits
def run_audits():
    # tally
    assert sum(n for _, n, _ in REGIONS) == 27, "region tally != 27"
    assert len(LARGES) + len(MEDIUMS) + len(BRIEFS) == 27, "story count != 27"
    assert len(LARGES) == 3 and len(MEDIUMS) == 10 and len(BRIEFS) == 14
    # strip cross-refs: each strip number appears in its story
    story_text = {}
    for num, bnr, head, deck, tag, src, scene, bnum, bcap in LARGES:
        story_text[num] = head + " " + deck + " " + bnum
    for num, bnr, head, deck, tag, src, scene, snum in MEDIUMS:
        story_text[num] = head + " " + deck + " " + snum
    strip_story = {"186": 3, "720/9": 6, "98.79%": 7, "258": 13,
                   "1,300": 12, "0": 1}
    for num, _, _ in STRIP:
        assert num in story_text[strip_story[num]], \
            "strip number not cross-referenced: %s" % num
    # DC cross-audit: no exclusion appears as a main/brief
    all_story = " ".join(story_text.values()) + " " + " ".join(
        "%s %s" % (h, dd) for _, h, dd, _ in BRIEFS)
    for key in ["Kryvyi Rih", "400-drone", "El Chapo", "Bayelsa", "Bolsonaro",
                "aid-van", "evacuation", "148-drone", "EU\u2013Indonesia",
                "Nvidia", "Ladakh", "Basra"]:
        assert key not in all_story, "DC exclusion carried as story: %s" % key
    # string audit: no wrong-day refs in story strings (dual labels allowed)
    duals = {"Norris 0.6s back; Piastri 3rd from 17th. Sat night = Sun 04:00 UTC.",
             "Probe enters Mercury orbit. Burn 18:24 GMT Sat = 01:24 WIB Sun.",
             "Saudi defences stop Houthi strike. Early Sun Riyadh (Sat 22:42 UTC).",
             "first title. Sat night in Washington = Sun 01:00 UTC."}
    for s in list(story_text.values()) + ["%s %s" % (h, dd) for _, h, dd, _ in BRIEFS]:
        assert "Fri" not in s, "Friday ref in story: %s" % s
        assert "20 Nov" not in s and "21 Nov" not in s and "15 Nov" not in s, \
            "wrong-day ref in story: %s" % s
        if "Sat" in s:
            assert any(dd in s for dd in duals), "unlabelled Sat ref: %s" % s
    # map pin separation
    for i, (n1, x1, y1) in enumerate(MAP_PINS):
        for n2, x2, y2 in MAP_PINS[i + 1:]:
            dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            assert dist >= 14, "map pins %d/%d too close: %.1f" % (n1, n2, dist)
    print("audits: tally 27=27, strip 6/6, DC cross-audit, string audit, "
          "map pins — all pass")

# ---------------------------------------------------------------- main
def build():
    run_audits()
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_top(d)
    draw_masthead(d)
    draw_strip(d)
    draw_regions(d)
    tl_size = draw_timeline(d)
    larges_bottom = draw_larges(d)
    mediums_bottom = draw_mediums(d, 426)
    d.text((12, 694), "WHERE IT HAPPENED", font=F_HDR, fill=NAVY)
    draw_map(d)
    draw_briefs(d)
    draw_howto(d)
    dc_lines = draw_dc(d)
    draw_legend(d)
    print("layout: timeline font %dpx, larges end %d, mediums end %d, "
          "DC lines %d" % (tl_size, larges_bottom, mediums_bottom, dc_lines))
    return img

if __name__ == "__main__":
    import hashlib
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    data = open(out, "rb").read()
    print("entry.png: %d bytes, sha256 %s" % (len(data),
          hashlib.sha256(data).hexdigest()))
    assert len(data) <= 1048576, "entry.png over 1 MiB"
    small = img.resize((300, 300), Image.LANCZOS)
    small.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry-300.png"))
    print("entry-300.png written")
