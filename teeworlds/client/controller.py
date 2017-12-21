import pygame
from pygame.locals import *
import os
import time

from connection_client_transmitter import Connection # класс, выделяющий сокет

class Controller:
    def __init__(self, sock):
        self.connection_to_server = Connection(sock) # инициируем сокет для отправки данных
        self.events_interceptor() # запускаем цикл перехвата кнопок

    # метод отправляет на сервер байты "номер_клавиши"
    def handle_keyboard(self, button_info):
        self.connection_to_server.send_event(
            (
                str(button_info)
            )
        )
        time.sleep(0.1)

    # метод отправляет на сервер байты "номер_кнопки_мыши координата_Х координата_У"
    def handle_mouse(self, mouse_info):
        self.connection_to_server.send_event(
            (
                str(mouse_info[0]) + ' ' +
                str(mouse_info[1][0]) + ' ' +
                str(mouse_info[1][1])
            )
        )
        time.sleep(0.1)

    def events_interceptor(self):
        from display_class import display
        from map_class import map1, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR
        button_pressed = False
        start_time = time.time()

        while True:
            # отправить серверу данные о своей активности
            now_time = time.time()
            if now_time-start_time > 5:
                start_time = int(now_time)
                self.connection_to_server.send_event('ONLINE')

            event = pygame.event.poll()
            pressed = pygame.key.get_pressed()

            try:
                pos = event.pos
            except:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                button_pressed = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                button_pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse((1, pos)) #TODO одновременное нажатие не работает

            if button_pressed:
                self.handle_mouse((3, pos))

            if pressed[K_a]:
                self.handle_keyboard(K_a)

            if pressed[K_d]:
                self.handle_keyboard(K_d)

            if (event.type == KEYDOWN) and (event.key == K_SPACE):
                self.handle_keyboard(K_SPACE)

            if event.type == QUIT:
                self.connection_to_server.send_event('DIS')
                pygame.event.clear()
                break

            display.rendering_background()
            display.rendering_map(map1, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR)
            display.display_update()

        self.connection_to_server.destroy_socket()
        display.kill_screen()
        os._exit(0)