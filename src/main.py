import socket
import sys
import time
import json
import os

import pygame

from settings import *
from level import Level


# connecting to the server
host = 'localhost'
port = 5555

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
level = Level(level_map, screen)


def keys_to_dict(keys):
    commands = {
        'right': keys[pygame.K_RIGHT],
        'left': keys[pygame.K_LEFT],
        'jump': keys[pygame.K_UP]
    }
    return commands


def keys_to_dict_pl2(keys):
    commands = {
        'right': keys[pygame.K_d],
        'left': keys[pygame.K_a],
        'jump': keys[pygame.K_w]
    }
    return commands


print('process id:', os.getpid())
while True:
    # read commands
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # keys = pygame.key.get_pressed()

    # send a command to the server
    keys_dict = (keys_to_dict(pygame.key.get_pressed())
                 if player_no == 1
                 else keys_to_dict_pl2(pygame.key.get_pressed()))
    keys_to_send = json.dumps(keys_dict).encode('ascii')
    # print(keys_to_send, '   size   ', len(keys_to_send))

    client_socket.send(keys_to_send)

    # we get a new state of the field from the server
    # print('here')
    teammate_keys = client_socket.recv(2**10)
    # print('bytes team keys: ', teammate_keys)
    teammate_keys = json.loads(teammate_keys.decode('ascii'))
    # print('teammate keys: ', teammate_keys)

    # drawing a new field state
    # print(data)

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        print('pressed left, player_no', player_no)

    screen.fill('black')
    if player_no == 1:
        level.run(keys_dict, teammate_keys)
    else:
        level.run(teammate_keys, keys_dict)
    # level.run()

    pygame.display.update()
    clock.tick(60)
