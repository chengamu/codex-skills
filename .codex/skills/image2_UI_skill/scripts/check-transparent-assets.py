#!/usr/bin/env python3
"""Check PNG transparency and report optional Pillow-based edge details.

This script verifies assets; it does not generate or modify images.
It intentionally uses the Python standard library first. If Pillow is
installed, it prints additional alpha and edge-fringe diagnostics.
"""

from __future__ import annotations

import argparse
import struct
import sys
from dataclasses import dataclass
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


COLOR_TYPES = {
    0: "grayscale",
    2: "truecolor",
    3: "indexed-color",
    4: "grayscale-alpha",
    6: "truecolor-alpha",
}


@dataclass
class PngInfo:
    path: Path
    width: int
    height: int
    bit_depth: int
    color_type: int
    has_alpha_channel: bool
    has_trns: bool

    @property
    def has_transparency_signal(self) -> bool:
        return self.has_alpha_channel or self.has_trns


def read_png_info(path: Path) -> PngInfo:
    with path.open("rb") as file:
        signature = file.read(8)
        if signature != PNG_SIGNATURE:
            raise ValueError("not a PNG file")

        width = height = bit_depth = color_type = None
        has_trns = False

        while True:
            raw_len = file.read(4)
            if len(raw_len) != 4:
                raise ValueError("unexpected end of file")
            chunk_len = struct.unpack(">I", raw_len)[0]
            chunk_type = file.read(4)
            chunk_data = file.read(chunk_len)
            file.read(4)  # CRC

            if chunk_type == b"IHDR":
                width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk_data[:10])
            elif chunk_type == b"tRNS":
                has_trns = True
            elif chunk_type == b"IEND":
                break

        if width is None or height is None or bit_depth is None or color_type is None:
            raise ValueError("missing IHDR chunk")

        return PngInfo(
            path=path,
            width=width,
            height=height,
            bit_depth=bit_depth,
            color_type=color_type,
            has_alpha_channel=color_type in (4, 6),
            has_trns=has_trns,
        )


def pillow_report(path: Path) -> list[str]:
    try:
        from PIL import Image
    except Exception:
        return ["pillow: unavailable"]

    lines: list[str] = []
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        alpha_min, alpha_max = alpha.getextrema()
        bbox = alpha.getbbox()
        total = rgba.width * rgba.height
        transparent = sum(1 for value in alpha.getdata() if value == 0)
        translucent = sum(1 for value in alpha.getdata() if 0 < value < 255)

        lines.append("pillow: available")
        lines.append(f"alpha_extrema: min={alpha_min}, max={alpha_max}")
        lines.append(f"transparent_pixels: {transparent}/{total}")
        lines.append(f"translucent_pixels: {translucent}/{total}")
        lines.append(f"nontransparent_bbox: {bbox}")

        if alpha_min == 255:
            lines.append("alpha_content: opaque-only")
        elif transparent == 0 and translucent > 0:
            lines.append("alpha_content: translucent-only")
        else:
            lines.append("alpha_content: contains-transparent-pixels")

        fringe = estimate_white_fringe(rgba)
        lines.append(f"edge_white_fringe_suspect_pixels: {fringe}")

    return lines


def estimate_white_fringe(rgba) -> int:
    pixels = rgba.load()
    width, height = rgba.size
    suspect = 0

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0 or a > 245:
                continue
            if r < 235 or g < 235 or b < 235:
                continue
            if has_nearby_transparent_pixel(pixels, width, height, x, y):
                suspect += 1

    return suspect


def has_nearby_transparent_pixel(pixels, width: int, height: int, x: int, y: int) -> bool:
    for ny in range(max(0, y - 1), min(height, y + 2)):
        for nx in range(max(0, x - 1), min(width, x + 2)):
            if nx == x and ny == y:
                continue
            if pixels[nx, ny][3] == 0:
                return True
    return False


def check_file(path: Path) -> int:
    print(f"file: {path}")
    try:
        info = read_png_info(path)
    except Exception as exc:
        print(f"status: error")
        print(f"error: {exc}")
        return 2

    color_name = COLOR_TYPES.get(info.color_type, f"unknown-{info.color_type}")
    print("status: ok")
    print(f"dimensions: {info.width}x{info.height}")
    print(f"bit_depth: {info.bit_depth}")
    print(f"color_type: {color_name}")
    print(f"alpha_channel: {str(info.has_alpha_channel).lower()}")
    print(f"trns_chunk: {str(info.has_trns).lower()}")
    print(f"transparency_signal: {str(info.has_transparency_signal).lower()}")

    for line in pillow_report(path):
        print(line)

    if not info.has_transparency_signal:
        print("result: no PNG alpha or tRNS transparency signal")
        return 1

    print("result: PNG transparency signal present")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check PNG alpha/transparency metadata.")
    parser.add_argument("files", nargs="+", help="PNG files to inspect")
    args = parser.parse_args(argv)

    worst = 0
    for index, raw_path in enumerate(args.files):
        if index:
            print("")
        code = check_file(Path(raw_path))
        worst = max(worst, code)

    return worst


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
