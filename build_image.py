#!/usr/bin/env python3
"""Build entry.png: one image summing up the world news of Tuesday 24 November 2026.

Draws a newspaper front page with Pillow at 2x scale and downsamples it,
so edges and text stay clean. Layout is measured first (every text block
is wrapped and counted before anything is drawn), so no caption can ever
overflow its panel.

Run locally to (re)build the image:

    python3 build_image.py

The competition entry itself is main.py, which only copies entry.png to
/output/entry.png inside the grader's sandbox (standard library only).
"""

import math

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor
W, H = 1024 * S, 1024 * S

PAPER = (248, 244, 232)
CARD = (255, 253, 246)
INK = (20, 22, 26)
MUTE = (92, 92, 88)
RED = (179, 35, 42)
GREEN = (29, 111, 66)
NAVY = (39, 65, 86)
DARKRED = (122, 31, 43)
GOLD = (138, 90, 18)
PURPLE = (75, 46, 131)
BLUE = (46, 96, 178)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FONT_DIR}/liberation/LiberationSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf"
SANS_I = f"{FONT_DIR}/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size * S)


def wrap(d, text, font, max_w):
    """Greedy word wrap on measured text width."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block_h(font, n_lines, leading=1.18):
    """Height of n_lines of text, in final-scale (1024) pixels."""
    asc, desc = font.getmetrics()
    return int((asc + desc) * leading) * n_lines // S


def draw_lines(d, x, y, lines, font, fill, leading=1.18):
    asc, desc = font.getmetrics()
    step = int((asc + desc) * leading)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += step
    return y


def centered(d, cx, y, text, font, fill):
    w_ = d.textlength(text, font=font)
    d.text((cx - w_ / 2, y), text, font=font, fill=fill)
    asc, desc = font.getmetrics()
    return y + asc + desc


def chip(d, x, y, text, color):
    f = F(SANS_B, 20)
    tw = d.textlength(text, font=f)
    pad_x, h = 13 * S, 32 * S
    d.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + h], radius=8 * S, fill=color)
    d.text((x + pad_x, y + 5 * S), text, font=f, fill=(255, 255, 255))
    return h


# ---------------------------------------------------------------- icons
def icon_satellite(d, cx, cy, r):
    w_ = 7 * S
    d.ellipse([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], outline=MUTE, width=4 * S)
    d.rounded_rectangle([cx - r * 0.22, cy - r * 0.34, cx + r * 0.22, cy + r * 0.3],
                        radius=8 * S, outline=INK, width=w_)
    for sgn in (-1, 1):
        x0 = cx + sgn * r * 0.3
        x1 = cx + sgn * r * 0.88
        d.rectangle([min(x0, x1), cy - r * 0.26, max(x0, x1), cy + r * 0.2],
                    outline=INK, width=w_ - 2 * S)
        mid = (x0 + x1) / 2
        d.line([mid, cy - r * 0.26, mid, cy + r * 0.2], fill=INK, width=w_ - 3 * S)
    d.arc([cx - r * 0.16, cy + r * 0.22, cx + r * 0.16, cy + r * 0.54],
          0, 180, fill=INK, width=w_ - 2 * S)
    sx, sy, sr = cx + r * 0.62, cy - r * 0.82, r * 0.17
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = sr if i % 2 == 0 else sr * 0.45
        pts.append((sx + rad * math.cos(ang), sy + rad * math.sin(ang)))
    d.polygon(pts, fill=RED)


def icon_chip_return(d, cx, cy, r):
    w_ = 7 * S
    box = [cx - r * 0.52, cy - r * 0.52, cx + r * 0.52, cy + r * 0.52]
    d.rounded_rectangle(box, radius=12 * S, outline=INK, width=w_)
    for i in range(3):
        off = -r * 0.3 + i * r * 0.3
        d.line([cx + off, cy - r * 0.52, cx + off, cy - r * 0.82], fill=INK, width=w_ - 2 * S)
        d.line([cx + off, cy + r * 0.52, cx + off, cy + r * 0.82], fill=INK, width=w_ - 2 * S)
        d.line([cx - r * 0.52, cy + off, cx - r * 0.82, cy + off], fill=INK, width=w_ - 2 * S)
        d.line([cx + r * 0.52, cy + off, cx + r * 0.82, cy + off], fill=INK, width=w_ - 2 * S)
    rr = r * 0.3
    d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 300, 200, fill=PURPLE, width=w_)
    ax, ay = cx + rr * 0.87, cy - rr * 0.5
    d.polygon([(ax + r * 0.16, ay - r * 0.02), (ax - r * 0.05, ay - r * 0.16),
               (ax - r * 0.02, ay + r * 0.14)], fill=PURPLE)


def icon_talk(d, cx, cy, r):
    w_ = 7 * S
    b1 = [cx - r * 0.95, cy - r * 0.72, cx + r * 0.18, cy + r * 0.18]
    d.rounded_rectangle(b1, radius=16 * S, outline=INK, width=w_)
    d.polygon([(cx - r * 0.6, cy + r * 0.16), (cx - r * 0.34, cy + r * 0.16),
               (cx - r * 0.58, cy + r * 0.5)], outline=INK, width=w_ - 2 * S)
    for i in range(2):
        yy = cy - r * 0.42 + i * r * 0.3
        d.line([cx - r * 0.72, yy, cx - r * 0.05, yy], fill=INK, width=w_ - 2 * S)
    b2 = [cx - r * 0.18, cy - r * 0.18, cx + r * 0.95, cy + r * 0.72]
    d.rounded_rectangle(b2, radius=16 * S, outline=GREEN, width=w_)
    d.polygon([(cx + r * 0.36, cy + r * 0.7), (cx + r * 0.6, cy + r * 0.7),
               (cx + r * 0.58, cy + r * 1.0)], outline=GREEN, width=w_ - 2 * S)
    for i in range(2):
        yy = cy + r * 0.1 + i * r * 0.3
        d.line([cx + r * 0.04, yy, cx + r * 0.72, yy], fill=GREEN, width=w_ - 2 * S)


def icon_drone(d, cx, cy, r):
    w_ = 7 * S
    # building sits lower and wider so the drone reads clearly above it
    bx0, by0, bx1, by1 = cx - r * 0.68, cy + r * 0.34, cx + r * 0.68, cy + r * 0.98
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=w_)
    for i in range(3):
        wx = bx0 + (i + 0.5) * (bx1 - bx0) / 3
        d.rectangle([wx - r * 0.09, cy + r * 0.54, wx + r * 0.09, cy + r * 0.74],
                    outline=INK, width=w_ - 3 * S)
    d.line([cx, by0, cx, cy + r * 0.02], fill=INK, width=w_ - 2 * S)
    d.polygon([(cx, cy + r * 0.02), (cx + r * 0.32, cy + r * 0.1),
               (cx, cy + r * 0.18)], fill=BLUE)
    dx_, dy_ = cx - r * 0.42, cy - r * 0.58
    d.line([dx_ - r * 0.3, dy_ - r * 0.18, dx_ + r * 0.3, dy_ + r * 0.18],
           fill=INK, width=w_ - 2 * S)
    d.line([dx_ - r * 0.3, dy_ + r * 0.18, dx_ + r * 0.3, dy_ - r * 0.18],
           fill=INK, width=w_ - 2 * S)
    for sx, sy in ((-0.3, -0.18), (0.3, -0.18), (-0.3, 0.18), (0.3, 0.18)):
        px, py = dx_ + sx * r, dy_ + sy * r
        d.ellipse([px - r * 0.13, py - r * 0.05, px + r * 0.13, py + r * 0.05],
                  outline=RED, width=4 * S)
    d.ellipse([dx_ - r * 0.09, dy_ - r * 0.09, dx_ + r * 0.09, dy_ + r * 0.09], fill=RED)


def icon_capitol(d, cx, cy, r):
    w_ = 7 * S
    base = cy + r * 0.78
    d.line([cx - r, base, cx + r, base], fill=INK, width=w_)
    for i in range(5):
        x = cx - r * 0.72 + i * r * 0.36
        d.line([x, cy + r * 0.28, x, base - 4 * S], fill=INK, width=w_ - 2 * S)
    d.line([cx - r * 0.88, cy + r * 0.28, cx + r * 0.88, cy + r * 0.28],
           fill=INK, width=w_)
    d.arc([cx - r * 0.55, cy - r * 0.62, cx + r * 0.55, cy + r * 0.3],
          180, 360, fill=INK, width=w_)
    d.line([cx - r * 0.55, cy - r * 0.16, cx + r * 0.55, cy - r * 0.16],
           fill=INK, width=w_ - 2 * S)
    d.line([cx, cy - r * 0.62, cx, cy - r * 0.92], fill=INK, width=w_)
    d.line([cx - r * 0.3, cy - r * 0.5, cx + r * 0.3, cy + r * 0.05], fill=RED, width=8 * S)
    d.line([cx - r * 0.3, cy + r * 0.05, cx + r * 0.3, cy - r * 0.5], fill=RED, width=8 * S)


# ---------------------------------------------------------------- content
LEAD = {
    "label": "LEAD STORY · SPACE DEFENCE",
    "color": NAVY,
    "headline": "NATO vows space defence over Russia nuclear satellite report",
    "caption": ("German media report Moscow plans a launch within weeks that could destroy "
                "satellites; the allies promise a joint defence of orbit."),
    "icon": icon_satellite,
}

PANELS = [
    {
        "label": "TECHNOLOGY · NVIDIA", "color": PURPLE,
        "headline": "Nvidia brings back Huang as CEO after Trump push",
        "caption": "Jensen Huang returns 11 days after quitting in a 'spy' row; shares jump 33% on the reversal.",
        "icon": icon_chip_return,
    },
    {
        "label": "WAR · UKRAINE", "color": GREEN,
        "headline": "Zelensky calls for four-way talks 'as soon as possible'",
        "caption": "Ukraine's president urges direct talks with Russia while strikes on the Kyiv region continue.",
        "icon": icon_talk,
    },
    {
        "label": "AFRICA · SUDAN", "color": DARKRED,
        "headline": "Drones hit homes and a UN building in Khartoum",
        "caption": "Strikes land in Sudan's capital as the civil war grinds on into another year.",
        "icon": icon_drone,
    },
    {
        "label": "UNITED STATES", "color": GOLD,
        "headline": "Congressman Gomez to resign after ethics findings",
        "caption": "The California Democrat steps down on 1 December after a House panel found evidence of sexual misconduct.",
        "icon": icon_capitol,
    },
]

TICKER = ("GTA VI hacker gets 7 years in London   •   "
          "More bodies recovered from Indonesia factory fire   •   "
          "Thousands march in Lisbon over living costs")


# ---------------------------------------------------------------- layout
def panel_h(d, p, text_w):
    hf, cf = F(SANS_B, 25), F(SANS, 19)
    nh = len(wrap(d, p["headline"], hf, text_w))
    nc = len(wrap(d, p["caption"], cf, text_w))
    return 14 + 32 + 10 + block_h(hf, nh, 1.12) + 4 + block_h(cf, nc, 1.22) + 14


def draw_panel(d, box, p):
    x0, y0, x1, y1 = [v * S for v in box]
    d.rounded_rectangle([x0, y0, x1, y1], radius=10 * S, fill=CARD, outline=INK, width=2 * S)
    chip(d, x0 + 16 * S, y0 + 14 * S, p["label"], p["color"])
    icon_r = 46 * S
    p["icon"](d, x1 - icon_r - 18 * S, y0 + 94 * S, icon_r)
    text_w = (x1 - x0) - 32 * S - (icon_r * 2 + 26 * S)
    hf, cf = F(SANS_B, 25), F(SANS, 19)
    y = y0 + 56 * S
    y = draw_lines(d, x0 + 16 * S, y, wrap(d, p["headline"], hf, text_w), hf, INK, 1.12)
    y += 4 * S
    draw_lines(d, x0 + 16 * S, y, wrap(d, p["caption"], cf, text_w), cf, (52, 52, 50), 1.22)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 34

    # masthead
    y = centered(d, W // 2, 14 * S,
                 "O N E   D A Y  ·  O N E   P I C T U R E  ·  T H E   W H O L E   W O R L D",
                 F(SANS_B, 19), MUTE)
    y = centered(d, W // 2, y + 2 * S, "TUESDAY 24 NOVEMBER 2026", F(SERIF_B, 62), RED)
    d.line([M * S, y + 2 * S, W - M * S, y + 2 * S], fill=INK, width=5 * S)
    d.line([M * S, y + 9 * S, W - M * S, y + 9 * S], fill=INK, width=2 * S)
    cur = (y + 20 * S) // S

    # lead story panel
    lead_text_w = (1024 - 2 * M - 40) * S - 235 * S
    hf, cf = F(SANS_B, 40), F(SANS, 22)
    nh = len(wrap(d, LEAD["headline"], hf, lead_text_w))
    nc = len(wrap(d, LEAD["caption"], cf, lead_text_w))
    lead_h = 16 + 32 + 12 + block_h(hf, nh, 1.1) + 6 + block_h(cf, nc, 1.22) + 14
    x0, y0, x1, y1 = M, cur, 1024 - M, cur + lead_h
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=10 * S,
                        fill=CARD, outline=INK, width=3 * S)
    chip(d, x0 * S + 18 * S, y0 * S + 16 * S, LEAD["label"], LEAD["color"])
    icon_satellite(d, x1 * S - 118 * S, y0 * S + (lead_h // 2 + 8) * S, 82 * S)
    yy = y0 * S + 60 * S
    yy = draw_lines(d, x0 * S + 18 * S, yy, wrap(d, LEAD["headline"], hf, lead_text_w), hf, INK, 1.1)
    yy += 6 * S
    draw_lines(d, x0 * S + 18 * S, yy, wrap(d, LEAD["caption"], cf, lead_text_w),
               cf, (52, 52, 50), 1.22)
    cur = y1 + 12

    # 2 x 2 grid, each row sized by its tallest panel
    gw = (1024 - 2 * M - 12) // 2
    text_w = gw * S - 32 * S - (88 * S + 26 * S)
    rows = [PANELS[:2], PANELS[2:]]
    for row in rows:
        rh = max(panel_h(d, p, text_w) for p in row)
        for i, p in enumerate(row):
            px = M + i * (gw + 12)
            draw_panel(d, [px, cur, px + gw, cur + rh], p)
        cur += rh + 12

    # ticker bar along the bottom
    tf = F(SANS, 22)
    n_t = len(wrap(d, TICKER, tf, (1024 - 2 * M - 36) * S))
    tick_h = 12 + 30 + 4 + block_h(tf, n_t, 1.25) + 12
    d.rectangle([M * S, cur * S, (1024 - M) * S, (cur + tick_h) * S], fill=INK)
    d.text(((M + 16) * S, (cur + 11) * S), "ALSO ON TUESDAY",
           font=F(SANS_B, 21), fill=(255, 205, 84))
    draw_lines(d, (M + 16) * S, (cur + 44) * S,
               wrap(d, TICKER, tf, (1024 - 2 * M - 36) * S), tf, (245, 242, 232), 1.25)
    cur += tick_h + 10

    # footer line
    centered(d, W // 2, cur * S,
             "Compiled from the day's reporting by SCMP, the Japan Times and the Manila Times  ·  Tuesday 24 November 2026",
             F(SANS_I, 18), MUTE)
    print(f"layout ends at y={cur + 26} of 1024")

    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
