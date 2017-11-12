from connection_server_reciver import Multiconnection
from connection_server_transmitter import Multitransmitter
from multiprocessing import Process, Pipe

server_host = '127.0.0.1'
server_port = 2056

client_host = '127.0.0.1'
client_port = 38224

class Server:
    def __init__(self):
        #нужно манагерить подключения к серверу
        self.proc_list = []
        self.setup()
        
    def __del__(self):
        self.stop_process()

    def stop_process(self):
        for proc in self.proc_list:
            proc.terminate()

    def setup(self):
        event_queue = self.get_events_buffer(server_host, server_port) # "ленивая" очередь событий, которые нужно обработать
        world_state_sender = self.getter_world_states(client_host, client_port) # труба для отправки "кадра" TODO list

        while True:
            print('iterate')
            s = event_queue.recv()
            print('getted', s[0], 'from', s[1])
            world_state_sender.send(s[0])
            print(s[0], 'sended to', client_host, client_port)

    def get_events_buffer(self, server_host, server_port):
        parent_conn, child_conn = Pipe()

        connection_for_sending_world_state = Process(
            target=Multiconnection,
            args=(server_host, server_port, child_conn)
        )
        connection_for_sending_world_state.start()
        self.proc_list.append(connection_for_sending_world_state)
        return parent_conn

    def getter_world_states(self, trans_host, trans_port):
        parent_conn, child_conn = Pipe()

        connection_for_sending_world_state = Process(
            target=Multitransmitter,
            args=(trans_host, trans_port, child_conn)
        )
        connection_for_sending_world_state.start()
        self.proc_list.append(connection_for_sending_world_state)
        return parent_conn