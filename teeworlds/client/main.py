from multiprocessing import Process, Pipe, Queue
import psutil # делаем sudo -H pip3 install psutil
from socket import *

from controller import Controller # импоритм класс-процесс "контроллер"
from connection_client_reciver import Data_reciver # импортим класс-процесс "получатель состояний мира" (на отрисовку)

server_host = '127.0.0.1'
server_port = 2056

# метод вернёт процес "контроллер"
def start_generating_controller_event(sock, proc_list):
    controller_proc = Process(
        target=Controller,
        args=(sock, )
    )
    controller_proc.start()
    proc_list.append(controller_proc)
    return controller_proc

# метод вернёт очередь состояний игрового мира
def start_reciving_world_state(client_host, client_port, proc_list):
    data_queue = Queue()

    getting_world_states_proc = Process(
        target=Data_reciver,
        args=(client_host, (client_port+1), data_queue)
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

# здесь инициируем подключение к серверу,
# чтобы он знал какой порт для входящих кадров ему выделен
def init_connection():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.connect((server_host, server_port))
    sock.send(b'HI')
    return sock

def run_game(s_host, s_port, proc_list):
    # тут сообщаем серверу про наш открытый порт TODO fix необходимости запускать клиент позже сервера
    try:
        sock = init_connection()
        c_host, c_port = sock.getsockname()
    except:
        ConnectionError()
        c_host = None
        c_port = None

    # труба, получалка "кадров" от сервера
    try:
        get_world_state_queue = start_reciving_world_state(
            c_host,
            c_port,
            proc_list
        )
    except:
        ConnectionError()
        c_host = None
        c_port = None

    # запуск процесса отправки событий на сервер
    try:
        controller_proc = start_generating_controller_event(
            sock,
            proc_list
        )
    except:
        ConnectionError()
        c_host = None
        c_port = None

    if (c_port is not None) and (c_host is not None):
        from visible_objects.player import Player
        player_sprite_list = [Player() for i in range(16)]

        # главный цикл игры
        while controller_proc.is_alive():
            if not get_world_state_queue.empty():
                coord_list = get_world_state_queue.get().split(b' ')
                for i in range(len(coord_list)):
                    b_x, b_y = coord_list[i].split(b',')
                    player_sprite_list[i].update(int(b_x), int(b_y))

                print('recive', picture, 'from', c_host, c_port)
                print()
    else:
        print('try restart client')


def main():
    import sys
    path = sys.path[0]
    path = path[:-6] + 'maps'
    sys.path.append(path)

    proc_list = [] # тут храним дочерние процессы

    run_game(server_host, server_port, proc_list)

    stop_process(proc_list)

if __name__ == '__main__':
    main()