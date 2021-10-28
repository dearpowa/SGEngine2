import pygame
from pygame import color
import sgengine
from sgengine.lifecycle import Node
from sgengine.physics import Gravity
from sgengine.screen import Camera
from entita import Player, Tree
from sgengine.utils import FPSCounter


class Scene1(Node):

    def start(self) -> None:
        self.player = Player()
        gravity = Gravity()
        self.add_child(self.player)
        self.add_child(Camera())
        self.add_child(FPSCounter())
        self.add_child(gravity)

        self.tree1 = Tree()
        self.tree2 = Tree()
        self.tree3 = Tree()

        self.add_child(self.tree1)
        self.add_child(self.tree2)
        self.add_child(self.tree3)

        return super().start()

    def started(self) -> None:
        self.tree1.rect.move_ip(30, 100)
        self.tree2.rect.move_ip(100, 10)
        self.tree3.rect.move_ip(500, 150)
        self.player.rect.move_ip(0, -500)
        return super().started()

    def update(self) -> None:
        return super().update()
