import string
import sys
import os
import datetime
import pytz
import json

from datetime import datetime

#   Name of channel we're gonna be inspecting
channel = "#" + str(sys.argv[1])

LEC_Livestreams = False

word_counter = {}
nickname_list = {}

timezone = pytz.timezone('Europe/Warsaw')
datatime_information_set = datetime.now(timezone)

date_string_formatted = f"{datatime_information_set.month}-{datatime_information_set.day}-{datatime_information_set.year}"
hour_string_formatted = f"{datatime_information_set.hour}{datatime_information_set.minute}"

#   Holder for private data
secrets_store = {}

good_characters = list(string.ascii_lowercase + string.ascii_uppercase)
numbers = list(string.digits)
special_characters = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',',
    '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
    ']', '^', '_', '`', '{', '|', '}', '~', ' '
]

#   All of the correct numbers, letters and special characters in english alphabet 
correct_unicode_list = numbers + good_characters + special_characters

#   Amount of overall messages sent by users on chat throughout the livestream
messages_sent_by_users = 0

def create_directory_to_file(channel_name, file_name):
    directory_path = f"Data_Gathered/{channel_name}/{date_string_formatted}"
    os.makedirs(directory_path, exist_ok=True)

#   Construct the full path to the file, including the directory
    file_path = os.path.join(directory_path, file_name)

    return file_path

def determine_file_name(channel_name):
    # Determine name of the file
    if LEC_Livestreams:
        file_name = f"LEC_Week3_Day3_Analysis_{hour_string_formatted}_{date_string_formatted}.txt"
    else:
        file_name = channel_name + f"_Analysis_{hour_string_formatted}_{date_string_formatted}.txt"

    return file_name

#   Grab nickname and message sent by user from the call taken from resp
def format_user_message(resp):
    first_split = resp.split("!")
    ending_split = first_split[1].split(":")

    user_nickname = first_split[0].replace(":","")
    pre_formatted_user_message = ending_split[1]

    for letter in special_characters:
        if letter in pre_formatted_user_message:
            pre_formatted_user_message = pre_formatted_user_message.replace(letter," ")

    user_message = pre_formatted_user_message.split()

    return user_nickname, user_message

#   Grab the message, send PING message to prevent disconnection with Twitch every 5 minutes,
#   Then analyse the message, send to files,
#   Repeat

def Data_Analyser(socket, secrets):
    global messages_sent_by_users
    global word_counter
    global secrets_store

    secrets_store = secrets

    resp = socket.recv(2048).decode('utf-8')

#   Sometimes twitch returns message PING to check if we're still using channel 
#   Just return socket.send PONG to confirm it

    if resp.startswith('PING'):
        print("PING MESSAGE")
        socket.send("PONG\n".encode('utf-8'))  
        resp = socket.recv(2048).decode('utf-8')

    user_nickname, user_message = format_user_message(resp)

#   Appending to nickname list

    if user_nickname in nickname_list:
        nickname_list[user_nickname] += 1
    else:
        nickname_list[user_nickname] = 1

#   Appending to Word list

    for word in user_message:
        correct_word = True

        # if LEC_Livestreams:
            #league_analyser.main(word)

        for letter in word:
            if letter not in correct_unicode_list:
                correct_word = False
        
        formatted_word_from_sentence = word.lower()

        #   Correct word is used to check whether the word from the sentence sent by user had a character which could not be decoded
        #   If it didn't then just add it or add another occurence

        if correct_word == False:
            continue
        elif formatted_word_from_sentence in word_counter:
            word_counter[formatted_word_from_sentence] += 1
        else: 
            word_counter[formatted_word_from_sentence] = 1

    #Simple Logger
    print(messages_sent_by_users + 1,":",user_nickname,":",user_message)

    messages_sent_by_users += 1

    #   Sorting:
    #   Nicknames by the amount they typed the message on chat
    #   Messages by the amount they occured on chat
    sorted_dict_nickname = dict(sorted(nickname_list.items(), key=lambda item: item[1], reverse=True))
    sorted_dict_message = dict(sorted(word_counter.items(), key=lambda item: item[1], reverse=True))

    #   Every 100 messages update the data files
    if messages_sent_by_users % 100 == 0:
        update_data_files(sorted_dict_nickname, sorted_dict_message, messages_sent_by_users)
        update_json_files(sorted_dict_nickname, sorted_dict_message, messages_sent_by_users)

def update_data_files(user_list, message_list, message_count):
    global secrets_store

    channel_name = channel.replace("#","")
    file_name = determine_file_name(channel_name)

    # Handle where file would go
    file_directory = create_directory_to_file(channel_name, file_name)
    file_handler = open(f"{file_directory}","w")

    # Basic content of TXT file, 
    list_message = f"""
        {channel_name} live stream information for:

        -------------------------------------------------------------
        | Date:                     {date_string_formatted}   
        | Hour turned on:           {hour_string_formatted} UTC
        | Nickname on chat:         {secrets_store["account_nickname"]}              
        | Twitch_stream_link:       www.twitch.tv/{channel_name}    
        | Messages sent overall:    {message_count}                 
        -------------------------------------------------------------
        
        User messsage's sent list:
            {user_list}
        <------------------------------------------->
        Messages sent list:
            {message_list}
    """

    # Input it to the file, close it
    file_handler.write(list_message)
    file_handler.close()

def update_json_files(user_list, message_list, message_count):
    global secrets_store
    
    channel_name = channel.replace("#","")
    channel_link = "www.twitch.tv/" + channel_name

    file_name = file_name = determine_file_name(channel_name)

    # Handle where file would go
    file_directory = create_directory_to_file(channel_name, file_name)
    file_handler = open(f"{file_directory}","w")

    # Basic content of JSON file, 
    updated_set_of_information = {
        "Livestream Information": {
            "Date": date_string_formatted,
            "Timezone": "UTC",
            "Hour turned on": hour_string_formatted, 
            "Nickname on chat": secrets_store["account_nickname"],
            "Twitch Stream Link": channel_link,
            "Messages sent overall": message_count
        },
        "Nickname list": user_list,
        "Messages list": message_list
    }

    # Input it to the file, close it
    json_object = json.dumps(updated_set_of_information, indent=4)
    file_handler.write(json_object)
