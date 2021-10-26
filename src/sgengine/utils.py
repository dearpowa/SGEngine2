from typing import Tuple
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
        self.text = self.font.render(
            "{:.1f}".format(fps), True, (255, 255, 255))
        return super().update()


def is_colliding(node: lifecycle.Node, check_self=False) -> Tuple[bool, lifecycle.Node]:
    if node.solid and node.rect != None:
        for other in sgengine.event_loop().alive_nodes():
            if other.id != node.id or check_self:
                if other.solid and other.rect != None and node.rect.colliderect(other.rect):
                    return True, other

    return False, None
