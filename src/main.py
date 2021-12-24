import json
import socket
import sys

import pygame

from settings import *
from level import Level


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

# management_2 = {
#         'right': pygame.K_d,
#         'left': pygame.K_a,
#         'jump': pygame.K_w
#     }


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((host, port))


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()
level = Level(level_map, screen)


while True:
    # read commands
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # print(keys)

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

    screen.fill('black')
    level.run(keys_dict)

    pygame.display.update()
    clock.tick(60)

# while True:
    # read commands
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         sys.exit()

    # keys = pygame.key.get_pressed()

    # send a command to the server
    # keys_dict = (keys_to_dict(pygame.key.get_pressed()))
    # keys_to_send = json.dumps(keys_dict).encode('ascii')
    # print(keys_to_send, '   size   ', len(keys_to_send))

    # client_socket.send(keys_to_send)

    # we get a new state of the field from the server
    # print('here')
    # teammate_keys = client_socket.recv(2**10)
    # print('bytes team keys: ', teammate_keys)
    # teammate_keys = json.loads(teammate_keys.decode('ascii'))
    # print('teammate keys: ', teammate_keys)

    # drawing a new field state
    # print(data)

    # if pygame.key.get_pressed()[pygame.K_LEFT]:
    #     print('pressed left, player_no', player_no)

    # screen.fill('black')
    # # if player_no == 1:
    # #     level.run(keys_dict, teammate_keys)
    # # else:
    # #     level.run(teammate_keys, keys_dict)
    # level.run(keys_dict)
    # # level.run()
    #
    # pygame.display.update()
    # clock.tick(60)
