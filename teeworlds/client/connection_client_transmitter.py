from socket import *
from pygame.time import Clock
from multiprocessing import Queue

class Connection:
    def __init__(self, sock, queue):
        self.udp_socket = sock
        self.antilag_timer = Clock()
        try:
            while True:
                self.antilag_timer.tick(60)
                self.udp_socket.send(str.encode(queue.get()))
        except:
            pass