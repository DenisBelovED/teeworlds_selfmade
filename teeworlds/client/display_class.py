import pygame
from pygame import *

WIN_WIDTH = 800 # ширина создаваемого окна
WIN_HEIGHT = 640 # высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#00FF00"

class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY, 0, 32)
        pygame.display.set_caption('Teeworlds')
        self.back_groung = Surface(DISPLAY)
        self.back_groung.fill(Color(BACKGROUND_COLOR))

    def render(self):
        self.screen.blit(self.back_groung, (0, 0))
        pygame.display.update()

    def kill_screen(self):
        pygame.quit()


display = Display()