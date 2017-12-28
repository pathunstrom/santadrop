import logging

from ppb import BaseScene
from ppb import Vector
from pygame import display
from pygame.sprite import LayeredDirty
from pygame.sprite import groupcollide

import santa_drop.config as config
from santa_drop.controllers import Controller
from santa_drop.controllers import InfiniteObjectManager
from santa_drop.controllers import Spawner
from santa_drop.sprites import Chimney
from santa_drop.sprites import Santa
from santa_drop.sprites import Score
from santa_drop import resources


class Game(BaseScene):

    def __init__(self, engine):
        super().__init__(engine, background_color=(10, 21, 41))
        self.render_group = LayeredDirty()
        self.spawn_objects = [InfiniteObjectManager(self, Chimney, self.groups[config.KEY_CHIMNEY])]
        self.spawner = Spawner()
        self.spawn_objects.append(self.spawner)
        santa = Santa(self,
                      Vector(*self.engine.display.get_rect().center),
                      self.groups[config.KEY_GIFTS],
                      self.groups[config.KEY_SANTA])
        self.controller = Controller(actor=santa)
        channel = resources.sounds["santaclauseiscoming"].play(-1)
        channel.set_volume(0.1)
        self.score = 0
        Score(self, lambda: self.score, self.groups[config.KEY_UI])

    def render(self):
        window = display.get_surface()
        for group in self.groups.values():
            self.render_group.add(group.sprites())
        for sprite in self.render_group.sprites():
            self.render_group.change_layer(sprite, sprite.layer)
            sprite.pre_draw()
        return self.render_group.draw(window, self.background)

    def simulate(self, time_delta: float):
        self.controller.respond()
        super().simulate(time_delta)
        for spawn_object in self.spawn_objects:
            spawn_object.resolve(time_delta)
        collisions = groupcollide(self.groups[config.KEY_CHIMNEY], self.groups[config.KEY_GIFTS], False, False)
        successes = 0
        for chimney, gifts in collisions.items():
            for gift in gifts:
                if chimney.rect.left < gift.position.x < chimney.rect.right:
                    successes += 1
                    gift.kill()
        if successes:
            self.score += config.POINTS_GIFT_DELIVERED * successes
            logging.debug(f"{successes} Successes!")
