from pygame import *

WIDTH = 22
HEIGHT = 32
COLOR = "#888888"


class Player(sprite.Sprite):
    def __init__(self, x = -1, y = -1):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.visible = False

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y
        if self.rect.x < 0:
            self.visible = False
        else:
            self.visible = True

    def reset(self):
        self.rect.x = -1
        self.rect.y = -1
        self.visible = False
