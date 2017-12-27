import pygame
from pygame import *

WIN_WIDTH = 800 # ширина создаваемого окна
WIN_HEIGHT = 640 # высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#ADD8E6"

class Display:
    def __init__(self):
        pygame.init()
        self.texture = {
            'w': pygame.image.load('textures/horisontal_grass.png'),
            'a': pygame.image.load('textures/anti_vertical_grass.png'),
            'd': pygame.image.load('textures/vertical_grass.png'),
            's': pygame.image.load('textures/anti_horisontal_grass.png'),
            'q': pygame.image.load('textures/lu_grass.png'),
            'e': pygame.image.load('textures/ru_grass.png'),
            'z': pygame.image.load('textures/ld_grass.png'),
            'c': pygame.image.load('textures/rd_grass.png'),
        }
        self.screen = pygame.display.set_mode(DISPLAY, 0, 32)
        pygame.display.set_caption('Teeworlds')
        self.back_groung = Surface(DISPLAY)
        self.back_groung.fill(Color(BACKGROUND_COLOR))

    def rendering_players(self, players_list):
        for player in players_list:
            if player.visible:
                self.screen.blit(player.image, (player.rect.x, player.rect.y))
                player.render()

    def rendering_background(self):
        self.screen.blit(self.back_groung, (0, 0))

    def rendering_map(self, map, PLATFORM_WIDTH, PLATFORM_HEIGHT):
        x = 0
        y = 0
        for row in map:
            for col in row:
                if col != " ":
                    self.screen.blit(self.texture[col], (x, y))
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0

    def display_update(self):
        pygame.display.update()

    def kill_screen(self):
        pygame.quit()


display = Display()