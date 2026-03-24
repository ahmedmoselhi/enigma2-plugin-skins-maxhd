#!/usr/bin/env python3
"""Resize Enigma2 icon sets to 1080p-friendly PNG canvases.

This script reads the legacy 100x60 palette PNG assets from the skin's
shared icon directories, scales each icon proportionally to fit inside a
189x123 transparent canvas, and writes the result back as RGBA PNG.
"""

from __future__ import annotations

import argparse
import binascii
import math
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
TARGET_SIZE = (150, 90)
DEFAULT_DIRS = (
    Path("usr/share/enigma2/cript"),
    Path("usr/share/enigma2/piconCrypt"),
    Path("usr/share/enigma2/piconProv"),
    Path("usr/share/enigma2/piconSat"),
)


@dataclass
class PNGImage:
    width: int
    height: int
    pixels: List[List[Tuple[int, int, int, int]]]


def iter_chunks(payload: bytes) -> Iterable[Tuple[bytes, bytes]]:
    offset = len(PNG_SIGNATURE)
    while offset < len(payload):
        length = struct.unpack(">I", payload[offset : offset + 4])[0]
        chunk_type = payload[offset + 4 : offset + 8]
        data = payload[offset + 8 : offset + 8 + length]
        yield chunk_type, data
        offset += 12 + length
        if chunk_type == b"IEND":
            break


def paeth_predictor(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def unfilter_scanlines(raw: bytes, width: int, height: int, bpp: int) -> List[bytes]:
    stride = width * bpp
    rows: List[bytes] = []
    pos = 0
    prev = bytearray(stride)
    for _ in range(height):
        filter_type = raw[pos]
        pos += 1
        current = bytearray(raw[pos : pos + stride])
        pos += stride
        if filter_type == 0:
            pass
        elif filter_type == 1:
            for i in range(stride):
                left = current[i - bpp] if i >= bpp else 0
                current[i] = (current[i] + left) & 0xFF
        elif filter_type == 2:
            for i in range(stride):
                current[i] = (current[i] + prev[i]) & 0xFF
        elif filter_type == 3:
            for i in range(stride):
                left = current[i - bpp] if i >= bpp else 0
                up = prev[i]
                current[i] = (current[i] + ((left + up) // 2)) & 0xFF
        elif filter_type == 4:
            for i in range(stride):
                left = current[i - bpp] if i >= bpp else 0
                up = prev[i]
                up_left = prev[i - bpp] if i >= bpp else 0
                current[i] = (current[i] + paeth_predictor(left, up, up_left)) & 0xFF
        else:
            raise ValueError(f"Unsupported PNG filter {filter_type}")
        rows.append(bytes(current))
        prev = current
    return rows


def decode_png(path: Path) -> PNGImage:
    payload = path.read_bytes()
    if not payload.startswith(PNG_SIGNATURE):
        raise ValueError(f"{path} is not a PNG file")

    width = height = bit_depth = color_type = interlace = None
    palette: List[Tuple[int, int, int]] = []
    alpha_table: List[int] = []
    idat_parts: List[bytes] = []

    for chunk_type, data in iter_chunks(payload):
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, _comp, _filter, interlace = struct.unpack(">IIBBBBB", data)
        elif chunk_type == b"PLTE":
            palette = [tuple(data[i : i + 3]) for i in range(0, len(data), 3)]
        elif chunk_type == b"tRNS":
            alpha_table = list(data)
        elif chunk_type == b"IDAT":
            idat_parts.append(data)
        elif chunk_type == b"IEND":
            break

    if None in {width, height, bit_depth, color_type, interlace}:
        raise ValueError(f"{path} is missing IHDR metadata")
    if bit_depth != 8:
        raise ValueError(f"{path} must use 8-bit channels, got bit_depth={bit_depth}")
    if interlace != 0:
        raise ValueError(f"{path} uses unsupported interlace method {interlace}")

    raw = zlib.decompress(b"".join(idat_parts))
    if color_type == 3:
        alpha_table.extend([255] * (len(palette) - len(alpha_table)))
        rows = unfilter_scanlines(raw, width, height, 1)
        pixels = []
        for row in rows:
            pixel_row = []
            for index in row:
                r, g, b = palette[index]
                a = alpha_table[index]
                pixel_row.append((r, g, b, a))
            pixels.append(pixel_row)
    elif color_type == 6:
        rows = unfilter_scanlines(raw, width, height, 4)
        pixels = []
        for row in rows:
            pixel_row = []
            for offset in range(0, len(row), 4):
                pixel_row.append(tuple(row[offset : offset + 4]))
            pixels.append(pixel_row)
    elif color_type == 2:
        rows = unfilter_scanlines(raw, width, height, 3)
        pixels = []
        for row in rows:
            pixel_row = []
            for offset in range(0, len(row), 3):
                pixel_row.append(tuple(row[offset : offset + 3]) + (255,))
            pixels.append(pixel_row)
    else:
        raise ValueError(f"{path} must be indexed, RGB, or RGBA PNG, got color_type={color_type}")
    return PNGImage(width, height, pixels)


def premultiply(pixel: Tuple[int, int, int, int]) -> Tuple[float, float, float, float]:
    r, g, b, a = pixel
    alpha = a / 255.0
    return r * alpha, g * alpha, b * alpha, alpha


def clamp_channel(value: float) -> int:
    return max(0, min(255, int(round(value))))


def resize_rgba(image: PNGImage, target_width: int, target_height: int) -> PNGImage:
    if image.width == target_width and image.height == target_height:
        return image

    src = image.pixels
    dst: List[List[Tuple[int, int, int, int]]] = []
    x_scale = image.width / target_width
    y_scale = image.height / target_height

    for y in range(target_height):
        src_y = (y + 0.5) * y_scale - 0.5
        y0 = max(0, min(image.height - 1, int(math.floor(src_y))))
        y1 = max(0, min(image.height - 1, y0 + 1))
        wy = src_y - y0
        row = []
        for x in range(target_width):
            src_x = (x + 0.5) * x_scale - 0.5
            x0 = max(0, min(image.width - 1, int(math.floor(src_x))))
            x1 = max(0, min(image.width - 1, x0 + 1))
            wx = src_x - x0

            p00 = premultiply(src[y0][x0])
            p10 = premultiply(src[y0][x1])
            p01 = premultiply(src[y1][x0])
            p11 = premultiply(src[y1][x1])

            top = tuple(p00[i] * (1.0 - wx) + p10[i] * wx for i in range(4))
            bottom = tuple(p01[i] * (1.0 - wx) + p11[i] * wx for i in range(4))
            value = tuple(top[i] * (1.0 - wy) + bottom[i] * wy for i in range(4))
            alpha = max(0.0, min(1.0, value[3]))
            if alpha == 0:
                row.append((0, 0, 0, 0))
            else:
                row.append(
                    (
                        clamp_channel(value[0] / alpha),
                        clamp_channel(value[1] / alpha),
                        clamp_channel(value[2] / alpha),
                        clamp_channel(alpha * 255.0),
                    )
                )
        dst.append(row)
    return PNGImage(target_width, target_height, dst)


def fit_to_canvas(image: PNGImage, canvas_width: int, canvas_height: int) -> PNGImage:
    scale = min(canvas_width / image.width, canvas_height / image.height)
    scaled_width = max(1, int(round(image.width * scale)))
    scaled_height = max(1, int(round(image.height * scale)))
    resized = resize_rgba(image, scaled_width, scaled_height)

    pixels = [[(0, 0, 0, 0) for _ in range(canvas_width)] for _ in range(canvas_height)]
    offset_x = (canvas_width - scaled_width) // 2
    offset_y = (canvas_height - scaled_height) // 2
    for y in range(scaled_height):
        for x in range(scaled_width):
            pixels[offset_y + y][offset_x + x] = resized.pixels[y][x]
    return PNGImage(canvas_width, canvas_height, pixels)


def encode_rgba_png(image: PNGImage) -> bytes:
    raw_rows = []
    for row in image.pixels:
        raw_rows.append(b"\x00" + bytes(channel for pixel in row for channel in pixel))
    compressed = zlib.compress(b"".join(raw_rows), level=9)

    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        crc = binascii.crc32(chunk_type)
        crc = binascii.crc32(data, crc) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", image.width, image.height, 8, 6, 0, 0, 0)
    return PNG_SIGNATURE + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def resize_file(path: Path, target_size: Sequence[int]) -> None:
    source = decode_png(path)
    converted = fit_to_canvas(source, target_size[0], target_size[1])
    path.write_bytes(encode_rgba_png(converted))


def process_directories(directories: Iterable[Path], target_size: Sequence[int]) -> List[Path]:
    updated: List[Path] = []
    for directory in directories:
        for path in sorted(directory.glob("*.png")):
            resize_file(path, target_size)
            updated.append(path)
    return updated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs="*", type=Path, default=DEFAULT_DIRS)
    parser.add_argument("--width", type=int, default=TARGET_SIZE[0])
    parser.add_argument("--height", type=int, default=TARGET_SIZE[1])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    updated = process_directories(args.directories, (args.width, args.height))
    print(f"Updated {len(updated)} PNG files to {args.width}x{args.height} canvases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
