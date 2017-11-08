import pygame
from pygame.locals import *
from connection_client import Connection

class Controller:

    event_key_dict_down = {
        K_w: (K_w, KEYDOWN),
        K_a: (K_a, KEYDOWN),
        K_s: (K_s, KEYDOWN),
        K_d: (K_d, KEYDOWN),
        K_SPACE: (K_SPACE, KEYDOWN)
    }

    event_key_dict_up = {
        K_w: (K_w, KEYUP),
        K_a: (K_a, KEYUP),
        K_s: (K_s, KEYUP),
        K_d: (K_d, KEYUP),
    }

    def __init__(self, ip_host, port):
        self.connection_to_server = Connection(ip_host, port)
        self.events_interceptor()

    def __del__(self):
        self.connection_to_server.destroy_socket()

    def handle_keyboard(self, button_info): #номер нажата/отжата
        self.connection_to_server.send_event(
            (
                str(button_info[0])+' '+
                str(button_info[1])
            )
        )

    def handle_mouse(self, mouse_info): #номер х у нажата/отжата
        self.connection_to_server.send_event(
            (
                str(mouse_info[0]) + ' ' +
                str(mouse_info[1][0]) + ' ' +
                str(mouse_info[1][1]) + ' ' +
                str(mouse_info[2])
            )
        )

    def events_interceptor(self):
        event_loop = True
        while event_loop:
            for event in pygame.event.get():
                try:
                    if event.type == QUIT:
                        event_loop = False

                    if event.type == KEYDOWN:
                        self.handle_keyboard(self.event_key_dict_down[event.key])

                    if event.type == KEYUP:
                        self.handle_keyboard(self.event_key_dict_up[event.key])

                    if event.type == MOUSEBUTTONDOWN:
                        self.handle_mouse((event.button, event.pos, MOUSEBUTTONDOWN))

                    if (event.type == MOUSEBUTTONUP) and (event.button == 3):
                        self.handle_mouse((event.button, event.pos, MOUSEBUTTONUP))
                except:
                    pass