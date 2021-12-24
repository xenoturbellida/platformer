import json
import socket
import sys

import pygame

from settings import *
from level import Level
from game_data import level_0


# connecting to the server
host = 'localhost'
port = 5555


def keys_to_dict(keys):
    commands = {
        'right': keys[pygame.K_RIGHT],
        'left': keys[pygame.K_LEFT],
        'jump': keys[pygame.K_UP],
        'right2': keys[pygame.K_d],
        'left2': keys[pygame.K_a],
        'jump2': keys[pygame.K_w]
    }
    return commands


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((host, port))
player_no = int(client_socket.recv(256).decode('ascii'))
print('player_no: ', player_no)


class Game:
    def __init__(self):
        self.stars = 0


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()
level = Level(level_0, screen)


while True:
    # read commands
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_dict = (keys_to_dict(pygame.key.get_pressed()))
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

    screen.fill(sky_color)
    level.run(keys_dict)

    pygame.display.update()
    clock.tick(fps)
