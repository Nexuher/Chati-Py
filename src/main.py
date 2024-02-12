import socket_manager
import data_pack
import sys
import Logger
from data_analyser import analyse_next_message

server = 'irc.chat.twitch.tv'
port = 6667
inputted_channel = "#" + str(sys.argv[1])

def main():
    # Grab stuff needed to connect to twitch
    data_package = data_pack.return_data_pack()

    socket = socket_manager.create_socket(server, port, data_package.secrets_store["account_nickname"], data_package.secrets_store["token"], inputted_channel)
    socket_manager.handle_twitch_test_messages(socket)
    
    Logger.handle_logs("INFO", "Chati_Py is running")
    print(f"Starting connecting to: Port: {port}\nInspecting Channel: {data_package.channel_name}")

    while True:
        try:
            analyse_next_message(socket, data_package)
        except Exception as error_name:
            Logger.handle_logs("ERROR", error_name)

main()