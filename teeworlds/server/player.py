from pygame import *

MOVE_SPEED = 5
WIDTH = 22
HEIGHT = 32
JUMP_POWER = 10
GRAVITY = 0.35


class Player():
    def __init__(self, x, y):
        self.yvel = 0
        self.onGround = False
        self.rect = Rect(x, y, WIDTH, HEIGHT) #TODO need Rect?

    def update_model(self, event):
        if event == b'32' and self.onGround:
            self.yvel = -JUMP_POWER
        if not self.onGround:
            self.yvel += GRAVITY
        if event == b'97':
            self.rect.x -= MOVE_SPEED
        if event == b'100':
            self.rect.x += MOVE_SPEED

        self.onGround = False
        self.rect.y += self.yvel

    def get_coordinates(self):
        return (self.rect.x, self.rect.y)
