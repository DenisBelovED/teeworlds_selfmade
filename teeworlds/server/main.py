from connection_server import Multiconnection
from multiprocessing import Process, Pipe

server_host = '127.0.0.1'
server_port = 2056

connection_for_getting_events = None

def get_events_buffer():
    parent_conn, child_conn = Pipe()

    connection_for_getting_events = Process(
        target=Multiconnection,
        args=(server_host, server_port, child_conn)
    )
    connection_for_getting_events.start()

    return parent_conn

def prepare_exit():
    connection_for_getting_events.terminate()

def main():
    event_queue = get_events_buffer()

    while True:
        print(event_queue.recv())

    #prepare_exit()


if __name__ == '__main__':
    main()