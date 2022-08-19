import random
import uuid
from threading import Thread
import pygame
import time
from typing import ClassVar, List, Type
import sgengine

class Node:

    def __init__(self, parent: 'Node'=None) -> None:
        self.position = (0, 0)
        self.parent: 'Node' = None
        self.childs: List['Node'] = []
        self.id = str(uuid.uuid4())
        self.render_type = sgengine.screen.RenderType.SPACE
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.solid = False
        self.camera_priority = 0
        self.gravity_settings = physics.GravitySettings()
        self.on_start: function = None
        self.on_update: function = None
        self.on_kill: function = None
        # Se l'event loop è in creazione, deve accedere a se stesso direttamente
        if issubclass(type(self), EventLoop):
            self.add_alive_node(self)
        else:
            sgengine.event_loop().add_alive_node(self)
        if parent:
            parent.add_child(self, True)

    def start(self) -> None:
        for child in self.childs:
            if issubclass(type(child), Node):
                child.start()
        self.started()
        if self.on_start:
            self.on_start()

    def started(self) -> None:
        pass

    def update(self) -> None:
        for child in self.childs:
            if issubclass(type(child), Node):
                # Se il figlio non è vivo provo a eliminarlo di nuovo
                if child.is_alive():
                    child.update()
                else:
                    child.kill()
            else:
                # Se il figlio non è un nodo lo rimuovo
                self.remove_child(child)

        if self.on_update:
            self.on_update()
        pass

    """
    Aggiunge un figlio al nodo
    ritorna se il processo è andato a buon fine
    """
    def add_child(self, child: 'Node', trigger_start=False) -> bool:
        if issubclass(type(child), Node):
            child.parent = self
            if trigger_start:
                child.start()
            self.childs.append(child)
            return True
        else:
            return False

    """
    Rimuove un figlio dal nodo
    ritorna se il processo è andato a buon fine
    """
    def remove_child(self, child: 'Node') -> bool:
        try:
            self.childs.remove(child)
            child.parent = None
            return True
        except:
            return False

    """
    Sostituisco un figlio con uno nuovo, quello vecchio viene anche eliminato dalla lista dei nodi vivi
    ritorna se il processo è andato a buon fine
    """
    def substitute_child(self, child: 'Node', new_child: 'Node') -> bool:
        return child.kill() and self.add_child(new_child)

    """
    Elimino il nodo, se ha figli elimino anche i figli, se ha un genitore rimuovo il nodo dal genitore
    infine elimino il nodo dalla lista dei nodi vivi
    ritorna se il processo è andato a buon fine
    """
    def kill(self) -> bool:
        # Se uccido un nodo devo uccidere anche tutti i figli
        try:
            result = True

            for c in self.childs:
                result = result and c.kill()

            if self.parent != None:
                result = self.parent.remove_child(self)

            sgengine.event_loop().remove_alive_node(self)
            if self.on_kill:
                self.on_kill()

            return result
        except:
            return False

    """
    ritorna se il nodo è presente nella lista dei nodi vivi
    """

    def is_alive(self) -> bool:
        return sgengine.event_loop().is_node_alive(self)

    def find_node_by_type(self, clz) -> 'Node':
        return sgengine.event_loop().find_node_by_type(clz)

    def find_node_by_id(self, id: str) -> 'Node':
        return sgengine.event_loop().find_node_by_id(id)

from sgengine import physics

class EventLoop(Node):
    _instance = None

    @staticmethod
    def get_instance() -> 'EventLoop':
        if EventLoop._instance == None:
            EventLoop._instance = EventLoop()
        return EventLoop._instance

    def start(self) -> None:
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.framerate = 120
        self.current_frametime = 0
        self.current_framerate = 0
        self.screen_update_thread = Thread(target=self.start_screen_update)

        super().start()
        self.screen_update_thread.start()
        self.start_update()

    def start_update(self):
        while self.is_running:
            self.update()

    def start_screen_update(self):
        while self.is_running:
            pygame.display.update()

    def update(self) -> None:
        self._current_events = pygame.event.get()
        super().update()
        self.current_frametime = self.clock.tick(self.framerate)
        self.current_framerate = self.clock.get_fps()

    def stop(self) -> None:
        self.is_running = False

    def get_current_events(self) -> List[pygame.event.Event]:
        if not hasattr(self, "_current_events"):
            self._current_events = []
        return self._current_events

    """
    ritorna la lista dei nodi vivi
    """
    def alive_nodes(self) -> List[Node]:
        if not hasattr(self, "_alive_nodes") or self._alive_nodes == None:
            self._alive_nodes = []
        return self._alive_nodes[:]

    """
    aggiunge un nodo alla lista dei nodi vivi
    """
    def add_alive_node(self, node: Node) -> None:
        if not hasattr(self, "_alive_nodes") or self._alive_nodes == None:
            self._alive_nodes = []
        self._alive_nodes.append(node)

    """
    rimuove un nodo dalla lista dei nodi vivi
    """
    def remove_alive_node(self, node: Node) -> None:
        if not hasattr(self, "_alive_nodes") or self._alive_nodes == None:
            self._alive_nodes = []
        self._alive_nodes.remove(node)

    """
    ritorna se un nodo è presente nella lista dei nodi vivi
    """
    def is_node_alive(self, node: Node) -> bool:
        if not hasattr(self, "_alive_nodes") or self._alive_nodes == None:
            self._alive_nodes = []
        return node in self._alive_nodes

    def find_node_by_type(self, clz) -> Node:
        for node in self.alive_nodes():
            if (issubclass(type(node), clz)):
                return node

        return None

    """
    ritorna un nodo tramite il suo id, se il nodo non è presente ritorna None
    """
    def find_node_by_id(self, id: str) -> Node:
        for node in self.alive_nodes():
            if (node.id == id):
                return node

        return None

