from logging import DEBUG

from ppb import GameEngine

from santa_drop.scenes import Game

with GameEngine(Game, resolution=(800, 800), log_level=DEBUG) as engine:
    engine.run()