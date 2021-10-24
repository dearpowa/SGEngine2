import pygame
from pygame import color
import sgengine
from sgengine.lifecycle import Node
from sgengine.screen import Camera
from entita import Player, Tree
from sgengine.utils import FPSCounter

class Scene1(Node):
    
    def start(self) -> None:
        self.add_child(Player())
        self.add_child(Camera())
        self.add_child(FPSCounter())

        self.tree1 = Tree()
        self.tree2 = Tree()
        self.tree3 = Tree()

        self.add_child(self.tree1)
        self.add_child(self.tree2)
        self.add_child(self.tree3)

        return super().start()

    def started(self) -> None:
        self.tree1.rect.move_ip(30, 50)
        self.tree2.rect.move_ip(60, 10)
        self.tree3.rect.move_ip(200, 150)
        return super().started()

    def update(self) -> None:

        for child in self.childs:
            if (issubclass(type(child), Tree)):
                print(child.rect)
        return super().update()