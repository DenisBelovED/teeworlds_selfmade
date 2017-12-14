from socket import *

class Model:
    def __init__(self):
        self.gamers_dict = {} # {адрес : персоонаж}
        self.connected_client_dict = {}  # {addr : pipe}

    def __del__(self):
        pass

    def hook(self):
        #TODO
        pass

    def shot(self):
        #todo
        pass

    def jump(self):
        #TODO
        pass

    def move(self):
        #TODO
        pass

    def disconnect(self, gamer_addr):
        #TODO
        pass

    def connect(self, gamer_addr, pipe_conn):
        self.gamers_dict.update({gamer_addr : None}) # TODO None change from player
        self.connected_client_dict.update({gamer_addr: pipe_conn})
        print(gamer_addr, ' - has been connected')
        self.spawn(gamer_addr)

    def spawn(self, gamer_addr):
        #TODO spawn
        world_state = b'spawned'
        self.world_rendering(world_state)

    def handle_event(self, event):
        #TODO прописать ифы обработки
        #test
        world_state = event[0]
        #test
        self.world_rendering(world_state)

    def world_rendering(self, world_state):
        for client in self.connected_client_dict:
            self.connected_client_dict[client].send(world_state)
            print(world_state, 'sended to', client)
        #TODO создание кадра на отрисовку

    def player_alive(self, gamer_addr):
        #TODO
        pass


game_model = Model()