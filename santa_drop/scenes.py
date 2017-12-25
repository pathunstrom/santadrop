from ppb import BaseScene
from ppb import Vector
from pygame import display
from pygame.sprite import LayeredDirty

from santa_drop.controllers import Controller
from santa_drop.controllers import Spawner
from santa_drop.sprites import Chimney
from santa_drop.sprites import Santa
from santa_drop import resources

CHIMNEY_KEY = "chimney"
GIFTS_KEY = "gifts"
SANTA_KEY = "santa"


class Game(BaseScene):

    def __init__(self, engine):
        super().__init__(engine, background_color=(10, 21, 41))
        self.render_group = LayeredDirty()

        self.spawner = Spawner()
        Chimney(self, self.groups["chimney"])
        santa = Santa(self,
                      Vector(*self.engine.display.get_rect().center),
                      self.groups[GIFTS_KEY],
                      self.groups[SANTA_KEY])
        self.controller = Controller(actor=santa)
        channel = resources.sounds["santaclauseiscoming"].play(-1)
        channel.set_volume(0.1)

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
        self.spawner.resolve()
