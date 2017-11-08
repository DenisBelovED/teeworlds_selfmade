from socket import *
from multiprocessing import Process, Pipe


class Multiconnection:
    def __init__(self, host, port, pipe_out_connection):
        self.server_addr = (host, port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.bind(self.server_addr)

        while True:
            pipe_out_connection.send(self.udp_socket.recvfrom(11))

    def __del__(self):
        self.__destroy_socket__()

    def __destroy_socket__(self):
        self.udp_socket.close()