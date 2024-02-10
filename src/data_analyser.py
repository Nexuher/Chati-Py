import string
import sys
import datetime
import pytz
import file_handlers
from datetime import datetime

#   Name of channel we're gonna be inspecting
channel = "#" + str(sys.argv[1])

#   Holder for private data
secrets_store = {}

#   Amount of overall messages sent by users on chat throughout the livestream
messages_sent_by_users = 0

#   List containing words and nicknames that got caught by algorithm
word_counter = {}
nickname_list = {}

#   Setting up correct alphabet: 
#   lower, uppercases, special characters and all numbers
good_characters = list(string.ascii_lowercase + string.ascii_uppercase)
numbers = list(string.digits)
special_characters = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',',
    '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
    ']', '^', '_', '`', '{', '|', '}', '~', ' '
]

#   All of the correct numbers, letters and special characters in english alphabet 
correct_unicode_list = numbers + good_characters + special_characters

#   Acquiring information relating the data by using pytz and datetime
timezone = pytz.timezone('Europe/Warsaw')
datatime_information_set = datetime.now(timezone)

date_string_formatted = f"{datatime_information_set.month}-{datatime_information_set.day}-{datatime_information_set.year}"
hour_string_formatted = f"{datatime_information_set.hour}{datatime_information_set.minute}"


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

# Whole algorithm happens here

def Data_Analyser(socket, secrets):
    global messages_sent_by_users
    global word_counter
    global secrets_store

    secrets_store = secrets

    resp = socket.recv(2048).decode('utf-8')

    #  Sometimes twitch returns message PING to check if we're still using channel 
    #  Return PONG to confirm it

    if resp.startswith('PING'):
        print("PING MESSAGE")
        socket.send("PONG\n".encode('utf-8'))  
        resp = socket.recv(2048).decode('utf-8')

    user_nickname, user_message = format_user_message(resp)

    # Add nick to nickname list
    if user_nickname in nickname_list:
        nickname_list[user_nickname] += 1
    else:
        nickname_list[user_nickname] = 1

    # Add word to word list
    for word in user_message:
        correct_word = True

        for letter in word:
            if letter not in correct_unicode_list:
                correct_word = False
        
        formatted_word_from_sentence = word.lower()

        if correct_word == False:
            continue
        elif formatted_word_from_sentence in word_counter:
            word_counter[formatted_word_from_sentence] += 1
        else: 
            word_counter[formatted_word_from_sentence] = 1

    #Simple Logger
    print(messages_sent_by_users + 1,":",user_nickname,":",user_message)

    messages_sent_by_users += 1

#   Sorting nicknames and messages
    sorted_dict_nickname = dict(sorted(nickname_list.items(), key=lambda item: item[1], reverse=True))
    sorted_dict_message = dict(sorted(word_counter.items(), key=lambda item: item[1], reverse=True))

#   Every 100 messages update the data files
    if messages_sent_by_users % 100 == 0:
        file_handlers.update_text_data_file(sorted_dict_nickname, sorted_dict_message, messages_sent_by_users)
        file_handlers.update_json_data_file(sorted_dict_nickname, sorted_dict_message, messages_sent_by_users)