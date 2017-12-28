import pygame
from pygame import *
import pyganim

WIDTH = 22
HEIGHT = 32
COLOR = "#2F4F4F"
ANIMATION_DELAY = 50
ANIMATION_RIGHT = [('mario/r1.png'),
            ('mario/r2.png'),
            ('mario/r3.png'),
            ('mario/r4.png'),
            ('mario/r5.png')]
ANIMATION_LEFT = [('mario/l1.png'),
            ('mario/l2.png'),
            ('mario/l3.png'),
            ('mario/l4.png'),
            ('mario/l5.png')]
ANIMATION_JUMP_LEFT = [('mario/jl.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('mario/jr.png', ANIMATION_DELAY)]
ANIMATION_JUMP = [('mario/j.png', ANIMATION_DELAY)]
ANIMATION_STAY = [('mario/0.png', ANIMATION_DELAY)]


class Player:
    def __init__(self, x = -1, y = -1):
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.delta_x = 0
        self.delta_y = 0
        self.id = -1 # -1 означает, что сущности не существует
        self.visible = False

        #        Анимация движения вправо
        bolt_anim = []
        for anim in ANIMATION_RIGHT:
            bolt_anim.append((anim, ANIMATION_DELAY))
        self.bolt_anim_right = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_right.play()
        #        Анимация движения влево
        bolt_anim = []
        for anim in ANIMATION_LEFT:
            bolt_anim.append((anim, ANIMATION_DELAY))
        self.bolt_anim_left = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_left.play()

        self.bolt_anim_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.bolt_anim_stay.play()
        self.bolt_anim_stay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.bolt_anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.bolt_anim_jump_left.play()

        self.bolt_anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.bolt_anim_jump_right.play()

        self.bolt_anim_jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.bolt_anim_jump.play()

    def update(self, x, y):
        self.delta_x = x - self.rect.x
        self.delta_y = y - self.rect.y
        self.rect.x = x
        self.rect.y = y
        if self.rect.x < 0:
            self.visible = False
        else:
            self.visible = True

    def render(self):
        if self.delta_y < 0:
            self.image.fill(Color(COLOR))
            self.bolt_anim_jump.blit(self.image, (0, 0))

        if self.delta_x < 0:
            self.image.fill(Color(COLOR))
            if self.delta_y != 0:
                self.bolt_anim_jump_left.blit(self.image, (0, 0))
            else:
                self.bolt_anim_left.blit(self.image, (0, 0))

        if self.delta_x > 0:
            self.image.fill(Color(COLOR))
            if self.delta_y != 0:
                self.bolt_anim_jump_right.blit(self.image, (0, 0))
            else:
                self.bolt_anim_right.blit(self.image, (0, 0))

        if self.delta_x == 0:  # стоим, когда нет указаний идти
            if not (self.delta_y != 0):
                self.image.fill(Color(COLOR))
                self.bolt_anim_stay.blit(self.image, (0, 0))

    def reset(self):
        self.rect.x = -1
        self.rect.y = -1
        self.visible = False
