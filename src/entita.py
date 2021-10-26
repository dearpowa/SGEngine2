from sgengine import utils
from sgengine.lifecycle import Node
import sgengine
import pygame

from sgengine.screen import Camera


class Player(Node):
    def start(self) -> None:
        self.sprite = pygame.image.load("assets/simpleguy_small.bmp")
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.movement_speed = 5
        self.camera_priority = -10
        self.solid = True
        self.camera = self.find_node_by_type(Camera)
        return super().start()

    def update(self) -> None:
        ev = sgengine.event_loop().get_current_events()

        for e in ev:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.movement_x[0] = True  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = True  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = True  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = True  # Giu
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.movement_x[0] = False  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = False  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = False  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = False  # Giu

        x = 0
        y = 0

        if not self.movement_x == [True, True]:
            if self.movement_x[0]:
                x = -self.movement_speed
            if self.movement_x[1]:
                x = +self.movement_speed

        if not self.movement_y == [True, True]:
            if self.movement_y[0]:
                y = -self.movement_speed
            if self.movement_y[1]:
                y = +self.movement_speed

        self.rect.move_ip(x, y)

        colliding, other = utils.is_colliding(self)

        if (colliding):
            self.rect.move_ip(-x, -y)

        self.camera.rect.center = self.rect.center

        return super().update()

class Tree(Node):
    def start(self) -> None:
        self.sprite = pygame.image.load("assets/simpletree.bmp")
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.solid = True
        return super().start()
