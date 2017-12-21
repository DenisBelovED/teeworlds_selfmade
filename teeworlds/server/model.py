from socket import *
import time

from player import Player

class Model:
    def __init__(self):
        self.gamers_dict = {} # {адрес : player}
        self.connected_client_dict = {} # {addr : pipe}
        self.gamers_time = {} # {addr : time}

    # отключаем одного игрока
    def disconnect(self, gamer_addr):
        self.gamers_dict.pop(gamer_addr)
        self.connected_client_dict.pop(gamer_addr)
        self.gamers_time.pop(gamer_addr)

    #отключаем лист игроков
    def disconnect_list(self, kik_list):
        for addr in kik_list:
            self.gamers_dict.pop(addr)
            self.connected_client_dict.pop(addr)
            self.gamers_time.pop(addr)
        print(kik_list, ' - unactive')

    # подключаем игрока
    def connect(self, gamer_addr, pipe_conn):
        self.gamers_time.update({gamer_addr : time.time()})
        self.gamers_dict.update({gamer_addr : Player(50, 50)}) #TODO spawn and spawn point
        self.connected_client_dict.update({gamer_addr: pipe_conn})
        print(gamer_addr, ' - has been connected')
        self.spawn(gamer_addr)

    def spawn(self, gamer_addr):
        #TODO spawn
        print(gamer_addr, ' - spawned')

    # обработка события от клиента
    def handle_event(self, event):
        self.gamers_dict[event[1]].update_model(event[0]);
        world_state = []
        for addr in self.gamers_dict:
            world_state.append(self.gamers_dict[addr].get_coordinates())
        self.world_rendering(world_state)

    # отправка состояния игрового мира всем клиентам
    def world_rendering(self, world_state):
        world_state = self.__serialize(world_state)
        for client in self.connected_client_dict:
            self.connected_client_dict[client].send(world_state)
            #print(world_state, ' - genered and sended')

    # тут обновляем время присутствия тех, кто послал нам b'ONLINE'
    def update_player_time(self, gamer_addr):
        current_time = time.time()
        self.gamers_time[gamer_addr] = current_time
        print(gamer_addr, ' - time updated')

    # удаляем тех, кто перестал нам посылать пакет b'ONLINE'
    def kik_afk_players(self):
        current_time = time.time()
        kik_list = []
        for gamer_addr in self.gamers_time:
            if current_time-self.gamers_time[gamer_addr] > 15:
                kik_list.append(gamer_addr)
        self.disconnect_list(kik_list)

    # метод превращает лист таплов в байтовую строку
    def __serialize(self, list_objects):
        result = b''
        for obj in list_objects:
            result+=(str(obj[0])+','+str(obj[1])+' ').encode()
        return result


game_model = Model()