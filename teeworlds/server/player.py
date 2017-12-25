from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.sprite import collide_rect

MOVE_SPEED = 3
WIDTH = 22
HEIGHT = 32
JUMP_POWER = 10
GRAVITY = 0.35


class Player(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.yvel = 0
        self.xvel = 0
        self.onGround = False
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update_model(self, event, platforms):
        left = False
        right = False

        if event == b'32' and self.onGround:
            self.yvel = -JUMP_POWER

        if event == b'97':
            self.xvel = -MOVE_SPEED
            left = True

        if event == b'100':
            self.xvel = MOVE_SPEED
            right = True

        if not (left or right):
            self.xvel = 0

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False

        self.rect.y += self.yvel
        self.collide_y(platforms)

        self.rect.x += self.xvel
        self.collide_x(platforms)

    def get_coordinates(self):
        return (self.rect.x, self.rect.y)

    def collide_x(self, platforms):
        for p in platforms:
            if collide_rect(self, p):  # если есть пересечение платформы с игроком

                if self.xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if self.xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

    def collide_y(self, platforms):
        for p in platforms:
            if collide_rect(self, p):  # если есть пересечение платформы с игроком

                if self.yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if self.yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
