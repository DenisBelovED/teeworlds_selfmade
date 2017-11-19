import pygame
from pygame.locals import *
from sys import exit

# initializing variables
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 24)

# main loop which displays the pressed keys on the screen
while True:
    event = pygame.event.poll() #!!!!!
    press = pygame.key.get_pressed()
    for i in range(0, len(press)):
        if press[i] == 1:
            print(pygame.key.name(i))