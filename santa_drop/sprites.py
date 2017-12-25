from abc import ABC
from abc import abstractmethod
from enum import Enum
from os import path
from random import choice
from random import random as rand
from random import randint

from ppb import BaseScene
from ppb import Vector
import pygame.image as pgimage
from pygame.sprite import DirtySprite
from pygame.sprite import LayeredDirty
from pygame.transform import rotate

from santa_drop.util import scale
from santa_drop.controllers import Spawner
from santa_drop.resources import sprites

RESOURCES = path.join(path.dirname(__file__), "..", "resources")


# ABC

class Game(ABC):

    @property
    @abstractmethod
    def spawner(self) -> Spawner:
        pass


class Layers(Enum):
    BACKGROUND = -1
    GIFTS_BEHIND = 1
    CHIMNEY = 2
    HOUSES = 3
    GIFTS_IN_FRONT = 4
    SANTA = 0


class Chimney(DirtySprite):
    image = sprites["chimney"]

    def __init__(self, scene, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        display_rect = scene.engine.display.get_rect()
        self.rect.bottom = display_rect.bottom
        self.rect.left = display_rect.right
        self.position = Vector(*self.rect.center)
        self.layer = Layers.CHIMNEY.value

    def pre_draw(self):
        self.rect.center = tuple(self.position)

    def update(self, time_delta):
        self.position += Santa.speed * time_delta


class Gift(DirtySprite):

    sources = None

    def __init__(self, scene: BaseScene, spawn_position: Vector, *groups: LayeredDirty):
        super().__init__(*groups)
        self.scene = scene
        if type(self).sources is None:
            self.initialize_sprites()
        self.source_image = choice(self.sources)
        self._rotation = 0
        self.image = None
        self.rect = None
        self.set_image()
        self.position = spawn_position
        self.rect.center = tuple(self.position)
        self.layer = choice((Layers.GIFTS_BEHIND, Layers.GIFTS_IN_FRONT)).value

    @classmethod
    def initialize_sprites(cls):
        names = ["gift-green-yellow", "gift-red-green", "gift-yellow-red"]
        cls.sources = [sprites[name] for name in names]

    def pre_draw(self):
        self.set_image()
        self.rect.center = tuple(self.position)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value: int):
        if value >= 360:
            value -= 360
        if value <= 0:
            value += 360
        self._rotation = value

    def set_image(self):
        self.image = rotate(self.source_image, self.rotation)
        self.rect = self.image.get_rect()

    def update(self, time_delta):
        self.position += (Vector(0, 40) + Santa.speed) * time_delta
        self.rotation += randint(1, 3) * -1
        self.dirty = 1


class Santa(DirtySprite):

    limit = 50
    minimum = 25
    max_move = 1
    min_move = 0.5
    layer = Layers.SANTA.value
    drop_offset = Vector(0, 20)
    speed = Vector(-50, 0)

    def __init__(self, scene: Game, center_point: Vector, gift_group, *groups: LayeredDirty):
        # Sprite stuff
        super().__init__(*groups)
        self.image = sprites["santa"]
        self.image = scale(self.image, 2)
        self.rect = self.image.get_rect()
        self.rect.center = tuple(center_point)

        # Relationships
        self.scene = scene
        self.gift_group = gift_group

        # State
        self.anchor_point = center_point
        self.count_down = 0.5
        self.direction = Vector(0, -1)
        self.dirty = 1
        self.position = center_point
        self.throw_gift = False

    def activate(self):
        self.scene.spawner.spawn(Gift, self.scene, self.position + self.drop_offset, self.gift_group)

    def change_direction(self):
        self.direction *= -1
        self.count_down = rand() * (((self.max_move - self.min_move) + 1) + self.min_move)

    def pre_draw(self):
        pass

    def update(self, time_delta):
        self.count_down -= time_delta
        if self.count_down <= 0 or (self.position - self.anchor_point).length >= self.limit:
            self.change_direction()
        speed = randint(self.minimum, self.limit * 2)
        self.position += self.direction * speed * time_delta
        self.rect.center = tuple(self.position)
        self.dirty = 1

