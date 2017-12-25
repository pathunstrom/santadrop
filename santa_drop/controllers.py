from typing import Dict
from typing import Iterable
from typing import List
from typing import NamedTuple
from typing import Type

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

    def __init__(self, scene):
        self.scene = scene


class SpawnCommand(NamedTuple):
    type: Type
    args: Iterable
    kwargs: Dict


class Spawner:

    def __init__(self):
        self.spawn_commands: List[SpawnCommand] = []

    def spawn(self, cls: Type, *args, **kwargs):
        self.spawn_commands.append(SpawnCommand(cls, args, kwargs))

    def resolve(self):
        commands = self.spawn_commands
        self.spawn_commands = []
        for c in commands:
            c.type(*c.args, **c.kwargs)
