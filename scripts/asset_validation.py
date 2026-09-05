"""Maintainer-only checks for the package's passive SVG and RGBA PNG assets.

Pillow owns PNG decoding. This module enforces the narrower Servotab asset
contract; it is not a general SVG sanitizer or a browser-rendering substitute.
"""
from __future__ import annotations

import io
import math
import re
import struct
import warnings
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

MAX_ASSET_BYTES = 5 * 1024 * 1024
SVG_NS = "http://www.w3.org/2000/svg"
SVG_ELEMENTS = {"svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "title", "desc"}
SVG_ATTRIBUTES = {
    "width", "height", "viewBox", "role", "aria-label", "aria-labelledby",
    "shape-rendering", "id", "transform", "x", "y", "x1", "y1", "x2", "y2",
    "cx", "cy", "r", "rx", "ry", "d", "points", "fill", "fill-rule", "opacity",
    "fill-opacity", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin",
    "stroke-opacity", "preserveAspectRatio",
}
NUMBER = r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
LENGTH = re.compile(rf"({NUMBER})(?:px)?\Z")
PAINT = re.compile(r"(?:#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})|none|currentColor|transparent)\Z")


def asset_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError("asset must be a regular, non-symlink file")
    if path.stat().st_size > MAX_ASSET_BYTES:
        raise ValueError("asset exceeds the 5 MiB maintainer limit")
    return path.read_bytes()


def validate_png(path: Path, size: tuple[int, int]) -> list[str]:
    try:
        data = asset_bytes(path)
        if not data.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82"):
            raise ValueError("PNG must end at a complete IEND chunk")
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data), formats=["PNG"]) as image:
                if image.size != size or image.mode != "RGBA" or image.n_frames != 1:
                    raise ValueError(f"PNG must be a single-frame {size[0]} x {size[1]} 8-bit RGBA image")
                # Pillow may expose 16-bit RGBA as RGBA after conversion.
                if len(data) < 33 or data[12:16] != b"IHDR" or struct.unpack(">BB", data[24:26]) != (8, 6):
                    raise ValueError("PNG source must be 8-bit RGBA, without decoder conversion")
                image.verify()
            # verify checks the container; load also exercises the compressed pixels.
            with Image.open(io.BytesIO(data), formats=["PNG"]) as image:
                image.load()
        return []
    except (OSError, SyntaxError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        return [f"invalid PNG: {exc}"]


def validate_svg(path: Path) -> list[str]:
    try:
        text = asset_bytes(path).decode("utf-8")
        # Reject DTDs/entities and processing instructions before the XML parser.
        if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b|<\?(?!xml\s)", text, re.IGNORECASE):
            raise ValueError("SVG declarations and processing instructions are not allowed")
        root = ET.fromstring(text)
        if root.tag != f"{{{SVG_NS}}}svg":
            raise ValueError("asset must have an SVG namespace root")
        parts = re.split(r"[\s,]+", root.attrib.get("viewBox", "").strip())
        if len(parts) != 4 or any(not re.fullmatch(NUMBER, value) for value in parts):
            raise ValueError("SVG viewBox must contain four finite numbers")
        viewbox = [float(value) for value in parts]
        if not all(math.isfinite(value) for value in viewbox) or min(viewbox[2:]) < 48:
            raise ValueError("SVG viewBox must be finite and at least 48 x 48 pixels")
        for name in ("width", "height"):
            if name in root.attrib:
                match = LENGTH.fullmatch(root.attrib[name].strip())
                value = float(match.group(1)) if match else float("nan")
                if not math.isfinite(value) or value < 48:
                    raise ValueError("SVG explicit dimensions must be finite and at least 48 x 48 pixels")
        for node in root.iter():
            if node.tag not in {f"{{{SVG_NS}}}{name}" for name in SVG_ELEMENTS}:
                raise ValueError("SVG contains an element outside the passive geometry allowlist")
            for name, value in node.attrib.items():
                if name not in SVG_ATTRIBUTES:
                    raise ValueError(f"SVG attribute is not allowed: {name}")
                if name in {"fill", "stroke"} and not PAINT.fullmatch(value):
                    raise ValueError("SVG paint must be a literal color or none; resources are not allowed")
        return []
    except (OSError, UnicodeError, ValueError, ET.ParseError) as exc:
        return [f"invalid SVG: {exc}"]
