from multiprocessing import Process, Pipe, Queue
from controller import Controller
from connection_client_reciver import Data_reciver
import psutil #piped

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
            psutil.Process(proc.pid).kill()
        except:
            pass

def run_game(s_host, s_port, c_host, c_port, proc_list):

    # запуск процесса отправки событий на сервер
    controller_proc = start_generating_controller_event(
        s_host,
        s_port,
        proc_list
    )

    # труба, получалка "кадров" от сервера
    get_world_state_queue = start_reciving_world_state(
        c_host,
        c_port,
        proc_list
    )

    while controller_proc.is_alive():
        try:
            picture = get_world_state_queue.get(timeout=1)
            print('recive', picture, 'from', c_host, c_port)
            print()
        except:
            print('empty queue')


def main():
    proc_list = []

    run_game(server_host, server_port, client_host, client_port, proc_list)

    stop_process(proc_list)

if __name__ == '__main__':
    main()