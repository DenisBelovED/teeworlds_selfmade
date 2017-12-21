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

    def rendering_background(self):
        self.screen.blit(self.back_groung, (0, 0))

    def rendering_map(self, map, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR):
        x = 0
        y = 0
        for row in map:
            for col in row:
                if col == "-":
                    block = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    block.fill(Color(PLATFORM_COLOR))
                    self.screen.blit(block, (x, y))
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0

    def display_update(self):
        pygame.display.update()

    def kill_screen(self):
        pygame.quit()


display = Display()