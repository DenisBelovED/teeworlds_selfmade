from socket import *
import time

from player import Player
from game_world import Game_world
from map_class import map1

class Model:
    def __init__(self):
        self.gamers_dict = {} # {адрес : player}
        self.connected_client_dict = {} # {addr : pipe}
        self.gamers_time = {} # {addr : time}
        self.spawned_players = {} # {addr : bool}
        self.world = Game_world()
        self.world.uploading_map(map1)

    # отключаем одного игрока
    def disconnect(self, gamer_addr):
        try:
            self.connected_client_dict.pop(gamer_addr)
            self.world.remove_entity(self.gamers_dict[gamer_addr])
            self.gamers_dict.pop(gamer_addr)
        except:
            print(gamer_addr, 'incorrect exit (single)')
        self.gamers_time.pop(gamer_addr)
        self.spawned_players.pop(gamer_addr)

    #отключаем лист игроков
    def disconnect_list(self, kik_list):
        for addr in kik_list:
            try:
                self.connected_client_dict.pop(addr)
                self.world.remove_entity(self.gamers_dict[addr])
                self.gamers_dict.pop(addr)
            except:
                print(addr, 'incorrect exit (list)')
                self.gamers_time.pop(addr)
                self.spawned_players.pop(addr)
        print(kik_list, ' - unactive')

    # подключаем игрока
    def connect(self, gamer_addr, pipe_conn):
        self.gamers_time.update({gamer_addr : time.time()})
        self.connected_client_dict.update({gamer_addr: pipe_conn})
        self.spawned_players.update({gamer_addr : False})
        print(gamer_addr, ' - has been connected')

    #генерируем точку спавна TODO доработать
    def get_spawn_point(self):
        x = 50
        y = 50
        return (x, y)

    # спавним игрока, когда от него пришло событие b'SPAWN'
    def spawn(self, gamer_addr):
        try:
            if (not self.spawned_players[gamer_addr]) and (len(self.spawned_players)<=16):
                x, y = self.get_spawn_point()
                self.gamers_dict.update({gamer_addr : Player(x, y)})
                self.spawned_players[gamer_addr] = True
                self.world.add_entity(self.gamers_dict[gamer_addr])
                self.world_rendering()
                print(gamer_addr, ' - has been spawned')
        except:
            pass

    # обработка события от клиента
    def handle_event(self, event, addr):
        if len(self.gamers_dict) > 0:
            if (event is not None):
                if (addr in self.gamers_dict):
                    self.gamers_dict[addr].update_model(event.decode(), self.world.platforms)
            else:
                for addr in self.gamers_dict:
                    self.gamers_dict[addr].update_model('000', self.world.platforms)
            self.world_rendering()

    # отправка состояния игрового мира всем клиентам
    def world_rendering(self):
        world_state = self.__serialize([self.gamers_dict[addr].get_coordinates() for addr in self.gamers_dict])
        for client in self.connected_client_dict:
            self.connected_client_dict[client].send(world_state)
            #print(world_state, ' - genered and sended')

    # тут обновляем время присутствия тех, кто послал нам b'ONLINE'
    def update_player_time(self, gamer_addr):
        current_time = time.time()
        self.gamers_time[gamer_addr] = current_time
        #print(gamer_addr, ' - time updated')

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