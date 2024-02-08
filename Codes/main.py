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
#   Grab stuff needed to connect to twitch
    secrets_manager.get_secrets()

#   Create the socket, flick it to Data_analyser
    socket = socket_manager.create_socket(server, port, secrets_manager.secrets_store["account_nickname"], secrets_manager.secrets_store["token"], channel)

#   Call two messages sent by Twitch 
    socket_manager.pass_testing_messages(socket)
    
    Logger.handle_logs("INFO", "Chati_Py is running")
    print("Active")

    while True:
        try:
            Data_Analyser(socket, secrets_manager.secrets_store)
        except Exception as error_name:
            print(error_name)

main()