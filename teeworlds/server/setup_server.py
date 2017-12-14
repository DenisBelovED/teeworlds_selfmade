from connection_server_reciver import Multiconnection
from connection_server_transmitter import Multitransmitter

from multiprocessing import Process, Pipe
import psutil
from socket import *

server_host = '127.0.0.1'
server_port = 2056

class Server:
    def __init__(self):
        self.proc_list = []
        self.alive = True
        self.main_loop()

    # тут убиваем все порождённые процессы
    def stop_process(self):
        game_model.__del__()
        for proc in self.proc_list:
            try:
                psutil.Process(proc.pid).kill()
            except:
                pass

    def main_loop(self): # TODO correct exit
        from model import game_model # импортим модель игры

        event_queue = self.get_events_buffer(server_host, server_port)  # "ленивая" очередь событий, которые нужно обработать

        while self.alive:

            if event_queue.poll():
                event = event_queue.recv()
                gamer_addr = (event[1][0], event[1][1])

                print('getted', event[0], 'from', event[1])

                # тут добавляем игрока в модель, если раньше его не было
                if event[0] == b'HI':
                    game_model.connect(gamer_addr, self.getter_world_states(event[1][0], event[1][1]))
                    continue

                # тут удаляем игрока, когда он закрывает клиент
                if event[0][0:3] == b'DIS':
                    string = event[0].decode('utf-8')
                    lst = string.split()
                    game_model.disconnect((lst[1], int(lst[2])))
                    continue

                #тут обработка событий
                game_model.handle_event(event)

    def get_events_buffer(self, server_host, server_port):
        parent_conn, child_conn = Pipe()

        connection_for_sending_world_state = Process(
            target=Multiconnection,
            args=(server_host, server_port, child_conn)
        )
        connection_for_sending_world_state.start()
        self.proc_list.append(connection_for_sending_world_state)
        return parent_conn

    def getter_world_states(self, trans_host, trans_port):
        parent_conn, child_conn = Pipe()

        connection_for_sending_world_state = Process(
            target=Multitransmitter,
            args=(trans_host, trans_port, child_conn)
        )
        connection_for_sending_world_state.start()
        self.proc_list.append(connection_for_sending_world_state)
        return parent_conn