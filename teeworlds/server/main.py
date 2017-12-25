from server_model import Server

import sys

def main():
    path = sys.path[0]
    path = path[:-6] + 'maps'
    sys.path.append(path)

    s1 = Server()
    #TODO s1.stop_process() "contexlib"

if __name__ == '__main__':
    main()