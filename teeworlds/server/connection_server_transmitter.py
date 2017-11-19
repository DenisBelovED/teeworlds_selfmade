#здесь описана отправка данных всем подключённым клиеентам

from socket import *
from multiprocessing import Process, Pipe


class Multitransmitter:
    def __init__(self, client_host, client_port, pipe_out_connection):
        self.client_addr = (client_host, client_port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.connect(self.client_addr)

        while True:
            self.udp_socket.send(pipe_out_connection.recv())

    def __del__(self):
        self.udp_socket.close()