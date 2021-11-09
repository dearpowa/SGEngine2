from typing import Tuple
from sgengine import lifecycle
import pygame
import math

import sgengine


def create_line(origin: Tuple[float, float], lenght: float, angle: float) -> Tuple[Tuple[float], Tuple[float]]:
    return(origin, (origin[0] + (lenght * math.cos(math.radians(angle))), origin[1] + (lenght * math.sin(math.radians(angle)))))

def line_lenght(origin: Tuple[float, float], end: Tuple[float, float]) -> float:
    x1, y1 = origin
    x2, y2 = end
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

class FPSCounter(lifecycle.Node):

    def start(self) -> None:
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.text: pygame.Surface = None
        self.font = pygame.font.Font("assets/OpenSans-Regular.ttf", 30)
        return super().start()

    def update(self) -> None:
        fps = sgengine.event_loop().current_framerate
        frametime = sgengine.event_loop().current_frametime

        text = "fps: " + "{:.1f}".format(fps) + " frametime: " + "{:.1f}".format(frametime)

        self.text = self.font.render(text, True, (255, 255, 255))
        return super().update()