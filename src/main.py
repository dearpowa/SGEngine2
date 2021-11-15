import pygame
import sgengine
from scenes import Scene1, Scene2

sgengine.init()
sgengine.event_loop().add_child(Scene1())
sgengine.window_manager().resolution = (800, 600)
sgengine.start()