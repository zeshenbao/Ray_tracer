from __future__ import annotations

import argparse
from pathlib import Path

from .core import Chessboard, Light, Material, Point, RGB, Sphere, Vector
from .io import write_ppm
from .render import RenderConfig, Scene, render


def build_demo_scene() -> Scene:
    camera = Vector(0, -0.35, -1.0)

    objects = [
        Sphere(0.6, Vector(1.25, -0.1, 1), Material(RGB(0, 100, 0))),
        Sphere(0.4, Vector(-0.25, -0.1, 1.5), Material()),
        Sphere(0.2, Vector(0.6, 0.1, 1.5), Material(RGB(0, 0, 100))),
        Sphere(0.8, Vector(-1.25, -0.6, 2), Material(RGB(0, 50, 50), 0, 0.5, 0.3, 0.01)),
        Sphere(
            10000,
            Vector(0, 10000.5, 1),
            Chessboard(RGB(255, 255, 255), RGB(0, 0, 0), 0, 1.0, 1.0, 0.2),
        ),
    ]

    lights = [Light(Point(-2, -0.5, -2)), Light(Point(1, -1.5, -2))]

    return Scene(camera=camera, objects=objects, lights=lights)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Static ray tracer demo scene")
    parser.add_argument("--width", type=int, default=320, help="Output image width")
    parser.add_argument("--height", type=int, default=200, help="Output image height")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("render.ppm"),
        help="Output PPM file path",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=5,
        help="Max reflection recursion depth",
    )
    parser.add_argument(
        "--soft-shadow-radius",
        type=int,
        default=5,
        help="Soft shadow sampling radius (0 disables)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    scene = build_demo_scene()
    config = RenderConfig(
        max_depth=args.max_depth,
        soft_shadow_radius=max(0, args.soft_shadow_radius),
    )

    image = render(scene, args.width, args.height, config)
    write_ppm(args.output, image)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
