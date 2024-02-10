import pytz
import datetime
import os
import sys
import json
import secrets_manager
from datetime import datetime

secrets_manager.get_secrets()

# Channel name we're inspecting
channel = "#" + str(sys.argv[1])

# Acquiring information relating the data by using pytz and datetime
timezone = pytz.timezone('Europe/Warsaw')
datatime_information_set = datetime.now(timezone)

date_string_formatted = f"{datatime_information_set.month}-{datatime_information_set.day}-{datatime_information_set.year}"
hour_string_formatted = f"{datatime_information_set.hour};{datatime_information_set.minute}"


def create_directory_to_file(channel_name, file_name):
    directory_path = f"Data_Gathered/{channel_name}/{date_string_formatted}"
    os.makedirs(directory_path, exist_ok=True)

    # Construct the full path to the file, including the directory
    file_path = os.path.join(directory_path, file_name)

    return file_path


def update_text_data_file(user_list, message_list, message_count):
    global secrets_store

    channel_name = channel.replace("#","")
    new_file_name = channel_name + f"_Analysis_{hour_string_formatted}_{date_string_formatted}.txt"

    # Handle where file would go
    file_directory = create_directory_to_file(channel_name, new_file_name)
    file_handler = open(f"{file_directory}","w")

    file_text_content = f"""
        {channel_name} live stream information for:

        -------------------------------------------------------------
        | Date:                     {date_string_formatted}   
        | Hour turned on:           {hour_string_formatted} UTC
        | Nickname on chat:         {secrets_manager.secrets_store["account_nickname"]}              
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
    file_handler.write(file_text_content)
    file_handler.close()


def update_json_data_file(user_list, message_list, message_count):
    global secrets_store
    
    channel_name = channel.replace("#","")
    channel_link = "www.twitch.tv/" + channel_name

    file_name = channel_name + f"_Analysis_{hour_string_formatted}_{date_string_formatted}.txt"

    # Handle where file would go
    file_directory = create_directory_to_file(channel_name, file_name)
    file_handler = open(f"{file_directory}","w")

    # Basic content of JSON file, 
    file_text_content = {
        "Livestream Information": {
            "Date": date_string_formatted,
            "Timezone": "UTC",
            "Hour turned on": hour_string_formatted, 
            "Nickname on chat": secrets_manager.secrets_store["account_nickname"],
            "Twitch Stream Link": channel_link,
            "Messages sent overall": message_count
        },
        "Nickname list": user_list,
        "Messages list": message_list
    }

    # Input it to the file, close it
    json_object = json.dumps(file_text_content, indent=4)
    file_handler.write(json_object)