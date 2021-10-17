import pygame
import time
from typing import List

import sgengine


class Node:

    def __init__(self) -> None:
        self.position = (0, 0)
        self.parent = None
        self.childs = []
        self.id = time.time() * 1000
        #Se l'event loop è in creazione, deve accedere a se stesso direttamente
        if issubclass(type(self), EventLoop):
            self.add_alive_node(self)
        else:
            sgengine.event_loop().add_alive_node(self)


    def start(self) -> None:
        for child in self.childs:
            if issubclass(type(child), Node):
                child.start()
        pass

    def update(self) -> None:
        for child in self.childs:
            if issubclass(type(child), Node):
                child.update()
        pass

    def add_child(self, child) -> None:
        if issubclass(type(child), Node):
            child.parent = self
            child.start()
            self.childs.append(child)

    def remove_child(self, child) -> None:
        try:
            self.childs.remove(child)
            child.parent = None
        finally:
            pass

    def kill(self):
        if self.parent != None:
            self.parent.remove_child(self)
        EventLoop.remove_alive_node(self)
        


class EventLoop(Node):
    _instance = None

    @staticmethod
    def get_instance() -> 'EventLoop':
        if EventLoop._instance == None:
            EventLoop._instance = EventLoop()
        return EventLoop._instance

    def start(self) -> None:
        self.is_running = True

        super().start()
        while self.is_running:
            self.update()
            
    def update(self) -> None:
        self._current_events = pygame.event.get()
        return super().update()

    def stop(self) -> None:
        self.is_running = False

    def get_current_events(self) -> List:
        if not hasattr(self, "_current_events"):
            self._current_events = []
        return self._current_events

    def alive_nodes(self) -> List[Node]:
        if not hasattr(self, "_alive_nodes") or self._alive_nodes == None:
            self._alive_nodes = []
        return self._alive_nodes[:]

    def add_alive_node(self, node: Node) -> None:
        if not hasattr(self, "_alive_nodes") or self._alive_nodes == None:
            self._alive_nodes = []
        self._alive_nodes.append(node)

    def remove_alive_node(self, node: Node) -> None:
        if not hasattr(self, "_alive_nodes") or self._alive_nodes == None:
            self._alive_nodes = []
        self._alive_nodes.remove(node)