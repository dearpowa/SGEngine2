from pygame import Rect, Surface
import pygame
import sgengine
from sgengine.input import check_input
from sgengine.lifecycle import Node
from sgengine.utils import log

class PlayerController(Node):
    def start(self) -> None:
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.movement_speed = 1
        self.src_sprite: Surface = None
        self.rect = Rect(0, 0, 0, 0)
        self.flip_x = False
        self.flip_y = False
        return super().start()

    def set_sprite(self, sprite: Surface):
        self.src_sprite = sprite
        
        if sprite:
            self.rect = sprite.get_rect()

    def update(self) -> None:

        events = sgengine.event_loop().get_current_events()

        x = 0
        y = 0

        #left
        if check_input("left", events):
            self.movement_x[0] = True
        if check_input("left", events, pygame.KEYUP):
            self.movement_x[0] = False

        #right
        if check_input("right", events):
            self.movement_x[1] = True
        if check_input("right", events, pygame.KEYUP):
            self.movement_x[1] = False

        #up
        if check_input("up", events):
            self.movement_y[0] = True
        if check_input("up", events, pygame.KEYUP):
            self.movement_y[0] = False

        #down
        if check_input("down", events):
            self.movement_y[1] = True
        if check_input("down", events, pygame.KEYUP):
            self.movement_y[1] = False
        
        #log(self.movement_x)
        #log(self.movement_y)

        if self.movement_x != [True, True]:
            if self.movement_x[0]:
                x = -self.movement_speed
            if self.movement_x[1]:
                x = +self.movement_speed

        if self.movement_y != [True, True]:
            if self.movement_y[0]:
                y = -self.movement_speed
            if self.movement_y[1]:
                y = +self.movement_speed

        self.rect.move_ip(x, y)

        if x != 0:
            self.flip_x = x < 0


        self.sprite = pygame.transform.flip(self.src_sprite, self.flip_x, self.flip_y)

        return super().update()

