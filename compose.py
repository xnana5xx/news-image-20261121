#!/usr/bin/env python3
"""Compose the front-page image for news-image-20261121.

Builds a 1024x1024 newspaper front page summing up Saturday
21 November 2026: masthead, date, hero illustration, and the five
biggest stories of the day, drawn with PIL so every headline stays
legible. Run: python3 compose.py  ->  assets/entry.png
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO = os.path.join(HERE, "assets",
                    "media-generation-news-hero-20261121-0-69e2016f-0adc-4835-a31d-5725e9009b41.webp")
OUT = os.path.join(HERE, "assets", "entry.png")

W, H = 1024, 1024
CREAM = (247, 242, 231)
NAVY = (22, 35, 63)
RED = (178, 34, 34)
INK = (26, 26, 26)
GREY = (90, 88, 80)

STORIES = [
    ("SUMMIT AFTERMATH",
     "Trump calls European allies on Ukraine",
     "A day after his Shenzhen talks with Putin and Xi, Trump dials into a meeting of Europe's leaders on the war."),
    ("UKRAINE",
     "Russia pounds Kyiv bridges; nine killed",
     "A massive aerial assault hits the capital; a strike on Kryvyi Rih kills two and wounds 42, four of them children."),
    ("CLIMATE",
     "COP31 talks deadlocked as deadline nears",
     "Negotiators struggle for consensus, with no agreement in sight at the crunch stage of the summit."),
    ("DENMARK",
     "Copenhagen accuses Russia of a murder plot",
     "Danish officials say Russian intelligence plotted to kill an American-Ukrainian on Danish soil."),
    ("BRAZIL",
     "Bolsonaro hospitalised with abdominal pain",
     "Brazil's former president is taken to hospital; no further details have been released."),
]


def find_font(bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def font(bold, size):
    path = find_font(bold)
    return ImageFont.truetype(path, size) if path else ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    page = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(page)

    # Masthead band.
    draw.rectangle([0, 0, W, 84], fill=NAVY)
    title = "THE WORLD IN ONE PAGE"
    tf = font(True, 52)
    draw.text(((W - draw.textlength(title, font=tf)) / 2, 14),
              title, font=tf, fill=(255, 255, 255))
    draw.rectangle([0, 84, W, 90], fill=RED)

    # Date line.
    date = "SATURDAY 21 NOVEMBER 2026"
    df = font(True, 34)
    draw.text(((W - draw.textlength(date, font=df)) / 2, 102),
              date, font=df, fill=NAVY)
    sub = "One day's world news, in one picture"
    sf = font(False, 22)
    draw.text(((W - draw.textlength(sub, font=sf)) / 2, 146),
              sub, font=sf, fill=GREY)

    # Hero illustration strip.
    hero = Image.open(HERO).convert("RGB")
    hw, hh = hero.size
    target_h = 200
    scale = W / hw
    hero = hero.resize((W, int(hh * scale)), Image.LANCZOS)
    top = int((hero.height - target_h) / 2)
    hero = hero.crop((0, top, W, top + target_h))
    page.paste(hero, (0, 182))
    draw.rectangle([0, 182, W, 184], fill=NAVY)
    draw.rectangle([0, 380, W, 382], fill=NAVY)

    # Story blocks.
    y = 396
    kf = font(True, 19)
    hf = font(True, 29)
    df2 = font(False, 20)
    for i, (kicker, headline, deck) in enumerate(STORIES):
        draw.text((48, y), f"{i + 1}.  {kicker}", font=kf, fill=RED)
        y += 26
        for line in wrap(draw, headline, hf, W - 96):
            draw.text((48, y), line, font=hf, fill=INK)
            y += 33
        for line in wrap(draw, deck, df2, W - 96):
            draw.text((48, y), line, font=df2, fill=GREY)
            y += 24
        y += 4
        if i < len(STORIES) - 1:
            draw.line([(48, y), (W - 48, y)], fill=(200, 192, 175), width=2)
            y += 10

    # Footer.
    foot = "Sources: AP · The Hindu · Manila Times · Reuters  —  21 November 2026"
    ff = font(False, 18)
    draw.text(((W - draw.textlength(foot, font=ff)) / 2, H - 30),
              foot, font=ff, fill=GREY)

    page.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {page.size} PNG {size} bytes")
    assert page.size[0] <= 1024 and page.size[1] <= 1024
    assert size <= 1048576, "image over 1 MiB"


if __name__ == "__main__":
    main()
