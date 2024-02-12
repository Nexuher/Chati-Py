import socket
import requests
import sys

def create_socket(server, port, nickname, token, channel):
    new_socket = socket.socket()

    new_socket.connect((server,port))

    new_socket.send(f"PASS {token}\n".encode('utf-8'))
    new_socket.send(f"NICK {nickname}\n".encode('utf-8'))
    new_socket.send(f"JOIN {channel}\n".encode('utf-8'))

    return new_socket

#   Twitch sends testing messages, call it and then analyse the messages
def handle_twitch_test_messages(socket):
    socket.recv(2048).decode('utf-8')
    socket.recv(2048).decode('utf-8')

    print("")

# Experimental function, doesnt work and isnt used
# def check_livestream_status():
#     channel_name_formatted = channel.replace("#","")

#     contents = requests.get('https://www.twitch.tv/' + channel_name_formatted).content.decode('utf-8')

#     if 'isLiveBroadcast' in contents:
#         return True
#     else:
#         return False
