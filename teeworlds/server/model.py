from socket import *
import time

class Model:
    def __init__(self):
        self.gamers_dict = {} # {адрес : персоонаж}
        self.connected_client_dict = {} # {addr : pipe}
        self.gamers_time = {} # {addr : time}

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
        self.gamers_dict.pop(gamer_addr)
        self.connected_client_dict.pop(gamer_addr)
        self.gamers_time.pop(gamer_addr)

    def disconnect_list(self, kik_list):
        for addr in kik_list:
            self.gamers_dict.pop(addr)
            self.connected_client_dict.pop(addr)
            self.gamers_time.pop(addr)
        print(kik_list, ' - unactive')

    def connect(self, gamer_addr, pipe_conn):
        self.gamers_time.update({gamer_addr : time.time()})
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

    def update_player_time(self, gamer_addr):
        current_time = time.time()
        self.gamers_time[gamer_addr] = current_time
        print(gamer_addr, ' - time updated')

    def kik_afk_players(self):
        current_time = time.time()
        kik_list = []
        for gamer_addr in self.gamers_time:
            if current_time-self.gamers_time[gamer_addr] > 15:
                kik_list.append(gamer_addr)

        self.disconnect_list(kik_list)


game_model = Model()