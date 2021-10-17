import pygame
import sgengine
from sgengine.screen import Camera

camera = Camera()
camera.sprite = pygame.image.load("assets/simpleguy_small.bmp")
camera.sprite = pygame.transform.scale(camera.sprite, (200, 200))

sgengine.event_loop().add_child(camera)
sgengine.start()