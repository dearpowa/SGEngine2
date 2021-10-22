import pygame
from pygame import color
import sgengine
from sgengine.lifecycle import Node
from sgengine.screen import Camera
from entita import Player

class Scene1(Node):
    
    def start(self) -> None:
        self.add_child(Player())
        self.add_child(Camera())
        self.font = pygame.font.Font("assets/OpenSans-Regular.ttf", 30)
        self.rect = None
        return super().start()

    def update(self) -> None:
        fps = sgengine.event_loop().current_framerate
        self.text = self.font.render("{:.1f}".format(fps), True, (255, 255, 255))
        self.rect = self.text.get_rect(top=0, left=0)

        return super().update()