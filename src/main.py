import json
import socket
import sys

import pygame

from settings import *
from level import Level
from game_data import level_0
from overworld import Overworld


class Game:
    def __init__(self):
        self.max_level = 1
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self, keys_dict):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run(keys_dict)

# connecting to the server
host = 'localhost'
port = 5555


# def keys_to_dict(keys):
#     commands = {
#         'right': keys[pygame.K_RIGHT],
#         'left': keys[pygame.K_LEFT],
#         'jump': keys[pygame.K_UP],
#         'right2': keys[pygame.K_d],
#         'left2': keys[pygame.K_a],
#         'jump2': keys[pygame.K_w]
#     }
#     return commands


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((host, port))
player_no = int(client_socket.recv(256).decode('ascii'))
print('player_no: ', player_no)


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()
game = Game()

while True:
    # read commands
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # keys_dict = (keys_to_dict(pygame.key.get_pressed()))
    keys_dict = pygame.key.get_pressed()
    keys_to_send = json.dumps(keys_dict).encode('ascii')

    client_socket.send(keys_to_send)

    """
    # send a command to the server
    client_socket.send('To left'.encode())

    # we get a new state of the field from the server
    data = client_socket.recv(2**20)
    data = data.decode()

    # drawing a new field state
    print(data)
    """

    game.run(keys_dict)

    pygame.display.update()
    clock.tick(fps)
