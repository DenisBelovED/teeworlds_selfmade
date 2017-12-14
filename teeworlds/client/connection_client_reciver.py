from socket import *

class Data_reciver:
    def __init__(self, client_host, client_port, data_queue):
        self.addr = (client_host, client_port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.bind(self.addr)

        while True:
            data_queue.put_nowait(self.udp_socket.recvfrom(32))

    def __del__(self):
        self.udp_socket.close()

