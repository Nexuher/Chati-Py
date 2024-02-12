import string
import Logger
import file_handlers
import data_pack

data_package = data_pack.return_data_pack()

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

def analyse_next_message(socket, data_package):
    resp = socket.recv(2048).decode('utf-8')

    #  Sometimes twitch returns message PING to check if we're still using channel 
    #  Return PONG to confirm it

    if resp.startswith('PING'):
        print("PING MESSAGE")
        socket.send("PONG\n".encode('utf-8'))  
        resp = socket.recv(2048).decode('utf-8')

    try:
        user_nickname, user_message = format_user_message(resp)
    except Exception as error:
        Logger.handle_logs("ERROR", error, resp)
        return

    # Add nick to nickname list
    if user_nickname in data_package.nickname_list:
        data_package.nickname_list[user_nickname] += 1
    else:
        data_package.nickname_list[user_nickname] = 1

    # Add word to word list
    for word in user_message:
        correct_word = True

        for letter in word:
            if letter not in correct_unicode_list:
                correct_word = False
        
        formatted_word_from_sentence = word.lower()

        if correct_word == False:
            continue
        elif formatted_word_from_sentence in data_package.word_counter:
            data_package.word_counter[formatted_word_from_sentence] += 1
        else: 
            data_package.word_counter[formatted_word_from_sentence] = 1

    #Simple Logger
    print(data_package.messages_sent_by_users + 1,":",user_nickname,":",user_message)

    data_package.messages_sent_by_users += 1

#   Sorting nicknames and messages
    sorted_dict_nickname = dict(sorted(data_package.nickname_list.items(), key=lambda item: item[1], reverse=True))
    sorted_dict_message = dict(sorted(data_package.word_counter.items(), key=lambda item: item[1], reverse=True))

#   Every 100 messages update the data files
    if data_package.messages_sent_by_users % 2 == 0:
        file_handlers.update_text_data_file(sorted_dict_nickname, sorted_dict_message, data_package.messages_sent_by_users)
        file_handlers.update_json_data_file(sorted_dict_nickname, sorted_dict_message, data_package.messages_sent_by_users)