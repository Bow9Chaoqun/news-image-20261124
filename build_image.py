#!/usr/bin/env python3
"""Render entry.png for the news-image-20261124 make.fun entry.

The picture is a one-page newspaper for Tuesday 24 November 2026.
Everything is drawn with Pillow on a canvas twice the final size and
then reduced, which keeps the lettering crisp at 1024 x 1024.

    python3 build_image.py        # writes ./entry.png

main.py is the graded program; it only copies the finished PNG.
"""

from dataclasses import dataclass
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SS = 2
FINAL = 1024
CANVAS = FINAL * SS
OUT = Path(__file__).with_name("entry.png")

BG = (248, 244, 232)
PANEL_BG = (255, 253, 246)
BODY = (24, 24, 28)
SOFT = (54, 54, 52)
GREY = (94, 94, 90)
CRIMSON = (179, 35, 42)
LEAF = (29, 111, 66)
SEA = (39, 65, 86)
WINE = (122, 31, 43)
OCHRE = (138, 90, 18)
VIOLET = (75, 46, 131)
SKY = (46, 96, 178)

FONT_ROOT = Path("/usr/share/fonts/truetype/liberation")
SERIF = FONT_ROOT / "LiberationSerif-Bold.ttf"
BOLD = FONT_ROOT / "LiberationSans-Bold.ttf"
REG = FONT_ROOT / "LiberationSans-Regular.ttf"
ITAL = FONT_ROOT / "LiberationSans-Italic.ttf"


def load(path, pt):
    return ImageFont.truetype(str(path), pt * SS)


def wrapped(draw, sentence, face, limit):
    out, line = [], ""
    for word in sentence.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=face) <= limit or line == "":
            line = trial
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def leading(face, ratio):
    a, b = face.getmetrics()
    return int((a + b) * ratio)


def stack_height(face, count, ratio=1.18):
    return leading(face, ratio) * count // SS


def paint_stack(draw, x, y, rows, face, colour, ratio=1.18):
    step = leading(face, ratio)
    for row in rows:
        draw.text((x, y), row, font=face, fill=colour)
        y += step
    return y


def centred(draw, y, sentence, face, colour):
    draw.text((CANVAS // 2, y), sentence, font=face, fill=colour, anchor="ma")
    a, b = face.getmetrics()
    return y + a + b


def pill(draw, x, y, wording, colour):
    face = load(BOLD, 20)
    width = draw.textlength(wording, font=face)
    draw.rounded_rectangle(
        [x, y, x + width + 26 * SS, y + 32 * SS],
        radius=8 * SS, fill=colour)
    draw.text((x + 13 * SS, y + 5 * SS), wording, font=face, fill=(255, 255, 255))


# ------------------------------------------------------------- pictograms
def pictogram_satellite(draw, cx, cy, rad):
    thick = 7 * SS
    draw.ellipse([cx - rad, cy - rad * 0.6, cx + rad, cy + rad * 0.6],
                 outline=GREY, width=4 * SS)
    draw.rounded_rectangle(
        [cx - rad * 0.2, cy - rad * 0.32, cx + rad * 0.2, cy + rad * 0.28],
        radius=8 * SS, outline=BODY, width=thick)
    for side in (-1, 1):
        near = cx + side * rad * 0.28
        far = cx + side * rad * 0.86
        left, right = min(near, far), max(near, far)
        draw.rectangle([left, cy - rad * 0.24, right, cy + rad * 0.18],
                       outline=BODY, width=thick - 2 * SS)
        draw.line([(near + far) / 2, cy - rad * 0.24,
                   (near + far) / 2, cy + rad * 0.18],
                  fill=BODY, width=thick - 3 * SS)
    draw.arc([cx - rad * 0.15, cy + rad * 0.2, cx + rad * 0.15, cy + rad * 0.5],
             0, 180, fill=BODY, width=thick - 2 * SS)
    star_x, star_y, star_r = cx + rad * 0.6, cy - rad * 0.8, rad * 0.16
    points = []
    for k in range(10):
        angle = -pi / 2 + k * pi / 5
        reach = star_r if k % 2 == 0 else star_r * 0.45
        points.append((star_x + reach * cos(angle), star_y + reach * sin(angle)))
    draw.polygon(points, fill=CRIMSON)


def pictogram_chip(draw, cx, cy, rad):
    thick = 7 * SS
    draw.rounded_rectangle(
        [cx - rad * 0.5, cy - rad * 0.5, cx + rad * 0.5, cy + rad * 0.5],
        radius=12 * SS, outline=BODY, width=thick)
    for k in range(3):
        shift = -rad * 0.3 + k * rad * 0.3
        draw.line([cx + shift, cy - rad * 0.5, cx + shift, cy - rad * 0.8],
                  fill=BODY, width=thick - 2 * SS)
        draw.line([cx + shift, cy + rad * 0.5, cx + shift, cy + rad * 0.8],
                  fill=BODY, width=thick - 2 * SS)
        draw.line([cx - rad * 0.5, cy + shift, cx - rad * 0.8, cy + shift],
                  fill=BODY, width=thick - 2 * SS)
        draw.line([cx + rad * 0.5, cy + shift, cx + rad * 0.8, cy + shift],
                  fill=BODY, width=thick - 2 * SS)
    ring = rad * 0.3
    draw.arc([cx - ring, cy - ring, cx + ring, cy + ring],
             300, 200, fill=VIOLET, width=thick)
    tip_x, tip_y = cx + ring * 0.87, cy - ring * 0.5
    draw.polygon([(tip_x + rad * 0.16, tip_y - rad * 0.02),
                  (tip_x - rad * 0.05, tip_y - rad * 0.16),
                  (tip_x - rad * 0.02, tip_y + rad * 0.14)], fill=VIOLET)


def pictogram_talks(draw, cx, cy, rad):
    thick = 7 * SS
    draw.rounded_rectangle(
        [cx - rad * 0.95, cy - rad * 0.72, cx + rad * 0.18, cy + rad * 0.18],
        radius=16 * SS, outline=BODY, width=thick)
    draw.polygon([(cx - rad * 0.6, cy + rad * 0.16), (cx - rad * 0.34, cy + rad * 0.16),
                  (cx - rad * 0.58, cy + rad * 0.5)], outline=BODY, width=thick - 2 * SS)
    for k in range(2):
        yy = cy - rad * 0.42 + k * rad * 0.3
        draw.line([cx - rad * 0.72, yy, cx - rad * 0.05, yy],
                  fill=BODY, width=thick - 2 * SS)
    draw.rounded_rectangle(
        [cx - rad * 0.18, cy - rad * 0.18, cx + rad * 0.95, cy + rad * 0.72],
        radius=16 * SS, outline=LEAF, width=thick)
    draw.polygon([(cx + rad * 0.36, cy + rad * 0.7), (cx + rad * 0.6, cy + rad * 0.7),
                  (cx + rad * 0.58, cy + rad * 1.0)], outline=LEAF, width=thick - 2 * SS)
    for k in range(2):
        yy = cy + rad * 0.1 + k * rad * 0.3
        draw.line([cx + rad * 0.04, yy, cx + rad * 0.72, yy],
                  fill=LEAF, width=thick - 2 * SS)


def pictogram_drone(draw, cx, cy, rad):
    thick = 7 * SS
    left_b = cx - rad * 0.68
    right_b = cx + rad * 0.68
    top_b = cy + rad * 0.34
    base_b = cy + rad * 0.98
    draw.rectangle([left_b, top_b, right_b, base_b], outline=BODY, width=thick)
    for k in range(3):
        mid = left_b + (k + 0.5) * (right_b - left_b) / 3
        draw.rectangle([mid - rad * 0.09, cy + rad * 0.54,
                        mid + rad * 0.09, cy + rad * 0.74],
                       outline=BODY, width=thick - 3 * SS)
    draw.line([cx, top_b, cx, cy + rad * 0.02], fill=BODY, width=thick - 2 * SS)
    draw.polygon([(cx, cy + rad * 0.02), (cx + rad * 0.32, cy + rad * 0.1),
                  (cx, cy + rad * 0.18)], fill=SKY)
    drone_x, drone_y = cx - rad * 0.42, cy - rad * 0.58
    draw.line([drone_x - rad * 0.3, drone_y - rad * 0.18,
               drone_x + rad * 0.3, drone_y + rad * 0.18],
              fill=BODY, width=thick - 2 * SS)
    draw.line([drone_x - rad * 0.3, drone_y + rad * 0.18,
               drone_x + rad * 0.3, drone_y - rad * 0.18],
              fill=BODY, width=thick - 2 * SS)
    for dx, dy in ((-0.3, -0.18), (0.3, -0.18), (-0.3, 0.18), (0.3, 0.18)):
        px, py = drone_x + dx * rad, drone_y + dy * rad
        draw.ellipse([px - rad * 0.13, py - rad * 0.05,
                      px + rad * 0.13, py + rad * 0.05],
                     outline=CRIMSON, width=4 * SS)
    draw.ellipse([drone_x - rad * 0.09, drone_y - rad * 0.09,
                  drone_x + rad * 0.09, drone_y + rad * 0.09], fill=CRIMSON)


def pictogram_capitol(draw, cx, cy, rad):
    thick = 7 * SS
    floor = cy + rad * 0.78
    draw.line([cx - rad, floor, cx + rad, floor], fill=BODY, width=thick)
    for k in range(5):
        xx = cx - rad * 0.72 + k * rad * 0.36
        draw.line([xx, cy + rad * 0.28, xx, floor - 4 * SS],
                  fill=BODY, width=thick - 2 * SS)
    draw.line([cx - rad * 0.88, cy + rad * 0.28, cx + rad * 0.88, cy + rad * 0.28],
              fill=BODY, width=thick)
    draw.arc([cx - rad * 0.55, cy - rad * 0.62, cx + rad * 0.55, cy + rad * 0.3],
             180, 360, fill=BODY, width=thick)
    draw.line([cx - rad * 0.55, cy - rad * 0.16, cx + rad * 0.55, cy - rad * 0.16],
              fill=BODY, width=thick - 2 * SS)
    draw.line([cx, cy - rad * 0.62, cx, cy - rad * 0.92], fill=BODY, width=thick)
    draw.line([cx - rad * 0.3, cy - rad * 0.5, cx + rad * 0.3, cy + rad * 0.05],
              fill=CRIMSON, width=8 * SS)
    draw.line([cx - rad * 0.3, cy + rad * 0.05, cx + rad * 0.3, cy - rad * 0.5],
              fill=CRIMSON, width=8 * SS)


# ------------------------------------------------------------- the stories
@dataclass
class Story:
    tag: str
    colour: tuple
    title: str
    detail: str
    draw_icon: object


LEAD_STORY = Story(
    tag="LEAD STORY · SPACE DEFENCE",
    colour=SEA,
    title="NATO vows space defence over Russia nuclear satellite report",
    detail=("German media report Moscow plans a launch within weeks that could "
            "destroy satellites; the allies promise a joint defence of orbit."),
    draw_icon=pictogram_satellite,
)

GRID_STORIES = [
    Story("TECHNOLOGY · NVIDIA", VIOLET,
          "Nvidia brings back Huang as CEO after Trump push",
          "Jensen Huang returns 11 days after quitting in a 'spy' row; "
          "shares jump 33% on the reversal.",
          pictogram_chip),
    Story("WAR · UKRAINE", LEAF,
          "Zelensky calls for four-way talks 'as soon as possible'",
          "Ukraine's president urges direct talks with Russia while "
          "strikes on the Kyiv region continue.",
          pictogram_talks),
    Story("AFRICA · SUDAN", WINE,
          "Drones hit homes and a UN building in Khartoum",
          "Strikes land in Sudan's capital as the civil war grinds "
          "on into another year.",
          pictogram_drone),
    Story("UNITED STATES", OCHRE,
          "Congressman Gomez to resign after ethics findings",
          "The California Democrat steps down on 1 December after a House "
          "panel found evidence of sexual misconduct.",
          pictogram_capitol),
]

BOTTOM_LINE = (
    "GTA VI hacker gets 7 years in London   •   "
    "More bodies recovered from Indonesia factory fire   •   "
    "Thousands march in Lisbon over living costs"
)


# ------------------------------------------------------------- page layout
def grid_panel_height(draw, story, text_width):
    head = load(BOLD, 25)
    body = load(REG, 19)
    title_rows = len(wrapped(draw, story.title, head, text_width))
    detail_rows = len(wrapped(draw, story.detail, body, text_width))
    return 14 + 32 + 10 + stack_height(head, title_rows, 1.12) + 4 \
        + stack_height(body, detail_rows, 1.22) + 14


def render_grid_panel(draw, box, story):
    x0, y0, x1, y1 = [v * SS for v in box]
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10 * SS,
                           fill=PANEL_BG, outline=BODY, width=2 * SS)
    pill(draw, x0 + 16 * SS, y0 + 14 * SS, story.tag, story.colour)
    icon_rad = 46 * SS
    story.draw_icon(draw, x1 - icon_rad - 18 * SS, y0 + 94 * SS, icon_rad)
    usable = (x1 - x0) - 32 * SS - (icon_rad * 2 + 26 * SS)
    head, body = load(BOLD, 25), load(REG, 19)
    cursor = y0 + 56 * SS
    cursor = paint_stack(draw, x0 + 16 * SS, cursor,
                         wrapped(draw, story.title, head, usable), head, BODY, 1.12)
    paint_stack(draw, x0 + 16 * SS, cursor + 4 * SS,
                wrapped(draw, story.detail, body, usable), body, SOFT, 1.22)


def build():
    page = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(page)
    margin = 34

    # masthead block
    top = centred(draw, 14 * SS,
                  "O N E   D A Y  ·  O N E   P I C T U R E  ·  T H E   W H O L E   W O R L D",
                  load(BOLD, 19), GREY)
    top = centred(draw, top + 2 * SS, "TUESDAY 24 NOVEMBER 2026",
                  load(SERIF, 62), CRIMSON)
    draw.line([margin * SS, top + 2 * SS, CANVAS - margin * SS, top + 2 * SS],
              fill=BODY, width=5 * SS)
    draw.line([margin * SS, top + 9 * SS, CANVAS - margin * SS, top + 9 * SS],
              fill=BODY, width=2 * SS)
    y_pos = (top + 20 * SS) // SS

    # lead panel, with the satellite pictogram on its right
    lead_head, lead_body = load(BOLD, 40), load(REG, 22)
    lead_width = (FINAL - 2 * margin - 40) * SS - 235 * SS
    title_rows = wrapped(draw, LEAD_STORY.title, lead_head, lead_width)
    detail_rows = wrapped(draw, LEAD_STORY.detail, lead_body, lead_width)
    lead_height = 16 + 32 + 12 + stack_height(lead_head, len(title_rows), 1.1) \
        + 6 + stack_height(lead_body, len(detail_rows), 1.22) + 14
    lx0, ly0 = margin, y_pos
    lx1, ly1 = FINAL - margin, y_pos + lead_height
    draw.rounded_rectangle([lx0 * SS, ly0 * SS, lx1 * SS, ly1 * SS],
                           radius=10 * SS, fill=PANEL_BG, outline=BODY, width=3 * SS)
    pill(draw, lx0 * SS + 18 * SS, ly0 * SS + 16 * SS,
         LEAD_STORY.tag, LEAD_STORY.colour)
    pictogram_satellite(draw, lx1 * SS - 118 * SS,
                        ly0 * SS + (lead_height // 2 + 8) * SS, 82 * SS)
    text_y = ly0 * SS + 60 * SS
    text_y = paint_stack(draw, lx0 * SS + 18 * SS, text_y,
                         title_rows, lead_head, BODY, 1.1)
    paint_stack(draw, lx0 * SS + 18 * SS, text_y + 6 * SS,
                detail_rows, lead_body, SOFT, 1.22)
    y_pos = ly1 + 12

    # four smaller stories in two rows of two
    col_width = (FINAL - 2 * margin - 12) // 2
    inner_width = col_width * SS - 32 * SS - (92 * SS + 26 * SS)
    for row_start in (0, 2):
        pair = GRID_STORIES[row_start:row_start + 2]
        row_height = max(grid_panel_height(draw, s, inner_width) for s in pair)
        for offset, story in enumerate(pair):
            left = margin + offset * (col_width + 12)
            render_grid_panel(draw, [left, y_pos, left + col_width,
                                     y_pos + row_height], story)
        y_pos += row_height + 12

    # black ticker strip with the day's shorter items in white
    ticker_face = load(REG, 22)
    ticker_rows = wrapped(draw, BOTTOM_LINE, ticker_face,
                          (FINAL - 2 * margin - 36) * SS)
    strip_height = 12 + 30 + 4 + stack_height(ticker_face, len(ticker_rows), 1.25) + 12
    draw.rectangle([margin * SS, y_pos * SS, (FINAL - margin) * SS,
                    (y_pos + strip_height) * SS], fill=BODY)
    draw.text(((margin + 16) * SS, (y_pos + 11) * SS), "ALSO ON TUESDAY",
              font=load(BOLD, 21), fill=(255, 205, 84))
    paint_stack(draw, (margin + 16) * SS, (y_pos + 44) * SS,
                ticker_rows, ticker_face, (245, 242, 232), 1.25)
    y_pos += strip_height + 10

    centred(draw, y_pos * SS,
            "Compiled from the day's reporting by SCMP, the Japan Times and "
            "the Manila Times  ·  Tuesday 24 November 2026",
            load(ITAL, 18), GREY)
    print(f"layout ends at y={y_pos + 26} of {FINAL}")

    page.resize((FINAL, FINAL), Image.LANCZOS).save(OUT, optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
