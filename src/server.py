import socket
import time

host = 'localhost'
port = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind((host, port))
# server_socket.setblocking(False)
server_socket.listen(5)
print('Create server socket')


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


error = False
while not error:
    for i in range(2):
        try:
            data = players_sockets[i].recv(2**20)
            players_sockets[(i + 1) % 2].send(data)
            if i == 0:
                print(f'player {i} with data {data}')
        except socket.error as e:
            print(f'disconnection with error {e}')
            players_sockets[i].close()
            error = True

    """        
    # data received from the player
    for sock in players_sockets:
        try:
            data = sock.recv(1024)
            data = data.decode()
            print('Get ', data)
        except:
            print('Nothing')

    # click processing

    # sending a new field state
    for sock in players_sockets:
        try:
            sock.send('New field state'.encode())
        except:
            players_sockets.remove(sock)
            sock.close()
            print('Unconect')
    """