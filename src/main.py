import socket
import sys

import pygame

from settings import *
from level import Level


# connecting to the server
host = 'localhost'
port = 5555

management_1 = {
            'right': pygame.K_RIGHT,
            'left': pygame.K_LEFT,
            'jump': pygame.K_UP
        }
management_2 = {
        'right': pygame.K_d,
        'left': pygame.K_a,
        'jump': pygame.K_w
    }

"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((host, port))
"""

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
    print(keys)

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
    level.run()

    pygame.display.update()
    clock.tick(60)
