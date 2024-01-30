# Chati_Py - Twitch Chat Analyzer

Chati_Py is a tool crafted to analyze Twitch chat interactions, offering profound insights into user engagement through comprehensive message frequency statistics.
The bot sorts the messages and users by most occurences on the chat by default, see the example of file below

This Python-based application leverages JSON and TXT files for seamless functionality.

## Libraries Utilized:

- `Datetime`
- `Sockets`
- `Requests`
- `JSON` and `.txt` Files
- Chati_Py Extensions (Optional) (TBA)

## Experimental Version Disclaimer

**[Experimental Version / BUGGY]**

Kindly note that the current version of Chati_Py may contain a few bugs as it's constantly under development. 

Rest assured, I am actively dedicated to addressing these issues and consistently implementing fixes on a daily basis. 

Your understanding and patience are sincerely appreciated as I pursue to elevate the stability and performance of Chati_Py.

## Data saved 

Example of .txt and json file:
{
    "Livestream Information": {
        "Date": "1-29-2024",
        "Timezone": "UTC",
        "Hour turned on": "1600",
        "Nickname on chat": "example_nickname_1",
        "Twitch Stream Link": "www.twitch.tv/{twitch_streamer_name}",
        "Messages sent overall": 28
    },
    "Nickname list": {
        "nightbot": 4,
        "user_one" : 3
        "user_three" : 1
    },
    "Messages list": {
        "message_one": 6,
        "message_two": 4,
        "aaaa": 1,
    }
}
