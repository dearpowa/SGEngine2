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

def line_rectangle_intersection(line_start, line_end, rectangle_start, rectangle_end):
    lx1, ly1 = line_start
    lx2, ly2 = line_end
    rx1, ry1 = rectangle_start
    rx2, ry2 = rectangle_end

    dx = lx2 - lx1
    dy = ly2 - ly1

    rx_min, rx_max = min(rx1, rx2), max(rx1, rx2)
    ry_min, ry_max = min(ry1, ry2), max(ry1, ry2)

    if dx == 0:
        # line is vertical
        if lx1 < rx_min or lx1 > rx_max:
            return None
        else:
            y = ly1 + dy * (rx_max - lx1) / dx
            if y >= ry_min and y <= ry_max:
                return (lx1, y)
            else:
                return None
    elif dy == 0:
        # line is horizontal
        if ly1 < ry_min or ly1 > ry_max:
            return None
        else:
            x = lx1 + dx * (ry_max - ly1) / dy
            if x >= rx_min and x <= rx_max:
                return (x, ly1)
            else:
                return None
    else:
        # line has slope
        k = dy / dx
        n = ly1 - k * lx1
        y = k * rx_min + n
        if y >= ry_min and y <= ry_max:
            return (rx_min, y)

        y = k * rx_max + n
        if y >= ry_min and y <= ry_max:
            return (rx_max, y)

        x = (ry_min - n) / k
        if x >= rx_min and x <= rx_max:
            return (x, ry_min)

        x = (ry_max - n) / k
        if x >= rx_min and x <= rx_max:
            return (x, ry_max)

    return None



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
        self.last_frame_time = 0

    def update(self) -> None:
        fps = sgengine.event_loop().current_framerate
        frametime = sgengine.event_loop().current_frametime

        if (self.last_frame_time == 0):
            self.last_frame_time = frametime

        avg_frame_time = (self.last_frame_time + frametime) / 2

        self.text = "fps: " + "{:.1f}".format(fps) + " frametime: " + "{:.1f}".format(frametime) + " avg frametime: " + "{:.0f}".format(avg_frame_time)

        self.last_frame_time = frametime
        return super().update()