from socket import *
import sys

class Connection:
    def __init__(self, host, port):
        self.addr = (host, port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.connect(self.addr)

    def send_event(self, event):
        if (not event) or (event.__class__ != str):
            raise KeyError()
        #print(event)
        self.udp_socket.send(str.encode(event))

    #def get_event(self):
    #    return self.udp_socket.recv(11)

    def destroy_socket(self):
        self.udp_socket.close()

    def is_close(self):
        return self.udp_socket._closed