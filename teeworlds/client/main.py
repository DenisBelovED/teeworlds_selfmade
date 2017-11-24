from multiprocessing import Process, Pipe, Queue
import os, signal
from controller import Controller
from connection_client_reciver import Data_reciver

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
    data_queue = Queue()

    getting_world_states_proc = Process(
        target=Data_reciver,
        args=(server_host, server_port, data_queue)
    )
    getting_world_states_proc.start()
    proc_list.append(getting_world_states_proc)
    return data_queue

def stop_process(proc_list):
    for proc in proc_list:
        try:
            os.kill(proc.pid, signal.SIGKILL)
        except:
            pass

def main():
    proc_list = []

    controller_proc = start_generating_controller_event(server_host, server_port, proc_list) #запуск процесса отправки событий на сервер
    get_world_state_queue = start_reciving_world_state(client_host, client_port, proc_list) #труба, получалка "кадров" от сервера

    while controller_proc.is_alive(): #TODO correct exit
        try:
            picture = get_world_state_queue.get(timeout=1)
            print('recive', picture)
            print('from', client_host, client_port)
            print()
        except:
            print('empty queue')

    stop_process(proc_list)

if __name__ == '__main__':
    main()