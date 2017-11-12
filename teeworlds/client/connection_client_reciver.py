from socket import *

class Data_reciver:
    def __init__(self, client_host, client_port, pipe_input):
        self.pipe = pipe_input
        self.addr = (client_host, client_port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.bind(self.addr)

        while True:
            pipe_input.send(self.udp_socket.recvfrom(11))

    def __del__(self):
        self.udp_socket.close()
        self.pipe.close()

