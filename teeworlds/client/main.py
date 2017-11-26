from multiprocessing import Process, Pipe, Queue
import psutil # делаем sudo -H pip3 install psutil

from controller import Controller # импоритм класс-процесс "контроллер"
from connection_client_reciver import Data_reciver # импортим класс-процесс "получатель состояний мира" (на отрисовку)

server_host = '127.0.0.1'
server_port = 2056

client_host = ''
client_port = 38224

# метод вернёт процес "контроллер"
def start_generating_controller_event(server_host, server_port, proc_list):
    controller_proc = Process(
        target=Controller,
        args=(server_host, server_port)
    )
    controller_proc.start()
    proc_list.append(controller_proc)
    return controller_proc

# метод вернёт очередь состояний игрового мира
def start_reciving_world_state(client_host, client_port, proc_list):
    data_queue = Queue()

    getting_world_states_proc = Process(
        target=Data_reciver,
        args=(client_host, client_port, data_queue)
    )
    getting_world_states_proc.start()
    proc_list.append(getting_world_states_proc)
    return data_queue

# тут убиваем все порождённые процессы
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

    # главный цикл игры
    while controller_proc.is_alive():
        try:
            picture = get_world_state_queue.get(timeout=1)
            print('recive', picture, 'from', c_host, c_port)
            print()
        except:
            print('empty queue')


def main():
    proc_list = [] # тут храним дочерние процессы

    run_game(server_host, server_port, client_host, client_port, proc_list)

    stop_process(proc_list)

if __name__ == '__main__':
    main()