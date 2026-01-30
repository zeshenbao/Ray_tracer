from __future__ import annotations

from dataclasses import dataclass

from .core import Color, Light, Point, Ray, RGB, Sphere, normalize_color


@dataclass(frozen=True)
class Scene:
    camera: Point
    objects: list[Sphere]
    lights: list[Light]
    background: Color = RGB(0, 0, 0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "background", normalize_color(self.background))


@dataclass(frozen=True)
class RenderConfig:
    max_depth: int = 5
    specular_power: float = 50.0
    light_intensity: float = 4.0
    reflection_bias: float = 0.0001
    ambient_light: Color = RGB(0.2, 0.24, 0.82)
    soft_shadow_radius: int = 5
    soft_shadow_intensity: float = 3.0
    soft_shadow_gamma: float = 1.0


def render(scene: Scene, width: int, height: int, config: RenderConfig | None = None) -> list[list[Color]]:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if not scene.objects or not scene.lights:
        return _blank_image(width, height, scene.background)

    config = config or RenderConfig()
    image = _blank_image(width, height, scene.background)

    ratio = height / width
    x0, x1 = -1.0, 1.0
    y0, y1 = -ratio, ratio
    x_step = (x1 - x0) / width
    y_step = (y1 - y0) / height

    for light in scene.lights:
        light_buffer = _blank_image(width, height, RGB(0, 0, 0))
        shadow_cache = [set() for _ in scene.objects]
        light_cache = [set() for _ in scene.objects]

        for j in range(width):
            x = x0 + (j + 1) * x_step
            for i in range(height):
                y = y0 + (i + 1) * y_step
                direction = Point(x, y) - scene.camera
                ray = Ray(origin=scene.camera, direction=direction)
                color = trace_ray(
                    ray=ray,
                    scene=scene,
                    light=light,
                    config=config,
                    depth=0,
                    pixel=(i, j),
                    shadow_cache=shadow_cache,
                    light_cache=light_cache,
                )
                light_buffer[i][j] = color

        if config.soft_shadow_radius > 0:
            _apply_soft_shadows(
                light_buffer,
                shadow_cache,
                light_cache,
                width,
                height,
                config,
            )

        for i in range(height):
            row = image[i]
            light_row = light_buffer[i]
            for j in range(width):
                row[j] = row[j] + light_row[j]

    return image


def trace_ray(
    *,
    ray: Ray,
    scene: Scene,
    light: Light,
    config: RenderConfig,
    depth: int,
    pixel: tuple[int, int] | None,
    shadow_cache: list[set[tuple[int, int]]] | None,
    light_cache: list[set[tuple[int, int]]] | None,
) -> Color:
    obj_hit = None
    min_t = None
    obj_index = None

    for idx, obj in enumerate(scene.objects):
        t = obj.intersect(ray)
        if t is None:
            continue
        if min_t is None or t < min_t:
            min_t = t
            obj_hit = obj
            obj_index = idx

    if obj_hit is None or min_t is None:
        return scene.background

    hit_pos = ray.at(min_t)

    to_light = light.position - hit_pos
    shadow_ray = Ray(origin=hit_pos, direction=to_light)
    in_shadow = False

    for obj in scene.objects:
        if obj is obj_hit:
            continue
        block_t = obj.intersect(shadow_ray)
        if block_t is None:
            continue
        block_point = shadow_ray.at(block_t)
        if (block_point - hit_pos).length() < to_light.length():
            in_shadow = True
            break

    if depth == 0 and pixel is not None and obj_index is not None:
        if in_shadow and shadow_cache is not None:
            shadow_cache[obj_index].add(pixel)
        elif light_cache is not None:
            light_cache[obj_index].add(pixel)

    if in_shadow:
        return scene.background

    normal = obj_hit.normal_at(hit_pos)
    view_dir = (scene.camera - hit_pos).normalized()

    material = obj_hit.material
    ambient = material.ambient * config.ambient_light

    distance = to_light.length()
    light_dir = shadow_ray.direction
    attenuation = config.light_intensity / distance

    diffuse = (
        max(0.0, normal.dot(light_dir))
        * material.diffuse
        * material.color_at(hit_pos)
        * attenuation
    )

    half_vec = (view_dir + light_dir).normalized()
    specular = (
        max(0.0, normal.dot(half_vec)) ** config.specular_power
        * material.specular
        * light.color
        * attenuation
    )

    color = ambient + diffuse + specular

    if depth < config.max_depth and material.reflection > 0:
        reflected_origin = hit_pos + normal * config.reflection_bias
        reflected_dir = ray.direction - normal * (2 * ray.direction.dot(normal))
        reflected_ray = Ray(origin=reflected_origin, direction=reflected_dir)
        color = color + (
            trace_ray(
                ray=reflected_ray,
                scene=scene,
                light=light,
                config=config,
                depth=depth + 1,
                pixel=None,
                shadow_cache=None,
                light_cache=None,
            )
            * material.reflection
        )

    return color


def _apply_soft_shadows(
    buffer: list[list[Color]],
    shadow_cache: list[set[tuple[int, int]]],
    light_cache: list[set[tuple[int, int]]],
    width: int,
    height: int,
    config: RenderConfig,
) -> None:
    area = config.soft_shadow_radius
    if area <= 0:
        return

    for obj_idx in range(len(shadow_cache)):
        if not shadow_cache[obj_idx]:
            continue

        shadow_pixels = shadow_cache[obj_idx]
        light_pixels = light_cache[obj_idx]

        for i, j in shadow_pixels:
            visible = 0
            total = 0
            for di in range(-area, area + 1):
                for dj in range(-area, area + 1):
                    ni = i + di
                    nj = j + dj
                    if ni < 0 or nj < 0 or ni >= height or nj >= width:
                        continue
                    if (ni, nj) in light_pixels:
                        visible += 1
                        total += 1
                    elif (ni, nj) in shadow_pixels:
                        total += 1

            if total == 0:
                continue

            factor = (visible / total) ** config.soft_shadow_gamma
            buffer[i][j] = buffer[i][j] * (factor * config.soft_shadow_intensity)


def _blank_image(width: int, height: int, fill: Color) -> list[list[Color]]:
    return [[fill for _ in range(width)] for _ in range(height)]
