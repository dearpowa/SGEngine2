from typing import Tuple
from sgengine import lifecycle
import pygame
import sgengine

class WindowManager(lifecycle.Node):

    _instance = None

    @staticmethod
    def get_instance() -> 'WindowManager':
        if WindowManager._instance == None:
            WindowManager._instance = WindowManager()
        return WindowManager._instance

    def start(self) -> None:
        self.update_window()
        return super().start()

    def update(self) -> None:
        #cerco di ottenere gli eventi in modo da capire quando la finestra viene chiusa
        for event in sgengine.event_loop().get_current_events():
            if event.type == pygame.QUIT:
                sgengine.stop()

        return super().update()

    @property
    def resolution(self) -> Tuple[int]:
        if not hasattr(self, "_resolution"):
            self._resolution = (800, 600)
        return self._resolution

    @resolution.setter
    def resolution(self, resolution: Tuple[int]) -> None:
        self._resolution = resolution
        self.update_window()

    @property
    def title(self) -> str:
        if not hasattr(self, "_title"):
            self._title = "SGEngine 2.0"
        return self._title
    
    @title.setter
    def title(self, title) -> None:
        self._title = title
        self.update_window()

    @property
    def window(self) -> pygame.Surface:
        if not hasattr(self, "_window"):
            return None
        return self._window

    @window.setter
    def window(self, window) -> None:
        self._window = window

    def update_window(self) -> None:
        self.window = pygame.display.set_mode(self.resolution, flags=pygame.HWSURFACE|pygame.DOUBLEBUF, vsync=1)
        pygame.display.set_caption(self.title)


class Camera(lifecycle.Node):
    def start(self) -> None:
        self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        return super().start()

    def update(self) -> None:
        self.draw_on_screen()
        return super().update()

    def draw_on_screen(self) -> None:
        wm = self.find_window_manager()

        if wm == None or wm.window == None:
            return

        frame = pygame.Surface(wm.window.get_size(), flags=pygame.HWSURFACE)

        frame_rect = frame.get_rect()
        
        self.rect.width = frame_rect.width
        self.rect.height = frame_rect.height

        print(self.rect)

        for node in sgengine.event_loop().alive_nodes():
            if hasattr(node, "sprite") and node.sprite != None and hasattr(node, "rect") and node.rect != None:
                sprite = node.sprite
                rect = node.rect.move(-self.rect.left, -self.rect.top)
                frame.blit(sprite, rect)

        for node in sgengine.event_loop().alive_nodes():
            if hasattr(node, "text") and node.text != None and hasattr(node, "rect") and node.rect != None:
                text = node.text
                rect = node.rect
                frame.blit(text, rect)
                
        wm.window.blit(frame, (0,0))

    def find_window_manager(self) -> WindowManager:
        return sgengine.window_manager()
