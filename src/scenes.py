import pygame
from pygame import color
from sgengine import event_loop, window_manager
from sgengine.common import PlayerController
from sgengine.input import check_input
from sgengine.lifecycle import Node
from sgengine.physics import Gravity
from sgengine.screen import Camera, RenderType
from entita import FPSCamera, FPSPlayer, Player, Tree, Wall
from sgengine.utils import FPSCounter, UIText


class Scene1(Node):

    def start(self) -> None:
        self.player = Player()
        gravity = Gravity()
        camera = Camera()
        fps_counter = FPSCounter()
        self.add_child(self.player)
        self.add_child(camera)
        self.add_child(fps_counter)
        self.add_child(gravity)

        self.tree1 = Tree()
        self.tree2 = Tree()
        self.tree3 = Tree()

        self.add_child(self.tree1)
        self.add_child(self.tree2)
        self.add_child(self.tree3)

        super().start()
        camera.internal_resolution = (320, 180)
        fps_counter.set_size(10)
        window_manager().resolution = (800, 400)
        window_manager().fullscreen = False

    def started(self) -> None:
        self.tree1.rect.move_ip(0, 10)
        self.tree2.rect.move_ip(10, 10)
        self.tree3.rect.move_ip(50, 15)
        self.player.rect.move_ip(0, -50)
        return super().started()

    def update(self) -> None:
        events = event_loop().get_current_events()

        for e in events:
            if e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                event_loop().is_running = False
        return super().update()


class Scene2(Node):
    def start(self) -> None:
        self.wall1 = Wall()
        self.wall2 = Wall()
        self.camera = Camera()
        self.add_child(FPSCamera())
        self.add_child(self.camera)
        self.add_child(FPSCounter())
        self.add_child(FPSPlayer())
        self.add_child(self.wall1)
        self.add_child(self.wall2)
        return super().start()

    def started(self) -> None:
        self.wall1.rect.move_ip(-30, 30)
        self.wall2.rect.move_ip(30, 30)
        self.wall1.color = (255, 0, 0)
        self.wall2.color = (0, 255, 0)
        self.camera.transparent = True
        return super().started()


class Scene3(Node):
    
    def start(self) -> None:
        super().start()
        foxy = PlayerController(self)
        foxy.id = "foxy"
        camera = Camera(self)
        fps_counter = FPSCounter(self)
        foxy_pos = UIText(self)
        foxy_pos.id = "foxy_pos"
        foxy_pos.rect.topleft = (0, 30)
        foxy_pos.set_font("assets/OpenSans-Regular.ttf")
        foxy_pos.set_size(30)
        
        foxy.set_sprite(pygame.image.load("assets/foxy.bmp"))
        foxy.on_update = lambda: self.update_camera(foxy, camera)

    def update(self) -> None:
        events = event_loop().get_current_events()

        foxy_pos: UIText = self.find_node_by_id("foxy_pos")
        foxy: PlayerController = self.find_node_by_id("foxy")
        foxy_pos.text = f'Foxy pos: {foxy.rect.topleft}'

        if check_input("exit", events, pygame.KEYUP):
            event_loop().stop()

        super().update()

    def update_camera(self, node1: Node, camera: Camera):
        camera.rect.center = node1.rect.center