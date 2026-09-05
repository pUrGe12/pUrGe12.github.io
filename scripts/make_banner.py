#!/usr/bin/env python3
"""Crop a picture into a post banner.

Takes the top band of the source image at the banner aspect ratio, scales it to
the target width and writes it to static/assets/banners/<slug>.jpg.

    python3 scripts/make_banner.py ~/Pictures/wallpaper.jpeg ocaml-tagged-integers

Then point the post at it in the front matter:

    [extra]
    banner = "assets/banners/ocaml-tagged-integers.jpg"

--offset shifts the band down when the very top of a picture is dead space
(an empty sky, a black margin); it is a fraction of the leftover height, so
0 is the top edge and 1 is the bottom.
"""

import argparse
import pathlib
import sys

from PIL import Image, ImageOps

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "static" / "assets" / "banners"


def parse_ratio(text):
    w, _, h = text.partition(":")
    try:
        ratio = float(w) / float(h)
    except (ValueError, ZeroDivisionError):
        raise argparse.ArgumentTypeError(f"expected W:H, got {text!r}")
    if ratio <= 0:
        raise argparse.ArgumentTypeError(f"expected a positive ratio, got {text!r}")
    return ratio


def make_banner(source, slug, ratio, width, offset, quality, out_dir=OUT_DIR):
    img = ImageOps.exif_transpose(Image.open(source)).convert("RGB")

    band = round(img.width / ratio)
    if band <= img.height:
        top = round((img.height - band) * offset)
        img = img.crop((0, top, img.width, top + band))
    else:
        # Source is already wider than the banner: trim the sides instead so we
        # keep full height rather than upscaling.
        band = round(img.height * ratio)
        left = round((img.width - band) / 2)
        img = img.crop((left, 0, left + band, img.height))

    if img.width != width:
        img = img.resize((width, round(width / ratio)), Image.LANCZOS)

    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{slug}.jpg"
    img.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)
    return dest, img.size


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", type=pathlib.Path, help="picture to crop")
    p.add_argument("slug", help="output name, without extension")
    p.add_argument("--ratio", type=parse_ratio, default="4:1", help="banner aspect ratio (default 4:1)")
    p.add_argument("--width", type=int, default=1600, help="output width in px (default 1600)")
    p.add_argument("--offset", type=float, default=0.0, help="0 = top edge (default), 1 = bottom edge")
    p.add_argument("--quality", type=int, default=88, help="JPEG quality (default 88)")
    p.add_argument("--out-dir", type=pathlib.Path, default=OUT_DIR,
                   help="where to write it (default static/assets/banners)")
    args = p.parse_args()

    if not args.source.is_file():
        sys.exit(f"no such file: {args.source}")
    if not 0.0 <= args.offset <= 1.0:
        sys.exit(f"--offset must be between 0 and 1, got {args.offset}")

    dest, size = make_banner(args.source, args.slug, args.ratio, args.width, args.offset,
                             args.quality, args.out_dir)
    try:
        rel = dest.resolve().relative_to(REPO / "static")
    except ValueError:
        rel = dest
    print(f'{dest}  {size[0]}x{size[1]}  {dest.stat().st_size // 1024} KB')
    print(f'front matter:  banner = "{rel}"')


if __name__ == "__main__":
    main()
