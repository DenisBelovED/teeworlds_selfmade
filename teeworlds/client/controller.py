import pygame
from pygame.locals import *
import os
import time
from multiprocessing import Process, Queue

from connection_client_transmitter import Connection # класс, выделяющий сокет

class Controller:
    def __init__(self, sock, sock2, data_queue):
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
        queue2 = Queue(5) # ограничение, чтобы не дудосить сервер

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

    # метод отправляет на сервер байты "номер_кнопки_мыши координата_Х координата_У"
    def handle_mouse(self, mouse_info):
        if self.queue_for_transmit_player_event.full():
            self.queue_for_transmit_player_event.get()
        self.queue_for_transmit_player_event.put(
            (
                str(mouse_info[0]) + ' ' +
                str(mouse_info[1][0]) + ' ' +
                str(mouse_info[1][1])
            )
        )

    # метод для снятия событий с клавиатуры и их отправки
    def events_interceptor(self):
        from display_class import display
        from map_class import map1, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR

        from visible_objects.player import Player
        player_sprite_list = [Player() for i in range(16)]

        #button_pressed = False
        start_time = time.time()

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse((1, pos)) #TODO одновременное нажатие не работает

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.handle_mouse((3, pos))

            #if button_pressed:
            #    self.handle_mouse((3, pos))

            self.player_button_bytes = [0, 0, 0]

            if pressed[K_SPACE]:
                self.player_button_bytes[0] = 1

            if pressed[K_a] and not pressed[K_d]:
                self.player_button_bytes[1] = 1

            if pressed[K_d] and not pressed[K_a]:
                self.player_button_bytes[2] = 1

            self.handle_keyboard()

            if (event.type == KEYDOWN) and (event.key == K_RETURN):
                self.queue_for_transmit_control_event.put('SPAWN')

            if event.type == QUIT:
                self.queue_for_transmit_control_event.put('DIS')
                pygame.event.clear()
                break

            # считываем данные объектов, и далее их отрисовываем
            if not self.data_queue.empty():
                coord_list = self.data_queue.get_nowait()
                if coord_list is None:
                    break
                count_online = len(coord_list)
                if not (count_online == 1 and coord_list[0] == b''):
                    for i in range(16):
                        if i < count_online:
                            b_x, b_y = coord_list[i].split(b',')
                            player_sprite_list[i].update(int(b_x), int(b_y))
                        else:
                            player_sprite_list[i].reset()

            display.rendering_background()
            display.rendering_map(map1, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR) #TODO get map from server
            display.rendering_players(player_sprite_list)
            display.display_update()

        time.sleep(0.1) # дожидаемся дисконнекта
        self.proc_conn1.terminate()
        self.proc_conn2.terminate()
        self.queue_for_transmit_control_event.close()
        self.queue_for_transmit_player_event.close()
        display.kill_screen()
        os._exit(0)