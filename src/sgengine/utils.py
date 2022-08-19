from typing import Tuple
from pygame import surface

from pygame.surface import Surface
import pygame
import math
from datetime import datetime

import sgengine
from sgengine.lifecycle import Node

def create_line(origin: Tuple[float, float], lenght: float, angle: float) -> Tuple[Tuple[float], Tuple[float]]:
    return(origin, (origin[0] + (lenght * math.cos(math.radians(angle))), origin[1] + (lenght * math.sin(math.radians(angle)))))

def line_lenght(origin: Tuple[float, float], end: Tuple[float, float]) -> float:
    x1, y1 = origin
    x2, y2 = end
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

def clear_surface(surf: Surface) -> None:
    surf.fill((0, 0, 0))

def make_transparent(surf: Surface) -> None:
    clear_surface(surf)
    surf.convert_alpha()
    surf.set_colorkey((0, 0, 0))

def log(log: str):
    print(f"[{datetime.now()}]: {log}")

class Text(Node):

    def start(self) -> None:
        self.text = ""
        self.sprite: pygame.Surface = None,
        self.__font_path: str = None
        self.__size: int = None
        self.__font: pygame.font.Font = None
        self.color = (255, 255, 255)
        self.aliased = True
        return super().start()

    def update(self) -> None:
        if self.__font is not None and self.color is not None:
            self.sprite = self.__font.render(self.text, self.aliased, self.color)
        return super().update()

    def set_font(self, font_path: str):
        self.__font_path = font_path
        self.__update_font()

    def set_size(self, size: int):
        self.__size = size
        self.__update_font()

    def __update_font(self):
        if self.__font_path is not None and self.__size is not None:
            self.__font = pygame.font.Font(self.__font_path, self.__size)

class UIText(Text):
    def start(self) -> None:
        super().start()
        self.render_type = sgengine.screen.RenderType.UI

class FPSCounter(UIText):

    def start(self) -> None:
        super().start()
        self.set_size(30)
        self.set_font("assets/OpenSans-Regular.ttf")

    def update(self) -> None:
        fps = sgengine.event_loop().current_framerate
        frametime = sgengine.event_loop().current_frametime

        self.text = "fps: " + "{:.1f}".format(fps) + " frametime: " + "{:.1f}".format(frametime)
        return super().update()