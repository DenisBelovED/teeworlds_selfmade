from socket import *
import os
from multiprocessing import Queue

class Data_reciver:
    def __init__(self, client_host, client_port, data_queue):
        self.addr = (client_host, client_port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.bind(self.addr)

        try:
            while True:
                data_queue.put(self.udp_socket.recv(128))
        except:
            data_queue.put(None)
            self.udp_socket.close()
            data_queue.close()
            os._exit(0)
