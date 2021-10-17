from sgengine.lifecycle import Node
from sgengine.screen import Camera
from entita import Player

class Scene1(Node):
    
    def start(self) -> None:
        self.add_child(Player())
        self.add_child(Camera())
        return super().start()