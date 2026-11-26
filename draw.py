#!/usr/bin/env python3
"""Sum up 25 November's world news in one image.

Entry for make.fun bounty news-image-20261125:
"Sum up 25 November's world news in one image" ($100 USDC).

The program draws a 1024x1024 newspaper front page with Pillow only.
No network, no randomness, no timestamps, no external files: the same
input always produces byte-identical output, so two runs match.

Run:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 draw.py
    # writes out/entry.png (1024x1024, PNG, under 1 MiB)
In the grader, MAKEFUN_OUTPUT_DIR is unset and the image goes to
/output/entry.png.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)      # off-white paper
INK = (20, 33, 61)           # dark navy ink
RED = (180, 35, 24)          # single red accent
MUTED = (90, 90, 82)
WHITE = (255, 255, 255)
BLUE = (37, 99, 168)
TEAL = (31, 122, 109)
ORANGE = (217, 108, 0)
GOLD = (184, 134, 11)
LIGHT = (232, 228, 216)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)                  # noqa: E731


def wrap(draw, text, fnt, max_width):
    """Wrap text into lines that fit max_width. Returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, lines, fnt, fill, spacing=None):
    """Draw centred lines starting at y. Returns y below the last line."""
    if spacing is None:
        spacing = int(fnt.size * 1.18)
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += spacing
    return y


def draw_left(draw, x, y, lines, fnt, fill, spacing=None):
    if spacing is None:
        spacing = int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += spacing
    return y


# ---------------------------------------------------------------- icons
def icon_tanker(draw, cx, cy):
    """Oil tanker on waves, with a spiked mine and flame. Centred at cx, cy."""
    # sea
    draw.ellipse([cx - 150, cy + 55, cx + 150, cy + 115], fill=BLUE)
    draw.rectangle([cx - 150, cy + 80, cx + 150, cy + 115], fill=BLUE)
    for dx in (-110, -40, 30, 100):
        draw.arc([cx + dx - 28, cy + 62, cx + dx + 28, cy + 102],
                 start=200, end=340, fill=WHITE, width=4)
    # hull
    draw.polygon([(cx - 135, cy - 5), (cx + 135, cy - 5), (cx + 115, cy + 55),
                  (cx - 115, cy + 55)], fill=INK)
    draw.rectangle([cx - 135, cy - 12, cx + 135, cy - 5], fill=RED)
    # deck / bridge
    draw.rectangle([cx + 70, cy - 55, cx + 125, cy - 12], fill=WHITE,
                   outline=INK, width=2)
    draw.rectangle([cx + 78, cy - 47, cx + 117, cy - 30], fill=BLUE)
    # containers
    for i, col in enumerate((RED, GOLD, TEAL)):
        x0 = cx - 120 + i * 52
        draw.rectangle([x0, cy - 48, x0 + 46, cy - 12], fill=col,
                       outline=INK, width=2)
    # mine, top right
    mx, my = cx + 105, cy - 105
    for ang in range(0, 360, 45):
        import math
        r = 16
        x1 = mx + int(r * math.cos(math.radians(ang)))
        y1 = my + int(r * math.sin(math.radians(ang)))
        x2 = mx + int(26 * math.cos(math.radians(ang)))
        y2 = my + int(26 * math.sin(math.radians(ang)))
        draw.line([x1, y1, x2, y2], fill=INK, width=4)
    draw.ellipse([mx - 16, my - 16, mx + 16, my + 16], fill=INK)
    # flame above the tanker
    fx, fy = cx - 55, cy - 105
    draw.polygon([(fx - 22, fy + 28), (fx, fy - 28), (fx + 10, fy + 2),
                  (fx + 24, fy + 28)], fill=ORANGE)
    draw.polygon([(fx - 10, fy + 28), (fx, fy - 6), (fx + 12, fy + 28)],
                 fill=GOLD)


def icon_refinery(draw, cx, cy):
    """Refinery towers with a flame. Fits cy +/- 32."""
    base = cy + 28
    draw.rectangle([cx - 55, base, cx + 55, base + 4], fill=INK)
    for x0, hgt, col in ((-52, 42, INK), (-26, 30, BLUE), (0, 50, INK),
                         (28, 36, TEAL)):
        draw.rectangle([cx + x0, base - hgt, cx + x0 + 20, base], fill=col)
        draw.rectangle([cx + x0 + 5, base - hgt - 7, cx + x0 + 15,
                        base - hgt], fill=col)
    draw.line([cx - 32, base - 18, cx - 6, base - 18], fill=INK, width=3)
    fx, fy = cx + 10, base - 62
    draw.polygon([(fx - 8, fy + 10), (fx, fy - 10), (fx + 4, fy + 1),
                  (fx + 9, fy + 10)], fill=ORANGE)


def icon_rocket(draw, cx, cy):
    """Rocket on an orbit arc, with stars. Fits cy +/- 32."""
    for sx, sy in ((-70, -28), (68, -24), (58, 26), (-66, 22)):
        draw.ellipse([cx + sx - 2, cy + sy - 2, cx + sx + 2, cy + sy + 2],
                     fill=GOLD)
    draw.arc([cx - 78, cy - 28, cx + 78, cy + 52], start=200, end=340,
             fill=TEAL, width=3)
    draw.polygon([(cx - 13, cy + 12), (cx - 13, cy - 22), (cx, cy - 32),
                  (cx + 13, cy - 22), (cx + 13, cy + 12)], fill=WHITE,
                 outline=INK, width=2)
    draw.ellipse([cx - 6, cy - 16, cx + 6, cy - 4], fill=BLUE,
                 outline=INK, width=1)
    draw.polygon([(cx - 13, cy + 12), (cx - 26, cy + 26), (cx - 13, cy + 22)],
                 fill=RED)
    draw.polygon([(cx + 13, cy + 12), (cx + 26, cy + 26), (cx + 13, cy + 22)],
                 fill=RED)
    draw.polygon([(cx - 7, cy + 26), (cx, cy + 32), (cx + 7, cy + 26)],
                 fill=ORANGE)


def icon_chip(draw, cx, cy):
    """Microchip (Huawei = tech trial). Fits cy +/- 32."""
    draw.rectangle([cx - 28, cy - 28, cx + 28, cy + 28], fill=INK)
    draw.rectangle([cx - 15, cy - 15, cx + 15, cy + 15], fill=BLUE,
                   outline=WHITE, width=2)
    draw.text((cx - 5, cy - 8), "H", font=SANS_BOLD(15), fill=WHITE)
    for i in (-18, 0, 18):
        draw.line([cx + i, cy - 28, cx + i, cy - 34], fill=INK, width=3)
        draw.line([cx + i, cy + 28, cx + i, cy + 34], fill=INK, width=3)
        draw.line([cx - 28, cy + i, cx - 34, cy + i], fill=INK, width=3)
        draw.line([cx + 28, cy + i, cx + 34, cy + i], fill=INK, width=3)


def icon_tariff(draw, cx, cy):
    """Bar chart with a rising arrow. Fits cy +/- 32."""
    base = cy + 28
    draw.line([cx - 55, base, cx + 55, base], fill=INK, width=3)
    for i, (hgt, col) in enumerate(((16, TEAL), (26, BLUE), (38, RED))):
        x0 = cx - 48 + i * 32
        draw.rectangle([x0, base - hgt, x0 + 22, base], fill=col)
    draw.line([cx - 50, cy - 22, cx + 50, cy - 28], fill=INK, width=3)
    draw.polygon([(cx + 50, cy - 28), (cx + 34, cy - 30), (cx + 46, cy - 16)],
                 fill=INK)


def icon_climate(draw, cx, cy):
    """Globe with a thermometer. Fits cy +/- 32."""
    draw.ellipse([cx - 48, cy - 30, cx + 8, cy + 26], fill=BLUE)
    draw.ellipse([cx - 36, cy - 18, cx - 18, cy - 2], fill=TEAL)
    draw.ellipse([cx - 22, cy + 4, cx + 2, cy + 22], fill=TEAL)
    draw.arc([cx - 48, cy - 30, cx + 8, cy + 26], start=0, end=360,
             fill=INK, width=2)
    draw.line([cx - 48, cy - 2, cx + 8, cy - 2], fill=WHITE, width=2)
    draw.rectangle([cx + 28, cy - 28, cx + 40, cy + 12], fill=WHITE,
                   outline=INK, width=2)
    draw.rectangle([cx + 31, cy - 4, cx + 37, cy + 10], fill=RED)
    draw.ellipse([cx + 24, cy + 8, cx + 44, cy + 28], fill=RED,
                 outline=INK, width=2)


def icon_balloon(draw, cx, cy):
    """Parade balloon over rooftops. Fits cy +/- 32."""
    draw.rectangle([cx - 60, cy + 22, cx + 60, cy + 30], fill=INK)
    for x0, hgt in ((-58, 14), (-30, 20), (2, 16), (32, 22)):
        draw.rectangle([cx + x0, cy + 22 - hgt, cx + x0 + 22, cy + 22],
                       fill=BLUE)
    draw.ellipse([cx - 26, cy - 32, cx + 26, cy + 8], fill=RED)
    draw.polygon([(cx - 8, cy + 7), (cx, cy + 18), (cx + 8, cy + 7)],
                 fill=RED)
    draw.ellipse([cx - 16, cy - 24, cx - 5, cy - 10], fill=(255, 255, 255))
    for (dx, dy, col) in ((-48, -22, GOLD), (48, -20, TEAL), (-40, 8, ORANGE),
                          (44, 6, BLUE)):
        draw.rectangle([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3],
                       fill=col)


# ---------------------------------------------------------------- page
PANELS = [
    ("MIDDLE EAST", icon_refinery,
     "HOUTHIS HIT SAUDI REFINERY",
     "Houthis say they attacked the Ras Tanura oil refinery, causing fires."),
    ("SPACE", icon_rocket,
     "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
     "Shenzhou-24 docked at China's Tiangong station with Muhammad Zeeshan Ali aboard."),
    ("TECH", icon_chip,
     "HUAWEI CONVICTED IN U.S. TRIAL",
     "Jury found Huawei guilty of trade-secret theft and bank fraud, not racketeering."),
    ("TRADE", icon_tariff,
     "U.S. PROPOSES NEW TARIFFS",
     "Washington proposed new tariffs on 14 trading partners, with a hearing set for 25 January."),
    ("CLIMATE", icon_climate,
     "COP31 CLIMATE TALKS FAIL",
     "U.N. climate talks ended with no deal; Pope Leo XIV warned of more extreme weather."),
    ("U.S.", icon_balloon,
     "MACY'S PARADE POSTPONED",
     "The 100th Thanksgiving parade in New York was put off to Saturday by forecast storms — a first in 100 years."),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---- header
    draw.rectangle([mx, 20, W - mx, 26], fill=RED)
    draw_centered(draw, W // 2, 34, ["WORLD NEWS"], SERIF_BOLD(84), INK,
                  spacing=96)
    draw_centered(draw, W // 2, 132, ["WEDNESDAY, 25 NOVEMBER 2026"],
                  SANS_BOLD(34), RED, spacing=44)
    draw.line([mx, 182, W - mx, 182], fill=INK, width=2)
    draw_centered(draw, W // 2, 192,
                  ["From Hormuz to orbit: the day's biggest stories, in one page"],
                  SANS(18), MUTED, spacing=24)

    # ---- lead story
    ly0, ly1 = 224, 540
    draw.rectangle([mx, ly0, W - mx, ly1], fill=WHITE, outline=INK, width=2)
    draw.rectangle([mx, ly0, W - mx, ly0 + 8], fill=RED)
    tx = mx + 24
    draw.text((tx, ly0 + 22), "LEAD STORY  ·  MIDDLE EAST",
              font=SANS_BOLD(17), fill=RED)
    headline = ["TANKERS HIT MINES", "IN THE STRAIT", "OF HORMUZ"]
    y = draw_left(draw, tx, ly0 + 52, headline, SERIF_BOLD(42), INK,
                  spacing=50)
    body = wrap(draw,
                "Oil tankers struck naval mines and caught fire in the "
                "Strait of Hormuz, Iran's Revolutionary Guard said.",
                SANS(19), 560)
    draw_left(draw, tx, y + 14, body, SANS(19), INK, spacing=25)
    icon_tanker(draw, 800, 380)

    # ---- six panels, 3 x 2
    pw, ph, gap = 312, 214, 16
    gy0 = 556
    for i, (tag, icon, headline_text, body_text) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x0 = mx + col * (pw + gap)
        y0 = gy0 + row * (ph + gap)
        draw.rectangle([x0, y0, x0 + pw, y0 + ph], fill=WHITE,
                       outline=INK, width=2)
        draw.text((x0 + 14, y0 + 10), tag, font=SANS_BOLD(13), fill=RED)
        icon(draw, x0 + pw // 2, y0 + 60)
        # headline, centred, max 2 lines at 21pt
        hl = wrap(draw, headline_text, SANS_BOLD(20), pw - 24)
        y = draw_centered(draw, x0 + pw // 2, y0 + 100, hl,
                          SANS_BOLD(20), INK, spacing=23)
        bl = wrap(draw, body_text, SANS(14), pw - 28)
        draw_centered(draw, x0 + pw // 2, y + 4, bl, SANS(14), MUTED,
                      spacing=18)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=False)
    return path


if __name__ == "__main__":
    print(build())
