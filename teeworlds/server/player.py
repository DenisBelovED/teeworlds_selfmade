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
        self.yvel = 0 # speed y
        self.xvel = 0 # speed x
        self.onGround = False
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update_model(self, event, platforms): # event имеет формат 'xxx' где может быть x = 0 или x = 1
        if event[0] == '1' and self.onGround:
            self.yvel = -JUMP_POWER

        if event[1] == '1':
            self.xvel = -MOVE_SPEED

        if event[2] == '1':
            self.xvel = MOVE_SPEED

        if not ((event[1] == '1') or (event[2] == '1')):
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

    # проверка, есть контакт с каким-нибдь объектом
    def collide_x(self, platforms):
        for p in platforms:
            if collide_rect(self, p):  # если есть пересечение платформы с игроком

                if self.xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if self.xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

    # проверка, есть контакт с каким-нибдь объектом
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
