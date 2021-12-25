import socket

import pygame
from settings import *


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
# game = Game()


error = False
while not error:
    for i in range(2):
        try:
            data = players_sockets[i].recv(2 ** 20)
            # print(data)
            players_sockets[(i + 1) % 2].send(data)
            screen = players_sockets[i].recv(2 ** 20)
            players_sockets[(i + 1) % 2].send(screen)
            # if i == 0:
            #     print(f'player {i} with data {data}')
            # game.run(data)
        except socket.error as e:
            print(f'disconnection with error {e}')
            players_sockets[i].close()
            error = True

    pygame.display.update()
    clock.tick(fps)

    # sending a new field state
    # for sock in players_sockets:
    #     try:
    #         sock.send('New field state'.encode())
    #     except:
    #         players_sockets.remove(sock)
    #         sock.close()
    #         print('Unconect')
