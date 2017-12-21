from pygame import *

MOVE_SPEED = 3
WIDTH = 22
HEIGHT = 32


class Player():
    def __init__(self, x, y):
        self.delta_x = 0
        #self.startX = x
        #self.startY = y
        self.rect = Rect(x, y, WIDTH, HEIGHT) #TODO need Rect?

    def update_model(self, event):
        if event == b'97':
            self.delta_x = -MOVE_SPEED
        if event == b'100':
            self.delta_x = MOVE_SPEED
        self.rect.x += self.delta_x
        self.delta_x = 0

    def get_coordinates(self):
        return (self.rect.x, self.rect.y)
