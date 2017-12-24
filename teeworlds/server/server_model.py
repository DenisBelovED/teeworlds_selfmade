from connection_server_reciver import Multiconnection
from connection_server_transmitter import Multitransmitter

from multiprocessing import Process, Pipe
import psutil
from socket import *
import time
from pygame.time import Clock

server_host = '127.0.0.1'
server_port = 2056

class Server:
    def __init__(self):
        self.proc_list = []
        self.alive = True
        self.server_work_time = time.time()
        self.main_loop()

    # тут убиваем все порождённые процессы
    def stop_process(self):
        for proc in self.proc_list:
            try:
                psutil.Process(proc.pid).kill()
            except:
                pass

    def main_loop(self):
        from model import game_model # импортим модель игры
        event_queue = self.get_events_buffer(server_host, server_port)  # "ленивая" очередь событий, которые нужно обработать
        start_record = time.time()
        server_tick = Clock() # магия, без которой не работает
        event = [None, None]

        while self.alive:
            server_tick.tick(60)
            event = [None, None]
            if event_queue.poll():
                event = event_queue.recv()
                gamer_addr = (event[1][0], event[1][1])

                #print('getted', event[0], 'from', event[1])

                # тут добавляем игрока в модель, если раньше его не было
                if event[0] == b'HI':
                    game_model.connect(gamer_addr, self.getter_world_states(event[1][0], event[1][1]))
                    continue

                # здесь игрок говорит серверу, что он подключён
                if event[0] == b'ONLINE':
                    game_model.update_player_time(event[1])
                    continue

                # тут удаляем игрока, когда он закрывает клиент
                if event[0] == b'DIS':
                    game_model.disconnect(event[1])
                    continue

                # спавним игрока, когда он нажал ентер
                if event[0] == b'SPAWN':
                    game_model.spawn(event[1])
                    continue

            # тут обработка событий
            game_model.handle_event(event[0], event[1])

            # тут удаляем тех, у кого отвалилось соединение
            if time.time() - start_record > 15:
                start_record = time.time()
                game_model.kik_afk_players()

            # если в мире больше минуты нет игроков, он закрывается
            if not game_model.gamers_dict:
                if time.time() - self.server_work_time > 300:
                    print('stop game world')
                    self.alive=False
            else:
                self.server_work_time=time.time()

        self.stop_process()

    # процесс для чтения данных
    def get_events_buffer(self, server_host, server_port):
        parent_conn, child_conn = Pipe()

        connection_for_sending_world_state = Process(
            target=Multiconnection,
            args=(server_host, server_port, child_conn)
        )
        connection_for_sending_world_state.start()
        self.proc_list.append(connection_for_sending_world_state)
        return parent_conn

    # процесс для отправки данных клиенту
    def getter_world_states(self, trans_host, trans_port):
        parent_conn, child_conn = Pipe()

        connection_for_sending_world_state = Process(
            target=Multitransmitter,
            args=(trans_host, (trans_port + 1), child_conn)
        )
        connection_for_sending_world_state.start()
        self.proc_list.append(connection_for_sending_world_state)
        return parent_conn