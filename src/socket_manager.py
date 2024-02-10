import socket

def create_socket(server, port, nickname, token, channel):
    new_socket = socket.socket()

    new_socket.connect((server,port))

    new_socket.send(f"PASS {token}\n".encode('utf-8'))
    new_socket.send(f"NICK {nickname}\n".encode('utf-8'))
    new_socket.send(f"JOIN {channel}\n".encode('utf-8'))

    return new_socket

#   Twitch sends testing messages, call it and then analyse the messages
def handle_twitch_test_messages(socket):
    test_resp = socket.recv(2048).decode('utf-8')
    ANOTHER_test_resp = socket.recv(2048).decode('utf-8')