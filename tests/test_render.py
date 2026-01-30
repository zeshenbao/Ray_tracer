from __future__ import annotations

from ray_tracer.core import Light, Material, Point, RGB, Sphere, Vector
from ray_tracer.render import RenderConfig, Scene, render


def test_render_smoke() -> None:
    scene = Scene(
        camera=Vector(0, 0, -1),
        objects=[Sphere(0.5, Vector(0, 0, 1), Material(RGB(200, 50, 50)))],
        lights=[Light(Point(-1, -1, -2))],
    )
    config = RenderConfig(soft_shadow_radius=0, max_depth=1)

    image = render(scene, width=20, height=12, config=config)

    assert len(image) == 12
    assert len(image[0]) == 20

    non_black = sum(1 for row in image for color in row if color.length() > 0)
    assert non_black > 0
