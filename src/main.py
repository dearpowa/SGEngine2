import pygame
import sgengine
from scenes import Scene1

sgengine.event_loop().add_child(Scene1())
sgengine.start()