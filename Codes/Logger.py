import file_handlers
import os

# Special File Handler for Logger
def create_logger_path_location(logger_file_name):
    directory_path = f"Error_logs/"
    os.makedirs(directory_path, exist_ok=True)

#   Construct the full path to the file, including the directory
    file_path = os.path.join(directory_path, logger_file_name)

    return file_path


# Error Logger
def handle_logs(error_type, error_name, function_name, file_name,  user_message):
    file_directory = create_logger_path_location("Logger.txt")
    file_handler = open(f"{file_directory}","w")

    error_log = f"""
        --- Error Log ---

            Date of error occurrence:    {file_handler.date_string_formatted}
            Error Type:                  {error_type}
            Error:                       {error_name}
            Module:                      {file_name}
            Function:                    {function_name}

        --- Additional Details ---
            Channel:                     {file_handlers.channel}
            Message inputted:            {user_message}
"""

    file_handler.write(error_log)
    file_handler.close()


# Info Logger
def handle_logs(error_type, error_message):
    file_directory = create_logger_path_location("Logger.txt")
    file_handler = open(f"{file_directory}","w")

    error_log = f"""{file_handlers.date_string_formatted} {file_handlers.datatime_information_set.hour}:{file_handlers.datatime_information_set.minute} - {error_type} - {error_message}"""

    file_handler.write(error_log)
    file_handler.close()