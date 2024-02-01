import socket_manager
import secrets_manager
import requests
import sys
import Logger
from data_analyser import Data_Analyser

server = 'irc.chat.twitch.tv'
port = 6667
channel = "#" + str(sys.argv[1])
secrets = {}

#   Twitch sends testing messages, why?
#   God if I know, just call those two and don't do anything with them
def pass_testing_messages(socket):
    test_resp = socket.recv(2048).decode('utf-8')
    ANOTHER_test_resp = socket.recv(2048).decode('utf-8')


#   Experimental to check whether the live is still working,
#   Spoiler, the code doesn't work, sometimes it throws error and can't figure out why
def check_livestream_status():
    channel_name_formatted = channel.replace("#","")

    contents = requests.get('https://www.twitch.tv/' + channel_name_formatted).content.decode('utf-8')

    if 'isLiveBroadcast' in contents:
        return True
    else:
        return False


def main():
#   Grab stuff needed to connect to twitch
    secrets_manager.get_secrets()

#   Create the socket, flick it to Data_analyser
    socket = socket_manager.create_socket(server, port, secrets_manager.secrets_store["account_nickname"], secrets_manager.secrets_store["token"], channel)

#   Call two messages sent by Twitch I presume
    pass_testing_messages(socket)
    
    Logger.handle_logs("INFO", "Chati_Py is running")
    print("Active")

#   Constantly check if livestream is live, if so then go and analyse the messages
    while True:
        try:
            Data_Analyser(socket, secrets_manager.secrets_store)
        except Exception as error_name:
            print(error_name)

main()