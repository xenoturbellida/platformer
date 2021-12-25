import socket

import pygame
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        self.max_level = 1
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

        self.stars = 0
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_stars, self.check_game_over)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def change_stars(self, amount):
        self.stars += amount

    def check_game_over(self, amount):
        self.stars -= amount

    def run(self, keys_dict):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run(keys_dict)
            self.ui.show_coins(self.stars)


host = 'localhost'
port = 5555

# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind((host, port))
# server_socket.setblocking(0)
server_socket.listen(2)


players_sockets = []
# connecting new players
while len(players_sockets) != 2:
    try:
        new_socket, addr = server_socket.accept()
        print(addr)
        # new_socket.setblocking(False)
        players_sockets.append(new_socket)
        print('Connect ', addr)
        player_no = '1' if len(players_sockets) == 1 else '2'
        new_socket.send(player_no.encode('ascii'))
    except:
        print('There is no new socket')


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()
game = Game()


while True:
    for i in range(2):
        try:
            data = players_sockets[i].recv(2 ** 20)
            players_sockets[(i + 1) % 2].send(data)
            if i == 0:
                print(f'player {i} with data {data}')
            game.run(data)
        except socket.error as e:
            print(f'disconnection with error {e}')
            players_sockets[i].close()
            error = True

    # sending a new field state
    for sock in players_sockets:
        try:
            sock.send('New field state'.encode())
        except:
            players_sockets.remove(sock)
            sock.close()
            print('Unconect')
