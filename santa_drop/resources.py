import logging
from os import path
from os import walk

import pygame
from pygame import image
from pygame import mixer

pygame.init()

sprites = {}
sounds = {}

RESOURCE_PATH = path.join(path.dirname(__file__), "..", "resources")

for dirpath, dirnames, filenames in walk(RESOURCE_PATH):
    dirname = dirpath.split(path.sep)[-1]
    if dirname == "images":
        func = image.load
        resource_dict = sprites
    elif dirname == "sounds":
        func = mixer.Sound
        resource_dict = sounds
    else:
        continue
    for filename in filenames:
        resource_dict[filename.split(".")[0]] = func(path.join(dirpath, filename))
