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

# Experimental function, doesnt work and isnt used
def check_livestream_status():
    channel_name_formatted = channel.replace("#","")

    contents = requests.get('https://www.twitch.tv/' + channel_name_formatted).content.decode('utf-8')

    if 'isLiveBroadcast' in contents:
        return True
    else:
        return False


def main():
    # Grab stuff needed to connect to twitch
    secrets_manager.get_secrets()

    socket = socket_manager.create_socket(server, port, secrets_manager.secrets_store["account_nickname"], secrets_manager.secrets_store["token"], channel)
    socket_manager.handle_twitch_test_messages(socket)
    
    Logger.handle_logs("INFO", "Chati_Py is running")
    print("Chati_Py is running")

    while True:
        try:
            Data_Analyser(socket, secrets_manager.secrets_store)
        except Exception as error_name:
            Logger.handle_logs("ERROR", error_name)
            Data_Analyser(socket, secrets_manager.secrets_store)

main()