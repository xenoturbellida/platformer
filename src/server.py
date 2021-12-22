import socket
import sys

import pygame
from settings import *

from src.level import Level
from src.player import Player
from src.settings import start_position_player_1

host = 'localhost'
port = 5555

# create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind((host, port))
server_socket.setblocking(0)
server_socket.listen(2)

# create server window
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

players_sockets = []
players = []
while True:
    # connecting new players
    try:
        new_socket, addr = server_socket.accept()
        new_socket.setblocking(0)
        players_sockets.append(new_socket)
        print(len(players))
        if len(players) <= 2:
            new_player = Player(start_position_player_1)
            players.append(new_player)
            print('Connect ', new_player)
    except:
        pass
        # print('Not new socket')

    # data received from the player
    for sock in players_sockets:
        try:
            data = sock.recv(1024)
            data = data.decode()
            print('Get ', data)
        except:
            pass
            # print('Nothing')

    # click processing

    # sending a new field state
    for sock in players_sockets:
        try:
            sock.send('New field state'.encode())
        except:
            players_sockets.remove(sock)
            sock.close()
            print('Unconect')

    # server window
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.run(players)

    pygame.display.update()
