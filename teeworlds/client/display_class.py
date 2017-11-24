import pygame

class Display:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((300, 300), 0, 32)

    def kill_screen():
        pygame.quit()


display = Display()