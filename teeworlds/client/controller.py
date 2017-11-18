import pygame
from pygame.locals import *
from connection_client_transmitter import Connection
import os

class Controller:
    def __init__(self, ip_host, port):
        self.connection_to_server = Connection(ip_host, port)
        self.events_interceptor()

    #TODO try autosender decorator
    def handle_keyboard(self, button_info): #номер нажата/отжата
        self.connection_to_server.send_event(
            (
                str(button_info[0])+' '+
                str(button_info[1])
            )
        )

    # TODO try autosender decorator
    def handle_mouse(self, mouse_info): #номер х у нажата/отжата
        self.connection_to_server.send_event(
            (
                str(mouse_info[0]) + ' ' +
                str(mouse_info[1][0]) + ' ' +
                str(mouse_info[1][1]) + ' ' +
                str(mouse_info[2])
            )
        )
    #TODO проработать кнопки
    def events_interceptor(self):
        while True:
            event = pygame.event.poll()

            if event.type == QUIT:
                pygame.event.clear()
                break

            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.handle_keyboard((K_a, KEYDOWN))

                if event.key == K_d:
                    self.handle_keyboard((K_d, KEYDOWN))

                if event.key == K_SPACE:
                    self.handle_keyboard((K_SPACE, KEYDOWN))

            if event.type == MOUSEBUTTONDOWN:
                self.handle_mouse((event.button, event.pos, MOUSEBUTTONDOWN))

        self.connection_to_server.destroy_socket()
        os._exit(0)

