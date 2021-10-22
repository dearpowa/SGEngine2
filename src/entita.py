from sgengine.lifecycle import Node
import sgengine
import pygame

class Player(Node):
    def start(self) -> None:
        self.sprite = pygame.image.load("assets/simpleguy_small.bmp")
        self.sprite = pygame.transform.scale(self.sprite, (30, 30))
        self.sprite.set_colorkey((0,0,0))
        self.rect = self.sprite.get_rect()
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.movement_speed = 5
        return super().start()

    def update(self) -> None:
        ev = sgengine.event_loop().get_current_events()

        for e in ev:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.movement_x[0] = True #Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = True #Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = True #Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = True #Giu
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.movement_x[0] = False #Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = False #Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = False #Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = False #Giu

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

        print((x, y))

        self.rect = self.sprite.get_rect(top=self.rect.top, left=self.rect.left).move(x, y)

        return super().update()