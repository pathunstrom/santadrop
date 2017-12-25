import logging
from random import random as rand

from typing import Dict
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Type

from ppb import Vector
from pygame import K_SPACE
from pygame import key


class Controller:

    def __init__(self, actor):
        self.actor = actor
        self.pressed = False

    def respond(self):
        key_pressed = key.get_pressed()
        if not self.pressed and key_pressed[K_SPACE]:
            self.pressed = True
            self.actor.activate()
        if self.pressed and not key_pressed[K_SPACE]:
            self.pressed = False


class InfiniteObjectManager:

    min_wait = 1
    max_wait = 4

    def __init__(self, scene, game_object, group):
        self.scene = scene
        self.timer = 0
        self.active_objects = []
        self.inactive_objects = []
        self.GameObject: Type = game_object
        self.play_area = self.scene.engine.display.get_rect()
        self.group = group

    def cull_objects(self):
        for i, sprite in enumerate(self.active_objects[:]):
            if sprite.rect.right < self.play_area.left:
                sprite.deactivate()
                self.active_objects.pop(i)
                self.inactive_objects.append(sprite)

    def place_object(self):
        new_sprite = None
        if self.inactive_objects:
            new_sprite = self.inactive_objects.pop()
        new_sprite = new_sprite or self.GameObject(self.scene, self.group)
        new_sprite.activate()
        self.active_objects.append(new_sprite)
        logging.getLogger(type(self).__name__).debug(f"Total Objects: {len(self.active_objects) + len(self.inactive_objects)}")
        new_sprite.rect.left = self.play_area.right
        new_sprite.position = Vector(*new_sprite.rect.center)

    def reset_timer(self):
        self.timer = rand() * (self.max_wait - self.min_wait) + self.min_wait

    def resolve(self, time_delta: float):
        self.timer += -time_delta
        if self.timer <= 0:
            self.place_object()
            self.reset_timer()
        self.cull_objects()


class SpawnCommand(NamedTuple):
    type: Type
    args: Iterable
    kwargs: Dict


class Spawner:

    def __init__(self):
        self.spawn_commands: List[SpawnCommand] = []

    def spawn(self, cls: Type, *args, **kwargs):
        self.spawn_commands.append(SpawnCommand(cls, args, kwargs))

    def resolve(self, *_):
        commands = self.spawn_commands
        self.spawn_commands = []
        for c in commands:
            c.type(*c.args, **c.kwargs)
