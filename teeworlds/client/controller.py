import pygame
from pygame.locals import *
import os
import time

from connection_client_transmitter import Connection # класс, выделяющий сокет

class Controller:
    def __init__(self, sock, data_queue):
        self.data_queue = data_queue
        self.connection_to_server = Connection(sock) # инициируем сокет для отправки данных
        self.events_interceptor() # запускаем цикл перехвата кнопок

    # метод отправляет на сервер байты "номер_клавиши"
    def handle_keyboard(self, button_info):
        self.connection_to_server.send_event(
            (
                str(button_info)
            )
        )
        time.sleep(0.003)

    # метод отправляет на сервер байты "номер_кнопки_мыши координата_Х координата_У"
    def handle_mouse(self, mouse_info):
        self.connection_to_server.send_event(
            (
                str(mouse_info[0]) + ' ' +
                str(mouse_info[1][0]) + ' ' +
                str(mouse_info[1][1])
            )
        )
        time.sleep(0.003)

    def events_interceptor(self):
        from display_class import display
        from map_class import map1, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR

        from visible_objects.player import Player
        player_sprite_list = [Player() for i in range(16)]

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

            if not self.data_queue.empty(): #TODO доработать
                coord_list = self.data_queue.get_nowait()
                for i in range(len(coord_list)):
                    b_x, b_y = coord_list[i].split(b',')
                    player_sprite_list[i].update(int(b_x), int(b_y))

            display.rendering_background()
            display.rendering_map(map1, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR)
            display.rendering_players(player_sprite_list)
            display.display_update()

        self.connection_to_server.destroy_socket()
        display.kill_screen()
        os._exit(0)