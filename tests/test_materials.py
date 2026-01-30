from __future__ import annotations

from ray_tracer.core import Chessboard, Light, Material, Point, RGB, Vector


def test_material_color_normalization() -> None:
    material = Material(RGB(0, 123, 255))
    color = material.color_at(Vector(1, 2, 3))
    assert color == Vector(0, 123 / 255, 1)


def test_chessboard_colors() -> None:
    chess = Chessboard(RGB(0, 100, 0), RGB(0, 0, 100))
    assert chess.color_at(Vector(1, 1, 0)) == Vector(0, 100 / 255, 0)
    assert chess.color_at(Vector(2, 2, 0)) == Vector(0, 0, 100 / 255)


def test_light_color_normalization() -> None:
    light = Light(Point(1, 0, 1), RGB(255, 0, 0))
    assert light.position == Vector(1, 0, 1)
    assert light.color == Vector(1, 0, 0)
