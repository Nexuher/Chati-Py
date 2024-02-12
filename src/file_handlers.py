import json
import data_pack

# Acquiring information relating the data by using pytz and datetime
data_package = data_pack.return_data_pack()

def update_text_data_file(user_list, message_list, message_count):
    file_handler = open(f"{data_package.text_file_directory}","w")

    file_text_content = f"""
        {data_package.channel_name} live stream information for:

        -------------------------------------------------------------
        | Date:                     {data_package.date_string_formatted}   
        | Hour turned on:           {data_package.hour_string_formatted} UTC
        | Nickname on chat:         {data_package.secrets_store["account_nickname"]}              
        | Twitch_stream_link:       www.twitch.tv/{data_package.channel_name}    
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
    channel_link = "www.twitch.tv/" + data_package.channel_name

    # Handle where file would go
    file_handler = open(f"{data_package.json_file_directory}","w")

    # Basic content of JSON file, 
    file_text_content = {
        "Livestream Information": {
            "Date": data_package.date_string_formatted,
            "Timezone": "UTC",
            "Hour turned on": data_package.hour_string_formatted, 
            "Nickname on chat": data_package.secrets_store["account_nickname"],
            "Twitch Stream Link": channel_link,
            "Messages sent overall": message_count
        },
        "Nickname list": user_list,
        "Messages list": message_list
    }

    # Input it to the file, close it
    json_object = json.dumps(file_text_content, indent=4)
    file_handler.write(json_object)