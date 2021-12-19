import socket
import time

host = 'localhost'
port = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind((host, port))
server_socket.setblocking(0)
server_socket.listen(2)
print('Create server socket')


players_sockets = []
while True:
    # connecting new players
    try:
        new_socket, addr = server_socket.accept()
        print(addr)
        new_socket.setblocking(0)
        players_sockets.append(new_socket)
        print('Connect ', addr)
    except:
        print('Not new socket')

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

    time.sleep(1)
