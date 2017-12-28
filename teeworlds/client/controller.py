import pygame
from pygame.locals import *
import os
import time
from multiprocessing import Process, Queue

from connection_client_transmitter import Connection # класс, выделяющий сокет

class Controller:
    def __init__(self, sock, sock2, data_queue):
        self.my_player = None
        self.data_queue = data_queue # очередь с кадрами на отрисовку
        self.proc_conn1 = None
        self.proc_conn2 = None
        self.player_button_bytes = [0, 0, 0] # состояние нажатости K_SPACE, K_a, K_d соответственно
        # инициируем класс-процессы для отправки данных контроллера
        control_queue, player_queue = self.create_event_sender(sock, sock2) 
        self.queue_for_transmit_control_event = control_queue # очередь для отправки контроллирующих событий
        self.queue_for_transmit_player_event = player_queue # очередь для отправки нажатий кнопок
        self.events_interceptor() # запускаем цикл перехвата кнопок

    # порождаем класс-процесс, который будет отправлять события с задержкой
    # независимо от скорости отрисовки
    def create_event_sender(self, sock, sock2):
        queue = Queue()
        queue2 = Queue(3) # ограничение, чтобы не дудосить сервер

        connection_for_sending_control_events = Process(
            target=Connection,
            args=(sock, queue)
        )

        connection_for_sending_player_events = Process(
            target=Connection,
            args=(sock2, queue2)
        )

        self.proc_conn1 = connection_for_sending_control_events
        self.proc_conn2 = connection_for_sending_player_events

        connection_for_sending_control_events.start()
        connection_for_sending_player_events.start()
        return queue, queue2

    # метод отправляет на сервер байты "номер_клавиши"
    def handle_keyboard(self):
        if (self.player_button_bytes[0] | self.player_button_bytes[1] | self.player_button_bytes[2]):
            if not self.queue_for_transmit_player_event.full():
                self.queue_for_transmit_player_event.put(
                    str(self.player_button_bytes[0]) +
                    str(self.player_button_bytes[1]) +
                    str(self.player_button_bytes[2])
                )

    '''# метод отправляет на сервер байты "номер_кнопки_мыши координата_Х координата_У"
    def handle_mouse(self, mouse_info):
        if self.queue_for_transmit_player_event.full():
            self.queue_for_transmit_player_event.get()
        self.queue_for_transmit_player_event.put(
            (
                str(mouse_info[0]) + ' ' +
                str(mouse_info[1][0]) + ' ' +
                str(mouse_info[1][1])
            )
        )'''

    # метод для снятия событий с клавиатуры и их отправки
    def events_interceptor(self):
        from display_class import display
        from map_class import map1, PLATFORM_WIDTH, PLATFORM_HEIGHT
        from Camera import Camera

        from player import Player
        player_sprite_list = [Player() for i in range(16)]

        def get_spawned_players():
            lst = []
            for p in player_sprite_list:
                if p.id != -1:
                   lst.append(p)
            return lst

        #button_pressed = False
        start_time = time.time()

        total_level_width = len(map1[0]) * PLATFORM_WIDTH  # высчитываем фактическую ширину уровня
        total_level_height = len(map1) * PLATFORM_HEIGHT  # высоту
        camera = Camera(total_level_width, total_level_height)

        while True:
            # отправить серверу данные о своей активности
            now_time = time.time()
            if now_time-start_time > 3:
                start_time = int(now_time)
                self.queue_for_transmit_control_event.put('ONLINE')

            event = pygame.event.poll()
            pressed = pygame.key.get_pressed()

            try:
                pos = event.pos
            except:
                pass

            #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #    button_pressed = True

            #if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            #    button_pressed = False

            '''if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse((1, pos)) #TODO одновременное нажатие не работает

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.handle_mouse((3, pos))'''

            #if button_pressed:
            #    self.handle_mouse((3, pos))

            self.player_button_bytes = [0, 0, 0]

            if pressed[K_a] and not pressed[K_d]:
                self.player_button_bytes[1] = 1

            if pressed[K_d] and not pressed[K_a]:
                self.player_button_bytes[2] = 1

            if pressed[K_SPACE]:
                self.player_button_bytes[0] = 1

            self.handle_keyboard()

            if (event.type == KEYDOWN) and (event.key == K_RETURN):
                self.queue_for_transmit_control_event.put('SPAWN')

            if event.type == QUIT:
                self.queue_for_transmit_control_event.put('DIS')
                pygame.event.clear()
                break

            # считываем данные объектов, и далее их отрисовываем
            if not self.data_queue.empty():
                data_list = b''

                data_list = self.data_queue.get_nowait()
                
                if data_list is None:
                    break

                if data_list[0] == b'id':
                    id = int(data_list[1])
                    self.my_player = player_sprite_list[id]
                    self.my_player.id = id
                    continue
                
                count_bytestr = len(data_list)

                if (not (count_bytestr == 1 and data_list[0] == b'')) and (data_list[0] != b'id'):
                    id_connected_list = []

                    for block_bytes in data_list:
                        b_x, b_y, id = block_bytes.split(b',')
                        b_x = int(b_x)
                        b_y = int(b_y)
                        id = int(id)
                        player_sprite_list[id].update(b_x, b_y)
                        id_connected_list.append(id)

                    for i in range(16):
                        if i not in id_connected_list:
                            player_sprite_list[i].reset()

            if self.my_player is None:
                display.rendering_background()
                display.rendering_map(map1) #TODO get map from server
                display.rendering_players(player_sprite_list)
                display.display_update()
            else:
                display.rendering_background()
                camera.update(self.my_player)
                display.rendering_map_for_self(camera, map1)  # TODO get map from server
                display.rendering_players_for_self(camera, player_sprite_list)
                display.display_update()

        time.sleep(0.1) # дожидаемся дисконнекта
        self.proc_conn1.terminate()
        self.proc_conn2.terminate()
        self.queue_for_transmit_control_event.close()
        self.queue_for_transmit_player_event.close()
        display.kill_screen()
        os._exit(0)