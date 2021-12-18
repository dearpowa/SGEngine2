from typing import List
import pygame
from pygame.event import Event

from sgengine.utils import log

class Input:
    def __init__(self, *keys: int) -> None:
        self.keys = keys
        pass
"""
configurazione standard degli input
"""
input_config = {
    "left": Input(pygame.K_a, pygame.K_LEFT),
    "right": Input(pygame.K_d, pygame.K_RIGHT),
    "up": Input(pygame.K_w, pygame.K_UP),
    "down": Input(pygame.K_s, pygame.K_DOWN),
    "action": Input(pygame.K_f, pygame.K_KP_ENTER),
    "exit": Input(pygame.K_ESCAPE, pygame.K_BACKSPACE),
    "jump": Input(pygame.K_SPACE),
    "fire1": Input(pygame.K_k, pygame.K_LCTRL),
    "fire2": Input(pygame.K_l, pygame.K_LALT)
}

"""
@returns se un input da input_config ha avuto un evento di tipo type
"""
def check_input(name: str, events: List[Event], type: int=pygame.KEYDOWN) -> bool:
    input = input_config[name]
    if input:
        for e in events:
            #log(f"event: {e}")
            if e.type == type:
                for k_c in input.keys:
                    if e.key == k_c:
                        return True
    
    return False


        