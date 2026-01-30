from __future__ import annotations

import math

from ray_tracer.core import Material, Ray, Sphere, Vector


def test_sphere_intersections() -> None:
    sphere = Sphere(1, Vector(1, -2, 0), Material())

    # No intersection
    ray0 = Ray(origin=Vector(4, 0, 0), direction=Vector(-1, 0, 0))
    assert sphere.intersect(ray0) is None
    assert ray0.hit(sphere) is None

    # One intersection (tangent-ish)
    ray1 = Ray(origin=Vector(0, 0, -2), direction=Vector(0.000001, -1, 1))
    t1 = sphere.intersect(ray1)
    assert t1 is not None
    assert math.isclose(t1, math.sqrt(8), rel_tol=1e-2)

    hit1 = ray1.hit(sphere)
    assert hit1 is not None
    assert round(hit1.x) == 0
    assert math.floor(hit1.y) == -2
    assert round(hit1.z) == 0

    # Two intersections
    ray2 = Ray(origin=Vector(1, 0, 0), direction=Vector(0, -1, 0))
    t2 = sphere.intersect(ray2)
    assert t2 == 1
    assert ray2.hit(sphere) == Vector(1, -1, 0)

    normal = sphere.normal_at(ray2.hit(sphere))
    assert normal == Vector(0, 1, 0)
