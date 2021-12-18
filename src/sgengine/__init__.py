from sgengine import lifecycle, screen, utils, physics, input, common
import pygame


def event_loop() -> lifecycle.EventLoop:
    return lifecycle.EventLoop.get_instance()

def window_manager() -> screen.WindowManager:
    return screen.WindowManager.get_instance()

def init():
    pygame.init()
    #Aggiungo il window manager al loop in modo che possa creare la finestra
    event_loop().add_child(window_manager())

def start():
    event_loop().start()


def stop():
    event_loop().stop()