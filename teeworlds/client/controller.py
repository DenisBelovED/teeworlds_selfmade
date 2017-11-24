import pygame
from pygame.locals import *
from connection_client_transmitter import Connection
import os
import time

class Controller:
    def __init__(self, ip_host, port):
        self.connection_to_server = Connection(ip_host, port)
        self.events_interceptor()

    def handle_keyboard(self, button_info):
        self.connection_to_server.send_event(
            (
                str(button_info)
            )
        )
        time.sleep(0.1)

    def handle_mouse(self, mouse_info): #номер х у нажата/отжата
        self.connection_to_server.send_event(
            (
                str(mouse_info[0]) + ' ' +
                str(mouse_info[1][0]) + ' ' +
                str(mouse_info[1][1])
            )
        )
        time.sleep(0.1)

    def events_interceptor(self):

        from display_class import display #!!!! какая-то магия
        # порождает объект display при каждом import'e
        # проблема в том, что при вызове name_process.start() происходит повторный вызов в main файле, но тут всё норм...

        while True:
            event = pygame.event.poll()
            pressed_mouse = pygame.mouse.get_pressed()
            pressed = pygame.key.get_pressed()

            try:
                pos = event.pos
            except:
                pass

            if (event.type == MOUSEBUTTONDOWN) and (event.button) == 1:
                self.handle_mouse((1, event.pos))

            if pressed_mouse[2] == 1:
                self.handle_mouse((3, pos))

            if pressed[K_a] == 1:
                self.handle_keyboard(K_a)

            if pressed[K_d] == 1:
                self.handle_keyboard(K_d)

            if (event.type == KEYDOWN) and (event.key == K_SPACE):
                self.handle_keyboard(K_SPACE)

            if event.type == QUIT:
                pygame.event.clear()
                break

        display.kill_screen()
        self.connection_to_server.destroy_socket()
        os._exit(0)

#if __name__ == '__main__':
#    controller = Controller()