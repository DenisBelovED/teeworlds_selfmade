import pygame
from controller import Controller
from multiprocessing import Process, Pipe
from connection_client_reciver import Data_reciver
from threading import Timer
import os, signal

server_host = '127.0.0.1'
server_port = 2056

client_host = '127.0.0.1'
client_port = 38224

def start_generating_controller_event(server_host, server_port, proc_list):
    controller_proc = Process(
        target=Controller,
        args=(server_host, server_port)
    )
    controller_proc.start()
    proc_list.append(controller_proc)
    return controller_proc

def start_reciving_world_state(server_host, server_port, proc_list):
    parent_conn, child_conn = Pipe()

    getting_world_states_proc = Process(
        target=Data_reciver,
        args=(server_host, server_port, child_conn)
    )
    getting_world_states_proc.start()
    proc_list.append(getting_world_states_proc)
    return parent_conn

def stop_process(proc_list):
    for proc in proc_list:
        try:
            os.kill(proc.pid, signal.SIGKILL)
        except:
            pass

def main():
    proc_list = []

    pygame.init()
    screen = pygame.display.set_mode((300, 300), 0, 32)

    controller_proc = start_generating_controller_event(server_host, server_port, proc_list) #запуск процесса отправки событий на сервер
    get_world_state = start_reciving_world_state(client_host, client_port, proc_list) #труба, получалка "кадров" от сервера

    while controller_proc.is_alive(): #TODO correct exit
        picture = get_world_state.recv()
        print('recive', picture)
        print('from', client_host, client_port)
        print()


    pygame.quit()
    stop_process(proc_list)

if __name__ == '__main__':
    main()