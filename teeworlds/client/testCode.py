import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((400, 100), 0, 32)
#pygame.display.set_caption("My First PyGame Windows");
#helloText = "Hello, World and GCUP"
#(x, y, fontSize) = (10, 40, 40)
#myFont = pygame.font.SysFont("None", fontSize)
#fontColor = (255, 255, 0)
#bgColor = (255, 255, 255)
#fontImage = myFont.render(helloText, 0, (fontColor))
mainLoop = True

while mainLoop:
    for event in pygame.event.get():
        if event.type == QUIT:
            mainLoop = False
        print(event)
    #screen.fill(bgColor)
    #screen.blit(fontImage, (x, y))
    pygame.display.update()
pygame.quit()
