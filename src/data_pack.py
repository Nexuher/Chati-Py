import secrets_manager
import sys
import os
import pytz
from datetime import datetime

class data_pack_object():
    inputted_channel = "#" + str(sys.argv[1])
    channel_name = inputted_channel.replace("#","")
    
    text_file_directory = ""
    json_file_directory = ""

    #   Acquiring information relating the data by using pytz and datetime
    datatime_information_set = datetime.now(pytz.timezone('Europe/Warsaw'))

    date_string_formatted = f"{datatime_information_set.month}-{datatime_information_set.day}-{datatime_information_set.year}"
    hour_string_formatted = f"{datatime_information_set.hour}{datatime_information_set.minute}"

    # Amount of overall messages sent by users on chat throughout the livestream
    messages_sent_by_users = 0

    # List containing words and nicknames that got caught by algorithm
    word_counter = {}
    nickname_list = {}

    # Holder for private data
    secrets_store = secrets_manager.get_secrets()

    def create_directory_to_file(channel_name, file_name):
        directory_path = f"output_data/{channel_name}/{data_pack_object.date_string_formatted}"
        os.makedirs(directory_path, exist_ok=True)

        # Construct the full path to the file, including the directory
        file_path = os.path.join(directory_path, file_name)

        return file_path
    
    @staticmethod
    def create_logger_path_location():
        directory_path = f"logs/"
        os.makedirs(directory_path, exist_ok=True)

        # Construct the full path to the file
        file_path = os.path.join(directory_path, "Logger.txt")

        return file_path
    
    def __init__(self):
        text_file_name = data_pack_object.channel_name + f"_Analysis_{data_pack_object.hour_string_formatted}_{data_pack_object.date_string_formatted}.txt"
        json_file_name = data_pack_object.channel_name + f"_Analysis_{data_pack_object.hour_string_formatted}_{data_pack_object.date_string_formatted}.json"
        
        data_pack_object.text_file_directory = data_pack_object.create_directory_to_file(data_pack_object.channel_name, text_file_name)
        data_pack_object.json_file_directory = data_pack_object.create_directory_to_file(data_pack_object.channel_name, json_file_name)
        
        pass
    
def return_data_pack():
    new_data_pack = data_pack_object()

    return new_data_pack
