import pygame
from pygame.locals import *
import os
import time
from multiprocessing import Process, Queue

from connection_client_transmitter import Connection # класс, выделяющий сокет

class Controller:
    def __init__(self, sock, data_queue):
        self.data_queue = data_queue # очередь с кадрами на отрисовку
        self.proc_conn = None
        self.queue_for_transmit_event = self.create_event_sender(sock) # инициируем класс-процесс для отправки данных
        self.events_interceptor() # запускаем цикл перехвата кнопок

    # порождаем класс-процесс, который будет отправлять события с задержкой
    # независимо от скорости отрисовки
    def create_event_sender(self, sock):
        queue = Queue(10)

        connection_for_sending_events = Process(
            target=Connection,
            args=(sock, queue)
        )
        self.proc_conn = connection_for_sending_events
        connection_for_sending_events.start()
        return queue

    # метод отправляет на сервер байты "номер_клавиши"
    def handle_keyboard(self, button_info):
        if not self.queue_for_transmit_event.full():
            self.queue_for_transmit_event.put(str(button_info))

    # метод отправляет на сервер байты "номер_кнопки_мыши координата_Х координата_У"
    def handle_mouse(self, mouse_info):
        if self.queue_for_transmit_event.full():
            self.queue_for_transmit_event.get()
        self.queue_for_transmit_event.put(
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
                if self.queue_for_transmit_event.full():
                    self.queue_for_transmit_event.get()
                self.queue_for_transmit_event.put('ONLINE')

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

            # вот так боремся с рассинхронизаией между клиентом и сервером
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                try:
                    self.queue_for_transmit_event.get_nowait()
                    self.queue_for_transmit_event.get_nowait()
                    self.queue_for_transmit_event.get_nowait()
                    self.queue_for_transmit_event.get_nowait()
                    self.queue_for_transmit_event.get_nowait()
                except:
                    pass
                finally:
                    self.queue_for_transmit_event.put_nowait(str(K_SPACE))
                    self.queue_for_transmit_event.put_nowait(str(K_SPACE))
                    self.queue_for_transmit_event.put_nowait(str(K_SPACE))
                    self.queue_for_transmit_event.put_nowait(str(K_SPACE))
                    self.queue_for_transmit_event.put_nowait(str(K_SPACE))

            '''if pressed[K_SPACE]:
                if self.queue_for_transmit_event.full():
                    self.queue_for_transmit_event.get()
                self.handle_keyboard(K_SPACE)'''

            if pressed[K_a] and not pressed[K_d]:
                self.handle_keyboard(K_a)

            if pressed[K_d] and not pressed[K_a]:
                self.handle_keyboard(K_d)

            if (event.type == KEYDOWN) and (event.key == K_RETURN):
                if self.queue_for_transmit_event.full():
                    self.queue_for_transmit_event.get()
                self.queue_for_transmit_event.put('SPAWN')

            if event.type == QUIT:
                while not self.queue_for_transmit_event.empty():
                    self.queue_for_transmit_event.get_nowait()
                while not self.queue_for_transmit_event.full():
                    self.queue_for_transmit_event.put('DIS')
                pygame.event.clear()
                break

            # считываем данные объектов, и далее их отрисовываем
            if not self.data_queue.empty():
                coord_list = self.data_queue.get_nowait()
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
        self.proc_conn.terminate()
        self.queue_for_transmit_event.close()
        display.kill_screen()
        os._exit(0)