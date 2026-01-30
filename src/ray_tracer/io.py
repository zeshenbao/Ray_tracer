from __future__ import annotations

from pathlib import Path

from .core import Color


def image_to_ppm(image: list[list[Color]]) -> str:
    if not image or not image[0]:
        raise ValueError("image must not be empty")

    height = len(image)
    width = len(image[0])
    lines = [f"P3 {width} {height}\n255\n"]

    for row in image:
        parts: list[str] = []
        for color in row:
            clamped = color.clamp(0.0, 1.0)
            r = round(clamped.x * 255)
            g = round(clamped.y * 255)
            b = round(clamped.z * 255)
            parts.append(f"{r} {g} {b} ")
        lines.append("".join(parts) + "\n")

    return "".join(lines)


def write_ppm(path: str | Path, image: list[list[Color]]) -> None:
    ppm_data = image_to_ppm(image)
    path_obj = Path(path)
    path_obj.write_text(ppm_data, encoding="utf-8")
