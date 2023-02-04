from datetime import datetime
from sgengine import physics, start, utils
from sgengine.lifecycle import Node
from threading import Thread
import sgengine
import pygame
import math

from sgengine.screen import Camera


class Player(Node):
    def start(self) -> None:
        self.sprite = pygame.image.load("assets/simpleguy_small.bmp")
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.movement_speed = 1
        self.camera_priority = -10
        self.solid = True
        self.camera: Camera = None
        self.gravity_settings.enabled = False
        return super().start()

    def update(self) -> None:
        ev = sgengine.event_loop().get_current_events()

        for e in ev:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.movement_x[0] = True  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = True  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = True  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = True  # Giu
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.movement_x[0] = False  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = False  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = False  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = False  # Giu

        x = 0
        y = 0

        if not self.movement_x == [True, True]:
            if self.movement_x[0]:
                x = -self.movement_speed
            if self.movement_x[1]:
                x = +self.movement_speed

        if not self.movement_y == [True, True]:
            if self.movement_y[0]:
                y = -self.movement_speed
            if self.movement_y[1]:
                y = +self.movement_speed

        last_pos = self.rect.copy()
        self.rect.move_ip(x, y)

        colliding, other = physics.is_colliding(self)

        if (colliding):
            self.rect.topleft = last_pos.topleft

        if self.camera:
            self.camera.rect.center = self.rect.center

        return super().update()

class Tree(Node):
    def start(self) -> None:
        self.sprite = pygame.image.load("assets/simpletree.bmp")
        self.sprite.set_colorkey((0, 0, 0))
        self.rect = self.sprite.get_rect()
        self.solid = True
        return super().start()


class Wall(Node):
    def start(self) -> None:
        self.wall = True
        self.color = (128, 128, 128)
        self.rect = pygame.Rect(0, 0, 20, 20)
        return super().start()

class FPSCamera(Camera):
    def start(self) -> None:
        self.fov = 80
        self.render_distance = 100
        self.rotation = 0
        self.rect = pygame.Rect(0, 0, 0 ,0)
        self.last_frame: pygame.Surface = None
        self.render_thread: Thread = None

        super().start()
        self.render_thread = Thread(target=self.render_frame)
        self.render_thread.start()

    def draw_on_screen(self) -> None:

        wm = self.find_window_manager()

        if wm == None or wm.window == None:
            return
        
        if self.last_frame:
            wm.window.blit(self.last_frame, (0, 0))

    def render_frame(self):
        while self.is_alive():
            self.construct_frame()

    def construct_frame(self):
        wm = self.find_window_manager()

        if wm == None or wm.window == None:
            return
    
        half_fov = self.fov/2
        start_angle = int(self.rotation - half_fov)
        finish_angle = int(self.rotation + half_fov)

        origin = self.rect.center

        frame = pygame.Surface(wm.window.get_size())

        step_size = self.fov / frame.get_rect().width

        alive_nodes = sgengine.event_loop().alive_nodes()

        angle = start_angle

        for i in range(frame.get_rect().width):
            line = utils.create_line(origin, self.render_distance, angle)

            lenghts = []

            for node in alive_nodes:
                if hasattr(node, "wall") and node.wall and node.rect and hasattr(node, "color") and node.color:
                    #Render vertical line
                    result = node.rect.clipline(line)
                    #result = utils.line_rectangle_intersection(line[0], line[1], node.rect.topleft, node.rect.bottomright)
                    if result:
                        start, end = result
                        lenght = utils.line_lenght(origin, start)

                        if lenght > 0:
                            lenghts.append((lenght, node.color))
                        

            if len(lenghts) > 0:
                lenghts.sort(key=lambda l: l[0])
                closer_lenght = lenghts[0][0]
                color = lenghts[0][1]

                angle_diff = self.rotation - angle

                closer_lenght = closer_lenght * math.cos(math.radians(angle_diff))

                height_to_screen = frame.get_height() / (closer_lenght / 10)

                height_to_screen = height_to_screen if height_to_screen < frame.get_height() else frame.get_height()

                rect_to_draw = pygame.Rect(0, 0, 1, height_to_screen)
                rect_to_draw.centery = frame.get_rect().centery
                rect_to_draw.left = i

                pygame.draw.line(frame, color=color, start_pos=rect_to_draw.bottomleft, end_pos=rect_to_draw.topright, width=1)

            angle += step_size

        self.last_frame = frame


class FPSPlayer(Node):
    def start(self) -> None:
        self.movement_speed = 3
        self.movement_x = [False, False]
        self.movement_y = [False, False]
        self.camera = self.find_node_by_type(FPSCamera)
        return super().start()

    def update(self) -> None:
        ev = sgengine.event_loop().get_current_events()

        for e in ev:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.movement_x[0] = True  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = True  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = True  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = True  # Giu
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.movement_x[0] = False  # Sinistra
                if e.key == pygame.K_d:
                    self.movement_x[1] = False  # Destra
                if e.key == pygame.K_w:
                    self.movement_y[0] = False  # Su
                if e.key == pygame.K_s:
                    self.movement_y[1] = False  # Giu

        x = 0
        y = 0

        if not self.movement_x == [True, True]:
            if self.movement_x[0]:
                x = -self.movement_speed
            if self.movement_x[1]:
                x = +self.movement_speed

        if not self.movement_y == [True, True]:
            if self.movement_y[0]:
                y = -self.movement_speed
            if self.movement_y[1]:
                y = +self.movement_speed


        self.camera.rotation += x

        line = utils.create_line(self.camera.rect.center, -y, self.camera.rotation)

        mx, my = end_pos = line[1]

        self.camera.rect.center = end_pos
    

        return super().update()
  