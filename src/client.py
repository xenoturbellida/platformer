import socket


host = 'localhost'
port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((host, port))


while True:
    # read commands

    # send a command to the server
    client_socket.send('To left'.encode())

    # we get a new state of the field from the server
    data = client_socket.recv(1024)
    data = data.decode()

    # drawing a new field state
    print(data)
