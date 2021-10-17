from sgengine import lifecycle, screen
import pygame


def event_loop() -> lifecycle.EventLoop:
    return lifecycle.EventLoop.get_instance()

def window_manager() -> lifecycle.EventLoop:
    return screen.WindowManager.get_instance()

def start():
    pygame.init()
    #Aggiungo il window manager al loop in modo che possa creare la finestra
    event_loop().add_child(window_manager())
    event_loop().start()


def stop():
    event_loop().stop()