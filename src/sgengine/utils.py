from sgengine import lifecycle
import pygame

import sgengine


class FPSCounter(lifecycle.Node):
    
    def start(self) -> None:
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.text: pygame.Surface = None
        self.font = pygame.font.Font("assets/OpenSans-Regular.ttf", 30)
        return super().start()


    def update(self) -> None:
        fps = sgengine.event_loop().current_framerate
        self.text = self.font.render("{:.1f}".format(fps), True, (255, 255, 255))
        return super().update()