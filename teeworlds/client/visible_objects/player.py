from pygame import *

MOVE_SPEED = 7
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
        if x < 0:
            self.visible = False
        else:
            self.visible = True

    def rendering_player(self, screen):
        if self.visible:
            screen.blit(self.image, (self.rect.x, self.rect.y))
