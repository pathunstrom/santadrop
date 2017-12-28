from numbers import Number

from pygame import Surface
from pygame import transform


def scale(image: Surface, factor: Number) -> Surface:
    return transform.smoothscale(image, (int(image.get_width() * factor), int(image.get_height() * factor)))
