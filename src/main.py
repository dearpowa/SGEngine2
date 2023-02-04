import pygame
import sgengine
from scenes import Scene1, Scene2, Scene3

sgengine.init()
sgengine.event_loop().add_child(Scene2())
sgengine.start()