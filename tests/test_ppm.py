from __future__ import annotations

from ray_tracer.core import RGB
from ray_tracer.io import image_to_ppm


def test_ppm_output() -> None:
    width = 3
    height = 2

    image = [[RGB(0, 0, 0) for _ in range(width)] for _ in range(height)]
    image[0][0] = RGB(1, 0, 0)
    image[0][1] = RGB(0, 1, 0)
    image[0][2] = RGB(0, 0, 1)

    image[1][0] = RGB(1, 1, 0)
    image[1][1] = RGB(1, 1, 1)
    image[1][2] = RGB(0, 0, 0)

    ppm = image_to_ppm(image)
    assert ppm == (
        "P3 3 2\n"
        "255\n"
        "255 0 0 0 255 0 0 0 255 \n"
        "255 255 0 255 255 255 0 0 0 \n"
    )
