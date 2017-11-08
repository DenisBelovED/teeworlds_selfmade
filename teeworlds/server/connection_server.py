from socket import *
from multiprocessing import Process, Pipe


def __getting_events__(socket, connection):
    while True:
        connection.send(socket.recvfrom(11))

class Multiconnection:
    def __init__(self, host, port, pipe_out_connection):
        self.server_addr = (host, port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.bind((host, port))

        parent_conn, child_conn = Pipe()

        self.getting_events_process = Process(
            target=__getting_events__,
            args=(self.udp_socket, child_conn)
        )
        self.getting_events_process.start()

        self.__resending_events__(pipe_out_connection, parent_conn)

    def __del__(self):
        self.__destroy_socket__()

    def __destroy_socket__(self):
        self.getting_events_process.terminate()
        self.udp_socket.close()

    def __resending_events__(self, pipe_for_send, pipe_for_recv):
        while True:
            pipe_for_send.send(pipe_for_recv.recv())

    #def is_close(self):
    #    return self.udp_socket._closed