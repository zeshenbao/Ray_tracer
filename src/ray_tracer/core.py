from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Protocol, TypeAlias


@dataclass(frozen=True)
class Vector:
    """Simple 3D vector with basic linear algebra operations."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector":
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def length(self) -> float:
        return sqrt(self.dot(self))

    def normalized(self) -> "Vector":
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero-length vector")
        return Vector(self.x / length, self.y / length, self.z / length)

    def clamp(self, min_value: float = 0.0, max_value: float = 1.0) -> "Vector":
        return Vector(
            min(max(self.x, min_value), max_value),
            min(max(self.y, min_value), max_value),
            min(max(self.z, min_value), max_value),
        )

    def as_tuple(self) -> tuple[float, float, float]:
        return self.x, self.y, self.z


RGB: TypeAlias = Vector
Color: TypeAlias = Vector
Point: TypeAlias = Vector


def normalize_color(color: Vector) -> Vector:
    """Normalize 0-255 RGB input to 0-1 range when needed."""

    if max(color.x, color.y, color.z) > 1.0:
        return color * (1.0 / 255.0)
    return color


class MaterialLike(Protocol):
    ambient: float
    diffuse: float
    specular: float
    reflection: float

    def color_at(self, hit_pos: Vector) -> Vector:
        ...


@dataclass(frozen=True)
class Material:
    """Material properties for a surface."""

    color: RGB = RGB(255, 0, 0)
    ambient: float = 0.05
    diffuse: float = 1.0
    specular: float = 1.0
    reflection: float = 0.5

    def __post_init__(self) -> None:
        object.__setattr__(self, "color", normalize_color(self.color))

    def color_at(self, hit_pos: Vector) -> Vector:
        return self.color

    def get_color(self, hit_pos: Vector) -> Vector:
        return self.color_at(hit_pos)


@dataclass(frozen=True)
class Chessboard:
    """Checkerboard material using two alternating colors."""

    color1: RGB = RGB(255, 255, 255)
    color2: RGB = RGB(0, 0, 0)
    ambient: float = 0.0
    diffuse: float = 1.0
    specular: float = 1.0
    reflection: float = 0.5

    def __post_init__(self) -> None:
        object.__setattr__(self, "color1", normalize_color(self.color1))
        object.__setattr__(self, "color2", normalize_color(self.color2))

    def color_at(self, hit_pos: Vector) -> Vector:
        if int(hit_pos.x * 2.5) % 2 == int(hit_pos.z * 2.5) % 2:
            return self.color1
        return self.color2

    def get_color(self, hit_pos: Vector) -> Vector:
        return self.color_at(hit_pos)


@dataclass(frozen=True)
class Light:
    """Point light source."""

    position: Point = Point()
    color: RGB = RGB(255, 255, 255)

    def __post_init__(self) -> None:
        object.__setattr__(self, "color", normalize_color(self.color))


@dataclass
class Ray:
    """Ray with origin and normalized direction."""

    origin: Point
    direction: Vector

    def __post_init__(self) -> None:
        self.direction = self.direction.normalized()

    def at(self, t: float) -> Vector:
        return self.origin + self.direction * t

    def hit(self, sphere: "Sphere") -> Vector | None:
        t = sphere.intersect(self)
        if t is None:
            return None
        return self.at(t)


@dataclass
class Sphere:
    """Sphere geometry."""

    radius: float
    center: Point
    material: MaterialLike

    def intersect(self, ray: Ray) -> float | None:
        sphere_ray = ray.origin - self.center
        b = 2 * ray.direction.dot(sphere_ray)
        c = sphere_ray.dot(sphere_ray) - self.radius**2
        discriminant = b * b - 4 * c

        if discriminant < 0:
            return None

        if discriminant == 0:
            t = -b / 2
            return t if t > 0 else None

        sqrt_disc = sqrt(discriminant)
        t1 = (-b - sqrt_disc) / 2
        t2 = (-b + sqrt_disc) / 2
        candidates = [t for t in (t1, t2) if t > 0]
        return min(candidates) if candidates else None

    def normal_at(self, hit: Vector) -> Vector:
        return (hit - self.center).normalized()
