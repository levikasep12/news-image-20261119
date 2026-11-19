#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261119.

A one-page broadsheet summing Thursday 19 November 2026 world news:
masthead + date, one illustrated lead (Shenzhen trilateral summit), two more
illustrated stories (Crimean Bridge strike, Cyclone Akvan), 12 numbered
stories, a dotted world map with numbered story locations, and 18 one-line
briefs -- 33 stories across six continents.

The three photos are AI-generated illustrations made for this entry (see
assets/); the text is drawn from 19 November 2026 reporting (BBC, The New
York Times, CBS News, The Guardian, The Japan Times, France 24, The Hindu).

Build tool only: it needs Pillow, which the grader does not install. The
entry itself is main.py, which just copies the finished entry.png. Run:
    python3 build_image.py
from this directory (or anywhere: paths derive from this file).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

NAVY = (22, 35, 63)
GOLD = (242, 183, 5)
RED = (192, 57, 43)
INK = (26, 26, 26)
GREY = (96, 96, 96)
PAPER = (250, 246, 236)
CARD = (255, 255, 255)
LINE = (205, 196, 176)
SEA = (223, 233, 240)
LAND = (74, 102, 130)
CHIP = (192, 57, 43)

FDIR = Path("/usr/share/fonts/truetype")


def font(name, size):
    return ImageFont.truetype(str(FDIR / name), size)


SERIF_B = "dejavu/DejaVuSerif-Bold.ttf"
SANS = "dejavu/DejaVuSans.ttf"
SANS_B = "dejavu/DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def photo_cover(path, box_w, box_h):
    """Centre-crop an image to exactly box_w x box_h."""
    im = Image.open(path).convert("RGB")
    scale = max(box_w / im.width, box_h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)),
                   Image.LANCZOS)
    x = (im.width - box_w) // 2
    y = (im.height - box_h) // 2
    return im.crop((x, y, x + box_w, y + box_h))


# Coarse land mask: (latitude, [(lon_min, lon_max), ...]) for a dotted map.
LAND_ROWS = [
    (70, [(-168, -140), (-125, -90), (-85, -68), (-58, -20), (30, 180), (-180, -178)]),
    (65, [(-168, -140), (-140, -95), (-78, -60), (-55, -22), (-22, -14), (12, 30), (30, 180), (-180, -170)]),
    (60, [(-165, -140), (-140, -95), (-78, -65), (-45, -40), (5, 30), (28, 180), (-180, -162)]),
    (55, [(-135, -130), (-130, -95), (-80, -65), (-6, 1), (8, 24), (22, 180), (-180, -162)]),
    (50, [(-125, -95), (-80, -60), (-5, 1), (0, 30), (25, 140), (85, 130), (142, 143), (156, 160)]),
    (45, [(-124, -67), (-9, 7), (7, 18), (19, 29), (36, 54), (50, 85), (85, 130), (140, 145)]),
    (40, [(-124, -74), (-9, -2), (8, 18), (20, 28), (26, 44), (47, 54), (55, 75), (75, 122), (126, 130), (130, 141)]),
    (35, [(-120, -80), (-6, 10), (10, 25), (25, 35), (35, 48), (44, 63), (61, 75), (70, 88), (78, 122), (130, 140)]),
    (30, [(-115, -87), (-81, -80), (-17, 32), (32, 35), (35, 55), (57, 63), (61, 70), (68, 88), (98, 122), (120, 122)]),
    (25, [(-110, -87), (-17, 32), (35, 58), (68, 88), (92, 110), (106, 120)]),
    (20, [(-105, -87), (-17, 32), (35, 58), (68, 85), (92, 109), (108, 120), (120, 122)]),
    (15, [(-95, -83), (-17, 32), (43, 58), (73, 80), (94, 109), (120, 122)]),
    (10, [(-86, -77), (-77, -52), (-17, 51), (76, 80), (98, 105), (120, 127)]),
    (5, [(-77, -50), (-13, 51), (95, 120), (131, 141)]),
    (0, [(-80, -50), (-8, 42), (95, 120), (131, 147)]),
    (-5, [(-80, -35), (9, 40), (95, 120), (131, 147)]),
    (-10, [(-78, -35), (12, 40), (105, 120), (131, 147)]),
    (-15, [(-75, -35), (12, 35), (44, 50), (114, 146)]),
    (-20, [(-70, -40), (14, 33), (44, 48), (114, 153)]),
    (-25, [(-70, -48), (16, 33), (44, 48), (114, 153)]),
    (-30, [(-70, -48), (16, 33), (114, 153)]),
    (-35, [(-72, -52), (18, 28), (115, 152)]),
    (-40, [(-73, -62), (140, 150), (167, 178)]),
    (-45, [(-73, -65), (168, 174)]),
    (-50, [(-74, -66)]),
    (-55, [(-70, -66)]),
]

# Numbered story locations on the map: (lon, lat, number).
MAP_DOTS = [
    (114, 22, "1"),   # Shenzhen summit
    (34, 45, "2"),    # Crimean Bridge
    (85, 20, "3"),    # Cyclone Akvan, Odisha
    (4, 52, "4"),     # ICJ, The Hague
    (56, 27, "5"),    # Gulf strikes
    (-74, 41, "6"),   # New York (IPO, Van Gogh)
    (151, -34, "7"),  # Sydney
    (3, 6, "8"),      # Lagos / Nigeria
]

MAP_KEY = ("1 Shenzhen summit  ·  2 Crimea bridge  ·  3 Cyclone Akvan  ·  4 ICJ, The Hague"
           "  ·  5 Gulf strikes  ·  6 New York  ·  7 Sydney  ·  8 Nigeria")

# 12 numbered mid stories: (headline, one-line deck).
NUMBERED = [
    ("ICJ rules on Rohingya genocide case", "Gambia v. Myanmar verdict at The Hague."),
    ("Iran hits Gulf states after US strike", "Tehran retaliates after US bombs Qeshm."),
    ("Anthropic IPO sets $81.3bn record", "Listing values the AI lab at $1.5tn."),
    ("COP31 ministers race for a deal", "Antalya talks still stuck on a final text."),
    ("Bangladesh unrest: Yunus home torched", "Violence spreads across 28 districts."),
    ("Van Gogh sells for $190.4m, a record", "'Chestnut Trees in Flower' tops record."),
    ("UK sends Ukraine 1,000 strike drones", "Kyiv keeps hitting Russian targets."),
    ("EU proposes \u20ac45bn loan for Ukraine", "Brussels unveils new support for Kyiv."),
    ("IAEA: N. Korea grew enrichment work", "Watchdog cites Yongbyon enrichment."),
    ("589m children live in conflict zones", "Record number as aid access is blocked."),
    ("Eisenkot tapped to form Israel govt", "President bypasses Netanyahu."),
    ("Russian military plane crash kills 19", "Transport aircraft down in Siberia."),
]

# 18 one-line briefs.
BRIEFS = [
    "Abu Dhabi talks end with no breakthrough",
    "Russia demands NATO pull back to 1997 borders",
    "US, Venezuela sign military cooperation deal",
    "IEA: Hormuz crisis worst energy threat yet",
    "Datacentre emissions to rise 70% by 2030 — IEA",
    "S. Korea's Lee urges dialogue with Pyongyang",
    "Four nations demand aid access to flooded Gaza",
    "GTA VI launches worldwide today",
    "IMF lifts Germany growth forecast to 1.3%",
    "England drought now covers 82% of the land",
    "Nigeria: Senate acts over 37 dead miners",
    "Romania: Georgescu moved to house arrest",
    "France: 4th weekend of cost-of-living protests",
    "Pew: Muslims to outnumber Christians by 2035",
    "Uganda landslide survivors seek justice at UN",
    "Free entry to Taj Mahal as Heritage Week opens",
    "Leasehold to be scrapped in England and Wales",
    "Ocean Photographer of the Year opens in Sydney",
]


def draw_map(draw, x0, y0, w, h):
    """Dotted world map with numbered story dots."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    lat_top, lat_bot = 72, -58
    for lat, spans in LAND_ROWS:
        y = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
        lon = -180.0
        while lon < 180:
            if any(a <= lon <= b for a, b in spans):
                x = x0 + (lon + 180) / 360 * w
                draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=LAND)
            lon += 2.5
    fnum = font(SANS_B, 11)
    for lon, lat, num in MAP_DOTS:
        x = x0 + (lon + 180) / 360 * w
        y = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = draw.textlength(num, font=fnum)
        draw.text((x - tw / 2, y - 7), num, font=fnum, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 92], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    f_title = font(SERIF_B, 44)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 8), title,
           font=f_title, fill=(255, 255, 255))
    date = "THURSDAY  19  NOVEMBER  2026"
    f_date = font(SANS_B, 19)
    d.text(((W - d.textlength(date, font=f_date)) / 2, 60), date,
           font=f_date, fill=GOLD)
    d.rectangle([0, 92, W, 96], fill=RED)

    # ---- Lead story: Shenzhen summit ----
    d.text((16, 104), "SHENZHEN  \u2022  LEAD STORY", font=font(SANS_B, 15),
           fill=RED)
    f_lead = font(SERIF_B, 36)
    d.text((16, 126), "THREE POWERS,", font=f_lead, fill=INK)
    d.text((16, 168), "ONE TABLE", font=f_lead, fill=INK)
    deck = ("Trump, Xi and Putin hold the first-ever three-way summit at "
            "APEC in Shenzhen \u2014 nuclear arms and Ukraine top the agenda.")
    f_deck = font(SANS, 16)
    y = 216
    for line in wrap(d, deck, f_deck, 568):
        d.text((16, y), line, font=f_deck, fill=INK)
        y += 22
    img.paste(photo_cover(HERE / "assets" / "summit.jpg", 404, 172),
              (604, 104))
    d.rectangle([604, 104, 1008, 276], outline=LINE, width=1)

    # ---- Second row: two illustrated stories ----
    cards = [
        (16, "bridge.jpg", "UKRAINE  \u2022  WAR",
         "Bridge hit again",
         "Third strike this week; a road span is down, car traffic halted."),
        (520, "cyclone.jpg", "INDIA  \u2022  WEATHER",
         "Cyclone Akvan nears land",
         "100,000+ evacuated in Odisha; red alert in Andhra Pradesh."),
    ]
    for x, photo, kicker, head, deck in cards:
        img.paste(photo_cover(HERE / "assets" / photo, 488, 100), (x, 284))
        d.rectangle([x, 284, x + 488, 384], outline=LINE, width=1)
        d.text((x + 2, 390), kicker, font=font(SANS_B, 12), fill=RED)
        d.text((x + 2, 406), head, font=font(SERIF_B, 21), fill=INK)
        f_cd = font(SANS, 12)
        yy = 432
        for line in wrap(d, deck, f_cd, 484):
            d.text((x + 2, yy), line, font=f_cd, fill=GREY)
            yy += 15

    # ---- 12 numbered stories ----
    d.rectangle([16, 448, 1008, 468], fill=NAVY)
    d.text((26, 451), "MORE OF THE DAY", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    f_num = font(SANS_B, 11)
    f_nh = font(SANS_B, 13)
    f_nd = font(SANS, 11)
    for i, (head, deck) in enumerate(NUMBERED):
        col, row = i % 3, i // 3
        x = 16 + col * 328
        y = 474 + row * 36
        d.ellipse([x, y, x + 19, y + 19], fill=CHIP)
        num = str(i + 1)
        d.text((x + (19 - d.textlength(num, font=f_num)) / 2, y + 2), num,
               font=f_num, fill=(255, 255, 255))
        d.text((x + 25, y - 1), head, font=f_nh, fill=INK)
        d.text((x + 25, y + 15), deck, font=f_nd, fill=GREY)

    # ---- World map ----
    d.rectangle([16, 620, 1008, 640], fill=NAVY)
    d.text((26, 623), "WHERE IT HAPPENED", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    draw_map(d, 16, 644, 992, 192)
    d.rectangle([16, 644, 1008, 836], outline=LINE, width=1)
    f_key = font(SANS, 11)
    d.text(((W - d.textlength(MAP_KEY, font=f_key)) / 2, 840), MAP_KEY,
           font=f_key, fill=GREY)

    # ---- 18 briefs ----
    d.rectangle([16, 860, 1008, 880], fill=NAVY)
    d.text((26, 863), "IN BRIEF", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    f_br = font(SANS, 11)
    for i, brief in enumerate(BRIEFS):
        col, row = i % 3, i // 3
        x = 16 + col * 328
        y = 886 + row * 17
        d.text((x, y), "\u2022  " + brief, font=f_br, fill=INK)

    # ---- Footer ----
    d.line([16, 992, 1008, 992], fill=LINE, width=1)
    f_ft = font(SANS, 10)
    src = ("Drawn from 19 November 2026 reporting: BBC  \u2022  The New York Times  "
           "\u2022  CBS News  \u2022  The Guardian  \u2022  The Japan Times  \u2022  France 24  "
           "\u2022  The Hindu")
    d.text(((W - d.textlength(src, font=f_ft)) / 2, 996), src, font=f_ft,
           fill=GREY)
    cred = "Illustrations: AI-generated scenes  \u2022  One image, one day \u2014 make.fun news-image-20261119"
    d.text(((W - d.textlength(cred, font=f_ft)) / 2, 1010), cred, font=f_ft,
           fill=GREY)

    out = HERE / "entry.png"
    img.save(out, "PNG", optimize=True)
    size = out.stat().st_size
    print(f"wrote {out} {img.size} {size} bytes")
    if size > 1048576:
        img.save(out, "JPEG", quality=88, optimize=True)
        print(f"PNG over 1 MiB; saved as JPEG {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
