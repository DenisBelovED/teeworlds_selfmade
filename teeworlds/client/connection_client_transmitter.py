from socket import *
import sys
import time

class Connection:
    def __init__(self, sock):
        self.udp_socket = sock

    def send_event(self, event):
        try:
            self.udp_socket.send(str.encode(event))
            #time.sleep(0.002)
        except:
            print('no connection to server')

    def destroy_socket(self):
        self.udp_socket.close()

    def is_close(self):
        return self.udp_socket._closed