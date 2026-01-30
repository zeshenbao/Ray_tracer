from __future__ import annotations

import math

import pytest

from ray_tracer.core import Vector


def test_vector_ops() -> None:
    v = Vector(1, 2, 3)
    u = Vector(1, -1, 0)
    n = Vector(0, 0, 0)

    assert v + v == Vector(2, 4, 6)
    assert v + n == v
    assert v - u == Vector(0, 3, 3)
    assert 2 * v == Vector(2, 4, 6)
    assert v * 2 == Vector(2, 4, 6)
    assert v * 0 == n

    assert v.dot(v) == 14
    assert v.dot(u) == -1
    assert n.dot(n) == 0

    assert math.isclose(v.length(), math.sqrt(14))
    assert n.length() == 0

    assert Vector(3, 0, 0).normalized() == Vector(1, 0, 0)


def test_normalize_zero_vector_raises() -> None:
    with pytest.raises(ValueError):
        Vector(0, 0, 0).normalized()
