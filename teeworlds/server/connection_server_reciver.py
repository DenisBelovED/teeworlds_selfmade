#здесь описана передача входных данных в процесс, на который прокинута труба
#данные приходят на какой-то хост/порт, а мы к нему здесь подсасываемся, и слушаем его
from socket import *

class Multiconnection:
    def __init__(self, server_host, server_port, pipe_out_connection):
        self.server_addr = (server_host, server_port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.bind(self.server_addr)

        while True:
            pipe_out_connection.send(self.udp_socket.recvfrom(32))

    def __del__(self):
        self.udp_socket.close()
