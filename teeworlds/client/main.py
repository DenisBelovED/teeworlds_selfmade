import pygame
from controller import Controller
from multiprocessing import Process

host = '127.0.0.1'
port = 2056

def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 300), 0, 32)
    controller_proc = Process(target=Controller, args=(host, port))

    #TODO visualiser class

    controller_proc.start()
    #controller_proc.terminate()

if __name__ == '__main__':
    main()