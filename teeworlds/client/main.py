import pygame
from controller import Controller
from multiprocessing import Process

host = '127.0.0.1'
port = 2056

controller_proc = None

def start_generating_controller_event(host, port):
    controller_proc = Process(target=Controller, args=(host, port))

def prepare_exit():
    controller_proc.terminate()

def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 300), 0, 32)


    #TODO visualiser class

    controller_proc.start()
    #prepare_exit()

if __name__ == '__main__':
    main()