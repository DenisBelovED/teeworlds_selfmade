from pygame.sprite import Sprite
from pygame.rect import Rect

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

class Platform(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)